"""
=====================
NWM File Client Tools
=====================
Client tools for retrieving National Water Model data from file-based sources

Classes
-------
NWMFileClient
"""

from .NWMClient import NWMClient, QueryError, StoreNotFoundError
from typing import Union, List
from pathlib import Path
from .NWMClientDefaults import _NWMClientDefault
from .ParquetStore import ParquetStore
from .NWMFileCatalog import NWMFileCatalog
import numpy as np
import pandas as pd
import xarray as xr
import ssl
import dask.dataframe as dd
from .FileDownloader import FileDownloader
from .NWMFileProcessor import NWMFileProcessor
import numpy.typing as npt
import warnings
from shutil import rmtree

class NWMFileClient(NWMClient):
    def __init__(
        self,
        file_directory: Union[str, Path] = "NWMFileClient_NetCDF_files",
        dataframe_store: Union[ParquetStore, None] = _NWMClientDefault.STORE,
        catalog: NWMFileCatalog = _NWMClientDefault.CATALOG,
        location_metadata_mapping: pd.DataFrame = _NWMClientDefault.CROSSWALK,
        ssl_context: ssl.SSLContext = _NWMClientDefault.SSL_CONTEXT,
        cleanup_files: bool = False,
        unit_system: str = "SI"
        ) -> None:
        """Client class for retrieving data as dataframes from a remote 
        file-based source of National Water Model data.

        Parameters
        ----------
        file_directory: str or pathlib.Path, optional, default None
            Directory to save downloaded NetCDF files. If None, will use 
            temporary files.
        dataframe_store: ParquetStore, default ParquetStore("nwm_store.parquet")
            Local parquet directory used to locally store retrieved dataframes.
        catalog: NWMFileCatalog, optional, default GCPFileCatalog()
            NWMFileCatalog object used to discover NWM files.
        location_metadata_mapping: pandas.DataFrame with nwm_feature_id Index and
            columns of corresponding site metadata. Defaults to 7500+ usgs_site_code
            used by the NWM for data assimilation.
        ssl_context: ssl.SSLContext, optional, default context
            SSL configuration context.
        cleanup_files: bool, default True
            Delete downloaded NetCDF files upon program exit.

        Returns
        -------
        NWMClient object
        """
        super().__init__()

        # Set file output directory
        self.file_directory = file_directory

        # Set dataframe store
        if dataframe_store:
            self.dataframe_store = dataframe_store
        else:
            self.dataframe_store = None

        # Set file catalog
        self.catalog = catalog

        # Set crosswalk
        self.crosswalk = location_metadata_mapping

        # Set CA bundle
        self.ssl_context = ssl_context

        # Set cleanup flag
        self.cleanup_files = cleanup_files

    def get_dataset(
        self,
        configuration: str,
        reference_time: pd.Timestamp,
        nwm_feature_ids: npt.ArrayLike = _NWMClientDefault.CROSSWALK.index,
        variables: List[str] = _NWMClientDefault.VARIABLES
        ) -> xr.Dataset:
        """Retrieve a single National Water Model cycle as an xarray.Dataset
        
        Parameters
        ----------
        configuration: str, required
            NWM configuration cycle.
        reference_time: datetime-like, required
            pandas.Timestamp compatible datetime object

        Returns
        -------
        xarray.Dataset of NWM data
        """
        # Generate list of urls
        urls = self.catalog.list_blobs(
            configuration=configuration,
            reference_time=reference_time
        )

        # Check urls
        if len(urls) == 0:
            message = (f"No data found for configuration '{configuration}' and " +
                f"reference time '{reference_time}'")
            raise QueryError(message)

        # Generate local filenames
        filenames = [f"part_{idx}.nc" for idx, _ in enumerate(urls)]

        # Output subdirectory
        subdirectory = self.file_directory / configuration / reference_time.strftime("RT%Y%m%dT%HZ")

        # Setup downloader
        downloader = FileDownloader(
            output_directory=subdirectory,
            create_directory=True,
            ssl_context=self.ssl_context
            )

        # Download files
        downloader.get(zip(urls,filenames))

        # Get dataset
        return NWMFileProcessor.get_dataset(
            input_directory=subdirectory,
            feature_id_filter=nwm_feature_ids,
            variables=variables
            )

    def get(
        self,
        configurations: List[str],
        reference_times: npt.ArrayLike,
        nwm_feature_ids: npt.ArrayLike = _NWMClientDefault.CROSSWALK.index,
        variables: List[str] = _NWMClientDefault.VARIABLES,
        compute: bool = True
        ) -> Union[pd.DataFrame, dd.DataFrame]:
        """Abstract method to retrieve National Water Model data as a 
        DataFrame.
        
        Parameters
        ----------
        configurations: List[str], required
            List of NWM configurations.
        reference_times: array-like, required
            array-like of reference times. Should be compatible with pandas.Timestamp.
        variables: List[str], optional, default ['streamflow']
            List of variables to retrieve from NWM files.
        nwm_feature_ids: array-like, optional
            array-like of NWM feature IDs to return. Defaults to channel features 
            with a known USGS mapping.
        compute: bool, optional, default True
            Return a pandas.DataFrame instead of a dask.dataframe.DataFrame.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data or a pandas.DataFrame in canonical 
        format.
        """
        # Check store
        if not self.dataframe_store:
            raise StoreNotFoundError("get requires a dataframe store")
        
        # Validate reference times
        reference_times = [pd.Timestamp(rft) for rft in reference_times]

        # Put features in array
        nwm_feature_ids = np.array(nwm_feature_ids)

        # Collect dataframes
        dfs = []
        open_datasets = {}
        for cfg in configurations:
            for rft in reference_times:
                # Build datetime string
                rft_str = rft.strftime("%Y%m%dT%HZ")

                # Retrieve or build and store dataframes
                for var in variables:
                    # Generate key
                    key = f"{cfg}_{rft_str}_{var}"

                    # Check store
                    if key in self.dataframe_store:
                        # Load data
                        df = self.dataframe_store[key]

                        # Check for features
                        missing = ~np.isin(nwm_feature_ids, df["nwm_feature_id"].compute())
                        missing_ids = nwm_feature_ids[missing]

                        # Load
                        dfs.append(df[df["nwm_feature_id"].isin(nwm_feature_ids)])

                        # If no IDs are missing, continue
                        if not np.any(missing):
                            continue
                    else:
                        missing_ids = nwm_feature_ids

                    # Open dataset
                    if f"{cfg}_{rft_str}" not in open_datasets:
                        # Open dataset for later retrieval
                        open_datasets[f"{cfg}_{rft_str}"] = self.get_dataset(cfg, rft, missing_ids, ["reference_time"]+variables)

                    # Process data
                    ds = open_datasets[f"{cfg}_{rft_str}"]

                    # Warn for no features
                    if ds.feature_id.size == 0:
                        message = f"These filter IDs returned no data: {missing_ids}"
                        warnings.warn(message)
                        continue

                    # Convert to dask
                    df = NWMFileProcessor.convert_to_dask_dataframe(ds)
                    
                    # Canonicalize
                    df = df[["reference_time", "feature_id", "time", var]].rename(columns={
                        "feature_id": "nwm_feature_id",
                        "time": "value_time",
                        var: "value"
                    })

                    # Add required columns
                    df["measurement_unit"] = ds[var].attrs["units"]
                    df["variable_name"] = var
                    df["configuration"] = ds.attrs["model_configuration"]

                    # Address ambigious "No-DA" cycle names
                    if cfg.endswith("no_da"):
                        df["configuration"] = df["configuration"] + "_no_da"
                        
                    # Map crosswalk
                    for col in self.crosswalk:
                        df[col] = df["nwm_feature_id"].map(self.crosswalk[col])

                    # Save
                    self.dataframe_store.append(key, df)

                    # Append
                    dfs.append(df[df["nwm_feature_id"].isin(nwm_feature_ids)])

        # Close datasets
        for _, ds in open_datasets.items():
            ds.close()

        # Check for empty data
        if not dfs:
            message = (
                f"Query returned no data for configurations {configurations}\n" + 
                f"reference_times {reference_times}\n" + 
                f"variables {variables}\n" + 
                f"nwm_feature_ids {nwm_feature_ids}\n"
                )
            raise QueryError(message)

        # Clean-up NetCDF files
        if self.cleanup_files:
            # Remove top directory
            try:
                rmtree(self.file_directory)
            except OSError as e:
                warnings.warn(str(e), RuntimeWarning)

        # Return pandas.DataFrame
        if compute:
            # Convert to pandas
            df = dd.multi.concat(dfs).compute()

            # Optimize memory
            df["nwm_feature_id"] = pd.to_numeric(df["nwm_feature_id"], downcast="integer")
            df["value"] = pd.to_numeric(df["value"], downcast="float")
            for cat in ["measurement_unit", "usgs_site_code", "variable_name", "configuration"]:
                df[cat] = df[cat].astype("category")

            # Reset to unique index
            return df.reset_index(drop=True)

        # Return dask dataframe
        return dd.multi.concat(dfs)

    @property
    def file_directory(self) -> Path:
        return self._file_directory

    @file_directory.setter
    def file_directory(self, file_directory: Union[str, Path]) -> None:
        self._file_directory = Path(file_directory).expanduser().resolve()
        self._file_directory.mkdir(exist_ok=True, parents=True)

    @property
    def dataframe_store(self) -> ParquetStore:
        return self._dataframe_store

    @dataframe_store.setter
    def dataframe_store(self, 
        dataframe_store: Union[ParquetStore, None]) -> None:
        self._dataframe_store = dataframe_store

    @property
    def catalog(self) -> NWMFileCatalog:
        return self._catalog

    @catalog.setter
    def catalog(self, 
        catalog: NWMFileCatalog) -> None:
        self._catalog = catalog

    @property
    def crosswalk(self) -> pd.DataFrame:
        return self._crosswalk

    @crosswalk.setter
    def crosswalk(self, 
        crosswalk: pd.DataFrame) -> None:
        self._crosswalk = crosswalk

    @property
    def ssl_context(self) -> ssl.SSLContext:
        return self._ssl_context

    @ssl_context.setter
    def ssl_context(self, ssl_context: ssl.SSLContext) -> None:
        self._ssl_context = ssl_context

    @property
    def cleanup_files(self) -> bool:
        return self._cleanup_files

    @cleanup_files.setter
    def cleanup_files(self, cleanup_files: bool) -> None:
        self._cleanup_files = cleanup_files

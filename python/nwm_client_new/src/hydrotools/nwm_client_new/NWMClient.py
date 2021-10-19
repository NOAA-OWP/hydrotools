"""
================
NWM Client Tools
================
Client tools for retrieving National Water Model data from various sources.

Classes
-------
NWMClient
NWMFileClient
"""

from abc import ABC, abstractmethod
import pandas as pd
import dask.dataframe as dd
from typing import List, Union
from pathlib import Path
from dataclasses import dataclass
import ssl
import shutil

from .ParquetCache import ParquetCache
from .FileDownloader import FileDownloader
from .NWMFileProcessor import NWMFileProcessor
from .NWMFileCatalog import NWMFileCatalog, GCPFileCatalog

@dataclass
class NWMClientDefaults:
    """Stores application default options."""
    CROSSWALK: pd.DataFrame = None
    CACHE: ParquetCache = ParquetCache(
        "nwm_cache.parquet",
        write_index=False,
        compression="snappy"
    )
    CATALOG: NWMFileCatalog = GCPFileCatalog()
    CANONICAL_COLUMN_MAPPING: pd.Series = pd.Series({
        "feature_id": "nwm_feature_id",
        "time": "value_time",
        "streamflow": "value"
    })
    SSL_CONTEXT: ssl.SSLContext = ssl.create_default_context()
    def __post_init__(self):
        # Gather routelink files
        rl_filepath = Path(__file__).parent / "data/routelink_files"
        rl_files = rl_filepath.glob("*.csv")

        # Generate crosswalk
        dfs = []
        for rl_file in rl_files:
            dfs.append(pd.read_csv(
            rl_file,
            dtype={"nwm_feature_id": int, "usgs_site_code": str},
            comment='#'
        ).set_index('nwm_feature_id')[['usgs_site_code']])
        self.CROSSWALK = pd.concat(dfs)
_NWMClientDefault = NWMClientDefaults()

class NWMClient(ABC):
    
    @abstractmethod
    def get(
        self,
        configuration: str,
        reference_times: List[str],
        compute: bool = True
        ) -> Union[pd.DataFrame, dd.DataFrame]:
        """Abstract method to retrieve National Water Model data as a 
        DataFrame.
        
        Parameters
        ----------
        configuration: str, required
            NWM configuration cycle.
        reference_times: List[str], required
            List of reference time strings in %Y%m%dT%HZ format. 
            e.g. ['20210912T01Z']
        compute: bool, optional, default True
            Return a pandas.DataFrame instead of a dask.dataframe.DataFrame.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data or a pandas.DataFrame in canonical 
        format.
        """

    @classmethod
    def canonicalize_dataframe(
        cls,
        df: dd.DataFrame,
        configuration: str,
        column_mapping: pd.Series = _NWMClientDefault.CANONICAL_COLUMN_MAPPING,
        variable_name: str = "streamflow",
        measurement_unit: str = "m3/s",
        location_metadata_mapping: pd.DataFrame = _NWMClientDefault.CROSSWALK
        ) -> dd.DataFrame:
        """Reformat dask.dataframe.DataFrame to adhere to HydroTools canonical 
        format.
        
        Parameters
        ----------
        df: dask.dataframe.DataFrame, required
            Input dataframe to transform.
        configuration: str, required
            NWM configuration label used for "configuration" column values
        column_mapping: dict, optional
            Mapping used to rename columns. See NWMClientDefault for default 
            values
        variable_name: str, optional
            Variable name used for "variable_name" column values
        measurement_unit: str, optional
            Measurement unit used for "measurment_unit" column values
        location_metadata_mapping : pandas.DataFrame with nwm_feature_id Index and
            columns of corresponding site metadata. Defaults to 7500+ usgs_site_code
            used by the NWM for data assimilation

        Returns
        -------
        dask.dataframe.DataFrame in canonical format
        """
        # Rename columns
        df = df.rename(columns=column_mapping)

        # Add new columns
        df["configuration"] = configuration
        df["variable_name"] = variable_name
        df["measurement_unit"] = measurement_unit

        # Categorize columns
        df["configuration"] = df["configuration"].astype("category")
        df["variable_name"] = df["variable_name"].astype("category")
        df["measurement_unit"] = df["measurement_unit"].astype("category")

        # Apply crosswalk
        for col in location_metadata_mapping:
            df[col] = df['nwm_feature_id'].map(location_metadata_mapping[col]).astype("category")

        return df

class NWMFileClient(NWMClient):
    def __init__(
        self,
        file_directory: Union[str, Path] = "NWMFileClient_NetCDF_files",
        dataframe_cache: Union[ParquetCache, None] = _NWMClientDefault.CACHE,
        catalog: NWMFileCatalog = _NWMClientDefault.CATALOG,
        location_metadata_mapping: pd.DataFrame = _NWMClientDefault.CROSSWALK,
        ssl_context: ssl.SSLContext = _NWMClientDefault.SSL_CONTEXT,
        cleanup_files: bool = True
        ) -> None:
        """Client class for retrieving data as dataframes from a remote 
        file-based source of National Water Model data.

        Parameters
        ----------
        file_directory: str or pathlib.Path, optional, default None
            Directory to save downloaded NetCDF files. If None, will use 
            temporary files.
        dataframe_cache: ParquetCache, default ParquetCache("nwm_cache.parquet")
            Local parquet directory used to locally cache retrieved dataframes.
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

        # Set dataframe cache
        if dataframe_cache:
            self.dataframe_cache = dataframe_cache
        else:
            self._dataframe_cache = None

        # Set file catalog
        self.catalog = catalog

        # Set crosswalk
        self.crosswalk = location_metadata_mapping

        # Set CA bundle
        self.ssl_context = ssl_context

        # Set cleanup flag
        self.cleanup_files = cleanup_files

    def get_cycle(
        self,
        configuration: str,
        reference_time: str,
        netcdf_dir: Union[str, Path]
        ) -> dd.DataFrame:
        """Retrieve a single National Water Model cycle as a 
        dask.dataframe.DataFrame.
        
        Parameters
        ----------
        configuration: str, required
            NWM configuration cycle.
        reference_time: str, required
            Reference time string in %Y%m%dT%HZ format. 
            e.g. '20210912T01Z'
        netcdf_dir: str or pathlib.Path, required
            Directory to save downloaded NetCDF files.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data
        """
        # Generate list of urls
        urls = self.catalog.list_blobs(
            configuration=configuration,
            reference_time=reference_time
        )

        # Setup downloader
        downloader = FileDownloader(
            output_directory=netcdf_dir,
            create_directory=True,
            ssl_context=self.ssl_context
            )

        # Download files
        downloader.get(urls)

        # Get dataset
        ds = NWMFileProcessor.get_dataset(
            input_directory=netcdf_dir,
            feature_id_filter=self.crosswalk.index
            )

        # Convert to dataframe
        df = NWMFileProcessor.convert_to_dask_dataframe(ds)

        # Canonicalize
        return NWMClient.canonicalize_dataframe(
            df=df,
            configuration=configuration
        )

    def get(
        self,
        configuration: str,
        reference_times: List[str] = None,
        compute: bool = True
        ) -> Union[pd.DataFrame, dd.DataFrame]:
        """Retrieve National Water Model data as a DataFrame.
        
        Parameters
        ----------
        configuration: str, required
            NWM configuration cycle.
        reference_times: List[str], optional, default None
            List of reference time strings in %Y%m%dT%HZ format. 
            e.g. ['20210912T01Z',]
        compute: bool, optional, default True
            Return a pandas.DataFrame instead of a dask.dataframe.DataFrame.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data or a pandas.DataFrame in canonical 
        format.
        """
        # List of individual parquet files
        parquet_files = []

        # Cache data
        for reference_time in reference_times:
            # Set subdirectory
            subdirectory = f"{configuration}/RT{reference_time}"

            # Set download directory
            netcdf_dir = self.file_directory / subdirectory

            # Get dask dataframe
            df = self.dataframe_cache.get(
                function=self.get_cycle,
                subdirectory=subdirectory,
                configuration=configuration,
                reference_time=reference_time,
                netcdf_dir=netcdf_dir
            )

            # Note file created
            parquet_files.append(self.dataframe_cache.directory/subdirectory)

        # Clean-up NetCDF files
        shutil.rmtree(self.file_directory)

        # Limit to canonical columns
        # NOTE I could not keep dask from adding a "dir0" column using either
        #  fastparquet or pyarrow as backends
        #  A future version of dask or the backends may fix this
        columns = [
            'nwm_feature_id',
            'reference_time',
            'value_time',
            'value',
            'configuration',
            'variable_name',
            'measurement_unit',
            'usgs_site_code'
            ]

        # Return all reference times
        df = dd.read_parquet(parquet_files, columns=columns)
        
        # Return pandas dataframe
        if compute:
            # Compute
            df = df.compute()

            # Downcast
            df["value"] = pd.to_numeric(df["value"], downcast="float")
            df["nwm_feature_id"] = pd.to_numeric(df["nwm_feature_id"], downcast="integer")
            return df
        return df

    @property
    def file_directory(self) -> Path:
        return self._file_directory

    @file_directory.setter
    def file_directory(self, file_directory: Union[str, Path]) -> None:
        self._file_directory = Path(file_directory).expanduser().resolve()
        self._file_directory.mkdir(exist_ok=True, parents=True)

    @property
    def dataframe_cache(self) -> ParquetCache:
        return self._dataframe_cache

    @dataframe_cache.setter
    def dataframe_cache(self, 
        dataframe_cache: Union[ParquetCache, None]) -> None:
        self._dataframe_cache = dataframe_cache

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

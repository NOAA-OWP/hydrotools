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
from pandas.io import parquet
import dask.dataframe as dd
from typing import List, Union
from pathlib import Path
import tempfile
from dataclasses import dataclass

from .ParquetCache import ParquetCache
from .FileDownloader import FileDownloader
from .NWMFileProcessor import NWMFileProcessor
from .NWMFileCatalog import NWMFileCatalog, GCPFileCatalog

@dataclass
class NWMClientDefault:
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

class NWMClient(ABC):
    
    @abstractmethod
    def get(
        self,
        configuration: str,
        reference_times: List[str] = None,
        compute: bool = True
        ) -> Union[pd.DataFrame, dd.DataFrame]:
        """Abstract method to retrieve National Water Model data as a 
        DataFrame.
        
        Parameters
        ----------
        configuration: str, required
            NWM configuration cycle.
        reference_times: str or List[str], optional, default None
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
        column_mapping: pd.Series = NWMClientDefault.CANONICAL_COLUMN_MAPPING,
        variable_name: str = "streamflow",
        measurement_unit: str = "m3/s",
        location_metadata_mapping: pd.DataFrame = NWMClientDefault().CROSSWALK
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
        file_directory: Union[str, Path] = None,
        dataframe_cache: Union[ParquetCache, None] = NWMClientDefault.CACHE,
        catalog: NWMFileCatalog = NWMClientDefault.CATALOG,
        location_metadata_mapping: pd.DataFrame = NWMClientDefault().CROSSWALK,
        verify: str = None
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
        location_metadata_mapping : pandas.DataFrame with nwm_feature_id Index and
            columns of corresponding site metadata. Defaults to 7500+ usgs_site_code
            used by the NWM for data assimilation.
        verify: str, optional, default None
            Path to CA bundle for https verification.

        Returns
        -------
        NWMClient object
        """
        super().__init__()

        # Set file output directory
        if file_directory:
            self.__temp_dir = None
            self.file_directory = file_directory
        else:
            self.__temp_dir = tempfile.TemporaryDirectory()
            self.file_directory = self.__temp_dir.name

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
        self.verify = verify

    def __del__(self) -> None:
        # Clean up
        if self.__temp_dir:
            self.__temp_dir.cleanup()

    def get_cycle(
        self,
        configuration: str,
        reference_time: str
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

        Returns
        -------
        dask.dataframe.DataFrame of NWM data
        """
        # Generate list of urls
        urls = self.catalog.list_blobs(
            configuration=configuration,
            reference_time=reference_time
        )

        # Set subdirectory
        subdirectory = self.file_directory / f"RT{reference_time}"

        # Set download directory
        downloader = FileDownloader(
            output_directory=subdirectory,
            create_directory=True,
            verify=self.verify
            )

        # Download files
        downloader.get(urls)

        # Get dataset
        ds = NWMFileProcessor.get_dataset(
            input_directory=subdirectory,
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
        reference_times: str or List[str], optional, default None
            List of reference time strings in %Y%m%dT%HZ format. 
            e.g. ['20210912T01Z']
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

            # Get dask dataframe
            df = self.dataframe_cache.get(
                function=self.get_cycle,
                subdirectory=subdirectory,
                configuration=configuration,
                reference_time=reference_time
            )

            # Note file created
            parquet_files.append(self.dataframe_cache.directory/subdirectory)

        # Return all data
        df = dd.read_parquet(parquet_files)
        
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
    def verify(self) -> str:
        return self._verify

    @verify.setter
    def verify(self, 
        verify: str) -> None:
        self._verify = verify

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
    DOWNLOADER: FileDownloader = FileDownloader()
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
        startRT: str = None,
        endRT: str = None,
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
        startRT: str, optional
            Retrieve all available cycles starting with this reference time. 
            If endRT is not set, then retrieve from startRT until now.
        endRT: str, optional
            Used with startRT. Sets the final reference time to retrieve.
        compute: bool, optional, default True
            Return a pandas.DataFrame instead of a dask.dataframe.DataFrame.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data or a pandas.DataFrame in canonical 
        format.
        """

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
        verify: str, optional, default None
            Path to CA bundle for https verification.

        Returns
        -------
        NWMClient object
        """
        super().__init__()

        # Set file output directory
        if file_directory:
            self.file_directory = file_directory
        else:
            self._file_directory = None

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
        
    def get(
        self,
        configuration: str,
        reference_times: List[str] = None,
        startRT: str = None,
        endRT: str = None,
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
        startRT: str, optional
            Retrieve all available cycles starting with this reference time. 
            If endRT is not set, then retrieve from startRT until now.
        endRT: str, optional
            Used with startRT. Sets the final reference time to retrieve.
        compute: bool, optional, default True
            Return a pandas.DataFrame instead of a dask.dataframe.DataFrame.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data or a pandas.DataFrame in canonical 
        format.
        """

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

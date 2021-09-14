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

from .parquet_cache import ParquetCache
from .FileDownloader import FileDownloader
from .NWMFileProcessor import NWMFileProcessor
from .NWMFileCatalog import NWMFileCatalog, GCPFileCatalog

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
        dataframe_cache: Union[ParquetCache, None] = ParquetCache("nwm_cache.parquet"),
        catalog: NWMFileCatalog = GCPFileCatalog(),
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

        # Set CA bundle
        self.verify = verify

    def download_files(self, urls: List[str], directory: Path) -> None:
        """Download a list of urls to directory.

        Parameters
        ----------
        urls: List[str], required
            List of NWM NetCDF url strings.
        directory: pathlib.Path, required
            Path to directory where downloaded files are written.

        Returns
        -------
        None
        """
        # Download files
        downloader = FileDownloader(
            output_directory=directory,
            verify=self.verify
            )
        downloader.get(urls)

    def get_dask_dataframe(self, urls: List[str]) -> dd.DataFrame:
        """Download and merge a list of urls into a dask.dataframe.DataFrame.

        Parameters
        ----------
        urls: List[str], required
            List of NWM NetCDF url strings to download and combine.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data.
        """
        # Download files to non-temp directory
        if self.file_directory:
            self.download_files(urls, self.file_directory)
            return NWMFileProcessor.get_dask_dataframe(self.file_directory)
        
        # Download filed to temp directory
        with tempfile.TemporaryDirectory() as tdir:
            self.download_files(urls, tdir)
            return NWMFileProcessor.get_dask_dataframe(tdir)
    
    def get_cycle(
        self,
        configuration: str,
        reference_time: str
        ) -> dd.DataFrame:
        """Retrieve National Water Model data as a dask.dataframe.DataFrame 
        from a file-based data source for a single cycle.
        
        Parameters
        ----------
        configuration: str, required
            NWM configuration cycle.
        reference_time: str, required
            Reference time in %Y%m%dT%HZ format. e.g. '20210912T01Z'

        Returns
        -------
        dask.dataframe.DataFrame of NWM data.
        """
        # Get list of file URLs
        urls = self.catalog.list_blobs(
            configuration=configuration,
            reference_time=reference_time
            )

        # Download files and get a dask DataFrame
        if self.dataframe_cache:
            return self.dataframe_cache.get(
                self.get_dask_dataframe,
                f"{configuration}/RT{reference_time}",
                urls
            )
        return self.get_dask_dataframe(urls)
    
    def get(
        self,
        configuration: str,
        reference_times: List[str],
        startRT: str = None,
        endRT: str = None,
        compute: bool = True
        ) -> Union[pd.DataFrame, dd.DataFrame]:
        """Retrieve National Water Model data as a dask.dataframe.DataFrame 
        from a file-based data source.
        
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
        # Retrieve each cycle
        dfs = []
        for ref_time in reference_times:
            dfs.append(self.get_cycle(configuration, ref_time))

        # Concatenate cycles
        df = dd.multi.concat(dfs, ignore_unknown_divisions=True)

        # Return pandas.DataFrame
        if compute:
            return df.head() # FIXME Return head for testing
            return df.compute() # Enable this option
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
    def verify(self) -> str:
        return self._verify

    @verify.setter
    def verify(self, 
        verify: str) -> None:
        self._verify = verify

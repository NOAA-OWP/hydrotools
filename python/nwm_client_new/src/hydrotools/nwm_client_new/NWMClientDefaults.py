"""
===================
NWM Client Defaults
===================
Manages default options to build National Water Model clients.

Classes
-------
NWMClientDefaults
"""
from dataclasses import dataclass, field
import pandas as pd
from .ParquetStore import ParquetStore
from .NWMFileCatalog import NWMFileCatalog
from .GCPFileCatalog import GCPFileCatalog
import ssl
import dask.dataframe as dd
from tempfile import TemporaryDirectory
from .FileDownloader import FileDownloader
from pathlib import Path
from typing import List

@dataclass
class NWMClientDefaults:
    """Stores application default options.

    STORE: Configured ParquetStore instance.
    CATALOG: Concrete NWM data source instance.
    SSL_CONTEXT: ssl context instance.
    ROUTELINK_URL: URL string path that points at an HDF5 file containing a
        pandas.DataFrame with NWM crosswalk data.
    CROSSWALK: A property that generates a pandas.DataFrame that maps between 
        point feature data source identifiers (i.e. USGS gage id -> NWM feature 
        ID).
    DOWNLOAD_DIRECTORY: Local path to save downloaded NWM files.
    """
    STORE: ParquetStore = ParquetStore(
        "nwm_store.parquet",
        write_index=False,
        compression="snappy"
    )
    CATALOG: NWMFileCatalog = GCPFileCatalog()
    SSL_CONTEXT: ssl.SSLContext = ssl.create_default_context()
    ROUTELINK_URL: str = "https://www.hydroshare.org/resource/d154f19f762c4ee9b74be55f504325d3/data/contents/RouteLink.h5"
    VARIABLES: List[str] = field(default_factory=lambda: ["streamflow"])

    def _download_and_read_routelink_file(self) -> dd.DataFrame:
        """Retrieve NWM RouteLink data from URL and return a 
        dask.dataframe.DataFrame.
            
        Returns
        -------
        df: dask.dataframe.DataFrame
            DataFrame containing associated location metadata.
        """
        with TemporaryDirectory() as td:
            # Setup downloader
            downloader = FileDownloader(
                output_directory=td,
                create_directory=False,
                ssl_context=self.SSL_CONTEXT
                )

            # Download files
            downloader.get([(self.ROUTELINK_URL, "RouteLink.h5")])
            return dd.from_pandas(pd.read_hdf(Path(td)/"RouteLink.h5"), 
                npartitions=1)
    
    @property
    def CROSSWALK(self) -> pd.DataFrame:
        """Retrieve and store a default crosswalk for use by a NWM client."""
        key = "CROSSWALK"
        if key not in self.STORE:
            self.STORE[key] = self._download_and_read_routelink_file()
        return self.STORE[key].compute()[["nwm_feature_id", "usgs_site_code"]].set_index(
            "nwm_feature_id")

# Initialize defaults
_NWMClientDefault = NWMClientDefaults()

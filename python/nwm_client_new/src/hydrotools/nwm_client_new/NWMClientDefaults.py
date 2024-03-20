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
from .UnitHandler import UnitHandler
import ssl
import dask.dataframe as dd
from tempfile import TemporaryDirectory
from .FileDownloader import FileDownloader
from pathlib import Path
from typing import List, Dict
from enum import Enum

class MeasurementUnitSystem(Enum):
    """A system of units to define measurements.
    Options are SI or US.
    """
    SI = "SI"
    US = "US"

@dataclass
class NWMClientDefaults:
    """Stores application default options.

    STORE: Configured ParquetStore instance. Default is class level object, not instance object.
    CATALOG: Concrete NWM data source instance.
    SSL_CONTEXT: ssl context instance. Default is class level object, not instance object.
    ROUTELINK_URL: URL string path that points at an HDF5 file containing a
        pandas.DataFrame with NWM crosswalk data.
    VARIABLES: default list of variables to retrieve from channel_rt files.
    NWM_TO_SI_UNIT_MAPPING: mapping from NWM units to pint compatible metric unit symbols
    SI_TO_US_UNIT_MAPPING: mapping from SI units to default US standard conversion units
    CROSSWALK: A property that generates a pandas.DataFrame that maps between 
        point feature data source identifiers (i.e. USGS gage id -> NWM feature 
        ID).
    NWM_TO_US_UNIT_CONVERSION: Propertying mapping NWM units to US standard units and conversion factors
    DOWNLOAD_DIRECTORY: Local path to save downloaded NWM files. Default is class level object, not instance object.
    UNIT_SYSTEM: Default system of measurements.
    """
    STORE: ParquetStore = ParquetStore(
        "hydrotools_data/nwm_store.parquet",
        write_index=False,
        compression="snappy"
    )
    CATALOG: NWMFileCatalog = GCPFileCatalog()
    SSL_CONTEXT: ssl.SSLContext = ssl.create_default_context()
    ROUTELINK_URL: str = "https://www.hydroshare.org/resource/e9fe66730d184bdfbaea19639bd7cb55/data/contents/RouteLink.h5"
    VARIABLES: List[str] = field(default_factory=lambda: ["streamflow"])
    NWM_TO_SI_UNIT_MAPPING: Dict[str, str] = field(default_factory=lambda: {"m": "m", "m s-1": "m/s", "m3 s-1": "m^3/s"})
    SI_TO_US_UNIT_MAPPING: Dict[str, str] = field(default_factory=lambda: {"m": "ft", "m/s": "ft/s", "m^3/s": "ft^3/s"})
    DOWNLOAD_DIRECTORY: Path = Path("hydrotools_data/NWMFileClient_NetCDF_files")
    UNIT_SYSTEM: MeasurementUnitSystem = MeasurementUnitSystem.SI

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
    
    @property
    def NWM_TO_US_UNIT_CONVERSION(self) -> Dict[str, Dict[str, float]]:
        """Mapping from NWM units to US standard units and respective conversion factors."""
        # Set up unit handler
        unit_handler = UnitHandler()

        # Build conversion from NWM to US
        nwm_to_us_mapping = {key: self.SI_TO_US_UNIT_MAPPING[val] for key, val in self.NWM_TO_SI_UNIT_MAPPING.items()}
        si_to_us_conversion = {key: unit_handler.conversion_factor(key, val) for key, val in self.SI_TO_US_UNIT_MAPPING.items()}
        nwm_to_us_conversion = {key: si_to_us_conversion[val] for key, val in self.NWM_TO_SI_UNIT_MAPPING.items()}

        return {"measurement_unit_conversion": nwm_to_us_mapping, "conversion_factor": nwm_to_us_conversion}

# Initialize defaults
_NWMClientDefault = NWMClientDefaults()

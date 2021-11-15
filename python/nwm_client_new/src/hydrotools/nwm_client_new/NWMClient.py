"""
================
NWM Client Tools
================
Client tools for retrieving National Water Model data from various sources.

Classes
-------
NWMClient
"""

from abc import ABC, abstractmethod
import pandas as pd
import dask.dataframe as dd
from typing import List, Union
# from pathlib import Path
# from dataclasses import dataclass
# from tempfile import TemporaryDirectory
# import ssl
# import shutil
# from urllib.parse import unquote
# import warnings

# from .ParquetCache import ParquetCache
# from .FileDownloader import FileDownloader
# from .NWMFileProcessor import NWMFileProcessor
# from .NWMFileCatalog import NWMFileCatalog
# from .GCPFileCatalog import GCPFileCatalog
from .NWMClientDefaults import NWMClientDefaults

class CacheNotFoundError(Exception):
    """Exception raised for methods that require a cache."""
    pass

class QueryError(Exception):
    """Exception raised when a combination of configuration and/or reference 
    times does not return any results."""
    pass

# Initialize defaults
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
    def canonicalize_dask_dataframe(
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
            Measurement unit used for "measurement_unit" column values
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

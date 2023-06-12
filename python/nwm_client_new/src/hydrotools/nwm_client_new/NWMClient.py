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
import numpy.typing as npt
from .NWMClientDefaults import _NWMClientDefault

class StoreNotFoundError(Exception):
    """Exception raised by methods that require a dataframe store."""
    pass

class QueryError(Exception):
    """Exception raised when a combination of configuration and/or reference 
    times does not return any results."""
    pass

class NWMClient(ABC):
    """Abstract base class by building National Water Model output data clients."""
    
    @abstractmethod
    def get(
        self,
        configurations: List[str],
        reference_times: npt.ArrayLike,
        variables: List[str] = ["streamflow"],
        nwm_feature_ids: npt.ArrayLike = _NWMClientDefault.CROSSWALK.index,
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
            When True returns a pandas.DataFrame. When False returns a dask.dataframe.DataFrame.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data or a pandas.DataFrame in canonical 
        format.
        """

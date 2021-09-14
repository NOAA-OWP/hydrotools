"""
================
NWM Client Tools
================
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Union
from pathlib import Path

class NWMClient(ABC):
    
    @abstractmethod
    def get(
        self,
        configuration: str,
        reference_time: Union[str, List[str]] = None,
        startRT: str = None,
        endRT: str = None
        ) -> pd.DataFrame():
        """Abstract method to retrieve National Water Model data as a 
        pandas.DataFrame.
        
        Parameters
        ----------
        configuration: str, required
            NWM configuration cycle.
        reference_time: str or List[str], optional, default None
            Either a single reference time or a list of reference time strings 
            in %Y%m%dT%HZ format. E.g. 20210912T01Z
        startRT: str, optional
            Retrieve all available cycles starting with this reference time. 
            If endRT is not set, then retrieve from startRT until now.
        endRT: str, optional
            Used with startRT. Sets the final reference time to retrieve.

        Returns
        -------
        pandas.DataFrame of NWM data in hydrotools canonical format.
        """

class NWMFileClient(NWMClient):
    def __init__(
        self,
        file_directory: Union[str, Path] = None
        ) -> None:
        super().__init__()

        # Set file output directory
        if file_directory:
            self.file_directory = file_directory
        else:
            self._file_directory = None
    
    def get(
        self,
        configuration: str,
        reference_time: Union[str, List[str]] = None,
        startRT: str = None,
        endRT: str = None
        ) -> pd.DataFrame():
        """Retrieve National Water Model data as a pandas.DataFrame from a 
        file-based data source.
        
        Parameters
        ----------
        configuration: str, required
            NWM configuration cycle.
        reference_time: str or List[str], optional, default None
            Either a single reference time or a list of reference time strings 
            in %Y%m%dT%HZ format. E.g. 20210912T01Z
        startRT: str, optional
            Retrieve all available cycles starting with this reference time. 
            If endRT is not set, then retrieve from startRT until now.
        endRT: str, optional
            Used with startRT. Sets the final reference time to retrieve.

        Returns
        -------
        pandas.DataFrame of NWM data in hydrotools canonical format.
        """

    @property
    def file_directory(self) -> Path:
        return self._file_directory

    @file_directory.setter
    def file_directory(self, file_directory: Union[str, Path]) -> None:
        self._file_directory = Path(file_directory).expanduser().resolve()
        

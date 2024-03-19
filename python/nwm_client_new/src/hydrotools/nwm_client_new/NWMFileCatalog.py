"""
================
NWM File Catalog
================
Tools for discovering operational NWM NetCDF data from file-based sources.

Classes
-------
NWMFileCatalog
"""
from abc import ABC, abstractmethod
from typing import List, Tuple
import pandas as pd

class NWMFileCatalog(ABC):
    """Abstract base class for sources of NWM file data."""

    def raise_invalid_configuration(self, configuration) -> None:
        """Raises an error for an invalid configuration.

        Parameters
        ----------
        configuration: str, required
            Configuration to validate

        Returns
        -------
        None

        Raises
        ------
        ValueError if the configuration is invalid.
        """
        # Validate configuration
        if configuration not in self.configurations:
            message = (f"Invalid configuration '{configuration}'. " + 
                f"Valid options: {str(self.configurations)}")
            raise ValueError(message)

    @staticmethod
    def separate_datetime(reference_time: pd.Timestamp) -> Tuple[str, str]:
        """Divide reference time into separate date and time strings.

        Parameters
        ----------
        reference_time: pandas.Timestamp, required
            pandas.Timestamp compatible datetime object

        Returns
        -------
        Two strings: issue_date, issue_time
        """
        # Break-up reference time
        tokens = reference_time.strftime("%Y%m%dT%HZ").split('T')
        issue_date = tokens[0]
        issue_time = tokens[1].lower()
        return issue_date, issue_time

    @abstractmethod
    def list_blobs(
        self,
        configuration: str,
        reference_time: str
        ) -> List[str]:
        """Abstract method to query for NWM files.

        Parameters
        ----------
        configuration : str, required
            Particular model simulation or forecast configuration. For a list 
            of available configurations see NWMDataService.configurations
        reference_time : str, required
            Model simulation or forecast issuance/reference time in 
            %Y%m%dT%HZ format.

        Returns
        -------
        A list of blob names that satisfy the criteria set by the parameters.
        """

    @property
    def configurations(self) -> List[str]:
        return [
            'analysis_assim',
            'analysis_assim_alaska',
            'analysis_assim_alaska_no_da',
            'analysis_assim_extend',
            'analysis_assim_extend_no_da',
            'analysis_assim_extend_alaska',
            'analysis_assim_extend_alaska_no_da',
            'analysis_assim_hawaii',
            'analysis_assim_hawaii_no_da',
            'analysis_assim_no_da',
            'analysis_assim_puertorico',
            'analysis_assim_puertorico_no_da',
            'analysis_assim_long',
            'analysis_assim_long_no_da',
            'long_range_mem1',
            'long_range_mem2',
            'long_range_mem3',
            'long_range_mem4',
            'medium_range_alaska_mem1',
            'medium_range_alaska_mem2',
            'medium_range_alaska_mem3',
            'medium_range_alaska_mem4',
            'medium_range_alaska_mem5',
            'medium_range_alaska_mem6',
            'medium_range_alaska_no_da',
            'medium_range_mem1',
            'medium_range_mem2',
            'medium_range_mem3',
            'medium_range_mem4',
            'medium_range_mem5',
            'medium_range_mem6',
            'medium_range_mem7',
            'medium_range_no_da',
            'short_range',
            'short_range_alaska',
            'short_range_hawaii',
            'short_range_hawaii_no_da',
            'short_range_puertorico',
            'short_range_puertorico_no_da',
            ]

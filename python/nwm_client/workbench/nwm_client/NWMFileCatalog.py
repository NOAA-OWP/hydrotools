"""
===============
NWM File Source
===============
Tools for discovering operational NWM NetCDF data.

Classes
-------
NWMFileSource
HTTPFileSource
GCPFileSource
"""
from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from typing import List, Tuple
import asyncio
import aiohttp
import ssl
from bs4 import BeautifulSoup

class NWMFileSource(ABC):
    """Abstract base class for sources of NWM file data."""

    def __init__(
        self,
        location_metadata_mapping: pd.DataFrame = pd.DataFrame()
        ) -> None:
        super().__init__()

        # Set crosswalk
        self.crosswalk = location_metadata_mapping

        # Check for empty crosswalk
        if self.crosswalk.empty:
            # Use default routelink files
            default_path = (Path(__file__).resolve().parent / 
                "data/routelink_files")

            # List routelink files
            routelink_files = default_path.glob("*.csv")

            # Generate crosswalk
            dfs = []
            for file in routelink_files:
                dfs.append(pd.read_csv(
                file,
                dtype={"nwm_feature_id": int, "usgs_site_code": str},
                comment='#'
            ).set_index('nwm_feature_id')[['usgs_site_code']])
            self.crosswalk = pd.concat(dfs)

    def raise_invalid_configuration(self, configuration) -> None:
        """Raises an error for an invalid configuration."""
        # Validate configuration
        if configuration not in self.configurations:
            message = (f"Invalid configuration '{configuration}'. " + 
                f"Valid options: {str(self.configurations)}")
            raise ValueError(message)

    @classmethod
    def separate_datetime(cls, reference_time: str) -> Tuple[str, str]:
        """Divide reference time into separate date and time strings."""
        # Break-up reference time
        tokens = reference_time.split('T')
        issue_date = tokens[0]
        issue_time = tokens[1].lower()
        return issue_date, issue_time

    @abstractmethod
    def list_blobs(self):
        """Abstract method to query for NWM files."""

    @property
    def crosswalk(self) -> pd.DataFrame:
        return self._crosswalk

    @crosswalk.setter
    def crosswalk(self, crosswalk: pd.DataFrame) -> None:
        self._crosswalk = crosswalk

    @property
    def configurations(self) -> List[str]:
        return [
            'analysis_assim',
            'analysis_assim_extend',
            'analysis_assim_hawaii',
            'analysis_assim_long',
            'analysis_assim_puertorico',
            'long_range_mem1',
            'long_range_mem2',
            'long_range_mem3',
            'long_range_mem4',
            'medium_range_mem1',
            'medium_range_mem2',
            'medium_range_mem3',
            'medium_range_mem4',
            'medium_range_mem5',
            'medium_range_mem6',
            'medium_range_mem7',
            'short_range',
            'short_range_hawaii',
            'short_range_puertorico',
            'analysis_assim_no_da',
            'analysis_assim_extend_no_da',
            'analysis_assim_hawaii_no_da',
            'analysis_assim_long_no_da',
            'analysis_assim_puertorico_no_da',
            'medium_range_no_da',
            'short_range_hawaii_no_da',
            'short_range_puertorico_no_da'
            ]

class HTTPFileSource(NWMFileSource):

    def __init__(
        self,
        server: str,
        verify: str = None,
        location_metadata_mapping: pd.DataFrame = pd.DataFrame(),
        ) -> None:
        super().__init__(location_metadata_mapping=location_metadata_mapping)
        self.server = server
        self.verify = verify

    @classmethod
    async def get_html(cls, url, verify):
        # SSL
        if verify:
            ssl_context = ssl.create_default_context(
                purpose=ssl.Purpose.SERVER_AUTH, 
                cafile=verify)
        else:
            ssl_context = ssl.create_default_context()

        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=ssl_context) as response:
                # Get html content
                html_doc = await response.text()

                # Raise for no results found
                if response.status >= 400:
                    raise FileNotFoundError(html_doc)

                # Otherwise return response content
                return html_doc

    def list_blobs(
        self,
        configuration: str,
        reference_time: str,
        must_contain: str = 'channel_rt'
        ) -> List[str]:
        """List available blobs with provided parameters.

        Parameters
        ----------
        configuration : str, required
            Particular model simulation or forecast configuration. For a list 
            of available configurations see NWMDataService.configurations
        reference_time : str, required
            Model simulation or forecast issuance/reference time in 
            YYYYmmddTHHZ format.
        must_contain : str, optional, default 'channel_rt'
            Optional substring found in each blob name.

        Returns
        -------
        blob_list : list
            A list of blob names that satisfy the criteria set by the
            parameters.

        Examples
        --------
        >>> from hydrotools.nwm_client import http as nwm
        >>> model_data_service = nwm.NWMDataService()
        >>> blob_list = model_data_service.list_blobs(
        ...     configuration = "short_range",
        ...     reference_time = "20210101T01Z"
        ...     )
        
        """
        # Validate configuration
        self.raise_invalid_configuration(configuration)

        # Break-up reference time
        issue_date, issue_time = NWMFileSource.separate_datetime(reference_time)

        # Set prefix
        prefix = f"nwm.{issue_date}/{configuration}/"
        
        # Generate url
        directory = self.server + prefix

        # Get directory listing
        html_doc = asyncio.run(self.get_html(directory, self.verify))

        # Parse content
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        # Get links
        elements = soup.select("a[href]")

        # Generate list
        blob_list = []
        for e in elements:
            filename = e.get("href")
            if filename.startswith(f"nwm.t{issue_time}"):
                full_path = directory + filename
                blob_list.append(full_path)

        return [b for b in blob_list if must_contain in b]

    @property
    def server(self) -> str:
        return self._server

    @server.setter
    def server(self, server: str) -> None:
        self._server = server

    @property
    def verify(self) -> str:
        return self._verify

    @verify.setter
    def verify(self, verify: str) -> None:
        self._verify = verify

class GCPFileSource(NWMFileSource):

    def list_blobs(self):
        """Query for NWM files on Google Cloud Platform."""

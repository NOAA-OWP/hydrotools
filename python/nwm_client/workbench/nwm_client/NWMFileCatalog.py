"""
================
NWM File Catalog
================
Tools for discovering operational NWM NetCDF data on generic web servers, for 
example:
NOMADS -- https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/

and Google Cloud Platform (GCP).

GCP -- https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model

Classes
-------
NWMFileCatalog
HTTPFileCatalog
GCPFileCatalog
"""
from abc import ABC, abstractmethod
from typing import List, Tuple
import asyncio
import aiohttp
import ssl
from bs4 import BeautifulSoup
from google.cloud import storage

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

    @classmethod
    def separate_datetime(cls, reference_time: str) -> Tuple[str, str]:
        """Divide reference time into separate date and time strings.

        Parameters
        ----------
        reference_time: str, required
            Reference time string formatted like %Y%m%dT%HZ, for example:
            "20210910T00Z"

        Returns
        -------
        Two strings: issue_date, issue_time
        """
        # Break-up reference time
        tokens = reference_time.split('T')
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

class HTTPFileCatalog(NWMFileCatalog):
    """An HTTP client class for NWM data.
    This HTTPFileCatalog class provides various methods for discovering NWM 
    files on generic web servers.
    """

    def __init__(
        self,
        server: str,
        ssl_context: ssl.SSLContext = ssl.create_default_context()
        ) -> None:
        """Initialize HTTP File Catalog of NWM data source.

        Parameters
        ----------
        server : str, required
            Fully qualified path to web server endpoint. Example:
            "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"
        ssl_context : ssl.SSLContext, optional, default context
            SSL configuration context.
            
        Returns
        -------
        None
        """
        super().__init__()
        # Server path
        self.server = server

        # Setup SSL context
        self.ssl_context = ssl_context

    @classmethod
    async def get_html(
        cls,
        url: str,
        ssl_context: ssl.SSLContext = ssl.create_default_context()
        ) -> str:
        """Retrieve an HTML document.

        Parameters
        ----------
        url : str, required
            Path to HTML document
        ssl_context : ssl.SSLContext, optional, default context
            SSL configuration context.

        Returns
        -------
        HTML document retrieved from url.
        """
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
            %Y%m%dT%HZ format.
        must_contain : str, optional, default 'channel_rt'
            Optional substring that must be found in each blob name.

        Returns
        -------
        A list of blob names that satisfy the criteria set by the parameters.
        """
        # Validate configuration
        self.raise_invalid_configuration(configuration)

        # Break-up reference time
        issue_date, issue_time = NWMFileCatalog.separate_datetime(reference_time)

        # Set prefix
        prefix = f"nwm.{issue_date}/{configuration}/"
        
        # Generate url
        directory = self.server + prefix

        # Get directory listing
        html_doc = asyncio.run(self.get_html(directory, self.ssl_context))

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
    def ssl_context(self) -> ssl.SSLContext:
        return self._ssl_context

    @ssl_context.setter
    def ssl_context(self, ssl_context: ssl.SSLContext) -> None:
        self._ssl_context = ssl_context

class GCPFileCatalog(NWMFileCatalog):
    """A Google Cloud client class for NWM data.
    This GCPFileCatalog class provides various methods for discovering NWM 
    files on Google Cloud Platform.
    """

    def __init__(
        self,
        bucket_name: str = 'national-water-model'
        ) -> None:
        """Initialize catalog of NWM data source on Google Cloud Platform.

        Parameters
        ----------
        bucket_name : str, required, default 'national-water-model'
            Name of Google Cloud Bucket
            
        Returns
        -------
        None
        """
        super().__init__()
        self.bucket_name = bucket_name

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
        A list of blob names that satisfy the criteria set by the parameters.
        """
        # Validate configuration
        self.raise_invalid_configuration(configuration)

        # Break-up reference time
        issue_date, issue_time = NWMFileCatalog.separate_datetime(reference_time)

        # Connect to bucket with anonymous client
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(self.bucket_name)

        # Get list of blobs
        blobs = client.list_blobs(
            bucket,
            prefix=f'nwm.{issue_date}/{configuration}/nwm.t{issue_time}'
            )

        # Return blob names
        return [b.public_url for b in list(blobs) if must_contain in b.name]

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name: str) -> None:
        self._bucket_name = bucket_name
    
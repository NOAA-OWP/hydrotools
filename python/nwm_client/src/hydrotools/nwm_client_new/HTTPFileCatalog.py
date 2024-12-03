"""
=====================
NWM HTTP File Catalog
=====================
Concrete implementation of a National Water Model file client for discovering 
files on generic HTTP servers, for example:

NOMADS -- https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/

Classes
-------
HTTPFileCatalog
"""
from .NWMFileCatalog import NWMFileCatalog
import asyncio
import aiohttp
import ssl
from bs4 import BeautifulSoup
from typing import List

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

    @staticmethod
    async def get_html(
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
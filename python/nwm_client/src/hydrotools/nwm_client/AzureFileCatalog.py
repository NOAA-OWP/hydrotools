"""
=============================================
NWM Azure Blob Storage Container File Catalog
=============================================
Concrete implementation of a National Water Model file client for discovering 
files on Microsoft Azure.

https://planetarycomputer.microsoft.com/dataset/storage/noaa-nwm

Classes
-------
AzureFileCatalog
"""
from .NWMFileCatalog import NWMFileCatalog
from hydrotools._restclient.urllib import Url
import azure.storage.blob
import planetary_computer
import adlfs
from typing import List

class AzureFileCatalog(NWMFileCatalog):
    """An Azure Cloud client class for NWM data.
    This AzureFileCatalog class provides various methods for discovering NWM 
    files on Azure Blob Storage.
    """

    def __init__(
        self,
        server: str = 'https://noaanwm.blob.core.windows.net/'
        ) -> None:
        """Initialize catalog of NWM data source on Azure Blob Storage.

        Parameters
        ----------
        server : str, required
            Fully qualified path to Azure Cloud endpoint.
            
        Returns
        -------
        None
        """
        super().__init__()
        self.server = server

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
        issue_date, issue_time = self.separate_datetime(reference_time)

        # Get list of blobs
        fs = adlfs.AzureBlobFileSystem(
            "noaanwm", credential=planetary_computer.sas.get_token("noaanwm", "nwm").token
        )
        blobs = fs.glob(f"nwm/nwm.{issue_date}/{configuration}/nwm.t{issue_time}*")

        # Return blob URLs
        return [
            str(self.server / suffix) 
            for suffix in list(blobs) 
            if must_contain in suffix
            ]

    @property
    def server(self) -> str:
        return self._server

    @server.setter
    def server(self, server: str) -> None:
        self._server = Url(server)
    
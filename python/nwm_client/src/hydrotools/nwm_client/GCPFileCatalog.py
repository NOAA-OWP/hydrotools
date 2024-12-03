"""
======================================
NWM Google Cloud Platform File Catalog
======================================
Concrete implementation of a National Water Model file client for discovering 
files on Google Cloud Platform (GCP).

GCP -- https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model

Classes
-------
GCPFileCatalog
"""
from .NWMFileCatalog import NWMFileCatalog
from google.cloud import storage
from typing import List

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
        issue_date, issue_time = self.separate_datetime(reference_time)

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
    
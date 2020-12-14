"""
================================
Google Cloud Platform NWM Client
================================
This module provides classes that offer a convenient 
interface to retrieve National Water Model (NWM) data 
from Google Cloud Platform.

https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model

Classes
-------
    NWMDataService

"""

from google.cloud import storage
from io import BytesIO
import xarray as xr
import pandas as pd
from os import cpu_count
from multiprocessing import Pool
from typing import Union, Iterable
from pathlib import Path

# Global singletons for holding location and df/None of NWM feature id to usgs site
# code mapping
_FEATURE_ID_TO_USGS_SITE_MAP_FILE = (
    Path(__file__).resolve().parent / "data/nwm_2_0_feature_id_with_usgs_site.csv"
)
_FEATURE_ID_TO_USGS_SITE_MAP = None


def NWM_bytes_to_DataFrame(
    bytes_string,
    filter: bool = True,
    filter_nwm_feature_id_with: Union[pd.DataFrame, pd.Series, Iterable] = None,
    join_on: str = "nwm_feature_id",
) -> pd.DataFrame:
    """Convert bytes from an NWM channel route netcdf4 file to a
    pandas.DataFrame

    Parameters
    ----------
    bytes_string : bytes, required
        Raw bytes from NWM channel route file.
    filter : bool, optional, default True
        To or not to filter returned df.
    filter_nwm_feature_id_with : Union[pd.DataFrame, pd.Series, Iterable], optional, default None
        Object used to filter the returned df. Dataframe, Series, list, np.array
    join_on : str, optional, default "nwm_feature_id"
        Field in filter_nwm_feature_id_with to filter by if applicable. Typically a
        column name.

    Returns
    -------
    pd.DataFrame
        A stacked DataFrame.
    """
    # Load data as xarray DataSet
    ds = xr.load_dataset(BytesIO(bytes_string), engine='h5netcdf', 
        mask_and_scale=False)

    # Extract streamflow data to pandas DataFrame
    df = pd.DataFrame({
        'nwm_feature_id': ds['streamflow'].feature_id.values,
        'value': ds['streamflow'].values
    })

    # Subset data
    # TODO implement RouteLink
    df = df.head(100)

    # Scale data
    scale_factor = ds['streamflow'].scale_factor[0]
    df.loc[:, 'value'] = df['value'].mul(scale_factor)

    # Convert feature IDs to strings
    df['nwm_feature_id'] = df['nwm_feature_id'].astype(str)

    # Extract valid datetime
    value_date = pd.to_datetime(ds.time.values[0])
    df['value_date'] = value_date

    # Extract reference datetime
    start_date = pd.to_datetime(ds.reference_time.values[0])
    df['start_date'] = start_date

    return df

class NWMDataService:
    """A Google Cloud Storage client class.
    The NWMDataService class provides various methods for constructing 
    requests, retrieving data, and parsing responses from the NWM dataset 
    on Google Cloud Platform.
    """

    def __init__(self, bucket_name='national-water-model', max_processes=None):
        """Instantiate NWM Data Service.

        Parameters
        ----------
        bucket_name : str, required
            Name of Google Cloud Bucket

        Returns
        -------
        data_service : gcp.NWMDataService
            A NWM data service object.

        Examples
        --------
        >>> from evaluation_tools.gcp_client import gcp
        >>> model_data_service = gcp.NWMDataService()
        
        """
        self._bucket_name = bucket_name

        if max_processes:
            self._max_procs = max_processes
        else:
            self._max_procs = cpu_count() - 2

    def get_blob(self, blob_name) -> bytes:
        """Retrieve a blob from the data service as bytes.

        Parameters
        ----------
        blob_name : str, required
            Name of blob to retrieve.

        Returns
        -------
        data : bytes
            The data stored in the blob.
        
        """
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(self.bucket_name)
        return bucket.blob(blob_name).download_as_bytes(timeout=120)

    def get_DataFrame(self, blob_name) -> pd.DataFrame:
        """Retrieve a blob from the data service as a pandas.DataFrame.

        Parameters
        ----------
        blob_name : str, required
            Name of blob to retrieve.

        Returns
        -------
        df : pandas.DataFrame
            The data stored in the blob.
        
        """
        bytes_string = self.get_blob(blob_name)
        return NWM_bytes_to_DataFrame(bytes_string)

    def _make_blob_name(self, configuration, reference_time, valid_hour) -> str:
        """Generate blob name for retrieval.

        Parameters
        ----------
        configuration : str, required
            Operational cycle of NWM.
        reference_time : str, required
            Issue time of model output in YYYYmmddTHHZ format.
        valid_hour : int, required
            Valid hour of data to retrieve.

        Returns
        -------
        blob_name : str
            String containing name of blob.
        
        """
        # Split reference_time string
        date_tokens = reference_time.split('T')

        # Issue day
        idt = date_tokens[0]

        # Issue time
        itm = date_tokens[1].lower()

        # Valid hour
        vhr = str(valid_hour).zfill(2)

        return f'nwm.{idt}/{configuration}/nwm.t{itm}.{configuration}.channel_rt.tm{vhr}.conus.nc'

    def get(self, configuration, reference_time) -> pd.DataFrame:
        """Retrieve a blob from the data service as a pandas.DataFrame.

        Parameters
        ----------
        configuration : str, required
            Operational cycle of NWM.
        reference_time : str, required
            Issue time of model output in YYYYmmddTHHZ format.

        Returns
        -------
        df : pandas.DataFrame
            Model data in stacked format.

        Examples
        --------
        >>> from evaluation_tools.gcp_client import gcp
        >>> model_data_service = gcp.NWMDataService()
        >>> df = model_data_service.get(
        ...     configuration='analysis_assim_extend',
        ...     reference_time='20201209T16Z'
        ... )
        
        """
        # Valid hours to retrieve
        valid_hours = [(configuration, reference_time, i) for i in range(28)]
        
        # Spawn processes
        with Pool(processes=self.max_processes) as pool:
            # Generate blob names
            blob_names = pool.starmap(self._make_blob_name, valid_hours)
            
            # Get data
            data_frames = pool.map(self.get_DataFrame, blob_names)
            
            # Concatenate
            return pd.concat(data_frames, ignore_index=True)

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def max_processes(self) -> int:
        return self._max_procs
    
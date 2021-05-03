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
import warnings
import pandas as pd
from os import cpu_count
from multiprocessing import Pool
from typing import Union
import numpy.typing as npt
from pathlib import Path
from collections.abc import Iterable

# Global singletons for holding location and df/None of NWM feature id to usgs site
# code mapping
_FEATURE_ID_TO_USGS_SITE_MAP_FILE = (
    Path(__file__).resolve().parent / "data/RouteLink_NWMv2.0.csv"
)

class NWMDataService:
    """A Google Cloud Storage client class.
    The NWMDataService class provides various methods for constructing 
    requests, retrieving data, and parsing responses from the NWM dataset 
    on Google Cloud Platform.
    """

    def __init__(
        self, 
        bucket_name: str = 'national-water-model', 
        max_processes: int = None,
        location_metadata_mapping: pd.DataFrame = None
        ):
        """Instantiate NWM Data Service.

        Parameters
        ----------
        bucket_name : str, required, default 'national-water-model'
            Name of Google Cloud Bucket
        max_processes : int, optional, default os.cpu_count() - 2
            Maximum number of simultaneous requests/connections.
        location_metadata_mapping : pandas.DataFrame with nwm_feature_id Index and
            columns of corresponding site metadata. Defaults to 7500+ usgs_site_code
            used by the NWM for data assimilation.

        Returns
        -------
        data_service : gcp.NWMDataService
            A NWM data service object.

        Examples
        --------
        >>> from hydrotools.gcp_client import gcp
        >>> model_data_service = gcp.NWMDataService()
        
        """
        # Set bucket name
        self._bucket_name = bucket_name

        # Set max processes
        if max_processes:
            self._max_procs = max_processes
        else:
            self._max_procs = cpu_count() - 2

        # Set default site mapping
        if location_metadata_mapping != None:
            self._crosswalk = location_metadata_mapping
        else:
            self._crosswalk = pd.read_csv(
                _FEATURE_ID_TO_USGS_SITE_MAP_FILE,
                dtype={"nwm_feature_id": int, "usgs_site_code": str},
                comment='#'
            ).set_index('nwm_feature_id')[['usgs_site_code']]

        # Set default dataframe cache
        self._cache = Path('gcp_cache.h5')

    # TODO find publicly available authoritative source of service
    #  compatible valid model configuration strings
    def list_blobs(
        self,
        configuration: str,
        reference_time: str,
        must_contain: str = 'channel_rt'
        ) -> list:
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
        >>> from hydrotools.gcp_client import gcp
        >>> model_data_service = gcp.NWMDataService()
        >>> blob_list = model_data_service.list_blobs(
        ...     configuration = "short_range",
        ...     reference_time = "20210101T01Z"
        ...     )
        
        """
        # Validate configuration
        if configuration not in self.configurations:
            message = f'Invalid configuration. Must select from {str(self.configurations)}'
            raise ValueError(message)

        # Break-up reference time
        tokens = reference_time.split('T')
        issue_date = tokens[0]
        issue_time = tokens[1].lower()

        # Connect to bucket with anonymous client
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(self.bucket_name)

        # Get list of blobs
        blobs = client.list_blobs(
            bucket,
            prefix=f'nwm.{issue_date}/{configuration}/nwm.t{issue_time}'
            )

        # Return blob names
        return [b.name for b in list(blobs) if must_contain in b.name]

    def get_blob(self, blob_name: str) -> bytes:
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
        # Setup anonymous client and retrieve blob data
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(self.bucket_name)
        return bucket.blob(blob_name).download_as_bytes(timeout=120)

    def get_Dataset(
        self, 
        blob_name: str,
        feature_id_filter: Union[npt.ArrayLike, bool] = True
        ) -> xr.Dataset:
        """Retrieve a blob from the data service as xarray.Dataset

        Parameters
        ----------
        blob_name : str, required
            Name of blob to retrieve.
        feature_id_filter : bool or array-like, optional, default False
            If True, filter data using default list of feature ids (USGS gaging locations).
            Alternatively, limit data returned to feature ids in feature_id_filter 
            list.

        Returns
        -------
        ds : xarray.Dataset
            The data stored in the blob.
        
        """
        # Get raw bytes
        raw_bytes = self.get_blob(blob_name)

        # Create Dataset
        ds = xr.load_dataset(
            BytesIO(raw_bytes),
            engine='h5netcdf',
            mask_and_scale=False
            )

        # Attempt to filter Dataset
        if isinstance(feature_id_filter, Iterable):
            try:
                feature_id_filter = list(feature_id_filter)
                return ds.sel(feature_id=feature_id_filter)
            except:
                warnings.warn("Invalid feature_id_filter")
                return ds

        # Return unfiltered Dataset
        if feature_id_filter == False:
            return ds

        # Return default filtered Dataset
        feature_id_filter = list(self.crosswalk.index)
        return ds.sel(feature_id=feature_id_filter)
            
    def get_DataFrame(
        self,
        *args,
        streamflow_only: bool = True,
        **kwargs
        ) -> pd.DataFrame:
        """Retrieve a blob from the data service as pandas.DataFrame

        Parameters
        ----------
        args : 
            Positional arguments passed to get_Dataset
        streamflow_only : bool, optional, default True
            Only return streamflow and omit other variables.
        kwargs : 
            Keyword arguments passed to get_Dataset

        Returns
        -------
        df : pandas.DataFrame
            The data stored in the blob.
        
        """
        # Retrieve the dataset
        ds = self.get_Dataset(*args, **kwargs)

        # Transform to DataFrame
        if streamflow_only:
            # Convert to DataFrame
            df = ds[['reference_time', 'time', 'streamflow']].to_dataframe().reset_index()
            
            # Extract scale factor
            scale_factor = ds['streamflow'].scale_factor[0]
            
            # Scale data
            df.loc[:, 'streamflow'] = df['streamflow'].mul(scale_factor)
        else:
            df = ds.to_dataframe().reset_index()

        # Release resources
        ds.close()

        # Rename columns
        df = df.rename(columns={
            'time': 'valid_time',
            'feature_id': 'nwm_feature_id'
        })

        # Categorize feature id
        df['nwm_feature_id'] = df['nwm_feature_id'].astype(str).astype(dtype="category")
        
        # Downcast floats
        df_float = df.select_dtypes(include=["float"])
        converted_float = df_float.apply(pd.to_numeric, downcast="float")
        df[converted_float.columns] = converted_float

        # Return DataFrame
        return df

    def get(
        self,
        configuration: str,
        reference_time: str
        ) -> pd.DataFrame:
        """Return streamflow data for a single model cycle in a pandas DataFrame.

        Parameters
        ----------
        configuration : str, required
            Particular model simulation or forecast configuration. For a list 
            of available configurations see NWMDataService.configurations
        reference_time : str, required
            Model simulation or forecast issuance/reference time in 
            YYYYmmddTHHZ format.

        Returns
        -------
        df : pandas.DataFrame
            Simluted or forecasted streamflow data associated with a single
            run of the National Water Model.

        Examples
        --------
        >>> from hydrotools.gcp_client import gcp
        >>> model_data_service = gcp.NWMDataService()
        >>> forecast_data = model_data_service.get(
        ...     configuration = "short_range",
        ...     reference_time = "20210101T01Z"
        ...     )
        
        """
        # Check cache
        # TODO Numpy complains about deprecated np.objects, downstream
        #  packages haven't caught up yet, in this case tables and/or pandas
        key = f'{configuration}/DT{reference_time}'
        if self.cache.exists():
            with pd.HDFStore(self.cache) as store:
                if key in store:
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", category=DeprecationWarning)
            
                        return store[key]

        # Get list of blob names
        blob_list = self.list_blobs(
            configuration=configuration,
            reference_time=reference_time
        )

        # Check for empty list
        if len(blob_list) == 0:
            raise ValueError("Config/Time combination returned no data")

        # Retrieve data
        with Pool(processes=self.max_processes) as pool:
            dataframes = pool.map(self.get_DataFrame, blob_list)
        
        # Concatenate data
        df = pd.concat(dataframes)

        # Rename
        df = df.rename(columns={'streamflow': 'value'})

        # Reformat crosswalk
        xwalk = self.crosswalk.reset_index()

        # Additional columns
        xwalk['configuration'] = configuration
        xwalk['measurement_unit'] = 'm3/s'
        xwalk['variable_name'] = 'streamflow'

        # Categorize
        xwalk = xwalk.astype(str).astype('category')
        xwalk = xwalk.set_index('nwm_feature_id')

        # Apply crosswalk metadata
        for col in xwalk:
            df[col] = df['nwm_feature_id'].map(xwalk[col])

        # Sort values
        df = df.sort_values(
            by=['nwm_feature_id', 'valid_time'],
            ignore_index=True
            )
        
        # Cache
        # TODO Remove warning when tables/pandas catches up to Numpy
        with pd.HDFStore(self.cache) as store:
            if key not in store:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=DeprecationWarning)

                    store.put(key, value=df, format='table')

        # Return all data
        return df

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def max_processes(self) -> int:
        return self._max_procs

    @property
    def crosswalk(self) -> pd.DataFrame:
        return self._crosswalk
        
    @property
    def cache(self) -> Path:
        return self._cache

    @cache.setter
    def cache(self, filepath):
        self._cache = Path(filepath)

    @property
    def configurations(self) -> list:
        # Valid configurations compatible with this client
        # TODO Find crosswalk for Alaska, Hawaii, Puerto Rico, and US Virgin Islands
        return [
            'analysis_assim',
            'analysis_assim_extend',
            # 'analysis_assim_hawaii',
            'analysis_assim_long',
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
            # 'short_range_hawaii'
            ]
            
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

from hydrotools.caches.hdf import HDFCache
from google.cloud import storage

from io import BytesIO
import xarray as xr
import warnings
import numpy as np
import pandas as pd
from os import cpu_count
from concurrent.futures import ProcessPoolExecutor
from typing import Union
import numpy.typing as npt
from pathlib import Path
from collections.abc import Iterable
from . import UnitHandler

# Global singletons for holding location and df/None of NWM feature id to usgs site
# code mapping
_FEATURE_ID_TO_USGS_SITE_MAP_FILES = (
    Path(__file__).resolve().parent / "data/RouteLink_CONUS_NWMv2.1.6.csv",
    Path(__file__).resolve().parent / "data/RouteLink_PuertoRico_NWMv2.1_20191204.csv",
    Path(__file__).resolve().parent / "data/RouteLink_HI.csv",
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
        *,
        location_metadata_mapping: pd.DataFrame = None,
        cache_path: Union[str, Path] = "nwm_client.h5",
        cache_group: str = 'nwm_client',
        unit_system: str = "SI"
        ):
        """Instantiate NWM Data Service.

        Note: By default, only nwm sites codes with an associated USGS site are returned by
        `NWMDataService.get`. See `NWMDataService`'s `location_metadata_mapping` parameter to change
        this behavior.

        Parameters
        ----------
        bucket_name : str, required, default 'national-water-model'
            Name of Google Cloud Bucket
        max_processes : int, optional, default os.cpu_count() - 2
            Maximum number of simultaneous requests/connections.
        location_metadata_mapping : pandas.DataFrame with nwm_feature_id Index and
            columns of corresponding site metadata. Defaults to 7500+ usgs_site_code
            used by the NWM for data assimilation.
        cache_path : str or pathlib.Path, optional, default 'gcp_client.h5'
            Path to HDF5 file used to store data locally.
        cache_group : str, optional, default 'gcp_client'
            Root group inside cache_path used to store HDF5 datasets.
            Structure defaults to storing pandas.DataFrames in PyTable format.
            Individual DataFrames can be accessed directly using key patterns 
            that look like '/{cache_group}/{configuration}/DT{reference_time}'
        unit_system: str, optional, default 'SI'
            The default measurement_unit for NWM streamflow data are cubic meter per second. 
            Setting this option to "US" will convert the units to cubic foot per second.

        Returns
        -------
        data_service : gcp.NWMDataService
            A NWM data service object.

        Examples
        --------
        >>> from hydrotools.nwm_client import gcp as nwm
        >>> model_data_service = nwm.NWMDataService()
        >>> # get nwm short range forecast data as a dataframe
        >>> # for nwm sites with associated USGS gage
        >>> forecast_data = model_data_service.get(
        ...     configuration = "short_range",
        ...     reference_time = "20210101T01Z"
        ...     )
        
        """
        # Set bucket name
        self._bucket_name = bucket_name

        # Set max processes
        if max_processes:
            self._max_procs = max(max_processes, 1)
        else:
            self._max_procs = max((cpu_count() - 2), 1)

        # Set default site mapping
        if location_metadata_mapping != None:
            self.crosswalk = location_metadata_mapping
        else:
            dfs = []
            for MAP_FILE in _FEATURE_ID_TO_USGS_SITE_MAP_FILES:
                dfs.append(pd.read_csv(
                MAP_FILE,
                dtype={"nwm_feature_id": int, "usgs_site_code": str},
                comment='#'
            ).set_index('nwm_feature_id')[['usgs_site_code']])
            self.crosswalk = pd.concat(dfs)

        # Set caching options
        self._cache_path = Path(cache_path)
        self._cache_group = cache_group

        # Validate system of units
        if unit_system not in self.valid_unit_systems:
            message = f'Invalid unit system "{unit_system}". Must select from {str(self.valid_unit_systems)}'
            raise ValueError(message)
        
        # Set default unit registry
        if unit_system == "US":
            self._unit_handler = UnitHandler.UnitHandler()
        else:
            self._unit_handler = None

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
        >>> from hydrotools.nwm_client import gcp as nwm
        >>> model_data_service = nwm.NWMDataService()
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
        check = np.isin(self.crosswalk.index, ds.feature_id)
        feature_id_filter = self.crosswalk[check].index
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
            scale_factor = ds['streamflow'].scale_factor
            
            # Scale data
            df.loc[:, 'streamflow'] = df['streamflow'].mul(scale_factor)
        else:
            df = ds.to_dataframe().reset_index()

        # Release resources
        ds.close()

        # Rename columns
        df = df.rename(columns={
            'time': 'value_time',
            'feature_id': 'nwm_feature_id'
        })

        # Downcast floats
        df_float = df.select_dtypes(include=["float"])
        converted_float = df_float.apply(pd.to_numeric, downcast="float")
        df[converted_float.columns] = converted_float

        # Return DataFrame
        return df

    def get_cycle(
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
        >>> from hydrotools.nwm_client import gcp as nwm
        >>> model_data_service = nwm.NWMDataService()
        >>> forecast_data = model_data_service.get(
        ...     configuration = "short_range",
        ...     reference_time = "20210101T01Z"
        ...     )
        
        """
        # Get list of blob names
        blob_list = self.list_blobs(
            configuration=configuration,
            reference_time=reference_time
        )

        # Check for empty list
        if len(blob_list) == 0:
            raise ValueError("Config/Time combination returned no data")

        # Compute chunksize
        chunksize = (len(blob_list) // self.max_processes) + 1

        # Retrieve data
        with ProcessPoolExecutor(
            max_workers=self.max_processes) as executor:
            dataframes = executor.map(
                self.get_DataFrame, 
                blob_list,
                chunksize=chunksize
                )
        
        # Concatenate data
        df = pd.concat(dataframes)

        # Rename
        df = df.rename(columns={'streamflow': 'value'})

        # Reformat crosswalk
        xwalk = self.crosswalk
        
        # Additional columns
        xwalk['configuration'] = configuration
        xwalk['measurement_unit'] = 'm3/s'
        xwalk['variable_name'] = 'streamflow'

        # Apply crosswalk metadata
        for col in xwalk:
            df[col] = df['nwm_feature_id'].map(xwalk[col])

        # Categorize
        df['configuration'] = df['configuration'].astype("category")
        df['measurement_unit'] = df['measurement_unit'].astype("category")
        df['variable_name'] = df['variable_name'].astype("category")
        df['usgs_site_code'] = df['usgs_site_code'].astype("category")

        # Sort values
        df = df.sort_values(
            by=['nwm_feature_id', 'value_time'],
            ignore_index=True
            )

        # Return all data
        return df

    def get(
        self,
        configuration: str,
        reference_time: str,
        cache_data: bool = True,
        ) -> pd.DataFrame:
        """Return streamflow data for a single model cycle in a pandas DataFrame.

        Note: By default, only nwm sites codes with an associated USGS site are returned by
        `NWMDataService.get`. See `NWMDataService`'s `location_metadata_mapping` parameter to change
        this behavior.

        Parameters
        ----------
        configuration : str, required
            Particular model simulation or forecast configuration. For a list 
            of available configurations see NWMDataService.configurations
        reference_time : str, required
            Model simulation or forecast issuance/reference time in 
            YYYYmmddTHHZ format.
        cache_data : bool, optional, default True
            If True use a local HDFStore to save retrieved data.

        Returns
        -------
        df : pandas.DataFrame
            Simluted or forecasted streamflow data associated with a single
            run of the National Water Model.

        Examples
        --------
        >>> from hydrotools.nwm_client import gcp as nwm
        >>> model_data_service = nwm.NWMDataService()
        >>> forecast_data = model_data_service.get(
        ...     configuration = "short_range",
        ...     reference_time = "20210101T01Z"
        ...     )
        
        """
        # Retrieve from cache
        if cache_data:
            key = f"/{self.cache_group}/{configuration}/DT{reference_time}"
            with HDFCache(
                path=self.cache_path,
                complevel=1,
                complib='zlib',
                fletch32=True
            ) as cache:
                df = cache.get(
                    self.get_cycle,
                    key,
                    configuration=configuration,
                    reference_time=reference_time
                )
        else:
            # Retrieve without caching
            df = self.get_cycle(configuration, reference_time)

        # Convert units
        if self._unit_handler:
            df.loc[:, "value"] = self._unit_handler.convert_values(df["value"], "m^3/s", "ft^3/s")
            df["measurement_unit"] = "ft^3/s"
        return df

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def cache_path(self) -> Path:
        return self._cache_path

    @cache_path.setter
    def cache_path(self, path):
        self._cache_path = Path(path)

    @property
    def cache_group(self) -> str:
        return self._cache_group

    @cache_group.setter
    def cache_group(self, group):
        self._cache_group = group

    @property
    def max_processes(self) -> int:
        return self._max_procs

    @property
    def crosswalk(self) -> pd.DataFrame:
        return self._crosswalk

    @crosswalk.setter
    def crosswalk(self, mapping):
        # Validate mapping
        if type(mapping) != pd.DataFrame:
            message = "crosswalk must be a pandas.DataFrame with nwm_feature_id index and a usgs_site_code column"
            raise Exception(message)

        if 'usgs_site_code' not in mapping:
            message = "DataFrame does not contain a usgs_site_code column"
            raise Exception(message)

        # Set crosswalk
        self._crosswalk = mapping

    @property
    def configurations(self) -> list:
        # Valid configurations compatible with this client
        # TODO Find crosswalk for Alaska
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

    @property
    def valid_unit_systems(self) -> list:
        return ['SI', 'US']

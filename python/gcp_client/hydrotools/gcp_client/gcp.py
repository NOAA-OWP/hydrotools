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
# from functools import partial
from os import cpu_count
# from multiprocessing import Pool
# from typing import Union, Iterable
from pathlib import Path
from collections.abc import Iterable

# Global singletons for holding location and df/None of NWM feature id to usgs site
# code mapping
_FEATURE_ID_TO_USGS_SITE_MAP_FILE = (
    Path(__file__).resolve().parent / "data/nwm_2_0_feature_id_with_usgs_site.csv"
)
# _FEATURE_ID_TO_USGS_SITE_MAP = None


# def NWM_bytes_to_DataFrame(
#     bytes_string,
#     filter: bool = True,
#     filter_nwm_feature_id_with: Union[pd.DataFrame, pd.Series, Iterable] = None,
#     join_on: str = "nwm_feature_id",
# ) -> pd.DataFrame:
#     """Convert bytes from an NWM channel route netcdf4 file to a
#     pandas.DataFrame

#     Parameters
#     ----------
#     bytes_string : bytes, required
#         Raw bytes from NWM channel route file.
#     filter : bool, optional, default True
#         To or not to filter returned df.
#     filter_nwm_feature_id_with : Union[pd.DataFrame, pd.Series, Iterable], optional, default None
#         Object used to filter the returned df. Dataframe, Series, list, np.array
#     join_on : str, optional, default "nwm_feature_id"
#         Field in filter_nwm_feature_id_with to filter by if applicable. Typically a
#         column name.

#     Returns
#     -------
#     pd.DataFrame
#         A stacked DataFrame.
#     """
#     global _FEATURE_ID_TO_USGS_SITE_MAP
#     global _FEATURE_ID_TO_USGS_SITE_MAP_FILE

#     if not filter_nwm_feature_id_with:

#         if _FEATURE_ID_TO_USGS_SITE_MAP is None:
#             # if the dataframe holding the mapping from feature id to site code hasn't
#             # been loaded

#             # Read, ensure its the right data types
#             _FEATURE_ID_TO_USGS_SITE_MAP = pd.read_csv(
#                 _FEATURE_ID_TO_USGS_SITE_MAP_FILE,
#                 dtype={"nwm_feature_id": int, "usgs_site_code": str},
#             )

#         filter_nwm_feature_id_with = _FEATURE_ID_TO_USGS_SITE_MAP

#     # Load data as xarray DataSet
#     ds = xr.load_dataset(BytesIO(bytes_string), engine='h5netcdf', 
#         mask_and_scale=False)

#     # Extract streamflow data to pandas DataFrame
#     df = pd.DataFrame({
#         'nwm_feature_id': ds['streamflow'].feature_id.values,
#         'value': ds['streamflow'].values
#     })

#     # Subset data
#     if filter:
#         try:
#             # try to left merge using filter_nwm_feature_id_with and join_on key
#             df = pd.merge(
#                 filter_nwm_feature_id_with,
#                 df,
#                 how="left",
#                 left_on=join_on,
#                 right_on="nwm_feature_id",
#             )

#         except TypeError:
#             # object passed to pd.merge not dataframe or series
#             # assume some kind of list like object
#             df = df[df["nwm_feature_id"].isin(filter_nwm_feature_id_with)]

#     # Scale data
#     scale_factor = ds['streamflow'].scale_factor[0]
#     df.loc[:, 'value'] = df['value'].mul(scale_factor)

#     # Convert feature IDs to strings
#     df['nwm_feature_id'] = df['nwm_feature_id'].astype(str)

#     # Extract valid datetime
#     value_date = pd.to_datetime(ds.time.values[0])
#     df['value_date'] = value_date

#     # Extract reference datetime
#     start_date = pd.to_datetime(ds.reference_time.values[0])
#     df['start_date'] = start_date

#     return df

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
        default_site_map: pd.DataFrame = None
        ):
        """Instantiate NWM Data Service.

        Parameters
        ----------
        bucket_name : str, required, default 'national-water-model'
            Name of Google Cloud Bucket
        max_processes : int, optional, default os.cpu_count() - 2
            Maximum number of simultaneous requests/connections.
        default_site_map : pandas.DataFrame with nwm_feature_id Index and
            columns of alternative site identifiers. Defaults to 7500+ usgs_site_code
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
        if default_site_map != None:
            self._crosswalk = default_site_map
        else:
            self._crosswalk = pd.read_csv(
                _FEATURE_ID_TO_USGS_SITE_MAP_FILE,
                dtype={"nwm_feature_id": int, "usgs_site_code": str},
            ).set_index('nwm_feature_id')

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
            Particular model simulation or forecast configuration.
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
        >>> blob_list = model_data_service(
        ...     configuration = "short_range",
        ...     reference_time = "20210101T01Z"
        ...     )
        
        """
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
        feature_id_filter=True) -> xr.Dataset:
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
            mask_and_scale=True
            )

        # Attempt to filter Dataset
        if isinstance(feature_id_filter, Iterable):
            try:
                feature_id_filter = list(feature_id_filter)
                return ds.sel(feature_id=feature_id_filter)
            except:
                warnings.warn("Invalid feature_id_filter")
                return ds

        # Return default filtered Dataset
        if feature_id_filter == True:
            feature_id_filter = list(self.crosswalk.index)
            return ds.sel(feature_id=feature_id_filter)

        # Return unfiltered Dataset
        if feature_id_filter == False:
            return ds
            
    def get_DataFrame(
        self,
        *args,
        drop_variables=[
            'crs',
            'nudge',
            'velocity',
            'qSfcLatRunoff',
            'qBucket',
            'qBtmVertRunoff'
            ],
        **kwargs
        ) -> pd.DataFrame:
        """Retrieve a blob from the data service as pandas.DataFrame

        Parameters
        ----------
        args : 
            Positional arguments passed to get_Dataset
        drop_variables : list
            Variables to drop from datasets. By default keeps only streamflow.
        kwargs : 
            Keyword arguments passed to get_Dataset

        Returns
        -------
        df : pandas.DataFrame
            The data stored in the blob.
        
        """
        # Retrieve the dataset
        ds = self.get_Dataset(*args, **kwargs).drop_vars(drop_variables)

        # Transform to DataFrame
        df = ds.to_dataframe().reset_index()

        # Release resources
        ds.close()

        # Rename columns
        df = df.rename(columns={
            'time': 'value_date',
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

    # def get_DataFrame(self, blob_name, **kwargs) -> pd.DataFrame:
    #     """Retrieve a blob from the data service as a pandas.DataFrame.

    #     Parameters
    #     ----------
    #     blob_name : str, required
    #         Name of blob to retrieve.

    #     Returns
    #     -------
    #     df : pandas.DataFrame
    #         The data stored in the blob.
        
    #     """
    #     bytes_string = self.get_blob(blob_name)
    #     return NWM_bytes_to_DataFrame(bytes_string, **kwargs)

    # def _make_blob_name(self, configuration, reference_time, valid_hour) -> str:
    #     """Generate blob name for retrieval.

    #     Parameters
    #     ----------
    #     configuration : str, required
    #         Operational cycle of NWM.
    #     reference_time : str, required
    #         Issue time of model output in YYYYmmddTHHZ format.
    #     valid_hour : int, required
    #         Valid hour of data to retrieve.

    #     Returns
    #     -------
    #     blob_name : str
    #         String containing name of blob.
        
    #     """
    #     # Split reference_time string
    #     date_tokens = reference_time.split('T')

    #     # Issue day
    #     idt = date_tokens[0]

    #     # Issue time
    #     itm = date_tokens[1].lower()

    #     # Valid hour
    #     vhr = str(valid_hour).zfill(2)

    #     return f'nwm.{idt}/{configuration}/nwm.t{itm}.{configuration}.channel_rt.tm{vhr}.conus.nc'

    # def get(
    #     self,
    #     configuration,
    #     reference_time,
    #     filter: bool = True,
    #     filter_nwm_feature_id_with: Union[pd.DataFrame, pd.Series, Iterable] = None,
    #     join_on: str = "nwm_feature_id",
    # ) -> pd.DataFrame:
    #     """Retrieve a blob from the data service as a pandas.DataFrame.

    #     Parameters
    #     ----------
    #     configuration : str, required
    #         Operational cycle of NWM.
    #     reference_time : str, required
    #         Issue time of model output in YYYYmmddTHHZ format.
    #     filter : bool, optional, default True
    #         To or not to filter returned df.
    #     filter_nwm_feature_id_with : Union[pd.DataFrame, pd.Series, Iterable], optional, default None
    #         Object used to filter the returned df. Dataframe, Series, list, np.array
    #     join_on : str, optional, default "nwm_feature_id"
    #         Field in filter_nwm_feature_id_with to filter by if applicable. Typically a
    #         column name.

    #     Returns
    #     -------
    #     df : pandas.DataFrame
    #         Model data in stacked format.

    #     Examples
    #     --------
    #     >>> from hydrotools.gcp_client import gcp
    #     >>> model_data_service = gcp.NWMDataService()
    #     >>> df = model_data_service.get(
    #     ...     configuration='analysis_assim_extend',
    #     ...     reference_time='20201209T16Z'
    #     ... )

    #     >>> cribbs_mill_creek_nwm_feature_id = [18206880]
    #     >>> cribbs_mill_df = model_data_service.get(
    #     ...     configuration='analysis_assim_extend',
    #     ...     reference_time='20201209T16Z',
    #     ...     filter_nwm_feature_id_with=cribbs_mill_creek_nwm_feature_id
    #     ... )

    #     """
    #     # Valid hours to retrieve
    #     valid_hours = [(configuration, reference_time, i) for i in range(28)]

    #     # Spawn processes
    #     with Pool(processes=self.max_processes) as pool:
    #         # Generate blob names
    #         blob_names = pool.starmap(self._make_blob_name, valid_hours)

    #         # Wrap get_DataFrame with keyword arguments
    #         part = partial(
    #             self.get_DataFrame,
    #             filter=filter,
    #             filter_nwm_feature_id_with=filter_nwm_feature_id_with,
    #             join_on=join_on,
    #         )

    #         # Get data
    #         data_frames = pool.map(part, blob_names)

    #         # Concatenate
    #         return pd.concat(data_frames, ignore_index=True)

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def max_processes(self) -> int:
        return self._max_procs

    @property
    def crosswalk(self) -> pd.DataFrame:
        return self._crosswalk
    
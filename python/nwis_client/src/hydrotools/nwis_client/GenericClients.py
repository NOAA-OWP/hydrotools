"""
=========================
Generic NWIS Client Tools
=========================
Client tools for retrieving USGS NWIS site data from various sources.

Classes
-------
NWISGenericClient
NWISSiteClient
NWISPeakClient
NWISStatClient
NWISRatingCurveClient
NWISFloodStageClient
"""

from pathlib import Path
from hydrotools._restclient import RestClient, Url
from typing import Union, Dict, Callable
import pandas as pd
from io import StringIO
from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt
import warnings

class NWISGenericClient(ABC):
    """Abstract interface for USGS NWIS data services.

    Attributes
    ----------
    _service: str, required
        Service URL string.
    _default_parameters: Dict[str, str], optional, default {}
        Dictionary of query parameters to append to every call to the service.
    _headers: Dict[str, str], optional, default {"Accept-Encoding": "gzip, compress"}
        Dictionary of headers to include with every service call.
    _column_conversions: Dict[str, Callable], optional
        Mapping from column label suffixes to datatype transformation methods.
        Defaults to transformations for common column label suffixes.
    _column_mapping: Dict[str, str], optional, default None
        Optional mapping used to rename DataFrame columns.
    """
    _service: str
    _default_parameters: Dict[str, str] = {}
    _headers: Dict[str, str] = {"Accept-Encoding": "gzip, compress"}
    _column_conversions: Dict[str, Callable] = {
            "cd": lambda c: c.astype("category"),
            "no": lambda c: c.astype("category"),
            "id": lambda c: c.astype("category"),
            "va": lambda c: c.astype(float),
            "ht": lambda c: c.astype(float),
            "dt": lambda c: pd.to_datetime(c),
            "tm": lambda c: pd.to_timedelta(c.add(":00"), errors="coerce"),
            "nu": lambda c: c.astype(int),
            "yr": lambda c: c.astype(int),
            "yr": lambda c: c.astype(int)
        }
    _column_mapping: Dict[str, str] = {"site_no": "usgs_site_code"}

    def __init__(
        self, 
        enable_cache: bool = True, 
        cache_expire_after: int = 43200,
        cache_filename: Union[str, Path] = "nwis_client_cache"
        ) -> None:
        """Setup client.

        Parameters
        ----------
        enable_cache: bool, optional, default True
            If True will use a request cache.
        cache_expire_after: int, optional, default 43200
            Time in seconds after which cache items expire.
        cache_filename: str or pathlib.Path, optional, default "nwis_client_cache"
            Stem of .sqlite database file path to use as request cache.

        """
        # Setup base URL
        self._base_url = Url(
            f"{self._service}",
            safe="/:",
            quote_overide_map={"+": "%2B"},
        )

        # Set up RestClient
        self._rest_client = RestClient(
            base_url=self._base_url,
            headers=self._headers,
            enable_cache=enable_cache,
            cache_filename=str(cache_filename),
            cache_expire_after=cache_expire_after
        )

    def get_dataframe(self, **parameters: str) -> pd.DataFrame:
        """Retrieve data from NWIS service and return a pandas.DataFrame.
        Over-ride this method if the service does not return tab-separated 
        text-based data.

        Parameters
        ----------
        parameters: str, required
            Query parameters passed to the service.

        Returns
        -------
        pandas.DataFrame
        """
        # Get raw response
        response = self._rest_client.get(parameters=parameters)

        # Convert to DataFrame
        return pd.read_csv(StringIO(response.text()), comment="#", sep="\t")

    @classmethod
    def process_dataframe(cls, data: pd.DataFrame) -> pd.DataFrame:
        """Process a raw pandas.DataFrame returned from a 
        NWISGenericClient.get_dataframe method. Note: this method creates 
        a copy of the original DataFrame. Over-ride this method if the service 
        does not return tab-separated text-based data.

        Parameters
        ----------
        data: pandas.DataFrame, required
            Unprocessed DataFrame.

        Returns
        -------
        Processed pandas.DataFrame
        """
        # Drop first row
        df = data.iloc[1:,:].reset_index(drop=True).copy(deep=True)

        # Convert types
        for col in df:
            func = cls._column_conversions.get(col[-2:], None)
            if func:
                df[col] = func(df[col])

        # Rename columns
        if cls._column_mapping:
            df = df.rename(columns=cls._column_mapping)
        return df

    @abstractmethod
    def _handle_options(self, **options) -> Dict[str, str]:
        """Abstrace method used to convert method parameters into query
        parameters.
        """
        pass

    def get(self, **options) -> pd.DataFrame:
        """Retrieve data from the service and return processed pandas.DataFrame. 
        Over-ride this method if the service does not return tab-separated 
        text-based data.
        """
        # Set parameters
        parameters = {
            **self._handle_options(**options), 
            **self._default_parameters
            }

        # Get data
        df = self.get_dataframe(**parameters)

        # Process data
        return self.process_dataframe(df)

class NWISSiteClient(NWISGenericClient):
    """Concrete interface to the NWIS Site Service."""
    _service: str = "https://waterservices.usgs.gov/nwis/site/"
    _default_parameters: Dict[str, str] = {
        "format": "rdb",
        "siteStatus": "all"
        }

    def _handle_options(self, sites: str) -> Dict[str, str]:
        """Handles options for the NWIS Site Service.
        
        Parameters
        ----------
        sites: str, required
            Comma-delimited list of sites passed directly to service.

        Returns
        -------
        Dict[str, str] query parameters
        """
        # Set parameters
        return {"sites": sites}

class NWISPeakClient(NWISGenericClient):
    """Concrete interface to the NWIS Peak Service."""
    _service: str = "https://nwis.waterdata.usgs.gov/nwis/peak/"
    _default_parameters: Dict[str, str] = {
        "sitefile_output_format": "rdb",
        "column_name": "site_no",
        "format": "rdb",
        "date_format": "YYYY-MM-DD",
        "rdb_compression": "value",
        "list_of_search_criteria": "multiple_site_no"
        }

    def _handle_options(self, sites: str) -> Dict[str, str]:
        """Handles options for the NWIS Peak Service.
        
        Parameters
        ----------
        sites: str, required
            Comma-delimited list of sites passed directly to service.

        Returns
        -------
        Dict[str, str] query parameters
        """
        # Set parameters
        return {"multiple_site_no": sites}

class NWISStatClient(NWISGenericClient):
    """Concrete interface to the NWIS Stat Service."""
    _service: str = "http://waterservices.usgs.gov/nwis/stat/"
    _default_parameters: Dict[str, str] = {"format": "rdb"}

    def _handle_options(self, sites: str, parameterCd: str = "00060") -> Dict[str, str]:
        """Handles options for the NWIS Stat Service.
        
        Parameters
        ----------
        sites: str, required
            Comma-delimited list of sites passed directly to service.
        parameterCd: str, optional, default "00060"
            USGS data parameter code. Defaults to streamflow (foot^3/s).
            https://help.waterdata.usgs.gov/codes-and-parameters/parameters

        Returns
        -------
        Dict[str, str] query parameters
        """
        # Set parameters
        return {
            "site": sites,
            "parameterCd": parameterCd
            }

class NWISRatingCurveClient(NWISGenericClient):
    """Concrete interface to the NWIS Rating Curve Service."""
    _service: str = "https://waterdata.usgs.gov/nwisweb/get_ratings"
    _default_parameters: Dict[str, str] = {"file_type": "exsa"}
    _column_conversions = {
            "INDEP": lambda c: c.astype(float),
            "SHIFT": lambda c: c.astype(float),
            "DEP": lambda c: c.astype(float),
            "STOR": lambda c: c.astype("category")
        }

    @classmethod
    def process_dataframe(cls, data: pd.DataFrame) -> pd.DataFrame:
        """Processes pandas.DataFrame returned from the NWIS 
        rating curve service.

        Parameters
        ----------
        data: pandas.DataFrame, required
            Unprocessed dataframe.

        Returns
        -------
        Processed pandas.DataFrame
        """
        # Drop first row
        df = data.iloc[1:,:].reset_index(drop=True).copy(deep=True)

        # Convert types
        for col in df:
            func = cls._column_conversions.get(col, None)
            if func:
                df[col] = func(df[col])
        return df

    def _handle_options(self, site: str):
        """Handles options for the NWIS Rating Curve Service.
        
        Parameters
        ----------
        site: str, required
            Single USGS site code.

        Returns
        -------
        Dict[str, str] query parameters
        """
        # Set parameters
        return {"site_no": site}

    def get(self, sites: Union[str, npt.ArrayLike]) -> pd.DataFrame:
        """Retrieve rating curve for a list of USGS site codes.
        
        Parameters
        ----------
        sites: str or array-like, required
            String of usgs site codes in a comma-delimited list or an array-like of 
            usgs site code.

        Returns
        -------
        pandas.DataFrame
        """
        # Split string
        if isinstance(sites, str):
            sites = sites.split(",")

        # Build parameters
        parameters = [{**self._handle_options(s), **self._default_parameters} for s in sites]

        # Retrieve data
        responses = self._rest_client.mget(parameters=parameters)

        # Convert to dataframes
        frames = [pd.read_csv(StringIO(r.text()), comment="#", sep="\t") for r in responses]

        # Add site codes
        for s, f in zip(sites, frames):
            f["usgs_site_code"] = s

        # Process dataframes
        df = pd.concat([self.process_dataframe(f) for f in frames], ignore_index=True)

        # Optimize memory
        df["usgs_site_code"] = df["usgs_site_code"].astype("category")
        return df

class NWISFloodStageClient(NWISGenericClient):
    """Concrete interface to the NWIS Flood Stage Service. This service maps 
    National Weather Service flood stage categories to USGS site codes.
    """
    _service: str = "https://waterwatch.usgs.gov/webservices/floodstage/"
    _default_parameters: Dict[str, str] = {"format": "json"}
    _column_conversions: Dict[str, Callable] = {
            "stage": lambda c: c.astype(float),
            "no": lambda c: c.astype("category")
        }

    def process_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process pandas.DataFrame returned the NWISFloodStageClient. 
        Note: this method creates a copy of the original DataFrame.

        Parameters
        ----------
        data: pandas.DataFrame, required
            Unprocessed DataFrame.

        Returns
        -------
        Processed pandas.DataFrame
        """
        # Copy
        df = data.copy(deep=True)

        # Convert types
        for col in df:
            func = self._column_conversions.get(col.split("_")[-1], None)
            if func:
                df[col] = func(df[col])

        # Rename columns
        if self._column_mapping:
            df = df.rename(columns=self._column_mapping)
        return df

    def _handle_options(self, site: str):
        """Handles options for the NWIS Flood Stage Service.
        
        Parameters
        ----------
        site: str, required
            Single USGS site code. If all available flood categories are desired 
            set site="all".

        Returns
        -------
        Dict[str, str] query parameters
        """
        # Get all sites
        if site == "all":
            return {}

        # Get single site
        return {"site": site}
    
    def _convert_stage_series_to_flow(self, series: pd.Series, rating_curves: pd.DataFrame) -> np.ndarray:
        """Convert a series of NWS flood stages to flood flows using a dataframe of rating curves.
        
        Parameters
        ----------
        series: pandas.Series, required
            Series of NWS flood stages with a name that corresponds to one of the sites in rating_curves.
        rating_curves: pandas.DataFrame, required
            Dataframe containing USGS rating curves as returned by NWISRatingCurveClient

        Returns
        -------
        numpy.ndarray containing interpolated flood flows
        """
        # Extract data
        rc = rating_curves[rating_curves["usgs_site_code"] == series.name]

        # Check for empty
        if rc.empty:
            warnings.warn(f"No rating curve found for usgs_site_code {series.name}", RuntimeWarning)
            return series * np.nan

        return np.interp(
            x = series,
            xp = rc["INDEP"],
            fp = rc["DEP"],
            left=np.nan,
            right=np.nan
        )

    def _convert_stage_dataframe_to_flow(self, data: pd.DataFrame, rating_curves: pd.DataFrame) -> pd.DataFrame:
        """Convert a dataframe of NWS flood stages to flood flows using a dataframe of rating curves.
        
        Parameters
        ----------
        data: pandas.Series, required
            DataFrames of NWS flood stages indexed by usgs_site_code.
        rating_curves: pandas.DataFrame, required
            Dataframe containing USGS rating curves as returned by NWISRatingCurveClient

        Returns
        -------
        pandas.DataFrame containing interpolated flood flows
        """
        converted = data.apply(
            self._convert_stage_series_to_flow, 
            axis=1, 
            result_type="broadcast", 
            rating_curves=rating_curves
            )
        return converted.rename(columns={c: c.replace("_stage", "_flow") for c in converted.columns})

    def get(self, sites: Union[str, npt.ArrayLike], compute_flow: bool = False) -> pd.DataFrame:
        """Retrieve flood categories for a list of USGS site codes.
        
        Parameters
        ----------
        sites: str or array-like, required
            String of usgs site codes in a comma-delimited list or an array-like of 
            usgs site code.
        compute_flow: bool, optional, default False
            When True will use the NWISRatingCurveClient to convert stage to streamflow.
            New columns are added to the returned dataframe.

        Returns
        -------
        pandas.DataFrame
        """
        # Split string
        if isinstance(sites, str):
            sites = sites.split(",")

        # Build parameters
        parameters = [{**self._handle_options(s), **self._default_parameters} for s in sites]

        # Retrieve data
        responses = self._rest_client.mget(parameters=parameters)

        # Convert to dataframes
        frames = [pd.DataFrame.from_records(r.json()["sites"]) for r in responses]

        # Process dataframes
        df = pd.concat([self.process_dataframe(f) for f in frames], ignore_index=True)

        # Convert to flow
        if compute_flow:
            # Index by site code
            df = df.set_index("usgs_site_code")

            # Rating curve
            rc_client = NWISRatingCurveClient()
            rating_curves = rc_client.get(sites=df.index)

            # Convert
            flood_flows = self._convert_stage_dataframe_to_flow(df, rating_curves)

            # Concatenate
            return pd.concat([df, flood_flows], axis=1).reset_index()
        return df

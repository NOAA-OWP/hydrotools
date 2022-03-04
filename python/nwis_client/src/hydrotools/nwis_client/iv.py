"""
=================================================
USGS NWIS Instantaneous Values REST Client
=================================================
This module provides an IVDataService class that provides a convenient interface to
the USGS NWIS Instantaneous Values (IV) REST Service API.
Classes
-------

   IVDataService

"""

import datetime
from collections.abc import Iterable
from functools import partial
import re
import aiohttp
import six
import warnings

import numpy as np
import pandas as pd
from hydrotools._restclient import RestClient, Url
from collections.abc import Sequence

# typing imports
from pathlib import Path
from typing import Dict, List, Set, TypeVar, Union, Iterable

T = TypeVar("T")


# local imports
from ._utilities import verify_case_insensitive_kwargs

def _verify_case_insensitive_kwargs_handler(m: str) -> None:
    raise RuntimeError(m)

class IVDataService:
    """
    Provides a programatic way to retrieve USGS Instantanous Value Service data in the
    canonical hydrotools pandas dataframe format. The IVDataService implements an
    sqlite3 request cache and asynchronous request backend that splits up and retrieves
    requests concurrently.

    Parameters
    ----------
    enable_cache : bool
        Toggle sqlite3 request caching
    cache_expire_after : int
        Cached item life length in seconds
    value_time_label: str, default 'value_time'
        Label to use for datetime column returned by IVDataService.get
    cache_filename: str or Path default 'nwisiv_cache'
        Sqlite cache filename or filepath. Suffix '.sqlite' will be added to file if not included.

    Examples
    --------
    >>> from hydrotools.nwis_client import IVDataService
    >>> service = IVDataService()
    >>> df = service.get(sites='01646500', startDT="2021-01-01", endDT="2021-02-01")

    >>> # Retrieve discharge data from all sites in Alabama over the past 5 days
    >>> df = service.get(stateCd='AL', period="P5D")

    >>> # Retrieve latest discharge data from a list of sites
    >>> sites = ['02339495', '02342500', '023432415', '02361000', '02361500', '02362240', '02363000', '02364500', '02369800', '02371500']
    >>> # Also works with np array's, pd.Series, and comma seperated string. Try it out!
    >>> # sites = np.array(['02339495', '02342500', '023432415', '02361000', '02361500', '02362240', '02363000', '02364500', '02369800', '02371500'])
    >>> # sites = pd.array(['02339495', '02342500', '023432415', '02361000', '02361500', '02362240', '02363000', '02364500', '02369800', '02371500'])
    >>> # sites = '02339495,02342500,023432415,02361000,02361500,02362240,02363000,02364500,02369800,02371500'
    >>> df = service.get(sites=sites)

    >>> # Retrieve discharge data from sites within a bounding box from a point in the past until the present
    >>> #
    >>> bbox = "-83.0,36.5,-81.0,38.5"
    >>> # or specify in list. It's possible to specify multiple bounding boxes using a list of comma seperated string or nested lists
    >>> # np.array's and pd.Series's are accepted too!
    >>> # bbox = [-83.,36.5,-81.,38.5]
    >>> #
    >>> # You can also specify start and end times using datetime, np.datetime64, timestamps!
    >>> from datetime import datetime
    >>> start = datetime(2021, 5, 1, 12)
    >>> df = service.get(bBox=bbox, startDT=start)

    >>> # Retrieve stage height data from sites within two counties for the past day
    >>> counties = [36109, 36107]
    >>> # Can specify as collection(list, np.array, pd.Series) of strings or ints or a comma seperated list of strings.
    >>> # counties = ["36109", "36107"]
    >>> # counties = "36109,36107"
    >>> df = service.get(countyCd=counties, period='P5D')
    """

    # Class level variables
    _datetime_format = "%Y-%m-%dT%H:%M%z"
    _base_url = Url(
        "https://waterservices.usgs.gov/nwis/iv/",
        safe="/:",
        quote_overide_map={"+": "%2B"},
    )
    _headers = {"Accept-Encoding": "gzip, compress"}
    _value_time_label = None

    def __init__(self, *, 
        enable_cache: bool = True, 
        cache_expire_after: int = 43200,
        value_time_label: str = "value_time",
        cache_filename: Union[str, Path] = "nwisiv_cache"
        ):
        self._cache_enabled = enable_cache
        self._restclient = RestClient(
            base_url=self._base_url,
            headers=self._headers,
            enable_cache=self._cache_enabled,
            cache_filename=str(cache_filename),
            cache_expire_after=cache_expire_after,
        )
        if value_time_label == None:
            self._value_time_label = "value_date"
            warning_message = "Setting value_time_label to value_date. Future versions will default to value_time. To silence this warning set value_time_label."
            warnings.warn(warning_message, UserWarning)
        else:
            self._value_time_label = value_time_label

    @verify_case_insensitive_kwargs(handler=_verify_case_insensitive_kwargs_handler)
    def get(
        self,
        sites: Union[
            str,
            Union[List[str]],
            np.ndarray,
            pd.Series,
        ] = None,
        stateCd: Union[str, Union[List[str]], np.ndarray, pd.Series] = None,
        huc: Union[
            str,
            List[Union[str, int]],
            np.ndarray,
            pd.Series,
        ] = None,
        bBox: Union[
            str,
            List[Union[str, int]],
            np.ndarray,
            pd.Series,
            Union[List[List[Union[str, int]]]],
        ] = None,
        countyCd: Union[str, List[Union[int, str]]] = None,
        parameterCd: str = "00060",
        startDT: Union[
            str,
            datetime.datetime,
            np.datetime64,
            pd.Timestamp,
            None,
        ] = None,
        endDT: Union[
            str,
            datetime.datetime,
            np.datetime64,
            pd.Timestamp,
            None,
        ] = None,
        period: Union[str, None] = None,
        siteStatus: str = "all",
        **params,
    ):
        """Return Pandas DataFrame of NWIS IV data.

        Parameters
        ----------
        sites: str, List[str], pandas.Series[str], or numpy.Array[str], optional
            Single site, comma separated string list of sites, or iterable collection of string sites
        stateCd: str, List[str], optional
            2 character U.S. State of Territory abbreviation single, comma seperated string, or iterable collection of strings
        huc: str, List[int], List[str], optional
           Hydrologic Unit Codes as single string, comma seperated string, or iterable collection of strings or ints.
           Full list https://water.usgs.gov/GIS/huc_name.html
        bBox: str, List[str, int, float], List[List[str, int, float]], optional
            lat, lon in format: west, south, east, north. Accepted as comma seperated string, list of str, int, float, or nested list of str, int, float
        countyCd: str, List[int, str]
            Single, comma seperated string, or iterable collection of strings or integers of U.S. county codes
            Full list: https://help.waterdata.usgs.gov/code/county_query?fmt=html
        parameterCd: str, optional, default '00060' (Discharge)
            Comma separated list of parameter codes in string format.
            Full list: https://nwis.waterdata.usgs.gov/usa/nwis/pmcodes?radio_pm_search=param_group&pm_group=All+--+include+all+parameter+groups&pm_search=&casrn_search=&srsname_search=&format=html_table&show=parameter_group_nm&show=parameter_nm&show=casrn&show=srsname&show=parameter_units
        startDT: str, datetime.datetime, np.datetime64, pd.Timestamp, or None, optional, default None
            Observation record start time. If timezone information not provided, defaults to UTC.
        endDT: str, datetime.datetime, np.datetime64, pd.Timestamp, or None, optional, default None
            Observation record end time. If timezone information not provided, defaults to UTC.
        period: str, None
            Observation record for period until current time. Uses ISO 8601 period time.
        siteStatus: str, optional, default 'all'
            Site status in string format.
            Options: 'all', 'active', 'inactive'
        params:
            Additional parameters passed directly to service.

        Returns
        -------
        pandas.DataFrame :
            DataFrame in semi-WRES compatible format

        Examples
        --------
        >>> from hydrotools.nwis_client import IVDataService
        >>> service = IVDataService()
        >>> df = service.get(sites='01646500', startDT="2021-01-01", endDT="2021-02-01")

        >>> # Retrieve discharge data from all sites in Alabama over the past 5 days
        >>> df = service.get(stateCd='AL', period="P5D")

        >>> # Retrieve latest discharge data from a list of sites
        >>> sites = ['02339495', '02342500', '023432415', '02361000', '02361500', '02362240', '02363000', '02364500', '02369800', '02371500']
        >>> # Also works with np array's, pd.Series, and comma seperated string. Try it out!
        >>> # sites = np.array(['02339495', '02342500', '023432415', '02361000', '02361500', '02362240', '02363000', '02364500', '02369800', '02371500'])
        >>> # sites = pd.array(['02339495', '02342500', '023432415', '02361000', '02361500', '02362240', '02363000', '02364500', '02369800', '02371500'])
        >>> # sites = '02339495,02342500,023432415,02361000,02361500,02362240,02363000,02364500,02369800,02371500'
        >>> df = service.get(sites=sites)

        >>> # Retrieve discharge data from sites within a bounding box from a point in the past until the present
        >>> #
        >>> bbox = "-83.0,36.5,-81.0,38.5"
        >>> # or specify in list. It's possible to specify multiple bounding boxes using a list of comma seperated string or nested lists
        >>> # np.array's and pd.Series's are accepted too!
        >>> # bbox = [-83.,36.5,-81.,38.5]
        >>> #
        >>> # You can also specify start and end times using datetime, np.datetime64, timestamps!
        >>> from datetime import datetime
        >>> start = datetime(2021, 5, 1, 12)
        >>> df = service.get(bBox=bbox, startDT=start)

        >>> # Retrieve stage height data from sites within two counties for the past day
        >>> counties = [36109, 36107]
        >>> # Can specify as collection(list, np.array, pd.Series) of strings or ints or a comma seperated list of strings.
        >>> # counties = ["36109", "36107"]
        >>> # counties = "36109,36107"
        >>> df = service.get(countyCd=counties, period='P5D')
        """
        raw_data = self.get_raw(
            sites=sites,
            stateCd=stateCd,
            huc=huc,
            bBox=bBox,
            countyCd=countyCd,
            parameterCd=parameterCd,
            startDT=startDT,
            endDT=endDT,
            period=period,
            siteStatus=siteStatus,
            **params,
        )

        def list_to_df_helper(item: dict):
            values = item.pop("values")
            df = pd.DataFrame(values)

            for column_name, value in item.items():
                df[column_name] = value

            return df

        def empty_df_warning_helper():
            warning_message = "No data was returned by the request."
            warnings.warn(warning_message)

        list_of_frames = list(map(list_to_df_helper, raw_data))

        # Empty list. No data was returned in the request
        if not list_of_frames:
            empty_df_warning_helper()
            empty_df = _create_empty_canonical_df()
            empty_df = empty_df.rename(columns={"value_time": self.value_time_label})
            return empty_df

        # Concatenate list in single pd.DataFrame
        dfs = pd.concat(list_of_frames, ignore_index=True)

        # skip data processing steps if no data was retrieved and return empty canonical df
        if dfs.empty:
            empty_df_warning_helper()
            empty_df = _create_empty_canonical_df()
            empty_df = empty_df.rename(columns={"value_time": self.value_time_label})
            return empty_df

        # Convert values to numbers
        dfs.loc[:, "value"] = pd.to_numeric(dfs["value"], downcast="float")

        # Convert all times to UTC
        dfs[self.value_time_label] = pd.to_datetime(
            dfs["dateTime"], utc=True, infer_datetime_format=True
        ).dt.tz_localize(None)

        # Simplify variable name
        dfs["variable_name"] = dfs["variableName"].apply(self.simplify_variable_name)

        # Sort DataFrame
        dfs = dfs.sort_values(
            ["usgs_site_code", "measurement_unit", self.value_time_label], ignore_index=True
        )

        # Fill NaNs
        dfs = dfs.fillna("")

        # Convert categories
        cols = [
            "variable_name",
            "usgs_site_code",
            "measurement_unit",
            "qualifiers",
            "series",
        ]
        dfs[cols] = dfs[cols].astype(str)
        dfs[cols] = dfs[cols].astype(dtype="category")

        # Downcast floats
        df_float = dfs.select_dtypes(include=["float"])
        converted_float = df_float.apply(pd.to_numeric, downcast="float")
        dfs[converted_float.columns] = converted_float

        # DataFrame in semi-WRES compatible format
        return dfs[
            [
                self.value_time_label,
                "variable_name",
                "usgs_site_code",
                "measurement_unit",
                "value",
                "qualifiers",
                "series",
            ]
        ]

    def get_raw(
        self,
        sites: Union[
            str,
            List[str],
            np.ndarray,
            pd.Series,
        ] = None,
        stateCd: Union[str, List[str], np.ndarray, pd.Series] = None,
        huc: Union[
            str,
            List[Union[str, int]],
            np.ndarray,
            pd.Series,
        ] = None,
        bBox: Union[
            str,
            List[Union[str, int]],
            np.ndarray,
            pd.Series,
            Union[List[List[Union[str, int]]]],
        ] = None,
        countyCd: Union[str, List[Union[int, str]]] = None,
        parameterCd: str = "00060",
        startDT: Union[
            str,
            datetime.datetime,
            np.datetime64,
            pd.Timestamp,
            None,
        ] = None,
        endDT: Union[
            str,
            datetime.datetime,
            np.datetime64,
            pd.Timestamp,
            None,
        ] = None,
        period: Union[str, None] = None,
        siteStatus: str = "all",
        max_sites_per_request: int = 20,
        **params,
    ) -> List[aiohttp.ClientResponse]:
        """
        Return raw requests data from the NWIS IV Rest API in a list.
        See `IVDataService.get` for argument documentation.
        """
        # handle start, end, and period parameters
        kwargs = self._handle_start_end_period_url_params(
            startDT=startDT, endDT=endDT, period=period
        )

        # might want to move this to an enum in the future
        factory_members = (
            (
                sites,
                partial(
                    split,
                    values=sites,
                    key="sites",
                    split_threshold=max_sites_per_request,
                    join_on=",",
                ),
            ),  # type: Union[Dict[str, str], List[Dict[str, str]]]
            # NWIS IV API allows 1 state per api call
            (
                stateCd,
                partial(split, values=stateCd, key="stateCd", split_threshold=1),
            ),
            # NWIS IV API allows 10 hucs per api call
            (
                huc,
                partial(split, values=huc, key="huc", split_threshold=10, join_on=","),
            ),
            (
                bBox,
                lambda *args, **kwargs: [{"bBox": item} for item in _bbox_split(bBox)],
            ),
            # NWIS IV API allows 20 counties per api call
            (
                countyCd,
                partial(
                    split,
                    values=countyCd,
                    key="countyCd",
                    split_threshold=20,
                    join_on=",",
                ),
            ),
        )

        filtered_members = [
            member for member in factory_members if member[0] is not None
        ]

        # Verify the correct number of args being passed
        assert len(filtered_members) == 1

        # Callable method from factory
        _, func = filtered_members.pop()
        query_params = func()  # type: list[dict]

        # Fill dictionary of
        params.update(kwargs)
        params.update(
            {
                "parameterCd": parameterCd,
                "siteStatus": siteStatus,
                "format": "json",
            }
        )

        for query_params_dict in query_params:
            query_params_dict.update(params)

        # return query_params
        results = self._restclient.mget(parameters=query_params, headers=self._headers)

        # flatten list of lists
        return [item for r in results for item in self._handle_response(r)]

    def _handle_start_end_period_url_params(
        self, startDT=None, endDT=None, period=None
    ) -> dict:
        """Handle passed date or period ranges, returning valid parameters and
        parameter combinations. Valid parameters are returned as a dictionary with
        parameter name keys (i.e. startDT) and associated validated/transformed
        periods/datetime string values.

        startDT's and endDT's will be converted to UTC and output in
        `_datetime_format` format (i.e. "2020-01-01" -> "2020-01-01T00:00+0000). See
        `_handle_date` for more information. Period strings are validated against
        regex, see `_validate_period_string` for more information.

        The following are parameter combinations are valid:
            _handle_start_end_period_url_params(startDT, endDT)
            _handle_start_end_period_url_params(startDT)
            _handle_start_end_period_url_params(period)

        If a (startDT and period) or (endDT and period) are passed, a KeyError is
        raised. If an invalid period is passed, a KeyError is also raised.

        Parameters
        ----------
        startDT, endDT : int, float, str, datetime, optional
            `_datetime_format` datetime string, by default None
        period : str, optional
            iso 8601 period string, by default None

        Returns
        -------
        dict
            Dictionary

        Raises
        ------
        KeyError
            If the input is malformed, e.g. {"period": "P1DG"} (the G is not ISO 8601)
        TypeError
            If any input is non-string or
        """
        args = {"startDT": startDT, "endDT": endDT, "period": period}
        accepted = [set(), {"startDT", "endDT"}, {"startDT"}, {"period"}]
        error_message = (
            "Invalid set of datetime related arguments.\n"
            "Cannot only supply:\n"
            "`period` and `startDT` and `endDT`\n"
            "`period` and `startDT`\n"
            "`period` and `endDT`\n"
            "`endDT`"
        )

        valid_args = validate_optional_combinations(
            arg_mapping=args, valid_arg_keys=accepted, exception_message=error_message
        )

        def is_string_or_non_string_iterable(x) -> bool:
            # Return True if x is a string or non-iterable
            if isinstance(x, six.string_types):
                return True
            return not isinstance(x, Iterable)

        for arg in valid_args.values():
            if not is_string_or_non_string_iterable(arg):
                error_message = "Non-string iterable type cannot be passed."
                raise TypeError(error_message)

        params = {}

        # Handle startDT, endDT, and period optional arguments.
        if startDT is None and endDT is None and period is None:
            # Return IV case
            return params

        # startDT and optionally endDT is included logic
        elif startDT and period is None:

            startDT = self._handle_date(startDT)
            params["startDT"] = startDT

            if endDT is not None:
                endDT = self._handle_date(endDT)
                params["endDT"] = endDT

        # period logic
        elif period and startDT is None and endDT is None:
            # TODO: Add iso 8601 period handler for splitting purposes
            if self._validate_period_string(period):
                params.update({"period": period})
            else:
                error_message = "`period` is not a valid ISO 8601 period string."
                raise KeyError(error_message)

        # Covers endDT or (period and endDT) or (period and startDT):
        else:
            # Throw
            error_message = (
                "Invalid set of datetime related arguments.\n"
                "Cannot only supply:\n"
                "`period` and `startDT` and `endDT`\n"
                "`period` and `startDT`\n"
                "`period` and `endDT`\n"
                "`endDT`"
            )
            raise KeyError(error_message)

        return params

    @staticmethod
    def _handle_response(raw_response: aiohttp.ClientResponse) -> List[dict]:
        """From a raw response, return a list of extracted sites in dictionary form.
        Relevant dictionary keys are:

            "usgs_site_code"
            "variableName"
            "measurement_unit"
            "values"
            "series"

        Parameters
        ----------
        raw_response : aiohttp.ClientResponse 
            Request GET response

        Returns
        -------
        List[dict]
            A list of handled responses
        """
        # TODO: Speed test using orjson instead of native
        deserialized_response = raw_response.json()

        def extract_metadata(json_time_series):
            return {
                # Add site code
                "usgs_site_code": json_time_series["sourceInfo"]["siteCode"][0][
                    "value"
                ],
                # Add variable name
                "variableName": IVDataService.simplify_variable_name(
                    json_time_series["variable"]["variableName"]
                ),
                # Add units
                "measurement_unit": json_time_series["variable"]["unit"]["unitCode"],
            }

        flattened_data = []

        for response_value_timeSeries in deserialized_response["value"]["timeSeries"]:

            for indicies, site_data in enumerate(response_value_timeSeries["values"]):

                # Create general site metadata dictionary
                site_metadata = extract_metadata(response_value_timeSeries)

                # Add site time series values and its index number
                site_metadata.update({"values": site_data["value"], "series": indicies})
                flattened_data.append(site_metadata)

        return flattened_data

    @staticmethod
    def simplify_variable_name(variable_name: str, split_delimiter: str = ",") -> str:
        """
        Split an input string by a delimiter and return only the first split
        result lowered.

        Parameters
        ----------
        variable_name : str
            String to simplify.

        split_delimiter : str
            Delimiter used to split data.

        Returns
        -------
        variable_name : str
            Simplified variable name

        """
        return variable_name.lower().split(split_delimiter)[0]

    def _handle_date(
        self,
        date: Union[str, int, float, datetime.datetime, np.datetime64, pd.Timestamp],
    ) -> Union[str, np.array]:
        """Wrangle dates from a wide range of formats into a standard strftime
        string representation.

        Float and integers timestamps are assumed to have units of seconds. See
        pandas.to_datetime documentation on parameter `unit` for more detail.

        Parameters
        ----------
        date : Union[str, datetime.datetime, np.datetime64, pd.Timestamp]
            Single date

        Returns
        -------
        str, np.array[str]
            strftime string
        """

        def dtype_handler(timestamp):
            if isinstance(timestamp, int) or isinstance(timestamp, float):
                return pd.to_datetime(timestamp, unit="s")

            return pd.to_datetime(timestamp)

        if isinstance(date, Iterable) and not isinstance(date, six.string_types):
            handled_heterogenous_container = map(dtype_handler, date)
            handled_date = pd.DatetimeIndex(handled_heterogenous_container)

        else:
            handled_date = dtype_handler(date)

        if handled_date.tz is not None:
            # Convert to UTC time
            handled_date = handled_date.tz_convert("UTC")

            # Drop the tz info
            handled_date = handled_date.tz_localize(None)

            warning_message = (
                "parsing timezone aware datetimes is deprecated;\n"
                "the date has been converted to UTC and the tz information has been "
                "dropped, ergo the date is now considered `naive` UTC.\n"
                "See https://github.com/NOAA-OWP/hydrotools/issues/46"
            )
            warnings.warn(warning_message, DeprecationWarning)

        # Add UTC tz
        handled_date = handled_date.tz_localize("UTC")

        handled_date = handled_date.strftime(self.datetime_format)

        # If it is just a string, return it
        if isinstance(handled_date, six.string_types):
            return handled_date

        return np.array(handled_date)

    def _validate_period_string(self, period: str) -> bool:
        """Validate if a string adheres to the duration format introduced in
        in ISO 8601.

        Parameters
        ----------
        period : str
            ISO 8601 period string.

        Returns
        -------
        bool
            True if validates against regex
        """
        pattern = r"^(-?)P(?=\d|T\d)(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)([DW]))?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$"
        return True if re.fullmatch(pattern, period) else False

    @property
    def base_url(self) -> str:
        """ API Baseurl """
        return self._base_url

    @property
    def cache_enabled(self) -> bool:
        """ Is cache enabled"""
        return self._cache_enabled

    @property
    def headers(self) -> dict:
        """ HTTP GET Headers """
        return self._headers

    @property
    def datetime_format(self) -> str:
        """ API's expected datetime format """
        return self._datetime_format

    @property
    def value_time_label(self) -> str:
        """ Label to use for datetime column """
        return self._value_time_label


def validate_optional_combinations(
    arg_mapping: Dict[str, T],
    valid_arg_keys: List[Set[str]],
    sentinel=None,
    exception: Exception = KeyError,
    exception_message=None,
) -> Dict[str, T]:
    filtered = {k: v for k, v in arg_mapping.items() if v is not sentinel}
    n_valid_sets = 0
    arg_keys = set(filtered.keys())

    for comb in valid_arg_keys:
        n_valid_sets += arg_keys == comb

    if n_valid_sets != 1:
        if exception_message is None:
            exception_message = f"Invalid combination of arguments passed: {arg_keys}.\n Valid combinations are {valid_arg_keys}"
        raise exception(exception_message)

    return filtered


def sequence_scientific_array_like(values: T) -> bool:
    ACCEPTED_MRO = (Sequence, pd.Series, np.ndarray)

    if not isinstance(values, ACCEPTED_MRO):
        error_message = f"Must be {ACCEPTED_MRO}. values type: {type(values)}."
        raise TypeError(error_message)


def split(
    key: str, values, split_threshold: int, join_on: str = None
) -> List[Dict[str, List[str]]]:

    # Fail fast if not valid type
    sequence_scientific_array_like(values)

    if isinstance(values, str):
        values = values.split(",")

    # convert to str
    values = [str(i) for i in values]

    if len(values) > split_threshold:
        mod = len(values) % split_threshold != 0
        n_groups = len(values) // split_threshold + mod

        # sort values for caching purposes
        values.sort()

        values = np.array_split(values, n_groups)

        return [
            {key: sublist if join_on is None else join_on.join(sublist)}
            for sublist in values
        ]  # type: List[Dict]

    return [
        {key: values if join_on is None else join_on.join(values)}
    ]  # type: List[Dict]


def _bbox_split(values: Union[str, list, tuple, pd.Series, np.ndarray]) -> List[str]:
    # Fail fast if not valid type
    sequence_scientific_array_like(values)

    if isinstance(values, str):
        values = values.split(",")

    else:
        # must be nested sequence of items
        def flatten_and_stringify(v):
            """ Flatten to list of strings """
            VALID_COLLECTIONS_MRO = (list, tuple, pd.Series, np.ndarray)

            l = []
            for item in v:
                if isinstance(item, str):
                    l += item.split(",")
                elif isinstance(item, VALID_COLLECTIONS_MRO):
                    l += flatten_and_stringify(item)
                else:
                    l += [str(item)]
            return l

        values = flatten_and_stringify(values)

    # Must be divisible by 4
    if len(values) % 4 != 0:
        error_message = f"values: {values} must be divisible by 4"
        raise ValueError(error_message)

    # split values in list of sublists each with len 4
    n_groups = len(values) // 4
    value_groups = np.array_split(values, n_groups)

    return list(map(lambda i: ",".join(i), value_groups))


def _create_empty_canonical_df() -> pd.DataFrame:
    """Returns an empty hydrotools canonical dataframe with correct field datatypes."""
    cols = {
        "value_time": pd.Series(dtype="datetime64[ns]"),
        "variable_name": pd.Series(dtype="category"),
        "usgs_site_code": pd.Series(dtype="category"),
        "measurement_unit": pd.Series(dtype="category"),
        "value": pd.Series(dtype="float32"),
        "qualifiers": pd.Series(dtype="category"),
        "series": pd.Series(dtype="category"),
    }
    return pd.DataFrame(cols, index=[])

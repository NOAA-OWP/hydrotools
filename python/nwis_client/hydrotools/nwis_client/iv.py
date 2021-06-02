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
from multiprocessing import Pool
from functools import partial
from typing import Dict, List, Set, T, Tuple, Union, Iterable
import re
import requests
import six
import warnings

import numpy as np
import pandas as pd
from hydrotools._restclient import RestClient
from collections.abc import Sequence

from .constants import US_STATE_AND_TERRITORY_ABBREVIATIONS


class IVDataService:
    """A REST client class.
    The IVDataService class provides various methods for constructing
    requests, retrieving data, and parsing responses from the NWIS IV
    Service.

    Parameters
    ----------
    processes : int
        Max multiprocessing processes, default 3
    retry : int
        Max number of, per request retries, default 3
    """

    # Class level variables
    _datetime_format = "%Y-%m-%dT%H:%M%z"
    _base_url = "https://waterservices.usgs.gov/nwis/iv/"
    _requests_cache_filename = "nwisiv_cache"
    _headers = {"Accept-Encoding": "gzip, compress"}

    def __init__(self, *, enable_cache: bool = True, cache_expire_after: int = 43200):
        self._restclient = RestClient(
            base_url=self._base_url,
            headers=self._headers,
            enable_cache=enable_cache,
            cache_filename=self._requests_cache_filename,
            cache_expire_after=cache_expire_after,
        )

    @classmethod
    def get(
        cls,
        sites: Union[str, List[str]] = None,
        stateCd: str = None,
        huc: Union[List[Union[int, str]], str, int] = None,
        bBox: Union[List[Union[int, float]], str] = None,
        countyCd: Union[List[int], str] = None,
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
        sites: str, list, pandas.Series, or numpy.Array, required
            Comma separated list of sites in string format or iterable.
        stateCd: str, optional
            Single 2 character U.S. State of Territory abbreviation
        huc: str, int, List[int], List[str], optional
            Hydrologic Unit Codes. Full list https://water.usgs.gov/GIS/huc_name.html
        bBox: str, List[int], List[float], optional
            lat, lon in format: west, south, east, north
        countyCd: str, List[int]
            County codes, no more than 20. Full list: https://help.waterdata.usgs.gov/code/county_query?fmt=html
        parameterCd: str, optional, default '00060' (Discharge)
            Comma separated list of parameter codes in string format.
        startDT: str, datetime.datetime, np.datetime64, pd.Timestamp, or None
                 optional, default None
            Observation record start time. If timezone information not provided,
            defaults to UTC.
        endDT: str, datetime.datetime, np.datetime64, pd.Timestamp, or None
                 optional, default None
        period: str, None
            Observation record for period until current time. Uses ISO 8601
            period time.
        siteStatus: str, optional, default 'all'
            Site status in string format
        params:
            Additional parameters passed directly to service.

        Returns
        -------
        pandas.DataFrame :
            DataFrame in semi-WRES compatible format

        Examples
        --------
        >>> from hydrotools.nwis_client.iv import IVDataService
        >>> data = IVDataService.get(sites='01646500')
        """
        iv_data_service = cls()
        raw_data = iv_data_service.get_raw(
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

        list_of_frames = list(map(list_to_df_helper, raw_data))

        # Empty list. No data was returned in the request
        if not list_of_frames:
            import warnings

            warning_message = "No data was returned by the request."
            warnings.warn(warning_message)
            return pd.DataFrame(None)

        # Concatenate list in single pd.DataFrame
        dfs = pd.concat(list_of_frames, ignore_index=True)

        # Convert values to numbers
        dfs.loc[:, "value"] = pd.to_numeric(dfs["value"], downcast="float")

        # Convert all times to UTC
        dfs["value_date"] = pd.to_datetime(
            dfs["dateTime"], utc=True, infer_datetime_format=True
        ).dt.tz_localize(None)

        # # Simplify variable name
        dfs["variable_name"] = dfs["variableName"].apply(
            iv_data_service.simplify_variable_name
        )

        # Sort DataFrame
        dfs = dfs.sort_values(
            ["usgs_site_code", "measurement_unit", "value_date"], ignore_index=True
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
                "value_date",
                "variable_name",
                "usgs_site_code",
                "measurement_unit",
                "value",
                "qualifiers",
                "series",
            ]
        ]

    @classmethod
    def get_as_json(
        cls,
        sites: Union[str, List[str]] = None,
        stateCd: str = None,
        huc: Union[List[Union[int, str]], str, int] = None,
        bBox: Union[List[Union[int, float]], str] = None,
        countyCd: Union[List[int], str] = None,
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
        # TODO Docstring
        iv_data_service = cls()
        return iv_data_service.get_raw(
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

    def get_raw(
        self,
        sites: Union[str, List[str]] = None,
        stateCd: str = None,
        huc: Union[List[Union[int, str]], str, int] = None,
        bBox: Union[List[Union[int, float]], str] = None,
        countyCd: Union[List[int], str] = None,
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
    ) -> List[requests.Response]:
        """
        Return raw requests data from the NWIS IV Rest API in a list.

        Parameters
        ----------
        sites: str, list, pandas.Series, or numpy.Array, optional
            Comma separated list of sites in string format or iterable.
        stateCd: str, optional
            Single 2 character U.S. State of Territory abbreviation
        huc: str, int, List[int], List[str], optional
            Hydrologic Unit Codes. Full list https://water.usgs.gov/GIS/huc_name.html
        bBox: str, List[int], List[float], optional
            lat, lon in format: west, south, east, north
        countyCd: str, List[int]
            County codes, no more than 20. Full list: https://help.waterdata.usgs.gov/code/county_query?fmt=html
        parameterCd: str, optional, default '00060' (Discharge)
            Comma separated list of parameter codes in string format.
        startDT: str, datetime.datetime, np.datetime64, pd.Timestamp, or None
                 optional, default None
            Observation record start time. If timezone information not provided,
            defaults to UTC.
        endDT: str, datetime.datetime, np.datetime64, pd.Timestamp, or None
                 optional, default None
            Observation record end time. If timezone information not provided,
            defaults to UTC.
        period: str, None
            Observation record for period until current time. Uses ISO 8601
            period time.
        siteStatus: str, optional, default 'all'
            Site status in string format
        max_sites_per_request: int, optional, default 100
            Generally should not be changed. Maximum number of sites in any single
            `requests.get` call. Any number greater will cause sites to be divided
            evenly amongst parallel
            `requests.get` calls.
        kwargs:
            Additional parameters passed directly to service.

        Returns
        -------
        List[requests.Response] :
            A list of retrieved requests objects

        Examples
        --------
        >>> from hydrotools.nwis_client import iv
        >>> service = iv.IVDataService()
        >>> data = service.get(sites='01646500')

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

    def get_raw_sites(
        self,
        sites: Union[str, List[str]],
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
        max_sites_per_request: int = 100,
        **params,
    ):
        params = self._get_raw_params_handler(
            parameterCd, startDT, endDT, period, siteStatus, **params
        )

        # Split sites into list
        if isinstance(sites, str):
            sites = sites.split(",")

        sites = self._unique(sites)

        # Threshold for divide and conquer requests
        if len(sites) > max_sites_per_request:
            response = self._multiprocessing_get(
                sites, params, partition_max_size=max_sites_per_request
            )

        else:
            # requests GET call
            response = self._get_and_handle_response(sites=sites, parameters=params)

        return response

    def _get_raw_params_handler(
        self,
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
        params.update(
            {"parameterCd": parameterCd, "siteStatus": siteStatus, "format": "json"}
        )

        # handle start, end, and period parameters
        start_end_period_params = self._handle_start_end_period_url_params(
            startDT=startDT, endDT=endDT, period=period
        )

        # add start/end, period, or nothing to url creation parameters
        params.update(start_end_period_params)

        return params

    def get_raw_stateCd(
        self,
        stateCd: str,
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
        params = self._get_raw_params_handler(
            parameterCd, startDT, endDT, period, siteStatus, **params
        )

        # verify that state of interest is valid
        if stateCd.upper() not in US_STATE_AND_TERRITORY_ABBREVIATIONS:
            error_message = (
                f"Provided state, {stateCd}, is not a valid U.S. State or "
                "Territory abbreviation. See https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations"
            )
            raise ValueError(error_message)

        params["stateCd"] = stateCd

        # requests GET call
        return self._get_and_handle_response(parameters=params)

    def get_raw_huc(
        self,
        huc: Union[List[Union[int, str]], str, int],
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
        params = self._get_raw_params_handler(
            parameterCd, startDT, endDT, period, siteStatus, **params
        )

        params["huc"] = str(huc)

        # requests GET call
        return self._get_and_handle_response(parameters=params)

    def get_raw_bBox(
        self,
        bBox: Union[List[Union[int, float]], str],
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
        params = self._get_raw_params_handler(
            parameterCd, startDT, endDT, period, siteStatus, **params
        )

        if not isinstance(bBox, six.string_types):
            bBox = map(str, bBox)
            bBox = ",".join(bBox)

        params["bBox"] = bBox

        # requests GET call
        return self._get_and_handle_response(parameters=params)

    def get_raw_countyCd(
        self,
        countyCd: Union[List[int], str],
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
        params = self._get_raw_params_handler(
            parameterCd, startDT, endDT, period, siteStatus, **params
        )

        params["countyCd"] = str(countyCd)

        # requests GET call
        return self._get_and_handle_response(parameters=params)

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

        # # Boolean addition. For valid input, should equal 3
        # N_VALID_ARGS = (
        #     is_string_or_non_string_iterable(startDT)
        #     + is_string_or_non_string_iterable(endDT)
        #     + is_string_or_non_string_iterable(period)
        # )

        # if N_VALID_ARGS != 3:
        #     error_message = "Non-string iterable type cannot be passed."
        #     raise TypeError(error_message)

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
    def _handle_response(raw_response: requests.Response) -> List[dict]:
        """From a raw response, return a list of extracted sites in dictionary form.
        Relevant dictionary keys are:
            "usgs_site_code"
            "variableName"
            "measurement_unit"
            "values"
            "series"

        Parameters
        ----------
        raw_response : requests.Response
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
    def _unique(collection: Union[List, Tuple]) -> List:
        """Return a list of the unique items from a collection.

        Parameters
        ----------
        collection : Union[List, Tuple]

        Returns
        -------
        List
            Returns a list of unique members of collection in their input type
        """
        return sorted(list(set(collection)))

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

    def _get_and_handle_response(
        self,
        sites: List[str] = None,
        parameters: dict = None,
    ):
        """Thin procedural convenience wrapper for getting a GET response and
        handling a single response. Useful for multiprocessing.
        """
        if parameters is None:
            parameters = {}

        parameters["sites"] = sites
        # requests GET call
        response = self._restclient.get(
            parameters=parameters,
            headers=self._headers,
            parameter_delimeter=",",
        )
        return self._handle_response(response)

    def _multiprocessing_get(
        self, sites: List[str], parameters: dict, partition_max_size: int = 100
    ):
        chunked_sites = self._chunk_request(
            sites, partition_max_size=partition_max_size
        )

        # Retrieve responses
        with Pool(processes=self._procs) as pool:
            responses = pool.map(
                partial(self._get_and_handle_response, parameters=parameters),
                chunked_sites,
            )
            flattend_responses = [item for sublist in responses for item in sublist]

        return flattend_responses

    def _chunk_request(
        self, sites: Union[str, List[str]], partition_max_size: int = 100
    ) -> Tuple[List[str]]:

        # Split sites into list
        if isinstance(sites, str):
            # Split into list, notice variable name reuse
            sites = sites.split(",")

        elif not isinstance(sites, Iterable):
            error_message = (
                f"Did not receive a string or iterable collection.\nSites: {sites}"
            )
            raise TypeError(error_message)

        n_groups = (len(sites) // partition_max_size) + 1
        return np.array_split(sites, n_groups)

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
        pattern = "^(-?)P(?=\d|T\d)(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)([DW]))?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$"
        return True if re.fullmatch(pattern, period) else False

    @property
    def base_url(self) -> str:
        """ API Baseurl """
        return self._base_url

    @property
    def headers(self) -> dict:
        """ HTTP GET Headers """
        return self._headers

    @property
    def datetime_format(self) -> str:
        """ API's expected datetime format """
        return self._datetime_format


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
                    item = list(map(str, item))
                    l += flatten_and_stringify(item)
                else:
                    l += [str(item)]
            return l

        values = flatten_and_stringify(values)

    # Must be divisible by 4
    if len(values) % 4 != 0:
        error_message = f"values: {values} must be divisible by 4"
        raise ValueError(error_message)

    # cast members to strings
    values = list(map(str, values))

    # split values in list of sublists each with len 4
    n_groups = len(values) // 4
    value_groups = np.array_split(values, n_groups)

    return list(map(lambda i: ",".join(i), value_groups))

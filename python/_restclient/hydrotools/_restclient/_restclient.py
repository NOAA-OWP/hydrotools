"""
Generic REST Api client usable/inheritable for general usage and adaptable to more
specific use cases.

# TODO: Add more information about the class here
"""

from typing import Any, Dict, List, Tuple, Union
from collections.abc import Iterable
import asyncio
from aiohttp_client_cache import SQLiteBackend

import requests
import requests_cache
from urllib3.util.retry import Retry

# local imports
from .async_client import ClientSession
from .async_helpers import AsyncToSerialHelper


class RestClient(AsyncToSerialHelper):
    """Provides various methods for constructing requests, retrieving data, and
    parsing responses from the NWIS IV Service.

    Parameters
    ----------
    processes : int
        Max multiprocessing processes, default 3
    retry : int
        Max number of, per request retries, default 3
    """

    _response_codes = {
        200: "OK",
        304: "Not_Modified",
        400: "Bad_Request",
        403: "Access_Forbidden",
        404: "Not_Found",
        500: "Internal_Server_Error",
        503: "Service_Unavailable",
    }

    def __init__(
        self,
        *,
        base_url: Union[str, None] = None,
        headers: Union[dict, None] = None,
        enable_cache: bool = True,
        requests_cache_filename: str = "cache",
        requests_cache_expire_after: int = 43200,
        retry: bool = True,
        retries: int = 3,
        loop: asyncio.AbstractEventLoop = None,
    ):
        super().__init__(loop)  # implicitly adds self._loop
        self._base_url = base_url
        self._headers = headers
        self._retires = retries
        self._cache_enabled = enable_cache

        cache = None
        if enable_cache is True:
            cache = SQLiteBackend(
                cache_name=requests_cache_filename,
                expire_after=requests_cache_expire_after,
                allowed_codes=[200],
                allowed_methods=["GET"],
            )

        self._session = self._add_to_loop(
            ClientSession(cache=cache, retry=retry, n_retries=retries)
        )

    def get(
        self,
        url: str = None,
        parameters: dict = None,
        headers: dict = None,
        parameter_delimeter: str = None,
        **kwargs,
    ):
        if not isinstance(url, str):
            if not isinstance(self._base_url, str):
                error_message = "A base_url was not set nor was a url passed."
                raise AttributeError(error_message)

            url = self._base_url

        request = self.Request(
            url=url,
            parameters=parameters,
            headers=headers,
            parameter_delimiter=parameter_delimeter,
        )
        return self.Get(request, **kwargs)

    def Request(
        self,
        url: str = None,
        parameters: Dict[str, Union[str, List[Any]]] = None,
        parameter_delimiter: Union[str, None] = None,
        headers: Dict[str, str] = None,
    ) -> requests.PreparedRequest:
        """Create Prepared Request from url and parameters and headers. Parameter
        concatenation behavior can be changed by passing a different
        `parameter_delimiter` argument. For example, a comma could be specified for
        USGS. (i.e. https://example-site.com/?var=1,2,3)

        Parameters
        ----------
        url : str, optional
            url on which parameters are appended, by default self._base_url
        parameters : Dict[str, Union[str, List[Any]], optional
            parameters to append to url, by default None
        parameter_delimiter : Union[str, None], optional
            delimiter to separate parameters.
            None will resume normal Requests behavior, by default ","
        headers : Dict[str, str], optional
            headers, by default None

        Returns
        -------
        requests.PreparedRequest
            Prepared requests object

        Examples
        --------
        >>> 
        """

        # Handle default headers.
        if not isinstance(headers, dict):
            headers = {}

        if parameters and parameter_delimiter:
            # Join key parameters that are in a list with delimiter
            # `parameter_delimiter`
            for key, value in parameters.items():
                if isinstance(value, Iterable) and not isinstance(value, str):
                    try:
                        parameters[key] = f"{parameter_delimiter}".join(value)
                    except TypeError:
                        value = map(str, value)
                        parameters[key] = f"{parameter_delimiter}".join(value)

        # Build GET request url
        return requests.Request("GET", url, params=parameters).prepare()

    def Get(self, request: requests.PreparedRequest, **kwargs,) -> requests.Response:
        """ Thin request.Session.get wrapper. Take prepared request and get
        response handling errors along the way. Only requests status codes
        200 and 201 returned.If the initial request fails, `self._retries`
        number retries are attempted with a 0.1 backoff factor.

        Parameters
        ----------
        request : requests.PreparedRequest
            Prepared request object. Header and url are included
        kwargs :
            Keyword arguments passed to requests.Session().send
            See: https://requests.readthedocs.io/en/latest/_modules/requests/sessions/#Session.send
            

        Returns
        -------
        requests.Response
            request.Session.get response.

        Raises
        ------
        requests.exceptions.ConnectionError
           Raise if receive non 200 or 201 response
        """
        try:
            with self._create_session() as session:
                response = session.send(request, **kwargs)

                if response.status_code == 201 or response.status_code == 200:
                    return response

                # Failed to retrieve
                error_message = (
                    "Retrieval failed\n"
                    + f"Server code: {response.status_code}\n"
                    + f"Server status: {self._response_codes[response.status_code]}\n"
                    + f"Query url:\n{request.url}"
                )
                raise requests.exceptions.ConnectionError(error_message)

        except requests.ConnectionError:
            error_message = f"Verify the {request.url} is correct"
            BaseException(error_message)
            raise

    def _create_session(self):
        """Create requests.Session object with concrete retry strategy.

        Returns
        -------
        requests.Session
            Session
        """

        with requests.Session() as session:

            # retry times and backoff factor (how long to sleep in between
            # retries)
            retires = Retry(
                total=self._retires,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504],
            )

            session.mount(
                "https://", requests.adapters.HTTPAdapter(max_retries=retires)
            )

            return session

    @property
    def base_url(self) -> str:
        """ Base url """
        return self._base_url

    @property
    def headers(self) -> dict:
        """ GET request headers """
        return self._headers


class Variadic(str):
    """Specify list or tuple as delimeted str. The is useful when specifying arguments
    in a URL that do not conform to the &key=value&key=value2 convention.

    Example:
        url = "https://www.test.gov",
        async with ClientSession() as session:
            async with session.get(url,
                params={"this": Variadic(["that", "the", "other"])},
            ) as req:
                print(req.url) # Returns, https://www.test.gov/?this=that,the,other

    """

    def __init__(self, values: Union[List, Tuple], *, delimeter: str = ",") -> None:
        self.values = delimeter.join([str(v) for v in values])

    def __repr__(self):
        return self.values

    def __str__(self) -> str:
        return repr(self)

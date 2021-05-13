from typing import Any, List, Union
import asyncio
from aiohttp.client_reqrep import ClientResponse
from aiohttp_client_cache.response import CachedResponse
from aiohttp_client_cache import SQLiteBackend
import aiohttp
import forge
import atexit

# local imports
from .async_client import ClientSession
from .async_helpers import AsyncToSerialHelper
from .urllib import Url
from ._restclient_sigs import GET_SIGNATURE, MGET_SIGNATURE

__all__ = ["RestClient"]


class RestClient(AsyncToSerialHelper):
    """
    Class adept for supporting and simplifying RESTful client libraries and retrieval
    scripts. Behind the scenes requests are made asynchronously, however the API is
    exposed using serial methods to simplify usage.

    Features
    --------
    - Base url
    - SQLite request cache
    - Retry exponential backoff
    - Serial wrapper methods that make requests asynchronously (see `RestClient.mget`)

    Parameters
    ----------
    base_url: Union[str, Url, None], default None
        Request base url
    headers: dict, default {}
        Headers included in every request
    enable_cache: bool, default True
        Enable or disable caching
    cache_filename: str, default "cache"
        Cache filename with .sqlite filetype suffix
    cache_expire_after: int, default 43200
        Cached request life in seconds
    retry: bool, default True
        Enable exponential backoff
    n_retries: int, default 3
        Attempt retries n times before failing
    loop: asyncio.AbstractEventLoop, default None
        Async event loop

    Examples
    --------

    Simple Request
    >>> from hydrotools._restclient import RestClient
    >>>
    >>> client = RestClient()
    >>> resp = client.get("weather.gov")
    >>> print(resp.text())


    USGS NLDI Requests
    >>> from hydrotools._restclient import RestClient
    >>>
    >>> base_url = "https://labs.waterdata.usgs.gov/api/nldi/linked-data/nwissite/"
    >>> headers = {"Accept": "*/*", "Accept-Encoding": "gzip, compress"}
    >>> client = RestClient(base_url=base_url, headers=headers)
    >>>
    >>> sites = ["0423360405", "05106000","05078520","05078470","05125039","05124982"]
    >>> site_urls = [f"/USGS-{site}/navigation/UT/flowlines" for site in sites]
    >>> requests = client.mget(site_urls)
    >>> requests = [resp.json() for resp in requests]
    """

    def __init__(
        self,
        *,
        base_url: Union[str, Url, None] = None,
        headers: dict = {},
        enable_cache: bool = True,
        cache_filename: str = "cache",
        cache_expire_after: int = 43200,
        retry: bool = True,
        n_retries: int = 3,
        loop: asyncio.AbstractEventLoop = None,
    ):
        # implicitly adds self._loop and gets loop if None provided
        super().__init__(loop)
        self._base_url = Url(base_url) if base_url is not None else None
        self._headers = headers
        self._retires = n_retries
        self._cache_enabled = enable_cache

        cache = None
        if enable_cache is True:
            cache = SQLiteBackend(
                cache_name=cache_filename,
                expire_after=cache_expire_after,
                allowed_codes=[200],
                allowed_methods=["GET"],
            )

        # wrap ClientSession in coroutine and call in event loop
        self._session = self._add_to_loop(
            self._wrap_func_in_coro(
                ClientSession, cache=cache, retry=retry, n_retries=n_retries
            )()
        )  # type: ClientSession

        # register session removal at normal exit
        atexit.register(self.close)

    @GET_SIGNATURE
    def get(self, url, *, parameters, headers, **kwargs):
        """Make GET request. If base url is set, url is appended to the base url.
        Passed headers are given precedent over instance headers(if present), meaning
        passed headers replace instance headers with matching keys.

        Parameters
        ----------
        url : str, Url
            Request url
        parameters : Dict[str, Union[str, List[str, int, float]]]
            Query parameters
        headers : Dict[str, str]
            Request headers, if RestClient headers set provided headers are appended

        Returns
        -------
        aiohttp.ClientResponse
        """

        return self._add_to_loop(
            self._get(url, parameters=parameters, headers=headers, **kwargs)
        )

    @MGET_SIGNATURE
    def mget(self, urls, *, parameters, headers, **kwargs):
        """Make multiple asynchronous GET request. If base url is set, each url is
        appended to the base url. Passed headers are given precedent over instance
        headers(if present), meaning passed headers replace instance headers with
        matching keys.

        Parameters
        ----------
        urls : List[Union[str, Url]]
            Request urls
        parameters : Dict[str, Union[str, List[str, int, float]]]
            Query parameters
        headers : Dict[str, str]
            Request headers, if RestClient headers set provided headers are appended

        Returns
        -------
        List[aiohttp.ClientResponse]
        """
        return self._add_to_loop(
            self._mget(urls, parameters=parameters, headers=headers, **kwargs)
        )

    @GET_SIGNATURE
    async def _get(
        self,
        url: str = None,
        *,
        parameters,
        headers,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        if url is None:
            if self.base_url is None:
                raise ValueError("no url provided and no base url set")
            # only base url
            url = self._base_url

        elif self.base_url is not None:
            url = self._base_url / url

        # add query parameters and get quoted representation
        url = (Url(url) + parameters).quote_url

        # Fast way to merge dicts https://stackoverflow.com/a/1784128
        # Create copy of instance headers, merge headers with instance header copy.
        # Headers passed to _get have precedent over instance headers
        _headers = dict(self.headers)
        _headers.update(headers)

        resp = await self._session.get(url, headers=_headers, **kwargs)

        # Verify origin of response. Attr not in aiohttp.ClientSession, thus default None.
        from_cache = getattr(resp, "from_cache", None)

        # CachedResponses implement __slots__ and thus cannot be monkeypatched.
        # see https://www.attrs.org/en/stable/glossary.html#term-slotted-classes
        # Theirfore, wrapping coro's json() and text() cannot be achieved.
        if from_cache:
            resp = cached_response_to_client_response(resp, loop=self._loop)

        # implicitly sets resp._body which contains response data
        await resp.read()

        # release the resource
        # note, resp is "locked" until released meaning it cannot be patched until post-release
        resp.release()
        # Patch and wrap resp's, text and json methods with run_until_complete and forge their signatures
        resp = self._patch_get(resp)
        return resp

    @MGET_SIGNATURE
    async def _mget(
        self,
        urls,
        *,
        parameters,
        headers,
        **kwargs: Any,
    ) -> List[aiohttp.ClientResponse]:
        if parameters:
            assert len(parameters) == len(urls)
        if headers:
            assert len(headers) == len(urls)

        return await asyncio.gather(
            *[
                self._get(
                    url,
                    parameters=parameters[idx] if parameters else {},
                    headers=headers[idx] if headers else {},
                )
                for idx, url in enumerate(urls)
            ]
        )

    def _patch_get(
        self, client_response: aiohttp.ClientResponse
    ) -> aiohttp.ClientResponse:
        """ Wrap aiohttp.ClientResponse text and json coros in run_until_complete. Monkeypatch text and json with wrappers."""
        # May iter through methods and wrap all coro's in the future
        # however that may not work if a non-coro returns a async context manager for example
        text = self._wrap_coro_in_callable(client_response.text)
        json = self._wrap_coro_in_callable(client_response.json)
        # resign signatures
        text = forge.copy(aiohttp.ClientResponse.text, exclude="self")(text)
        json = forge.copy(aiohttp.ClientResponse.json, exclude="self")(json)

        client_response.text = text
        client_response.json = json
        return client_response

    @property
    def base_url(self) -> str:
        """ Base url """
        return self._base_url

    @property
    def headers(self) -> dict:
        """ GET request headers """
        return self._headers

    def close(self) -> None:
        """ Release aiohttp.ClientSession """
        if not self._session.closed:
            self._add_to_loop(self._session.close())

    def __del__(self) -> None:
        atexit.unregister(self.close)
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def cached_response_to_client_response(
    cached_response: CachedResponse, *, loop: asyncio.AbstractEventLoop
):
    """ Translation from aiohttp_client_cache.CachedResponse to aiohttp.ClientResponse """
    # Naive 'casting' to ClientResponse. Likely needs work to cover all cases.
    inst = ClientResponse(
        cached_response.method,
        cached_response.url,
        writer=None,
        continue100=False,
        timer=None,
        traces=[],
        session=None,
        request_info=cached_response.request_info,
        loop=loop,
    )
    inst._body = cached_response._body
    inst.version = cached_response.version
    inst.status = cached_response.status
    inst.reason = cached_response.reason
    inst._headers = cached_response.headers
    inst._raw_headers = cached_response.raw_headers
    return inst

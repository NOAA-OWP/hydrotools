"""Base OGC API Client.

This module provides the base class for all collection-specific USGS OGC API 
clients. It handles configuration state and the low-level request pipeline.
"""
import ssl
from typing import Any, Optional, Sequence, Generic
from functools import partial

from yarl import URL

from .async_web_client import get_all, ResponseContentType
from .client_config import SETTINGS
from .constants import USGSCollection, OGCPATH, OGCAPI
from .url_builder import (
    build_request,
    build_request_batch,
    build_request_batch_from_queries,
    build_request_batch_from_feature_ids,
    QueryType
)
from .transformers import TransformedResponse_co, ResponseTransformer, to_geodataframe

class BaseClient(Generic[TransformedResponse_co]):
    """Base class for USGS OGC API clients. Specific child classes may overwrite
    private attributes: _server, _api, _endpoint, _path, _content_type,
    _max_pages.
    Otherwise, these are set to package SETTINGS defaults.

    Attributes:
        concurrency_limit: Max simultaneous requests allowed for this client.
        max_retries: Number of times to attempt a failed request.
        timeout_seconds: Total request timeout in seconds.
        ssl_context: Custom SSL context for requests.
        transformer: Callable object that takes a list[dict[str, Any]] and returns
            a transformed result. Defaults to GeoDataFrame.
    """
    _server: URL = SETTINGS.usgs_base_url
    _api: OGCAPI = SETTINGS.default_api
    _endpoint: USGSCollection = SETTINGS.default_collection
    _path: OGCPATH = SETTINGS.default_path
    _content_type: ResponseContentType = ResponseContentType.JSON
    _max_pages: int = SETTINGS.max_pages

    def __init__(
        self,
        concurrency_limit: int = SETTINGS.default_concurrency,
        max_retries: int = SETTINGS.default_retries,
        timeout_seconds: int = SETTINGS.timeout_seconds,
        ssl_context: Optional[ssl.SSLContext] = None,
        transformer: Optional[ResponseTransformer] = to_geodataframe
    ) -> None:
        self.concurrency_limit = concurrency_limit
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        self.ssl_context = ssl_context
        self.transformer = transformer

        # Setup request builder
        self._builder = partial(
            build_request,
            server=self._server,
            api=self._api,
            endpoint=self._endpoint,
            path=self._path
            )

    def __init_subclass__(cls):
        super().__init_subclass__()

        # Enfore required attributes
        required = ["_endpoint", "_path", "_api", "_server", "_content_type"]
        for attr in required:
            if not hasattr(cls, attr) or getattr(cls, attr) is None:
                raise TypeError(
                    f"Class {cls.__name__} failed to define required attribute: {attr}"
                )

        # Check for `get` method
        if not callable(getattr(cls, "get", None)):
            raise NotImplementedError(
                f"Class {cls.__name__} must implement a public 'get' method "
                "that wraps the internal '_get_responses' pipeline."
            )

    def _build_urls(
        self,
        feature_ids: Optional[Sequence[str]] = None,
        queries: Optional[Sequence[QueryType]] = None
    ) -> list[URL]:
        """Constructs a list of yarl.URL objects given arguments.

        Args:
            feature_ids: Sequence of specific feature identifiers.
            queries: A sequence of query parameter dictionaries.

        Returns:
            A list of yarl.URL objects.

        """
        if (feature_ids is not None) and (queries is not None):
            return build_request_batch(
                feature_ids=feature_ids,
                queries=queries,
                request_builder=self._builder
            )
        elif queries is not None:
            return build_request_batch_from_queries(
                queries=queries,
                request_builder=self._builder
                )
        elif feature_ids is not None:
            return build_request_batch_from_feature_ids(
                feature_ids=feature_ids,
                request_builder=self._builder
                )
        return [self._builder()]

    def _get_json_responses(
        self,
        feature_ids: Optional[Sequence[str]] = None,
        queries: Optional[Sequence[QueryType]] = None
    ) -> list[dict[str, Any]]:
        """Internal method to build URLs and execute concurrent requests. Note
        that this method will silently drop bytes and None responses returned
        by `get_all`. These responses are logged in `async_web_client`.

        Args:
            feature_ids: Sequence of specific feature identifiers.
            queries: A sequence of query parameter dictionaries.

        Returns:
            A list of responses. Paginated responses are appended to the end
            of the list.

        """
        # Prepare initial fetch
        urls = self._build_urls(feature_ids, queries)
        results: list[dict[str, Any]] = []

        # Fetch data
        for _ in range(self._max_pages):
            # Get batch of URLs
            batch = get_all(
                urls=urls,
                concurrency_limit=self.concurrency_limit,
                max_retries=self.max_retries,
                ssl_context=self.ssl_context,
                timeout_seconds=self.timeout_seconds,
                content_type=self._content_type
            )

            # Filter batch
            json_batch: list[dict[str, Any]] = [b for b in batch if isinstance(b, dict)]

            # Extend results
            results.extend(json_batch)

            # Inspect links for pagination
            urls = [self._get_next_url(r) for r in json_batch if self._has_next_url(r)]

            # No more data to fetch
            if not urls:
                break
        return results

    def _has_next_url(self, response: dict[str, Any] | bytes | None) -> bool:
        """Checks response for the presence of pagination 'next' link."""
        if not isinstance(response, dict):
            return False
        return any(link.get("rel") == "next" for link in response.get("links", []))

    def _get_next_url(self, response: dict[str, Any]) -> URL:
        """Attempts to return the first 'next' link encountered in response."""
        if not isinstance(response, dict):
            raise TypeError("response is not a dict")

        for link in response.get("links", []):
            if link.get("rel") == "next":
                return URL(link["href"])
        raise KeyError("response does not contain 'next' link")

    def _handle_response(
            self,
            data: list[dict[str, Any]]
    ) -> list[dict[str, Any]] | TransformedResponse_co:
        """Handle JSON response and optionally transform.
    
        Args:
            data: A list of deserialized GeoJSON responses from an OGC-compliant API.
        
        Returns:
            If self.transformer is None, returns untransformed data, else returns
            transformed responses.
        """
        if self.transformer is None:
            return data
        return self.transformer(data)

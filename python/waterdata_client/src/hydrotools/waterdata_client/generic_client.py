"""Generic OGC API Client.

This module provides the base class for all collection-specific USGS OGC API 
clients. It handles configuration state and the low-level request pipeline.
"""
import ssl
from typing import Any, Optional, Sequence
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

class GenericClient:
    """Base class for USGS OGC API clients. Specific child classes may overwrite
    private attributes: _server, _api, _endpoint, _path, _content_type.
    Otherwise, these are set to package SETTINGS defaults.

    Attributes:
        concurrency_limit: Max simultaneous requests allowed for this client.
        max_retries: Number of times to attempt a failed request.
        timeout_seconds: Total request timeout in seconds.
        ssl_context: Custom SSL context for requests.
    """
    _server: URL = SETTINGS.usgs_base_url
    _api: OGCAPI = SETTINGS.default_api
    _endpoint: USGSCollection = SETTINGS.default_collection
    _path: OGCPATH = SETTINGS.default_path
    _content_type: ResponseContentType = ResponseContentType.JSON

    def __init__(
        self,
        concurrency_limit: int = SETTINGS.default_concurrency,
        max_retries: int = SETTINGS.default_retries,
        timeout_seconds: int = SETTINGS.timeout_seconds,
        ssl_context: Optional[ssl.SSLContext] = None
    ) -> None:
        self.concurrency_limit = concurrency_limit
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        self.ssl_context = ssl_context

    def _get_responses(
        self,
        feature_ids: Optional[Sequence[str]] = None,
        queries: Optional[Sequence[QueryType]] = None
    ) -> list[dict[str, Any] | bytes | None]:
        """Internal method to build URLs and execute concurrent requests.

        Args:
            feature_ids: Sequence of specific feature identifiers.
            queries: A sequence of query parameter dictionaries.

        Returns:
            A list of responses in the order of the input queries.

        """
        # Set request builder
        request_builder = partial(
            build_request,
            server=self._server,
            api=self._api,
            endpoint=self._endpoint,
            path=self._path
            )

        # Build URLs
        if (feature_ids is not None) and (queries is not None):
            urls = build_request_batch(
                feature_ids=feature_ids,
                queries=queries,
                request_builder=request_builder
            )
        elif queries is not None:
            urls = build_request_batch_from_queries(
                queries=queries,
                request_builder=request_builder
                )
        elif feature_ids is not None:
            urls = build_request_batch_from_feature_ids(
                feature_ids=feature_ids,
                request_builder=request_builder
                )
        else:
            urls = [request_builder()]

        # Fetch URLs
        return get_all(
            urls=urls,
            concurrency_limit=self.concurrency_limit,
            max_retries=self.max_retries,
            ssl_context=self.ssl_context,
            timeout_seconds=self.timeout_seconds,
            content_type=self._content_type
        )

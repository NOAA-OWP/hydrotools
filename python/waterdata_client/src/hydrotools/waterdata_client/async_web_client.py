"""Asynchronous HTTP client.

This module provides a low-level asynchronous client designed to handle 
concurrent HTTP requests. It includes built-in throttling 
via semaphores and automatic retry logic.

Example:
>>> from hydrotools.waterdata_client import get_all
>>> base_url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/"
>>> collection = "monitoring-locations/items"
>>> query = "?f=json&id=USGS-02146470"
>>> req = base_url + collection + query
>>> urls = [req]
>>> results = get_all(urls)
"""

import asyncio
import logging
import ssl
from pathlib import Path
from typing import Any, Optional, Self, Sequence
from concurrent.futures import ThreadPoolExecutor

import aiohttp
from tenacity import (
    AsyncRetrying,
    RetryCallState,
    before_sleep_log,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential
)
from yarl import URL

LOGGER: logging.Logger = logging.getLogger(Path(__file__).stem)
"""Module-level logger."""

def return_none_on_failure(retry_state: RetryCallState) -> None:
    """Callback function to handle exhausted retries.

    Args:
        retry_state: The current state of the retry call.
    """
    url = retry_state.args[0] if retry_state.args else "Unknown URL"
    LOGGER.error("Retries exhausted for %s. Returning None.", url)

class AsyncWebClient:
    """An asynchronous HTTP client.

    Attributes:
        ssl_context: SSL configuration for secure requests.
        semaphore: Controller for the maximum number of concurrent requests.
        timeout: The total timeout settings for aiohttp requests.
        session: The underlying persistent aiohttp client session.
        retrier: The tenacity AsyncRetrying instance used for requests.
    """

    def __init__(
        self,
        concurrency_limit: int = 10,
        max_retries: int = 3,
        ssl_context: Optional[ssl.SSLContext] = None,
        timeout_seconds: int = 900
    ) -> None:
        """Initializes the client.

        Args:
            concurrency_limit: Max simultaneous requests. Defaults to 10.
            max_retries: Number of times to attempt a failed request. Defaults to 3.
            ssl_context: Custom SSL context. Defaults to default system context.
            timeout_seconds: Total request timeout in seconds. Defaults to 900.
        """
        self.ssl_context = ssl_context or ssl.create_default_context()
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        self.session: Optional[aiohttp.ClientSession] = None

        self.retrier = AsyncRetrying(
            retry=retry_if_exception_type(
                (aiohttp.ClientResponseError, asyncio.TimeoutError, aiohttp.ClientError)
            ),
            stop=stop_after_attempt(max_retries),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            before_sleep=before_sleep_log(LOGGER, logging.WARNING),
            retry_error_callback=return_none_on_failure,
            reraise=False
        )

    async def __aenter__(self) -> Self:
        """Initializes the session with a pooled connector."""
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
            timeout=self.timeout
        )
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> None:
        """Closes the underlying session."""
        if self.session:
            await self.session.close()

    async def fetch(self, url: URL) -> Optional[dict[str, Any] | bytes]:
        """Fetches a URL with semaphore-based throttling and retries.

        Args:
            url: The URL to retrieve.

        Returns:
            Decoded JSON or raw bytes. Returns None if all retries fail.
        """
        if self.session is None or self.session.closed:
            raise RuntimeError("AsyncWebClient must be used within an 'async with' block.")
        return await self.retrier(self._execute_request, url)

    async def _execute_request(self, url: URL) -> Optional[dict[str, Any] | bytes]:
        """Internal method to perform the actual network I/O.
        
        Args:
            url: The URL to retrieve.
        """
        async with self.semaphore:
            async with self.session.get(url) as response:
                # Retry on 5xx
                if response.status >= 500:
                    response.raise_for_status()

                # Fail on 4xx
                if response.status != 200:
                    LOGGER.error("Request to %s failed with status %s", url, response.status)
                    return None

                content_type = response.headers.get("Content-Type", "").lower()
                if "json" in content_type:
                    return await response.json()
                return await response.read()

    async def fetch_all(
        self, url_list: Sequence[URL]
    ) -> list[dict[str, Any] | bytes | None]:
        """Concurrently fetches a list of URLs.

        Args:
            url_list: Sequence of URLs to fetch.

        Returns:
            List of responses in the order of the input URLs.
        """
        return list(await asyncio.gather(*[self.fetch(url) for url in url_list]))

def get_all(
    urls: Sequence[str | URL],
    concurrency_limit: int = 10,
    max_retries: int = 3,
    ssl_context: Optional[ssl.SSLContext] = None,
    timeout_seconds: int = 900
) -> list[dict[str, Any] | bytes | None]:
    """Synchronously retrieves data from multiple URLs concurrently.

    This function provides a wrapper around AsyncWebClient to handle the asyncio
    event loop internally.

    Args:
        urls: A sequence of URL strings or yarl URL objects.
        concurrency_limit: Max simultaneous requests. Defaults to 10.
        max_retries: Number of times to attempt a failed request. Defaults to 3.
        ssl_context: Custom SSL context. Defaults to default system context.
        timeout_seconds: Total request timeout in seconds. Defaults to 900.

    Returns:
        A list of parsed JSON objects, bytes, or None for each URL.
    """
    # Convert strings to URL objects if necessary
    url_objects = [URL(u) if isinstance(u, str) else u for u in urls]

    async def _run() -> list[Any]:
        async with AsyncWebClient(
            concurrency_limit=concurrency_limit,
            max_retries=max_retries,
            ssl_context=ssl_context,
            timeout_seconds=timeout_seconds
        ) as client:
            return await client.fetch_all(url_objects)

    # Isolate the event loop from the main thread to avoid nested event loops
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(asyncio.run, _run())
        return future.result()

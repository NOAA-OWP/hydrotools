"""Asynchronous HTTP client.

This module provides a low-level asynchronous client designed to handle 
concurrent HTTP requests. It includes built-in throttling 
via semaphores and automatic retry logic.

Example:
>>> import asyncio
>>> from yarl import URL
>>> from hydrotools.waterdata_client import AsyncWebClient
>>> base_url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/"
>>> collection = "monitoring-locations/items"
>>> query = "?f=json&id=USGS-02146470"
>>> req = base_url + collection + query
>>> async def main():
...     async with AsyncWebClient(concurrency_limit=5) as client:
...         urls = [URL(req)]
...         results = await client.fetch_all(urls)
...         print(results)
>>> asyncio.run(main())
"""

import asyncio
import logging
import ssl
from pathlib import Path
from typing import Any, Optional, Self, Sequence

import aiohttp
from tenacity import (
    RetryCallState,
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from yarl import URL

LOGGER: logging.Logger = logging.getLogger(Path(__file__).stem)
"""Module-level logger."""

def return_none_on_failure(retry_state: RetryCallState) -> None:
    """Callback function to handle exhausted retries.

    Args:
        retry_state: The current state of the retry call.
    """
    LOGGER.error("Retries exhausted for %s. Returning None.", retry_state.args[1])

class AsyncWebClient:
    """An asynchronous HTTP client with concurrency throttling.

    Attributes:
        ssl_context: SSL configuration for secure requests.
        semaphore: Controller for the maximum number of concurrent requests.
        timeout: The total timeout settings for aiohttp requests.
        session: The underlying persistent aiohttp client session.
    """

    def __init__(
        self,
        concurrency_limit: int = 10,
        ssl_context: Optional[ssl.SSLContext] = None,
        timeout_seconds: int = 900
    ) -> None:
        """Initializes the client with a semaphore for throttling.

        Args:
            concurrency_limit: Max simultaneous requests. Defaults to 10.
            ssl_context: Custom SSL context. Defaults to default system context.
            timeout_seconds: Total request timeout in seconds. Defaults to 900.
        """
        self.ssl_context = ssl_context or ssl.create_default_context()
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        self.session: Optional[aiohttp.ClientSession] = None

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

    @retry(
        retry=retry_if_exception_type(
            (aiohttp.ClientResponseError, asyncio.TimeoutError, aiohttp.ClientError)
        ),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        before_sleep=before_sleep_log(LOGGER, logging.WARNING),
        retry_error_callback=return_none_on_failure,
    )
    async def fetch(self, url: URL) -> Optional[dict[str, Any] | bytes]:
        """Fetches a URL with semaphore-based throttling and retries.

        Args:
            url: The URL to retrieve.

        Returns:
            Decoded JSON or raw bytes. Returns None if all retries fail.
        """
        if self.session is None or self.session.closed:
            raise RuntimeError("AsyncWebClient must be used within an 'async with' block.")

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
        tasks = [self.fetch(url) for url in url_list]
        return list(await asyncio.gather(*tasks))

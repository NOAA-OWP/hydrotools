"""USGS OGC API schema handling.

This module provides utilities to retrieve, cache, and resolve the 
OpenAPI/OGC schema used by USGS water data services.
"""
from pathlib import Path
from typing import Any
import logging
from io import BytesIO

import jsonref
import yaml
from yarl import URL

from .client_config import SETTINGS
from .async_web_client import get_all, ResponseContentType

LOGGER: logging.Logger = logging.getLogger(Path(__file__).stem)
"""Module-level logger."""

def retrieve_yaml(url: str) -> dict[str, Any]:
    """Retrieves and parses YAML data from a URL.

    This function acts as a loader for jsonref to resolve external 
    references within the OGC schema.

    Args:
        url: The URL string from which to retrieve and parse YAML.

    Returns:
        The parsed YAML content as a dictionary.

    Raises:
        RuntimeError: If the URL does not return a valid bytes response.
    """
    result = get_all(
        [URL(url)],
        concurrency_limit=SETTINGS.default_concurrency,
        max_retries=SETTINGS.default_retries,
        timeout_seconds=SETTINGS.timeout_seconds,
        content_type=ResponseContentType.BYTES
    )[0]

    if isinstance(result, bytes):
        return yaml.safe_load(BytesIO(result))

    raise RuntimeError(f"Did not receive bytes from {url}")

def get_schema_bytes() -> bytes:
    """Retrieves the OGC schema as raw bytes from the cache or USGS.

    This function checks the persistent disk cache before attempting a network
    request.

    Returns:
        The raw OGC schema content as bytes.

    Raises:
        RuntimeError: If the schema cannot be retrieved from the USGS endpoint.
    """
    # Check disk cache
    client_cache = SETTINGS.default_cache
    schema_disk_cache_key = str(SETTINGS.schema_url)
    cached_schema = client_cache.get(schema_disk_cache_key)
    if cached_schema:
        LOGGER.debug("Loaded OGC schema from disk cache.")
        return cached_schema

    # Fetch
    LOGGER.info("Fetching fresh OGC schema from USGS...")
    raw_bytes = get_all(
        urls=[SETTINGS.schema_url],
        concurrency_limit=SETTINGS.default_concurrency,
        max_retries=SETTINGS.default_retries,
        timeout_seconds=SETTINGS.timeout_seconds,
        content_type=ResponseContentType.BYTES
    )[0]

    if not isinstance(raw_bytes, bytes):
        raise RuntimeError("Could not retrieve OGC schema from USGS.")

    # Save to disk
    client_cache.set(
        schema_disk_cache_key,
        raw_bytes,
        expire=SETTINGS.cache_expires
    )
    return raw_bytes

def get_schema() -> dict[str, Any]:
    """Retrieves and resolves the OGC schema.

    This function uses jsonref to deserialize the schema and resolve 
    internal and external $ref pointers.

    Returns:
        The resolved JSON schema as a dictionary-like object.

    Raises:
        RuntimeError: If the schema cannot be parsed as a dictionary.
    """
    schema = jsonref.loads(
        get_schema_bytes(),
        loader=retrieve_yaml,
        lazy_load=True
    )

    if isinstance(schema, dict):
        return schema

    raise RuntimeError("Resolved OGC schema is not a valid dictionary.")

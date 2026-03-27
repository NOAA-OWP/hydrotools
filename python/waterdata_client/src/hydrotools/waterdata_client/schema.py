"""USGS OGC API schema handling."""
from pathlib import Path
from typing import Any, Optional
import logging
from io import BytesIO

import jsonref
import yaml
from yarl import URL

from .client_config import ClientConfig
from .async_web_client import get_all, ResponseContentType

LOGGER: logging.Logger = logging.getLogger(Path(__file__).stem)
"""Module-level logger."""

def retrieve_yaml(url: str) -> dict[str, Any]:
    """Retrieve YAML data from URL.
    
    Args:
        url: URL from which to retrieve and parse YAML.
    
    Returns:
        Parsed YAML as a dict.
    
    Raises:
        RuntimeError if url does not return bytes.
    """
    result = get_all([URL(url)], content_type=ResponseContentType.BYTES)[0]
    if isinstance(result, bytes):
        return yaml.safe_load(BytesIO(result))
    raise RuntimeError(f"Did not receive bytes from {url}")

def get_schema_bytes(
        client_config: Optional[ClientConfig] = None
        ) -> bytes:
    """Retrieves and resolves the OGC schema with disk caching.

    Args:
        client_config: ClientConfig object with package defaults.

    Returns:
        Schema as raw bytes.
    """
    # Load default config
    client_config = client_config or ClientConfig()

    # Check disk cache
    client_cache = client_config.build_cache()
    schema_disk_cache_key = str(client_config.schema_url)
    cached_schema = client_cache[schema_disk_cache_key]
    if cached_schema:
        LOGGER.debug("Loaded OGC schema from disk cache.")
        return cached_schema

    # Fetch
    LOGGER.info("Fetching fresh OGC schema from USGS...")
    raw_bytes = get_all(
        urls=[client_config.schema_url],
        max_retries=client_config.default_retries,
        content_type=ResponseContentType.BYTES
    )[0]

    if not isinstance(raw_bytes, bytes):
        raise RuntimeError("Could not retrieve OGC schema from USGS.")

    # Save to disk
    client_cache[schema_disk_cache_key] = raw_bytes
    return raw_bytes

def get_schema(
        client_config: Optional[ClientConfig] = None
        ) -> dict[str, Any]:
    """Retrieves and resolves the OGC schema with disk caching.

    Args:
        client_config: ClientConfig object with package defaults.

    Returns:
        De-serialized JSON schema as dict.
    """
    schema = jsonref.loads(
        get_schema_bytes(client_config),
        loader=retrieve_yaml,
        lazy_load=True
    )
    if isinstance(schema, dict):
        return schema
    raise RuntimeError("Unable to parse JSON schema.")

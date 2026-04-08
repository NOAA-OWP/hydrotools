"""Package-wide configuration and defaults.

This module provides a thread-safe, environment-aware configuration singleton 
for hydrotools WaterData clients.

Example:
    >>> from hydrotools.waterdata_client import SETTINGS
    >>> print(SETTINGS.usgs_base_url)
    https://api.waterdata.usgs.gov/ogcapi/v0
"""
__all__ = ["SETTINGS"]

import os
from sys import stdout
from enum import StrEnum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, Optional, TextIO, Self
from functools import cached_property

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

from yarl import URL
from platformdirs import user_cache_dir
from diskcache import Cache

from .constants import OGCAPI, OGCPATH, USGSCollection

APPLICATION_PREFIX: Final[str] = "HYDROTOOLS"
"""A prefix to use in order to preserve application setting isolation."""

SUBPACKAGE_NAME: Final[str] = __name__.split(".")[1]
"""Name of subpackage."""

KEY_SEPARATOR: Final[str] = os.environ.get(f"{APPLICATION_PREFIX}_KEY_SEPARATOR", "_")
"""A separator to use for environment variable keys."""

_KEY_START: Final[str] = APPLICATION_PREFIX + KEY_SEPARATOR if APPLICATION_PREFIX else ""
"""Helper constant for the beginning of environment keys"""

def generate_default_user_cache_path(
        application: str = APPLICATION_PREFIX,
        subpackage: str = SUBPACKAGE_NAME
) -> Path:
    """Generate the Path to the default user cache.
    
    Args:
        application: The overall application name (e.g. "hydrotools"). Used for
            the main cache directory.
        subpackage: The specific subpackage name (e.g. "waterdata_client"). Used
            for the subdirectory under the main cache directory.
    
    Returns:
        pathlib.Path to the system specific user cache directory.
    """
    return Path(user_cache_dir(application.lower())) / subpackage

class EnvironmentKey(StrEnum):
    """Keys for environment variables."""
    BASE_URL = f"{_KEY_START}USGS_BASE_URL"
    SCHEMA_PATH = f"{_KEY_START}OGC_SCHEMA_PATH"
    API = f"{_KEY_START}OGC_API"
    COLLECTION = f"{_KEY_START}USGS_COLLECTION"
    PATH = f"{_KEY_START}OGC_PATH"
    CACHE_DIRECTORY = f"{_KEY_START}CACHE_DIRECTORY"
    CACHE_EXPIRES = f"{_KEY_START}CACHE_EXPIRES"
    CONCURRENCY = f"{_KEY_START}CONCURRENCY"
    RETRIES = f"{_KEY_START}RETRIES"
    TIMEOUT = f"{_KEY_START}TIMEOUT"
    API_KEY = f"{_KEY_START}USGS_API_KEY"

    @classmethod
    def describe_keys(cls) -> str:
        """Create a text listing for each configured key."""
        return os.linesep.join(list(cls))

    @classmethod
    def print_keys(cls, stream: TextIO = stdout, flush: bool = False) -> None:
        """Write each key to a buffer

        Args:
            stream: Where to write each key. Defaults to stdout
            flush: Whether to flush the buffer after writing.
        """
        stream.write(cls.describe_keys())

        if flush:
            stream.flush()

@dataclass(frozen=True)
class _Settings:
    """Default settings for hydrotools WaterData clients.

    Attributes:
        usgs_base_url: The root URL for USGS OGC API services.
        schema_path: Specific path appended to base url to retrieve schema.
        default_api: Default api for individual client get requests.
        default_collection: Default USGS OGC API collection for client get requests.
        default_path: Default path for individual client get requests.
        default_query: Default query parameters.
        cache_dir: OS-specific directory for persistent storage.
        cache_expires: Seconds after-which items in cache expire.
        default_concurrency: Max simultaneous requests.
        default_retries: Number of retry attempts.
        timeout_seconds: Number of seconds to wait for response completion.
        usgs_api_key: Individual USGS API key for increased usage limits.
        schema_url: Returns URL to API schema from usgs_base_url, schema_path, and
            default_query.
        default_cache: Returns a diskcache.Cache object parameterized by cache_dir and
            cache_expires.
    """
    usgs_base_url: URL = URL("https://api.waterdata.usgs.gov/ogcapi/v0")
    schema_path: str = "openapi"
    default_api: OGCAPI = OGCAPI.COLLECTIONS
    default_collection: USGSCollection = USGSCollection.CONTINUOUS
    default_path: OGCPATH = OGCPATH.ITEMS
    default_query: dict[str, Any] = field(default_factory=lambda: {"f": "json"})
    cache_dir: Path = field(default_factory=generate_default_user_cache_path)
    cache_expires: int = 604_800
    default_concurrency: int = 10
    default_retries: int = 3
    timeout_seconds: int = 900
    usgs_api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> Self:
        """Creates a configuration object using environment variable overrides.

        Returns:
            A _Settings instance with values pulled from HYDROTOOLS_ prefixed 
            environment variables if they exist.
        """
        return cls(
            usgs_base_url=URL(os.getenv(EnvironmentKey.BASE_URL, cls.usgs_base_url)),
            schema_path=os.getenv(EnvironmentKey.SCHEMA_PATH, cls.schema_path),
            default_api=OGCAPI(os.getenv(EnvironmentKey.API, cls.default_api)),
            default_collection=USGSCollection(
                os.getenv(EnvironmentKey.COLLECTION, cls.default_collection)
            ),
            default_path=OGCPATH(os.getenv(EnvironmentKey.PATH, cls.default_path)),
            cache_dir=Path(
                os.getenv(EnvironmentKey.CACHE_DIRECTORY, generate_default_user_cache_path())
            ),
            cache_expires=int(os.getenv(EnvironmentKey.CACHE_EXPIRES, cls.cache_expires)),
            default_concurrency=int(os.getenv(EnvironmentKey.CONCURRENCY, cls.default_concurrency)),
            default_retries=int(os.getenv(EnvironmentKey.RETRIES, cls.default_retries)),
            timeout_seconds=int(os.getenv(EnvironmentKey.TIMEOUT, cls.timeout_seconds)),
            usgs_api_key=os.getenv(EnvironmentKey.API_KEY, cls.usgs_api_key)
            )

    @cached_property
    def schema_url(self) -> URL:
        """Builds and returns schema URL."""
        return (self.usgs_base_url / self.schema_path).with_query(self.default_query)

    @cached_property
    def default_cache(self) -> Cache:
        """Builds and returns ClientCache object using defaults."""
        return Cache(str(self.cache_dir))

SETTINGS: Final[_Settings] = _Settings.from_env()
"""Package-wide default settings."""

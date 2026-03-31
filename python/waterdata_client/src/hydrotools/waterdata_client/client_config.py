"""Package-wide configuration and defaults.

Most modules will just import the default configuration:
>>> from .client_config import CLIENT_DEFAULT_CONFIGURATION
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final
from functools import cached_property

from yarl import URL
from platformdirs import user_cache_dir

from diskcache import Cache

@dataclass(frozen=True)
class ClientConfig:
    """Default settings for hydrotools WaterData clients.

    Attributes:
        usgs_base_url: The root URL for USGS OGC API services.
        schema_path: Specific path appended to base url to retrieve schema.
        default_query: Default query parameters.
        cache_dir: OS-specific directory for persistent storage.
        cache_expires: Seconds after-which items in cache expire.
        default_concurrency: Max simultaneous requests.
        default_retries: Number of retry attempts.
        timeout_seconds: Number of seconds to wait for response completion.
    
    Properties:
        schema_url: Returns URL to API schema from usgs_base_url, schema_path, and
            default_query.
        default_cache: Returns a diskcache.Cache object parameterized by cache_dir and
            cache_expires.
    """
    usgs_base_url: URL = URL("https://api.waterdata.usgs.gov/ogcapi/v0")
    schema_path: str = "openapi"
    default_query: dict[str, Any] = field(default_factory=lambda: {"f": "json"})
    cache_dir: Path = field(
        default_factory=lambda: Path(user_cache_dir("hydrotools")) / "waterdata_client"
    )
    cache_expires: int = 604_800
    default_concurrency: int = 10
    default_retries: int = 3
    timeout_seconds: int = 900

    @cached_property
    def schema_url(self) -> URL:
        """Builds and returns schema URL."""
        return (self.usgs_base_url / self.schema_path).with_query(self.default_query)

    @cached_property
    def default_cache(self) -> Cache:
        """Builds and returns ClientCache object using defaults."""
        return Cache(str(self.cache_dir))

CLIENT_DEFAULT_CONFIGURATION: Final[ClientConfig] = ClientConfig()
"""Package-wide defaults."""

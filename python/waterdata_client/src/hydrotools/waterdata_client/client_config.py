"""Package-wide configuration and defaults."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from yarl import URL
from platformdirs import user_cache_dir

from .client_cache import ClientCache

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

    @property
    def schema_url(self) -> URL:
        """Builds and returns schema URL."""
        return (self.usgs_base_url / self.schema_path).with_query(self.default_query)

    def build_cache(self) -> ClientCache:
        """Builds and returns ClientCache object using defaults."""
        return ClientCache(
            cache_dir=self.cache_dir,
            expire=self.cache_expires
        )

"""Persistent disk caching for client data."""
from pathlib import Path
from typing import Any, Optional

from diskcache import Cache

class ClientCache:
    """Handles persistent disk caching.

    Attributes:
        cache_dir: Path to cache directory.
        expire: Seconds until items expire.
        _cache: The underlying diskcache.Cache instance.
    """

    def __init__(
            self,
            cache_dir: Path,
            expire: int
        ) -> None:
        """Initializes the cache directory.

        Args:
            cache_dir: Path to cache directory.
            expire: Seconds until items expire.
        """
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache = Cache(str(self.cache_dir))
        self.expire = expire

    def __setitem__(self, key: str, value: Any) -> None:
        """General purpose method to cache data returns.

        Args:
            key: Unique identifier (e.g., the URL or a hash of parameters).
            value: The data to store.
        """
        self._cache.set(key, value, expire=self.expire)

    def __getitem__(self, key: str) -> Optional[Any]:
        """Retrieves data from the disk cache.

        Args:
            key: The unique identifier for the data.
        """
        return self._cache.get(key)

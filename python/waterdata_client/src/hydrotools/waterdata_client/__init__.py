"""High-level client interfaces for USGS water data.

This package provides both synchronous and asynchronous clients for 
interacting with OGC-compliant APIs.
"""

from .async_web_client import AsyncWebClient, get_all
from ._version import __version__

__all__ = ["AsyncWebClient", "get_all"]

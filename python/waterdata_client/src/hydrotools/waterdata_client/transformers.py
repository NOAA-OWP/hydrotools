"""Defines transformation methods for handling deserialized JSON responses from
USGS OGC APIs.
"""
from typing import Any, Protocol, TypeVar, runtime_checkable

import pandas as pd
import geopandas as gpd

TransformedResponse_co = TypeVar("TransformedResponse_co", covariant=True)
"""Generic transformed response type for transformer methods."""

@runtime_checkable
class ResponseTransformer(Protocol[TransformedResponse_co]):
    """Protocol definition for response transformer methods."""
    def __call__(self, data: list[dict[str, Any]]) -> TransformedResponse_co:
        """Transforms a list of JSON-derived dictionaries to the target type."""
        ...

def to_geodataframe(data: list[dict[str, Any]]) -> gpd.GeoDataFrame:
    """Transforms a list of GeoJSON-derived dictionaries to a single GeoDataFrame.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
    
    Returns:
        Transformed and concatenated responses in a single GeoDataFrame.
    """
    return gpd.GeoDataFrame(pd.concat([gpd.GeoDataFrame(d) for d in data], ignore_index=True))

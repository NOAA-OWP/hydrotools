"""Defines transformation methods for handling deserialized JSON responses from
USGS OGC APIs.
"""
from typing import Any, Protocol, TypeVar, runtime_checkable

import pandas as pd
import geopandas as gpd

TransformedResponse_co = TypeVar("TransformedResponse_co", covariant=True)
"""Generic transformed response type for transformer methods."""

class NoDataError(Exception):
    """Custom exception raised when all data retrieval fails."""

@runtime_checkable
class ResponseTransformer(Protocol[TransformedResponse_co]):
    """Protocol definition for response transformer methods."""
    def __call__(self, data: list[dict[str, Any]]) -> TransformedResponse_co:
        """Transforms a list of JSON-derived dictionaries to the target type."""
        ...

def raise_on_no_data(data: list[dict[str, Any]]) -> None:
    """Raises if data list is empty or all items are None.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Check for empty list
    if not data:
        raise NoDataError("No data available to parse.")

    # Check for all None
    if all(d is None for d in data):
        raise NoDataError("All data returned were None.")

    # Check for no features
    if sum([d.get("numberReturned", 0) for d in data]) == 0:
        raise NoDataError("All responses returned 0 features.")

def check_features(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Checks a list of GeoJSON-derived dictionaries for minimal data.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
    
    Returns:
        Original responses in a single GeoDataFrame.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Check for data
    raise_on_no_data(data)
    return data

def to_geodataframe(data: list[dict[str, Any]]) -> gpd.GeoDataFrame:
    """Transforms a list of GeoJSON-derived dictionaries to a single GeoDataFrame.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
    
    Returns:
        Transformed and concatenated responses in a single GeoDataFrame.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Check for data
    raise_on_no_data(data)

    # Transform data
    return gpd.GeoDataFrame(pd.concat([
        gpd.GeoDataFrame.from_features(d) for d in data if d is not None
        ], ignore_index=True))

def to_dataframe(data: list[dict[str, Any]]) -> pd.DataFrame:
    """Transforms a list of GeoJSON-derived dictionaries to a single DataFrame.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
    
    Returns:
        Transformed and concatenated responses in a single DataFrame.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Check for data
    raise_on_no_data(data)

    # Transform data
    return pd.concat([
        pd.json_normalize(d, record_path=['features']) for d in data if d is not None
        ], ignore_index=True)

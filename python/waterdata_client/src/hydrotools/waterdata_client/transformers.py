"""Defines transformation methods for handling deserialized JSON responses from
USGS OGC APIs.
"""
from typing import Any, Protocol, TypeVar, runtime_checkable, Optional

import pandas as pd
from pandas._typing import Renamer
import geopandas as gpd

from .constants import HYDROTOOLS_DATAFRAME_COLUMN_MAPPING

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

def default_column_mapper(label: str) -> str:
    """Applies default column mapper to GeoDataFrame or DataFrame column labels."""
    return HYDROTOOLS_DATAFRAME_COLUMN_MAPPING.get(label, label)

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
        Original list of responses.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Check for data
    raise_on_no_data(data)
    return data

def to_geodataframe(
        data: list[dict[str, Any]],
        column_mapper: Optional[Renamer] = default_column_mapper
) -> gpd.GeoDataFrame:
    """Transforms a list of GeoJSON-derived dictionaries to a single GeoDataFrame.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
        column_mapper: Dict-like or function transformations to apply to that
            column values. Passed directly to GeoDataFrame.rename with axis=1.
    
    Returns:
        Transformed and concatenated responses in a single GeoDataFrame.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Check for data
    raise_on_no_data(data)

    # Flatten features
    flat_features = []
    for d in data:
        if d and "features" in d:
            flat_features.extend(d["features"])

    # Transform data
    dataframe = gpd.GeoDataFrame.from_features(flat_features)

    # Apply optional mapping
    if column_mapper is None:
        return dataframe
    return dataframe.rename(mapper=column_mapper, axis=1)

def to_dataframe(
        data: list[dict[str, Any]],
        column_mapper: Optional[Renamer] = default_column_mapper
) -> pd.DataFrame:
    """Transforms a list of GeoJSON-derived dictionaries to a single DataFrame.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
        column_mapper: Dict-like or function transformations to apply to that
            column values. Passed directly to DataFrame.rename with axis=1.
    
    Returns:
        Transformed and concatenated responses in a single DataFrame.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Check for data
    raise_on_no_data(data)

    # Flatten features
    flat_features = []
    for d in data:
        if d and "features" in d:
            flat_features.extend(d["features"])

    # Transform data
    dataframe = pd.json_normalize(flat_features)

    # Apply optional mapping
    if column_mapper is None:
        return dataframe
    return dataframe.rename(mapper=column_mapper, axis=1)

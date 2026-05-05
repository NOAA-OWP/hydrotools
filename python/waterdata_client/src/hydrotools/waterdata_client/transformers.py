"""Defines transformation methods for handling deserialized JSON responses from
USGS OGC APIs.
"""
from typing import (Any, Protocol, TypeVar, runtime_checkable, Optional,
    Callable, cast)

import pandas as pd
from pandas._typing import Renamer
import geopandas as gpd

from .constants import HYDROTOOLS_DATAFRAME_COLUMN_MAPPING, HydroToolsColumn

TransformedResponseT_co = TypeVar("TransformedResponseT_co", covariant=True)
"""Generic transformed response type for transformer methods."""

class NoDataError(Exception):
    """Custom exception raised when all data retrieval fails."""

@runtime_checkable
class ResponseTransformer(Protocol[TransformedResponseT_co]):
    """Protocol definition for response transformer methods."""
    def __call__(self, data: list[dict[str, Any]]) -> TransformedResponseT_co:
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

# pickle/multiprocessing friendly optimization strategies

DataFrameT = TypeVar("DataFrameT", bound=pd.DataFrame)
"""pandas.DataFrame or geopandas.GeoDataFrame"""

SeriesOptimizer = Callable[[pd.Series], pd.Series]
"""A callable that takes a pandas.Series and returns a memory-optimized version
of the same."""

def optimize_series_categorical(s: pd.Series) -> pd.Series:
    """Applies pandas.Categorical type to a pandas.Series."""
    return s.astype("category")

def optimize_series_datetime_utc(s: pd.Series) -> pd.Series:
    """Applies pandas.to_datetime to a pandas.Series. Converts to UTC and strips
    timezone awareness. Defaults to unit 's' (seconds).
    """
    return pd.to_datetime(s, utc=True).dt.tz_localize(None).astype("datetime64[s]")

def optimize_series_float32(s: pd.Series) -> pd.Series:
    """Applies float32 type to a pandas.Series."""
    return pd.to_numeric(s).astype("float32")

SERIES_OPTIMIZERS: dict[HydroToolsColumn, SeriesOptimizer] = {
    # Categorical optimizations
    HydroToolsColumn.USGS_SITE_CODE: optimize_series_categorical,
    HydroToolsColumn.USACE_GAUGE_ID: optimize_series_categorical,
    HydroToolsColumn.NWS_LID: optimize_series_categorical,
    HydroToolsColumn.PARAMETER_CODE: optimize_series_categorical,
    HydroToolsColumn.STATISTIC_ID: optimize_series_categorical,
    HydroToolsColumn.MEASUREMENT_UNIT: optimize_series_categorical,
    HydroToolsColumn.VARIABLE_NAME: optimize_series_categorical,
    HydroToolsColumn.QUALIFIERS: optimize_series_categorical,
    HydroToolsColumn.CONFIGURATION: optimize_series_categorical,
    HydroToolsColumn.APPROVAL_STATUS: optimize_series_categorical,
    HydroToolsColumn.ID: optimize_series_categorical,
    HydroToolsColumn.TIME_SERIES_ID: optimize_series_categorical,
    HydroToolsColumn.GEOMETRY_TYPE: optimize_series_categorical,
    HydroToolsColumn.GEO_FEATURE_ID: optimize_series_categorical,
    HydroToolsColumn.TYPE: optimize_series_categorical,

    # Numeric optimizations
    HydroToolsColumn.VALUE: optimize_series_float32,

    # DateTime optimizations
    HydroToolsColumn.VALUE_TIME: optimize_series_datetime_utc,
    HydroToolsColumn.LAST_MODIFIED: optimize_series_datetime_utc,
    HydroToolsColumn.START: optimize_series_datetime_utc,
    HydroToolsColumn.END: optimize_series_datetime_utc
}
"""Mapping from canonical hydrotools columns to optimization function."""

def optimize_dataframe(
        dataframe: DataFrameT,
        optimizations: Optional[dict[HydroToolsColumn, SeriesOptimizer]] = None
) -> DataFrameT:
    """Apply column-specific optimizations to a dataframe.
    
    Args:
        dataframe: Dataframe to be optimized.
        optimizations: Mapping from column labels to optimization functions.
            Defaults to hydrotools canonical optimizations.
    
    Returns:
        Optimized dataframe.
    """
    if optimizations is None:
        optimizations = SERIES_OPTIMIZERS

    # Copy to avoid set with copy error. Cast back to original dataframe type.
    df = cast(DataFrameT, dataframe.copy())

    # Look for optimizable columns
    for column, optimizer in optimizations.items():
        if column.value in df.columns:
            # Apply the conversion
            df[column.value] = optimizer(df[column.value])

    return df

def to_optimized_geodataframe(
        data: list[dict[str, Any]],
        column_mapper: Optional[Renamer] = default_column_mapper
) -> gpd.GeoDataFrame:
    """Transforms a list of GeoJSON-derived dictionaries to a single GeoDataFrame
    with memory-optimizations.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
        column_mapper: Dict-like or function transformations to apply to that
            column values. Passed directly to GeoDataFrame.rename with axis=1.
    
    Returns:
        Transformed and concatenated responses in a single GeoDataFrame.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Apply base transformation and optimize
    return optimize_dataframe(to_geodataframe(
        data=data, column_mapper=column_mapper
    ))

def to_optimized_dataframe(
        data: list[dict[str, Any]],
        column_mapper: Optional[Renamer] = default_column_mapper
) -> pd.DataFrame:
    """Transforms a list of GeoJSON-derived dictionaries to a single DataFrame
    with memory-optimizations.
    
    Args:
        data: A list of deserialized GeoJSON responses from an OGC-compliant API.
        column_mapper: Dict-like or function transformations to apply to that
            column values. Passed directly to DataFrame.rename with axis=1.
    
    Returns:
        Transformed and concatenated responses in a single DataFrame.
    
    Raises:
        NoDataError if data is empty or all items are None.
    """
    # Apply base transformation and optimize
    return optimize_dataframe(to_dataframe(
        data=data, column_mapper=column_mapper
    ))

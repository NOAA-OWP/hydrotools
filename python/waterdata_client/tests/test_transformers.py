"""Tests for the transformers module."""
import pytest
import numpy as np
import pandas as pd
import geopandas as gpd
from hydrotools.waterdata_client.constants import HydroToolsColumn
from hydrotools.waterdata_client.transformers import (
    to_dataframe,
    to_geodataframe,
    raise_on_no_data,
    NoDataError,
    optimize_dataframe,
    to_optimized_dataframe,
    to_optimized_geodataframe
)

@pytest.fixture
def mock_geojson_response():
    """Mock OGC FeatureCollection response."""
    return [{
        'type': 'FeatureCollection',
        'numberReturned': 2,
        'features': [
            {
                'type': 'Feature',
                'properties': {
                    'id': '1',
                    'monitoring_location_id': 'USGS-01',
                    'value': '1.1',
                    'time': '2026-05-05T18:15:00+00:00'
                },
                'geometry': {'type': 'Point', 'coordinates': [0, 0]}
            },
            {
                'type': 'Feature',
                'properties': {
                    'id': '2',
                    'monitoring_location_id': 'USGS-01',
                    'value': '2.2',
                    'time': '2026-05-05T18:30:00+00:00'
                },
                'geometry': {'type': 'Point', 'coordinates': [1, 1]}
            }
        ]
    }]

@pytest.fixture
def empty_geojson_response():
    """Mock response with zero features."""
    return [{
        'type': 'FeatureCollection',
        'numberReturned': 0,
        'features': []
    }]

def test_raise_on_no_data_empty():
    """Verify NoDataError on empty input."""
    with pytest.raises(NoDataError, match="No data available"):
        raise_on_no_data([])

def test_raise_on_no_data_none():
    """Verify NoDataError when all items are None."""
    with pytest.raises(NoDataError, match="All data returned were None"):
        raise_on_no_data([None, None])

def test_raise_on_no_data_zero_features(empty_geojson_response):
    """Verify NoDataError when numberReturned is 0."""
    with pytest.raises(NoDataError, match="returned 0 features"):
        raise_on_no_data(empty_geojson_response)

def test_to_dataframe_success(mock_geojson_response):
    """Verify JSON to DataFrame flattening."""
    df = to_dataframe(mock_geojson_response, column_mapper=None)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    # Verify json_normalize dot notation
    assert "properties.monitoring_location_id" in df.columns
    assert df.loc[0, "properties.value"] == "1.1"

def test_to_geodataframe_success(mock_geojson_response):
    """Verify JSON to GeoDataFrame conversion."""
    gdf = to_geodataframe(mock_geojson_response, column_mapper=None)

    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 2
    assert "monitoring_location_id" in gdf.columns
    assert hasattr(gdf, "geometry")
    assert gdf.geometry.iloc[0].x == 0

def test_transformer_integration_logic(mock_geojson_response):
    """Verify that multiple collections are concatenated correctly."""
    # Simulate two pages/batches of data
    multi_batch = mock_geojson_response + mock_geojson_response

    df = to_dataframe(multi_batch, column_mapper=None)
    assert len(df) == 4
    assert df.iloc[0]["properties.id"] == df.iloc[2]["properties.id"]

##
def test_optimize_dataframe_dtypes(mock_geojson_response):
    """Verify that columns are correctly cast to optimized types."""
    # Create a raw dataframe with strings and float64
    df = pd.DataFrame({
        HydroToolsColumn.VALUE: ["1.1", "2.2"],
        HydroToolsColumn.USGS_SITE_CODE: ["USGS-01", "USGS-01"],
        HydroToolsColumn.VALUE_TIME: ["2026-05-01T12:00:00Z", "2026-05-01T13:00:00Z"]
    })

    optimized_df = optimize_dataframe(df)

    # Check numeric downcasting
    assert optimized_df[HydroToolsColumn.VALUE].dtype == np.float32

    # Check categorical casting
    assert isinstance(optimized_df[HydroToolsColumn.USGS_SITE_CODE].dtype, pd.CategoricalDtype)

    # Check datetime conversion and TZ stripping
    assert pd.api.types.is_datetime64_any_dtype(optimized_df[HydroToolsColumn.VALUE_TIME])
    assert optimized_df[HydroToolsColumn.VALUE_TIME].dt.tz is None

def test_to_optimized_geodataframe_preserves_type(mock_geojson_response):
    """Verify that optimized GeoDataFrames retain their spatial identity."""
    gdf = to_optimized_geodataframe(mock_geojson_response)

    assert isinstance(gdf, gpd.GeoDataFrame)
    assert hasattr(gdf, "geometry")
    # Verify optimization was applied
    assert isinstance(gdf[HydroToolsColumn.USGS_SITE_CODE].dtype, pd.CategoricalDtype)

def test_to_optimized_dataframe_integration(mock_geojson_response):
    """Test full pipeline from JSON to optimized tabular format."""
    df = to_optimized_dataframe(mock_geojson_response)

    # Verify columns are correctly mapped and optimized
    assert HydroToolsColumn.VALUE in df.columns
    assert df[HydroToolsColumn.VALUE].dtype == np.float32
    assert df[HydroToolsColumn.VALUE_TIME].dtype == "datetime64[s]"

def test_optimize_dataframe_custom_strategies():
    """Verify that custom optimization dictionaries can be injected."""
    df = pd.DataFrame({
        "test_col": [1, 2, 3],
        "value": ["1.0", "2.0", "3.0"]
        })

    # Default should leave 'test_col' untouched
    optimized_df = optimize_dataframe(df)
    assert optimized_df["test_col"].dtype == np.int64
    assert optimized_df["value"].dtype == np.float32

    # Custom optimizer
    optimized_df = optimize_dataframe(
        df,
        transformations={
            HydroToolsColumn.VALUE: pd.to_numeric
        }
        )
    assert optimized_df["value"].dtype == np.float64

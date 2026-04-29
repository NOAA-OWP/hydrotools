"""Tests for the transformers module."""
import pytest
import pandas as pd
import geopandas as gpd
from hydrotools.waterdata_client.transformers import (
    to_dataframe,
    to_geodataframe,
    raise_on_no_data,
    NoDataError
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
                    'value': '1.1'
                },
                'geometry': {'type': 'Point', 'coordinates': [0, 0]}
            },
            {
                'type': 'Feature',
                'properties': {
                    'id': '2',
                    'monitoring_location_id': 'USGS-01',
                    'value': '2.2'
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

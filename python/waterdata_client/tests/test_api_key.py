import pytest
from unittest.mock import patch

import hydrotools.waterdata_client.clients.continuous as continuous
from hydrotools.waterdata_client.client_config import _Settings

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

def test_api_key_handling(mock_geojson_response):
    """Verify that setting api_key in get overrides the default."""
    client = continuous.ContinuousClient()

    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get_all:
        mock_get_all.return_value = mock_geojson_response

        client.get(api_key="ABCDEF123456")

        _, kwargs = mock_get_all.call_args
        assert "api_key=ABCDEF123456" in str(kwargs["urls"][0])

def test_api_key_handling_env(mock_geojson_response, monkeypatch):
    """Verify that api key is pulled in from the environment."""
    # Update environment
    monkeypatch.setenv("HYDROTOOLS_USGS_API_KEY", "123456ABCDEF")

    # Regenerate settings
    fresh_settings = _Settings.from_env()

    # Swap settings
    monkeypatch.setattr(continuous, "SETTINGS", fresh_settings)

    # Test
    client = continuous.ContinuousClient()

    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get_all:
        mock_get_all.return_value = mock_geojson_response

        client.get()

        _, kwargs = mock_get_all.call_args
        assert "api_key=123456ABCDEF" in str(kwargs["urls"][0])

    # Test override
    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get_all:
        mock_get_all.return_value = mock_geojson_response

        client.get(api_key="987654ABCDEF")

        _, kwargs = mock_get_all.call_args
        assert "api_key=987654ABCDEF" in str(kwargs["urls"][0])

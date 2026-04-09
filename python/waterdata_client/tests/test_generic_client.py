import pytest
from unittest.mock import MagicMock, patch
from yarl import URL

from hydrotools.waterdata_client.generic_client import GenericClient
from hydrotools.waterdata_client.constants import USGSCollection, OGCPATH, OGCAPI
from hydrotools.waterdata_client.async_web_client import ResponseContentType

class MockUSGSClient(GenericClient):
    _endpoint = USGSCollection.CONTINUOUS
    _path = OGCPATH.ITEMS

@pytest.fixture
def mock_client():
    """Provides a MockUSGSClient instance for testing."""
    return MockUSGSClient(concurrency_limit=5, max_retries=2)

def test_client_initialization(mock_client):
    """Verify instance attributes are correctly set from __init__."""
    assert mock_client.concurrency_limit == 5
    assert mock_client.max_retries == 2
    assert mock_client._endpoint == USGSCollection.CONTINUOUS

def test_get_responses_queries_only(mock_client):
    """Verify _get_responses correctly dispatches a query-only request."""
    with patch("hydrotools.waterdata_client.generic_client.get_all") as mock_get:
        mock_get.return_value = [{"data": "test"}]

        queries = [{"parameter_code": "00060"}]
        results = mock_client._get_responses(queries=queries)

        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args

        assert len(kwargs["urls"]) == 1
        assert "parameter_code=00060" in str(kwargs["urls"][0])
        assert kwargs["concurrency_limit"] == 5
        assert results == [{"data": "test"}]

def test_get_responses_feature_ids_only(mock_client):
    """Verify _get_responses correctly dispatches an ID-only request."""
    with patch("hydrotools.waterdata_client.generic_client.get_all") as mock_get:
        feature_ids = ["USGS-123", "USGS-456"]
        mock_client._get_responses(feature_ids=feature_ids)
        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args
        assert len(kwargs["urls"]) == 2
        assert all("items/USGS-" in str(u) for u in kwargs["urls"])

def test_get_responses_paired_batch(mock_client):
    """Verify _get_responses handles paired IDs and queries."""
    with patch("hydrotools.waterdata_client.generic_client.get_all") as mock_get:
        ids = ["USGS-1"]
        queries = [{"f": "json"}]
        mock_client._get_responses(feature_ids=ids, queries=queries)
        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args
        # URL should contain both the ID and the query param
        url_str = str(kwargs["urls"][0])
        assert "USGS-1" in url_str
        assert "f=json" in url_str

def test_bad_client_raises():
    """Verify RuntimeError is raised if _endpoint is missing."""
    with pytest.raises(TypeError,
        match="failed to define required attribute: _endpoint"):
        class BadClient(GenericClient):
            _endpoint = None

    with pytest.raises(TypeError,
        match="failed to define required attribute: _server"):
        class BadClient(GenericClient):
            _server = None

    with pytest.raises(TypeError,
        match="failed to define required attribute: _api"):
        class BadClient(GenericClient):
            _api = None

    with pytest.raises(TypeError,
        match="failed to define required attribute: _path"):
        class BadClient(GenericClient):
            _path = None

    with pytest.raises(TypeError,
        match="failed to define required attribute: _content_type"):
        class BadClient(GenericClient):
            _content_type = None

def test_get_responses_default_request(mock_client):
    """Verify a parameterless call builds a default URL."""
    with patch("hydrotools.waterdata_client.generic_client.get_all") as mock_get:
        mock_client._get_responses()
        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args
        # Should result in a single URL using default path/endpoint
        assert len(kwargs["urls"]) == 1

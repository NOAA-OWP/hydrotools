import pytest
from unittest.mock import patch

from yarl import URL

from hydrotools.waterdata_client.base_client import BaseClient
from hydrotools.waterdata_client.constants import USGSCollection, OGCPATH

class MockUSGSClient(BaseClient):
    _endpoint = USGSCollection.CONTINUOUS
    _path = OGCPATH.ITEMS
    _max_pages = 2

    def get(self, **kwargs):
        return self._get_json_responses(**kwargs)

@pytest.fixture
def mock_client():
    """Provides a MockUSGSClient instance for testing."""
    return MockUSGSClient(concurrency_limit=5, max_retries=2)

def test_client_initialization(mock_client):
    """Verify instance attributes are correctly set from __init__."""
    assert mock_client.concurrency_limit == 5
    assert mock_client.max_retries == 2
    assert mock_client._endpoint == USGSCollection.CONTINUOUS

def test_get_json_responses_queries_only(mock_client):
    """Verify _get_json_responses correctly dispatches a query-only request."""
    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get:
        mock_get.return_value = [{"data": "test"}]

        queries = [{"parameter_code": "00060"}]
        results = mock_client._get_json_responses(queries=queries)

        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args

        assert len(kwargs["urls"]) == 1
        assert "parameter_code=00060" in str(kwargs["urls"][0])
        assert kwargs["concurrency_limit"] == 5
        assert results == [{"data": "test"}]

def test_get_json_responses_feature_ids_only(mock_client):
    """Verify _get_json_responses correctly dispatches an ID-only request."""
    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get:
        feature_ids = ["USGS-123", "USGS-456"]
        mock_client._get_json_responses(feature_ids=feature_ids)
        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args
        assert len(kwargs["urls"]) == 2
        assert all("items/USGS-" in str(u) for u in kwargs["urls"])

def test_get_json_responses_paired_batch(mock_client):
    """Verify _get_json_responses handles paired IDs and queries."""
    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get:
        ids = ["USGS-1"]
        queries = [{"f": "json"}]
        mock_client._get_json_responses(feature_ids=ids, queries=queries)
        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args
        # URL should contain both the ID and the query param
        url_str = str(kwargs["urls"][0])
        assert "USGS-1" in url_str
        assert "f=json" in url_str

def test_bad_client_attribute_raises():
    """Verify RuntimeError is raised if _endpoint is missing."""
    with pytest.raises(TypeError,
        match="failed to define required attribute: _endpoint"):
        class BadClient1(BaseClient):
            _endpoint = None

    with pytest.raises(TypeError,
        match="failed to define required attribute: _server"):
        class BadClient2(BaseClient):
            _server = None

    with pytest.raises(TypeError,
        match="failed to define required attribute: _api"):
        class BadClient3(BaseClient):
            _api = None

    with pytest.raises(TypeError,
        match="failed to define required attribute: _path"):
        class BadClient4(BaseClient):
            _path = None

    with pytest.raises(TypeError,
        match="failed to define required attribute: _content_type"):
        class BadClient5(BaseClient):
            _content_type = None

def test_bad_client_get_raises():
    """Verify RuntimeError is raised if _endpoint is missing."""
    with pytest.raises(NotImplementedError,
        match="must implement a public 'get' method"):
        class BadClient(BaseClient):
            _endpoint = USGSCollection.LATEST_CONTINUOUS

def test_get_json_responses_default_request(mock_client):
    """Verify a parameterless call builds a default URL."""
    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get:
        mock_client._get_json_responses()
        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args
        # Should result in a single URL using default path/endpoint
        assert len(kwargs["urls"]) == 1

def test_get_json_responses_pagination(mock_client):
    """Verify pagination follow logic using a mock sequence."""
    resp1, resp2 = (
        {"data": "page1", "links": [{"rel": "next", "href": "http://api/page2"}]},
        {"data": "page2"}
    )

    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get:
        mock_get.side_effect = [[resp1], [resp2]]

        # This triggers the 'for' loop in _get_json_responses
        results = mock_client._get_json_responses()

    assert mock_get.call_count == 2
    assert len(results) == 2
    assert results == [resp1, resp2]

    # Verify the second call used the URL extracted from the first response
    last_call_kwargs = mock_get.call_args.kwargs
    assert last_call_kwargs["urls"] == [URL("http://api/page2")]

def test_get_json_responses_filters_non_dict(mock_client):
    """Verify that None and bytes are filtered out of results."""
    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get:
        mock_get.return_value = [{"ok": True}, None, b"binary"]

        results = mock_client._get_json_responses()

        assert results == [{"ok": True}]

def test_get_json_responses_max_pages_limit(mock_client):
    """Verify the loop stops at _max_pages even if 'next' exists."""
    response = {"links": [{"rel": "next", "href": "http://more"}]}
    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get:
        # Always return a 'next' link to simulate infinite data
        mock_get.return_value = [response]

        results = mock_client._get_json_responses()

        # Should only be called twice based on _max_pages
        assert mock_get.call_count == 2
        assert results == [response] * 2

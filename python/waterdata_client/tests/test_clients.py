"""Tests for the auto-generated clients module."""
import pytest
from unittest.mock import patch
from yarl import URL

# Import a few representative generated clients
from hydrotools.waterdata_client import (
    AgencyCodesClient,
    MonitoringLocationsClient,
    DailyClient,
    ContinuousClient
)

@pytest.mark.parametrize("client_class, test_args, expected_query_subset", [
    # Test AgencyCodesClient: Verify kebab-case mapping (bbox-crs)
    (
        AgencyCodesClient,
        {"agency_name": "USGS", "bbox_crs": URL("http://epsg.io/4326")},
        {"agency_name": "USGS", "bbox-crs": "http://epsg.io/4326"}
    ),
    # Test MonitoringLocationsClient: Verify identifier sanitization (query_filter -> filter)
    (
        MonitoringLocationsClient,
        {"query_filter": "huc=01010001"},
        {"filter": "huc=01010001"}
    ),
    # Test DailyClient: Verify numeric and default types
    (
        DailyClient,
        {"limit": 50, "parameter_code": "00060"},
        {"limit": 50, "parameter_code": "00060"}
    ),
    # Test ContinuousClient: Verify Literal/Enum types
    (
        ContinuousClient,
        {"approval_status": "Approved"},
        {"approval_status": "Approved"}
    )
])
def test_generated_client_get_mapping(client_class, test_args, expected_query_subset):
    """Verify that generated get methods correctly pack arguments into API query keys."""
    client = client_class()

    # We patch the internal pipeline to inspect the queries before network I/O
    with patch.object(client_class, "_get_json_responses") as mock_pipeline:
        client.get(**test_args)

        # Ensure the pipeline was called
        mock_pipeline.assert_called_once()

        # Extract the queries passed to the pipeline
        passed_queries = mock_pipeline.call_args.kwargs.get("queries", [])
        assert len(passed_queries) == 1

        for k, v in expected_query_subset.items():
            assert k in passed_queries[0]
            assert str(v) == str(passed_queries[0][k])

def test_generated_client_filters_none():
    """Verify that None arguments are excluded from the final query dictionary."""
    client = DailyClient()

    with patch.object(DailyClient, "_get_json_responses") as mock_pipeline:
        # Call with some Nones and some values
        client.get(limit=100, parameter_code=None)

        actual_query = mock_pipeline.call_args.kwargs.get("queries", [])[0]

        assert "limit" in actual_query
        assert actual_query["limit"] == 100
        # parameter_code should be stripped because it was None
        assert "parameter_code" not in actual_query

def test_generated_client_uses_correct_endpoint():
    """Verify that each client uses its assigned OGC collection endpoint."""
    clients_to_check = [
        (AgencyCodesClient, "agency-codes"),
        (MonitoringLocationsClient, "monitoring-locations"),
        (DailyClient, "daily")
    ]

    for client_class, expected_slug in clients_to_check:
        client = client_class()
        # Verify private attribute set by template
        assert client._endpoint.value == expected_slug

def test_get_all_is_called_with_client_config():
    """Verify that the high-level get method passes client settings to the network layer."""
    client = ContinuousClient(concurrency_limit=99, max_retries=5)

    # Patch the lower-level get_all called by _get_json_responses
    with patch("hydrotools.waterdata_client.base_client.get_all") as mock_get_all:
        mock_get_all.return_value = []

        client.get(limit=1)

        _, kwargs = mock_get_all.call_args
        assert kwargs["concurrency_limit"] == 99
        assert kwargs["max_retries"] == 5

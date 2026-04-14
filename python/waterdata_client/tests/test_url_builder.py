"""Tests functionality of url_builder methods."""
import pytest
from yarl import URL
from multidict import MultiDict
from hydrotools.waterdata_client.url_builder import (
    build_request,
    build_request_batch,
    build_request_batch_from_feature_ids,
    build_request_batch_from_queries
)
from hydrotools.waterdata_client.constants import OGCAPI, OGCPATH, USGSCollection
from hydrotools.waterdata_client.client_config import SETTINGS

def test_build_request_defaults():
    """Verify build_request uses SETTINGS defaults correctly."""
    test_url = build_request()

    expected_url = (
        URL(SETTINGS.usgs_base_url) /
        SETTINGS.default_api /
        SETTINGS.default_collection /
        SETTINGS.default_path
    ).with_query(SETTINGS.default_query)

    assert test_url == expected_url

def test_build_request_strings():
    """Verify build_request with string args."""
    test_url = build_request(
        server=URL("https://water.noaa.gov"),
        api="collections",
        endpoint="latest-continuous",
        path="queryables",
        feature_id="NWM-123",
        query={"limit": 50_000}
    )

    query_params = MultiDict(SETTINGS.default_query)
    query_params.update({"limit": 50_000})
    expected_url = (
        URL("https://water.noaa.gov") /
        "collections" /
        "latest-continuous" /
        "queryables" /
        "NWM-123"
    ).with_query(query_params)

    assert test_url == expected_url

def test_build_request_enums():
    """Verify build_request using enum args."""
    test_url = build_request(
        server=URL("https://water.noaa.gov"),
        api=OGCAPI.CONFORMANCE,
        endpoint=USGSCollection.LATEST_DAILY,
        path=OGCPATH.SCHEMA
    )

    expected_url = (
        URL("https://water.noaa.gov") /
        OGCAPI.CONFORMANCE /
        USGSCollection.LATEST_DAILY /
        OGCPATH.SCHEMA
    ).with_query(SETTINGS.default_query)

    assert test_url == expected_url

def test_build_request_query_merging():
    """Verify provided query parameters merge with and override defaults."""
    custom_query = {"parameter_code": "00060", "f": "geojson"}
    url = build_request(query=custom_query)

    # 'f' should be overridden to 'geojson', 'parameter_code' added
    assert url.query["f"] == "geojson"
    assert url.query["parameter_code"] == "00060"

def test_build_request_batch_valid():
    """Verify batch building with paired IDs and queries."""
    ids = ["ID1", "ID2"]
    queries = [{"p": "1"}, {"p": "2"}]

    urls = build_request_batch(ids, queries)

    assert len(urls) == 2
    assert "ID1" in str(urls[0]) and "p=1" in str(urls[0])
    assert "ID2" in str(urls[1]) and "p=2" in str(urls[1])

def test_build_request_batch_mismatch_raises():
    """Verify ValueError is raised when input lengths differ."""
    ids = ["ID1"]
    queries = [{"p": "1"}, {"p": "2"}]

    with pytest.raises(ValueError, match="Mismatched input lengths"):
        build_request_batch(ids, queries)

def test_build_request_batch_from_feature_ids():
    """Verify batch creation from a sequence of IDs."""
    ids = ["USGS-1", "USGS-2"]
    urls = build_request_batch_from_feature_ids(ids)

    assert len(urls) == 2
    assert all("items/USGS-" in str(u) for u in urls)

def test_build_request_batch_from_queries():
    """Verify batch creation from a sequence of query dicts."""
    queries = [{"site": "A"}, {"site": "B"}]
    urls = build_request_batch_from_queries(queries)

    assert len(urls) == 2
    assert "site=A" in str(urls[0])
    assert "site=B" in str(urls[1])

def test_build_request_with_multidict():
    """Verify build_request handles MultiDict with duplicate keys."""
    query = MultiDict([("site", "1"), ("site", "2")])
    url = build_request(query=query)
    assert str(url).count("site=") == 2

def test_build_request_batch_custom_builder():
    """Verify batch methods respect a custom request_builder."""
    fixed_url = URL("https://custom.com")
    def fixed_builder(feature_id=None, query=None):
        return fixed_url

    urls = build_request_batch_from_feature_ids(["ID1"], request_builder=fixed_builder)
    assert urls[0] == fixed_url

def test_build_request_with_tuple_sequence():
    """Verify build_request handles a sequence of tuples for query params."""
    query = [("parameter_code", "00060"), ("f", "json")]
    url = build_request(query=query)
    assert "parameter_code=00060" in str(url)
    assert "f=json" in str(url)

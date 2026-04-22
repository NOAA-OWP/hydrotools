"""Test the build_constants stand-alone script."""
import pytest
from typing import Any
from schema_extract import get_template_data

@pytest.fixture
def mock_schema() -> dict[str, Any]:
    """Mock test schema."""
    return {
        "paths": {
            "/collections/monitoring-locations/items": {"get": {}},
            "/collections/daily/items": {"get": {}},
            "/conformance": {"get": {}} 
        }
    }

@pytest.fixture
def bad_schema_special() -> dict[str, Any]:
    """Bad test schema with special characters."""
    return {
        "paths": {
            "/collections/@@$$%%/items": {"get": {}},
            "/collections/daily/items": {"get": {}},
            "/conformance": {"get": {}} 
        }
    }

@pytest.fixture
def bad_schema_digits() -> dict[str, Any]:
    """Bad test schema with initial digit."""
    return {
        "paths": {
            "/collections/123/items": {"get": {}},
            "/collections/daily/items": {"get": {}},
            "/conformance": {"get": {}} 
        }
    }

@pytest.fixture
def weird_schema() -> dict[str, Any]:
    """Mock test schema."""
    return {
        "paths": {
            "/collections/monitoring-locations/items/": {"get": {}},
            "/collections/daily-v2.beta/items": {"get": {}},
            "/collections/daily-v3.beta/items/": {"get": {}},
            "/collections/123-items/items": {"get": {}},
            "/collections/items/items": {"get": {}},
            "/conformance": {"get": {}} 
        }
    }

def test_get_template_data(mock_schema):
    """Verify extraction of collections."""
    data = get_template_data(mock_schema)

    assert len(data) == 2
    assert data[0]["value"] == "daily"
    assert data[1]["enum_member"] == "MONITORING_LOCATIONS"

def test_bad_schema_special(bad_schema_special):
    """Verify raises SyntaxError."""
    with pytest.raises(SyntaxError):
        data = get_template_data(bad_schema_special)

def test_bad_schema_digits(bad_schema_digits):
    """Verify raises SyntaxError."""
    with pytest.raises(SyntaxError):
        data = get_template_data(bad_schema_digits)

def test_ignore_bad_schema(bad_schema_special):
    """Verify extraction of collections."""
    data = get_template_data(bad_schema_special, ignore_errors=True)

    assert len(data) == 1
    assert data[0]["value"] == "daily"
    assert data[0]["enum_member"] == "DAILY"

def test_weird_collections(weird_schema):
    """Verify extraction of weird collections."""
    data = get_template_data(weird_schema, ignore_errors=True)

    assert len(data) == 4
    assert data[0]["value"] == "daily-v2.beta"
    assert data[3]["enum_member"] == "MONITORING_LOCATIONS"

def test_fix_errors_default(weird_schema):
    """Verify extraction of weird collections."""
    data = get_template_data(weird_schema, fix_errors=True)

    assert len(data) == 5
    assert data[0]["value"] == "123-items"
    assert data[0]["enum_member"] == "COLLECTION_123_ITEMS"

def test_fix_errors_custom(weird_schema):
    """Verify extraction of weird collections."""
    data = get_template_data(weird_schema, fix_errors=True, error_prefix="ENDPOINT_")

    assert len(data) == 5
    assert data[0]["value"] == "123-items"
    assert data[0]["enum_member"] == "ENDPOINT_123_ITEMS"

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
def mock_parameter_schema() -> dict[str, Any]:
    """Mock test schema."""
    return {
        "paths": {
            "/collections/monitoring-locations/items": {"get": {
                "description": "MONITORING LOCATIONS",
                "parameters": [{
                    "description": "PARAMETER ONE",
                    "in": "query",
                    "name": "parameter_one",
                    "required": False,
                    "schema": {
                        "default": 10_000,
                        "type": "integer"
                    }
                },
                {
                    "description": "PARAMETER TWO",
                    "in": "query",
                    "name": "parameter_two",
                    "required": True,
                    "schema": {
                        "default": "left",
                        "type": "string",
                        "enum": ["left", "right"]
                    }
                },
                {
                    "description": "PARAMETER THREE",
                    "in": "query",
                    "name": "parameter_three",
                    "required": False,
                    "schema": {
                        "default": 4.3,
                        "type": "number"
                    }
                },
                {
                    "description": "PARAMETER X",
                    "in": "query",
                    "name": "parameter_x",
                    "required": True,
                    "schema": {
                        "default": True,
                        "type": "boolean"
                    }
                },
                {
                    "description": "PARAMETER ZEE",
                    "in": "query",
                    "name": "parameter_zee",
                    "required": False,
                    "schema": {
                        "items": {"type": "number"},
                        "type": "array"
                    }
                },
                {
                    "description": "IGNORE ME",
                    "in": "not_query",
                    "name": "ignore_me",
                    "required": True,
                    "schema": {
                        "items": {"type": "number"},
                        "type": "array"
                    }
                },
                {
                    "description": "OBJECT",
                    "in": "query",
                    "name": "zobject_parameter",
                    "required": True,
                    "schema": {
                        "default": {"key": "key", "value": 1.0},
                        "type": "object"
                    }
                },
                {
                    "description": "FILTER",
                    "in": "query",
                    "name": "filter",
                    "required": False,
                    "schema": {
                        "type": "string"
                    }
                }]
            }},
        }
    }

@pytest.fixture
def mock_schema_bad_parameter() -> dict[str, Any]:
    """Mock test schema."""
    return {
        "paths": {
            "/collections/monitoring-locations/items": {"get": {
                "description": "MONITORING LOCATIONS",
                "parameters": [{
                    "description": "PARAMETER ONE",
                    "in": "query",
                    "required": False,
                    "schema": {
                        "default": 10_000,
                        "type": "integer"
                    }
                }]
            }},
        }
    }

@pytest.fixture
def mock_schema_bad_parameter_name() -> dict[str, Any]:
    """Mock test schema."""
    return {
        "paths": {
            "/collections/monitoring-locations/items": {"get": {
                "description": "MONITORING LOCATIONS",
                "parameters": [{
                    "description": "PARAMETER ONE",
                    "name": "$$%%",
                    "in": "query",
                    "required": False,
                    "schema": {
                        "default": 10_000,
                        "type": "integer"
                    }
                }]
            }},
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

def test_get_template_parameters(mock_parameter_schema):
    """Verify extraction of collection parameters."""
    data = get_template_data(mock_parameter_schema)

    assert len(data) == 1
    assert data[0]["enum_member"] == "MONITORING_LOCATIONS"
    assert data[0]["class_name"] == "MonitoringLocationsClient"
    assert data[0]["description"] == "MONITORING LOCATIONS"
    assert data[0]["value"] == "monitoring-locations"
    assert len(data[0]["parameters"]) == 7

    # Check parameter one
    assert data[0]["parameters"][0]["name"] == "parameter_one"
    assert data[0]["parameters"][0]["python_name"] == "parameter_one"
    assert data[0]["parameters"][0]["type_hint"] == "Optional[int]"
    assert data[0]["parameters"][0]["default"] == 10_000
    assert data[0]["parameters"][0]["description"] == "PARAMETER ONE"

    # Check parameter three
    assert data[0]["parameters"][1]["name"] == "parameter_three"
    assert data[0]["parameters"][1]["python_name"] == "parameter_three"
    assert data[0]["parameters"][1]["type_hint"] == 'Optional[float]'
    assert data[0]["parameters"][1]["default"] == 4.3
    assert data[0]["parameters"][1]["description"] == "PARAMETER THREE"

    # Check parameter two
    assert data[0]["parameters"][2]["name"] == "parameter_two"
    assert data[0]["parameters"][2]["python_name"] == "parameter_two"
    assert data[0]["parameters"][2]["type_hint"] == 'Literal["left", "right"]'
    assert data[0]["parameters"][2]["default"] == '"left"'
    assert data[0]["parameters"][2]["description"] == "PARAMETER TWO"

    # Check parameter x
    assert data[0]["parameters"][3]["type_hint"] == 'bool'
    assert data[0]["parameters"][3]["default"]

    # Check parameter zee
    assert data[0]["parameters"][4]["type_hint"] == 'Optional[Sequence[float]]'
    assert data[0]["parameters"][4]["default"] is None

    # Check parameter filter
    assert data[0]["parameters"][5]["type_hint"] == 'Optional[str]'
    assert data[0]["parameters"][5]["default"] is None
    assert data[0]["parameters"][5]["python_name"] == "query_filter"

    # Check object parameter
    assert data[0]["parameters"][6]["type_hint"] == 'dict'
    assert data[0]["parameters"][6]["default"] == {"key": "key", "value": 1.0}

def test_bad_parameters(mock_schema_bad_parameter):
    """Verify extraction of collection parameters."""
    with pytest.raises(KeyError):
        data = get_template_data(mock_schema_bad_parameter)

def test_bad_parameter_name(mock_schema_bad_parameter_name):
    """Verify extraction of collection parameters."""
    with pytest.raises(SyntaxError):
        data = get_template_data(mock_schema_bad_parameter_name)

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
    assert data[2]["value"] == "123-items"
    assert data[2]["enum_member"] == "ENDPOINT_123_ITEMS"

"""Tests for the schema module.

This module verifies that the OGC schema is correctly retrieved, cached, 
and resolved using jsonref and yaml utilities.
"""
from pathlib import Path
from unittest.mock import patch
import json

import pytest
import yaml
from yarl import URL

from hydrotools.waterdata_client.schema import (
    retrieve_yaml,
    get_schema_bytes,
    get_schema
)
from hydrotools.waterdata_client.client_config import _Settings

@pytest.fixture
def mock_schema_content():
    """Minimal schema for testing."""
    return {"openapi": "3.0.0", "info": {"title": "Test API"}, "paths": {
        "/test": {
            "get": {
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        }
                    }
                }
            }
        }
    }, "components": {"schemas": {"Item": {"type": "object"}}}}

@pytest.fixture
def temp_settings(tmp_path: Path):
    """Provides a fresh, isolated Settings instance with a temp cache directory."""
    return _Settings(
        cache_dir=tmp_path,
        cache_expires=600,
        usgs_base_url=URL("https://test.api.gov")
    )

def test_retrieve_yaml_success(mock_schema_content: dict) -> None:
    """Verifies that retrieve_yaml correctly parses bytes into a dictionary."""
    yaml_bytes = yaml.dump(mock_schema_content).encode("utf-8")

    with patch("hydrotools.waterdata_client.schema.get_all") as mock_get:
        # get_all returns a list of results; we return one bytes object
        mock_get.return_value = [yaml_bytes]

        result = retrieve_yaml("https://example.com/api.yaml")

        assert result == mock_schema_content
        mock_get.assert_called_once()

def test_retrieve_yaml_failure() -> None:
    """Verifies that retrieve_yaml raises RuntimeError if bytes are not received."""
    with patch("hydrotools.waterdata_client.schema.get_all") as mock_get:
        mock_get.return_value = [None]

        with pytest.raises(RuntimeError, match="Did not receive bytes"):
            retrieve_yaml("https://example.com/api.yaml")

def test_get_schema_bytes_cache_hit(temp_settings, mock_schema_content):
    """Test a 'Hit': Data is found in the cache and returned immediately."""
    schema_bytes = yaml.dump(mock_schema_content).encode("utf-8")

    # Manually 'prime' the cache so it's a hit
    temp_settings.default_cache.set(str(temp_settings.schema_url), schema_bytes)

    # Patch 'SETTINGS' inside the schema module to use our temp_settings
    with patch("hydrotools.waterdata_client.schema.SETTINGS", temp_settings):
        result = get_schema_bytes()

        assert result == schema_bytes
        # Ensure no network call was made
        with patch("hydrotools.waterdata_client.schema.get_all") as mock_get:
            get_schema_bytes()
            mock_get.assert_not_called()

def test_get_schema_bytes_cache_miss(temp_settings, mock_schema_content):
    """Test a 'Miss': Cache is empty, so we must fetch from the network."""
    schema_bytes = yaml.dump(mock_schema_content).encode("utf-8")

    with patch("hydrotools.waterdata_client.schema.SETTINGS", temp_settings), \
         patch("hydrotools.waterdata_client.schema.get_all") as mock_get:

        mock_get.return_value = [schema_bytes]

        result = get_schema_bytes()

        assert result == schema_bytes
        mock_get.assert_called_once()

        # Verify it was saved to the temp disk cache for next time
        assert temp_settings.default_cache.get(str(temp_settings.schema_url)) == schema_bytes

def test_get_schema_bytes_fetch_failure(temp_settings):
    """Test a 'Failure': Cache miss followed by a network error."""
    with patch("hydrotools.waterdata_client.schema.SETTINGS", temp_settings), \
         patch("hydrotools.waterdata_client.schema.get_all") as mock_get:

        # Simulate network returning None (Failure)
        mock_get.return_value = [None]

        with pytest.raises(RuntimeError, match="Could not retrieve OGC schema"):
            get_schema_bytes()

def test_get_schema_resolution(mock_schema_content: dict) -> None:
    """Verifies that get_schema resolves internal $ref pointers."""
    # Add a reference to the mock schema
    schema_bytes = json.dumps(mock_schema_content).encode("utf-8")

    with patch("hydrotools.waterdata_client.schema.get_schema_bytes") as mock_bytes_func:
        mock_bytes_func.return_value = schema_bytes

        resolved_schema = get_schema()

        # Accessing the ref should yield the actual object content
        response_schema = resolved_schema["paths"]["/test"]["get"]["responses"]
        item_schema = response_schema["200"]["content"]["application/json"]["schema"]
        assert item_schema["type"] == "object"
        assert "Item" not in str(type(item_schema))  # It's a resolved proxy

def test_get_schema_invalid_dict() -> None:
    """Verifies that get_schema raises RuntimeError if result is not a dict."""
    with patch("hydrotools.waterdata_client.schema.get_schema_bytes") as mock_bytes_func, \
         patch("jsonref.loads") as mock_jsonref:

        mock_bytes_func.return_value = b"some data"
        mock_jsonref.return_value = ["not", "a", "dict"]

        with pytest.raises(RuntimeError, match="not a valid dictionary"):
            get_schema()

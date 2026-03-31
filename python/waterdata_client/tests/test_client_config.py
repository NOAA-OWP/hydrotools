"""Tests for the client_config module.

This module verifies that package-wide settings are correctly initialized from 
defaults and environment variable overrides.

Example:
    $ pytest tests/test_client_config.py
"""

import os
from pathlib import Path
from io import StringIO
from dataclasses import FrozenInstanceError
import pytest
from yarl import URL
from diskcache import Cache
from hydrotools.waterdata_client.client_config import (
    EnvironmentKey,
    _Settings,
    SETTINGS
)

def test_environment_key_describe_keys() -> None:
    """Verifies that describe_keys returns a newline-separated string of keys."""
    description = EnvironmentKey.describe_keys()
    assert isinstance(description, str)
    assert EnvironmentKey.BASE_URL in description
    assert EnvironmentKey.API_KEY in description
    assert len(description.split(os.linesep)) == len(EnvironmentKey)

def test_environment_key_print_keys() -> None:
    """Verifies that print_keys writes the expected keys to a stream."""
    stream = StringIO()
    EnvironmentKey.print_keys(stream=stream)
    output = stream.getvalue()
    assert EnvironmentKey.describe_keys() in output

def test_settings_defaults() -> None:
    """Verifies the default values of a fresh _Settings instance."""
    # Instantiating a fresh _Settings to check hardcoded defaults
    settings = _Settings()
    assert settings.usgs_base_url == URL("https://api.waterdata.usgs.gov/ogcapi/v0")
    assert settings.schema_path == "openapi"
    assert settings.default_concurrency == 10
    assert settings.default_retries == 3
    assert settings.timeout_seconds == 900
    assert settings.usgs_api_key is None

def test_settings_from_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifies that from_env correctly picks up environment variable overrides.

    Args:
        monkeypatch: Pytest fixture for mocking environment variables.
    """
    # Define values for overrides
    new_url = "https://test.api.gov/v1"
    new_concurrency = "50"
    new_api_key = "test-key-123"

    # Apply overrides using the generated EnvironmentKey strings
    monkeypatch.setenv(EnvironmentKey.BASE_URL, new_url)
    monkeypatch.setenv(EnvironmentKey.CONCURRENCY, new_concurrency)
    monkeypatch.setenv(EnvironmentKey.API_KEY, new_api_key)

    # from_env should generate a new instance with these values
    settings = _Settings.from_env()

    assert settings.usgs_base_url == URL(new_url)
    assert settings.default_concurrency == int(new_concurrency)
    assert settings.usgs_api_key == new_api_key

    # Verify that non-overridden values remain at their defaults
    assert settings.default_retries == 3

def test_settings_schema_url() -> None:
    """Verifies the schema_url cached property construction."""
    settings = _Settings(
        usgs_base_url=URL("https://api.example.com"),
        schema_path="test_schema"
    )

    # expected query 'f=json' comes from default_query field
    expected_url = URL("https://api.example.com/test_schema?f=json")
    assert settings.schema_url == expected_url

def test_settings_default_cache(tmp_path: Path) -> None:
    """Verifies that default_cache returns a valid diskcache.Cache instance.

    Args:
        tmp_path: Pytest fixture for a temporary directory.
    """
    settings = _Settings(cache_dir=tmp_path)
    cache = settings.default_cache

    assert isinstance(cache, Cache)
    # diskcache.Cache uses the directory provided
    assert Path(cache.directory) == tmp_path

def test_settings_singleton_initialization() -> None:
    """Verifies the global SETTINGS singleton is initialized."""
    # Ensure the exported singleton is an instance of the settings class
    assert isinstance(SETTINGS, _Settings)

def test_settings_is_frozen() -> None:
    """Verifies that SETTINGS is immutable and raises FrozenInstanceError on mutation.
    
    This ensures that package-wide defaults cannot be accidentally changed 
    at runtime by other modules.
    """
    with pytest.raises(FrozenInstanceError):
        # Attempting to modify a frozen dataclass field
        SETTINGS.default_concurrency = 999

def test_settings_cannot_delete_attr() -> None:
    """Verifies that attributes cannot be deleted from the SETTINGS singleton."""
    with pytest.raises(FrozenInstanceError):
        # Attempting to delete a field also triggers FrozenInstanceError
        del SETTINGS.timeout_seconds

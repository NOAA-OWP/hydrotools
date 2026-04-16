"""Tests for auto-generated constants module.
"""
from hydrotools.waterdata_client.constants import OGCAPI, OGCPATH, USGSCollection

def test_for_collections_api():
    """Verify presence of a collections API."""
    assert "collections" in list(OGCAPI)

def test_for_items_path():
    """Verify presence of a items path."""
    assert "items" in list(OGCPATH)

def test_for_continuous_collection():
    """Verify presence of a continuous collection."""
    assert "continuous" in list(USGSCollection)

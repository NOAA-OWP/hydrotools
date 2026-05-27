"""Tests conversion to StringSequence field types."""
import pytest
from typing import Optional
from pydantic import BaseModel, ValidationError
from pandas import Series
from hydrotools.waterdata_client.request_partitioning import StringIterable

class MockModel(BaseModel):
    """Minimal testing model for validation."""
    locations: Optional[StringIterable] = None

@pytest.mark.parametrize("test_case, expected", [
    (None, None),
    ("USGS-01", ("USGS-01",)),
    ([f"item-{i}" for i in range(5)], ("item-0,item-1,item-2", "item-3,item-4")),
    (Series([f"item-{i}" for i in range(5)]), ("item-0,item-1,item-2", "item-3,item-4")),
    (Series([f"item-{i}" for i in range(5)]).astype("category"), ("item-0,item-1,item-2", "item-3,item-4"))
])
def test_iterable_conversion(test_case, expected):
    """Tests basic validation."""
    model = MockModel(locations=test_case)
    assert model.locations == expected

@pytest.mark.parametrize("test_case", [
    ([None, None],)
])
def test_iterable_validation_error(test_case):
    """Tests basic validation."""
    with pytest.raises(ValidationError, match="Unable to convert"):
        MockModel(locations=test_case)

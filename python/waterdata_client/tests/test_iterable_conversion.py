"""Tests conversion to StringSequence field types."""
import pytest
from typing import Optional
from pydantic import BaseModel, ValidationError
from pandas import Series
from hydrotools.waterdata_client.request_models.continuous import ContinuousRequest

@pytest.mark.parametrize("test_case, expected_no_queries", [
    (None, 1),
    ("USGS-01", 1),
    ([f"item-{i}" for i in range(5)], 5),
    (Series([f"item-{i}" for i in range(4)]), 4),
    (Series([f"item-{i}" for i in range(3)]).astype("category"), 3)
])
def test_iterable_conversion(test_case, expected_no_queries):
    """Tests basic iterable handling."""
    model = ContinuousRequest(
        monitoring_location_id=test_case
    )
    assert len(model.generate_queries()) == expected_no_queries

@pytest.mark.parametrize("test_case", [
    ([None, None],)
])
def test_iterable_validation_error(test_case):
    """Tests basic validation."""
    with pytest.raises(ValidationError, match="Unable to convert"):
        ContinuousRequest(
            monitoring_location_id=test_case
        )

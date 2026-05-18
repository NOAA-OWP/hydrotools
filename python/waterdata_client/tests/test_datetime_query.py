import pytest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from unittest.mock import patch
import pandas as pd
from hydrotools.waterdata_client.request_models.continuous import ContinuousRequest
from pydantic_core import ValidationError

MOCK_CURRENT_TIME: pd.Timestamp = pd.Timestamp("2025-05-05")
"""Replaces pandas.Timestamp.now in tests."""

@pytest.mark.parametrize("datetime_object, datetime_string", [
    ("ABCD", "ABCD"),
    (pd.Timestamp("2010-01-01"), "2010-01-01T00:00:00+00:00"),
    (pd.Timestamp("2010-01-01", tzinfo=ZoneInfo("America/Chicago")), "2010-01-01T06:00:00+00:00"),
    (datetime(2025, 2, 3, 4, 5, 6), "2025-02-03T04:05:06+00:00"),
    (datetime(2025, 2, 3, 4, 5, 11, tzinfo=ZoneInfo("America/Chicago")), "2025-02-03T10:05:11+00:00"),
    (timedelta(hours=36), "2025-05-03T12:00:00+00:00/2025-05-05T00:00:00+00:00"),
    (pd.Timedelta(hours=25), "2025-05-03T23:00:00+00:00/2025-05-05T00:00:00+00:00"),
    ([pd.Timestamp("2020-01-01"), datetime(2020, 1, 2)], "2020-01-01T00:00:00+00:00/2020-01-02T00:00:00+00:00"),
    ([pd.Timestamp("2020-01-01"), None], "2020-01-01T00:00:00+00:00/.."),
    ([None, datetime(2020, 1, 2)], "../2020-01-02T00:00:00+00:00"),
    ([pd.Timestamp("2020-01-01", tzinfo=ZoneInfo("America/Chicago")), datetime(2020, 1, 1, 7)], "2020-01-01T06:00:00+00:00/2020-01-01T07:00:00+00:00")
])
def test_datetime_validation(datetime_object, datetime_string) -> None:
    """Verfies handling of datetime-like objects and conversion to USGS API
    compatible strings. Verifies that string inputs are not transformed.
    """
    with patch("hydrotools.waterdata_client.datetime_utilities.pd.Timestamp.now") as mock_now:
        mock_now.return_value = MOCK_CURRENT_TIME
        model = ContinuousRequest(datetime=datetime_object)
        assert model.datetime == datetime_string

@pytest.mark.parametrize("datetime_object, match_string", [
    ([None, None], "objects are None"),
    ([pd.Timestamp("2025-01-01"), pd.Timestamp("2025-01-02"), pd.Timestamp("2025-01-03")], "exactly length two"),
    (999, "Cannot convert"),
    ([pd.Timestamp("2026-06-06"), 789], "All items in"),
    ([datetime(2020, 1, 2), datetime(2020, 1, 1)], "Improper interval")
])
def test_raises_validation_error(datetime_object, match_string) -> None:
    """Verifies raises on incompatible datetime objects."""
    with pytest.raises(ValidationError, match=match_string):
        model = ContinuousRequest(datetime=datetime_object)

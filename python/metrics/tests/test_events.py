import pytest
import numpy as np
import hydrotools.metrics.events as emet

one_series = np.ones(10)
range_series = np.arange(9)
negative_series = -one_series
empty_series = np.empty(0)

def test_flashiness():
    assert emet.flashiness(one_series) == 0.0
    assert emet.flashiness(range_series) == 0.25

    with pytest.raises(AssertionError):
        emet.flashiness(empty_series)

def test_peak():
    assert emet.peak(one_series) == 1.0
    assert emet.peak(range_series) == 8.0

    with pytest.raises(AssertionError):
        emet.peak(empty_series)

def test_runoff_ratio():
    assert emet.runoff_ratio(one_series, one_series*2.0) == 0.5
    assert emet.runoff_ratio(range_series, range_series*2.0) == 0.5

    with pytest.warns(RuntimeWarning):
        assert emet.runoff_ratio(range_series, range_series*0.5) == 2.0

    with pytest.raises(AssertionError):
        emet.runoff_ratio(negative_series, range_series*0.5)

    with pytest.raises(AssertionError):
        emet.runoff_ratio(range_series, negative_series*0.5)

    with pytest.raises(AssertionError):
        emet.runoff_ratio(empty_series, range_series*0.5)

    with pytest.raises(AssertionError):
        emet.runoff_ratio(range_series, empty_series)

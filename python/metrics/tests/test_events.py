"""This module tests methods found in the hydrotools.metrics.events module."""
import pytest
import numpy as np
import numpy.typing as npt
import hydrotools.metrics.events as emet

ONE_SERIES: npt.NDArray[np.float64] = np.ones(10)
"""An array of 10 ones for trivial tests cases."""
RANGE_SERIES: npt.NDArray[np.float64] = np.arange(9)
"""An array of 10 monotonically increasing values for trivial tests cases."""
NEGATIVE_SERIES: npt.NDArray[np.float64] = -ONE_SERIES
"""An array of 10 negative ones for trivial tests cases."""
EMPTY_SERIES: npt.NDArray[np.float64] = np.empty(0)
"""An empty array for trivial tests cases."""

def test_flashiness() -> None:
    """Tests flashiness method. This test verifies that an uniform array
    returns 0.0 flashiness. It verifies that a known array returns a known
    flashiness. Lastly, it verifies an assertion error is raised for an empty
    array."""
    assert emet.flashiness(ONE_SERIES) == 0.0
    assert emet.flashiness(RANGE_SERIES) == 0.25

    with pytest.raises(AssertionError):
        emet.flashiness(EMPTY_SERIES)

def test_peak() -> None:
    """Tests peak method. This test verifies that an uniform array
    returns the correct single value. It verifies that a known array returns a
    known maximum. Lastly, it verifies an assertion error is raised for an
    empty array."""
    assert emet.peak(ONE_SERIES) == 1.0
    assert emet.peak(RANGE_SERIES) == 8.0

    with pytest.raises(AssertionError):
        emet.peak(EMPTY_SERIES)

def test_runoff_ratio() -> None:
    """Tests runoff ratio method. This test verifies that uniform arrays
    return a known value. It verifies that known arrays returns a known
    runoff ratio. Lastly, it verifies an assertion error is raised for an empty
    array or an array containing negative values."""
    assert emet.runoff_ratio(ONE_SERIES, ONE_SERIES*2.0) == 0.5
    assert emet.runoff_ratio(RANGE_SERIES, RANGE_SERIES*2.0) == 0.5

    with pytest.warns(RuntimeWarning):
        assert emet.runoff_ratio(RANGE_SERIES, RANGE_SERIES*0.5) == 2.0

    with pytest.raises(AssertionError):
        emet.runoff_ratio(NEGATIVE_SERIES, RANGE_SERIES*0.5)

    with pytest.raises(AssertionError):
        emet.runoff_ratio(RANGE_SERIES, NEGATIVE_SERIES*0.5)

    with pytest.raises(AssertionError):
        emet.runoff_ratio(EMPTY_SERIES, RANGE_SERIES*0.5)

    with pytest.raises(AssertionError):
        emet.runoff_ratio(RANGE_SERIES, EMPTY_SERIES)

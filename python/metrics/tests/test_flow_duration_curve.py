"""This module tests flow duration curve functionality."""
import pytest
import numpy as np
import numpy.typing as npt
import hydrotools.metrics.flow_duration_curve as fdc

BASIC_ARRAY: npt.NDArray[np.float64] = np.arange(50.0) + 1.0
"""Trivial monotonically increasing array for basic test cases (len=50)."""
PROBABILITIES: npt.NDArray[np.float64] = np.linspace(0.0, 1.0, 101)
"""Fabricated set of probabilities for test cases (len=101)."""
VALUES: npt.NDArray[np.float64] = np.concatenate((
    np.ones(51), np.ones(50) * 0.5))
"""Fabricated set of values for test cases (len=101). First half of array is
all ones. Latter half is all equal to 0.5."""

def test_empirical_flow_duration_curve():
    """Test empirical flow duration curve functionality. Flow duration curve
    methods should return a tuple where the first value is an array
    probabilities and the second value is corresponding streamflow values.
    Probabiliites should be between 0 and 1, and arranged from smallest to
    largest. The maximum value should match the lowest probability and the
    minimum value should match the largest probability. The returned lengths
    should match the length of the input. Use of alternative plotting positions
    should have the same results."""
    p, v = fdc.empirical_flow_duration_curve(BASIC_ARRAY)
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert np.all(np.min(BASIC_ARRAY) <= v)
    assert np.all(v <= np.max(BASIC_ARRAY))
    assert v[0] >= v[1]
    assert len(p) == len(BASIC_ARRAY)
    assert len(v) == len(BASIC_ARRAY)

    p, v = fdc.empirical_flow_duration_curve(BASIC_ARRAY, alpha=0.5, beta=0.5)
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert np.all(np.min(BASIC_ARRAY) <= v)
    assert np.all(v <= np.max(BASIC_ARRAY))
    assert v[0] >= v[1]
    assert len(p) == len(BASIC_ARRAY)
    assert len(v) == len(BASIC_ARRAY)

def test_pearson_flow_duration_curve():
    """Test pearson flow duration curve functionality. Flow duration curve
    methods should return a tuple where the first value is an array
    probabilities and the second value is corresponding streamflow values.
    Probabiliites should be between 0 and 1, and arranged from smallest to
    largest. The maximum value should match the lowest probability and the
    minimum value should match the largest probability. The returned lengths
    should match the length of the input. Curve interpolation via 
    number_of_points should result in the same."""
    p, v = fdc.pearson_flow_duration_curve(BASIC_ARRAY)
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert np.all(np.min(BASIC_ARRAY) <= v)
    assert np.all(v <= np.max(BASIC_ARRAY))
    assert v[0] >= v[1]
    assert len(p) == len(BASIC_ARRAY)
    assert len(v) == len(BASIC_ARRAY)

    p, v = fdc.pearson_flow_duration_curve(BASIC_ARRAY, number_of_points=100)
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert np.all(np.min(BASIC_ARRAY) <= v)
    assert np.all(v <= np.max(BASIC_ARRAY))
    assert v[0] >= v[1]
    assert len(p) == 100
    assert len(v) == 100

def test_empirical_bootstrap():
    """Test bootstrapping of empirical FDCs. Every quantile should adhere to
    the same criteria used to test basic flow duration curves. The number of
    returned quantile traces should match the number of input quantiles."""
    p, qs = fdc.bootstrap_flow_duration_curve(
        BASIC_ARRAY,
        quantiles=[0.025, 0.5, 0.975],
        repetitions=10
        )
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert len(p) == len(BASIC_ARRAY)
    assert len(qs) == 3
    for q in qs:
        assert np.all(np.min(BASIC_ARRAY) <= q)
        assert np.all(q <= np.max(BASIC_ARRAY))
        assert q[0] >= q[1]
        assert len(q) == len(BASIC_ARRAY)

def test_pearson_bootstrap():
    """Test bootstrapping of pearson FDCs. Every quantile should adhere to
    the same criteria used to test basic flow duration curves. The number of
    returned quantile traces should match the number of input quantiles.
    Make sure FDC generator kwargs are passed through correctly."""
    p, qs = fdc.bootstrap_flow_duration_curve(
        BASIC_ARRAY,
        quantiles=[0.025, 0.5, 0.975],
        repetitions=10,
        fdc_generator=fdc.pearson_flow_duration_curve,
        number_of_points=100
        )
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert len(p) == 100
    assert len(qs) == 3
    for q in qs:
        assert np.all(np.min(BASIC_ARRAY) <= q)
        assert np.all(q <= np.max(BASIC_ARRAY))
        assert q[0] >= q[1]
        assert len(q) == 100

def test_exceedance():
    """Test exceedance values are correctly interpolated given trivial
    FDCs."""

    e = fdc.exceedance_values(0.5, [0.0, 1.0], [10.0, 0.0])
    assert e == 5.0

    es = fdc.exceedance_values([0.2, 0.8], [0.0, 1.0], [10.0, 0.0])
    assert es[0] == 8.0
    assert es[1] == 2.0

def test_recurrence():
    """Test recurrence intervals are correctly interpolated given trivial
    FDCs."""

    r = fdc.recurrence_values(2.0, [0.0, 1.0], [10.0, 0.0])
    assert r == 5.0

    rs = fdc.recurrence_values([5.0, 1.25], [0.0, 1.0], [10.0, 0.0])
    assert rs[0] == 8.0
    assert rs[1] == 2.0

def test_flow_variability():
    """Test that standardized indices of flow variability are correctly
    computed."""

    rfr = fdc.richards_flow_responsiveness(PROBABILITIES, VALUES)
    assert rfr["10R90"] == 2.0
    assert rfr["20R80"] == 2.0
    assert rfr["25R75"] == 2.0
    assert rfr[".5S"] == 0.5
    assert rfr[".6S"] == 0.5
    assert rfr[".8S"] == 0.5
    assert np.isclose(rfr["CVLF5"], -1.0, atol=0.1)

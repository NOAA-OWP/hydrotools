"""This module tests flow duration curve functionality."""
import pytest
import numpy as np
import numpy.typing as npt
import hydrotools.metrics.flow_duration_curve as fdc

def test_all():
    # Tests
    s = np.arange(50.0) + 1.0

    p, v = fdc.empirical_flow_duration_curve(s)
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert np.all(1.0 <= v)
    assert np.all(v <= 51.0)
    assert v[0] >= v[1]
    assert len(p) == 50
    assert len(v) == 50

    p, v = fdc.empirical_flow_duration_curve(s, alpha=0.5, beta=0.5)
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert np.all(1.0 <= v)
    assert np.all(v <= 51.0)
    assert v[0] >= v[1]
    assert len(p) == 50
    assert len(v) == 50

    p, v = fdc.pearson_flow_duration_curve(s)
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert np.all(1.0 <= v)
    assert np.all(v <= 51.0)
    assert v[0] >= v[1]
    assert len(p) == 50
    assert len(v) == 50

    p, v = fdc.pearson_flow_duration_curve(s, number_of_points=100)
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert np.all(1.0 <= v)
    assert np.all(v <= 51.0)
    assert v[0] >= v[1]
    assert len(p) == 100
    assert len(v) == 100

    p, qs = fdc.bootstrap_flow_duration_curve(
        s,
        quantiles=[0.025, 0.5, 0.975],
        repetitions=10
        )
    assert np.all(0.0 <= p)
    assert np.all(p <= 1.0)
    assert len(p) == 50
    assert len(qs) == 3
    for q in qs:
        assert np.all(1.0 <= q)
        assert np.all(q <= 51.0)
        assert q[0] >= q[1]
        assert len(q) == 50

    p, qs = fdc.bootstrap_flow_duration_curve(
        s,
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
        assert np.all(1.0 <= q)
        assert np.all(q <= 51.0)
        assert q[0] >= q[1]
        assert len(q) == 100

    e = fdc.exceedance_values(0.5, [0.0, 1.0], [10.0, 0.0])
    assert e == 5.0

    es = fdc.exceedance_values([0.2, 0.8], [0.0, 1.0], [10.0, 0.0])
    assert es[0] == 8.0
    assert es[1] == 2.0

    r = fdc.recurrence_values(2.0, [0.0, 1.0], [10.0, 0.0])
    assert r == 5.0

    rs = fdc.recurrence_values([5.0, 1.25], [0.0, 1.0], [10.0, 0.0])
    assert rs[0] == 8.0
    assert rs[1] == 2.0

    p = np.linspace(0.0, 1.0, 101)
    v = np.concatenate((np.ones(51), np.ones(50) * 0.5))
    rfr = fdc.richards_flow_responsiveness(p, v)
    assert rfr["10R90"] == 2.0
    assert rfr["20R80"] == 2.0
    assert rfr["25R75"] == 2.0
    assert rfr[".5S"] == 0.5
    assert rfr[".6S"] == 0.5
    assert rfr[".8S"] == 0.5
    assert np.isclose(rfr["CVLF5"], -1.0, atol=0.1)

import pytest
from hydrotools.events.baseflow import eckhardt as bf

import numpy as np
import pandas as pd

def test_linear_recession_analysis():
    # Test exponential decay (perfect linear reservoir)
    test_value = -0.8
    s = np.exp(test_value * np.linspace(0.0, 50.0, 51))
    a = bf.linear_recession_analysis(s)
    assert np.isclose(np.log(a), test_value, atol=1e-6)

    # Test with a different window size
    a = bf.linear_recession_analysis(s, window=6)
    assert np.isclose(np.log(a), test_value, atol=1e-6)

    # Test with random noise
    rng = np.random.default_rng(seed=2025)
    noise = np.abs(rng.normal(0.0, 0.01, 51))
    a = bf.linear_recession_analysis(s+noise)
    assert a > 0.0
    assert a < 1.0

    # Test with outliers
    a_without_outliers = bf.linear_recession_analysis(s)
    s[30:36] = np.exp(-0.79 * np.linspace(0.0, 5.0, 6))
    a_with_outliers = bf.linear_recession_analysis(s)
    relative_difference = (a_with_outliers - a_without_outliers) / a_with_outliers
    assert relative_difference <= 0.02

def test_maximum_baseflow_analysis():
    rng = np.random.default_rng(seed=2025)
    s = rng.normal(100.0, 10.0, 100)

    bfi_max = bf.maximum_baseflow_analysis(s, 0.9)

    assert bfi_max >= 0.0
    assert bfi_max <= 1.0

def test_apply_filter():
    rng = np.random.default_rng(seed=2025)
    s = rng.normal(100.0, 10.0, 100)

    b = bf.apply_filter(s, 0.9, 0.5)
    assert b[0] == s[0]
    assert b.sum() < s.sum()

def test_separate_baseflow():
    rng = np.random.default_rng(seed=2025)
    s = pd.Series(
        rng.normal(0.0, 0.01, 30000) + np.exp(-0.8 * np.linspace(0.0, 1.0, 30000)),
        pd.date_range(
            "2020-01-01",
            periods=30000,
            freq="5min"
        )
    )
    b = bf.separate_baseflow(s, "15min")
    s = s.resample("15min").first()

    assert b.recession_constant <= 1.0
    assert b.recession_constant >= 0.0
    assert b.maximum_baseflow_index <= 1.0
    assert b.maximum_baseflow_index >= 0.0
    assert b.values.sum() < s.sum()
    assert b.values.count() == s.count()

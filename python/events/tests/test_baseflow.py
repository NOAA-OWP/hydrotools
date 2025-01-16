import pytest
from hydrotools.events.baseflow import eckhardt as bf

import numpy as np
import pandas as pd

def test_linear_recession_analysis():
    s = np.exp(-0.8 * np.linspace(0.0, 1.0, 100))
    a = bf.linear_recession_analysis(s)

    assert a >= 0.0
    assert a <= 1.0

def test_maximum_baseflow_analysis():
    rng = np.random.default_rng()
    s = rng.normal(100.0, 10.0, 100)

    bfi_max = bf.maximum_baseflow_analysis(s, 0.9)

    assert bfi_max >= 0.0
    assert bfi_max <= 1.0

def test_separate_baseflow():
    rng = np.random.default_rng()
    s = rng.normal(100.0, 10.0, 100)

    b = bf.separate_baseflow(s, 0.9, 0.5)
    assert b[0] == s[0]

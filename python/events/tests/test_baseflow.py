import pytest
from hydrotools.events.baseflow import eckhardt as bf

import numpy as np
import pandas as pd

def test_linear_recession_analysis():
    s = np.exp(-0.9 * np.linspace(0.0, 1.0, 100))
    a = bf.linear_recession_analysis(s)

    assert a == 0.9

def test_maximum_baseflow_analysis():
    s = np.exp(-0.9 * np.linspace(0.0, 1.0, 100))
    bfi_max = bf.maximum_baseflow_analysis(s, 0.9)

    assert bfi_max == 0.5

def test_separate_baseflow():
    rng = np.random.default_rng()
    s = rng.normal(100.0, 10.0, 100)

    # Test numpy
    from time import perf_counter
    start = perf_counter()
    b = bf.separate_baseflow(s, 0.9, 0.5)
    end = perf_counter()
    print(f"{end-start:.6f} s")
    assert b[0] == s[0]

import pytest
import numpy as np
from hydrotools.metrics import _validation
import pandas as pd

def test_raise_for_non_vector():
    x = np.array([[1, 2, 3, 4], [1, 1, 1, 4]])
    y = [1, 2, 3, 4]

    _validation.raise_for_non_vector(y)

    with pytest.raises(_validation.NonVectorError):
        _validation.raise_for_non_vector(x)

def test_raise_for_inconsistent_shapes():
    x = np.array([[1, 2, 3, 4], [1, 1, 1, 4]])
    y = [1, 2, 3, 4]
    z = [5, 6, 7, 8]

    _validation.raise_for_inconsistent_shapes(y, z)

    with pytest.raises(_validation.InconsistentShapesError):
        _validation.raise_for_inconsistent_shapes(x, y)

def test_validate_boolean_categorical_series():
    # Check for non-Series
    with pytest.raises(pd.errors.UnsupportedFunctionCall):
        x = _validation.validate_boolean_categorical_series([1, 2, 3])

    # Check for non-categorical
    with pytest.warns(UserWarning):
        s = pd.Series([True, True, False])
        s = _validation.validate_boolean_categorical_series(s)
        assert hasattr(s, "cat")

    # Check for True
    with pytest.warns(UserWarning):
        s = pd.Series([False, False, False], dtype="category")
        s = _validation.validate_boolean_categorical_series(s)
        assert True in s.cat.categories

    # Check for False
    with pytest.warns(UserWarning):
        s = pd.Series([False, False, False], dtype="category")
        s = _validation.validate_boolean_categorical_series(s)
        assert False in s.cat.categories

    # Check for two categories
    with pytest.raises(pd.errors.UnsupportedFunctionCall):
        s = pd.Series([True, False, "5"], dtype="category")
        s = _validation.validate_boolean_categorical_series(s)

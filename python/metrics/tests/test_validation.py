import pytest
import numpy as np
from hydrotools.metrics import _validation

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

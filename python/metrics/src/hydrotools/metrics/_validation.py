"""
=============================
Method Validation for Metrics
=============================
Various methods and objects for validating metric inputs.

Functions
---------
 - raise_for_non_vector
 - raise_for_inconsistent_shapes

"""

import numpy as np
import numpy.typing as npt
from typing import List

def raise_for_non_vector(
    *arrays: List[npt.ArrayLike]
    ) -> None:
    """
    Validate that all arrays are 1-dimensional.

    Parameters
    ----------
    arrays: arbitrary number of array-like values, required
        Arrays to check.

    Raises
    ------
    ValueError:
        Raises if one of the arrays is not 1-dimensional.
    """
    # Check each array
    for x in arrays:
        if len(np.array(x).shape) != 1:
            message = "all input arrays must be 1-dimensional"
            raise ValueError(message)

def raise_for_inconsistent_shapes(
    *arrays: List[npt.ArrayLike]
    ) -> None:
    """
    Validate that all arrays are the same shape.

    Parameters
    ----------
    arrays: arbitrary number of array-like values, required
        Arrays to check.

    Raises
    ------
    ValueError:
        Raises if all of the arrays are not the same shape.
    """
    # Convert to numpy arrays
    arrays = [np.array(x) for x in arrays]

    # Extract first array
    x = arrays[0]

    # Check shape of each
    for y in arrays:
        # Test each array
        test = all(i == j for i, j in zip(x.shape, y.shape))
        if not test:
            message = "all input arrays must be the same shape"
            raise ValueError(message)

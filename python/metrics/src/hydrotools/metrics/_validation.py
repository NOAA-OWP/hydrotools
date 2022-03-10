"""
=============================
Method Validation for Metrics
=============================
Various methods and objects for validating metric inputs.

Functions
---------
 - raise_for_non_vector
 - raise_for_inconsistent_shapes
 - warn_for_nondichotomous_categories

Classes
-------
 - InconsistentShapesError
 - NonVectorError

"""

import numpy as np
import numpy.typing as npt
from typing import List, Tuple
import pandas as pd
import warnings

class InconsistentShapesError(Exception):
    def __init__(self,
        *args: object,
        array_shape_1: Tuple[int],
        array_shape_2: Tuple[int]
        ) -> None:
        self._array_shape_1 = array_shape_1
        self._array_shape_2 = array_shape_2
        super().__init__(*args)

    def __str__(self) -> str:
        a1s = self._array_shape_1
        a2s = self._array_shape_2
        message = f"Arrays are not the same shape. The array shapes are {a1s} and {a2s}."
        return message

class NonVectorError(Exception):
    def __init__(self,
        *args: object,
        arr: npt.ArrayLike
        ) -> None:
        self._arr = arr
        super().__init__(*args)

    def __str__(self) -> str:
        message = f"This array is not 1-dimensional\n {self._arr}"
        return message

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
    NonVectorError:
        Raises if one of the arrays is not 1-dimensional.
    """
    # Check each array
    for x in arrays:
        if len(np.array(x).shape) != 1:
            raise NonVectorError(arr=x)

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
    InconsistentShapesError:
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
            raise InconsistentShapesError(
                array_shape_1=x.shape,
                array_shape_2=y.shape
                )

def validate_boolean_categorical_series(
    series: pd.Series
    ) -> None:
    """
    Validate that series is a boolean categorical variable.

    Parameters
    ----------
    series: pandas.Series, required
        Series to validate.

    Warnings
    --------
    UserWarning:
        Warns if series is not a boolean Categorical and attempts to convert.

    Raises
    ------
    pandas.errors.UnsupportedFunctionCall:
        Raises if series is not a pandas.Series or if series does not contain two categories: True and False

    Returns
    -------
    Validated boolean categorical series.
    """
    # Check for Series
    if not isinstance(series, pd.Series):
        raise pd.errors.UnsupportedFunctionCall(f"{series} is not a pandas.Series")

    # Check for categorical
    if not hasattr(series, "cat"):
        message = f"{series} is not a categorical pandas.Series, attempting to convert"
        warnings.warn(message=message, category=UserWarning)
        series = series.astype("category")

    # Check for True category
    no_true_category = True
    for c in series.cat.categories:
        if c is True:
            no_true_category = False
    if no_true_category:
        message = f"{series} has no True category, attempting to add"
        warnings.warn(message=message, category=UserWarning)
        series = series.cat.add_categories([True])

    # Check for False category
    no_false_category = True
    for c in series.cat.categories:
        if c is False:
            no_false_category = False
    if no_false_category:
        message = f"{series} has no False category, attempting to add"
        warnings.warn(message=message, category=UserWarning)
        series = series.cat.add_categories([False])

    # Check number of categories
    if len(series.cat.categories) != 2:
        raise pd.errors.UnsupportedFunctionCall(f"{series} does not have exactly two categories: True and False")

    # Return validated series
    return series
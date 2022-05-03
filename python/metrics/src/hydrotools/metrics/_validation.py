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
from typing import List, Tuple, Sequence
import pandas as pd
import warnings
from pandas.api.types import CategoricalDtype

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


def _array_attr(seq: Sequence, attr: str) -> npt.ArrayLike:
    if not hasattr(seq, attr):
        return np.asarray(seq)
    return seq

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
        if _array_attr(x, "ndim").ndim != 1:
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
    # Extract first array
    xshape = _array_attr(arrays[0], "shape").shape

    # Check shape of each
    for y in arrays[1:]:
        yshape = _array_attr(y, "shape").shape
        if xshape != yshape:
            raise InconsistentShapesError(
                array_shape_1=xshape,
                array_shape_2=yshape
                )

def convert_to_boolean_categorical_series(
    data: npt.ArrayLike
    ) -> pd.Series:
    """
    Transform data into a boolean categorical pandas.Series.

    Parameters
    ----------
    data: array-like, required
        Data to convert. Should only contain True or False values.

    Warnings
    --------
    UserWarning:
        Warns if any values in data are not True or False. These values will become NaN.

    Returns
    -------
    Validated boolean categorical series.
    """
    # Create boolean categorical series
    s = pd.Series(
        data=data,
        dtype=CategoricalDtype([True, False])
    )

    # Check for NaN
    if s.isnull().any():
        message = f"{data} contains values that could not be converted to True or False."
        warnings.warn(message=message, category=UserWarning)

    return s
    

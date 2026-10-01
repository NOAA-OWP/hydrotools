import warnings

import numpy as np
import pandas as pd
import pytest

from hydrotools.metrics import _validation


@pytest.mark.parametrize(
    "data, expected_values, expects_warning",
    [
        (
            [True, False, "invalid", None, 1, 0],
            [True, False, np.nan, np.nan, True, False],
            True,
        ),
        (np.array([True, False, "invalid"], dtype=object), [True, False, np.nan], True),
        (
            pd.Series([True, "invalid", False], index=[10, 20, 30], name="flags"),
            [True, np.nan, False],
            True,
        ),
        (
            pd.Series([True, False, "invalid"], dtype="category"),
            [True, False, np.nan],
            True,
        ),
        (pd.Series([True, False, pd.NA], dtype="boolean"), [True, False, np.nan], True),
        ([True, False, 1, 0], [True, False, True, False], False),
        ([1, 2, 3], [np.nan, np.nan, np.nan], True),
        ([1.0, 0.0, 2.0], [np.nan, np.nan, np.nan], True),
        ([], [], False),
    ],
    ids=[
        "list",
        "array",
        "indexed-series",
        "categorical",
        "nullable",
        "valid",
        "integers",
        "floats",
        "empty",
    ],
)
def test_boolean_categorical_conversion_without_deprecation(
    data, expected_values, expects_warning
):
    """Preserve invalid-value handling without pandas deprecation warnings.

    Parameters
    ----------
    data : array-like
        Boolean, equivalent numeric, missing, or invalid input values.
    expected_values : list
        Expected boolean values and missing-value positions.
    expects_warning : bool
        Whether the documented UserWarning should be emitted.

    Returns
    -------
    None
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = _validation.convert_to_boolean_categorical_series(data)

    assert [warning.category for warning in caught] == (
        [UserWarning] if expects_warning else []
    )
    expected = pd.Series(
        expected_values,
        index=data.index if isinstance(data, pd.Series) else None,
        name=data.name if isinstance(data, pd.Series) else None,
        dtype=pd.CategoricalDtype([True, False]),
    )
    pd.testing.assert_series_equal(result, expected)

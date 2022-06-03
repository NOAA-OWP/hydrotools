import pytest
from hydrotools.nwm_client import UnitHandler
import numpy as np
import pandas as pd

@pytest.fixture
def setup_unit_handler():
    return UnitHandler.UnitHandler()

def test_conversion_factor(setup_unit_handler):
    f = setup_unit_handler.conversion_factor(
        from_units="m^3/s",
        to_units="ft^3/s"
    )

    assert np.isclose(f, (0.3048 ** -3.0))

def test_convert_values(setup_unit_handler):
    s = pd.Series([1, 1, 1])
    s = setup_unit_handler.convert_values(
        value=s,
        from_units="ft",
        to_units="m"
    )

    assert (np.all(np.isclose(s, 0.3048)))

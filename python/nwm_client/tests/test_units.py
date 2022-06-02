import pytest
from hydrotools.nwm_client import measurement_units
import numpy as np

def test_conversion_factor():
    f = measurement_units.conversion_factor(
        from_units="m^3/s",
        to_units="ft^3/s"
    )

    assert np.isclose(f, (0.3048 ** -3.0))

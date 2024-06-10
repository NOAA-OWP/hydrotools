import pytest
from hydrotools.nwm_client_new import UnitHandler
import numpy as np
import pandas as pd
from tempfile import TemporaryDirectory
from pint import UnitRegistry

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

def test_alt_unit_registry():
    with TemporaryDirectory() as td:
        uh = UnitHandler.UnitHandler(
            unit_registry=UnitRegistry(cache_folder=td)
            )
        test_conversion_factor(uh)
        test_convert_values(uh)
        from pathlib import Path
        assert next(Path(td).iterdir(), None)

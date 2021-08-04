import pytest
from hydrotools.nwm_client import http as nwm
from os import cpu_count
import numpy as np
import pandas as pd

# Set reference time
yesterday = pd.Timestamp.utcnow() - pd.Timedelta("1D")
reference_time = yesterday.strftime("%Y%m%dT%-HZ")

@pytest.fixture
def setup_nwm():
    return nwm.NWMDataService(
        server="https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"
    )

def test_bucket_name(setup_nwm):
    assert (setup_nwm.server) == "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"

def test_max_processes(setup_nwm):
    count = max(cpu_count() - 2, 1)
    assert (setup_nwm.max_processes) == count

def test_crosswalk(setup_nwm):
    assert setup_nwm.crosswalk['usgs_site_code'].count() > 4000
    assert setup_nwm.crosswalk['usgs_site_code'].count() < 9000

    with pytest.raises(Exception):
        setup_nwm.crosswalk = 0

    with pytest.raises(Exception):
        setup_nwm.crosswalk = pd.DataFrame()

    assert setup_nwm.crosswalk.loc[6186112, "usgs_site_code"] == "01360640"

def test_cache_path(setup_nwm):
    assert str(setup_nwm.cache_path) == 'nwm_client.h5'

    setup_nwm.cache_path = 'custom_cache.h5'
    assert str(setup_nwm.cache_path) == 'custom_cache.h5'

def test_cache_group(setup_nwm):
    assert str(setup_nwm.cache_group) == 'nwm_client'

    setup_nwm.cache_group = 'simulations'
    assert str(setup_nwm.cache_group) == 'simulations'

@pytest.mark.slow
def test_get(setup_nwm):
    # Test ANA
    df = setup_nwm.get(
        configuration="analysis_assim",
        reference_time=reference_time
    )
    assert df['value_time'].unique().size == 3

def test_invalid_configuration_exception(setup_nwm):
    # Test invalid configuration
    with pytest.raises(Exception):
        df = setup_nwm.get(
            configuration="medium_range",
            reference_time="20210101T06Z"
        )

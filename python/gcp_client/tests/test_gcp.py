import pytest
from hydrotools.gcp_client import gcp
from os import cpu_count
import numpy as np
import pandas as pd

@pytest.fixture
def setup_gcp():
    return gcp.NWMDataService()

def test_bucket_name(setup_gcp):
    assert (setup_gcp.bucket_name) == "national-water-model"

def test_max_processes(setup_gcp):
    count = cpu_count() - 2
    assert (setup_gcp.max_processes) == count

def test_crosswalk(setup_gcp):
    assert setup_gcp.crosswalk['usgs_site_code'].count() > 4000
    assert setup_gcp.crosswalk['usgs_site_code'].count() < 9000

    with pytest.raises(Exception):
        setup_gcp.crosswalk = 0

    with pytest.raises(Exception):
        setup_gcp.crosswalk = pd.DataFrame()

    assert setup_gcp.crosswalk.loc[6186112, "usgs_site_code"] == "01360640"

def test_cache_path(setup_gcp):
    assert str(setup_gcp.cache_path) == 'gcp_client.h5'

    setup_gcp.cache_path = 'custom_cache.h5'
    assert str(setup_gcp.cache_path) == 'custom_cache.h5'

def test_cache_group(setup_gcp):
    assert str(setup_gcp.cache_group) == 'gcp_client'

    setup_gcp.cache_group = 'simulations'
    assert str(setup_gcp.cache_group) == 'simulations'

@pytest.mark.slow
def test_list_blobs(setup_gcp):
    blob_list = setup_gcp.list_blobs(
        configuration="short_range",
        reference_time="20210101T01Z"
    )

    assert len(blob_list) == 18

@pytest.mark.slow
def test_get_blob(setup_gcp):
    blob_name = "nwm.20210101/short_range/nwm.t01z.short_range.channel_rt.f001.conus.nc"
    blob_data = setup_gcp.get_blob(blob_name)
    assert type(blob_data) == bytes

@pytest.mark.slow
def test_get_Dataset(setup_gcp):
    blob_name = "nwm.20210101/short_range/nwm.t01z.short_range.channel_rt.f001.conus.nc"
    
    # Test default filter
    ds = setup_gcp.get_Dataset(blob_name)
    assert ds.feature_id.size > 4000
    assert ds.feature_id.size < 8000

    # Test filter with list
    ds = setup_gcp.get_Dataset(blob_name, 
        feature_id_filter=[101, 179])
    assert ds.feature_id.size == 2

    # Test filter with numpy.array
    ds = setup_gcp.get_Dataset(blob_name, 
        feature_id_filter=np.asarray([101, 179]))
    assert ds.feature_id.size == 2

    # Test filter with pandas.Series
    features = pd.Series(data=[101, 179])
    ds = setup_gcp.get_Dataset(blob_name, 
        feature_id_filter=features)
    assert ds.feature_id.size == 2

    # Test no filter
    ds = setup_gcp.get_Dataset(blob_name, 
        feature_id_filter=False)
    assert ds.feature_id.size > 8000

@pytest.mark.slow
def test_get_DataFrame(setup_gcp):
    blob_name = "nwm.20210101/short_range/nwm.t01z.short_range.channel_rt.f001.conus.nc"
    
    # Test default
    df = setup_gcp.get_DataFrame(blob_name)
    assert len(df.columns) == 4

    # Test all variables
    df = setup_gcp.get_DataFrame(blob_name, streamflow_only=False)
    assert len(df.columns) > 4

@pytest.mark.slow
def test_get_cycle(setup_gcp):
    # Test ANA
    df = setup_gcp.get_cycle(
        configuration="analysis_assim",
        reference_time="20210101T01Z"
    )
    assert df['value_time'].unique().size == 3

    # Test mapping
    df = df[df["usgs_site_code"] == "01360640"]
    assert df["nwm_feature_id"].iloc[0] == 6186112

@pytest.mark.slow
def test_cache_disable(setup_gcp):
    setup_gcp.cache_path = 'disabled_cache.h5'

    # Test ANA
    df = setup_gcp.get(
        configuration="analysis_assim",
        reference_time="20210101T01Z",
        cache_data=False
    )
    assert df['value_time'].unique().size == 3
    assert not setup_gcp.cache_path.exists()

@pytest.mark.slow
def test_cache_key(setup_gcp):
    # Test ANA
    df1 = setup_gcp.get(
        configuration="analysis_assim",
        reference_time="20210101T02Z",
        cache_data=True
    )
    first = df1['value_time'].unique().size

    with pd.HDFStore(setup_gcp.cache_path) as store:
        df2 = store[f"/{setup_gcp.cache_group}/analysis_assim/DT20210101T02Z"]
        second = df2['value_time'].unique().size
    assert first == second

@pytest.mark.slow
def test_get(setup_gcp):
    # Test ANA
    df = setup_gcp.get(
        configuration="analysis_assim",
        reference_time="20210101T01Z"
    )
    assert df['value_time'].unique().size == 3

    # Test Ext. ANA
    df = setup_gcp.get(
        configuration="analysis_assim_extend",
        reference_time="20210101T16Z"
    )
    assert df['value_time'].unique().size == 28

    # Test short range
    df = setup_gcp.get(
        configuration="short_range",
        reference_time="20210101T01Z"
    )
    assert df['value_time'].unique().size == 18

    # Test medium range
    df = setup_gcp.get(
        configuration="medium_range_mem1",
        reference_time="20210101T06Z"
    )
    assert df['value_time'].unique().size == 80

    # Test long range
    df = setup_gcp.get(
        configuration="long_range_mem1",
        reference_time="20210101T06Z"
    )
    assert df['value_time'].unique().size == 120

    # Test Hawaii ANA
    df = setup_gcp.get(
        configuration="analysis_assim_hawaii",
        reference_time="20210101T01Z"
    )
    assert df['value_time'].unique().size == 3

    # Test Hawaii Short Range
    df = setup_gcp.get(
        configuration="short_range_hawaii",
        reference_time="20210101T00Z"
    )
    assert df['value_time'].unique().size == 60

    # Test Puerto Rico ANA
    df = setup_gcp.get(
        configuration="analysis_assim_puertorico",
        reference_time="20210501T00Z"
    )
    assert df['value_time'].unique().size == 3

    # Test Puerto Rico Short Range
    df = setup_gcp.get(
        configuration="short_range_puertorico",
        reference_time="20210501T06Z"
    )
    assert df['value_time'].unique().size == 48

@pytest.mark.slow
def test_get_no_da(setup_gcp):
    # No DA Cycles
    cycles = [
        ('analysis_assim_no_da', "20210501T06Z", 3),
        ('analysis_assim_extend_no_da', "20210501T16Z", 28),
        ('analysis_assim_hawaii_no_da', "20210501T00Z", 12),
        ('analysis_assim_long_no_da', "20210501T00Z", 12),
        ('analysis_assim_puertorico_no_da', "20210501T00Z", 3),
        ('medium_range_no_da', "20210501T00Z", 80),
        ('short_range_hawaii_no_da', "20210501T00Z", 192),
        ('short_range_puertorico_no_da', "20210501T06Z", 48)
    ]
    # Test
    for cycle, ref_tm, validate in cycles:
        df = setup_gcp.get(
            configuration=cycle,
            reference_time=ref_tm
        )
        assert df['value_time'].unique().size == validate

def test_invalid_configuration_exception(setup_gcp):
    # Test invalid configuration
    with pytest.raises(Exception):
        df = setup_gcp.get(
            configuration="medium_range",
            reference_time="20210101T06Z"
        )

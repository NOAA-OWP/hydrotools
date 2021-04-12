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
    assert setup_gcp.crosswalk['usgs_site_code'].count() < 8000

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
    print(df.info())
    assert len(df.columns) == 4

    # Test all variables
    df = setup_gcp.get_DataFrame(blob_name, drop_variables=[])
    assert len(df.columns) > 4

@pytest.mark.slow
def test_get(setup_gcp):
    # Test ANA
    df = setup_gcp.get(
        configuration="analysis_assim",
        reference_time="20210101T01Z"
    )
    assert df['valid_time'].unique().size == 3

    # Test Ext. ANA
    df = setup_gcp.get(
        configuration="analysis_assim_extend",
        reference_time="20210101T16Z"
    )
    assert df['valid_time'].unique().size == 28

    # Test short range
    df = setup_gcp.get(
        configuration="short_range",
        reference_time="20210101T01Z"
    )
    assert df['valid_time'].unique().size == 18

    # Test medium range
    df = setup_gcp.get(
        configuration="medium_range_mem1",
        reference_time="20210101T06Z"
    )
    assert df['valid_time'].unique().size == 80

    # Test long range
    df = setup_gcp.get(
        configuration="long_range_mem1",
        reference_time="20210101T06Z"
    )
    assert df['valid_time'].unique().size == 120

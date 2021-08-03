import pytest
from hydrotools.nwm_client import http as nwm
from os import cpu_count
import numpy as np
import pandas as pd

@pytest.fixture
def setup_nwm():
    return nwm.NWMDataService(
        server="http://0.0.0.0:8000/data/"
    )

def test_bucket_name(setup_nwm):
    assert (setup_nwm.server) == "http://0.0.0.0:8000/data/"

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

# @pytest.mark.slow
# def test_list_blobs(setup_nwm):
#     blob_list = setup_nwm.list_blobs(
#         configuration="short_range",
#         reference_time="20210101T01Z"
#     )

#     assert len(blob_list) == 18

# @pytest.mark.slow
# def test_get_blob(setup_nwm):
#     blob_name = "nwm.20210101/short_range/nwm.t01z.short_range.channel_rt.f001.conus.nc"
#     blob_data = setup_nwm.get_blob(blob_name)
#     assert type(blob_data) == bytes

# @pytest.mark.slow
# def test_get_Dataset(setup_nwm):
#     blob_name = "nwm.20210101/short_range/nwm.t01z.short_range.channel_rt.f001.conus.nc"
    
#     # Test default filter
#     ds = setup_nwm.get_Dataset(blob_name)
#     assert ds.feature_id.size > 4000
#     assert ds.feature_id.size < 8000

#     # Test filter with list
#     ds = setup_nwm.get_Dataset(blob_name, 
#         feature_id_filter=[101, 179])
#     assert ds.feature_id.size == 2

#     # Test filter with numpy.array
#     ds = setup_nwm.get_Dataset(blob_name, 
#         feature_id_filter=np.asarray([101, 179]))
#     assert ds.feature_id.size == 2

#     # Test filter with pandas.Series
#     features = pd.Series(data=[101, 179])
#     ds = setup_nwm.get_Dataset(blob_name, 
#         feature_id_filter=features)
#     assert ds.feature_id.size == 2

#     # Test no filter
#     ds = setup_nwm.get_Dataset(blob_name, 
#         feature_id_filter=False)
#     assert ds.feature_id.size > 8000

# @pytest.mark.slow
# def test_get_DataFrame(setup_nwm):
#     blob_name = "nwm.20210101/short_range/nwm.t01z.short_range.channel_rt.f001.conus.nc"
    
#     # Test default
#     df = setup_nwm.get_DataFrame(blob_name)
#     assert len(df.columns) == 4

#     # Test all variables
#     df = setup_nwm.get_DataFrame(blob_name, streamflow_only=False)
#     assert len(df.columns) > 4

# @pytest.mark.slow
# def test_get_cycle(setup_nwm):
#     # Test ANA
#     df = setup_nwm.get_cycle(
#         configuration="analysis_assim",
#         reference_time="20210101T01Z"
#     )
#     assert df['value_time'].unique().size == 3

#     # Test mapping
#     df = df[df["usgs_site_code"] == "01360640"]
#     assert df["nwm_feature_id"].iloc[0] == 6186112

# @pytest.mark.slow
# def test_cache_disable(setup_nwm):
#     setup_nwm.cache_path = 'disabled_cache.h5'

#     # Test ANA
#     df = setup_nwm.get(
#         configuration="analysis_assim",
#         reference_time="20210101T01Z",
#         cache_data=False
#     )
#     assert df['value_time'].unique().size == 3
#     assert not setup_nwm.cache_path.exists()

# @pytest.mark.slow
# def test_cache_key(setup_nwm):
#     # Test ANA
#     df1 = setup_nwm.get(
#         configuration="analysis_assim",
#         reference_time="20210101T02Z",
#         cache_data=True
#     )
#     first = df1['value_time'].unique().size

#     with pd.HDFStore(setup_nwm.cache_path) as store:
#         df2 = store[f"/{setup_nwm.cache_group}/analysis_assim/DT20210101T02Z"]
#         second = df2['value_time'].unique().size
#     assert first == second

# @pytest.mark.slow
# def test_get(setup_nwm):
#     # Test ANA
#     df = setup_nwm.get(
#         configuration="analysis_assim",
#         reference_time="20210101T01Z"
#     )
#     assert df['value_time'].unique().size == 3

#     # Test Ext. ANA
#     df = setup_nwm.get(
#         configuration="analysis_assim_extend",
#         reference_time="20210101T16Z"
#     )
#     assert df['value_time'].unique().size == 28

#     # Test short range
#     df = setup_nwm.get(
#         configuration="short_range",
#         reference_time="20210101T01Z"
#     )
#     assert df['value_time'].unique().size == 18

#     # Test medium range
#     df = setup_nwm.get(
#         configuration="medium_range_mem1",
#         reference_time="20210101T06Z"
#     )
#     assert df['value_time'].unique().size == 80

#     # Test long range
#     df = setup_nwm.get(
#         configuration="long_range_mem1",
#         reference_time="20210101T06Z"
#     )
#     assert df['value_time'].unique().size == 120

#     # Test Hawaii ANA
#     df = setup_nwm.get(
#         configuration="analysis_assim_hawaii",
#         reference_time="20210101T01Z"
#     )
#     assert df['value_time'].unique().size == 3

#     # Test Hawaii Short Range
#     df = setup_nwm.get(
#         configuration="short_range_hawaii",
#         reference_time="20210101T00Z"
#     )
#     assert df['value_time'].unique().size == 60

#     # Test Puerto Rico ANA
#     df = setup_nwm.get(
#         configuration="analysis_assim_puertorico",
#         reference_time="20210501T00Z"
#     )
#     assert df['value_time'].unique().size == 3

#     # Test Puerto Rico Short Range
#     df = setup_nwm.get(
#         configuration="short_range_puertorico",
#         reference_time="20210501T06Z"
#     )
#     assert df['value_time'].unique().size == 48

# @pytest.mark.slow
# def test_get_no_da(setup_nwm):
#     # No DA Cycles
#     cycles = [
#         ('analysis_assim_no_da', "20210501T06Z", 3),
#         ('analysis_assim_extend_no_da', "20210501T16Z", 28),
#         ('analysis_assim_hawaii_no_da', "20210501T00Z", 12),
#         ('analysis_assim_long_no_da', "20210501T00Z", 12),
#         ('analysis_assim_puertorico_no_da', "20210501T00Z", 3),
#         ('medium_range_no_da', "20210501T00Z", 80),
#         ('short_range_hawaii_no_da', "20210501T00Z", 192),
#         ('short_range_puertorico_no_da', "20210501T06Z", 48)
#     ]
#     # Test
#     for cycle, ref_tm, validate in cycles:
#         df = setup_nwm.get(
#             configuration=cycle,
#             reference_time=ref_tm
#         )
#         assert df['value_time'].unique().size == validate

def test_invalid_configuration_exception(setup_nwm):
    # Test invalid configuration
    with pytest.raises(Exception):
        df = setup_nwm.get(
            configuration="medium_range",
            reference_time="20210101T06Z"
        )

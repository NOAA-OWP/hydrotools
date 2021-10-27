import pytest
from hydrotools.nwm_client_new.NWMClient import NWMFileClient
from hydrotools.nwm_client_new.NWMFileCatalog import HTTPFileCatalog
import pandas as pd
from tempfile import TemporaryDirectory
from hydrotools.nwm_client_new.NWMClient import CacheNotFoundError, QueryError

# Set reference time
yesterday = pd.Timestamp.utcnow() - pd.Timedelta("1D")
reference_time_gcp = yesterday.strftime("%Y%m%dT%-HZ")
reference_time_http = (yesterday+pd.Timedelta("1H")).strftime("%Y%m%dT%-HZ")

# Canonical columns
canonical_columns = [
    "nwm_feature_id",
    "reference_time",
    "usgs_site_code",
    "value_time",
    "measurement_unit",
    "variable_name",
    "value",
    "configuration"
]

@pytest.fixture
def setup_gcp():
    return NWMFileClient()

@pytest.fixture
def setup_http():
    catalog = HTTPFileCatalog(
        server="https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"
        )
    return NWMFileClient(catalog=catalog)

@pytest.mark.slow
def test_gcp_get_cycle(setup_gcp):
    with TemporaryDirectory() as td:
        df = setup_gcp.get_cycle(
            configuration="analysis_assim",
            reference_time=reference_time_gcp,
            netcdf_dir=td
        ).head()
        for col in canonical_columns:
            assert col in df
        assert "analysis_assim" in df["configuration"].values
        assert "streamflow" in df["variable_name"].values

@pytest.mark.slow
def test_gcp_client(setup_gcp):
    df = setup_gcp.get(
        configuration="analysis_assim",
        reference_times=[reference_time_gcp]
    ).head()
    for col in canonical_columns:
        assert col in df
    assert "analysis_assim" in df["configuration"].values
    assert "streamflow" in df["variable_name"].values

@pytest.mark.slow
def test_http_client(setup_http):
    df = setup_http.get(
        configuration="analysis_assim",
        reference_times=[reference_time_http]
    ).head()
    for col in canonical_columns:
        assert col in df
    assert "analysis_assim" in df["configuration"].values
    assert "streamflow" in df["variable_name"].values

def test_CacheNotFoundError(setup_gcp):
    with pytest.raises(CacheNotFoundError):
        setup_gcp.dataframe_cache = None
        df = setup_gcp.get(
            configuration="analysis_assim",
            reference_times=[reference_time_gcp]
        ).head()

def test_QueryError(setup_gcp):
    with TemporaryDirectory() as td:
        with pytest.raises(QueryError):
            df = setup_gcp.get_cycle(
                configuration="analysis_assim",
                reference_time="20T00Z",
                netcdf_dir=td
            ).head()
    with pytest.raises(QueryError):
        df = setup_gcp.get(
            configuration="analysis_assim",
            reference_times=["20T00Z", "30T01Z"]
        ).head()

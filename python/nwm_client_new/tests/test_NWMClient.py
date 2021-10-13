import pytest
from hydrotools.nwm_client_new.NWMClient import NWMFileClient
from hydrotools.nwm_client_new.NWMFileCatalog import HTTPFileCatalog
import pandas as pd

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

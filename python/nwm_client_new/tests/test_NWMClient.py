import pytest
from hydrotools.nwm_client_new.NWMFileClient import NWMFileClient
from hydrotools.nwm_client_new.HTTPFileCatalog import HTTPFileCatalog
import pandas as pd
from hydrotools.nwm_client_new.NWMClient import StoreNotFoundError, QueryError

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
def test_gcp_get_dataset(setup_gcp):
    with pytest.warns(UserWarning):
        ds = setup_gcp.get_dataset(
            configuration="analysis_assim",
            reference_time=reference_time_gcp
        )
        assert "reference_time" in ds
        assert "feature_id" in ds
        assert "time" in ds
        assert "streamflow" in ds
        assert ds.attrs["model_configuration"] == "analysis_and_assimilation"
        ds.close()

@pytest.mark.slow
def test_gcp_client(setup_gcp):
    with pytest.warns(UserWarning):
        df = setup_gcp.get(
            configurations=["analysis_assim"],
            reference_times=[reference_time_gcp]
        ).head()
        for col in canonical_columns:
            assert col in df
        assert "analysis_and_assimilation" in df["configuration"].values
        assert "streamflow" in df["variable_name"].values

@pytest.mark.slow
def test_http_client(setup_http):
    with pytest.warns(UserWarning):
        df = setup_http.get(
            configurations=["analysis_assim"],
            reference_times=[reference_time_http]
        ).head()
        for col in canonical_columns:
            assert col in df
        assert "analysis_and_assimilation" in df["configuration"].values
        assert "streamflow" in df["variable_name"].values

def test_StoreNotFoundError(setup_gcp):
    with pytest.raises(StoreNotFoundError):
        setup_gcp.dataframe_store = None
        df = setup_gcp.get(
            configurations=["analysis_assim"],
            reference_times=[reference_time_gcp]
        ).head()

def test_QueryError(setup_gcp):
    with pytest.raises(QueryError):
        ds = setup_gcp.get_dataset(
            configuration="analysis_assim",
            reference_time="2050-08-01 10:00"
        )

    with pytest.raises(QueryError):
        df = setup_gcp.get(
            configurations=["analysis_assim"],
            reference_times=["2050-08-01 10:00"]
        ).head()

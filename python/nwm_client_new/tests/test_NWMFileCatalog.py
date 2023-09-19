import pytest
from hydrotools.nwm_client_new.GCPFileCatalog import GCPFileCatalog
from hydrotools.nwm_client_new.HTTPFileCatalog import HTTPFileCatalog
from hydrotools.nwm_client_new.AzureFileCatalog import AzureFileCatalog
import pandas as pd

# Set reference time
yesterday = pd.Timestamp.utcnow() - pd.Timedelta("1D")
reference_time = yesterday.strftime("%Y%m%dT%-HZ")

@pytest.fixture
def setup_gcp():
    return GCPFileCatalog()

@pytest.fixture
def setup_http():
    return HTTPFileCatalog(
        server="https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"
        )

@pytest.fixture
def setup_azure():
    return AzureFileCatalog()

def test_parameters(setup_gcp, setup_http, setup_azure):
    assert setup_gcp.configurations
    assert setup_http.configurations
    assert setup_azure.configurations

    assert setup_http.server == "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"
    assert setup_http.ssl_context

    assert setup_gcp.bucket_name == "national-water-model"

    assert setup_azure.server == "https://noaanwm.blob.core.windows.net/"

@pytest.mark.slow
def test_gcp_list_blobs(setup_gcp):
    blobs = setup_gcp.list_blobs(
        configuration="analysis_assim",
        reference_time=pd.Timestamp(reference_time)
    )
    assert len(blobs) == 3

@pytest.mark.slow
def test_http_list_blobs(setup_http):
    blobs = setup_http.list_blobs(
        configuration="analysis_assim",
        reference_time=pd.Timestamp(reference_time)
    )
    assert len(blobs) == 3

@pytest.mark.slow
def test_azure_list_blobs(setup_azure):
    blobs = setup_azure.list_blobs(
        configuration="analysis_assim",
        reference_time=pd.Timestamp(reference_time)
    )
    assert len(blobs) == 3
import pytest
from hydrotools.gcp_client import gcp
from os import cpu_count

@pytest.fixture
def setup_gcp():
    return gcp.NWMDataService()

def test_bucket_name(setup_gcp):
    assert (setup_gcp.bucket_name) == "national-water-model"

def test_max_processes(setup_gcp):
    count = cpu_count() - 2
    assert (setup_gcp.max_processes) == count

@pytest.mark.slow
def test_get(setup_gcp):
    # TODO
    """Test data retrieval and parsing"""
    df = setup_gcp.get(
        configuration='analysis_assim_extend',
        reference_time='20201209T16Z'
    )
    assert not df.empty

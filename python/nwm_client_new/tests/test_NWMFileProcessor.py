import pytest
from hydrotools.nwm_client_new.NWMFileProcessor import NWMFileProcessor
from pathlib import Path

input_directory = Path(__file__).parent / "short_range"

def test_get_dataset():
    with pytest.warns(UserWarning):
        ds = NWMFileProcessor.get_dataset(input_directory)
        assert "reference_time" in ds
        assert "time" in ds
        assert "streamflow" in ds
        ds.close()

@pytest.mark.slow
def test_convert_to_dask_dataframe():
    ds = NWMFileProcessor.get_dataset(input_directory, feature_id_filter=[])
    df = NWMFileProcessor.convert_to_dask_dataframe(ds)
    assert df.npartitions == 2
    ds.close()

@pytest.mark.slow
def test_convert_to_dataframe():
    with pytest.warns(UserWarning):
        ds = NWMFileProcessor.get_dataset(input_directory)
        df = NWMFileProcessor.convert_to_dataframe(ds)
        assert "feature_id" in df
        ds.close()

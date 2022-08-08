import pytest
from hydrotools.nwm_client_new.NWMFileProcessor import NWMFileProcessor
from pathlib import Path

input_directory = Path(__file__).parent / "short_range"


def test_get_dataset():
    files = input_directory.glob("*.nc")
    with pytest.warns(UserWarning):
        ds = NWMFileProcessor.get_dataset(files)
        assert "reference_time" in ds
        assert "time" in ds
        assert "streamflow" in ds
        ds.close()

@pytest.mark.slow
def test_convert_to_dask_dataframe():
    files = input_directory.glob("*.nc")
    ds = NWMFileProcessor.get_dataset(files, feature_id_filter=[])
    df = NWMFileProcessor.convert_to_dask_dataframe(ds)
    assert df.npartitions == 2
    ds.close()

@pytest.mark.slow
def test_convert_to_dataframe():
    files = input_directory.glob("*.nc")
    with pytest.warns(UserWarning):
        ds = NWMFileProcessor.get_dataset(files)
        df = NWMFileProcessor.convert_to_dataframe(ds)
        assert "feature_id" in df
        ds.close()

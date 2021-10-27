import pytest
from hydrotools.nwm_client_new.ParquetCache import ParquetCache
from tempfile import TemporaryDirectory
import pandas as pd
import dask.dataframe as dd

def make_dataframe(column_a: str):
    df = pd.DataFrame({
        column_a: [1.0, 2.0, 3.0],
        "b": [0.4, 0.5, 0.6]
    })
    return dd.from_pandas(df, npartitions=1)

@pytest.fixture
def setup_cache():
    with TemporaryDirectory() as td:
        return ParquetCache(
            f"{td}/nwm_cache.parquet",
            write_index=False,
            compression="snappy"
        )

def test_parameters(setup_cache):
    assert not setup_cache.parameters["write_index"]
    assert setup_cache.parameters["compression"] == "snappy"
    assert setup_cache.directory.name == "nwm_cache.parquet"

def test_get(setup_cache):
    # Retrieve and cache
    df = setup_cache.get(
        function=make_dataframe,
        subdirectory="my_data",
        column_a="aa"
    ).compute()
    
    assert "aa" in df

    # Retrieve from cache
    df = setup_cache.get(
        function=make_dataframe,
        subdirectory="my_data",
        column_a="aa"
    ).compute()
    
    assert "aa" in df

    # Retrieve directly from cache
    ifile = setup_cache.directory/"my_data"
    df = dd.read_parquet(ifile).compute()
    
    assert "aa" in df

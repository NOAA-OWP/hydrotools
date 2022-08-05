from tkinter import N
import pytest
from hydrotools.nwm_client_new.ParquetStore import ParquetStore
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
def setup_store():
    with TemporaryDirectory() as td:
        return ParquetStore(
            f"{td}/nwm_store.parquet",
            write_index=False,
            compression="snappy"
        )

def test_parameters(setup_store):
    assert not setup_store.parameters["write_index"]
    assert setup_store.parameters["compression"] == "snappy"
    assert setup_store.root.name == "nwm_store.parquet"
    assert str(setup_store) == str(setup_store.root)

def test_set_get(setup_store):
    # Retrieve and store
    setup_store["my_data"] = make_dataframe("aa")
    df = setup_store["my_data"]
    
    assert "aa" in df

    # Retrieve directly from store
    ifile = setup_store.root/"my_data"
    df = dd.read_parquet(ifile).compute()
    
    assert "aa" in df

def test_key_error(setup_store):
    with pytest.raises(KeyError):
        df = setup_store["my_data"]

def test_set_delete(setup_store):
    setup_store["my_data"] = make_dataframe("aa")

    setup_store.pop("my_data", None)
    assert "my_data" not in setup_store

def test_length(setup_store):
    assert len(setup_store) == 0

    setup_store["my_data"] = make_dataframe("aa")

    assert len(setup_store) == 1

def test_iter(setup_store):
    setup_store["my_data"] = make_dataframe("aa")
    for key, val in setup_store.items():
        assert key == "my_data"
        assert "aa" in val.compute()

def test_append(setup_store):
    setup_store["my_data"] = make_dataframe("aa")
    setup_store.append("my_data", make_dataframe("aa"))

    expected = make_dataframe("aa").compute()["aa"].count() * 2
    result = setup_store["my_data"].compute()["aa"].count()
    assert result == expected

def test_context():
    with TemporaryDirectory() as td:
        with ParquetStore(f"{td}/nwm_store.parquet") as store:
            assert store.root.name == "nwm_store.parquet"

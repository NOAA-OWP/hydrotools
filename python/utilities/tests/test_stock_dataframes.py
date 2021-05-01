import pytest
from  hydrotools.utilities import stock_dataframes
import pandas as pd
import warnings

def test_random_dataframe():
    # Generate a random dataframe
    with pytest.warns(UserWarning):
        df = stock_dataframes.random_dataframe()

    # Test defaults
    for col in ['value_time', 'value']:
        assert col in df
    assert df['value'].count() == 10
    assert pd.Timestamp('1970-01-01T01') == df['value_time'].iloc[0]
    assert pd.infer_freq(df['value_time']) == 'H'
    

import pytest
from hydrotools.caches.hdf import HDFCache
import pandas as pd
import numpy as np
import tempfile
from pathlib import Path

def test_cache():
    def random_dataframe():
        return pd.DataFrame({
            'A': np.random.random(100),
            'B': np.random.random(100)
        })

    with tempfile.TemporaryDirectory() as tmpdirname:
        cache_path = Path(tmpdirname) / 'test_cache.h5'

        cache = HDFCache(cache_path)
        df1 = cache.get(random_dataframe, 'data/results')
        df2 = cache.get(random_dataframe, 'data/results')
        assert df1.equals(df2)
        cache.close()

        with pd.HDFStore(cache_path) as store:
            df3 = store['data/results']
            assert df1.equals(df3)

def test_cache_context():
    def random_dataframe():
        return pd.DataFrame({
            'A': np.random.random(100),
            'B': np.random.random(100)
        })

    with tempfile.TemporaryDirectory() as tmpdirname:
        cache_path = Path(tmpdirname) / 'test_cache.h5'

        with HDFCache(cache_path) as cache:
            df1 = cache.get(random_dataframe, 'data/results')
            df2 = cache.get(random_dataframe, 'data/results')
            assert df1.equals(df2)

def test_string_encoding():
    def random_dataframe():
        return pd.DataFrame({
            'A': np.random.random(100),
            'B': np.random.random(100)
        })

    with tempfile.TemporaryDirectory() as tmpdirname:
        cache_path = Path(tmpdirname) / 'test_cache.h5'

        cache = HDFCache(cache_path)

        with pytest.raises(TypeError):
            df = cache.get(random_dataframe, b'data/results')

        utf_key = 'data/results'
        ascii_key = b'data/results'.decode('ascii', 'replace')

        df_utf = cache.get(random_dataframe, utf_key)
        df_ascii = cache.get(random_dataframe, ascii_key)
        assert df_utf.equals(df_ascii)

        cache.close()

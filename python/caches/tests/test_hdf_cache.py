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

        with HDFCache(cache_path) as cache:
            df1 = cache.get(random_dataframe, 'data/results')
            df2 = cache.get(random_dataframe, 'data/results')
            assert df1.equals(df2)

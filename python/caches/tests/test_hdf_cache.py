import pytest
from hydrotools.caches.hdf import HDFCache
import pandas as pd
import numpy as np
from pathlib import Path

cache_path = Path('test_cache.h5')

def test_cache():
    def random_dataframe():
        return pd.DataFrame({
            'A': np.random.random(100),
            'B': np.random.random(100)
        })

    with HDFCache('test_cache.h5') as cache:
        df1 = cache.get(random_dataframe, 'data/results')
        df2 = cache.get(random_dataframe, 'data/results')
        assert df1.equals(df2)

    cache_path.unlink()

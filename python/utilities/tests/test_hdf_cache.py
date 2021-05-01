import pytest
from  hydrotools.utilities.hdf_cache import hdf_cache
import pandas as pd
import numpy as np
from pathlib import Path
import warnings

def test_hdf_cache():
    # Make a DataFrame function
    @hdf_cache
    def make_a_frame():
        return pd.DataFrame({
            'A': np.random.random(10),
            'B': np.random.random(10)
        })

    # Setup
    hdf_cache_path = Path('make_a_frame_cache.h5')
    hdf_cache_key = "/make_a_frame/test1"

    # Create and cache the frame
    df1 = make_a_frame(
        hdf_cache_path=hdf_cache_path,
        hdf_cache_key=hdf_cache_key
    )

    # Retrieve original frame
    df2 = make_a_frame(
        hdf_cache_path=hdf_cache_path,
        hdf_cache_key=hdf_cache_key
    )

    # Retrieve an uncached DataFrame
    with pytest.warns(UserWarning):
        df3 = make_a_frame()

    # Test for equality/inequality
    for col in df1:
        assert np.all(df1[col] == df2[col])
        assert np.all(df1[col] != df3[col])

    # Delete the cache
    hdf_cache_path.unlink()

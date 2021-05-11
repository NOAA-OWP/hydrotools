import pytest
from hydrotools.caches.hdf import HDFCache

import pandas as pd
from time import sleep

def test_cache():
    # Some long running process that returns a pandas.DataFrame
    def long_process(cols, rows):
        sleep(1.0)
        data = {f'col_{i}' : [j for j in range(rows)] for i in range(cols)}
        return pd.DataFrame(data)

    # Setup the cache with a context manager
    #  Similar to setting up a pandas.HDFStore
    with HDFCache(
        path='test_cache.h5',
        complevel=1,
        complib='zlib',
        fletcher32=True
        ) as cache:
        # The first call runs long_process and stores the result
        df = cache.get(long_process, 'data/results', cols=10, rows=1000000)


        # The second call retrieves the result from cache without 
        #  running long_process
        df = cache.get(long_process, 'data/results', cols=10, rows=1000000)
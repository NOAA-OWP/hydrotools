# HydroTools :: Utilities

This subpackage implements various methods commonly used by other `hydrotools` packages. A list of current utilities is given below. See the [Utilities Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.utilities.html) for a complete list and description of the currently available methods. To report bugs or request new features, submit an issue through the [HydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

## List of Utility Modules

1. `hdf_cache`: Add caching features to methods that return `pandas.DataFrame`
2. `stock_dataframes`: Generate dummy `pandas.DataFrame` for testing

## Installation

In accordance with the python community, we support and advise the usage of virtual
environments in any workflow using python. In the following installation guide, we
use python's built-in `venv` module to create a virtual environment in which the
tool will be installed. Note this is just personal preference, any python virtual
environment manager should work just fine (`conda`, `pipenv`, etc. ).

```bash
# Create and activate python environment, requires python >= 3.8
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip

# Install utilities
$ python3 -m pip install hydrotools.utilities
```

## Usage

The following example demonstrates how one might use `hydrotools.utilities` to generate random `DataFrame` and cache `DataFrame` results for later retrieval.

### HDF Cache
#### Code
```python
# Import the Utilities
from hydrotools.utilities.hdf_cache import hdf_cache
import pandas as pd
from pathlib import Path
import time
execution_times = [0, 0, 0]

# Create a caching function
@hdf_cache
def long_running_process(n=10):
    time.sleep(1.0)
    return pd.DataFrame({
        'A': [i for i in range(n)],
        'B': [i for i in range(n)]
    })

# Call the function without caching
start = time.perf_counter()
df = long_running_process()
execution_times[0] = time.perf_counter() - start
print('(1) Run process, no caching')
print('=======================')
print(df)
print()

# Call the function with caching
start = time.perf_counter()
df = long_running_process(
    hdf_cache_path='interim_data.h5',
    hdf_cache_key='/data/results/AB'
)
execution_times[1] = time.perf_counter() - start
print('(2) Run the process and cache')
print('=========================')
print(df)
print()

# This second call with caching will check the cache first, 
#  then only run the process if it can't find a cached DataFrame
start = time.perf_counter()
df = long_running_process(
    hdf_cache_path='interim_data.h5',
    hdf_cache_key='/data/results/AB'
)
execution_times[2] = time.perf_counter() - start
print('(3) Recover cached result without running the process')
print('=====================================================')
print(df)
print()

# Delete the cache
Path('interim_data.h5').unlink()
print('Cache deleted')
print()

# Report times
print('Execution Times')
print('===============')
for idx, t in enumerate(execution_times):
    print(f"({idx}) {t:.3f} s")

```
#### Output
```console
UserWarning: long_running_process caching disabled. Enable by setting hdf_cache_path and hdf_cache_key
  warnings.warn(message)
Run process, no caching
=======================
   A  B
0  0  0
1  1  1
2  2  2
3  3  3
4  4  4
5  5  5
6  6  6
7  7  7
8  8  8
9  9  9

Run the process and cache
=========================
   A  B
0  0  0
1  1  1
2  2  2
3  3  3
4  4  4
5  5  5
6  6  6
7  7  7
8  8  8
9  9  9

Recover cached result without running the process
=================================================
   A  B
0  0  0
1  1  1
2  2  2
3  3  3
4  4  4
5  5  5
6  6  6
7  7  7
8  8  8
9  9  9

Cache deleted

Execution Times
===============
(0) 1.002 s
(1) 1.137 s
(2) 0.006 s
```

### Stock DataFrames
#### Code
```python
# Import the Utilities
from hydrotools.utilities.stock_dataframes import random_dataframe
import pandas as pd

# Create a DataFrame with random data, do not cache
#  Note random_dataframe is a caching method, so it will raise
#  a warning if caching is not enabled.
df = random_dataframe()
print('Uncached DataFrame')
print('==================')
print(df)
print()

# Create a DataFrame with random data and cache
df = random_dataframe(
    hdf_cache_path='random_dataframes.h5',
    hdf_cache_key='/data/random/A'
)
print('Cached DataFrame')
print('==================')
print(df)
print()

# We can retrieve the same DataFrame by rerunning the
#  previous method with same parameters
df = random_dataframe(
    hdf_cache_path='random_dataframes.h5',
    hdf_cache_key='/data/random/A'
)
print('Cached DataFrame (2nd run)')
print('==========================')
print(df)
print()

# We can also retrieve the DataFrame manually using the key
df = pd.read_hdf('random_dataframes.h5', key='/data/random/A')
print('Cached DataFrame (pandas.read_hdf)')
print('==================================')
print(df)
```
#### Output
```console
UserWarning: random_dataframe caching disabled. Enable by setting hdf_cache_path and hdf_cache_key
  warnings.warn(message)
Uncached DataFrame
==================
           value_time     value
0 1970-01-01 01:00:00  0.937773
1 1970-01-01 02:00:00  0.468992
2 1970-01-01 03:00:00  0.734990
3 1970-01-01 04:00:00  0.757705
4 1970-01-01 05:00:00  0.198859
5 1970-01-01 06:00:00  0.655419
6 1970-01-01 07:00:00  0.083886
7 1970-01-01 08:00:00  0.761608
8 1970-01-01 09:00:00  0.296274
9 1970-01-01 10:00:00  0.971867

Cached DataFrame
==================
           value_time     value
0 1970-01-01 01:00:00  0.425507
1 1970-01-01 02:00:00  0.697758
2 1970-01-01 03:00:00  0.932153
3 1970-01-01 04:00:00  0.839545
4 1970-01-01 05:00:00  0.166794
5 1970-01-01 06:00:00  0.105933
6 1970-01-01 07:00:00  0.523726
7 1970-01-01 08:00:00  0.859374
8 1970-01-01 09:00:00  0.815113
9 1970-01-01 10:00:00  0.767973

Cached DataFrame (2nd run)
==================
           value_time     value
0 1970-01-01 01:00:00  0.425507
1 1970-01-01 02:00:00  0.697758
2 1970-01-01 03:00:00  0.932153
3 1970-01-01 04:00:00  0.839545
4 1970-01-01 05:00:00  0.166794
5 1970-01-01 06:00:00  0.105933
6 1970-01-01 07:00:00  0.523726
7 1970-01-01 08:00:00  0.859374
8 1970-01-01 09:00:00  0.815113
9 1970-01-01 10:00:00  0.767973

Cached DataFrame (pandas.read_hdf)
==================
           value_time     value
0 1970-01-01 01:00:00  0.425507
1 1970-01-01 02:00:00  0.697758
2 1970-01-01 03:00:00  0.932153
3 1970-01-01 04:00:00  0.839545
4 1970-01-01 05:00:00  0.166794
5 1970-01-01 06:00:00  0.105933
6 1970-01-01 07:00:00  0.523726
7 1970-01-01 08:00:00  0.859374
8 1970-01-01 09:00:00  0.815113
9 1970-01-01 10:00:00  0.767973

Cache deleted
```

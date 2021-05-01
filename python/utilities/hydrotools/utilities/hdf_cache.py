"""
====================================
HDF5-backed pandas.DataFrame caching
====================================
Implements methods to create and manage a DataFrame cache backed by
HDF5 files.

Methods
-------
hdf_cache

"""

import pandas as pd
from functools import wraps
from typing import Callable
import warnings

def hdf_cache(function: Callable) -> Callable:
    """A function decorator that returns a caching version of function that 
    accepts two new keyword arguments.
    
    Parameters
    ----------
    function: callable, required
        A function that returns a pandas.DataFrame.

    Returns
    -------
    callable
        A caching version of the decorated function.

    Warnings
    --------
    Warns if parameters for a caching function are not set.
    UserWarning: {function} caching disabled. Enable by setting 
        hdf_cache_path and hdf_cache_key

    Notes
    -----
    The decorated function will gain two new parameters.
    hdf_cache_path: str, path object, pandas.HDFStore or file-like object, optional
        Path or buffer to writable/readable HDF5 file location to use as a 
        cache for processed pandas.DataFrames. Must also set hdf_cache_key.
    hdf_cache_key: str, optional
        Key used to store and retrieve pandas.DataFrame from an HDF5 file. This 
        functionality stores DataFrames as PyTables. Must also set 
        hdf_cache_path.

    """
    @wraps(function)
    def dataframe_caching_function(*args, **kwargs):
        # Check for HDFStore key keyword
        if 'hdf_cache_path' in kwargs:
            if 'hdf_cache_key' in kwargs:
                # Get path and key
                path_or_buf = kwargs['hdf_cache_path']
                key = kwargs['hdf_cache_key']

                # Check HDFStore
                with pd.HDFStore(path_or_buf) as store:
                    if key in store:
                        # Return cached result
                        return store[key]

                # Strip kwarg
                del kwargs['hdf_cache_path']
                del kwargs['hdf_cache_key']

                # Run the function
                df = function(*args, **kwargs)

                # Cache the result
                with pd.HDFStore(path_or_buf) as store:
                    if key not in store:
                        store.put(
                            value=df,
                            key=key,
                            format='table'
                        )
                # Return result after caching
                return df

        # Run the result without caching
        message = f"{function.__name__} caching disabled. Enable by setting hdf_cache_path and hdf_cache_key"
        warnings.warn(message)
        return function(*args, **kwargs)
    return dataframe_caching_function
    
"""
=================================
HDF5-backed Caching Functionality
=================================
Cache pandas objects resulting from long processes for later retrieval to avoid 
reprocessing.

Classes
---------
 - HDFCache

"""

import pandas as pd
from typing import Callable

class HDFCache:
    def __init__(self, path:str, format:str='table', *args, **kwargs):
        """
        Interface for caching pandas objects returned by long running 
        processes. The internal pandas.HDFStore is accessible 
        using the HDFCache.store property.

        Parameters
        ----------
        path: str
            File path to HDF5 file.
        format : 'fixed(f)|table(t)', default is 'table'
            Format to use when storing object in HDFStore. Value can be one of:
            ``'fixed'``
                Fixed format.  Fast writing/reading. Not-appendable, nor searchable. 
                    Fixed format is incompatible with pandas.Categorical data types.
            ``'table'``
                Table format.  Write as a PyTables Table structure which may perform
                worse but allow more flexible operations like searching / selecting
                subsets of the data.
        *args
            Additional arguments passed to pandas.HDFStore
        **kwargs
            Additional arguments passed to pandas.HDFStore
        """
        self._path = path
        self._format = format
        self._store = pd.HDFStore(path, *args, **kwargs)
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """
        Close the Pandas HDFStore.
        
        """
        self._store.close()

    def get(self, function: Callable, key: str, *args, **kwargs):
        """
        Check HDFStore for key and return the object. If key is not in 
        the cache, then run function and store the result for later retrieval.

        Parameters
        ----------
        function: Callable
            Function to run to produce the object for storage.
        key: str
            Key used to reference object in HDFStore.
        *args
            Additional arguments passed directly to function.
        **kwargs
            Additional arguments passed directly to function.

        Returns
        -------
        object
            Retrieve object from file.
        """
        # Validate key
        if type(key) != str:
            message = "key must be str type"
            raise TypeError(message)

        # Check cache and return if available
        if key in self.store:
            return self.store[key]

        # Run function
        df = function(*args, **kwargs)

        # Cache result
        if key not in self.store:
            self.store.put(
                key = key,
                value = df,
                format = self.format,
            )

        # Return result
        return df

    @property
    def store(self):
        return self._store

    @property
    def path(self):
        return self._path

    @property
    def format(self):
        return self._format
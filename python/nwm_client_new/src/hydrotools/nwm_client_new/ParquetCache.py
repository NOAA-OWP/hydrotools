"""
====================================
Parquet-backed Caching Functionality
====================================
Cache dask.dataframe.DataFrame for later retrieval to avoid reprocessing.

Classes
---------
 - ParquetCache

"""

import dask.dataframe as dd
from typing import Callable, Union
from pathlib import Path

class ParquetCache:
    def __init__(self, directory: Union[str, Path], **kwargs) -> None:
        """
        Interface for caching dask.dataframe.DataFrame resulting from long
        processes.

        Parameters
        ----------
        directory: str or pathlib.Path, required
            Path to parquet cache root directory.
        **kwargs
            Additional arguments passed to dask.dataframe.DataFrame.to_parquet
        """
        self.directory = directory
        self.parameters = kwargs
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def __del__(self):
        pass

    def __str__(self) -> str:
        return str(self.directory)

    def get(
        self,
        function: Callable,
        subdirectory: Union[str, Path],
        *args,
        **kwargs
        ) -> dd.DataFrame:
        """
        Check cache for subdirectory and return the object. If subdirectory 
        does not exist, then run function and store the result for later 
        retrieval.

        Parameters
        ----------
        function: Callable
            Function to run to produce the object for storage.
        subdirectory: str
            subdirectory used to reference object in parquet root directory.
        *args
            Additional arguments passed directly to function.
        **kwargs
            Additional arguments passed directly to function.

        Returns
        -------
        dask.dataframe.DataFrame
            Retrieve DataFrame from file.

        Examples
        --------
        >>> import pandas as pd
        >>> import dask.dataframe as dd
        >>> from time import sleep
        >>> from hydrotools.nwm_client_new.ParquetCache import ParquetCache

        >>> def my_long_running_process(data: dict) -> dd.DataFrame:
        >>>     # Some long running process
        >>>     sleep(0.2)
        >>>     return dd.from_pandas(pd.DataFrame(data), npartitions=1)

        >>> # Use context manager to setup cache
        >>> with ParquetCache(
        >>>     "my_cache.parquet",
        >>>     write_index=False,
        >>>     compression="snappy"
        >>>     ) as cache:
        >>>     # Fabricate some data to feed the function
        >>>     my_data = {"A": [1, 2, 3]}

        >>>     # Call the function with caching
        >>>     df = cache.get(
        >>>         function=my_long_running_process,
        >>>         subdirectory="my_dataframe",
        >>>         data=my_data
        >>>     )
        """
        # Set path
        filepath = self.directory / subdirectory

        # Check cache and return if available
        if filepath.exists():
            return dd.read_parquet(filepath)

        # Run function
        df = function(*args, **kwargs)

        # Cache result
        df.to_parquet(filepath, **self.parameters)

        # Return result
        return df

    @property
    def directory(self) -> Path:
        return self._directory

    @directory.setter
    def directory(self, directory) -> None:
        self._directory = Path(directory).resolve().expanduser()

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, parameters) -> None:
        self._parameters = parameters
    
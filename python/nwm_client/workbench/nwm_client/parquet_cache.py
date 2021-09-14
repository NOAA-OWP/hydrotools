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
    def __init__(self, directory: Union[str, Path], *args, **kwargs) -> None:
        """
        Interface for caching dask.dataframe.DataFrame resulting from long
        processes.

        Parameters
        ----------
        directory: str or pathlib.Path, required
            Path to parquet cache root directory.
        *args
            Additional arguments passed to dask.dataframe.DataFrame.to_parquet
        **kwargs
            Additional arguments passed to dask.dataframe.DataFrame.to_parquet
        """
        self.directory = directory
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def __del__(self):
        pass

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
        object
            Retrieve object from file.
        """
        # Set path
        filepath = self.directory / subdirectory

        # Check cache and return if available
        if filepath.exists():
            return dd.read_parquet(filepath)

        # Run function
        df = function(*args, **kwargs)

        # Cache result
        df.to_parquet(filepath, write_index=False, compression="snappy")

        # Return result
        return df

    @property
    def directory(self) -> Path:
        return self._directory

    @directory.setter
    def directory(self, directory) -> None:
        self._directory = Path(directory).resolve().expanduser()
    
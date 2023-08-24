"""
==============================
Parquet-backed DataFrame Store
==============================
Store dask dataframes using a key-value interface.

Classes
---------
 - ParquetStore

"""

import dask.dataframe as dd
from typing import Union, Iterator
from pathlib import Path
from collections.abc import MutableMapping

class ParquetStore(MutableMapping):
    def __init__(self, root: Union[str, Path], **kwargs) -> None:
        """
        Interface for storing dask.dataframe.DataFrame.

        Parameters
        ----------
        root: str or pathlib.Path, required
            Path to parquet store root directory.
        **kwargs
            Additional arguments passed to dask.dataframe.DataFrame.to_parquet

        Notes
        -----
        ParquetStore is really a collection of conveniene methods for common 
        data access patterns wrapped around a parquet file. This module 
        was not specifically designed for parallel workflows and should not 
        be considered thread-safe. For more complicated file-io patterns 
        see the dask.dataframe.DataFrame documentation.

        Examples
        --------
        >>> import pandas as pd
        >>> import dask.dataframe as dd
        >>> from time import sleep
        >>> from hydrotools.nwm_client_new.ParquetStore import ParquetStore
        >>> def my_long_running_process(data: dict) -> dd.DataFrame:
        >>>     # Some long running process
        >>>     sleep(0.2)
        >>>     return dd.from_pandas(pd.DataFrame(data), npartitions=1)
        >>> # Use context manager to setup store
        >>> with ParquetStore(
        >>>     "my_store.parquet",
        >>>     write_index=False,
        >>>     compression="snappy"
        >>>     ) as store:
        >>>     # Fabricate some data to feed the function
        >>>     my_data = {"A": [1, 2, 3]}
        >>>     # Check store before running process
        >>>     if "my_dataframe" in store:
        >>>         df = store["my_dataframe"]
        >>>     else:
        >>>         df = my_long_running_process(my_data)
        >>>         store["my_dataframe"] = df
        """
        super().__init__()
        self.root = root
        self.parameters = kwargs
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def __del__(self):
        pass

    def __str__(self) -> str:
        # Return root directory string
        return str(self.root)
    
    def __bool__(self) -> bool:
        return bool(str(self))
        
    def __getitem__(self, subdirectory: str) -> dd.DataFrame:
        # Set path
        filepath = self.root / subdirectory

        # Check filepath and return dataframe if available
        if filepath.exists():
            return dd.read_parquet(filepath)

        # Raise if filepath does not exist
        raise KeyError(f"{subdirectory}")

    def __setitem__(self, subdirectory: str, df: dd.DataFrame) -> None:
        # Set path
        filepath = self.root / subdirectory

        # Save dataframe
        df.to_parquet(filepath, **self.parameters)

    def __delitem__(self, subdirectory: str) -> None:
        # Set path
        filepath = self.root / subdirectory

        # Delete partitions and filepath
        if filepath.exists():
            for f in filepath.glob("*"):
                f.unlink()
            filepath.rmdir()

    def __iter__(self) -> Iterator[str]:
        # Iterator of subdirectory names
        return iter([f.name for f in self.root.glob("*")])

    def __len__(self) -> int:
        # Number of subdirectories under root
        return len([f for f in self.root.glob("*")])

    def append(self, subdirectory: str, df: dd.DataFrame) -> None:
        """Append data to a parquet file.

        Parameters
        ----------
        subdirectory: str, required
            Key-path under ParquetStore.root where existing dataframe is stored.
        df: dask.dataframe.DataFrame, required
            Data to append.

        Returns
        -------
        None
        
        """
        # Set path
        filepath = self.root / subdirectory

        # Save dataframe
        df.to_parquet(filepath, append=True, **self.parameters)

    @property
    def root(self) -> Path:
        return self._directory

    @root.setter
    def root(self, root) -> None:
        self._directory = Path(root).resolve().expanduser()

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, parameters) -> None:
        self._parameters = parameters
    
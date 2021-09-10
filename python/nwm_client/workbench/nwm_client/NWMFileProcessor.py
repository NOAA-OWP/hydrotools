"""
==================
NWM File Processor
==================
Tools for processing NWM data in NetCDF format.

Classes
-------
NWMFileProcessor
"""
from pathlib import Path
import xarray as xr
import dask.dataframe as dd
import pandas as pd
from typing import List, Union

class NWMFileProcessor:

    @classmethod
    def get_dataset(
        cls,
        input_directory: Union[str, Path],
        variables: List[str] = ["reference_time", "time", "streamflow"]
        ) -> xr.Dataset:
        """Generate an xarray.Dataset from an input directory of NWM .nc files.

        Parameters
        ----------
        input_directory: str, pathlib.Path, required
            Directory containing collection of National Water Model NetCDF 
            files.
        variables: list of str, optional, default ["reference_time", "time",
             "streamflow"]
             List of variables to retrieve from source files. Options include: 
             'time', 'reference_time', 'feature_id', 'crs', 'streamflow', 
             'nudge', 'velocity', 'qSfcLatRunoff', 'qBucket', 'qBtmVertRunoff'

        Returns
        -------
        xarray.Dataset of input_directory lazily loaded.
        """
        # Resolve input directory
        idir = Path(input_directory).expanduser().resolve()

        # Generate file list
        file_list = [f for f in idir.glob("*.nc")]

        # Return dataset
        return xr.open_mfdataset(file_list)[variables]

    @classmethod
    def get_dask_dataframe(
        cls,
        input_directory: Union[str, Path],
        variables: List[str] = ["reference_time", "time", "streamflow"]
        ) -> dd.DataFrame:
        """Generate a dask.dataframe.DataFrame from an input directory of NWM 
        .nc files.

        Parameters
        ----------
        input_directory: str, pathlib.Path, required
            Directory containing collection of National Water Model NetCDF 
            files.
        variables: list of str, optional, default ["reference_time", "time",
             "streamflow"]
             List of variables to retrieve from source files. Options include: 
             'time', 'reference_time', 'feature_id', 'crs', 'streamflow', 
             'nudge', 'velocity', 'qSfcLatRunoff', 'qBucket', 'qBtmVertRunoff'

        Returns
        -------
        dask.dataframe.DataFrame of input_directory
        """
        # Retrieve dataset
        with cls.get_dataset(input_directory, variables) as ds:
            # Convert to dask dataframe
            df = ds.to_dask_dataframe()

            # Add and categorize configuration column
            df["configuration"] = ds.attrs["model_configuration"]
            df["configuration"] = df["configuration"].astype("category")

            # Downcast floats
            float_columns = df.select_dtypes(include=["float"])
            for col in float_columns:
                df[col] = pd.to_numeric(df[col], downcast="float")

            # Return dataframe
            return df

    @classmethod
    def get_dataframe(
        cls,
        input_directory: Union[str, Path],
        variables: List[str] = ["reference_time", "time", "streamflow"]
        ) -> pd.DataFrame:
        """Generate a pandas.DataFrame from an input directory of NWM .nc files.

        Parameters
        ----------
        input_directory: str, pathlib.Path, required
            Directory containing collection of National Water Model NetCDF 
            files.
        variables: list of str, optional, default ["reference_time", "time",
             "streamflow"]
             List of variables to retrieve from source files. Options include: 
             'time', 'reference_time', 'feature_id', 'crs', 'streamflow', 
             'nudge', 'velocity', 'qSfcLatRunoff', 'qBucket', 'qBtmVertRunoff'

        Returns
        -------
        pandas.DataFrame of input_directory data
        """
        # Retrieve dask dataframe, compute pandas dataframe, and return
        return cls.get_dask_dataframe(input_directory, variables).compute()

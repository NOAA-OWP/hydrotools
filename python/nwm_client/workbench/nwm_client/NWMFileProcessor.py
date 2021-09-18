"""
==================
NWM File Processor
==================
Tools for processing NWM data in NetCDF (.nc) format.

Classes
-------
NWMFileProcessor
"""
from pathlib import Path
import xarray as xr
import dask.dataframe as dd
import pandas as pd
import numpy as np
import numpy.typing as npt
from typing import List, Union

class NWMFileProcessor:
    """Provides an interface for methods used to process National Water Model 
    data from NetCDF (.nc) format to xarray.Dataset, dask.dataframe.Dataframe, 
    or pandas.DataFrame.
    """

    @classmethod
    def get_dataset(
        cls,
        input_directory: Union[str, Path],
        feature_id_filter: npt.ArrayLike = [],
        variables: List[str] = ["reference_time", "time", "streamflow"]
        ) -> xr.Dataset:
        """Generate an xarray.Dataset from an input directory of NWM .nc files.

        Parameters
        ----------
        input_directory: str, pathlib.Path, required
            Directory containing collection of National Water Model NetCDF 
            files.
        feature_id_filter: array-like, optional, default []
            Subset of feature IDs to return.
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
        input_directory = Path(input_directory)

        # Generate file list
        file_list = [f for f in input_directory.glob("*.nc")]

        # Open dataset
        ds = xr.open_mfdataset(file_list)

        # Prepare feature_id filter
        if len(feature_id_filter) != 0:
            # Convert to array
            feature_id_filter = np.asarray(feature_id_filter)

            # Validate filter IDs
            check = np.isin(feature_id_filter, ds.feature_id)

            # Subset by feature ID and variable
            return ds.sel(feature_id=feature_id_filter[check])[variables]

        # Subset by variable only
        return ds[variables]

    @classmethod
    def convert_to_dask_dataframe(
        cls,
        ds: xr.Dataset
        ) -> dd.DataFrame:
        """Generate a dask.dataframe.DataFrame from an xarray.Dataset.

        Parameters
        ----------
        ds: xarray.Dataset, required
            xarray.Dataset containing National Water Model data.

        Returns
        -------
        dask.dataframe.DataFrame of NWM data.
        """
        # Convert to dask dataframe
        df = ds.to_dask_dataframe()

        # Compute number of partitions
        #  Best practice is ~100 MB per partition
        #  TODO Make this a parameter
        npartitions = 1 + len(df.index) // 2_400_000

        # Sort by feature ID
        #  Most applications will benefit from this
        df = df.sort_values(by="feature_id")

        # Reset index
        df = df.set_index("feature_id").reset_index()

        # Repartition
        return df.repartition(npartitions=npartitions)

    @classmethod
    def convert_to_dataframe(
        cls,
        ds: xr.Dataset
        ) -> pd.DataFrame:
        """Generate a pandas.DataFrame from an xarray.Dataset.

        Parameters
        ----------
        ds: xarray.Dataset, required
            xarray.Dataset containing National Water Model data.

        Returns
        -------
        pandas.DataFrame of NWM data.
        """
        # Compute pandas dataframe
        return cls.convert_to_dask_dataframe(ds).compute()

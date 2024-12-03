"""
==================
NWM File Processor
==================
Tools for processing NWM data in NetCDF (.nc) format.

Classes
-------
NWMFileProcessor
"""

import xarray as xr
import dask.dataframe as dd
import pandas as pd
import numpy as np
import numpy.typing as npt
from typing import List, Union
import warnings
from .NWMClientDefaults import _NWMClientDefault

class NWMFileProcessor:
    """Provides a concrete interface for methods used to process National Water 
    Model data from NetCDF (.nc) format to xarray.Dataset, 
    dask.dataframe.Dataframe, or pandas.DataFrame.
    """

    @classmethod
    def get_dataset(
        cls,
        paths: Union[str, npt.ArrayLike],
        feature_id_filter: npt.ArrayLike = _NWMClientDefault.CROSSWALK.index,
        variables: List[str] = _NWMClientDefault.VARIABLES
        ) -> xr.Dataset:
        """Generate an xarray.Dataset from an input directory of NWM .nc files.

        Parameters
        ----------
        paths: str or array-like of paths, required
            Glob string or array-like of paths passed directly to xarray.open_mfdataset
        feature_id_filter: array-like, optional
            Subset of feature IDs to return. Defaults to USGS assimilation locations.
        variables: list of str, optional, default ["streamflow"]
             List of variables to retrieve from source files. Options include: 
             'streamflow', 'nudge', 'velocity', 'qSfcLatRunoff', 'qBucket', 'qBtmVertRunoff'
             
        Returns
        -------
        xarray.Dataset of paths lazily loaded.
        """
        # Minimum coordinates
        coordinates = []
        for c in ["feature_id", "time", "reference_time"]:
            if c not in variables:
                coordinates.append(c)

        # Open dataset
        ds = xr.open_mfdataset(paths, engine="netcdf4")

        # Prepare feature_id filter
        if len(feature_id_filter) != 0:
            # Convert to integer array
            feature_id_filter = np.asarray(feature_id_filter, dtype=int)

            # Subset by feature ID and variable
            try:
                return ds.sel(feature_id=feature_id_filter)[coordinates+variables]
            except KeyError:
                # Validate filter IDs
                check = np.isin(feature_id_filter, ds.feature_id)

                # Note invalid feature IDs
                missing = feature_id_filter[~check]

                # Warn
                message = f"These filter IDs were not in the index: {missing}"
                warnings.warn(message)

                # Subset by valid feature ID and variable
                return ds.sel(feature_id=feature_id_filter[check])[coordinates+variables]

        # Subset by variable only
        return ds[coordinates+variables]

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

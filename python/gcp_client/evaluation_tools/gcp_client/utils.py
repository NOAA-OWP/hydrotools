#!/usr/bin/env python3
"""
================================
Google Cloud Platform NWM Client
================================
This module provides methods for handling common model parameter files that can be
used in part with the other portions of this subpackage. One pragmatic use of this
module is to extract nhdPlus links associated with usgs sites to filter stations of
interest.
"""

import pandas as pd
import xarray as xr
from pathlib import Path
from typing import Union


def nwm_routelink_extract_usgs_sites(
    routelink_file_or_url: Union[
        str,
        Path,
    ]
) -> pd.DataFrame:
    """From a NWM routelink file, extract nwm_feature_id's that have associated USGS
    NWIS Stations, returning a df with cols `nwm_feature_id` and `usgs_site_code`.

    Routelink files can be obtained from nomads production server:
    https://www.nco.ncep.noaa.gov/pmb/codes/nwprod/

    Under ./nwm.v*/parm/domain/RouteLink*.nc

    Parameters
    ----------
    routelink_file_or_url : Union[ str, Path, ]
        NWM Routelink file containing channel parameters

    Returns
    -------
    pd.DataFrame
        Dataframe with cols `nwm_feature_id` and `usgs_site_code`

    Examples
    --------
    >>> from evaluation_tools.gcp_client import utils
    >>> df = utils.nwm_routelink_extract_usgs_sites("RouteLink_NHDPLUS.nc")
    >>> import csv
    >>> df.to_csv("nwm_feature_id_with_usgs_site.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

    """
    # open dataset
    ds = xr.open_dataset(routelink_file_or_url, mask_and_scale=False, engine="h5netcdf")

    df = pd.DataFrame(
        {
            "nwm_feature_id": ds.gages.feature_id.values,
            "usgs_site_code": ds.gages.values,
        }
    )

    # remove ds from mem
    del ds

    # decode bytes to string and strip whitespaces
    df.loc[:, "usgs_site_code"] = df["usgs_site_code"].str.decode("utf-8").str.strip()

    # return rows that have an associated gage
    return df[df["usgs_site_code"].str.len() > 0].reset_index(drop=True)
#!/usr/bin/env python3
"""
===================================
National Water Model File Utilities
===================================
This module provides methods for handling common model parameter files that can be
used in part with the other portions of this subpackage. One pragmatic use of this
module is to extract nhdPlus links associated with usgs sites to filter stations of
interest.
"""

import pandas as pd
import xarray as xr
import six
from pathlib import Path
from typing import Union, List


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
    >>> from hydrotools.nwm_client import utils
    >>> df = utils.nwm_routelink_extract_usgs_sites("RouteLink_NHDPLUS.nc")
    >>> import csv
    >>> df.to_csv("nwm_feature_id_with_usgs_site.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

    """
    # open dataset
    ds = xr.open_dataset(routelink_file_or_url, mask_and_scale=False, engine="h5netcdf")

    df = pd.DataFrame(
        {
            "nwm_feature_id": ds.link.values,
            "usgs_site_code": ds.gages.values,
        }
    )

    # remove ds from mem
    del ds

    # decode bytes to string and strip whitespaces
    df.loc[:, "usgs_site_code"] = df["usgs_site_code"].str.decode("utf-8").str.strip()

    # return rows that have an associated gage
    return df[df["usgs_site_code"].str.len() > 0].reset_index(drop=True)


def crosswalk(
    usgs_site_codes: Union[str, List[str]] = None,
    nwm_feature_ids: Union[str, List[str]] = None,
) -> pd.DataFrame:
    """Return the nwm_feature_id(s) OR usgs_site_codes for one or more provided
    usgs_sites_codes or nwm_feature_ids.

    Parameters
    ----------
    usgs_site_codes : Union[str, List[str]], either usgs_site_codes or nwm_feature_ids
        USGS site code as string, string seperated by commas, or list of strings
    nwm_feature_ids : Union[str, List[str]], either usgs_site_codes or nwm_feature_ids
        NWM feature id(s) as string, string seperated by commas, or list of strings

    Returns
    -------
    pd.DataFrame
        df of `nwm_feature_id` and `usgs_site_code` cols

    Examples
    --------
    >>> from hydrotool.nwm_client import utils
    >>> cribbs_creek = "02465292"
    >>> crx_walk = utils.crosswalk(usgs_site_codes=cribbs_creek)

    >>> sites = ["02465292", "04234000"]
    >>> crx_walk = utils.crosswalk(usgs_site_codes=sites)

    >>> sites = "02465292,04234000"
    >>> crx_walk = utils.crosswalk(usgs_site_codes=sites)

    >>> nwm_feature = 18206880
    >>> crx_walk = utils.crosswalk(nwm_feature_ids=nwm_feature)
    """

    # Handle keyword args. XNOR is invalid
    if (not usgs_site_codes and not nwm_feature_ids) or (
        usgs_site_codes and nwm_feature_ids
    ):
        error_message = (
            "Cannot pass both `usgs_site_codes` and `nwm_feature_ids` parameters."
        )
        raise TypeError(error_message)

    if usgs_site_codes:
        crosswalk_var = "usgs_site_code"
        crosswalk_values = usgs_site_codes

    else:
        crosswalk_var = "nwm_feature_id"
        crosswalk_values = nwm_feature_ids

    # Path to crosswalk file
    crosswalk_file = (
        Path(__file__).resolve().parent / "data/RouteLink_NWMv2.0.csv"
    )

    # Read crosswalk file in as df, ensure its the right data types
    crosswalk_df = pd.read_csv(
        crosswalk_file,
        dtype={"nwm_feature_id": int, "usgs_site_code": str},
        comment='#'
    )[['nwm_feature_id', 'usgs_site_code']]

    # If passed site codes are singular or in string form convert to list
    if isinstance(crosswalk_values, six.string_types):
        crosswalk_values = crosswalk_values.split(",")
    
    # Return df of nwm_feature_ids and matching usgs_site_codes
    return crosswalk_df[crosswalk_df[crosswalk_var].isin(crosswalk_values)]

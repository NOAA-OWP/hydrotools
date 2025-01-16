"""
====================
Baseflow :: Eckhardt
====================
Methods to support hydrograph baseflow separation using digital recursive
filters.

Collischonn, W., & Fan, F. M. (2013). Defining parameters for Eckhardt's
    digital baseflow filter: DEFINING PARAMETERS FOR ECKHARDT'S DIGITAL
    BASEFLOW FILTER. Hydrological Processes, 27(18), 2614-2622.
    https://doi.org/10.1002/hyp.9391
Eckhardt, K. (2005). How to construct recursive digital filters for baseflow
    separation. Hydrological Processes, 19(2), 507-515.
    https://doi.org/10.1002/hyp.5675
Eckhardt, K. (2008). A comparison of baseflow indices, which were calculated
    with seven different baseflow separation methods. Journal of Hydrology,
    352(1-2), 168-173. https://doi.org/10.1016/j.jhydrol.2008.01.005

Functions
---------
linear_recession_analysis
maximum_baseflow_analysis
apply_filter
separate_baseflow

"""

from dataclasses import dataclass
import datetime
from typing import Union
import numpy as np
import numpy.lib as npl
import numpy.typing as npt
from numba import jit, float64
import pandas as pd

@dataclass
class BaseflowData:
    """DataClass containing a pandas.Series of baseflow values with
        a DateTimeIndex and associated filter parameter values.
    
        Parameters
        ----------
        values: pandas.Series
            A pandas.Series of baseflow values with a DateTimeIndex.
        recession_constant: float
            Linear reservoir recession constant, a, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.85 and 0.95 for daily streamflow.
        maximum_baseflow_index: float
            The maximum baseflow index, $BFI_{max}$, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.25 and 0.8 for daily streamflow.
    """
    values: pd.Series
    recession_constant: float
    maximum_baseflow_index: float

def linear_recession_analysis(
        series: npt.ArrayLike,
        window: int = 5
    ) -> float:
    """Performs recession analysis on series assuming a linear reservoir.
    
        Parameters
        ----------
        series: array-like, required
            An array of streamflow values.
        window: int, optional, default 5
            The minimum number of consecutively decreasing values in series
            that indicate a period of recession.
            
        Returns
        -------
        recession_constant: float
            The recession parameter, a, from Eckhardt (2005, 2008).
    """
    # Find decreases in streamflow from time step to the next
    # Note first decrease is a[i+1] - a[i]
    decreases = np.diff(series) < 0.0

    # Inspect overlapping windows to identify recession periods
    # Periods where all values decreased are "recessions"
    periods = npl.stride_tricks.sliding_window_view(
        decreases,
        window_shape=window
        )
    recessions = np.all(periods, axis=1)

    # Determine index of recession period central values
    # Note: Increase index by one because np.diff caused a shift
    indices = np.where(recessions)[0] + window // 2 + 1

    # Select recession values
    x = series[indices-1]
    y = series[indices]

    # Compute recession constant using regression through the origin
    return np.sum(x * y) / np.sum(x * x)

@jit(float64(float64[:], float64), nogil=True)
def maximum_baseflow_analysis(
        series: npt.NDArray,
        recession_constant: float
    ) -> float:
    """Applies reverse filtering to estimate the maximum baseflow index
        (Collischonn & Fan, 2013).
    
        Parameters
        ----------
        series: array-like, required
            A numpy array of streamflow values. Assumes last value in series is baseflow.
        recession_constant: float, required
            Linear reservoir recession constant, a, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.85 and 0.95 for daily streamflow.
            
        Returns
        -------
        maximum_baseflow_index: float
            The maximum baseflow index, $BFI_{max}$, from Eckhardt (2005, 2008).
    """
    # Instantiate maximum baseflow series
    # Assume last value is baseflow
    baseflow = np.empty(series.size)
    baseflow[0] = series[-1]

    # Apply reverse filter and compute
    #   maximum baseflow index
    flipped = series[::-1]
    for i in range(1, series.size):
        baseflow[i] = min(flipped[i], baseflow[i-1] / recession_constant)
    return np.sum(baseflow) / np.sum(series)

@jit(float64[:](float64[:], float64, float64), nogil=True)
def apply_filter(
        series: npt.NDArray,
        recession_constant: float,
        maximum_baseflow_index: float
) -> npt.NDArray:
    """Applies a digitial recursive baseflow separation filter to series
        and returns the result.
    
        Parameters
        ----------
        series: array-type, required
            A numpy array of streamflow values. Assumes first value in series is baseflow.
        recession_constant: float, required
            Linear reservoir recession constant, a, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.85 and 0.95 for daily streamflow.
        maximum_baseflow_index: float
            The maximum baseflow index, $BFI_{max}$, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.25 and 0.8 for daily streamflow.
            
        Returns
        -------
        baseflow: array-type
            An array containing the separated baseflow values.
    """
    # Compute filter parameters
    denominator = 1 - recession_constant * maximum_baseflow_index
    A = (1.0 - maximum_baseflow_index) * recession_constant / denominator
    B = (1.0 - recession_constant) * maximum_baseflow_index / denominator

    # Instantiate baseflow series
    # Assume first value is baseflow
    baseflow = np.empty(series.size)
    baseflow[0] = series[0]

    # Apply filter and return result
    for i in range(1, series.size):
        baseflow[i] = min(series[i], A * baseflow[i-1] + B * series[i])
    return baseflow

def separate_baseflow(
        series: pd.Series,
        output_time_scale: Union[pd.Timedelta, datetime.timedelta, np.timedelta64, str, int],
        recession_time_scale: Union[pd.Timedelta, datetime.timedelta, np.timedelta64, str, int] = "1D",
        recession_window: int = 5
) -> BaseflowData:
    """Applies a digitial recursive baseflow separation filter to series
        and returns the result. This is a higher level method than `apply_filter`
        that includes time resampling and filter parameter estimation.
    
        Parameters
        ----------
        series: pandas.Series, required
            A pandas.Series of streamflow values with a DateTimeIndex. Assumes
            first value in series is baseflow.
        output_time_scale: pandas.Timedelta, datetime.timedelta, numpy.timedelta64, str, int, required
            Output time-scale (or 'time-step') of the output baseflow time series.
        recession_time_scale: pandas.Timedelta, datetime.timedelta, numpy.timedelta64, str, int, optional, default '1D'
            Time-scale or 'time-step' over which to conduct recession analysis.
        recession_window: int, optional, default 5
            The minimum number of consecutively decreasing values in series
            that indicate a period of recession.

        Returns
        -------
        baseflow_data: BaseflowData
            A BaseflowData DataClass containing the separated baseflow and associated filter parameters.
    """
    # Compute recession constant
    recession_series = series.resample(recession_time_scale).nearest(limit=1)
    a = linear_recession_analysis(
        recession_series.values,
        recession_window
        )

    # Convert recession constant to output time-scale
    no_output_periods = pd.Timedelta(recession_time_scale) / pd.Timedelta(output_time_scale)
    a = 1.0 - ((1.0 - a) / no_output_periods)

    # Compute maximum baseflow index
    baseflow_series = series.resample(output_time_scale).nearest(limit=1)
    bfi_max = maximum_baseflow_analysis(
        baseflow_series.values,
        a
    )

    # Perform baseflow separation
    return BaseflowData(
        pd.Series(
            apply_filter(
            baseflow_series.values,
            a,
            bfi_max
        ),
        baseflow_series.index
    ),
    a, bfi_max)

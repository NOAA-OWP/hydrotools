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

from typing import Callable
from dataclasses import dataclass
import datetime
import numpy as np
import numpy.lib as npl
import numpy.typing as npt
from numba import jit, float64
import pandas as pd

class ConvergenceError(Exception):
    """Exception raised when iterative numerical process fails
    to converge on a solution."""

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
            Influenced by basin size, precipitation frequency, and other catchment
            characteristics.
        maximum_baseflow_index: float
            The maximum baseflow index, $BFI_{max}$, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.25 and 0.8 for daily streamflow.
            Influenced by aquifer porosity, streamflow frequency, and other catchment
            characteristics.
    """
    values: pd.Series
    recession_constant: float
    maximum_baseflow_index: float

def linear_recession_analysis(
        series: npt.NDArray,
        window: int = 5,
        maximum_relative_error: float = 0.02,
        maximum_iterations: int = 100
    ) -> float:
    """Performs recession analysis on series assuming a linear reservoir. Using
        the method from Eckhardt (2008).

        Parameters
        ----------
        series: array-type, required
            A numpy array of streamflow values.
        window: int, optional, default 5
            The minimum number of consecutively decreasing values in series
            that indicate a period of recession.
        maximum_relative_error: float, optional, default 0.02
            The maximum allowable error in the recession constant due to
            random observational errors. Defaults to 0.02 (2.0 %).
        maximum_iterations: int, optional, default 100
            Maximum number of times to remove outliers and recompute.

        Returns
        -------
        recession_constant: float
            Linear reservoir recession constant, a, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.85 and 0.95 for daily streamflow.
            Influenced by basin size, precipitation frequency, and other catchment
            characteristics.
    """
    # Check size of series
    assert series.size > 0, "empty input series"

    # Find decreases in streamflow
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
    # Note: Increase index by one because np.diff
    #   dropped the original first value
    indices = np.where(recessions)[0] + window // 2 + 1

    # Select central recession values and
    #   preceding values
    x = series[indices-1]
    y = series[indices]

    for _ in range(maximum_iterations):
        # Check for values
        if (x.size == 0) or (y.size == 0):
            message = "Not enough values to estimate recession constant."
            raise ConvergenceError(message)

        # Compute recession constant using regression through the origin
        ideal_value = np.sum(x * y) / np.sum(x * x)

        # Test empirical values
        empirical_values = y / x

        # Compute deviation from ideal value
        errors = (empirical_values - ideal_value) / ideal_value

        # Note outliers, if none, return ideal value
        outliers = errors[errors > maximum_relative_error]
        if outliers.size == 0:
            return ideal_value

        # Remove outliers and recompute
        x = x[errors <= maximum_relative_error]
        y = y[errors <= maximum_relative_error]

    # Did not converge
    message = f"Recession analysis failed to converge in {maximum_iterations} iterations."
    raise ConvergenceError(message)

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
            Influenced by basin size, precipitation frequency, and other catchment
            characteristics.
            
        Returns
        -------
        maximum_baseflow_index: float
            The maximum baseflow index, $BFI_{max}$, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.25 and 0.8 for daily streamflow.
            Influenced by aquifer porosity, streamflow frequency, and other catchment
            characteristics.
    """
    # Check size of series
    assert series.size > 0, "empty input series"

    # Instantiate maximum baseflow series
    # Assume last value is baseflow
    total_baseflow = series[-1]
    current_baseflow = series[-1]

    # Apply reverse filter and compute
    #   maximum baseflow index
    flipped = series[::-1]
    for i in range(1, series.size):
        current_baseflow = min(flipped[i], current_baseflow / recession_constant)
        total_baseflow += current_baseflow
    return total_baseflow / np.sum(series)

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
            Influenced by basin size, precipitation frequency, and other catchment
            characteristics.
        maximum_baseflow_index: float
            The maximum baseflow index, $BFI_{max}$, from Eckhardt (2005, 2008). Must be
            between 0.0 and 1.0, typically between 0.25 and 0.8 for daily streamflow.
            Influenced by aquifer porosity, streamflow frequency, and other catchment
            characteristics.
            
        Returns
        -------
        baseflow: array-type
            An array containing the separated baseflow values.
    """
    # Check size of series
    assert series.size > 0, "empty input series"

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
        output_time_scale: pd.Timedelta | datetime.timedelta | np.timedelta64 | str | int,
        recession_time_scale: pd.Timedelta | datetime.timedelta | np.timedelta64 | str | int = "1D",
        aggregation_function: str | Callable = "mean",
        recession_window: int = 5
) -> BaseflowData:
    """Applies a digitial recursive baseflow separation filter to series
        and returns the result. This is a higher level method than `apply_filter`
        that includes time resampling and filter parameter estimation.
    
        Parameters
        ----------
        series: pandas.Series, required
            A pandas.Series of streamflow values with a DateTimeIndex. Assumes
            first and last values in series are baseflow.
        output_time_scale: pandas.Timedelta, datetime.timedelta, numpy.timedelta64, str, int, required
            Output time-scale (or 'time-step') of the output baseflow time series.
            Typically the same time-scale as series.
        recession_time_scale: pandas.Timedelta, datetime.timedelta, numpy.timedelta64, str, int, optional, default '1D'
            Time-scale or 'time-step' over which to conduct recession analysis.
            Generally, it's better to use a recession_time_scale greater than the series time-scale.
            The default of '1D' is good for many catchments, but smaller catchments can benefit from a
            shorter time-scale of '18h' or '12h'.
        aggregation_function: str or Callable, optional, default 'mean'
            The aggregation function to use when resampling series to the desired time-scale. Defaults
            to 'mean' per Eckhardt 2008, which used mean daily volumetric streamflow. Generally, volumetric
            streamflow (i.e. L^3/S) will want to use 'mean'. Discharge per unit area (i.e. L) will want to use
            'sum'. Some other cases of "instantaneous values" or unit flux (i.e. L/S) may more appropriately use 'first'.
        recession_window: int, optional, default 5
            The minimum number of consecutively decreasing values in series
            that indicate a period of recession.

        Returns
        -------
        baseflow_data: BaseflowData
            A BaseflowData DataClass containing the separated baseflow and associated filter parameters.
    """
    # Check size of series
    assert series.size > 0, "empty input series"

    # Compute recession constant
    recession_series = series.resample(recession_time_scale).agg(aggregation_function)
    a = linear_recession_analysis(
        recession_series.values.astype(np.float64),
        recession_window
        )

    # Convert recession constant to output time-scale
    no_output_periods = pd.Timedelta(recession_time_scale) / pd.Timedelta(output_time_scale)
    a = 1.0 - ((1.0 - a) / no_output_periods)

    # Compute maximum baseflow index
    baseflow_series = series.resample(output_time_scale).nearest(limit=1)
    baseflow_array = baseflow_series.values.astype(np.float64)
    bfi_max = maximum_baseflow_analysis(
        baseflow_array,
        a
    )

    # Perform baseflow separation
    return BaseflowData(
        pd.Series(
            apply_filter(
            baseflow_array,
            a,
            bfi_max
        ),
        baseflow_series.index
    ),
    a, bfi_max)

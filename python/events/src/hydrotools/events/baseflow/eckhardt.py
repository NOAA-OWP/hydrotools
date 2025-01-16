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

"""

import numpy as np
import numpy.typing as npt
from numba import jit, float64

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
    return 0.9

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
            Linear reservoir recession constant.
            
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
def separate_baseflow(
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
            Linear reservoir recession constant, a, from Eckhardt (2005, 2008).
        maximum_baseflow_index: float
            The maximum baseflow index, $BFI_{max}$, from Eckhardt (2005, 2008).
            
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

"""
===================
Event-based Metrics
===================
Methods for computing common event-based metrics. For purposes of model
evaluation, these metrics are often used in combination with a method that
computes the model error in terms of these metrics. A classic example is peak
bias or the difference in a modeled peak and an observed peak. There are many
ways to express this bias including relative error, mean squared error, root
mean squared error, absolute error, and others.
    This module focuses specifically on metrics used to characterize
event-scale processes. These methods are intended for use on subsets of
singular time series. Applying these methods to model evaluation requires the
use of an "event detection" method. See the documentation for some examples of
how to implement this process.

References
----------
Baker, D. B., Richards, R. P., Loftus, T. T., & Kramer, J. W. (2004). A NEW
    FLASHINESS INDEX: CHARACTERISTICS AND APPLICATIONS TO MIDWESTERN RIVERS AND
    STREAMS. Journal of the American Water Resources Association, 40(2),
    503-522. https://doi.org/10.1111/j.1752-1688.2004.tb01046.x

Functions
---------
 - flashiness
 - peak
 - runoff_ratio
"""

import warnings
import numpy as np
import numpy.typing as npt

def flashiness(series: npt.ArrayLike) -> float:
    """
    Compute Reynolds-Baker Flashiness Index (Baker et al., 2004). The
    flashiness index quantifies the "frequency and rapidity of short-term
    changes in streamflow." This characteristic is one way to describe the
    "flow regime" of a stream. Higher flashiness indices indicate more "flashy"
    streams. Note: that flashiness is sensitive to catchment area. Comparisons
    of flashiness across catchments of differnt area should be approached with
    caution.
        This implementaion uses the central difference formula found in
    Equation 3 of Baker et al., 2004. Gradients for edge values use a 1-D
    approximation. See numpy.gradient for more details.

    Parameters
    ----------
    series: array-like, required
        An array of numerical values over which to compute flashiness.

    Returns
    -------
    Reynolds-Baker Flashiness Index as a float.
    """
    # Validate
    assert len(series) > 0, "cannot compute flashiness for empty series"

    return np.sum(np.abs(np.gradient(series))) / np.sum(series)

def peak(series: npt.ArrayLike, **options) -> float:
    """
    Compute the maximum of an array.
    
    This is an alias for numpy.max

    Parameters
    ----------
    series: array-like, required
        An array of numerical values over which to compute peak.
    options: optional
        Additional keyword arguments passed directly to numpy.max.
    
    Returns
    -------
    Maximum value in series.
    """
    # Validate
    assert len(series) > 0, "cannot compute peak for empty series"

    return np.max(series, **options)

def runoff_ratio(
        runoff: npt.ArrayLike,
        precipitation: npt.ArrayLike,
        runoff_scale_factor: float = 1.0,
        precipitation_scale_factor: float = 1.0
        ) -> float:
    """
    Compute runoff ratio, also called runoff efficiency or runoff
    coefficient. This the ratio of runoff to precipitation. Typically, "direct
    runoff" is used which is total runoff minus baseflow. Precipitation is
    typically "effective precipitation" which is precipitation minus losses
    due to canopy interception (i.e. precipitation that hits the ground).
        This method assumes that runoff and precipitation are in the same
    units. Often units are in accumulated depth per unit area of 
    catchment over some time interval (e.g. cm, mm, inch, etc.).

    Parameters
    ----------
    runoff: array-like, required
        Array of streamflow values.
    precipitation: array-like, required
        Array of precipitation values.
    runoff_scale_factor: float, optional, default 1.0
        Multiplicative factor used to rescale runoff prior to computing the
        runoff ratio. Use this to ensure that runoff and precipitation are in
        the same measurement units. For example, to convert runoff from cubic
        feet per second to accumulated inches per hour, use a scale factor
        of 3 / (A * 1936) where A is the catchment area in square miles.
    precipitation_scale_factor: float, optional, default 1.0
        Multiplicative factor used to rescale precipitation prior to computing
        the runoff ratio. Use this to ensure that runoff and precipitation are
        in the same measurement units. This scale factor is rarely used.
    
    Returns
    -------
    runoff ratio as a float.
    """
    # Validate
    assert len(runoff) > 0, "cannot compute ratio for empty runoff series"
    assert len(precipitation) > 0,\
        "cannot compute ratio for empty precipitation series"
    assert np.all(runoff >= 0.0), "runoff cannot be negative"
    assert np.all(precipitation >= 0.0), "precipitation cannot be negative"

    # Compute
    ratio = (np.sum(runoff * runoff_scale_factor) /
            np.sum(precipitation * precipitation_scale_factor))

    # Warn for non-physical values
    if not 0.0 <= ratio <= 1.0:
        message = f"non-physical runoff ratio {ratio}"
        warnings.warn(message, RuntimeWarning)

    return ratio

"""
===================
Flow Duration Curve
===================

Methods for generating and analyzing flow duration curves (FDC) from streamflow 
time series. There are two methods used here to generate FDCs: empirical and
pearson. Generally, the empirical method will be much faster but can result in
choppy or unevenly distributed FDCs. The pearson method fits the data to a
Pearson Type-III distribution and results in a much smoother FDC. However, the
pearson method is much slower. Confidence intervals for both these methods can
be generated using bootstrap_flow_duration_curve.

References
----------
Leon Harter, H. (1984). Another look at plotting positions. Communications in
    Statistics-Theory and Methods, 13(13), 1613-1633.
Richards, R. P. (1990). Measures of flow variability and a new flow-based
    classification of Great Lakes tributaries. Journal of Great Lakes Research,
    16(1), 53-70.
Vogel, R. M., & Fennessey, N. M. (1994). Flow-duration curves. I: New
    interpretation and confidence intervals. Journal of Water Resources
    Planning and Management, 120(4), 485-504.

Classes
-------
FDCGenerator

Functions
---------
 - empirical_flow_duration_curve
 - pearson_flow_duration_curve
 - bootstrap_flow_duration_curve
 - exceedance_values
 - recurrence_values
 - richards_flow_responsiveness
"""

from typing import Protocol
import numpy as np
import numpy.typing as npt
from scipy.stats import pearson3, variation
from arch.bootstrap import optimal_block_length, StationaryBootstrap

class FDCGenerator(Protocol):
    """Protocol class defining an interface for methods that generate flow
    duration curves. An FDCGenerator is a callable that takes an array-like
    as its first argument and additional optional keyword arguments. It returns
    a tuple of length two. The first value in the tuple is a numpy.ndarray that
    contains values corresponding to exceedance probabilities. The second value
    in the tuple contains a numpy.ndarray correponding to sorted values from
    the input array. 
    """
    @staticmethod
    def __call__(
        series: npt.ArrayLike,
        **kwargs) -> tuple[npt.NDArray, npt.NDArray]:
        pass

def empirical_flow_duration_curve(
        series: npt.ArrayLike,
        alpha: float = 0.0,
        beta: float = 0.0
        ) -> tuple[npt.NDArray, npt.NDArray]:
    """
    Derive an empirical flow duration curve (FDC) from an array of streamflow
    values. The series values determine the type of FDC returned. A series of
    daily or hourly streamflow values will result in a "period-of-record" FDC.
    A series of annual maximum flows will result in an annual peak FDC, from
    which you can derive "annual recurrence intervals."

    Parameters
    ----------
    series: array-like, required
        An array of numerical streamflow values used to generate a flow
        duration curve.
    alpha: float, optional, default 0.0
        Plotting position parameter. Used for variations of plotting position
        formula. Affects how probabilities are calculated. Defaults to the
        "Weibull" plotting position formula.
    beta: float, optional, default 0.0
        Plotting position parameter. Used for variations of plotting position
        formula. Affects how probabilities are calculated. Defaults to the
        "Weibull" plotting position formula.
    
    Returns
    -------
    probabilities: numpy.ndarray
        Array of values that represent exceedance probabilities, also called
        exceedance frequencies. The range of possible values is [0.0, 1.0].
        These values usually represent the "x-values" on a flow duration curve
        plot. These values can be converted into recurrence intervals by
        dividing them into 1.0 (i.e. 1.0 / probabilities). Note that these
        recurrence intervals will reflect the sampling frequency of the input
        series (e.g. "hourly", "daily", or "annual" recurrence intervals). This
        array will have the same length as series.
    values: numpy.ndarray
        Array of actual streamflow values in the same units as the input
        series. These values correspond directly to exceedance frequencies in
        probabilities. These values usually represent the "y-values" on a flow
        duration curve plot.
    """
    # Validate
    size = len(series)
    assert size > 0, "series is empty"
    assert 0.0 <= alpha <= 1.0, "alpha must be between [0.0, 1.0]"
    assert 0.0 <= beta <= 1.0, "beta must be between [0.0, 1.0]"

    # Compute
    return (
        (np.arange(size) + 1 - alpha) / (size + 1 - alpha - beta),
        np.sort(series)[::-1]
        )

def pearson_flow_duration_curve(
        series: npt.ArrayLike,
        number_of_points: int | None = None
        ) -> tuple[npt.NDArray, npt.NDArray]:
    """
    Generate a flow duration curve (FDC) by fitting an array of streamflow
    values to a log-pearson type III distribution using Maximum Likelihood 
    Estimation. The series values determine the type of FDC returned. A series
    of daily or hourly streamflow values will result in a "period-of-record"
    FDC. A series of annual maximum flows will result in an annual peak FDC,
    from which you can derive "annual recurrence intervals."

    Parameters
    ----------
    series: array-like, required
        An array of numerical streamflow values used to fit a flow duration
        curve.
    number_of_points: int, optional
        Number of points in the resulting FDC. This directly determines the
        length of the returned probabilities numpy.ndarray. Point will be
        regularly sampled from the minimum value in series to the maximum
        value in series. The default `number_of_points` is equal to the length
        of series.
    
    Returns
    -------
    probabilities: numpy.ndarray
        Array of values that represent exceedance probabilities, also called
        exceedance frequencies. The range of possible values is [0.0, 1.0].
        These values usually represent the "x-values" on a flow duration curve
        plot. These values can be converted into recurrence intervals by
        dividing them into 1.0 (i.e. 1.0 / probabilities). Note that these
        recurrence intervals will reflect the sampling frequency of the input
        series (e.g. "hourly", "daily", or "annual" recurrence intervals). This
        array will have the same length as series.
    values: numpy.ndarray
        Array of actual streamflow values in the same units as the input
        series. These values correspond directly to exceedance frequencies in
        probabilities. These values usually represent the "y-values" on a flow
        duration curve plot.
    """
    # Validate
    size = len(series)
    assert size > 0, "series is empty"
    assert np.all(series > 0.0), "log pearson cannot fit zero values"
    if number_of_points is not None:
        assert number_of_points > 0, "number_of_points must be positive"
    else:
        number_of_points = len(series)

    # Fit
    log_series = np.log(series)
    parameters = pearson3.fit(log_series)

    # Generate curve
    values = np.linspace(
        np.max(log_series),
        np.min(log_series),
        number_of_points
        )
    return (
        1.0 - pearson3.cdf(values, *parameters),
        np.exp(values)
        )

def bootstrap_flow_duration_curve(
        series: npt.ArrayLike,
        quantiles: npt.ArrayLike,
        repetitions: int = 1200,
        fdc_generator: FDCGenerator = empirical_flow_duration_curve,
        **fdc_params
) -> tuple[npt.NDArray, npt.NDArray]:
    """
    Bootstrap quantiles for a flow duration curve (FDC) from an array of
    streamflow values. This method is typically used to generate confidence
    intervals. The exact nature of the FDC will depend on the fdc_generator
    chosen.
        This method uses the Stationary Bootstrap method, which is suitable for
    time series of streamflow that may have a high degree of time-dependent
    autocorrelation. This uses a method that automatically determines the
    optimal block size. This optimal block size will tend toward 1 for
    uncorrelated data and is suitable for series of independent values as well
    (e.g. annual peaks).

    Parameters
    ----------
    series: array-like, required
        An array of numerical streamflow values used to generate a flow
        duration curve.
    quantiles: array-like, required
        Passed directly to `numpy.quantiles`. Specifies the quantiles to sample
        from the bootstrapped posterior distribution. For a two-tailed 95%
        confidence interval use `quantiles=[0.025, 0.975]`.
    repetitions: int, optional, default 1200
        Number of bootstrapped samples in the posterior distribution of values
        used to extract quantiles.
    fdc_generator: FDCGenerator, optional
        A callable that takes a series and generates a flow duration curve.
        Defaults to `empirical_flow_duration_curve`.
    fdc_params: optional
        Additional keyword arguments passed directly to `fdc_generator`.
    
    Returns
    -------
    probabilities: numpy.ndarray
        Array of values that represent exceedance probabilities, also called
        exceedance frequencies. The range of possible values is [0.0, 1.0].
        These values usually represent the "x-values" on a flow duration curve
        plot. These values can be converted into recurrence intervals by
        dividing them into 1.0 (i.e. 1.0 / probabilities). Note that these
        recurrence intervals will reflect the sampling frequency of the input
        series (e.g. "hourly", "daily", or "annual" recurrence intervals).
    values: numpy.ndarray
        Array of actual streamflow values in the same units as the input
        series. These values correspond directly to exceedance frequencies in
        probabilities. These values usually represent the "y-values" on a flow
        duration curve plot. values will have a shape (m, n) where m is
        the number of `quantiles` specified and n is the number of values in 
        probabilities.
    """
    # Validate
    size = len(series)
    assert size > 0, "series is empty"
    assert repetitions > 0, "repetitions must be greater than 0"

    # Setup bootstrap
    block_size = optimal_block_length(series)["stationary"].iloc[0]
    bs = StationaryBootstrap(block_size, series, seed=2025)

    # Bootstrap values
    def value_generator(s):
        return fdc_generator(s, **fdc_params)[1]
    posterior = bs.apply(value_generator, repetitions)

    # Extract quantiles
    return (
        fdc_generator(series, **fdc_params)[0],
        np.quantile(posterior, quantiles, axis=0)
        )

def interpolate_exceedance_values(
        points: npt.ArrayLike,
        probabilities: npt.ArrayLike,
        values: npt.ArrayLike
        ) -> npt.NDArray | float:
    """
    Use 1-D piecewise linear interpolation to approximate exceedance values
    that correspond to probability points. Probabilities are assumed to be
    sorted from smallest to largest (increasing). Results for decreasing or
    unsorted probabilities will be meaningless.

    Parameters
    ----------
    points: array-like, required
        Coordinates that correspond to points in between those in probabilities
        at which to interpolate values.
    probabilities: array-like, required
        Array of values that represent exceedance probabilities, also called
        exceedance frequencies. The range of possible values is [0.0, 1.0].
        These values usually represent the "x-values" on a flow duration curve
        plot. These values are assumed to be sorted from smallest to
        largest (increasing). Results for decreasing or unsorted probabilities
        will be meaningless.
    values: array-like, required
        Array of actual streamflow values in the same units as the input
        series. These values correspond directly to exceedance frequencies in
        probabilities. These values usually represent the "y-values" on a flow
        duration curve plot.
    
    Returns
    -------
    exceedance_values: float or numpy.ndarray
        The interpolated values. Same shape as points.
    """
    return np.interp(points, probabilities, values)

def interpolate_recurrence_values(
        points: npt.ArrayLike,
        probabilities: npt.ArrayLike,
        values: npt.ArrayLike
        ) -> npt.NDArray | float:
    """
    Use 1-D piecewise linear interpolation to approximate exceedance values
    that correspond to probability points. Probabilities are assumed to be
    sorted from smallest to largest (increasing). Results for decreasing or
    unsorted probabilities will be meaningless.

    Parameters
    ----------
    points: array-like, required
        Coordinates that correspond to points in between those in probabilities
        at which to interpolate values. However, these values are not
        probabilities. These values indicate recurrence intervals. For example,
        if probabilities indicate annual exeedance probabilities and values
        indicate annual peak flows, then a points array that contains
        `[1.5, 50.0, 100.0]` will result in returned values that correspond to
        the 1.5-year, 50-year, and 100-year recurrence flows.
    probabilities: array-like, required
        Array of values that represent exceedance probabilities, also called
        exceedance frequencies. The range of possible values is [0.0, 1.0].
        These values usually represent the "x-values" on a flow duration curve
        plot. These values are assumed to be sorted from smallest to
        largest (increasing). Results for decreasing or unsorted probabilities
        will be meaningless.
    values: array-like, required
        Array of actual streamflow values in the same units as the input
        series. These values correspond directly to exceedance frequencies in
        probabilities. These values usually represent the "y-values" on a flow
        duration curve plot.
    
    Returns
    -------
    recurrence_values: float or numpy.ndarray
        The interpolated values. Same shape as points.
    """
    return interpolate_exceedance_values(1.0 / np.asarray(points),
        probabilities, values)

def richards_flow_responsiveness(
        probabilities: npt.ArrayLike,
        values: npt.ArrayLike
        ) -> dict[str, float]:
    """
    Derive flow responsiveness measures from a flow duration curve according to
    the methods in Richards, 1990.
        Note that this method needs probabilities in the range [0.05, 0.95] in
    order to perform interpolation.

    Parameters
    ----------
    probabilities: array-like, required
        Array of values that represent exceedance probabilities, also called
        exceedance frequencies. The range of possible values is [0.0, 1.0].
        These values usually represent the "x-values" on a flow duration curve
        plot. These values are assumed to be sorted from smallest to
        largest (increasing). Results for decreasing or unsorted probabilities
        will be meaningless.
    values: array-like, required
        Array of actual streamflow values in the same units as the input
        series. These values correspond directly to exceedance frequencies in
        probabilities. These values usually represent the "y-values" on a flow
        duration curve plot.
    
    Returns
    -------
    flow_responsiveness_measures: dict
        Seven measures of flow responsiveness in a dictionary with the
        following keys: ['10R90', '20R80', '25R75', '.5S', '.6S', '.8S',
        'CVLF5'] mapped to numerical float values.

        '10R90', '20R80', and '25R75' indicate "ratio measures" respectively
        computed by dividing the 10/90, 20/80, and 25/75 percentiles from the
        flow duration curve.

        '.5S', '.6S', and '.8S' indicate "spread measures" respectively
        computed by subtracting the 25-75, 20-80, and 10-90 percentiles from
        the flow duration curve, then dividing by the median (50th percentile).

        'CVLF5' is the coefficient of variation of the set of logs of every 5th
        percentile (5, 10, 15, ..., 85, 90, 95).
    """
    # Validate
    assert np.any(0.05 <= probabilities), "Unable to interpolate probabilities"
    assert np.any(0.95 >= probabilities), "Unable to interpolate probabilities"

    points = np.arange(0.05, 1.0, 0.05)
    exceedances = interpolate_exceedance_values(points, probabilities, values)
    mapping = {f"{p:.2f}": e for p, e in list(zip(points, exceedances))}
    return {
        "10R90": mapping["0.10"] / mapping["0.90"],
        "20R80": mapping["0.20"] / mapping["0.80"],
        "25R75": mapping["0.25"] / mapping["0.75"],
        ".5S": (mapping["0.25"] - mapping["0.75"]) / mapping["0.50"],
        ".6S": (mapping["0.20"] - mapping["0.80"]) / mapping["0.50"],
        ".8S": (mapping["0.10"] - mapping["0.90"]) / mapping["0.50"],
        "CVLF5": variation(np.log(exceedances))
    }

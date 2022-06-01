"""
==================
Evaluation Metrics
==================
Convenience methods for computing common evaluation metrics.

For a description of common evaluation metrics, see:

http://www.eumetrain.org/data/4/451/english/courses/msgcrs/index.htm

Functions
---------
 - compute_contingency_table
 - probability_of_detection
 - probability_of_false_detection
 - probability_of_false_alarm
 - threat_score
 - frequency_bias
 - percent_correct
 - base_chance
 - equitable_threat_score
 - mean_error
 - nash_sutcliffe_efficiency
 - kling_gupta_efficiency
 - volumetric_efficiency
 - mean_squared_error
 - root_mean_squared_error
 - mean_error_skill_score
 - coefficient_of_persistence
 - coefficient_of_extrapolation

"""

import numpy as np
import numpy.typing as npt
import pandas as pd
from typing import Union
from . import _validation as validate
from functools import partial

def mean_error(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    power: float = 1.0,
    root: bool = False
    ) -> float:
    """Compute the mean error or deviation. Default is Mean Absolute Error. The mean error 
    is given by:

    $$ME = \frac{1}{n}\sum_{i=1}^{n}\left| y_{s,i} - y_{o,i} \right|^{p}$$

    Where $n$ is the length of each array, $y_{s,i}$ is the *ith* simulated or predicted value, 
    $y_{o,i}$ is the *ith* observed or true value, and $p$ is the exponent.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,), required
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: array-like of shape (n_samples,), required
        Estimated target values, also called simulations or modeled values.
    power: float, default 1.0
        Exponent for each mean error summation value.
    root: bool, default False
        When True, return the root mean error.
        
    Returns
    -------
    mean_error: float
        Mean error or root mean error.
    
    """
    # Compute mean error
    _mean_error = np.sum(np.abs(np.subtract(y_true, y_pred)) ** power) / len(y_true)

    # Return mean error, optionally return root mean error
    if root:
        return np.sqrt(_mean_error)
    return _mean_error

mean_squared_error = partial(mean_error, power=2.0, root=False)
mean_squared_error.__doc__ = """Partial of hydrotools.metrics.mean_error with 
a default power value of 2.0 and root set to False.

See Also
--------
mean_error
"""

root_mean_squared_error = partial(mean_error, power=2.0, root=True)
root_mean_squared_error.__doc__ = """Partial of hydrotools.metrics.mean_error with 
a default power value of 2.0 and root set to True.

See Also
--------
mean_error
"""

def mean_error_skill_score(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    y_base: npt.ArrayLike,
    power: float = 1.0,
    normalized: bool = False
    ) -> float:
    """Compute a generic mean error based model skill score. The mean error skill score 
    is given by:

    $$MESS = 1 - \frac{\sum_{i=1}^{n}\left| y_{p,i} - y_{o,i} \right|^{p}}{\sum_{i=1}^{n}\left| y_{b,i} - y_{o,i} \right|^{p}}$$

    Where $n$ is the length of each array, $y_{s,i}$ is the *ith* simulated or predicted value, 
    $y_{b,i}$ is the *ith* baseline value, $y_{o,i}$ is the *ith* observed or true 
    value, and $p$ is the exponent.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,), required
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: array-like of shape (n_samples,), required
        Estimated target values, also called simulations or modeled values.
    y_base: array-like of shape (n_samples,), required
        Baseline value(s) against which to assess skill of y_pred.
    power: float, default 1.0
        Exponent for each mean error summation value.
    normalized: bool, default False
        When True, normalize the final skill score using the method from 
        Nossent & Bauwens, 2012.
        
    Returns
    -------
    score: float
        Skill score of y_pred relative to y_base.
        
    References
    ----------
    Nossent, J., & Bauwens, W. (2012, April). Application of a normalized 
        Nash-Sutcliffe efficiency to improve the accuracy of the Sobol'sensitivity 
        analysis of a hydrological model. In EGU General Assembly Conference 
        Abstracts (p. 237).
    
    """
    # Compute components
    numerator = mean_error(y_true, y_pred, power=power)
    denominator = mean_error(y_true, y_base, power=power)

    # Compute score, optionally normalize
    if normalized:
        return 1.0 / (1.0 + numerator/denominator)
    return 1.0 - numerator/denominator

volumetric_efficiency = partial(mean_error_skill_score, y_base=0.0, power=1.0)
volumetric_efficiency.__doc__ = """Partial of hydrotools.metrics.mean_error_skill_score 
with a default y_base of 0.0 and a power value of 1.0. Volumetric efficiency ranges from 
-inf to 1.0, higher is better. According to the authors, volumetric efficiency indicates 
the "portion of water that arrives on time." Note: that large over-predictions result in 
deeply negative values.

See Also
--------
mean_error_skill_score

References
----------
Criss, R. E., & Winston, W. E. (2008). Do Nash values have value? Discussion 
    and alternate proposals. Hydrological Processes: An International Journal, 
    22(14), 2723-2725.
"""

def nash_sutcliffe_efficiency(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    log: bool = False,
    power: float = 2.0,
    normalized: bool = False
    ) -> float:
    """Compute the Nash-Sutcliffe model efficiency coefficient (NSE), also called the 
    mean squared error skill score or the R^2 (coefficient of determination) regression score. 
    The NSE compares model errors to observed variance. The default NSE ranges from -inf to 1.0, 
    higher is better. A score of 0.0 indicates the model is as good a predictor as the mean of 
    observations. A score of 1.0 indicates the model exactly matches the observations.

    The "normalized" Nash-Sutcliffe model efficiency re-scales the NSE to a range from 0.0 to 1.0. 
    In this case, A score of 0.5 indicates the model is as good a predictor as the mean of 
    observations. A score of 1.0 still indicates the model exactly matches the observations.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,), required
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: array-like of shape (n_samples,), required
        Estimated target values, also called simulations or modeled values.
    log: bool, default False
        Apply numpy.log (natural logarithm) to y_true and y_pred 
        before computing the NSE.
    power: float, default 2.0
        Exponent for each mean error summation value.
    normalized: bool, default False
        When True, normalize the final NSE value using the method from 
        Nossent & Bauwens, 2012.
        
    Returns
    -------
    score: float
        Nash-Sutcliffe model efficiency coefficient
        
    References
    ----------
    Nash, J. E., & Sutcliffe, J. V. (1970). River flow forecasting through 
        conceptual models part I—A discussion of principles. Journal of 
        hydrology, 10(3), 282-290.
    Nossent, J., & Bauwens, W. (2012, April). Application of a normalized 
        Nash-Sutcliffe efficiency to improve the accuracy of the Sobol'sensitivity 
        analysis of a hydrological model. In EGU General Assembly Conference 
        Abstracts (p. 237).
    
    """
    # Raise if not 1-D arrays
    validate.raise_for_non_vector(y_true, y_pred)

    # Raise if not same shape
    validate.raise_for_inconsistent_shapes(y_true, y_pred)

    # Optionally transform components
    if log:
        y_true = np.log(y_true)
        y_pred = np.log(y_pred)

    # Compute score
    return mean_error_skill_score(y_true, y_pred, np.mean(y_true), 
        power=power, normalized=normalized)

def coefficient_of_persistence(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    lag: int = 1,
    log: bool = False,
    power: float = 2.0,
    normalized: bool = False
    ) -> float:
    """Compute the coefficient of persistence (Kitanidis & Bras, 1980). The coefficient of 
    persistence compares the model to a recent observation, given some lag. This score assesses 
    the model's skill compared to assuming a previous observation does not change (persists).

    In the default case, the *ith* modeled value will be compared to the *i-1* observed value. 
    The result is the mean squared error skill score using the *i-1* observed values as a baseline. 
    The coefficient of persistence ranges from -inf to 1.0, higher is better. A score of 0.0 indicates 
    skill no better than assuming the last observation would persist. A perfect score is 1.0.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,), required
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: array-like of shape (n_samples,), required
        Estimated target values, also called simulations or modeled values.
    lag: int, default 1
        Number of values by which to lag the baseline.
    log: bool, default False
        Apply numpy.log (natural logarithm) to y_true and y_pred 
        before computing the score.
    power: float, default 2.0
        Exponent for each mean error summation value.
    normalized: bool, default False
        When True, normalize the final score using the method from 
        Nossent & Bauwens, 2012.
        
    Returns
    -------
    score: float
        Coefficient of persistence.

    See Also
    --------
    mean_error_skill_score: Generic method for computing model skill.
        
    References
    ----------
    Kitanidis, P. K., & Bras, R. L. (1980). Real-time forecasting with a conceptual 
        hydrologic model: 2. Applications and results. Water Resources Research, 
        16(6), 1034-1044.
    Nossent, J., & Bauwens, W. (2012, April). Application of a normalized 
        Nash-Sutcliffe efficiency to improve the accuracy of the Sobol'sensitivity 
        analysis of a hydrological model. In EGU General Assembly Conference 
        Abstracts (p. 237).
    
    """
    # Raise if not 1-D arrays
    validate.raise_for_non_vector(y_true, y_pred)

    # Raise if not same shape
    validate.raise_for_inconsistent_shapes(y_true, y_pred)

    # Optionally transform components
    if log:
        y_true = np.log(y_true)
        y_pred = np.log(y_pred)

    # Compute baseline
    y_base = np.roll(y_true, lag)

    # Compute score
    return mean_error_skill_score(y_true[lag:], y_pred[lag:], y_base[lag:], 
        power=power, normalized=normalized)

def coefficient_of_extrapolation(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    log: bool = False,
    power: float = 2.0,
    normalized: bool = False
    ) -> float:
    """Compute the coefficient of extrapolation (Kitanidis & Bras, 1980). The coefficient of 
    extrapolation compares the model output to the last two values of the observations, assuming 
    the linear trend of the these values will continue. In other words, the coefficient of 
    extrapolation is a skill score with baseline values $y_{b,i} = y_{b,i-1} + (y_{b,i-1} - y_{b,i-2})$.

    The coefficient of extrapolation ranges from -inf to 1.0, higher is better. A score of 0.0 indicates 
    skill no better than assuming the difference between the last two observations will persist. A perfect 
    score is 1.0.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,), required
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: array-like of shape (n_samples,), required
        Estimated target values, also called simulations or modeled values.
    log: bool, default False
        Apply numpy.log (natural logarithm) to y_true and y_pred 
        before computing the NSE.
    power: float, default 2.0
        Exponent for each mean error summation value.
    normalized: bool, default False
        When True, normalize the final NSE value using the method from 
        Nossent & Bauwens, 2012.
        
    Returns
    -------
    score: float
        Coefficient of extrapolation.

    See Also
    --------
    mean_error_skill_score: Generic method for computing model skill.
        
    References
    ----------
    Kitanidis, P. K., & Bras, R. L. (1980). Real-time forecasting with a conceptual 
        hydrologic model: 2. Applications and results. Water Resources Research, 
        16(6), 1034-1044.
    Nossent, J., & Bauwens, W. (2012, April). Application of a normalized 
        Nash-Sutcliffe efficiency to improve the accuracy of the Sobol'sensitivity 
        analysis of a hydrological model. In EGU General Assembly Conference 
        Abstracts (p. 237).
    
    """
    # Raise if not 1-D arrays
    validate.raise_for_non_vector(y_true, y_pred)

    # Raise if not same shape
    validate.raise_for_inconsistent_shapes(y_true, y_pred)

    # Optionally transform components
    if log:
        y_true = np.log(y_true)
        y_pred = np.log(y_pred)

    # Compute baseline
    slope = np.diff(y_true)[:-1]
    y_base = y_true[2:] + slope

    # Compute score
    return mean_error_skill_score(y_true[2:], y_pred[2:], y_base, 
        power=power, normalized=normalized)

def kling_gupta_efficiency(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    r_scale: float = 1.0,
    a_scale: float = 1.0,
    b_scale: float = 1.0
    ) -> float:
    """Compute the Kling-Gupta model efficiency coefficient (KGE). The KGE is a 
    summary metric that combines the relative mean, relative variance, and linear 
    correlation between observed and simulated values. The final metric is computed 
    using the root sum of squares with optional scaling factors, similar to 
    computing distance in a 3-dimensional Euclidean space.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,), required
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: array-like of shape (n_samples,), required
        Estimated target values, also called simulations or modeled values.
    r_scale: float, optional, default 1.0
        Linear correlation (r) scaling factor. Used to re-scale the Euclidean space by 
        emphasizing different KGE components.
    a_scale: float, optional, default 1.0
        Relative variability (alpha) scaling factor. Used to re-scale the Euclidean space by 
        emphasizing different KGE components.
    b_scale: float, optional, default 1.0
        Relative mean (beta) scaling factor. Used to re-scale the Euclidean space by 
        emphasizing different KGE components.
        
    Returns
    -------
    score: float
        Kling-Gupta efficiency.
        
    References
    ----------
    Gupta, H. V., Kling, H., Yilmaz, K. K., & Martinez, G. F. (2009). Decomposition of 
        the mean squared error and NSE performance criteria: Implications for improving 
        hydrological modelling. Journal of hydrology, 377(1-2), 80-91. 
        https://doi.org/10.1016/j.jhydrol.2009.08.003
    
    """
    # Raise if not 1-D arrays
    validate.raise_for_non_vector(y_true, y_pred)

    # Raise if not same shape
    validate.raise_for_inconsistent_shapes(y_true, y_pred)

    # Pearson correlation coefficient
    linear_correlation = np.corrcoef(y_pred, y_true)[0,1]

    # Relative variability
    relative_variability = np.std(y_pred) / np.std(y_true)

    # Relative mean
    relative_mean = np.mean(y_pred) / np.mean(y_true)

    # Scaled Euclidean distance
    euclidean_distance = np.sqrt(
        (r_scale * (linear_correlation - 1.0)) ** 2.0 + 
        (a_scale * (relative_variability - 1.0)) ** 2.0 + 
        (b_scale * (relative_mean - 1.0)) ** 2.0
        )

    # Return KGE
    return 1.0 - euclidean_distance

def compute_contingency_table(
    observed: npt.ArrayLike,
    simulated: npt.ArrayLike,
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive',
    false_negative_key: str = 'false_negative',
    true_negative_key: str = 'true_negative'
    ) -> pd.Series:
    """Compute components of a contingency table required for the evaluation of categorical 
    forecasts and simulations. Returns a pandas.Series indexed by table component. 'true_positive' 
    indicates the number of times the simulation correctly indicated True according to the 
    observations. 'false_positive' indicates the number of times the simulation incorrectly 
    indicated True according to the observations. 'false_negative' indicates the number of times 
    the simulation incorrectly indicated False according to the observations. 'true_negative' 
    indicates the number of times the simulation correctly indicated False according to the 
    observations.
        
    Parameters
    ----------
    observed: array-like, required
        Array-like of boolean values indicating observed occurrences
    simulated: array-like, required
        Array-like of boolean values indicating simulated occurrences
    true_positive_key: str, optional, default 'true_positive'
        Label to use for true positives.
    false_positive_key: str, optional, default 'false_positive'
        Label to use for false positives.
    false_negative_key: str, optional, default 'false_negative'
        Label to use for false negatives.
    true_negative_key: str, optional, default 'true_negative'
        Label to use for true negatives.
        
    Returns
    -------
    contingency_table: pandas.Series
        pandas.Series of integer values keyed to pandas.Index([true_positive_key, false_positive_key, 
            false_negative_key, true_negative_key])

    Examples
    --------
    >>> obs = [True, True, True, False, False, False, False, False, True, True]
    >>> sim = [True, True, False, False, False, False, True, False, False, False]
    >>> metrics.compute_contingency_table(obs, sim)
    true_positive     2
    false_positive    1
    false_negative    3
    true_negative     4
    dtype: int64
        
    """
    # Raise if not 1-D arrays
    validate.raise_for_non_vector(observed, simulated)

    # Raise if not same shape
    validate.raise_for_inconsistent_shapes(observed, simulated)

    # Validate boolean categorical
    observed = validate.convert_to_boolean_categorical_series(observed)
    simulated = validate.convert_to_boolean_categorical_series(simulated)

    # Cross tabulate
    ctab = pd.crosstab(observed, simulated, dropna=False)

    # Reformat
    return pd.Series({
        true_positive_key : ctab.loc[True, True],
        false_positive_key : ctab.loc[False, True],
        false_negative_key : ctab.loc[True, False],
        true_negative_key : ctab.loc[False, False]
        })

def probability_of_detection(
    contingency_table: Union[dict, pd.DataFrame, pd.Series],
    true_positive_key: str = 'true_positive',
    false_negative_key: str = 'false_negative'
    ) -> float:
    """Compute probability of detection (POD), also called the "hit rate". POD 
    is the ratio of true positives to the number of observations. POD ranges 
    from 0.0 to 1.0, higher is better. Note: that this statistic is easy to 
    "hedge" if the model always indicates occurence. This statistic should 
    be considered alongside some metric of false positives, like probability 
    of false alarm or threat score.
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following 
        keys: true_positive_key, false_positive_key, false_negative_key, 
        true_negative_key; and int or float values
    true_positive_key: str, optional, default 'true_positive'
        Label to use for true positives.
    false_negative_key: str, optional, default 'false_negative'
        Label to use for false negatives.
        
    Returns
    -------
    POD: float
        Probability of detection.
        
    """
    # Convert values to numpy scalars
    contingency_table = pd.Series(contingency_table, dtype=np.float64)

    # Compute
    a = contingency_table[true_positive_key]
    c = contingency_table[false_negative_key]
    return a / (a+c)

def probability_of_false_detection(
    contingency_table: Union[dict, pd.DataFrame, pd.Series],
    false_positive_key: str = 'false_positive',
    true_negative_key: str = 'true_negative'
    ) -> float:
    """Compute probability of false detection/false alarm rate (POFD/FARate). POFD 
    indicates the portion of non-occurences that were false alarms. POFD ranges from 
    0.0 to 1.0, lower is better.
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following 
        keys: true_positive_key, false_positive_key, false_negative_key, 
        true_negative_key; and int or float values
    false_positive_key: str, optional, default 'false_positive'
        Label to use for false positives.
    true_negative_key: str, optional, default 'true_negative'
        Label to use for true negatives.
        
    Returns
    -------
    POFD: float
        Probability of false detection.
        
    """
    # Convert values to numpy scalars
    contingency_table = pd.Series(contingency_table, dtype=np.float64)

    # Compute
    b = contingency_table[false_positive_key]
    d = contingency_table[true_negative_key]
    return b / (b+d)

def probability_of_false_alarm(
    contingency_table: Union[dict, pd.DataFrame, pd.Series],
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive'
    ) -> float:
    """Compute probability of false alarm/false alarm ratio (POFA/FARatio). POFA 
    indicates the portion of predictions or simulated values that were false alarms. 
    POFA ranges from 0.0 to 1.0, lower is better. The complement of POFA (1.0 - POFA) is 
    the 'post-agreement (PAG).'
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following 
        keys: true_positive_key, false_positive_key, false_negative_key, 
        true_negative_key; and int or float values
    true_positive_key: str, optional, default 'true_positive'
        Label to use for true positives.
    false_positive_key: str, optional, default 'false_positive'
        Label to use for false positives.
        
    Returns
    -------
    POFA: float
        Probability of false alarm.
        
    """
    # Convert values to numpy scalars
    contingency_table = pd.Series(contingency_table, dtype=np.float64)

    # Compute
    b = contingency_table[false_positive_key]
    a = contingency_table[true_positive_key]
    return b / (b+a)

def threat_score(
    contingency_table: Union[dict, pd.DataFrame, pd.Series],
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive',
    false_negative_key: str = 'false_negative'
    ) -> float:
    """Compute threat score/critical success index (TS/CSI). CSI is the ratio 
    true positives to the sum of true positives, false positives, and false 
    negatives. CSI ranges from 0.0 to 1.0, higher is better. CSI is sensitive 
    to event frequency, in which case the equitable threat score may be more 
    suitable.
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following 
        keys: true_positive_key, false_positive_key, false_negative_key, 
        true_negative_key; and int or float values
    true_positive_key: str, optional, default 'true_positive'
        Label to use for true positives.
    false_positive_key: str, optional, default 'false_positive'
        Label to use for false positives.
    false_negative_key: str, optional, default 'false_negative'
        Label to use for false negatives.
        
    Returns
    -------
    TS: float
        Threat score.
        
    """
    # Convert values to numpy scalars
    contingency_table = pd.Series(contingency_table, dtype=np.float64)

    # Compute
    a = contingency_table[true_positive_key]
    b = contingency_table[false_positive_key]
    c = contingency_table[false_negative_key]
    return a / (a+b+c)

def frequency_bias(
    contingency_table: Union[dict, pd.DataFrame, pd.Series],
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive',
    false_negative_key: str = 'false_negative'
    ) -> float:
    """Compute frequency bias (FBI). FBI measures the tendency of the simulation 
    or forecast to over or under-predict. FBI ranges from 0.0 to inf. A perfect 
    score is 1.0. Values less than 1.0 indicate under-prediction. Values greater 
    than 1.0 indicate over-prediction.
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following 
        keys: true_positive_key, false_positive_key, false_negative_key, 
        true_negative_key; and int or float values
    true_positive_key: str, optional, default 'true_positive'
        Label to use for true positives.
    false_positive_key: str, optional, default 'false_positive'
        Label to use for false positives.
    false_negative_key: str, optional, default 'false_negative'
        Label to use for false negatives.
        
    Returns
    -------
    FBI: float
        Frequency bias.
        
    """
    # Convert values to numpy scalars
    contingency_table = pd.Series(contingency_table, dtype=np.float64)

    # Compute
    a = contingency_table[true_positive_key]
    b = contingency_table[false_positive_key]
    c = contingency_table[false_negative_key]
    return (a+b) / (a+c)

def percent_correct(
    contingency_table: Union[dict, pd.DataFrame, pd.Series],
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive',
    false_negative_key: str = 'false_negative',
    true_negative_key: str = 'true_negative'
    ) -> float:
    """Compute percent correct (PC). PC is the sum of both true positives and 
    true negatives compared to the total number of observations. PC is the portion 
    of correctly predicted occurences and non-occurences. PC ranges from 0.0 to 1.0, 
    higher is better.
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following 
        keys: true_positive_key, false_positive_key, false_negative_key, 
        true_negative_key; and int or float values
    true_positive_key: str, optional, default 'true_positive'
        Label to use for true positives.
    false_positive_key: str, optional, default 'false_positive'
        Label to use for false positives.
    false_negative_key: str, optional, default 'false_negative'
        Label to use for false negatives.
    true_negative_key: str, optional, default 'true_negative'
        Label to use for true negatives.
        
    Returns
    -------
    PC: float
        Percent correct.
        
    """
    # Convert values to numpy scalars
    contingency_table = pd.Series(contingency_table, dtype=np.float64)

    # Compute
    a = contingency_table[true_positive_key]
    b = contingency_table[false_positive_key]
    c = contingency_table[false_negative_key]
    d = contingency_table[true_negative_key]
    return (a+d) / (a+b+c+d)

def base_chance(
    contingency_table: Union[dict, pd.DataFrame, pd.Series],
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive',
    false_negative_key: str = 'false_negative',
    true_negative_key: str = 'true_negative'
    ) -> float:
    """Compute base chance to hit (a_r). Base chance is the relative frequency of 
    occurences. In other words, this is the probability of scoring a "hit" or true positive 
    by chance.
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following keys: true_positive_key, false_positive_key, 
            false_negative_key, true_negative_key; and int or float values 
    true_positive_key: str, optional, default 'true_positive'
        Label to use for true positives.
    false_positive_key: str, optional, default 'false_positive'
        Label to use for false positives.
    false_negative_key: str, optional, default 'false_negative'
        Label to use for false negatives.
    true_negative_key: str, optional, default 'true_negative'
        Label to use for true negatives.
        
    Returns
    -------
    a_r: float
        Base chance to hit by chance.
        
    """
    # Convert values to numpy scalars
    contingency_table = pd.Series(contingency_table, dtype=np.float64)

    # Compute
    a = contingency_table[true_positive_key]
    b = contingency_table[false_positive_key]
    c = contingency_table[false_negative_key]
    d = contingency_table[true_negative_key]
    return ((a+b) * (a+c)) / (a+b+c+d)

def equitable_threat_score(
    contingency_table: Union[dict, pd.DataFrame, pd.Series],
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive',
    false_negative_key: str = 'false_negative',
    true_negative_key: str = 'true_negative'
    ) -> float:
    """Compute equitable threat score (ETS). Threat score/Critical Success Index 
    tends to yield lower scores for rare events. ETS computes a threat score, but 
    accounts for the relative frequency of scoring a true positive by chance.
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following 
        keys: true_positive_key, false_positive_key, false_negative_key, 
        true_negative_key; and int or float values
    true_positive_key: str, optional, default 'true_positive'
        Label to use for true positives.
    false_positive_key: str, optional, default 'false_positive'
        Label to use for false positives.
    false_negative_key: str, optional, default 'false_negative'
        Label to use for false negatives.
    true_negative_key: str, optional, default 'true_negative'
        Label to use for true negatives.
        
    Returns
    -------
    ETS: float
        Equitable threat score.
        
    """
    # Convert values to numpy scalars
    contingency_table = pd.Series(contingency_table, dtype=np.float64)

    # Compute
    a_r = base_chance(contingency_table,
        true_positive_key=true_positive_key,
        false_positive_key=false_positive_key,
        false_negative_key=false_negative_key,
        true_negative_key=true_negative_key
        )
    a = contingency_table[true_positive_key]
    b = contingency_table[false_positive_key]
    c = contingency_table[false_negative_key]
    return (a-a_r) / (a+b+c-a_r)

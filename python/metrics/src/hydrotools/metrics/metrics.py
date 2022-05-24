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
 - mean_squared_error
 - nash_sutcliffe_efficiency
 - kling_gupta_efficiency

"""

import numpy as np
import numpy.typing as npt
import pandas as pd
from typing import Union, Mapping, MutableMapping
from . import _validation as validate

def mean_squared_error(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    root: bool = False
    ) -> float:
    """Compute the mean squared error, or optionally root mean squared error.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,), required
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: array-like of shape (n_samples,), required
        Estimated target values, also called simulations or modeled values.
    root: bool, default False
        When True, return the root mean squared error.
        
    Returns
    -------
    error: float
        Mean squared error or root mean squared error.
    
    """
    # Compute mean squared error
    MSE = np.sum(np.subtract(y_true, y_pred) ** 2.0) / len(y_true)

    # Return MSE, optionally return root mean squared error
    if root:
        return np.sqrt(MSE)
    return MSE

def nash_sutcliffe_efficiency(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    log: bool = False,
    normalized: bool = False
    ) -> float:
    """Compute the Nash-Sutcliffe model efficiency coefficient (NSE), also called the 
    mean squared error skill score or the R^2 (coefficient of determination) regression score.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,), required
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: array-like of shape (n_samples,), required
        Estimated target values, also called simulations or modeled values.
    log: bool, default False
        Apply numpy.log (natural logarithm) to y_true and y_pred 
        before computing the NSE.
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
        Nash-Sutcliffe efficiency to improve the accuracy of the Sobol' 
        sensitivity analysis of a hydrological model. In EGU General Assembly 
        Conference Abstracts (p. 237).
    
    """
    # Raise if not 1-D arrays
    validate.raise_for_non_vector(y_true, y_pred)

    # Raise if not same shape
    validate.raise_for_inconsistent_shapes(y_true, y_pred)

    # Optionally transform components
    if log:
        y_true = np.log(y_true)
        y_pred = np.log(y_pred)

    # Compute components
    numerator = mean_squared_error(y_true, y_pred)
    denominator = mean_squared_error(y_true, np.mean(y_true))

    # Compute score, optionally normalize
    if normalized:
        return 1.0 / (1.0 + numerator/denominator)
    return 1.0 - numerator/denominator

def kling_gupta_efficiency(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    r_scale: float = 1.0,
    a_scale: float = 1.0,
    b_scale: float = 1.0
    ) -> float:
    """Compute the Kling-Gupta model efficiency coefficient (KGE).
        
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
    r = np.corrcoef(y_pred, y_true)[0,1]

    # Relative variability
    a = np.std(y_pred) / np.std(y_true)

    # Relative mean
    b = np.mean(y_pred) / np.mean(y_true)

    # Scaled Euclidean distance
    EDs = np.sqrt(
        (r_scale * (r - 1.0)) ** 2.0 + 
        (a_scale * (a - 1.0)) ** 2.0 + 
        (b_scale * (b - 1.0)) ** 2.0
        )

    # Return KGE
    return 1.0 - EDs

def compute_contingency_table(
    observed: npt.ArrayLike,
    simulated: npt.ArrayLike,
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive',
    false_negative_key: str = 'false_negative',
    true_negative_key: str = 'true_negative'
    ) -> pd.Series:
    """Compute components of a contingency table.
        
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
        pandas.Series of integer values keyed to pandas.Index([true_positive_key, false_positive_key, false_negative_key, true_negative_key])
        
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
    """Compute probability of detection (POD).
        
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
    """Compute probability of false detection/false alarm rate (POFD/FARate).
        
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
    """Compute probability of false alarm/false alarm ratio (POFA/FARatio).
        
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
    """Compute threat score/critical success index (TS/CSI).
        
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
    """Compute frequency bias (FBI).
        
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
    """Compute percent correct (PC).
        
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
    """Compute base chance to hit (a_r).
        
    Parameters
    ----------
    contingency_table: dict, pandas.DataFrame, or pandas.Series, required
        Contingency table containing key-value pairs with the following keys: true_positive_key, false_positive_key, false_negative_key, true_negative_key; and int or float values 
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
    """Compute equitable threat score (ETS).
        
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

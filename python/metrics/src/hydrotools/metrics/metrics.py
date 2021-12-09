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
 - convert_mapping_values
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

"""

import numpy as np
import numpy.typing as npt
import pandas as pd
from typing import Union, Mapping, MutableMapping

def mean_squared_error(
    y_true: npt.ArrayLike,
    y_pred: npt.ArrayLike,
    root: bool = False
    ) -> float:
    """Compute the mean squared error, or optionally root mean squared error.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: pandas.Series, required
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
    """Compute the Nash–Sutcliffe model efficiency coefficient (NSE), also called the 
    mean squared error skill score or the R^2 (coefficient of determination) regression score.
        
    Parameters
    ----------
    y_true: array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values, also called observations, measurements, or observed values.
    y_pred: pandas.Series, required
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

def compute_contingency_table(
    observed: pd.Series,
    simulated: pd.Series,
    true_positive_key: str = 'true_positive',
    false_positive_key: str = 'false_positive',
    false_negative_key: str = 'false_negative',
    true_negative_key: str = 'true_negative'
    ) -> pd.Series:
    """Compute components of a contingency table.
        
    Parameters
    ----------
    observed: pandas.Series, required
        pandas.Series of boolean pandas.Categorical values indicating observed occurrences
    simulated: pandas.Series, required
        pandas.Series of boolean pandas.Categorical values indicating simulated occurrences
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
    # Cross tabulate
    ctab = pd.crosstab(observed, simulated, dropna=False)

    # Reformat
    return pd.Series({
        true_positive_key : ctab.loc[True, True],
        false_positive_key : ctab.loc[False, True],
        false_negative_key : ctab.loc[True, False],
        true_negative_key : ctab.loc[False, False]
        })

def convert_mapping_values(
    mapping: Mapping[str, npt.DTypeLike],
    converter: np.dtype = np.float64
    ) -> MutableMapping:
    """Convert mapping values to a consistent type. Primarily used to validate 
    contingency tables.
        
    Parameters
    ----------
    mapping: dict-like, required
        Input mapping with string keys and values that can be coerced into a 
        numpy data type.
    converter: numpy.dtype, optional, default numpy.float64
        Converter data type or function used to convert mapping values to a 
        consistent type.
        
    Returns
    -------
    converted_mapping: dict-like, same type as mapping
        New mapping with converted values.
        
    """
    # Populate new dictionary with converted values
    d = {}
    for key, value in dict(mapping).items():
        d[key] = converter(value)

    # Return new mapping with same type as original
    return type(mapping)(d)

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
    contingency_table = convert_mapping_values(contingency_table)

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
    contingency_table = convert_mapping_values(contingency_table)

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
    contingency_table = convert_mapping_values(contingency_table)

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
    contingency_table = convert_mapping_values(contingency_table)

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
    contingency_table = convert_mapping_values(contingency_table)

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
    contingency_table = convert_mapping_values(contingency_table)

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
    contingency_table = convert_mapping_values(contingency_table)

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
    contingency_table = convert_mapping_values(contingency_table)

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

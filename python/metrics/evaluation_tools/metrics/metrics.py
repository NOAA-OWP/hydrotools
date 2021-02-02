"""
==================
Evaluation Metrics
==================
Convenience methods for computing common evaluation metrics.

For a description of common evaluation metrics, see:

http://www.eumetrain.org/data/4/451/english/courses/msgcrs/index.htm

Functions
---------
compute_contingency_table
probability_of_detection
probability_of_false_detection
probability_of_false_alarm
threat_score
frequency_bias
percent_correct
base_chance
equitable_threat_score

"""

import pandas as pd
from typing import Union

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
            pandas.Series of boolean pandas.Categorical values indicating
            observed occurences
        simulated: pandas.Series, required
            pandas.Series of boolean pandas.Categorical values indicating
            simulated occurences
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
            pandas.Series of integer values keyed to pandas.Index([
                true_positive_key,
                false_positive_key
                false_negative_key,
                true_negative_key
                ])
        
    """
    # Cross tabulate
    ctab = pd.crosstab(observed, simulated, dropna=False)

    # Reformat
    return pd.Series({
        true_positive_key : ctab.loc[True, True],
        false_positive_key : ctab.loc[True, False],
        false_negative_key : ctab.loc[False, True],
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
        a_r: float
            Base chance to hit by chance.
        
    """
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
    a_r = base_chance(contingency_table)
    a = contingency_table[true_positive_key]
    b = contingency_table[false_positive_key]
    c = contingency_table[false_negative_key]
    return (a-a_r) / (a+b+c-a_r)

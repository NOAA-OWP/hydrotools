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

"""

import pandas as pd
from typing import Union

def compute_contingency_table(obs, sim):
    """Compute components of a contingency table
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    # Cross tabulate
    ctab = pd.crosstab(obs, sim, dropna=False)

    # Reformat
    return pd.Series({
        'true_positive' : ctab.loc[True, True],
        'false_positive' : ctab.loc[False, True],
        'false_negative' : ctab.loc[True, False],
        'true_negative' : ctab.loc[False, False]
        })

def probability_of_detection(contingency_table):
    """Compute probability of detection (POD).
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    a = contingency_table['true_positive']
    c = contingency_table['false_negative']
    return a / (a+c)

def probability_of_false_detection(contingency_table):
    """Compute probability of false detection/false alarm rate (POFD/FARate).
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    b = contingency_table['false_positive']
    d = contingency_table['true_negative']
    return b / (b+d)

def probability_of_false_alarm(contingency_table):
    """Compute probability of false alarm/false alarm ratio (POFD/FARatio).
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    b = contingency_table['false_positive']
    a = contingency_table['true_positive']
    return b / (b+a)

def threat_score(contingency_table):
    """Compute threat score/critical success index (TS/CSI).
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    a = contingency_table['true_positive']
    b = contingency_table['false_positive']
    c = contingency_table['false_negative']
    return a / (a+b+c)

def frequency_bias(contingency_table):
    """Compute frequency bias (FBI).
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    a = contingency_table['true_positive']
    b = contingency_table['false_positive']
    c = contingency_table['false_negative']
    return (a+b) / (a+c)

def percent_correct(contingency_table):
    """Compute percent correct (PC).
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    a = contingency_table['true_positive']
    b = contingency_table['false_positive']
    c = contingency_table['false_negative']
    d = contingency_table['true_negative']
    return (a+d) / (a+b+c+d)

def base_chance(contingency_table):
    """Compute base chance to hit (a_r).
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    a = contingency_table['true_positive']
    b = contingency_table['false_positive']
    c = contingency_table['false_negative']
    d = contingency_table['true_negative']
    return ((a+b) * (a+c)) / (a+b+c+d)

def equitable_threat_score(contingency_table):
    """Compute equitable threat score (ETS).
        
        Parameters
        ----------
        contingency_table: dict, pandas.DataFrame, or pandas.Series, required
            Contingency table containing key-value pairs with the following 
            keys: 'true_positive', 'false_positive', 'false_negative', 
                'true_negative'; and int or float values
            
        Returns
        -------
        POD: float
            Probability of detection.
        
    """
    a_r = base_chance(contingency_table)
    a = contingency_table['true_positive']
    b = contingency_table['false_positive']
    c = contingency_table['false_negative']
    return (a-a_r) / (a+b+c-a_r)

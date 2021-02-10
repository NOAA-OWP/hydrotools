import pytest
from evaluation_tools.metrics import metrics

import pandas as pd
from math import isclose

contigency_table = {
    'true_positive': 1,
    'false_positive': 2,
    'false_negative': 3,
    'true_negative': 4
}

alt_contigency_table = {
    'TP': 1,
    'FP': 2,
    'FN': 3,
    'TN': 4
}

def test_compute_contingency_table():
    obs = pd.Categorical([True, False, False, True, True, True,
        False, False, False, False])
    sim = pd.Categorical([True, True, True, False, False, False, 
        False, False, False, False])

    table = metrics.compute_contingency_table(obs, sim)

    assert table['true_positive'] == 1
    assert table['false_positive'] == 2
    assert table['false_negative'] == 3
    assert table['true_negative'] == 4

    alt_table = metrics.compute_contingency_table(obs, sim, 
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )

    assert alt_table['TP'] == 1
    assert alt_table['FP'] == 2
    assert alt_table['FN'] == 3
    assert alt_table['TN'] == 4

def test_probability_of_detection():
    POD = metrics.probability_of_detection(contigency_table)
    assert POD == (1/4)

    POD = metrics.probability_of_detection(alt_contigency_table,
        true_positive_key='TP',
        false_negative_key='FN'
        )
    assert POD == (1/4)

def test_probability_of_false_detection():
    POFD = metrics.probability_of_false_detection(contigency_table)
    assert POFD == (2/6)

    POFD = metrics.probability_of_false_detection(alt_contigency_table,
        false_positive_key='FP',
        true_negative_key='TN'
        )
    assert POFD == (2/6)

def test_probability_of_false_alarm():
    POFA = metrics.probability_of_false_alarm(contigency_table)
    assert POFA == (2/3)


    POFA = metrics.probability_of_false_alarm(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP'
        )
    assert POFA == (2/3)

def test_threat_score():
    TS = metrics.threat_score(contigency_table)
    assert TS == (1/6)


    TS = metrics.threat_score(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN'
        )
    assert TS == (1/6)

def test_frequency_bias():
    FBI = metrics.frequency_bias(contigency_table)
    assert FBI == (3/4)

    FBI = metrics.frequency_bias(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN'
        )
    assert FBI == (3/4)

def test_percent_correct():
    PC = metrics.percent_correct(contigency_table)
    assert PC == (5/10)

    PC = metrics.percent_correct(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert PC == (5/10)

def test_base_chance():
    a_r = metrics.base_chance(contigency_table)
    assert a_r == (12/10)

    a_r = metrics.base_chance(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert a_r == (12/10)

def test_equitable_threat_score():
    ETS = metrics.equitable_threat_score(contigency_table)
    assert isclose(ETS, (-0.2/4.8), abs_tol=0.000001)

    ETS = metrics.equitable_threat_score(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert isclose(ETS, (-0.2/4.8), abs_tol=0.000001)

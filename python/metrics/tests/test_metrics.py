import pytest
from evaluation_tools.metrics import metrics

import pandas as pd
from math import isclose

contigency_table= {
    'true_positive': 1,
    'false_positive': 2,
    'false_negative': 3,
    'true_negative': 4
}

def test_compute_contingency_table():
    obs = pd.Categorical([True, True, True, False, False, False, 
        False, False, False, False])
    sim = pd.Categorical([True, False, False, True, True, True, 
        False, False, False, False])

    table = metrics.compute_contingency_table(obs, sim)

    assert table['true_positive'] == 1
    assert table['false_positive'] == 2
    assert table['false_negative'] == 3
    assert table['true_negative'] == 4

def test_probability_of_detection():
    POD = metrics.probability_of_detection(contigency_table)
    assert POD == (1/4)

def test_probability_of_false_detection():
    POFD = metrics.probability_of_false_detection(contigency_table)
    assert POFD == (2/6)

def test_probability_of_false_alarm():
    POFA = metrics.probability_of_false_alarm(contigency_table)
    assert POFA == (2/3)

def test_threat_score():
    TS = metrics.threat_score(contigency_table)
    assert TS == (1/6)

def test_frequency_bias():
    FBI = metrics.frequency_bias(contigency_table)
    assert FBI == (3/4)

def test_percent_correct():
    PC = metrics.percent_correct(contigency_table)
    assert PC == (5/10)

def test_base_chance():
    a_r = metrics.base_chance(contigency_table)
    assert a_r == (12/10)

def test_equitable_threat_score():
    ETS = metrics.equitable_threat_score(contigency_table)
    assert isclose(ETS, (-0.2/4.8), abs_tol=0.000001)

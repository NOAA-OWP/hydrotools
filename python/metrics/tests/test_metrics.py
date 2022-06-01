import pytest
from hydrotools.metrics import metrics

import pandas as pd
import numpy as np

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

zero_contingency_table = {
    'true_positive': 0,
    'false_positive': 0,
    'false_negative': 0,
    'true_negative': 0
}

nan_contigency_table = {
    'true_positive': np.nan,
    'false_positive': np.nan,
    'false_negative': np.nan,
    'true_negative': np.nan
}

char_contigency_table = {
    'true_positive': '1',
    'false_positive': '2',
    'false_negative': '3',
    'true_negative': '4'
}

y_true = [1., 2., 3., 4.]
y_pred = [4., 3., 2., 1.]

z_true = [0., 0., 0., 0.]
z_pred = [0., 0., 0., 0.]

n_true = [np.nan, np.nan, np.nan, np.nan]
n_pred = [np.nan, np.nan, np.nan, np.nan]

y_true_series = pd.Series(
    data=y_true,
    index=pd.date_range(
        start="2020-01-01", 
        end="2020-01-04", 
        freq="1D"
    )
)

y_pred_series = pd.Series(
    data=y_pred,
    index=pd.date_range(
        start="2020-01-01", 
        end="2020-01-04", 
        freq="1D"
    )
)

def test_compute_contingency_table():
    obs = pd.Series([True, False, False, True, True, True,
        False, False, False, False], dtype="category")
    sim = pd.Series([True, True, True, False, False, False, 
        False, False, False, False], dtype="category")

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

    with pytest.warns(RuntimeWarning):
        POD = metrics.probability_of_detection(zero_contingency_table)
        assert np.isnan(POD)

    POD = metrics.probability_of_detection(nan_contigency_table)
    assert np.isnan(POD)

    POD = metrics.probability_of_detection(char_contigency_table)
    assert POD == (1/4)

def test_probability_of_false_detection():
    POFD = metrics.probability_of_false_detection(contigency_table)
    assert POFD == (2/6)

    POFD = metrics.probability_of_false_detection(char_contigency_table)
    assert POFD == (2/6)

    POFD = metrics.probability_of_false_detection(alt_contigency_table,
        false_positive_key='FP',
        true_negative_key='TN'
        )
    assert POFD == (2/6)

    with pytest.warns(RuntimeWarning):
        POFD = metrics.probability_of_false_detection(zero_contingency_table)
        assert np.isnan(POFD)

    POFD = metrics.probability_of_false_detection(nan_contigency_table)
    assert np.isnan(POFD)

def test_probability_of_false_alarm():
    POFA = metrics.probability_of_false_alarm(contigency_table)
    assert POFA == (2/3)

    POFA = metrics.probability_of_false_alarm(char_contigency_table)
    assert POFA == (2/3)

    POFA = metrics.probability_of_false_alarm(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP'
        )
    assert POFA == (2/3)

    with pytest.warns(RuntimeWarning):
        POFA = metrics.probability_of_false_alarm(zero_contingency_table)
        assert np.isnan(POFA)

    POFA = metrics.probability_of_false_alarm(nan_contigency_table)
    assert np.isnan(POFA)

def test_threat_score():
    TS = metrics.threat_score(contigency_table)
    assert TS == (1/6)

    TS = metrics.threat_score(char_contigency_table)
    assert TS == (1/6)

    TS = metrics.threat_score(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN'
        )
    assert TS == (1/6)

    with pytest.warns(RuntimeWarning):
        TS = metrics.threat_score(zero_contingency_table)
        assert np.isnan(TS)

    TS = metrics.threat_score(nan_contigency_table)
    assert np.isnan(TS)

def test_frequency_bias():
    FBI = metrics.frequency_bias(contigency_table)
    assert FBI == (3/4)

    FBI = metrics.frequency_bias(char_contigency_table)
    assert FBI == (3/4)

    FBI = metrics.frequency_bias(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN'
        )
    assert FBI == (3/4)

    with pytest.warns(RuntimeWarning):
        FBI = metrics.frequency_bias(zero_contingency_table)
        assert np.isnan(FBI)

    FBI = metrics.frequency_bias(nan_contigency_table)
    assert np.isnan(FBI)

def test_percent_correct():
    PC = metrics.percent_correct(contigency_table)
    assert PC == (5/10)

    PC = metrics.percent_correct(char_contigency_table)
    assert PC == (5/10)

    PC = metrics.percent_correct(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert PC == (5/10)

    with pytest.warns(RuntimeWarning):
        PC = metrics.percent_correct(zero_contingency_table)
        assert np.isnan(PC)

    PC = metrics.percent_correct(nan_contigency_table)
    assert np.isnan(PC)

def test_base_chance():
    a_r = metrics.base_chance(contigency_table)
    assert a_r == (12/10)

    a_r = metrics.base_chance(char_contigency_table)
    assert a_r == (12/10)

    a_r = metrics.base_chance(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert a_r == (12/10)

    with pytest.warns(RuntimeWarning):
        a_r = metrics.base_chance(zero_contingency_table)
        assert np.isnan(a_r)

    a_r = metrics.base_chance(nan_contigency_table)
    assert np.isnan(a_r)

def test_equitable_threat_score():
    ETS = metrics.equitable_threat_score(contigency_table)
    assert np.isclose(ETS, (-0.2/4.8), atol=0.000001)

    ETS = metrics.equitable_threat_score(char_contigency_table)
    assert np.isclose(ETS, (-0.2/4.8), atol=0.000001)

    ETS = metrics.equitable_threat_score(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert np.isclose(ETS, (-0.2/4.8), atol=0.000001)

    with pytest.warns(RuntimeWarning):
        ETS = metrics.equitable_threat_score(zero_contingency_table)
        assert np.isnan(ETS)

    ETS = metrics.equitable_threat_score(nan_contigency_table)
    assert np.isnan(ETS)

def test_mean_absolute_error():
    MAE = metrics.mean_error(y_true, y_pred)
    assert MAE == 2.0

def test_mean_error():
    MSE = metrics.mean_error(y_true, y_pred, power=2.0)
    assert MSE == 5.0

    RMSE = metrics.mean_error(y_true, y_pred, power=2.0, root=True)
    assert RMSE == np.sqrt(5.0)

def test_nash_sutcliffe_efficiency():
    NSE = metrics.nash_sutcliffe_efficiency(y_true, y_pred)
    assert NSE == -3.0
    
    NNSE = metrics.nash_sutcliffe_efficiency(y_true, y_pred, 
        normalized=True)
    assert NNSE == 0.2
    
    NSEL = metrics.nash_sutcliffe_efficiency(np.exp(y_true), 
        np.exp(y_pred), log=True)
    assert NSEL == -3.0
    
    NNSEL = metrics.nash_sutcliffe_efficiency(np.exp(y_true), 
        np.exp(y_pred), log=True, normalized=True)
    assert NNSEL == 0.2

def test_zero_mean_error():
    MSE = metrics.mean_error(z_true, z_pred, power=2.0)
    assert MSE == 0.0

    RMSE = metrics.mean_error(z_true, z_pred, power=2.0, root=True)
    assert RMSE == 0.0

def test_nan_mean_error():
    MSE = metrics.mean_error(n_true, n_pred, power=2.0)
    assert np.isnan(MSE)

    RMSE = metrics.mean_error(n_true, n_pred, power=2.0, root=True)
    assert np.isnan(RMSE)

def test_zero_nash_sutcliffe_efficiency():
    with pytest.warns(RuntimeWarning):
        NSE = metrics.nash_sutcliffe_efficiency(z_true, z_pred)
        assert np.isnan(NSE)
        
        NNSE = metrics.nash_sutcliffe_efficiency(z_true, z_pred, 
            normalized=True)
        assert np.isnan(NNSE)
       
        NSEL = metrics.nash_sutcliffe_efficiency(np.exp(z_true), 
            np.exp(z_pred), log=True)
        assert np.isnan(NSEL)
        
        NNSEL = metrics.nash_sutcliffe_efficiency(np.exp(z_true), 
            np.exp(z_pred), log=True, normalized=True)
        assert np.isnan(NNSEL)

def test_nan_nash_sutcliffe_efficiency():
    NSE = metrics.nash_sutcliffe_efficiency(n_true, n_pred)
    assert np.isnan(NSE)
    
    NNSE = metrics.nash_sutcliffe_efficiency(n_true, n_pred, 
        normalized=True)
    assert np.isnan(NNSE)
    
    NSEL = metrics.nash_sutcliffe_efficiency(np.exp(n_true), 
        np.exp(n_pred), log=True)
    assert np.isnan(NSEL)
    
    NNSEL = metrics.nash_sutcliffe_efficiency(np.exp(n_true), 
        np.exp(n_pred), log=True, normalized=True)
    assert np.isnan(NNSEL)

def test_kling_gupta_efficiency():
    # Default (inverse case)
    KGE = metrics.kling_gupta_efficiency(y_true, y_pred)
    expected = -1.0
    assert np.isclose(KGE, expected)

    # Half-scale
    KGE = metrics.kling_gupta_efficiency(y_true, np.array(y_true) * 0.5)
    expected = (1.0 - np.sqrt(0.5))
    assert np.isclose(KGE, expected)

    # Double-scale
    KGE = metrics.kling_gupta_efficiency(y_true, np.array(y_true) * 2.0)
    expected = (1.0 - np.sqrt(2.0))
    assert np.isclose(KGE, expected)

    # Identity
    KGE = metrics.kling_gupta_efficiency(y_true, np.array(y_true) * 1.0)
    expected = 1.0
    assert np.isclose(KGE, expected)

    # Scaling parameters
    KGE = metrics.kling_gupta_efficiency(y_true, np.array(y_true) * 0.25,
        r_scale=0.5, a_scale=0.25, b_scale=0.25)
    expected = (1.0 - np.sqrt(9.0/128.0))
    assert np.isclose(KGE, expected)

def test_coefficient_of_persistence():
    # Default
    COP = metrics.coefficient_of_persistence(y_true, y_pred)
    expected = (1.0 - 11.0/3.0)
    assert np.isclose(COP, expected)

    # Test with series
    COP = metrics.coefficient_of_persistence(y_true_series, y_pred_series)
    expected = (1.0 - 11.0/3.0)
    assert np.isclose(COP, expected)

    # Identity
    COP = metrics.coefficient_of_persistence(y_true, np.array(y_true) * 1.0)
    expected = 1.0
    assert np.isclose(COP, expected)

    # Lag
    COP = metrics.coefficient_of_persistence(y_true, y_pred, lag=2)
    expected = -0.25
    assert np.isclose(COP, expected)

    # Power
    COP = metrics.coefficient_of_persistence(y_true, y_pred, power=3)
    expected = (1.0 - 29.0 / 3.0)
    assert np.isclose(COP, expected)

    # Normalized
    COP = metrics.coefficient_of_persistence(y_true, y_pred, normalized=True)
    expected = 1.0 / (2.0 - (1.0 - 11.0/3.0))
    assert np.isclose(COP, expected)

    # Log
    COP = metrics.coefficient_of_persistence(y_true, y_pred, log=True)
    expected = -2.09313723301667
    assert np.isclose(COP, expected)

def test_coefficient_of_extrapolation():
    # Default
    v = [1, 2, 4, 5]
    COE = metrics.coefficient_of_extrapolation(v, y_pred)
    expected = -3.0
    assert np.isclose(COE, expected)

    # Test with series
    s = pd.Series(data=v, index=y_true_series.index)
    COE = metrics.coefficient_of_extrapolation(s, y_pred_series)
    expected = -3.0
    assert np.isclose(COE, expected)

    # Identity
    COE = metrics.coefficient_of_extrapolation(y_true, np.array(y_true) * 1.0)
    expected = 1.0
    assert np.isclose(COE, expected)

    # Power
    COE = metrics.coefficient_of_extrapolation(v, y_pred, power=1.5)
    expected = -1.82842712474619
    assert np.isclose(COE, expected)

    # Normalized
    COE = metrics.coefficient_of_extrapolation(v, y_pred, normalized=True)
    expected = 0.2
    assert np.isclose(COE, expected)

    # Log
    COE = metrics.coefficient_of_extrapolation(v, y_pred, log=True)
    expected = -2.19567503891363
    assert np.isclose(COE, expected)

def test_mean_squared_error():
    MSE = metrics.mean_squared_error(y_true, y_pred)
    assert MSE == 5.0

def test_root_mean_squared_error():
    RMSE = metrics.root_mean_squared_error(y_true, y_pred)
    assert RMSE == np.sqrt(5.0)

def test_volumetric_efficiency():
    VE = metrics.volumetric_efficiency(y_true, y_pred)
    assert np.isclose(VE, 0.2)

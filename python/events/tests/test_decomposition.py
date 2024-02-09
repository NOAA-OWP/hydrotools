import pytest
from hydrotools.events.event_detection import decomposition as ev

import pandas as pd
import numpy as np

def test_list_events():
    # Create trend
    t = np.linspace(1.0, 1001.0, 1000)
    trend = 100.0 * np.exp(-0.002 * t)

    # Create event
    zero_flows = np.zeros(500)
    event_flows = 1000.0 * np.exp(-0.004 * t[:500])
    event_flows = np.concatenate([zero_flows, event_flows])

    # Sum total flow
    flow = trend + event_flows

    # Create streamflow time series
    series = pd.Series(
        flow,
        index=pd.date_range(
            start=pd.to_datetime('2018-01-01'),
            periods=len(t),
            freq='h'),
        name='streamflow'
    )

    # Detect event
    events = ev.list_events(series, '6h', '7D')

    # Should detect a single event
    assert len(events.index) == 1

def test_list_events_noise():
    # Create trend
    t = np.linspace(1.0, 1001.0, 1000)
    trend = 100.0 * np.exp(-0.002 * t)

    # Create event
    zero_flows = np.zeros(500)
    event_flows = 1000.0 * np.exp(-0.004 * t[:500])
    event_flows = np.concatenate([zero_flows, event_flows])

    # Simulate noise
    x = np.linspace(0.0, 334*np.pi, 1000)
    noise = 5.0 * np.sin(x)

    # Sum total flow
    flow = trend + event_flows + noise

    # Create streamflow time series
    series = pd.Series(
        flow,
        index=pd.date_range(
            start=pd.to_datetime('2018-01-01'),
            periods=len(t),
            freq='h'),
        name='streamflow'
    )
    
    # Detect event
    events = ev.list_events(series, '6h', '7D', '6h', '7h')

    # Should detect a single event
    assert len(events.index) == 1

    # Start should have been shifted
    assert events['start'].iloc[0] == pd.Timestamp("2018-01-21 19:00:00")

def test_local_minimum_datetime_exception():
    # Build a series
    series = pd.Series(
        data=[i for i in range(10)],
        index=[i for i in range(10)]
    )

    # Test local minimum
    with pytest.raises(Exception):
        idx = ev.find_local_minimum(
            pd.Timestamp('2020-01-01 01:00'),
            '3h',
            series
        )

def test_origin_not_idx():
    # Build a series
    series = pd.Series(
        data=[i for i in range(10)],
        index=pd.date_range(
            start=pd.to_datetime('2018-01-01'),
            periods=10,
            freq='h'),
        name='streamflow'
    )

    # Test local minimum
    with pytest.raises(Exception):
        idx = ev.find_local_minimum(
            pd.Timestamp('2020-01-01 01:00'),
            '3h',
            series
        )

def test_bad_time_series_idx():
    # Not datetime
    series = pd.Series(
        data=[i for i in range(5)],
        index=[i for i in range(5)]
    )
    with pytest.raises(Exception):
        events = ev.list_events(series, '6h', '7D')

    # Not monotonic
    series = pd.Series(
        data=[i for i in range(5)],
        index=[
            pd.to_datetime('2018-01-01 04:00'),
            pd.to_datetime('2018-01-01 01:00'),
            pd.to_datetime('2018-01-01 02:00'),
            pd.to_datetime('2018-01-01 03:00'),
            pd.to_datetime('2018-01-01 05:00')
        ],
        name='streamflow'
    )
    with pytest.raises(Exception):
        events = ev.list_events(series, '6h', '7D')

    # Duplicated
    series = pd.Series(
        data=[i for i in range(5)],
        index=[
            pd.to_datetime('2018-01-01 00:00'),
            pd.to_datetime('2018-01-01 01:00'),
            pd.to_datetime('2018-01-01 02:00'),
            pd.to_datetime('2018-01-01 03:00'),
            pd.to_datetime('2018-01-01 03:00')
        ],
        name='streamflow'
    )
    with pytest.raises(Exception):
        events = ev.list_events(series, '6h', '7D')

def test_null_warning():
    series = pd.Series(
        data=[1.0, 1.0, np.nan, 1.0, 1.0],
        index=[
            pd.to_datetime('2018-01-01 01:00'),
            pd.to_datetime('2018-01-01 02:00'),
            pd.to_datetime('2018-01-01 03:00'),
            pd.to_datetime('2018-01-01 04:00'),
            pd.to_datetime('2018-01-01 05:00')
        ],
        name='streamflow'
    )
    with pytest.warns(UserWarning):
        events = ev.list_events(series, '6h', '7D')

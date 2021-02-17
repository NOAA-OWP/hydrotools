import pytest
from evaluation_tools.events.event_detection import decomposition as ev

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
            freq='H'),
        name='streamflow'
    )

    # Detect event
    events = ev.list_events(series, '6H', '7D')

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
    x = np.linspace(0.0, 42*np.pi, 1000)
    noise = 25.0 * np.sin(x)

    # Sum total flow
    flow = trend + event_flows + noise

    # Create streamflow time series
    series = pd.Series(
        flow,
        index=pd.date_range(
            start=pd.to_datetime('2018-01-01'),
            periods=len(t),
            freq='H'),
        name='streamflow'
    )
    
    # Detect event
    events = ev.list_events(series, '6H', '7D', '6H')

    # Should detect a single event
    assert len(events.index) == 1

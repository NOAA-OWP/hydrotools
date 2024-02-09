"""
================================
Event Detection :: Decomposition
================================
Use time series decomposition to detect hydrological events in 
streamflow time series as described in Regina & Ogden, 2020.

Regina, J.A., F.L. Ogden, 2020.  Automated Correction of Systematic 
    Errors in High-Frequency Stage Data from V-Notch Weirs using 
    Time Series Decomposition., Under review., Hydrol. Proc.

Functions
---------
rolling_minimum
detrend_streamflow
mark_event_flows
find_local_minimum
event_boundaries
list_events

"""

import numpy as np
import pandas as pd
from typing import Union
import datetime
import warnings

def rolling_minimum(
    series: pd.Series,
    window: Union[int, pd.tseries.offsets.DateOffset, pd.Index]
    ) -> pd.Series:
    """Model the trend in a streamflow time series using a rolling 
        minimum filter. 
        Return the trend of a streamflow time series.
        
        Parameters
        ----------
        series: pandas.Series with a DateTimeIndex, required
            The original streamflow time series.
        window: int, offset, or BaseIndexer subclass, required
            Size of the moving window for `pandas.Series.rolling.min`.
            This filter is used to model the trend in `series`.
            
        Returns
        -------
        trend: pandas.Series
            Approximate baseflow trend of original series.
        
        """
    # Check index
    if not isinstance(series.index, pd.DatetimeIndex):
        raise Exception("series index is not DatetimeIndex")

    # Estimate trend using a forward rolling minimum
    forward = series.rolling(window=window).min()

    # Flip series values to run filter in reverse
    reverse = pd.Series(series.values[::-1], 
        index=series.index)

    # Estimate trend using a backward rolling minimum
    backward = reverse.rolling(window=window).min()

    # Restore reversed series
    backward = pd.Series(backward.values[::-1], 
            index=backward.index)

    # Take the max of the forward and backward trends
    return np.maximum(forward, backward)

def detrend_streamflow(
    series: pd.Series,
    halflife: Union[float, str, pd.Timedelta],
    window: Union[int, pd.tseries.offsets.DateOffset, pd.Index]
    ) -> pd.Series:
    """Model the trend in a streamflow time series using a rolling 
        minimum filter. Remove the trend and residual components. The method 
        aims to produce a detrended time series with a median of 0.0. It assumes 
        any residual components less than twice the detrended median are random 
        noise.
        Return the detrended streamflow time series.
        
        Parameters
        ----------
        series: pandas.Series with a DateTimeIndex, required
            The original streamflow time series.
        halflife: float, str, timedelta, required
            Specifies the decay term for `pandas.Series.ewm.mean`. This filter 
            is used to smooth over interevent noise and reduce detection 
            of normal instrument fluctuations as events.
        window: int, offset, or BaseIndexer subclass, required
            Size of the moving window for `pandas.Series.rolling.min`.
            This filter is used to model the trend in `series`.
            
        Returns
        -------
        detrended: pandas.Series
            New streamflow time series with trend removed.
        
        """
    # Check index
    if type(series.index) != pd.DatetimeIndex:
        raise Exception("series index is not DatetimeIndex")

    if not series.index.is_monotonic_increasing:
        raise Exception("series index is not monotonically increasing")

    if series.index.has_duplicates:
        raise Exception("series index has duplicate timestamps")

    # Check values
    if series.isnull().any():
        warnings.warn("Series contains null values.", UserWarning)

    # Smooth series
    smooth = series.ewm(halflife=halflife, times=series.index, 
        adjust=True).mean()
    
    # Estimate a trend using a rolling minimum
    trend = rolling_minimum(smooth, window)

    # Remove the trend
    detrended = smooth - trend

    # Assume a residual equal to twice the detrended median
    residual = detrended.median() * 2.0

    # Remove the residual
    detrended = detrended - residual

    # Eliminate negative values
    detrended[detrended < 0.0] = 0.0

    # Return detrended series
    return detrended

def event_boundaries(event_points: pd.Series):
    """Return a two column pandas.DataFrame with 'start' and 'end' event times
        generated from a time series of boolean event points.
        
        Parameters
        ----------
        event_points: pandas.Series
            Boolean time series where True indicates the associated value
            in the `series` is part of an event.

        Returns
        -------
        events: pandas.DataFrame
            A two column DataFrame with a row for each event detected. `start` and 
            `end` columns indicate the boundaries of each event.
        
        """
    # Identify event starts
    forward_shift = event_points.shift(1).astype(bool).fillna(False)
    starts = (event_points & ~forward_shift)
    starts = starts[starts]

    # Identify event ends
    backward_shift = event_points.shift(-1).astype(bool).fillna(False)
    ends = (event_points & ~backward_shift)
    ends = ends[ends]

    # Extract times
    return pd.DataFrame({
        'start': starts.index,
        'end': ends.index
    })

def find_local_minimum(
    origin: pd.Timestamp,
    radius: Union[float, str, pd.Timedelta],
    timeseries: pd.Series
    ):
    """Return Datetime of the local minimum value within radius of origin.
        
        Parameters
        ----------
        origin: pandas.Timestamp, required
            The central datetime around which to search.
        radius: float, str, pd.Timedelta, required
            The search radius around origin to look for a minimum value.
        timseries: pandas.Series with a DateTimeIndex, required
            The original time series to inspect.
            
        Returns
        -------
        Index: 
            Datetime of the local minimum value.

    """
    # Check for DatetimeIndex
    if type(timeseries.index) != pd.DatetimeIndex:
        raise Exception("timeseries index is not DatetimeIndex")

    # Check origin is in index
    if origin not in timeseries.index:
        raise Exception("origin is not in index")

    # Define search radius
    radius = pd.Timedelta(radius)

    # Define window
    left = origin - radius
    right = origin + radius

    # Find index of minimum value
    return timeseries.loc[left:right].idxmin()

def mark_event_flows(
    series: pd.Series,
    halflife: Union[float, str, pd.Timedelta],
    window: Union[int, pd.tseries.offsets.DateOffset, pd.Index],
    minimum_event_duration: Union[pd.Timedelta, datetime.timedelta, np.timedelta64, str, int] = '0h',
    start_radius: Union[pd.Timedelta, datetime.timedelta, np.timedelta64, str, int] = '0h'
    ) -> pd.Series:
    """Model the trend in a streamflow time series by taking the max
        of two rolling minimum filters applied in a forward and 
        backward fashion. Remove the trend and residual components. The method 
        aims to produce a detrended time series with a median of 0.0. It assumes 
        any residual components less than twice the detrended median are random 
        noise.
        Return the boolean time series that indicates whether an 
        individual value in the original streamflow time series
        is part of an event (True) or not part of an event (False).
        
        Parameters
        ----------
        series: pandas.Series with a DateTimeIndex, required
            The original streamflow time series.
        halflife: float, str, timedelta, required
            Specifies the decay term for `pandas.Series.ewm.mean`. This filter 
            is used to smooth over interevent noise and reduce detection 
            of normal instrument fluctuations as events.
        window: int, offset, or BaseIndexer subclass, required
            Size of the moving window for `pandas.Series.rolling.min`.
            This filter is used to model the trend in `series`.
        minimum_event_duration: pandas.Timedelta, datetime.timedelta, numpy.timedelta64, str, int, optional, default '0h'
            Enforce a minimum event duration. This should generally be set equal to 
            halflife to reduce the number of false positives flagged as events.
        start_radius: pandas.Timedelta, datetime.timedelta, numpy.timedelta64, str, int, optional, default '0h'
            Shift event starts to a local minimum. Phase shifts imparted on the 
            original signal may advance or delay event start times depending upon how 
            much smoothing is required to eliminate noise.
            
        Returns
        -------
        event_points: pandas.Series
            Boolean time series where True indicates the associated value
            in the `series` is part of an event.
        
        """
    # Detrend with a minimum filter
    detrended = detrend_streamflow(series, halflife, window)
    
    # Generate mask of non-zero detrended flows
    event_points = pd.Series((detrended > 0.0), index=series.index)

    # Do not filter events
    minimum_event_duration = pd.Timedelta(minimum_event_duration)
    start_radius = pd.Timedelta(start_radius)
    if (minimum_event_duration == pd.Timedelta(0)) & (start_radius == pd.Timedelta(0)):
        # Return mask of non-zero detrended flows
        return event_points

    # Get list of potential events
    events = event_boundaries(event_points)

    # Filter by duration
    if minimum_event_duration != pd.Timedelta(0):
        # Compute duration
        durations = events['end'].sub(events['start'])

        # Filter events
        events = events[durations >= minimum_event_duration].reset_index(drop=True)

    # Adjust event starts
    if start_radius != pd.Timedelta(0):
        # Adjust
        events['start'] = events['start'].apply(find_local_minimum, 
            radius=start_radius, timeseries=series)
    
    # Refine event points
    filtered_event_points = pd.Series(data=False, index=event_points.index)
    for e in events.itertuples():
        filtered_event_points.loc[e.start:e.end] = True
    
    # Return filtered event points
    return filtered_event_points

def list_events(
    series: pd.Series,
    halflife: Union[float, str, pd.Timedelta],
    window: Union[int, pd.tseries.offsets.DateOffset, pd.Index],
    minimum_event_duration: Union[pd.Timedelta, datetime.timedelta, np.timedelta64, str, int] = '0h',
    start_radius: Union[pd.Timedelta, datetime.timedelta, np.timedelta64, str, int] = '0h'
    ) -> pd.DataFrame:
    """Apply time series decomposition to mark event values in a streamflow
        time series. Discretize continuous event values into indiviual events.
        Return a DataFrame with one row for each event detected with `start` and 
        `end` columns indicating the boundaries of each event.
        
        Parameters
        ----------
        series: pandas.Series with a DateTimeIndex, required
            The original streamflow time series.
        halflife: float, str, timedelta, required
            Specifies the decay term for `pandas.Series.ewm.mean`. This filter 
            is used to smooth over interevent noise and reduce detection 
            of normal instrument fluctuations as events.
        window: int, offset, or BaseIndexer subclass, required
            Size of the moving window for `pandas.Series.rolling.min`.
            This filter is used to model the trend in `series`.
        minimum_event_duration: pandas.Timedelta, datetime.timedelta, numpy.timedelta64, str, int, optional, default '0h'
            Enforce a minimum event duration. This should generally be set equal to 
            halflife to reduce the number of false positives flagged as events.
        start_radius: pandas.Timedelta, datetime.timedelta, numpy.timedelta64, str, int, optional, default '0h'
            Shift event starts to a local minimum. Phase shifts imparted on the 
            original signal may advance or delay event start times depending upon how 
            much smoothing is required to eliminate noise.
            
        Returns
        -------
        events: pandas.DataFrame
            A two column DataFrame with a row for each event detected. `start` and 
            `end` columns indicate the boundaries of each event.
        
        """
    # Detect event flows
    event_points = mark_event_flows(series, halflife, window, 
        minimum_event_duration, start_radius)

    # Return events
    return event_boundaries(event_points)

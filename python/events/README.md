# HydroTools :: Events

This subpackage implements methods to partition hydrometric times series into discrete "events." See the [Events Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.events.event_detection.html) for a complete list and description of the currently available methods. To report bugs or request new methods, submit an issue through the [HydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

## Installation

In accordance with the python community, we support and advise the usage of virtual
environments in any workflow using python. In the following installation guide, we
use python's built-in `venv` module to create a virtual environment in which the
tool will be installed. Note this is just personal preference, any python virtual
environment manager should work just fine (`conda`, `pipenv`, etc. ).

```bash
# Create and activate python environment, requires python >= 3.8
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip

# Install events
$ python3 -m pip install hydrotools.events
```

## Usage

The following example demonstrates how one might use `hydrotools.events.event_detection` to extract hydrological events from a time series of real streamflow measurements. This example requires the `hydrotools.nwis_client` package.

### Code
```python
# Import tools to retrieve data and detect events
from hydrotools.nwis_client.iv import IVDataService
from hydrotools.events.event_detection import decomposition as ev

# Use pandas to resample the data
from pandas import Grouper

# Use a helper function to detect events at multiple sites
def list_events_helper(mi_series, level, halflife, window):
    """Reduce multi-index series before applying event detection."""
    return ev.list_events(mi_series.droplevel(level), halflife, window)

# Retrieve streamflow observations for two sites
observations = IVDataService.get(
    sites='02146750,0214676115,09489000', 
    startDT='2019-10-01', 
    endDT='2020-09-30'
    )

# Drop extra columns to be more efficient
observations = observations[[
    'usgs_site_code', 
    'value_date', 
    'value'
    ]]

# Check for duplicate time series, keep first by default
observations = observations.drop_duplicates(
    subset=['usgs_site_code', 'value_date']
    )

# Resample to hourly, keep first measurement in each 1-hour bin
observations = observations.groupby([
    'usgs_site_code',
    Grouper(key='value_date', freq='H')
    ]).first().ffill()

# Detect events
events = observations['value'].groupby(
    level='usgs_site_code').apply(
        list_events_helper, 
        level='usgs_site_code', 
        halflife='6H', 
        window='7D'
    )

# Print event list    
print(events)
```

### Output
```console
                                start                 end
usgs_site_code                                           
02146750       0  2019-10-13 22:00:00 2019-10-15 04:00:00
               1  2019-10-16 09:00:00 2019-10-18 02:00:00
               2  2019-10-19 03:00:00 2019-10-23 19:00:00
               3  2019-10-27 05:00:00 2019-10-28 18:00:00
               4  2019-10-30 01:00:00 2019-11-02 18:00:00
...                               ...                 ...
09489000       34 2020-09-16 00:00:00 2020-09-16 19:00:00
               35 2020-09-17 00:00:00 2020-09-17 15:00:00
               36 2020-09-18 04:00:00 2020-09-18 10:00:00
               37 2020-09-27 01:00:00 2020-09-27 03:00:00
               38 2020-09-28 05:00:00 2020-09-28 11:00:00
```

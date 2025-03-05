# OWPHydroTools :: Metrics

This subpackage implements common evaluation metrics used in hydrological model validation and forecast verification. See the [Metrics Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.metrics.html) for a complete list and description of the currently available metrics. To request more metrics, submit an issue through the [OWPHydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

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

# Install metrics
$ python3 -m pip install hydrotools.metrics
```

## Evaluation Metrics

The following example demonstrates how one might use `hydrotools.metrics` to compute a Threat Score, also called the Critical Success Index, by comparing a persistence forecast to USGS streamflow observations. This example also requires the `hydrotools.nwis_client` package.

### Example Usage
```python
from hydrotools.metrics import metrics
from hydrotools.nwis_client.iv import IVDataService
import pandas as pd

# Get observed data
service = IVDataService()
observed = service.get(
    sites='01646500',
    startDT='2020-01-01',
    endDT='2021-01-01'
    )

# Preprocess data
observed = observed[['value_time', 'value']]
observed = observed.drop_duplicates(['value_time'])
observed = observed.set_index('value_time')

# Simulate a 10-day persistence forecast
issue_frequency = pd.Timedelta('6H')
forecast_length = pd.Timedelta('10D')
forecasts = observed.resample(issue_frequency).nearest()
forecasts = forecasts.rename(columns={"value": "sim"})

# Find observed maximum during forecast period
values = []
for idx, sim in forecasts.itertuples():
    obs = observed.loc[idx:idx+forecast_length, "value"].max()
    values.append(obs)
forecasts["obs"] = values

# Apply flood criteria using a "Hit Window" approach
#  A flood is observed or simluated if any value within the
#  forecast_length meets or exceeds the flood_criteria
# 
# Apply flood_criteria to forecasts
flood_criteria = 19200.0
forecasts['simulated_flood'] = (forecasts['sim'] >= flood_criteria)
forecasts['observed_flood'] = (forecasts['obs'] >= flood_criteria)

# Compute contingency table
contingency_table = metrics.compute_contingency_table(
    forecasts['observed_flood'],
    forecasts['simulated_flood']
)
print('Contingency Table Components')
print('============================')
print(contingency_table)

# Compute threat score/critical success index
TS = metrics.threat_score(contingency_table)
print('Threat Score: {:.2f}'.format(TS))
```

### Output
```console
Contingency Table Components
============================
true_positive      148
false_positive       0
false_negative     194
true_negative     1123
dtype: int64
Threat Score: 0.43
```

## Event Metrics

The `hydrotools.metrics.events` module contains simple methods for computing common event-scale metrics. The module currently includes `peak`, `flashiness`, and `runoff_ratio`. See the documentation for more information on each of these metrics.

### Example Usage

The following example demonstrates how to compute peak, flashiness, and runoff ratio on an event basis. For the purposes of this analysis, "event" refers to a discrete period of time during which a significant portion of a hydrograph is attributable to rainfall-driven runoff, also called stormflow. The techniques demonstrated rely on a number of hydrophysical assumptions. Generally, these types of events are more easily decomposed from hydrographs of catchments with relatively small drainage areas. Smaller basins make it more likely that a particular instance of rainfall can be associated with a particular period of the hydrograph where streamflow rises above and eventually returns to baseflow. The Eckardt method of baseflow separation further assumes that baseflow linearly recedes as a function of storage. Violation of these assumptions does not necessarily invalidate an analysis on the basis of "events," but will contribute to the uncertainty of the results.

This example requires the `hydrotools.nwis_client` and `hydrotools.events` packages.

```python
# Import tools to retrieve data and detect events
from hydrotools.nwis_client.iv import IVDataService
from hydrotools.events.baseflow import eckhardt as bf
from hydrotools.events.event_detection import decomposition as ev
import hydrtools.metrics.events as emet

# Retrieve streamflow observations and precipitation
service = IVDataService()
streamflow = service.get(
    sites="02146750",
    startDT="2023-10-01",
    endDT="2024-09-30"
    )
precipitation = service.get(
    sites="351104080521845",
    startDT="2023-10-01",
    endDT="2024-09-30",
    parameterCd="00045"
    )

# Drop extra columns to be more efficient
streamflow = streamflow[[
    "value_time", 
    "value"
    ]]
precipitation = precipitation[[
    "value_time", 
    "value"
    ]]

# Check for duplicate times, keep first by default, index by datetime
streamflow = streamflow.drop_duplicates(
    subset=["value_time"]
    ).set_index("value_time")
precipitation = precipitation.drop_duplicates(
    subset=["value_time"]
    ).set_index("value_time")

# Convert streamflow to hourly mean
streamflow = streamflow.resample("1h").mean().ffill()

# Perform baseflow separation on hourly time series
#  Note this method assumes baseflow recedes linearly as a function of
#  storage. Nonlinearities can arise due to seasonal effects, snowpack,
#  karst, land surface morphology, and other factors.
results = bf.separate_baseflow(
    streamflow["value"],
    output_time_scale = "1h",
    recession_time_scale = "12h"
    )
streamflow["baseflow"] = results.values
streamflow["direct_runoff"] = streamflow["value"].sub(
    streamflow["baseflow"])

# Convert streamflow to runoff inches accumulated per hour
drainage_area = 2.63 # sq. mi.
streamflow = streamflow * 3.0 / (drainage_area * 1936.0)

# Find event periods
events = ev.list_events(
    streamflow["value"],
    halflife="6h",
    window="7d"
)

# We'll use a buffer to accumulate precipitation before the hydrograph rise
events["buffer"] = (events["end"] - events["start"]) * 0.5

# Compute event metrics
events["peak"] = events.apply(
    lambda e: emet.peak(streamflow.loc[e.start:e.end, "value"]), axis=1)
events["flashiness"] = events.apply(
    lambda e: emet.flashiness(streamflow.loc[e.start:e.end, "value"]),
    axis=1)
events["runoff_ratio"] = events.apply(
    lambda e: emet.runoff_ratio(
        streamflow.loc[e.start:e.end, "direct_runoff"],
        precipitation.loc[e.start-e.buffer:e.end, "value"]), axis=1)

# Limit to events with physically consistent runoff ratios
#  This catchment is highly urbanized, so assumptions about baseflow
#  separation may not always apply.
print(events.query("runoff_ratio <= 1.0"))
```

### Output

```console
                 start                 end          buffer      peak  flashiness  runoff_ratio
0  2023-10-12 21:00:00 2023-10-14 03:00:00 0 days 15:00:00  0.016056    0.050381      0.705256
27 2024-06-03 07:00:00 2024-06-04 15:00:00 0 days 16:00:00  0.050033    0.055212      0.866002
39 2024-08-20 01:00:00 2024-08-21 11:00:00 0 days 17:00:00  0.054933    0.089661      0.960850
```

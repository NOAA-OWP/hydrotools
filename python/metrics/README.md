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

## Usage

The following example demonstrates how one might use `hydrotools.metrics` to compute a Threat Score, also called the Critical Success Index, by comparing a persistence forecast to USGS streamflow observations. This example also requires the `hydrotools.nwis_client` package.

### Code
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

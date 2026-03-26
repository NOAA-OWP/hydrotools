# OWPHydroTools :: WaterData Client

This subpackage implements an interface to the USGS [WaterData APIs](https://api.waterdata.usgs.gov/). The primary use for this tool is to populate `pandas.Dataframe` objects with USGS streamflow data. See the [WaterData Client Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.water_data.html) for a complete list and description of the currently available methods. To report bugs or request new features, submit an issue through the [OWPHydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

## Installation

In accordance with the python community, we support and advise the usage of virtual
environments in any workflow using python. In the following installation guide, we
use python's built-in `venv` module to create a virtual environment in which the
tool will be installed. Note this is just personal preference, any python virtual
environment manager should work just fine (`conda`, `pipenv`, etc. ).

```bash
# Create and activate python environment, requires python >= 3.11
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip

# Install waterdata_client
$ python3 -m pip install hydrotools.waterdata_client
```

## Usage

The following example demonstrates how one might use `hydrotools.waterdata_client` to retrieve USGS streamflow observations.

### Code

```python
# Import the WaterData Client
from hydrotools.waterdata_client import ContinuousClient

# Retrieve data from a single site
service = ContinuousClient(
    value_time_label="value_time"
)
observations_data = service.get(
    sites='01646500',
    startDT='2019-08-01',
    endDT='2020-08-01'
    )

# Look at the data
print(observations_data.head())
```

### Output

```console
           value_date variable_name usgs_site_code measurement_unit   value qualifiers  series
0 2019-08-01 04:00:00    streamflow       01646500            ft3/s  4170.0        [A]       0
1 2019-08-01 04:15:00    streamflow       01646500            ft3/s  4170.0        [A]       0
2 2019-08-01 04:30:00    streamflow       01646500            ft3/s  4170.0        [A]       0
3 2019-08-01 04:45:00    streamflow       01646500            ft3/s  4170.0        [A]       0
4 2019-08-01 05:00:00    streamflow       01646500            ft3/s  4170.0        [A]       0
```

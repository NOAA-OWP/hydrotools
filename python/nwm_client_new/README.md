# OWPHydroTools :: NWM Client New

This subpackage implements various interfaces to retrieve National Water Model (NWM) data from various sources including Google Cloud Platform, NOMADS, local directories, or a generic web server directory listing. The primary use for this tool is to populate `pandas.Dataframe` objects with NWM streamflow data. See the [NWM Client New Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.nwm_client_new.html) for a complete list and description of the currently available methods. To report bugs or request new features, submit an issue through the [OWPHydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

## Installation

In accordance with the python community, we support and advise the usage of virtual
environments in any workflow using python. In the following installation guide, we
use python's built-in `venv` module to create a virtual environment in which the
tool will be installed. Note this is just personal preference, any python virtual
environment manager should work just fine (`conda`, `pipenv`, etc. ).

```bash
# Create and activate python environment, requires python >= 3.8
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install --upgrade pip wheel

# Install nwm_client_new
$ python3 -m pip install hydrotools.nwm_client_new
```

## Usage

The following example demonstrates how one might use `hydrotools.nwm_client_new` to retrieve NWM streamflow forecasts.

### Code
```python
# Import the nwm Client
from hydrotools.nwm_client_new.NWMFileClient import NWMFileClient
import pandas as pd

# Instantiate model data client
#  Defaults to Google Cloud Platform
client = NWMFileClient()

# Set reference time
yesterday = pd.Timestamp.utcnow() - pd.Timedelta("1D")
reference_time = yesterday.strftime("%Y%m%dT%-HZ")

# Retrieve forecast data
#  By default, only retrieves data at USGS gaging sites in
#  CONUS that are used for model assimilation
forecast_data = client.get(
    configuration = "short_range",
    reference_times = [reference_time]
    )

# Look at the data
print(forecast_data.info(memory_usage='deep'))
print(forecast_data[['value_time', 'value']].head())
```
### Example output
```console
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 137628 entries, 0 to 137627
Data columns (total 8 columns):
 #   Column            Non-Null Count   Dtype         
---  ------            --------------   -----         
 0   reference_time    137628 non-null  datetime64[ns]
 1   value_time        137628 non-null  datetime64[ns]
 2   nwm_feature_id    137628 non-null  int64         
 3   value             137628 non-null  float32       
 4   usgs_site_code    137628 non-null  category      
 5   configuration     137628 non-null  category      
 6   measurement_unit  137628 non-null  category      
 7   variable_name     137628 non-null  category      
dtypes: category(4), datetime64[ns](2), float32(1), int64(1)
memory usage: 5.1 MB
None
           value_time  value
0 2021-01-01 02:00:00   5.29
1 2021-01-01 03:00:00   5.25
2 2021-01-01 04:00:00   5.20
3 2021-01-01 05:00:00   5.12
4 2021-01-01 06:00:00   5.03
```

## Development

This package uses a setup configuration file (`setup.cfg`) and assumes use of the `setuptools` backend to build the package. To install the package for development use:
```bash
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install -U pip
$ python3 -m pip install -U setuptools
$ python3 -m pip install -e .[develop]
```

To generate a source distribution:
```bash
$ python3 -m pip install -U wheel build
$ python3 -m build
```

The packages generated in `dist/` can be installed directly with `pip` or uploaded to PyPI using `twine`.

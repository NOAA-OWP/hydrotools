# HydroTools :: Utilities

This subpackage implements an various methods commonly used by other `hydrotools` packages. A list of current utilities is given below. See the [Utilities Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.utilities.html) for a complete list and description of the currently available methods. To report bugs or request new features, submit an issue through the [HydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

## List of Utility Modules

1. `stock_dataframes`
2. `hdf_cache`

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

# Install utilities
$ python3 -m pip install hydrotools.utilities
```

## Usage

The following example demonstrates how one might use `hydrotools.utilities` to generate random `DataFrame` and cache `DataFrame` results for later retrieval.

### Code
```python
# Import the Utilities
from hydrotools.gcp_client import gcp

# Instantiate model data service
model_data_service = gcp.NWMDataService()

# Retrieve forecast data
#  By default, only retrieves data at USGS gaging sites in
#  CONUS that are used for model assimilation
forecast_data = model_data_service.get(
    configuration = "short_range",
    reference_time = "20210101T01Z"
    )

# Look at the data
print(forecast_data.info(memory_usage='deep'))
print(forecast_data[['valid_time', 'value']].head())
```
### Output
```console
<class 'pandas.core.frame.DataFrame'>
Int64Index: 135738 entries, 0 to 135737
Data columns (total 8 columns):
 #   Column            Non-Null Count   Dtype         
---  ------            --------------   -----         
 0   nwm_feature_id    135738 non-null  category      
 1   reference_time    135738 non-null  datetime64[ns]
 2   valid_time        135738 non-null  datetime64[ns]
 3   value             135720 non-null  float32       
 4   usgs_site_code    135738 non-null  category      
 5   configuration     135738 non-null  category      
 6   measurement_unit  135738 non-null  category      
 7   variable_name     135738 non-null  category      
dtypes: category(5), datetime64[ns](2), float32(1)
memory usage: 6.0 MB
None
           valid_time      value
0 2021-01-01 02:00:00  16.940001
1 2021-01-01 03:00:00  25.570000
2 2021-01-01 04:00:00  37.590000
3 2021-01-01 05:00:00  52.279999
4 2021-01-01 06:00:00  67.869995
```

# HydroTools :: GCP Client

This subpackage implements an interface to the retrieve National Water Model (NWM) data from [Google Cloud Platform](https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model). The primary use for this tool is to populate `pandas.Dataframe` objects with NWM streamflow data. See the [GCP Client Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.gcp_client.html) for a complete list and description of the currently available methods. To report bugs or request new features, submit an issue through the [HydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

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

# Install nwis_client
$ python3 -m pip install hydrotools.nwis_client
```

## Usage

The following example demonstrates how one might use `hydrotools.gcp_client` to retrieve NWM streamflow forecasts.

### Code
```python
# Import the GCP Client
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
print(forecast_data.head())
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
### System Requirements
We employ several methods to make sure the resulting `pandas.DataFrame` produced by `gcp_client` are as efficient and manageable as possible. Nonetheless, this package can potentially use a large amount of memory.

The National Water Model generates multiple forecasts per day at over 2.7 million locations across the United States. A single forecast could be spread across hundreds of files and require repeated calls to Google Cloud Platform. The intermediate steps of retrieving and processing these files into leaner `DataFrame` may use several GB of memory. As such, recommended minimum requirements to use this package are a 4-core consumer processor and 8 GB of RAM.
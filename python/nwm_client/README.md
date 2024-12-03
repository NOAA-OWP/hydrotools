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

# Install nwm_client
$ python3 -m pip install hydrotools.nwm_client_new
```

## Usage

The following example demonstrates how one might use `hydrotools.nwm_client_new` to retrieve NWM streamflow forecasts.

### Code

<details><summary><b>View compatible configurations</b></summary>

```python
# Import the NWM Client
from hydrotools.nwm_client_new.NWMFileClient import NWMFileClient

# Instantiate model data client
model_data_client = NWMFileClient()

# Print compatible model configurations
#  Note that not all data sources contain the full range of available 
#  National Water Model data. This client defaults to Google Cloud Platform
#  Which has the largest amount of *operational* forecast data.
#  Also note that not all configurations are available for the entire
#  archive of NWM operational forecast data. For example, the configurations 
#  for Alaska only became available after August 2023.
print(model_data_client.catalog.configurations)
```
### Example output
```console
['analysis_assim', 'analysis_assim_alaska', 'analysis_assim_alaska_no_da', 'analysis_assim_extend', 'analysis_assim_extend_no_da', 'analysis_assim_extend_alaska', 'analysis_assim_extend_alaska_no_da', 'analysis_assim_hawaii', 'analysis_assim_hawaii_no_da', 'analysis_assim_no_da', 'analysis_assim_puertorico', 'analysis_assim_puertorico_no_da', 'analysis_assim_long', 'analysis_assim_long_no_da', 'long_range_mem1', 'long_range_mem2', 'long_range_mem3', 'long_range_mem4', 'medium_range_alaska_mem1', 'medium_range_alaska_mem2', 'medium_range_alaska_mem3', 'medium_range_alaska_mem4', 'medium_range_alaska_mem5', 'medium_range_alaska_mem6', 'medium_range_alaska_no_da', 'medium_range_mem1', 'medium_range_mem2', 'medium_range_mem3', 'medium_range_mem4', 'medium_range_mem5', 'medium_range_mem6', 'medium_range_mem7', 'medium_range_no_da', 'short_range', 'short_range_alaska', 'short_range_hawaii', 'short_range_hawaii_no_da', 'short_range_puertorico', 'short_range_puertorico_no_da']
```

</details>

<details><summary><b>Retrieving data from google cloud</b></summary>

```python
# Import the NWM Client
from hydrotools.nwm_client_new.NWMFileClient import NWMFileClient

# Instantiate model data client
#  By default, NWM values are in SI units
#  If you prefer US standard units, nwm_client can return
#  values in US standard units by setting the unit_system parameter 
#  to MeasurementUnitSystem.US
# 
# from hydrotools.nwm_client_new.NWMClientDefaults import MeasurementUnitSystem
# model_data_client = NWMFileClient(unit_system=MeasurementUnitSystem.US)
model_data_client = NWMFileClient()

# Retrieve forecast data
forecast_data = model_data_client.get(
    configurations = ["short_range"],
    reference_times = ["20210101T01Z"],
    nwm_feature_ids = [724696]
    )

# Look at the data
print(forecast_data.head())
```
### Example output
```console
       reference_time  nwm_feature_id          value_time      value measurement_unit variable_name configuration usgs_site_code
0 2021-01-01 01:00:00          724696 2021-01-01 02:00:00  56.340000           m3 s-1    streamflow   short_range       01013500
1 2021-01-01 01:00:00          724696 2021-01-01 17:00:00  56.090000           m3 s-1    streamflow   short_range       01013500
2 2021-01-01 01:00:00          724696 2021-01-01 16:00:00  56.119999           m3 s-1    streamflow   short_range       01013500
3 2021-01-01 01:00:00          724696 2021-01-01 15:00:00  56.149998           m3 s-1    streamflow   short_range       01013500
4 2021-01-01 01:00:00          724696 2021-01-01 14:00:00  56.180000           m3 s-1    streamflow   short_range       01013500
```

</details>

<details><summary><b>Retrieving data from Azure Blob Storage</b></summary>

```python
# Import the NWM Client
from hydrotools.nwm_client_new.NWMFileClient import NWMFileClient
from hydrotools.nwm_client_new.AzureFileCatalog import AzureFileCatalog
import pandas as pd

# Instantiate model data client
catalog = AzureFileCatalog()
model_data_client = NWMFileClient(catalog=catalog)

# Set reference time
yesterday = pd.Timestamp.utcnow() - pd.Timedelta("1D")

# Retrieve forecast data
forecast_data = model_data_client.get(
    configurations = ["short_range"],
    reference_times = [yesterday],
    nwm_feature_ids = [724696]
    )

# Look at the data
print(forecast_data.head())
```
### Example output
```console
       reference_time  nwm_feature_id          value_time      value measurement_unit variable_name configuration usgs_site_code
0 2022-08-07 18:00:00          724696 2022-08-07 19:00:00  20.369999           m3 s-1    streamflow   short_range       01013500
1 2022-08-07 18:00:00          724696 2022-08-08 10:00:00  24.439999           m3 s-1    streamflow   short_range       01013500
2 2022-08-07 18:00:00          724696 2022-08-08 09:00:00  24.469999           m3 s-1    streamflow   short_range       01013500
3 2022-08-07 18:00:00          724696 2022-08-08 08:00:00  24.490000           m3 s-1    streamflow   short_range       01013500
4 2022-08-07 18:00:00          724696 2022-08-08 07:00:00  24.510000           m3 s-1    streamflow   short_range       01013500
```

</details>

<details><summary><b>Retrieving data from Nomads</b></summary>

```python
# Import the NWM Client
from hydrotools.nwm_client_new.NWMFileClient import NWMFileClient
from hydrotools.nwm_client_new.HTTPFileCatalog import HTTPFileCatalog
import pandas as pd

# Instantiate model data client
catalog = HTTPFileCatalog("https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/")
model_data_client = NWMFileClient(catalog=catalog)

# Set reference time
yesterday = pd.Timestamp.utcnow() - pd.Timedelta("1D")

# Retrieve forecast data
forecast_data = model_data_client.get(
    configurations = ["short_range"],
    reference_times = [yesterday],
    nwm_feature_ids = [724696]
    )

# Look at the data
print(forecast_data.head())
```
### Example output
```console
       reference_time  nwm_feature_id          value_time      value measurement_unit variable_name configuration usgs_site_code
0 2022-08-07 18:00:00          724696 2022-08-07 19:00:00  20.369999           m3 s-1    streamflow   short_range       01013500
1 2022-08-07 18:00:00          724696 2022-08-08 10:00:00  24.439999           m3 s-1    streamflow   short_range       01013500
2 2022-08-07 18:00:00          724696 2022-08-08 09:00:00  24.469999           m3 s-1    streamflow   short_range       01013500
3 2022-08-07 18:00:00          724696 2022-08-08 08:00:00  24.490000           m3 s-1    streamflow   short_range       01013500
4 2022-08-07 18:00:00          724696 2022-08-08 07:00:00  24.510000           m3 s-1    streamflow   short_range       01013500
```

</details>

<details><summary><b>Retrieving data from a private file server</b></summary>

```python
# Import the NWM Client
from hydrotools.nwm_client_new.NWMFileClient import NWMFileClient
from hydrotools.nwm_client_new.HTTPFileCatalog import HTTPFileCatalog
from hydrotools.nwm_client_new.NWMClientDefaults import MeasurementUnitSystem
import ssl

# Create ssl context
context = ssl.create_default_context(cafile="/path/to/my/ca-bundle.crt")

# Instantiate model data client
catalog = HTTPFileCatalog(
    "https://path-to-my-private-server.com/nwm/2.2/", 
    ssl_context=context
    )
model_data_client = NWMFileClient(
    catalog=catalog,
    unit_system=MeasurementUnitSystem.US,
    ssl_context=context
)

# Retrieve forecast data
forecast_data = model_data_client.get(
    configurations = ["short_range"],
    reference_times = ["2022-06-01T13"],
    nwm_feature_ids = [724696]
    )

# Look at the data
print(forecast_data.head())
```
### Example output
```console
       reference_time  nwm_feature_id          value_time        value measurement_unit variable_name configuration usgs_site_code
0 2022-06-01 13:00:00          724696 2022-06-01 14:00:00  3586.910645           ft^3/s    streamflow   short_range       01013500
1 2022-06-01 13:00:00          724696 2022-06-02 05:00:00  2167.260986           ft^3/s    streamflow   short_range       01013500
2 2022-06-01 13:00:00          724696 2022-06-02 04:00:00  2168.673584           ft^3/s    streamflow   short_range       01013500
3 2022-06-01 13:00:00          724696 2022-06-02 03:00:00  2172.558350           ft^3/s    streamflow   short_range       01013500
4 2022-06-01 13:00:00          724696 2022-06-02 02:00:00  2177.855469           ft^3/s    streamflow   short_range       01013500
```

</details>

### System Requirements
We employ several methods to make sure the resulting `pandas.DataFrame` produced by `nwm_client` are as efficient and manageable as possible. Nonetheless, this package can potentially use a large amount of memory.

The National Water Model generates multiple forecasts per day at over 3.7 million locations across the United States. A single forecast could be spread across hundreds of files and require repeated calls to the data source. The intermediate steps of retrieving and processing these files into leaner `DataFrame` may use several GB of memory. As such, recommended minimum requirements to use this package are a 4-core consumer processor and 8 GB of RAM.

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

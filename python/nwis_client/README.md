# OWPHydroTools :: NWIS Client

This subpackage implements an interface to the USGS NWIS [Instantaneous Values Web Service](https://waterservices.usgs.gov/rest/IV-Service.html). The primary use for this tool is to populate `pandas.Dataframe` objects with USGS streamflow data. See the [NWIS Client Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.nwis_client.html) for a complete list and description of the currently available methods. To report bugs or request new features, submit an issue through the [OWPHydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

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

The following example demonstrates how one might use `hydrotools.nwis_client` to retrieve USGS streamflow observations.

### Code

```python
# Import the NWIS IV Client
from hydrotools.nwis_client.iv import IVDataService

# Retrieve data from a single site
service = IVDataService(
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

### Command Line Interface (CLI)
The `hydrotools.nwis_client` package includes a command-line utility.

This example demonstrates calling the help page:
```bash
$ nwis-client --help
```
```console
Usage: nwis-client [OPTIONS] [SITES]...

  Retrieve data from the USGS IV Web Service API and write in CSV format.

  Example:

  nwis-client 01013500 02146470

Options:
  -o, --output FILENAME       Output file path
  -s, --startDT TIMESTAMP     Start datetime
  -e, --endDT TIMESTAMP       End datetime
  -p, --parameterCd TEXT      Parameter code
  --comments / --no-comments  Enable/disable comments in output, enabled by
                              default
  --header / --no-header      Enable/disable header in output, enabled by
                              default
  --help                      Show this message and exit.
```

This example retrieves the last discharge value from two sites:
```bash
$ nwis-client 01013500 02146470
```
```console
# USGS IV Service Data
# 
# value_date: Datetime of measurement (UTC) (character string)
# variable: USGS variable name (character string)
# usgs_site_code: USGS Gage Site Code (character string)
# measurement_unit: Units of measurement (character string)
# value: Measurement value (float)
# qualifiers: Qualifier string (character string)
# series: Series number in case multiple time series are returned (integer)
# 
# Generated at 2022-03-04 21:56:30.296051+00:00
# nwis_client version: 3.2.0
# Source code: https://github.com/NOAA-OWP/hydrotools
# 
value_time,variable_name,usgs_site_code,measurement_unit,value,qualifiers,series
2022-03-04 21:45:00,streamflow,01013500,ft3/s,-999999.00,"['P', 'Ice']",0
2022-03-04 21:50:00,streamflow,02146470,ft3/s,1.04,['P'],0
```

This example retrieves stage data from two sites for a specific time period:
```bash
$ nwis-client -p 00065 -s 2021-06-01T00:00 -e 2021-06-01T01:00 01013500 02146470
```
```console
# USGS IV Service Data
# 
# value_date: Datetime of measurement (UTC) (character string)
# variable: USGS variable name (character string)
# usgs_site_code: USGS Gage Site Code (character string)
# measurement_unit: Units of measurement (character string)
# value: Measurement value (float)
# qualifiers: Qualifier string (character string)
# series: Series number in case multiple time series are returned (integer)
# 
# Generated at 2022-03-04 21:59:02.508468+00:00
# nwis_client version: 3.2.0
# Source code: https://github.com/NOAA-OWP/hydrotools
# 
value_time,variable_name,usgs_site_code,measurement_unit,value,qualifiers,series
2021-05-31 23:00:00,gage height,01013500,ft,4.28,['A'],0
2021-05-31 23:15:00,gage height,01013500,ft,4.28,['A'],0
2021-05-31 23:30:00,gage height,01013500,ft,4.28,['A'],0
2021-05-31 23:45:00,gage height,01013500,ft,4.28,['A'],0
2021-06-01 00:00:00,gage height,01013500,ft,4.28,['A'],0
2021-05-31 23:00:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:05:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:10:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:15:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:20:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:25:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:30:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:35:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:40:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:45:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:50:00,gage height,02146470,ft,3.14,['A'],0
2021-05-31 23:55:00,gage height,02146470,ft,3.14,['A'],0
2021-06-01 00:00:00,gage height,02146470,ft,3.14,['A'],0
```

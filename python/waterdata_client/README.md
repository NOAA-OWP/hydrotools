# OWPHydroTools :: WaterData Client

This subpackage implements an interface to the USGS [WaterData APIs](https://api.waterdata.usgs.gov/). The primary use for this tool is to populate `pandas.Dataframe` objects with USGS streamflow data. See the [WaterData Client Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.waterdata_client.html) for a complete list and description of the currently available methods. To report bugs or request new features, submit an issue through the [OWPHydroTools Issue Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

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
# Import client and geopandas for easy parsing
import geopandas as gpd
from hydrotools.waterdata_client import LatestContinuousClient

# Instantiate client
client = LatestContinuousClient()

# Retrieve data
data = client.get(
    monitoring_location_id="USGS-02146470"
    )

# Look at values
observations = gpd.GeoDataFrame.from_features(data[0])
print(observations)
print(observations.columns)
```

### Output

```console
                     geometry                                    id                    time_series_id  ... approval_status qualifier                     last_modified
0  POINT (-80.85306 35.16444)  1b39aa0f-6adb-40ea-ab4e-453f88b8b16c  6ec29c85c72246ea83912c6f02f6fd63  ...     Provisional      None  2026-04-24T16:06:22.291045+00:00
1  POINT (-80.85306 35.16444)  b3ce8113-2a1a-4d13-9d88-8a0237c11df6  27d30d4d1a4749bb887d1435da9fd278  ...     Provisional      None  2026-04-24T16:06:35.455215+00:00
2  POINT (-80.85306 35.16444)  e56f5a19-8a93-489d-a2a0-98cae31f9529  b1f149deee984fcea8768c17076b1d7f  ...     Provisional      None  2026-04-24T16:06:17.732760+00:00

[3 rows x 12 columns]
Index(['geometry', 'id', 'time_series_id', 'monitoring_location_id',
       'parameter_code', 'statistic_id', 'time', 'value', 'unit_of_measure',
       'approval_status', 'qualifier', 'last_modified'],
      dtype='str')
```

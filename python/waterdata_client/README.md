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
import geopandas as gpd
from hydrotools.waterdata_client import LatestContinuousClient
from hydrotools.waterdata_client.transformers import to_geodataframe

# Instantiate client
client = LatestContinuousClient(transformer=to_geodataframe)

# Retrieve data
observations = client.get(
    monitoring_location_id="USGS-02146470"
    )

# Look at values
print(observations)
print(observations.columns)
```

### Output

```console
                     geometry                                    id                    time_series_id  ... approval_status qualifiers                     last_modified
0  POINT (-80.85306 35.16444)  3373c03d-ef10-41b9-be8f-afcd1511dc27  27d30d4d1a4749bb887d1435da9fd278  ...     Provisional       None  2026-05-01T15:47:32.759180+00:00
1  POINT (-80.85306 35.16444)  48ba1d22-3278-449f-b767-a08f3ccffb2c  b1f149deee984fcea8768c17076b1d7f  ...     Provisional       None  2026-05-01T15:52:15.484900+00:00
2  POINT (-80.85306 35.16444)  c387f069-f5f4-4954-8810-38b1ad3ba1ab  6ec29c85c72246ea83912c6f02f6fd63  ...     Provisional       None  2026-05-01T15:52:20.586492+00:00

[3 rows x 12 columns]
Index(['geometry', 'id', 'time_series_id', 'usgs_site_code', 'parameter_code',
       'statistic_id', 'value_time', 'value', 'measurement_unit',
       'approval_status', 'qualifiers', 'last_modified'],
      dtype='str')
```

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

The following examples demonstrate typical usage of `hydrotools.waterdata_client`.

### Retrieve most recent streamflow values

```python
# The LatestContinuousClient provides an interface to the latest-continuous endpoint.
from hydrotools.waterdata_client import LatestContinuousClient

# The default client returns deserialized JSON as a list of Python dictionaries.
#   We'll import a transformer that converts these data to a GeoDataFrame.
from hydrotools.waterdata_client.transformers import to_geodataframe

# Instantiate the client with the GeoDataFrame transformer
client = LatestContinuousClient(transformer=to_geodataframe)

# Retrieve data
observations = client.get(
    monitoring_location_id="USGS-02146470",
    parameter_code="00060" # Volumetric streamflow in ft^3/s
    )

# Look at values
print(observations[["usgs_site_code", "value_time", "value", "geometry"]])
print(observations.columns)
```

#### Output

```console
  usgs_site_code                 value_time value                    geometry
0  USGS-02146470  2026-05-18T18:45:00+00:00  0.40  POINT (-80.85306 35.16444)

Index(['geometry', 'id', 'time_series_id', 'usgs_site_code', 'parameter_code',
       'statistic_id', 'value_time', 'value', 'measurement_unit',
       'approval_status', 'qualifiers', 'last_modified'],
      dtype='str')
```

### Retrieve values using datetime objects

```python
import pandas as pd
# from datetime import datetime, timedelta
# from zoneinfo import ZoneInfo

# The ContinuousClient provides an interface to the continuous endpoint.
from hydrotools.waterdata_client import ContinuousClient

# The default client returns deserialized JSON as a list of Python dictionaries.
#   We'll import a transformer that converts these data to a DataFrame.
from hydrotools.waterdata_client.transformers import to_dataframe

# Instantiate the client with the DataFrame transformer
client = ContinuousClient(transformer=to_dataframe)

# Retrieve data using datetime handling
observations = client.get(
    monitoring_location_id="USGS-02146470",
    limit=50_000,
    parameter_code="00065", # Stage in ft.

    # Strings are passed directly to the API without intervention. See the API
    #   documentation for more information about valid string formats (RFC 3339).
    # datetime="2025-05-03T12:00:00-05:00/2025-05-05T00:00:00-05:00",

    # Retrieve the last 6 hours using pandas.Timedelta
    datetime=pd.Timedelta(hours=6),

    # Retrieve a specific datetime using pandas.Timestamp
    #   Timezone naive objects are assumed to be UTC.
    # datetime=pd.Timestamp("2010-01-01"),

    # Timezone aware types are converted to UTC before retrieval.
    # datetime=pd.Timestamp("2010-01-01", tzinfo=ZoneInfo("America/Chicago")),

    # Retrieve using a standard datetime object
    # datetime=datetime(2026, 1, 1, 0, 30, 0),

    # Retrieve using a standard timedelta object
    # datetime=timedelta(hours=6),

    # Use a list of datetime objects to specify a bounded interval [start, end]
    # datetime=[pd.Timestamp("2026-01-01"), pd.Timestamp("2026-01-02")],

    # Specify a half-bounded interval using None
    # datetime=[pd.Timestamp("2026-05-01"), None],
    )

# Look at values
print(observations[["usgs_site_code", "value_time", "value", "geometry"]])
print(observations.columns)
```

#### Output

```console
   usgs_site_code                 value_time value geometry
0   USGS-02146470  2026-05-18T13:00:00+00:00  3.07     None
1   USGS-02146470  2026-05-18T13:05:00+00:00  3.07     None
2   USGS-02146470  2026-05-18T13:10:00+00:00  3.07     None
3   USGS-02146470  2026-05-18T13:15:00+00:00  3.08     None
4   USGS-02146470  2026-05-18T13:20:00+00:00  3.08     None
..            ...                        ...   ...      ...
66  USGS-02146470  2026-05-18T18:30:00+00:00  3.08     None
67  USGS-02146470  2026-05-18T18:35:00+00:00  3.08     None
68  USGS-02146470  2026-05-18T18:40:00+00:00  3.08     None
69  USGS-02146470  2026-05-18T18:45:00+00:00  3.08     None
70  USGS-02146470  2026-05-18T18:50:00+00:00  3.08     None

[71 rows x 4 columns]
Index(['type', 'id', 'geometry', 'geo_feature_id', 'time_series_id',
       'usgs_site_code', 'parameter_code', 'statistic_id', 'value_time',
       'value', 'measurement_unit', 'approval_status', 'qualifiers',
       'last_modified'],
      dtype='str')
```


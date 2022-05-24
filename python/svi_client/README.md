# OWPHydroTools :: SVI Client


This subpackage provides programmatic accessing the Center for Disease Control's (CDC) Social
Vulnerability Index (SVI). "Social vulnerability refers to the potential negative effects on
communities caused by external stresses on human health. Such stresses include natural or
human-caused disasters, or disease outbreaks. Reducing social vulnerability can decrease both human
suffering and economic loss." [[source](https://www.atsdr.cdc.gov/placeandhealth/svi/index.html)]

The SVI has been released 5 times (2000, 2010, 2014, 2016, and 2018) and calculates a relative
percentile ranking in four themes categories and an overall ranking at a given _geographic context_
and _geographic scale_. The themes are: 

- Socioeconomic
- Household Composition & Disability
- Minority Status & Language
- Housing Type & Transportation

Rankings are calculated relative to a _geographic context_, state or all states (United States) .
Meaning, for example, a ranking calculated for some location at the United States geographic context
would be relative to all other locations where rankings was calculated in the United States.
Similarly, SVI rankings are calculated at two _geographic scales_, census tract and county scales.
Meaning, the rankings correspond to a county for a census tract. For completeness, for example, if
you were to retrieve the 2018 SVI at the census tract scale, at the state context for the state of
Alabama, you would receive 1180 records (number of census tracts in AL in 2010 census) where each
ranked percentile is calculated relative to census tracts in Alabama.  The tool released in this PR
only supports querying for ranking calculated at the United States geographic context. Future work
will add support for retrieving rankings at the state spatial scale.

Documentation for each year release of the SVI are located below:

- [2000](https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI2000Documentation-H.pdf)
- [2010](https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI-2010-Documentation-H.pdf)
- [2014](https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI2014Documentation_01192022.pdf)
- [2016](https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI2016Documentation_01192022.pdf)
- [2018](https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI2018Documentation_01192022_1.pdf)


See the [SVI Client Documentation](https://noaa-owp.github.io/hydrotools/hydrotools.svi_client.html)
for a complete list and description of the currently available methods. To report bugs or request
new features, submit an issue through the [OWPHydroTools Issue
Tracker](https://github.com/NOAA-OWP/hydrotools/issues) on GitHub.

## Installation

In accordance with the python community, we support and advise the usage of virtual environments in
any workflow using python. In the following installation guide, we use python's built-in `venv`
module to create a virtual environment in which the tool will be installed. Note this is just
personal preference, any python virtual environment manager should work just fine (`conda`,
`pipenv`, etc. ).

```bash
# Create and activate python environment, requires python >= 3.8
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip

# Install nwis_client
$ python3 -m pip install hydrotools.svi_client
```


## Usage


### Code

```python
from hydrotools.svi_client import SVIClient

client = SVIClient()
df = client.get(
    location="AL", # state / nation name (i.e. "alabama" or "United States") also accepted. case insensitive
    geographic_scale="census_tract", # "census_tract" or "county"
    year="2018", # 2000, 2010, 2014, 2016, or 2018
    geographic_context="national" # only "national" supported. "state" will be supported in the future
    )
print(df)
```

### Example output

```console
            state_name state_abbreviation  ... svi_edition                                           geometry
0        alabama                 al  ...        2018  POLYGON ((-87.21230 32.83583, -87.20970 32.835...
1        alabama                 al  ...        2018  POLYGON ((-86.45640 31.65556, -86.44864 31.655...
...          ...                ...  ...         ...                                                ...
29498    alabama                 al  ...        2018  POLYGON ((-85.99487 31.84424, -85.99381 31.844...
29499    alabama                 al  ...        2018  POLYGON ((-86.19941 31.80787, -86.19809 31.808...
```
### System Requirements

## Development

```bash
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install -U pip
$ python3 -m pip install -U setuptools
$ python3 -m pip install -e ".[develop]"
```

To generate a source distribution:
```bash
$ python3 -m pip install -U wheel build
$ python3 -m build
```

The packages generated in `dist/` can be installed directly with `pip` or uploaded to PyPI using `twine`.

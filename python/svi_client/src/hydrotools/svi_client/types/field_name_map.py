from pydantic import BaseModel
from functools import partial
from types import MappingProxyType
from typing import Optional, Tuple

# local imports
from . import utilities
from .type_definitions import GeographicScale, Year


class FieldNameMap(BaseModel):
    """Map from canonical hydrotools SVI field names to SVI field names from another provenance."""

    state_name: str  # State name
    state_abbreviation: str  # State abbreviation
    county_name: str  # County name

    state_fips: str  # State FIPS code
    county_fips: str  # County name
    fips: str  # Census tract or county fips code

    svi_edition: str  # year corresponding to svi release (this assumes 2 SVI's will not be release in a given year in the future)

    rank_theme_1: str  # Socioeconomic
    rank_theme_2: str  # Household Composition / Disability
    rank_theme_3: str  # Minority Status / Language
    rank_theme_4: str  # Housing Type / Transportation
    rank_svi: str  # aggregated overall percentile ranking

    value_theme_1: Optional[str]  # Socioeconomic
    value_theme_2: Optional[str]  # Household Composition / Disability
    value_theme_3: Optional[str]  # Minority Status / Language
    value_theme_4: Optional[str]  # Housing Type / Transportation

    # aggregated overall value; sum of values from themes 1, 2, 3, 4.
    value_svi: Optional[str]


### Mapping types for data sourced from: https://services3.arcgis.com/ZvidGQkLaDJxRSJ2/ArcGIS/rest/services/. ###

## SVI Counties Types ##

# 2000s data does not include theme values
CdcEsri2000CountiesFieldNameMap = FieldNameMap(
    state_name="STATE_NAME",
    state_abbreviation="STATE_ABBR",
    county_name="COUNTY",
    state_fips="STATE_FIPS",
    county_fips="CNTY_FIPS",
    fips="STCOFIPS",
    svi_edition="2000",
    rank_theme_1="USG1TP",
    rank_theme_2="USG2TP",
    rank_theme_3="USG3TP",
    rank_theme_4="USG4TP",
    rank_svi="USTP",
)

CdcEsri2010CountiesFieldNameMap = FieldNameMap(
    state_name="FIRST_STATE_NAME",
    state_abbreviation="FIRST_STATE_ABBR",
    county_name="FIRST_COUNTY",
    state_fips="FIRST_STATE_FIPS",
    county_fips="FIRST_CNTY_FIPS",
    fips="STCOFIPS",
    svi_edition="2010",
    rank_theme_1="R_PL_THEME1",
    rank_theme_2="R_PL_THEME2",
    rank_theme_3="R_PL_THEME3",
    rank_theme_4="R_PL_THEME4",
    rank_svi="R_PL_THEMES",
    value_theme_1="S_PL_THEME1",
    value_theme_2="S_PL_THEME2",
    value_theme_3="S_PL_THEME3",
    value_theme_4="S_PL_THEME4",
    value_svi="S_PL_THEMES",
)

# svi_edition is excluded, so it can be parametrized
_CdcEsriCountiesFieldNameMap = partial(
    FieldNameMap,
    state_name="STATE",
    state_abbreviation="ST_ABBR",
    county_name="COUNTY",
    state_fips="ST",
    county_fips="FIPS",  # calculated FIPS[len(ST):]
    fips="FIPS",
    rank_theme_1="RPL_THEME1",
    rank_theme_2="RPL_THEME2",
    rank_theme_3="RPL_THEME3",
    rank_theme_4="RPL_THEME4",
    rank_svi="RPL_THEMES",
    value_theme_1="SPL_THEME1",
    value_theme_2="SPL_THEME2",
    value_theme_3="SPL_THEME3",
    value_theme_4="SPL_THEME4",
    value_svi="SPL_THEMES",
)

CdcEsri2014CountiesFieldNameMap = _CdcEsriCountiesFieldNameMap(svi_edition="2014")
CdcEsri2016CountiesFieldNameMap = _CdcEsriCountiesFieldNameMap(svi_edition="2016")
CdcEsri2018CountiesFieldNameMap = _CdcEsriCountiesFieldNameMap(svi_edition="2018")


##  SVI Tract Types  ##

# 2000s data does not include theme values
CdcEsri2000TractsFieldNameMap = FieldNameMap(
    state_name="STATE_NAME",
    state_abbreviation="STATE_ABBR",
    county_name="COUNTY",
    state_fips="STATE_FIPS",
    county_fips="CNTY_FIPS",
    fips="FIPS",
    svi_edition="2000",
    rank_theme_1="USG1TP",
    rank_theme_2="USG2TP",
    rank_theme_3="USG3TP",
    rank_theme_4="USG4TP",
    rank_svi="USTP",
)

CdcEsri2010TractsFieldNameMap = FieldNameMap(
    state_name="STATE_NAME",
    state_abbreviation="STATE_ABBR",
    county_name="COUNTY",
    state_fips="STATE_FIPS",
    county_fips="CNTY_FIPS",
    fips="FIPS",
    svi_edition="2010",
    rank_theme_1="R_PL_THEME1",
    rank_theme_2="R_PL_THEME2",
    rank_theme_3="R_PL_THEME3",
    rank_theme_4="R_PL_THEME4",
    rank_svi="R_PL_THEMES",
    value_theme_1="S_PL_THEME1",
    value_theme_2="S_PL_THEME2",
    value_theme_3="S_PL_THEME3",
    value_theme_4="S_PL_THEME4",
    value_svi="S_PL_THEMES",
)

# svi_edition is excluded, so it can be parametrized
_CdcEsriTractFieldNameMap = partial(
    FieldNameMap,
    state_name="STATE",
    state_abbreviation="ST_ABBR",
    county_name="COUNTY",
    state_fips="ST",
    county_fips="STCNTY",  # calculated STCNTY[len(ST):]
    fips="FIPS",
    rank_theme_1="RPL_THEME1",
    rank_theme_2="RPL_THEME2",
    rank_theme_3="RPL_THEME3",
    rank_theme_4="RPL_THEME4",
    rank_svi="RPL_THEMES",
    value_theme_1="SPL_THEME1",
    value_theme_2="SPL_THEME2",
    value_theme_3="SPL_THEME3",
    value_theme_4="SPL_THEME4",
    value_svi="SPL_THEMES",
)

CdcEsri2014TractsFieldNameMap = _CdcEsriTractFieldNameMap(svi_edition="2014")
CdcEsri2016TractsFieldNameMap = _CdcEsriTractFieldNameMap(svi_edition="2016")
CdcEsri2018TractsFieldNameMap = _CdcEsriTractFieldNameMap(svi_edition="2018")

_CdcEsriFieldNameMapFactory: MappingProxyType[
    Tuple[str, str], FieldNameMap
] = MappingProxyType(
    {
        # year, geographic scale: FieldNameMap
        # counties
        ("2000", "county"): CdcEsri2000CountiesFieldNameMap,
        ("2010", "county"): CdcEsri2010CountiesFieldNameMap,
        ("2014", "county"): CdcEsri2014CountiesFieldNameMap,
        ("2016", "county"): CdcEsri2016CountiesFieldNameMap,
        ("2018", "county"): CdcEsri2018CountiesFieldNameMap,
        # tracts
        ("2000", "census_tract"): CdcEsri2000TractsFieldNameMap,
        ("2010", "census_tract"): CdcEsri2010TractsFieldNameMap,
        ("2014", "census_tract"): CdcEsri2014TractsFieldNameMap,
        ("2016", "census_tract"): CdcEsri2016TractsFieldNameMap,
        ("2018", "census_tract"): CdcEsri2018TractsFieldNameMap,
    }
)


def CdcEsriFieldNameMapFactory(
    geographic_scale: GeographicScale, year: Year
) -> FieldNameMap:
    geographic_scale = utilities.validate_geographic_scale(geographic_scale)  # type: ignore
    year = utilities.validate_year(year)  # type: ignore

    search_tuple = (year, geographic_scale)
    return _CdcEsriFieldNameMapFactory[search_tuple]  # type: ignore


# Developer notes

# state_fips:
#     counties: STATE_FIPS, FIRST_STATE_FIPS, ST, ST, ST
#     tracts: STATE_FIPS, STATE_FIPS, ST, ST, ST
# county_fips:
#     counties: CNTY_FIPS, FIRST_CNTY_FIPS, FIPS[len(ST):], FIPS[len(ST):], FIPS[len(ST):]
#     tracts: CNTY_FIPS, CNTY_FIPS, STCNTY[len(ST):], STCNTY[len(ST):], STCNTY[len(ST):]
# fips:
#     counties: STCOFIPS, STCOFIPS, FIPS, FIPS, FIPS
#     tracts: FIPS, FIPS, FIPS, FIPS, FIPS
# state_name:
#     counties: STATE_NAME, FIRST_STATE_NAME, STATE, STATE, STATE
#     tracts: STATE_NAME, STATE_NAME, STATE.strip(), STATE, STATE
# state_abbreviation:
#     counties: STATE_ABBR, FIRST_STATE_ABBR, ST_ABBR, ST_ABBR, ST_ABBR
#     tracts: STATE_ABBR, STATE_ABBR, ST_ABBR, ST_ABBR, ST_ABBR
# county_name:
#     counties: COUNTY, FIRST_COUNTY, COUNTY, COUNTY, COUNTY
#     tracts: COUNTY, COUNTY, COUNTY.strip(), COUNTY, COUNTY
# svi_edition:
#     counties: 2000, 2010, 2014, 2016, 2018
#     tracts: 2000, 2010, 2014, 2016, 2018
# rank_theme_1
#     counties: USG1TP, R_PL_THEME1, RPL_THEME1, RPL_THEME1, RPL_THEME1
#     tracts: USG1TP, R_PL_THEME1, RPL_THEME1, RPL_THEME1, RPL_THEME1
# rank_theme_2
#     counties: USG2TP, R_PL_THEME2, RPL_THEME2, RPL_THEME2, RPL_THEME2
#     tracts: USG2TP, R_PL_THEME2, RPL_THEME2, RPL_THEME2, RPL_THEME2
# rank_theme_3
#     counties: USG3TP, R_PL_THEME3, RPL_THEME3, RPL_THEME3, RPL_THEME3
#     tracts: USG3TP, R_PL_THEME3, RPL_THEME3, RPL_THEME3, RPL_THEMES3
# rank_theme_4
#     counties: USG3TP, R_PL_THEME4, RPL_THEME4, RPL_THEME4, RPL_THEME4
#     tracts: USG3TP, R_PL_THEME4, RPL_THEME4, RPL_THEME4, RPL_THEME4
# rank_svi
#     counties: USTP, R_PL_THEMES, RPL_THEMES, RPL_THEMES, RPL_THEMES
#     tracts: USTP, R_PL_THEMES, RPL_THEMES, RPL_THEMES, RPL_THEMES
# value_theme_1
#     counties: NA, S_PL_THEME1, SPL_THEME1, SPL_THEME1, SPL_THEME1
#     tracts: NA, S_PL_THEME1, SPL_THEME1, SPL_THEME1, SPL_THEME1
# value_theme_2
#     counties: NA, S_PL_THEME2, SPL_THEME2, SPL_THEME2, SPL_THEME2
#     tracts: NA, S_PL_THEME2, SPL_THEME2, SPL_THEME2, SPL_THEME2
# value_theme_3
#     counties: NA, S_PL_THEME3, SPL_THEME3, SPL_THEME3, SPL_THEME3
#     tracts: NA, S_PL_THEME3, SPL_THEME3, SPL_THEMES3, SPL_THEME3
# value_theme_4
#     counties: NA, S_PL_THEME4, SPL_THEME4, SPL_THEME4, SPL_THEME4
#     tracts: NA, S_PL_THEME4, SPL_THEME4, SPL_THEME4, SPL_THEME4
# value_svi
#     counties: NA, S_PL_THEMES, SPL_THEMES, SPL_THEMES, SPL_THEMES
#     tracts: NA, S_PL_THEMES, SPL_THEMES, SPL_THEMES, SPL_THEMES

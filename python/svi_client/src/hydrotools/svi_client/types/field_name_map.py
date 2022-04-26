from __future__ import annotations
from pydantic import BaseModel
from functools import partial
from types import MappingProxyType
from typing import Optional, Tuple
import pandas as pd

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

    socioeconomic_rank: str  # theme_1_rank : Socioeconomic
    household_comp_and_disability_rank: str  # theme_2_rank : Household Composition / Disability
    minority_status_and_lang_rank: str  # theme_3_rank : Minority Status / Language
    housing_type_and_trans_rank: str  # theme_4_rank : Housing Type / Transportation
    svi_rank: str  # aggregated overall percentile ranking

    socioeconomic_value: Optional[str]  # theme_1_value : Socioeconomic
    household_comp_and_disability_value: Optional[
        str
    ]  # theme_2_value : Household Composition / Disability
    minority_status_and_lang_value: Optional[
        str
    ]  # theme_3_value : Minority Status / Language
    housing_type_and_trans_value: Optional[
        str
    ]  # theme_4_value : Housing Type / Transportation

    # aggregated overall value; sum of values from themes 1, 2, 3, 4.
    svi_value: Optional[str]

    @staticmethod
    def create_missing_fields(df: pd.DataFrame) -> pd.DataFrame:
        """subclasses should override this to create missing dataframe fields from existing fields.
        default behavior is to return input df.
        """
        return df


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
    socioeconomic_rank="USG1TP",
    household_comp_and_disability_rank="USG2TP",
    minority_status_and_lang_rank="USG3TP",
    housing_type_and_trans_rank="USG4TP",
    svi_rank="USTP",
)

CdcEsri2010CountiesFieldNameMap = FieldNameMap(
    state_name="FIRST_STATE_NAME",
    state_abbreviation="FIRST_STATE_ABBR",
    county_name="FIRST_COUNTY",
    state_fips="FIRST_STATE_FIPS",
    county_fips="FIRST_CNTY_FIPS",
    fips="STCOFIPS",
    svi_edition="2010",
    socioeconomic_rank="R_PL_THEME1",
    household_comp_and_disability_rank="R_PL_THEME2",
    minority_status_and_lang_rank="R_PL_THEME3",
    housing_type_and_trans_rank="R_PL_THEME4",
    svi_rank="R_PL_THEMES",
    socioeconomic_value="S_PL_THEME1",
    household_comp_and_disability_value="S_PL_THEME2",
    minority_status_and_lang_value="S_PL_THEME3",
    housing_type_and_trans_value="S_PL_THEME4",
    svi_value="S_PL_THEMES",
)


class _CdcEsriMissingCountyFipsFieldNameMap(FieldNameMap):
    @staticmethod
    def create_missing_fields(df: pd.DataFrame) -> pd.DataFrame:
        """
        derive `county_fips` from `fips`. county fips codes are five digits long, where the first
        two digits are the state fips.
        source: https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt
        """
        return df.assign(county_fips=lambda d: d["fips"].str.slice(2, 5))


# svi_edition is excluded, so it can be parametrized
_CdcEsriCountiesFieldNameMap = partial(
    _CdcEsriMissingCountyFipsFieldNameMap,
    state_name="STATE",
    state_abbreviation="ST_ABBR",
    county_name="COUNTY",
    state_fips="ST",
    county_fips="FIPS",  # calculated FIPS[2:5]
    fips="FIPS",
    socioeconomic_rank="RPL_THEME1",
    household_comp_and_disability_rank="RPL_THEME2",
    minority_status_and_lang_rank="RPL_THEME3",
    housing_type_and_trans_rank="RPL_THEME4",
    svi_rank="RPL_THEMES",
    socioeconomic_value="SPL_THEME1",
    household_comp_and_disability_value="SPL_THEME2",
    minority_status_and_lang_value="SPL_THEME3",
    housing_type_and_trans_value="SPL_THEME4",
    svi_value="SPL_THEMES",
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
    socioeconomic_rank="USG1TP",
    household_comp_and_disability_rank="USG2TP",
    minority_status_and_lang_rank="USG3TP",
    housing_type_and_trans_rank="USG4TP",
    svi_rank="USTP",
)

CdcEsri2010TractsFieldNameMap = FieldNameMap(
    state_name="STATE_NAME",
    state_abbreviation="STATE_ABBR",
    county_name="COUNTY",
    state_fips="STATE_FIPS",
    county_fips="CNTY_FIPS",
    fips="FIPS",
    svi_edition="2010",
    socioeconomic_rank="R_PL_THEME1",
    household_comp_and_disability_rank="R_PL_THEME2",
    minority_status_and_lang_rank="R_PL_THEME3",
    housing_type_and_trans_rank="R_PL_THEME4",
    svi_rank="R_PL_THEMES",
    socioeconomic_value="S_PL_THEME1",
    household_comp_and_disability_value="S_PL_THEME2",
    minority_status_and_lang_value="S_PL_THEME3",
    housing_type_and_trans_value="S_PL_THEME4",
    svi_value="S_PL_THEMES",
)

# svi_edition is excluded, so it can be parametrized
_CdcEsriTractFieldNameMap = partial(
    _CdcEsriMissingCountyFipsFieldNameMap,
    state_name="STATE",
    state_abbreviation="ST_ABBR",
    county_name="COUNTY",
    state_fips="ST",
    county_fips="STCNTY",  # calculated FIPS[2:5]
    fips="FIPS",
    socioeconomic_rank="RPL_THEME1",
    household_comp_and_disability_rank="RPL_THEME2",
    minority_status_and_lang_rank="RPL_THEME3",
    housing_type_and_trans_rank="RPL_THEME4",
    svi_rank="RPL_THEMES",
    socioeconomic_value="SPL_THEME1",
    household_comp_and_disability_value="SPL_THEME2",
    minority_status_and_lang_value="SPL_THEME3",
    housing_type_and_trans_value="SPL_THEME4",
    svi_value="SPL_THEMES",
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

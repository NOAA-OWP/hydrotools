from hydrotools._restclient import Url

# local imports
from .types import utilities, field_name_map
from .types import GeographicScale, GeographicContext, Year
from .consts import US_COUNTY_FEATURE_SERVER_URLS, US_TRACT_FEATURE_SERVERS_URLS

# typing imports
from typing import Optional


def build_csv_url(location: str, geographic_scale: GeographicScale, year: Year) -> str:
    location = utilities.validate_location(location)
    geographic_scale = utilities.validate_geographic_scale(geographic_scale)
    year = utilities.validate_year(year)

    base_path = f"Documents/Data/{year}_SVI_Data/CSV"

    if geographic_scale == "county":
        county_token = get_county_token(year)
        if location == "US":
            location_path = f"SVI{year}_US_{county_token}.csv"
        else:
            location_path = f"States_Counties/{location}_{county_token}.csv"

    else:
        if location == "US":
            location_path = f"SVI{year}_US.csv"
        else:
            location_path = f"States/{location}.csv"

    return f"{base_path}/{location_path}"


def build_feature_server_url(
    location: str,
    geographic_scale: GeographicScale,
    year: Year,
    geographic_context: GeographicContext,
    result_offset: Optional[int] = None,
    result_record_count: Optional[int] = None,
    count_only: bool = False,
) -> str:
    location = utilities.validate_location(location)
    geographic_scale = utilities.validate_geographic_scale(geographic_scale)
    year = utilities.validate_year(year)
    context = utilities.validate_geographic_context(geographic_context)

    if context == "state":
        error_message = (
            "the `state` geographic context has not yet been implimented. "
            "only svi ranked at the `national` context are currently supported."
        )
        raise NotImplemented(error_message)

    path = (
        US_COUNTY_FEATURE_SERVER_URLS[year]
        if geographic_scale == "county"
        else US_TRACT_FEATURE_SERVERS_URLS[year]
    )
    path = f"{path}/query"

    fnm = field_name_map.CdcEsriFieldNameMapFactory(geographic_scale, year)

    params = {
        # for entire US, use 1=1 where clause
        "where": f"{fnm.state_abbreviation} = '{location}'"
        if location != "us"
        else "1=1",
        "outFields": ",".join(
            fnm.dict(exclude_unset=True, exclude={"svi_edition"}).values()
        ),
        "returnGeometry": "true",
        "returnExceededLimitFeatures": "true",
        "returnCountOnly": "true" if count_only else "false",
        "resultOffset": "" if result_offset is None else result_offset,
        "resultRecordCount": "" if result_record_count is None else result_record_count,
        "f": "pgeojson",
    }

    o: Url = Url(path, safe="/'") + params
    return o.quote_url


def build_shp_url(location: str, geographic_scale: GeographicScale, year: Year) -> str:
    location = utilities.validate_location(location)
    geographic_scale = utilities.validate_geographic_scale(geographic_scale)
    year = utilities.validate_year(year)

    # shp: Documents/Data/2000_SVI_Data/{geo_option}_2000_SVI.zip
    # US

    base_path = f"Documents/Data/{year}_SVI_Data/CSV"

    if geographic_scale == "county":
        county_token = get_county_token(year)
        if location == "US":
            location_path = f"SVI{year}_US_{county_token}.csv"
        else:
            location_path = f"States_Counties/{location}_{county_token}.csv"

    else:
        if location == "US":
            location_path = f"SVI{year}_US.csv"
        else:
            location_path = f"States/{location}.csv"

    return f"{base_path}/{location_path}"


# helper functions


def get_county_token(year: Year) -> str:
    year = utilities.validate_year(year)

    if year not in ("2014", "2016", "2018"):
        error_message = "Country geographic scale only available for SVI years: 2014, 2016, and 2018."
        raise ValueError(error_message)

    return "CNTY" if year == "2014" else "COUNTY"


# Developer Notes:

# crosswalk urls:
# 2014: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/csv/SVIDocumentation_Table_Crosswalk_2014.csv
# 2016: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/csv/SVIDocumentation_Table_Crosswalk_2016.csv

# data dictionary urls:
# 2000: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/csv/SVIDocumentation_Table_DataDictionary_2000.csv
# 2010: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/csv/SVIDocumentation_Table_DataDictionary_2010.csv
# 2014: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/csv/SVIDocumentation_Table_DataDictionary_2014.csv
# 2016: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/csv/SVIDocumentation_Table_DataDictionary_2016.csv
# 2018: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/csv/SVIDocumentation_Table_DataDictionary_2018.csv

# documentation page urls:
# base_url_plus_path: https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/SVI_documentation_{year}.html

# data dictionary urls:
# 2000: https://svi.cdc.gov/Documents/Data/2000_SVI_Data/SVI2000DataDictionary.pdf
# NOTE: does not appear that 2010 follows the above url convention

# no data value = -999
#
# 14 / 16 / 18 have same col names (in csv case)

# CSVs
# 2000:
#     census_tracts:
#        ✔️ US: Documents/Data/2000_SVI_Data/CSV/SVI2000_US.csv
#        ✔️ single_state: Documents/Data/2000_SVI_Data/CSV/States/{geo_option}.csv
# 2010:
#     census_tracts:
#         ✔️ US: Documents/Data/2010_SVI_Data/CSV/SVI2010_US.csv
#         ✔ single_state: Documents/Data/2010_SVI_Data/CSV/States/{geo_option}.csv
# 2014:
#     census_tracts:
#         US: Documents/Data/2014_SVI_Data/CSV/SVI2014_US.csv
#         single_state: Documents/Data/2014_SVI_Data/CSV/States/{geo_option}.csv
#     counties:
#         US: Documents/Data/2014_SVI_Data/CSV/SVI2014_US_CNTY.csv
#         single_state: Documents/Data/2014_SVI_Data/CSV/States_Counties/{geo_option}_CNTY.csv
# 2016/2018:
#     census_tracts:
#         US: Documents/Data/{year}_SVI_Data/CSV/SVI{year}_US.csv
#         single_state: Documents/Data/{year}_SVI_Data/CSV/States/{geo_option}.csv
#     counties:
#         US: Documents/Data/{year}_SVI_Data/CSV/SVI{year}_US_COUNTY.csv
#         single_state: Documents/Data/{year}_SVI_Data/CSV/States_Counties/{geo_option}_COUNTY.csv


# SHP / GDBs
# 2000s case:
#     census_tracts:
#        US: Documents/Data/2000_SVI_Data/US_2000_SVI.zip # ESRI gdb
#        single_state: https://svi.cdc.gov/Documents/Data/2000_SVI_Data/State_2000_SVI.zip # ESRI gdb

# 2010s case:
#     census_tracts:
#         US: Documents/Data/2010_SVI_Data/SVI2010_US_03242014.zip
#         States: Documents/Data/2010_SVI_Data/SVI2010_States_03242014.zip
#         AllStates: Documents/Data/2010_SVI_Data/SVI2010_States_03242014.zip
#     counties:
#         US: Documents/Data/2010_SVI_Data/SVI2010_Counties.zip
#     unknown_spatial_resolution:
#         single_state: Documents/Data/2010_SVI_Data/States/{geo_option}_03242014.zip

# csv:
#     census_tracts:
#         ✔️ US: Documents/Data/2010_SVI_Data/CSV/SVI2010_US.csv
#         ✔ single_state: Documents/Data/2010_SVI_Data/CSV/States/{geo_option}.csv

# 2014s case:
# shp:
#     census_tracts:
#         US: Documents/Data/2014_SVI_Data/SVI2014_US.zip
#         single_state: Documents/Data/2014_SVI_Data/States/{geo_option).zip
#     counties:
#         US: Documents/Data/2014_SVI_Data/SVI2014_US_CNTY.zip
#         single_state: Documents/Data/2014_SVI_Data/States_Counties/{geo_option}_CNTY.zip

# csv:
#     census_tracts:
#         US: Documents/Data/2014_SVI_Data/CSV/SVI2014_US.csv
#         single_state: Documents/Data/2014_SVI_Data/CSV/States/{geo_option}.csv
#     counties:
#         US: Documents/Data/2014_SVI_Data/CSV/SVI2014_US_CNTY.csv
#         single_state: Documents/Data/2014_SVI_Data/CSV/States_Counties/{geo_option}_CNTY.csv

# 2016s case:
# 2018s case:
# shp:
#     census_tracts:
#         US: Documents/Data/{year}_SVI_Data/SVI{year}_US.zip
#         single_state: Documents/Data/{year}_SVI_Data/States/{geo_option).zip
#     counties:
#         US: Documents/Data/{year}_SVI_Data/SVI{year}_US_COUNTY.zip
#         single_state: Documents/Data/{year}_SVI_Data/States_Counties/{geo_option}_CNTY.zip

# csv:
#     census_tracts:
#         US: Documents/Data/{year}_SVI_Data/CSV/SVI{year}_US.csv
#         single_state: Documents/Data/{year}_SVI_Data/CSV/States/{geo_option}.csv
#     counties:
#         US: Documents/Data/{year}_SVI_Data/CSV/SVI{year}_US_COUNTY.csv
#         single_state: Documents/Data/{year}_SVI_Data/CSV/States_Counties/{geo_option}_COUNTY.csv

# Get counties for a given SVI year
# https://svi.cdc.gov/xmldata/SVI{year}_Counties.xml

# County level maps
#   base url: https://svi.cdc.gov/Documents/CountyMaps/
#
#   example:
#   https://svi.cdc.gov/Documents/CountyMaps/2014/Alabama/Alabama2014_Tuscaloosa.pdf

# 2000:
#   {state}{year}_{county}.pdf

# 2010:
#   {state}{year}_v2_{date-filename | county}.pdf

# 2014 | 2016 | 2018:
#   {state}{year}_{date-filename | county}.pdf
#   https://svi.cdc.gov/Documents/CountyMaps/{year}/{state}/{state}{year}_{data-filename | county}.pdf

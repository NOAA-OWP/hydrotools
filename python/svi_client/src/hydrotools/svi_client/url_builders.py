# local imports
from .types import utilities
from .types import GeographicScale, Year


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


# helper functions


def get_county_token(year: Year) -> str:
    year = utilities.validate_year(year)

    if year not in ("2014", "2016", "2018"):
        ...

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


# no data value = -999
#
# 14 / 16 / 18 have same col names (in csv case)

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


# 2000s case:
# shp: Documents/Data/2000_SVI_Data/{geo_option}_2000_SVI.zip

# csv:
#     census_tracts:
#        ✔️ US: Documents/Data/2000_SVI_Data/CSV/SVI2000_US.csv
#        ✔️ single_state: Documents/Data/2000_SVI_Data/CSV/States/{geo_option}.csv

# data dictionary: Documents/Data/2000_SVI_Data/SVI2000DataDictionary.pdf

# 2010s case:
# shp:
#     census_tracts:
#         US: Documents/Data/2010_SVI_Data/SVI2010_US_03242014.zip
#         States: Documents/Data/2010_SVI_Data/SVI2010_States_03242014.zip # not sure how this differs from census tracts for US
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

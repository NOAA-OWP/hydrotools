from types import MappingProxyType

_BASE_URL = "https://services3.arcgis.com/ZvidGQkLaDJxRSJ2/ArcGIS/rest/services"

US_COUNTY_FEATURE_SERVER_URLS = MappingProxyType(
    {
        "2000": f"{_BASE_URL}/Overall_2000_Counties/FeatureServer/0",
        "2010": f"{_BASE_URL}/Overall_2010_Counties/FeatureServer/0",
        "2014": f"{_BASE_URL}/Overall_2014_Counties/FeatureServer/1",
        "2016": f"{_BASE_URL}/Overall_2016_Counties/FeatureServer/0",
        "2018": f"{_BASE_URL}/CDC_Social_Vulnerability_Index_2018/FeatureServer/1",
    }
)

US_TRACT_FEATURE_SERVERS_URLS = MappingProxyType(
    {
        "2000": f"{_BASE_URL}/Overall_2000_Tracts/FeatureServer/0",
        "2010": f"{_BASE_URL}/Overall_2010_Tracts/FeatureServer/0",
        "2014": f"{_BASE_URL}/Overall_2014_Tracts/FeatureServer/1",
        "2016": f"{_BASE_URL}/Overall_2016_Tracts/FeatureServer/0",
        "2018": f"{_BASE_URL}/CDC_Social_Vulnerability_Index_2018/FeatureServer/2",
    }
)

# Developer documentation

# 2000:
# counties:
#     US: Overall_2000_Counties/FeatureServer/0
# tracts:
#     US: Overall_2000_Tracts/FeatureServer/0

# 2010:
# counties:
#     US: Overall_2010_Counties/FeatureServer/0
# tracts:
#     US: Overall_2010_Tracts/FeatureServer/0

# 2014:
# counties:
#     US: Overall_2014_Counties/FeatureServer/1
# tracts:
#     US: Overall_2014_Tracts/FeatureServer/1
#     # NOTE: all STATE and COUNTY fields are prefixed with a space
#     # use STATE LIKE '%%' to get around this

# 2016:
# counties:
#     US: Overall_2016_Counties/FeatureServer/0
# tracts:
#     US: Overall_2016_Tracts/FeatureServer/0

# 2018:
# counties:
#     US: CDC_Social_Vulnerability_Index_2018/FeatureServer/1
# tracts:
#     US: CDC_Social_Vulnerability_Index_2018/FeatureServer/2

# cols to support:
# state_fips: State FIPS code
# state_name: State name
# county_name: County name
# fips: Census tract or county fips code
# svi_edition: year corresponding to svi release (this assumes 2 SVI's will not be release in a given year in the future)
# geometry: County or census tract simple features geometry
# rank_theme_1: Socioeconomic
# rank_theme_2: Household Composition / Disability
# rank_theme_3: Minority Status / Language
# rank_theme_4: Housing Type / Transportation
# rank_svi: aggregated overall percentile ranking
# value_theme_1: Socioeconomic
# value_theme_2: Household Composition / Disability
# value_theme_3: Minority Status / Language
# value_theme_4: Housing Type / Transportation
# value_svi: aggregated overall value; sum of values from themes 1, 2, 3, 4.

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

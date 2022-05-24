from hydrotools._restclient import Alias, AliasGroup

# typing imports
# NOTE: use typing.Literal when minimum python version is 3.8
from typing_extensions import Literal

GeographicScale = Literal["census_tract", "county"]
GeographicContext = Literal["national", "state"]
DataFormat = Literal["csv", "shp"]
Year = Literal["2000", "2010", "2014", "2016", "2018", 2000, 2010, 2014, 2016, 2018]

# Geography options:
# source https://svi.cdc.gov/xmldata/SVI_StatesForDownload.xml
# used by form on https://svi.cdc.gov/data-download-wcms.html

# TODO: add "PuertoRico" and "States". will need to consider what datasets are available for these locations
# LOCATIONS = AliasGroup(
#     [
#         Alias("US", ["us", "united states"]),
#         Alias("Alabama", ["al", "alabama"]),
#         Alias("Alaska", ["ak", "alaska"]),
#         Alias("Arizona", ["az", "arizona"]),
#         Alias("Arkansas", ["ar", "arkansas"]),
#         Alias("California", ["ca", "california"]),
#         Alias("Colorado", ["co", "colorado"]),
#         Alias("Connecticut", ["ct", "connecticut"]),
#         Alias("Delaware", ["de", "delaware"]),
#         Alias("DistrictofColumbia", ["dc", "district of columbia"]),
#         Alias("Florida", ["fl", "florida"]),
#         Alias("Georgia", ["ga", "georgia"]),
#         Alias("Hawaii", ["hi", "hawaii"]),
#         Alias("Idaho", ["id", "idaho"]),
#         Alias("Illinois", ["il", "illinois"]),
#         Alias("Indiana", ["in", "indiana"]),
#         Alias("Iowa", ["ia", "iowa"]),
#         Alias("Kansas", ["ks", "kansas"]),
#         Alias("Kentucky", ["ky", "kentucky"]),
#         Alias("Louisiana", ["la", "louisiana"]),
#         Alias("Maine", ["me", "maine"]),
#         Alias("Maryland", ["md", "maryland"]),
#         Alias("Massachusetts", ["ma", "massachusetts"]),
#         Alias("Michigan", ["mi", "michigan"]),
#         Alias("Minnesota", ["mn", "minnesota"]),
#         Alias("Mississippi", ["ms", "mississippi"]),
#         Alias("Missouri", ["mo", "missouri"]),
#         Alias("Montana", ["mt", "montana"]),
#         Alias("Nebraska", ["ne", "nebraska"]),
#         Alias("Nevada", ["nv", "nevada"]),
#         Alias("NewHampshire", ["nh", "new hampshire"]),
#         Alias("NewJersey", ["nj", "new jersey"]),
#         Alias("NewMexico", ["nm", "new mexico"]),
#         Alias("NewYork", ["ny", "new york"]),
#         Alias("NorthCarolina", ["nc", "north carolina"]),
#         Alias("NorthDakota", ["nd", "north dakota"]),
#         Alias("Ohio", ["oh", "ohio"]),
#         Alias("Oklahoma", ["ok", "oklahoma"]),
#         Alias("Oregon", ["or", "oregon"]),
#         Alias("Pennsylvania", ["pa", "pennsylvania"]),
#         Alias("RhodeIsland", ["ri", "rhode island"]),
#         Alias("SouthCarolina", ["sc", "south carolina"]),
#         Alias("SouthDakota", ["sd", "south dakota"]),
#         Alias("Tennessee", ["tn", "tennessee"]),
#         Alias("Texas", ["tx", "texas"]),
#         Alias("Utah", ["ut", "utah"]),
#         Alias("Vermont", ["vt", "vermont"]),
#         Alias("Virginia", ["va", "virginia"]),
#         Alias("Washington", ["wa", "washington"]),
#         Alias("WestVirginia", ["wv", "west virginia"]),
#         Alias("Wisconsin", ["wi", "wisconsin"]),
#         Alias("Wyoming", ["wy", "wyoming"]),
#     ]
# )

# TODO: remove self refereing alias once bug in AliasGroup.get has been resolved
LOCATIONS = AliasGroup(
    [
        Alias("us", ["us", "united states"]),
        Alias("al", ["al", "alabama"]),
        Alias("ak", ["ak", "alaska"]),
        Alias("az", ["az", "arizona"]),
        Alias("ar", ["ar", "arkansas"]),
        Alias("ca", ["ca", "california"]),
        Alias("co", ["co", "colorado"]),
        Alias("ct", ["ct", "connecticut"]),
        Alias("de", ["de", "delaware"]),
        Alias("dc", ["dc", "district of columbia"]),
        Alias("fl", ["fl", "florida"]),
        Alias("ga", ["ga", "georgia"]),
        Alias("hi", ["hi", "hawaii"]),
        Alias("id", ["id", "idaho"]),
        Alias("il", ["il", "illinois"]),
        Alias("in", ["in", "indiana"]),
        Alias("ia", ["ia", "iowa"]),
        Alias("ks", ["ks", "kansas"]),
        Alias("ky", ["ky", "kentucky"]),
        Alias("la", ["la", "louisiana"]),
        Alias("me", ["me", "maine"]),
        Alias("md", ["md", "maryland"]),
        Alias("ma", ["ma", "massachusetts"]),
        Alias("mi", ["mi", "michigan"]),
        Alias("mn", ["mn", "minnesota"]),
        Alias("ms", ["ms", "mississippi"]),
        Alias("mo", ["mo", "missouri"]),
        Alias("mt", ["mt", "montana"]),
        Alias("ne", ["ne", "nebraska"]),
        Alias("nv", ["nv", "nevada"]),
        Alias("nh", ["nh", "new hampshire"]),
        Alias("nj", ["nj", "new jersey"]),
        Alias("nm", ["nm", "new mexico"]),
        Alias("ny", ["ny", "new york"]),
        Alias("nc", ["nc", "north carolina"]),
        Alias("nd", ["nd", "north dakota"]),
        Alias("oh", ["oh", "ohio"]),
        Alias("ok", ["ok", "oklahoma"]),
        Alias("or", ["or", "oregon"]),
        Alias("pa", ["pa", "pennsylvania"]),
        Alias("ri", ["ri", "rhode island"]),
        Alias("sc", ["sc", "south carolina"]),
        Alias("sd", ["sd", "south dakota"]),
        Alias("tn", ["tn", "tennessee"]),
        Alias("tx", ["tx", "texas"]),
        Alias("ut", ["ut", "utah"]),
        Alias("vt", ["vt", "vermont"]),
        Alias("va", ["va", "virginia"]),
        Alias("wa", ["wa", "washington"]),
        Alias("wv", ["wv", "west virginia"]),
        Alias("wi", ["wi", "wisconsin"]),
        Alias("wy", ["wy", "wyoming"]),
    ]
)

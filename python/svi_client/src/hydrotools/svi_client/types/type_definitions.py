from hydrotools._restclient import Alias, AliasGroup

# typing imports
from typing import Literal

GeographicScale = Literal["census_tract", "county"]
DataFormat = Literal["csv", "shp"]
Year = Literal["2000", "2010", "2014", "2016", "2018", 2000, 2010, 2014, 2016, 2018]

# Geography options:
# source https://svi.cdc.gov/xmldata/SVI_StatesForDownload.xml
# used by form on https://svi.cdc.gov/data-download-wcms.html

# TODO: add "PuertoRico" and "States". will need to consider what datasets are available for these locations
LOCATIONS = AliasGroup(
    [
        Alias("US", ["us", "united states"]),
        Alias("Alabama", ["al", "alabama"]),
        Alias("Alaska", ["ak", "alaska"]),
        Alias("Arizona", ["az", "arizona"]),
        Alias("Arkansas", ["ar", "arkansas"]),
        Alias("California", ["ca", "california"]),
        Alias("Colorado", ["co", "colorado"]),
        Alias("Connecticut", ["ct", "connecticut"]),
        Alias("Delaware", ["de", "delaware"]),
        Alias("DistrictofColumbia", ["dc", "district of columbia"]),
        Alias("Florida", ["fl", "florida"]),
        Alias("Georgia", ["ga", "georgia"]),
        Alias("Hawaii", ["hi", "hawaii"]),
        Alias("Idaho", ["id", "idaho"]),
        Alias("Illinois", ["il", "illinois"]),
        Alias("Indiana", ["in", "indiana"]),
        Alias("Iowa", ["ia", "iowa"]),
        Alias("Kansas", ["ks", "kansas"]),
        Alias("Kentucky", ["ky", "kentucky"]),
        Alias("Louisiana", ["la", "louisiana"]),
        Alias("Maine", ["me", "maine"]),
        Alias("Maryland", ["md", "maryland"]),
        Alias("Massachusetts", ["ma", "massachusetts"]),
        Alias("Michigan", ["mi", "michigan"]),
        Alias("Minnesota", ["mn", "minnesota"]),
        Alias("Mississippi", ["ms", "mississippi"]),
        Alias("Missouri", ["mo", "missouri"]),
        Alias("Montana", ["mt", "montana"]),
        Alias("Nebraska", ["ne", "nebraska"]),
        Alias("Nevada", ["nv", "nevada"]),
        Alias("NewHampshire", ["nh", "new hampshire"]),
        Alias("NewJersey", ["nj", "new jersey"]),
        Alias("NewMexico", ["nm", "new mexico"]),
        Alias("NewYork", ["ny", "new york"]),
        Alias("NorthCarolina", ["nc", "north carolina"]),
        Alias("NorthDakota", ["nd", "north dakota"]),
        Alias("Ohio", ["oh", "ohio"]),
        Alias("Oklahoma", ["ok", "oklahoma"]),
        Alias("Oregon", ["or", "oregon"]),
        Alias("Pennsylvania", ["pa", "pennsylvania"]),
        Alias("RhodeIsland", ["ri", "rhode island"]),
        Alias("SouthCarolina", ["sc", "south carolina"]),
        Alias("SouthDakota", ["sd", "south dakota"]),
        Alias("Tennessee", ["tn", "tennessee"]),
        Alias("Texas", ["tx", "texas"]),
        Alias("Utah", ["ut", "utah"]),
        Alias("Vermont", ["vt", "vermont"]),
        Alias("Virginia", ["va", "virginia"]),
        Alias("Washington", ["wa", "washington"]),
        Alias("WestVirginia", ["wv", "west virginia"]),
        Alias("Wisconsin", ["wi", "wisconsin"]),
        Alias("Wyoming", ["wy", "wyoming"]),
    ]
)

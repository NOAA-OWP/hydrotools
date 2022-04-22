import pytest
from hydrotools.svi_client import SVIClient

LOCATIONS = (
    "al",
    "ak",
    "az",
    "ar",
    "ca",
    "co",
    "ct",
    "de",
    "dc",
    "fl",
    "ga",
    "hi",
    "id",
    "il",
    "in",
    "ia",
    "ks",
    "ky",
    "la",
    "me",
    "md",
    "ma",
    "mi",
    "mn",
    "ms",
    "mo",
    "mt",
    "ne",
    "nv",
    "nh",
    "nj",
    "nm",
    "ny",
    "nc",
    "nd",
    "oh",
    "ok",
    "or",
    "pa",
    "ri",
    "sc",
    "sd",
    "tn",
    "tx",
    "ut",
    "vt",
    "va",
    "wa",
    "wv",
    "wi",
    "wy",
)

YEARS = ("2000", "2010", "2014", "2016", "2018")
GEOGRAPHIC_SCALES = ("county", "census_tract")


@pytest.mark.slow
@pytest.mark.parametrize("location", LOCATIONS)
@pytest.mark.parametrize("year", YEARS)
@pytest.mark.parametrize("scale", GEOGRAPHIC_SCALES)
def test_svi_client_get_integration(location, year, scale):
    client = SVIClient(enable_cache=False)
    df = client.get(location, scale, year)
    assert df.loc[0, "state_abbreviation"] == location


@pytest.mark.slow
@pytest.mark.parametrize("year", YEARS)
@pytest.mark.parametrize("scale", GEOGRAPHIC_SCALES)
def test_svi_client_get_integration_us(year, scale):
    client = SVIClient(enable_cache=False)
    df = client.get("us", scale, year)
    assert df.state_abbreviation.isin(LOCATIONS).all()

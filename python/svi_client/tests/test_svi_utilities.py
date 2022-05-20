import pytest
from hydrotools.svi_client.types import utilities

# test, validation
LOCATION_TESTS = (
    ("al", "al"),
    ("ALABAMA", "al"),
    ("alabama", "al"),
    ("AlAbAmA", "al"),
)


@pytest.mark.parametrize("test,val", LOCATION_TESTS)
def test_validate_locations(test: str, val: str):
    assert utilities.validate_location(test) == val


GEOGRAPHIC_SCALE_TESTS = (("census_tract", "census_tract"), ("county", "county"))


@pytest.mark.parametrize("test,val", GEOGRAPHIC_SCALE_TESTS)
def test_validate_geographic_scale(test, val):
    assert utilities.validate_geographic_scale(test) == val


GEOGRAPHIC_CONTEXT_TESTS = (("national", "national"), ("state", "state"))


@pytest.mark.parametrize("test,val", GEOGRAPHIC_CONTEXT_TESTS)
def test_validate_geographic_context(test, val):
    assert utilities.validate_geographic_context(test) == val


YEAR_TESTS = (
    (2000, "2000"),
    (2010, "2010"),
    (2014, "2014"),
    (2016, "2016"),
    (2018, "2018"),
    ("2000", "2000"),
    ("2010", "2010"),
    ("2014", "2014"),
    ("2016", "2016"),
    ("2018", "2018"),
)


@pytest.mark.parametrize("test,val", YEAR_TESTS)
def test_validate_year(test, val):
    assert utilities.validate_year(test) == val


# Tests for raising error


def test_validate_locations_raises_ValueError():
    test = "canada"

    with pytest.raises(ValueError):
        utilities.validate_location(test)


def test_validate_geographic_scale_raises_ValueError():
    test = "some fake scale"

    with pytest.raises(ValueError):
        utilities.validate_geographic_scale(test)


def test_validate_geographic_context_raises_ValueError():
    test = "some fake context"

    with pytest.raises(ValueError):
        utilities.validate_geographic_context(test)


def test_validate_year_raises_ValueError():
    test = 1999

    with pytest.raises(ValueError):
        utilities.validate_year(test)

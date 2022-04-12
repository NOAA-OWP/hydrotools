import typing


# local imports
from .type_definitions import LOCATIONS, GeographicScale, GeographicContext, Year


def validate_location(location: str) -> str:
    location_key = LOCATIONS.get(location.lower())  # noqa

    if location_key is None:
        ...

    return location_key


def validate_geographic_scale(geographic_scale: GeographicScale) -> str:
    if geographic_scale not in typing.get_args(GeographicScale):
        ...

    return geographic_scale


def validate_geographic_context(geographic_context: GeographicContext) -> str:
    if geographic_context not in typing.get_args(GeographicContext):
        ...

    return geographic_context


def validate_year(year: Year) -> str:
    year_str = str(year)

    if year_str not in typing.get_args(Year):
        ...

    return year_str

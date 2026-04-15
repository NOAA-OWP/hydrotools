# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
"""This is a Jinja2 auto-generated module. This module contains enums
and constants used package-wide. The `USGSCollection` StrEnum is generated
by inspecting the USGS OGC API JSON schema and identifying all "items" endpoints.

Package version: 0.1.0
Generation script: build_constants.py
Generated: 2026-04-15 15:40:32 Z
JSON Schema source: https://api.waterdata.usgs.gov/ogcapi/v0/openapi?f=json
JSON Schema version: 0.44.0
OpenAPI version: 3.0.2
"""
from enum import StrEnum

class OGCAPI(StrEnum):
    """OGC base API strings."""
    ROOT = ""
    COLLECTIONS = "collections"
    CONFORMANCE = "conformance"
    OPENAPI = "openapi"

class OGCPATH(StrEnum):
    """OGC endpoint path strings."""
    METADATA = ""
    ITEMS = "items"
    QUERYABLES = "queryables"
    SCHEMA = "schema"

class USGSCollection(StrEnum):
    """USGS OGC API Collections."""
    AGENCY_CODES = "agency-codes"
    ALTITUDE_DATUMS = "altitude-datums"
    AQUIFER_CODES = "aquifer-codes"
    AQUIFER_TYPES = "aquifer-types"
    CHANNEL_MEASUREMENTS = "channel-measurements"
    COMBINED_METADATA = "combined-metadata"
    CONTINUOUS = "continuous"
    COORDINATE_ACCURACY_CODES = "coordinate-accuracy-codes"
    COORDINATE_DATUM_CODES = "coordinate-datum-codes"
    COORDINATE_METHOD_CODES = "coordinate-method-codes"
    COUNTIES = "counties"
    COUNTRIES = "countries"
    DAILY = "daily"
    FIELD_MEASUREMENTS = "field-measurements"
    FIELD_MEASUREMENTS_METADATA = "field-measurements-metadata"
    HYDROLOGIC_UNIT_CODES = "hydrologic-unit-codes"
    LATEST_CONTINUOUS = "latest-continuous"
    LATEST_DAILY = "latest-daily"
    MEDIUM_CODES = "medium-codes"
    MONITORING_LOCATIONS = "monitoring-locations"
    NATIONAL_AQUIFER_CODES = "national-aquifer-codes"
    PARAMETER_CODES = "parameter-codes"
    RELIABILITY_CODES = "reliability-codes"
    SITE_TYPES = "site-types"
    STATES = "states"
    STATISTIC_CODES = "statistic-codes"
    TIME_SERIES_METADATA = "time-series-metadata"
    TIME_ZONE_CODES = "time-zone-codes"
    TOPOGRAPHIC_CODES = "topographic-codes"

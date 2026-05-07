# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
"""This is a Jinja2 auto-generated module. This module contains individual
pydantic request models for USGS OGC API items endpoints. These classes are generated
by inspecting the USGS OGC API JSON schema and identifying all "items" endpoints.

Package version: 0.8.0a0
Generation script: build_request_models.py
Generated: 2026-05-07 17:14:21 Z
JSON Schema source: https://api.waterdata.usgs.gov/ogcapi/v0/openapi?f=json
JSON Schema version: 0.49.2
OpenAPI version: 3.0.2
"""
from typing import Sequence, Literal, Optional, Any
from yarl import URL
from pydantic import BaseModel, Field

__all__ = [
    "AgencyCodesRequest",
    "AltitudeDatumsRequest",
    "AquiferCodesRequest",
    "AquiferTypesRequest",
    "ChannelMeasurementsRequest",
    "CitationsRequest",
    "CombinedMetadataRequest",
    "ContinuousRequest",
    "CoordinateAccuracyCodesRequest",
    "CoordinateDatumCodesRequest",
    "CoordinateMethodCodesRequest",
    "CountiesRequest",
    "CountriesRequest",
    "DailyRequest",
    "FieldMeasurementsRequest",
    "FieldMeasurementsMetadataRequest",
    "HydrologicUnitCodesRequest",
    "LatestContinuousRequest",
    "LatestDailyRequest",
    "MediumCodesRequest",
    "MethodCategoriesRequest",
    "MethodCitationsRequest",
    "MethodsRequest",
    "MonitoringLocationsRequest",
    "NationalAquiferCodesRequest",
    "ParameterCodesRequest",
    "PeaksRequest",
    "ReliabilityCodesRequest",
    "SiteTypesRequest",
    "StatesRequest",
    "StatisticCodesRequest",
    "TimeSeriesMetadataRequest",
    "TimeZoneCodesRequest",
    "TopographicCodesRequest",
]

class AgencyCodesRequest(BaseModel):
    """
    Code identifying the agency or organization used for site information,
    data sources, and permitting agencies. Agency codes are fixed values
    assigned by the National Water Information System (NWIS).
    """
    agency_name: Optional[str] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "agency_name"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "agency_name": self.agency_name,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class AltitudeDatumsRequest(BaseModel):
    """
    The recommended vertical datum is NAVD88 (North American Vertical
    Datum of 1988) where applicable as stated in Office of Information
    Technical Memo 2002.01. NGVD29 (National Geodetic Vertical Datum of
    1929) and NAVD88 are the only datums that can be converted on output.
    NWIS uses the North American Vertical Datum Conversions (VERTCON) of
    the National Geodetic Survey to convert from NGVD29 to NAVD88 or vice
    versa. Conversions to or from other vertical datums are not available.
    """
    altitude_datum_description: Optional[str] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "altitude_datum_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "altitude_datum_description": self.altitude_datum_description,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class AquiferCodesRequest(BaseModel):
    """
    Local aquifers in USGS data are identified by an aquifer name and
    geohydrologic unit code (a three-digit number related to the age of
    the formation, followed by a 4 or 5 character abbreviation for the
    geologic unit or aquifer name). For the age of formation (aquifer
    age), generally the smaller the number represents the younger the
    geohydrologic unit. Aquifer names and the definition of an aquifer can
    be very subjective. One rock unit may be called different aquifer
    names by different people. Local aquifers and layered aquifers are
    often grouped into larger named regional aquifers or aquifer systems.
    For example, the National Northern Atlantic Coastal Plain aquifer
    system (National aquifer) consists of five layered regional aquifers.
    Each regional aquifer is divided into two or more aquifers which may
    have a different name in each of the states in which the aquifer is
    found.
    """
    aquifer_name: Optional[str] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "aquifer_name"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "aquifer_name": self.aquifer_name,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class AquiferTypesRequest(BaseModel):
    """
    Groundwater occurs in aquifers under two different conditions. Where
    water only partly fills an aquifer, the upper surface is free to rise
    and decline. These aquifers are referred to as unconfined (or water-
    table) aquifers. Where water completely fills an aquifer that is
    overlain by a confining bed, the aquifer is referred to as a confined
    (or artesian) aquifer. When a confined aquifer is penetrated by a
    well, the water level in the well will rise above the top of the
    aquifer (but not necessarily above land surface).
    """
    aquifer_type_description: Optional[str] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "aquifer_type_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "aquifer_type_description": self.aquifer_type_description,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class ChannelMeasurementsRequest(BaseModel):
    """
    Channel measurements taken as part of streamflow field measurements.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    channel_area: Optional[str] = Field(frozen=True, default=None)
    channel_area_unit: Optional[str] = Field(frozen=True, default=None)
    channel_evenness: Optional[str] = Field(frozen=True, default=None)
    channel_flow: Optional[str] = Field(frozen=True, default=None)
    channel_flow_unit: Optional[str] = Field(frozen=True, default=None)
    channel_location_direction: Optional[str] = Field(frozen=True, default=None)
    channel_location_distance: Optional[str] = Field(frozen=True, default=None)
    channel_location_distance_unit: Optional[str] = Field(frozen=True, default=None)
    channel_material: Optional[str] = Field(frozen=True, default=None)
    channel_measurement_type: Optional[str] = Field(frozen=True, default=None)
    channel_name: Optional[str] = Field(frozen=True, default=None)
    channel_stability: Optional[str] = Field(frozen=True, default=None)
    channel_velocity: Optional[str] = Field(frozen=True, default=None)
    channel_velocity_unit: Optional[str] = Field(frozen=True, default=None)
    channel_width: Optional[str] = Field(frozen=True, default=None)
    channel_width_unit: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    datetime: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    field_visit_id: Optional[str] = Field(frozen=True, default=None)
    horizontal_velocity_description: Optional[str] = Field(frozen=True, default=None)
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    longitudinal_velocity_description: Optional[str] = Field(frozen=True, default=None)
    measurement_number: Optional[str] = Field(frozen=True, default=None)
    measurement_type: Optional[str] = Field(frozen=True, default=None)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "monitoring_location_id", "field_visit_id", "measurement_number", "time", "channel_name", "channel_flow", "channel_flow_unit", "channel_width", "channel_width_unit", "channel_area", "channel_area_unit", "channel_velocity", "channel_velocity_unit", "channel_location_distance", "channel_location_distance_unit", "channel_stability", "channel_material", "channel_evenness", "horizontal_velocity_description", "vertical_velocity_description", "longitudinal_velocity_description", "measurement_type", "last_modified", "channel_measurement_type", "channel_location_direction"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    time: Optional[str] = Field(frozen=True, default=None)
    vertical_velocity_description: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "channel_area": self.channel_area,
            "channel_area_unit": self.channel_area_unit,
            "channel_evenness": self.channel_evenness,
            "channel_flow": self.channel_flow,
            "channel_flow_unit": self.channel_flow_unit,
            "channel_location_direction": self.channel_location_direction,
            "channel_location_distance": self.channel_location_distance,
            "channel_location_distance_unit": self.channel_location_distance_unit,
            "channel_material": self.channel_material,
            "channel_measurement_type": self.channel_measurement_type,
            "channel_name": self.channel_name,
            "channel_stability": self.channel_stability,
            "channel_velocity": self.channel_velocity,
            "channel_velocity_unit": self.channel_velocity_unit,
            "channel_width": self.channel_width,
            "channel_width_unit": self.channel_width_unit,
            "crs": self.crs,
            "datetime": self.datetime,
            "f": self.f,
            "field_visit_id": self.field_visit_id,
            "horizontal_velocity_description": self.horizontal_velocity_description,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "longitudinal_velocity_description": self.longitudinal_velocity_description,
            "measurement_number": self.measurement_number,
            "measurement_type": self.measurement_type,
            "monitoring_location_id": self.monitoring_location_id,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "time": self.time,
            "vertical_velocity_description": self.vertical_velocity_description,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class CitationsRequest(BaseModel):
    """
    Citations associated with water measurement methods.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    citation_description: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "citation_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "citation_description": self.citation_description,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class CombinedMetadataRequest(BaseModel):
    """
    This endpoint combines metadata from timeseries and field measurements
    collections by site.
    """
    agency_code: Optional[str] = Field(frozen=True, default=None)
    agency_name: Optional[str] = Field(frozen=True, default=None)
    altitude: Optional[float] = Field(frozen=True, default=None)
    altitude_accuracy: Optional[float] = Field(frozen=True, default=None)
    altitude_method_code: Optional[str] = Field(frozen=True, default=None)
    altitude_method_name: Optional[str] = Field(frozen=True, default=None)
    aquifer_code: Optional[str] = Field(frozen=True, default=None)
    aquifer_type_code: Optional[str] = Field(frozen=True, default=None)
    basin_code: Optional[str] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    begin: Optional[str] = Field(frozen=True, default=None)
    computation_identifier: Optional[str] = Field(frozen=True, default=None)
    construction_date: Optional[str] = Field(frozen=True, default=None)
    contributing_drainage_area: Optional[float] = Field(frozen=True, default=None)
    country_code: Optional[str] = Field(frozen=True, default=None)
    country_name: Optional[str] = Field(frozen=True, default=None)
    county_code: Optional[str] = Field(frozen=True, default=None)
    county_name: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    data_type: Optional[str] = Field(frozen=True, default=None)
    depth_source_code: Optional[str] = Field(frozen=True, default=None)
    district_code: Optional[str] = Field(frozen=True, default=None)
    drainage_area: Optional[float] = Field(frozen=True, default=None)
    end: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    hole_constructed_depth: Optional[float] = Field(frozen=True, default=None)
    horizontal_position_method_code: Optional[str] = Field(frozen=True, default=None)
    horizontal_position_method_name: Optional[str] = Field(frozen=True, default=None)
    horizontal_positional_accuracy: Optional[str] = Field(frozen=True, default=None)
    horizontal_positional_accuracy_code: Optional[str] = Field(frozen=True, default=None)
    hydrologic_unit_code: Optional[str] = Field(frozen=True, default=None)
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    minor_civil_division_code: Optional[str] = Field(frozen=True, default=None)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    monitoring_location_name: Optional[str] = Field(frozen=True, default=None)
    monitoring_location_number: Optional[str] = Field(frozen=True, default=None)
    national_aquifer_code: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    original_horizontal_datum: Optional[str] = Field(frozen=True, default=None)
    original_horizontal_datum_name: Optional[str] = Field(frozen=True, default=None)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    parameter_description: Optional[str] = Field(frozen=True, default=None)
    parameter_name: Optional[str] = Field(frozen=True, default=None)
    parent_time_series_id: Optional[str] = Field(frozen=True, default=None)
    primary: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["monitoring_location_id", "agency_code", "agency_name", "monitoring_location_number", "monitoring_location_name", "district_code", "country_code", "country_name", "state_code", "state_name", "county_code", "county_name", "minor_civil_division_code", "site_type_code", "site_type", "hydrologic_unit_code", "basin_code", "altitude", "altitude_accuracy", "altitude_method_code", "altitude_method_name", "vertical_datum", "vertical_datum_name", "horizontal_positional_accuracy_code", "horizontal_positional_accuracy", "horizontal_position_method_code", "horizontal_position_method_name", "original_horizontal_datum", "original_horizontal_datum_name", "drainage_area", "contributing_drainage_area", "time_zone_abbreviation", "uses_daylight_savings", "construction_date", "aquifer_code", "national_aquifer_code", "aquifer_type_code", "well_constructed_depth", "hole_constructed_depth", "depth_source_code", "id", "unit_of_measure", "parameter_name", "parameter_code", "statistic_id", "last_modified", "begin", "end", "data_type", "computation_identifier", "thresholds", "sublocation_identifier", "primary", "web_description", "parameter_description", "parent_time_series_id"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    site_type: Optional[str] = Field(frozen=True, default=None)
    site_type_code: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    state_code: Optional[str] = Field(frozen=True, default=None)
    state_name: Optional[str] = Field(frozen=True, default=None)
    statistic_id: Optional[str] = Field(frozen=True, default=None)
    sublocation_identifier: Optional[str] = Field(frozen=True, default=None)
    thresholds: Optional[str] = Field(frozen=True, default=None)
    time_zone_abbreviation: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    uses_daylight_savings: Optional[str] = Field(frozen=True, default=None)
    vertical_datum: Optional[str] = Field(frozen=True, default=None)
    vertical_datum_name: Optional[str] = Field(frozen=True, default=None)
    web_description: Optional[str] = Field(frozen=True, default=None)
    well_constructed_depth: Optional[float] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "agency_code": self.agency_code,
            "agency_name": self.agency_name,
            "altitude": self.altitude,
            "altitude_accuracy": self.altitude_accuracy,
            "altitude_method_code": self.altitude_method_code,
            "altitude_method_name": self.altitude_method_name,
            "aquifer_code": self.aquifer_code,
            "aquifer_type_code": self.aquifer_type_code,
            "basin_code": self.basin_code,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "begin": self.begin,
            "computation_identifier": self.computation_identifier,
            "construction_date": self.construction_date,
            "contributing_drainage_area": self.contributing_drainage_area,
            "country_code": self.country_code,
            "country_name": self.country_name,
            "county_code": self.county_code,
            "county_name": self.county_name,
            "crs": self.crs,
            "data_type": self.data_type,
            "depth_source_code": self.depth_source_code,
            "district_code": self.district_code,
            "drainage_area": self.drainage_area,
            "end": self.end,
            "f": self.f,
            "hole_constructed_depth": self.hole_constructed_depth,
            "horizontal_position_method_code": self.horizontal_position_method_code,
            "horizontal_position_method_name": self.horizontal_position_method_name,
            "horizontal_positional_accuracy": self.horizontal_positional_accuracy,
            "horizontal_positional_accuracy_code": self.horizontal_positional_accuracy_code,
            "hydrologic_unit_code": self.hydrologic_unit_code,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "minor_civil_division_code": self.minor_civil_division_code,
            "monitoring_location_id": self.monitoring_location_id,
            "monitoring_location_name": self.monitoring_location_name,
            "monitoring_location_number": self.monitoring_location_number,
            "national_aquifer_code": self.national_aquifer_code,
            "offset": self.offset,
            "original_horizontal_datum": self.original_horizontal_datum,
            "original_horizontal_datum_name": self.original_horizontal_datum_name,
            "parameter_code": self.parameter_code,
            "parameter_description": self.parameter_description,
            "parameter_name": self.parameter_name,
            "parent_time_series_id": self.parent_time_series_id,
            "primary": self.primary,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "site_type": self.site_type,
            "site_type_code": self.site_type_code,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "state_code": self.state_code,
            "state_name": self.state_name,
            "statistic_id": self.statistic_id,
            "sublocation_identifier": self.sublocation_identifier,
            "thresholds": self.thresholds,
            "time_zone_abbreviation": self.time_zone_abbreviation,
            "unit_of_measure": self.unit_of_measure,
            "uses_daylight_savings": self.uses_daylight_savings,
            "vertical_datum": self.vertical_datum,
            "vertical_datum_name": self.vertical_datum_name,
            "web_description": self.web_description,
            "well_constructed_depth": self.well_constructed_depth,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class ContinuousRequest(BaseModel):
    """
    Continuous data are collected via automated sensors installed at a
    monitoring location. They are collected at a high frequency and often
    at a fixed 15-minute interval. Depending on the specific monitoring
    location, the data may be transmitted automatically via telemetry and
    be available on WDFN within minutes of collection, while other times
    the delivery of data may be delayed if the monitoring location does
    not have the capacity to automatically transmit data. Continuous data
    are described by parameter name and parameter code (pcode). These data
    might also be referred to as "instantaneous values" or "IV".
    """
    approval_status: Optional[Literal["Provisional", "Approved"]] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    datetime: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = Field(frozen=True, default=None)
    qualifier: Optional[str] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    statistic_id: Optional[str] = Field(frozen=True, default=None)
    time: Optional[str] = Field(frozen=True, default=None)
    time_series_id: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    value: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": self.approval_status,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "datetime": self.datetime,
            "f": self.f,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "monitoring_location_id": self.monitoring_location_id,
            "offset": self.offset,
            "parameter_code": self.parameter_code,
            "properties": self.properties,
            "qualifier": self.qualifier,
            "filter": self.query_filter,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "statistic_id": self.statistic_id,
            "time": self.time,
            "time_series_id": self.time_series_id,
            "unit_of_measure": self.unit_of_measure,
            "value": self.value,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class CoordinateAccuracyCodesRequest(BaseModel):
    """
    Appropriate code on the schedule to indicate the accuracy of the
    latitude-longitude values.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    coordinate_accuracy_description: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "coordinate_accuracy_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "coordinate_accuracy_description": self.coordinate_accuracy_description,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class CoordinateDatumCodesRequest(BaseModel):
    """
    Horizontal datum code for the latitude/longitude coordinates. There
    are currently more than 300 horizontal datums available for entry.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    coordinate_datum_description: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "coordinate_datum_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "coordinate_datum_description": self.coordinate_datum_description,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class CoordinateMethodCodesRequest(BaseModel):
    """
    Methods used to determine latitude-longitude values.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    coordinate_method_description: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "coordinate_method_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "coordinate_method_description": self.coordinate_method_description,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class CountiesRequest(BaseModel):
    """
    The name of the county or county equivalent (parish, borough, planning
    reagion, etc.) in which the site is located. List includes Census
    Bureau FIPS county codes, names and associated Country and State.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    country_code: Optional[str] = Field(frozen=True, default=None)
    county_fips_code: Optional[str] = Field(frozen=True, default=None)
    county_name: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "country_code", "state_fips_code", "county_fips_code", "county_name"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    state_fips_code: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "country_code": self.country_code,
            "county_fips_code": self.county_fips_code,
            "county_name": self.county_name,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "state_fips_code": self.state_fips_code,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class CountriesRequest(BaseModel):
    """
    FIPS country codes and names.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    country_name: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "country_name"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "country_name": self.country_name,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class DailyRequest(BaseModel):
    """
    Daily data provide one data value to represent water conditions for
    the day. Throughout much of the history of the USGS, the primary water
    data available was daily data collected manually at the monitoring
    location once each day. With improved availability of computer storage
    and automated transmission of data, the daily data published today are
    generally a statistical summary or metric of the continuous data
    collected each day, such as the daily mean, minimum, or maximum value.
    Daily data are automatically calculated from the continuous data of
    the same parameter code and are described by parameter code and a
    statistic code. These data have also been referred to as “daily
    values” or “DV”.
    """
    approval_status: Optional[Literal["Provisional", "Approved"]] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    datetime: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = Field(frozen=True, default=None)
    qualifier: Optional[str] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    statistic_id: Optional[str] = Field(frozen=True, default=None)
    time: Optional[str] = Field(frozen=True, default=None)
    time_series_id: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    value: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": self.approval_status,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "datetime": self.datetime,
            "f": self.f,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "monitoring_location_id": self.monitoring_location_id,
            "offset": self.offset,
            "parameter_code": self.parameter_code,
            "properties": self.properties,
            "qualifier": self.qualifier,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "statistic_id": self.statistic_id,
            "time": self.time,
            "time_series_id": self.time_series_id,
            "unit_of_measure": self.unit_of_measure,
            "value": self.value,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class FieldMeasurementsRequest(BaseModel):
    """
    Field measurements are physically measured values collected during a
    visit to the monitoring location. Field measurements consist of
    measurements of gage height and discharge, and readings of groundwater
    levels, and are primarily used as calibration readings for the
    automated sensors collecting continuous data. They are collected at a
    low frequency, and delivery of the data in WDFN may be delayed due to
    data processing time.
    """
    approval_status: Optional[Literal["Provisional", "Approved"]] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    control_condition: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    datetime: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    field_measurements_series_id: Optional[str] = Field(frozen=True, default=None)
    field_visit_id: Optional[str] = Field(frozen=True, default=None)
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    measurement_rated: Optional[str] = Field(frozen=True, default=None)
    measuring_agency: Optional[str] = Field(frozen=True, default=None)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    observing_procedure: Optional[str] = Field(frozen=True, default=None)
    observing_procedure_code: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "field_measurements_series_id", "field_visit_id", "parameter_code", "monitoring_location_id", "observing_procedure_code", "observing_procedure", "value", "unit_of_measure", "time", "qualifier", "vertical_datum", "approval_status", "measuring_agency", "last_modified", "control_condition", "measurement_rated"]]] = Field(frozen=True, default=None)
    qualifier: Optional[str] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    time: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    value: Optional[str] = Field(frozen=True, default=None)
    vertical_datum: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": self.approval_status,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "control_condition": self.control_condition,
            "crs": self.crs,
            "datetime": self.datetime,
            "f": self.f,
            "field_measurements_series_id": self.field_measurements_series_id,
            "field_visit_id": self.field_visit_id,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "measurement_rated": self.measurement_rated,
            "measuring_agency": self.measuring_agency,
            "monitoring_location_id": self.monitoring_location_id,
            "observing_procedure": self.observing_procedure,
            "observing_procedure_code": self.observing_procedure_code,
            "offset": self.offset,
            "parameter_code": self.parameter_code,
            "properties": self.properties,
            "qualifier": self.qualifier,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "time": self.time,
            "unit_of_measure": self.unit_of_measure,
            "value": self.value,
            "vertical_datum": self.vertical_datum,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class FieldMeasurementsMetadataRequest(BaseModel):
    """
    This endpoint provides metadata about field measurement collections,
    including when the earliest and most recent observations for a
    parameter occurred at a monitoring location and its units.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    begin: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    end: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    parameter_description: Optional[str] = Field(frozen=True, default=None)
    parameter_name: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "monitoring_location_id", "parameter_code", "parameter_name", "parameter_description", "begin", "end", "last_modified"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "begin": self.begin,
            "crs": self.crs,
            "end": self.end,
            "f": self.f,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "monitoring_location_id": self.monitoring_location_id,
            "offset": self.offset,
            "parameter_code": self.parameter_code,
            "parameter_description": self.parameter_description,
            "parameter_name": self.parameter_name,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class HydrologicUnitCodesRequest(BaseModel):
    """
    Hydrologic units are geographic areas representing part or all of a
    surface drainage basin or distinct hydrologic feature identified by a
    unique number (HUC), and a name. The United States is divided and sub-
    divided into successively smaller hydrologic units which are
    classified into four levels: regions, sub-regions, accounting units,
    and cataloging units. Each unit consists of two to eight digits based
    on the four levels of classification in the hydrologic unit system.
    Additional information can be found at
    <https://water.usgs.gov/GIS/huc.html>.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    hydrologic_unit_classification_code: Optional[str] = Field(frozen=True, default=None)
    hydrologic_unit_name: Optional[str] = Field(frozen=True, default=None)
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "hydrologic_unit_name", "hydrologic_unit_classification_code"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "hydrologic_unit_classification_code": self.hydrologic_unit_classification_code,
            "hydrologic_unit_name": self.hydrologic_unit_name,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class LatestContinuousRequest(BaseModel):
    """
    This endpoint provides the most recent observation for each time
    series of continuous data. Continuous data are collected via automated
    sensors installed at a monitoring location. They are collected at a
    high frequency and often at a fixed 15-minute interval. Depending on
    the specific monitoring location, the data may be transmitted
    automatically via telemetry and be available on WDFN within minutes of
    collection, while other times the delivery of data may be delayed if
    the monitoring location does not have the capacity to automatically
    transmit data. Continuous data are described by parameter name and
    parameter code. These data might also be referred to as "instantaneous
    values" or "IV"
    """
    approval_status: Optional[Literal["Provisional", "Approved"]] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    datetime: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = Field(frozen=True, default=None)
    qualifier: Optional[str] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    statistic_id: Optional[str] = Field(frozen=True, default=None)
    time: Optional[str] = Field(frozen=True, default=None)
    time_series_id: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    value: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": self.approval_status,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "datetime": self.datetime,
            "f": self.f,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "monitoring_location_id": self.monitoring_location_id,
            "offset": self.offset,
            "parameter_code": self.parameter_code,
            "properties": self.properties,
            "qualifier": self.qualifier,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "statistic_id": self.statistic_id,
            "time": self.time,
            "time_series_id": self.time_series_id,
            "unit_of_measure": self.unit_of_measure,
            "value": self.value,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class LatestDailyRequest(BaseModel):
    """
    Daily data provide one data value to represent water conditions for
    the day. Throughout much of the history of the USGS, the primary water
    data available was daily data collected manually at the monitoring
    location once each day. With improved availability of computer storage
    and automated transmission of data, the daily data published today are
    generally a statistical summary or metric of the continuous data
    collected each day, such as the daily mean, minimum, or maximum value.
    Daily data are automatically calculated from the continuous data of
    the same parameter code and are described by parameter code and a
    statistic code. These data have also been referred to as “daily
    values” or “DV”.
    """
    approval_status: Optional[Literal["Provisional", "Approved"]] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    datetime: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = Field(frozen=True, default=None)
    qualifier: Optional[str] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    statistic_id: Optional[str] = Field(frozen=True, default=None)
    time: Optional[str] = Field(frozen=True, default=None)
    time_series_id: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    value: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": self.approval_status,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "datetime": self.datetime,
            "f": self.f,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "monitoring_location_id": self.monitoring_location_id,
            "offset": self.offset,
            "parameter_code": self.parameter_code,
            "properties": self.properties,
            "qualifier": self.qualifier,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "statistic_id": self.statistic_id,
            "time": self.time,
            "time_series_id": self.time_series_id,
            "unit_of_measure": self.unit_of_measure,
            "value": self.value,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class MediumCodesRequest(BaseModel):
    """
    Medium refers to the specific environmental medium from which the
    sample was collected. Medium type differs from site type because one
    site type, such as surface water, could have data for several media,
    such as water, bottom sediment, fish tissue, and others.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    legacy_medium_code: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    medium_description: Optional[str] = Field(frozen=True, default=None)
    medium_name: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "medium_name", "medium_description", "legacy_medium_code"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "legacy_medium_code": self.legacy_medium_code,
            "limit": self.limit,
            "medium_description": self.medium_description,
            "medium_name": self.medium_name,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class MethodCategoriesRequest(BaseModel):
    """
    Categorical standards for methods describing the associated data's
    appropriateness for an intended use.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    method_category_description: Optional[str] = Field(frozen=True, default=None)
    method_category_name: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "method_category_name", "method_category_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "method_category_description": self.method_category_description,
            "method_category_name": self.method_category_name,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class MethodCitationsRequest(BaseModel):
    """
    Citation identifiers for water measurement methods.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    citation_method_number: Optional[str] = Field(frozen=True, default=None)
    citation_name: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    method_id: Optional[str] = Field(frozen=True, default=None)
    method_source: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "method_id", "citation_name", "citation_method_number", "method_source"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[int] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "citation_method_number": self.citation_method_number,
            "citation_name": self.citation_name,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "method_id": self.method_id,
            "method_source": self.method_source,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class MethodsRequest(BaseModel):
    """
    Water measurement or water-quality analytical methods. Codes and
    descriptions defining a method for calculating or measuring the value
    of a water quality or quantity parameter. Method codes are associated
    with one or many parameter codes.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    method_category: Optional[str] = Field(frozen=True, default=None)
    method_description: Optional[str] = Field(frozen=True, default=None)
    method_name: Optional[str] = Field(frozen=True, default=None)
    method_type: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "method_type", "method_category", "method_name", "method_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "method_category": self.method_category,
            "method_description": self.method_description,
            "method_name": self.method_name,
            "method_type": self.method_type,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class MonitoringLocationsRequest(BaseModel):
    """
    Location information is basic information about the monitoring
    location including the name, identifier, agency responsible for data
    collection, and the date the location was established. It also
    includes information about the type of location, such as stream, lake,
    or groundwater, and geographic information about the location, such as
    state, county, latitude and longitude, and hydrologic unit code (HUC).
    """
    agency_code: Optional[str] = Field(frozen=True, default=None)
    agency_name: Optional[str] = Field(frozen=True, default=None)
    altitude: Optional[float] = Field(frozen=True, default=None)
    altitude_accuracy: Optional[float] = Field(frozen=True, default=None)
    altitude_method_code: Optional[str] = Field(frozen=True, default=None)
    altitude_method_name: Optional[str] = Field(frozen=True, default=None)
    aquifer_code: Optional[str] = Field(frozen=True, default=None)
    aquifer_type_code: Optional[str] = Field(frozen=True, default=None)
    basin_code: Optional[str] = Field(frozen=True, default=None)
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    construction_date: Optional[str] = Field(frozen=True, default=None)
    contributing_drainage_area: Optional[float] = Field(frozen=True, default=None)
    country_code: Optional[str] = Field(frozen=True, default=None)
    country_name: Optional[str] = Field(frozen=True, default=None)
    county_code: Optional[str] = Field(frozen=True, default=None)
    county_name: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    depth_source_code: Optional[str] = Field(frozen=True, default=None)
    district_code: Optional[str] = Field(frozen=True, default=None)
    drainage_area: Optional[float] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    hole_constructed_depth: Optional[float] = Field(frozen=True, default=None)
    horizontal_position_method_code: Optional[str] = Field(frozen=True, default=None)
    horizontal_position_method_name: Optional[str] = Field(frozen=True, default=None)
    horizontal_positional_accuracy: Optional[str] = Field(frozen=True, default=None)
    horizontal_positional_accuracy_code: Optional[str] = Field(frozen=True, default=None)
    hydrologic_unit_code: Optional[str] = Field(frozen=True, default=None)
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    minor_civil_division_code: Optional[str] = Field(frozen=True, default=None)
    monitoring_location_name: Optional[str] = Field(frozen=True, default=None)
    monitoring_location_number: Optional[str] = Field(frozen=True, default=None)
    national_aquifer_code: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    original_horizontal_datum: Optional[str] = Field(frozen=True, default=None)
    original_horizontal_datum_name: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "agency_code", "agency_name", "monitoring_location_number", "monitoring_location_name", "district_code", "country_code", "country_name", "state_code", "state_name", "county_code", "county_name", "minor_civil_division_code", "site_type_code", "site_type", "hydrologic_unit_code", "basin_code", "altitude", "altitude_accuracy", "altitude_method_code", "altitude_method_name", "vertical_datum", "vertical_datum_name", "horizontal_positional_accuracy_code", "horizontal_positional_accuracy", "horizontal_position_method_code", "horizontal_position_method_name", "original_horizontal_datum", "original_horizontal_datum_name", "drainage_area", "contributing_drainage_area", "time_zone_abbreviation", "uses_daylight_savings", "construction_date", "aquifer_code", "national_aquifer_code", "aquifer_type_code", "well_constructed_depth", "hole_constructed_depth", "depth_source_code", "revision_note", "revision_created", "revision_modified"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    revision_created: Optional[str] = Field(frozen=True, default=None)
    revision_modified: Optional[str] = Field(frozen=True, default=None)
    revision_note: Optional[str] = Field(frozen=True, default=None)
    site_type: Optional[str] = Field(frozen=True, default=None)
    site_type_code: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    state_code: Optional[str] = Field(frozen=True, default=None)
    state_name: Optional[str] = Field(frozen=True, default=None)
    time_zone_abbreviation: Optional[str] = Field(frozen=True, default=None)
    uses_daylight_savings: Optional[str] = Field(frozen=True, default=None)
    vertical_datum: Optional[str] = Field(frozen=True, default=None)
    vertical_datum_name: Optional[str] = Field(frozen=True, default=None)
    well_constructed_depth: Optional[float] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "agency_code": self.agency_code,
            "agency_name": self.agency_name,
            "altitude": self.altitude,
            "altitude_accuracy": self.altitude_accuracy,
            "altitude_method_code": self.altitude_method_code,
            "altitude_method_name": self.altitude_method_name,
            "aquifer_code": self.aquifer_code,
            "aquifer_type_code": self.aquifer_type_code,
            "basin_code": self.basin_code,
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "construction_date": self.construction_date,
            "contributing_drainage_area": self.contributing_drainage_area,
            "country_code": self.country_code,
            "country_name": self.country_name,
            "county_code": self.county_code,
            "county_name": self.county_name,
            "crs": self.crs,
            "depth_source_code": self.depth_source_code,
            "district_code": self.district_code,
            "drainage_area": self.drainage_area,
            "f": self.f,
            "hole_constructed_depth": self.hole_constructed_depth,
            "horizontal_position_method_code": self.horizontal_position_method_code,
            "horizontal_position_method_name": self.horizontal_position_method_name,
            "horizontal_positional_accuracy": self.horizontal_positional_accuracy,
            "horizontal_positional_accuracy_code": self.horizontal_positional_accuracy_code,
            "hydrologic_unit_code": self.hydrologic_unit_code,
            "lang": self.lang,
            "limit": self.limit,
            "minor_civil_division_code": self.minor_civil_division_code,
            "monitoring_location_name": self.monitoring_location_name,
            "monitoring_location_number": self.monitoring_location_number,
            "national_aquifer_code": self.national_aquifer_code,
            "offset": self.offset,
            "original_horizontal_datum": self.original_horizontal_datum,
            "original_horizontal_datum_name": self.original_horizontal_datum_name,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "revision_created": self.revision_created,
            "revision_modified": self.revision_modified,
            "revision_note": self.revision_note,
            "site_type": self.site_type,
            "site_type_code": self.site_type_code,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "state_code": self.state_code,
            "state_name": self.state_name,
            "time_zone_abbreviation": self.time_zone_abbreviation,
            "uses_daylight_savings": self.uses_daylight_savings,
            "vertical_datum": self.vertical_datum,
            "vertical_datum_name": self.vertical_datum_name,
            "well_constructed_depth": self.well_constructed_depth,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class NationalAquiferCodesRequest(BaseModel):
    """
    National aquifers are the principal aquifers or aquifer systems in the
    United States, defined as regionally extensive aquifers or aquifer
    systems that have the potential to be used as a source of potable
    water.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    national_aquifer_name: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "national_aquifer_name"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "national_aquifer_name": self.national_aquifer_name,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class ParameterCodesRequest(BaseModel):
    """
    Parameter codes are 5-digit codes and associated descriptions used to
    identify the constituent measured and the units of measure. Some
    parameter code definitions include information about the sampling
    matrix, fraction, and methods used to measure the constituent. Some
    parameters are fixed-value (fxd) numeric codes having textual meaning
    (for example: parameter code 00041 is a weather code parameter, code
    of 60 means rain), but more commonly represent a numeric value for
    chemical, physical, or biological data.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    epa_equivalence: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    medium: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_description: Optional[str] = Field(frozen=True, default=None)
    parameter_group_code: Optional[str] = Field(frozen=True, default=None)
    parameter_name: Optional[str] = Field(frozen=True, default=None)
    particle_size_basis: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "parameter_name", "unit_of_measure", "parameter_group_code", "parameter_description", "medium", "statistical_basis", "time_basis", "weight_basis", "particle_size_basis", "sample_fraction", "temperature_basis", "epa_equivalence"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    sample_fraction: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    statistical_basis: Optional[str] = Field(frozen=True, default=None)
    temperature_basis: Optional[str] = Field(frozen=True, default=None)
    time_basis: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    weight_basis: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "epa_equivalence": self.epa_equivalence,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "medium": self.medium,
            "offset": self.offset,
            "parameter_description": self.parameter_description,
            "parameter_group_code": self.parameter_group_code,
            "parameter_name": self.parameter_name,
            "particle_size_basis": self.particle_size_basis,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "sample_fraction": self.sample_fraction,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "statistical_basis": self.statistical_basis,
            "temperature_basis": self.temperature_basis,
            "time_basis": self.time_basis,
            "unit_of_measure": self.unit_of_measure,
            "weight_basis": self.weight_basis,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class PeaksRequest(BaseModel):
    """
    Annual peak flow values are the maximum instantaneous streamflow
    values recorded at a particular site for the entire water year from
    October 1 to September 30. Note that the annual peak flow value may
    not occur at the same time the maximum water level occurs due to
    conditions such as backwater, tidal fluctuations, etc.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    day: Optional[int] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    month: Optional[int] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    peak_since: Optional[int] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["time_series_id", "monitoring_location_id", "parameter_code", "id", "unit_of_measure", "value", "last_modified", "time", "water_year", "year", "month", "day", "time_of_day", "peak_since"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    time: Optional[str] = Field(frozen=True, default=None)
    time_of_day: Optional[str] = Field(frozen=True, default=None)
    time_series_id: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    value: Optional[str] = Field(frozen=True, default=None)
    water_year: Optional[int] = Field(frozen=True, default=None)
    year: Optional[int] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "day": self.day,
            "f": self.f,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "monitoring_location_id": self.monitoring_location_id,
            "month": self.month,
            "offset": self.offset,
            "parameter_code": self.parameter_code,
            "peak_since": self.peak_since,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "time": self.time,
            "time_of_day": self.time_of_day,
            "time_series_id": self.time_series_id,
            "unit_of_measure": self.unit_of_measure,
            "value": self.value,
            "water_year": self.water_year,
            "year": self.year,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class ReliabilityCodesRequest(BaseModel):
    """
    Code indicating the reliability of the data available for the site.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "reliability_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    reliability_description: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "reliability_description": self.reliability_description,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class SiteTypesRequest(BaseModel):
    """
    The hydrologic cycle setting or a man-made feature thought to affect
    the hydrologic conditions measured at a site. Primary and secondary
    site types associated with data collection sites. All sites have a
    primary site type, and may additionally have a secondary site type
    that further describes the location.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "site_type_primary_flag", "site_type_name", "site_type_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    site_type_description: Optional[str] = Field(frozen=True, default=None)
    site_type_name: Optional[str] = Field(frozen=True, default=None)
    site_type_primary_flag: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "site_type_description": self.site_type_description,
            "site_type_name": self.site_type_name,
            "site_type_primary_flag": self.site_type_primary_flag,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class StatesRequest(BaseModel):
    """
    State name or territory. Includes U.S. states and foreign entities
    classified under FIPS as 'Principal Administrative Divisions'.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    country_code: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "country_code", "state_fips_code", "state_name", "state_postal_code"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    state_fips_code: Optional[str] = Field(frozen=True, default=None)
    state_name: Optional[str] = Field(frozen=True, default=None)
    state_postal_code: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "country_code": self.country_code,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "state_fips_code": self.state_fips_code,
            "state_name": self.state_name,
            "state_postal_code": self.state_postal_code,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class StatisticCodesRequest(BaseModel):
    """
    Statistic codes.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "statistic_name", "statistic_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    statistic_description: Optional[str] = Field(frozen=True, default=None)
    statistic_name: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "statistic_description": self.statistic_description,
            "statistic_name": self.statistic_name,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class TimeSeriesMetadataRequest(BaseModel):
    """
    Daily data and continuous measurements are grouped into time series,
    which represent a collection of observations of a single parameter,
    potentially aggregated using a standard statistic, at a single
    monitoring location. This endpoint provides metadata about those time
    series, including their operational thresholds, units of measurement,
    and when the earliest and most recent observations in a time series
    occurred.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    begin: Optional[str] = Field(frozen=True, default=None)
    begin_utc: Optional[str] = Field(frozen=True, default=None)
    computation_identifier: Optional[str] = Field(frozen=True, default=None)
    computation_period_identifier: Optional[str] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    end: Optional[str] = Field(frozen=True, default=None)
    end_utc: Optional[str] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    hydrologic_unit_code: Optional[str] = Field(frozen=True, default=None)
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    last_modified: Optional[str] = Field(frozen=True, default=None)
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000)
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    parameter_code: Optional[str] = Field(frozen=True, default=None)
    parameter_description: Optional[str] = Field(frozen=True, default=None)
    parameter_name: Optional[str] = Field(frozen=True, default=None)
    parent_time_series_id: Optional[str] = Field(frozen=True, default=None)
    primary: Optional[str] = Field(frozen=True, default=None)
    properties: Optional[Sequence[Literal["id", "unit_of_measure", "parameter_name", "parameter_code", "statistic_id", "hydrologic_unit_code", "state_name", "last_modified", "begin", "end", "begin_utc", "end_utc", "computation_period_identifier", "computation_identifier", "thresholds", "sublocation_identifier", "primary", "monitoring_location_id", "web_description", "parameter_description", "parent_time_series_id"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    state_name: Optional[str] = Field(frozen=True, default=None)
    statistic_id: Optional[str] = Field(frozen=True, default=None)
    sublocation_identifier: Optional[str] = Field(frozen=True, default=None)
    thresholds: Optional[str] = Field(frozen=True, default=None)
    unit_of_measure: Optional[str] = Field(frozen=True, default=None)
    web_description: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "begin": self.begin,
            "begin_utc": self.begin_utc,
            "computation_identifier": self.computation_identifier,
            "computation_period_identifier": self.computation_period_identifier,
            "crs": self.crs,
            "end": self.end,
            "end_utc": self.end_utc,
            "f": self.f,
            "hydrologic_unit_code": self.hydrologic_unit_code,
            "lang": self.lang,
            "last_modified": self.last_modified,
            "limit": self.limit,
            "monitoring_location_id": self.monitoring_location_id,
            "offset": self.offset,
            "parameter_code": self.parameter_code,
            "parameter_description": self.parameter_description,
            "parameter_name": self.parameter_name,
            "parent_time_series_id": self.parent_time_series_id,
            "primary": self.primary,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "state_name": self.state_name,
            "statistic_id": self.statistic_id,
            "sublocation_identifier": self.sublocation_identifier,
            "thresholds": self.thresholds,
            "unit_of_measure": self.unit_of_measure,
            "web_description": self.web_description,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class TimeZoneCodesRequest(BaseModel):
    """
    The ISO 8601 standard defines time zone offsets as a numerical value
    added to a local time to convert it to Coordinated Universal Time
    (UTC), either as +hh:mm or -hh:mm, or represented by the letter Z to
    explicitly indicate UTC. For example, +05:30 means 5 hours and 30
    minutes ahead of UTC, while -08:00 means 8 hours behind UTC. The
    offset Z specifically signifies UTC.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "time_zone_name", "time_zone_description", "time_zone_utc_offset", "time_zone_daylight_savings_time_code", "time_zone_daylight_savings_time_name", "time_zone_daylight_savings_utc_offset"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    time_zone_daylight_savings_time_code: Optional[str] = Field(frozen=True, default=None)
    time_zone_daylight_savings_time_name: Optional[str] = Field(frozen=True, default=None)
    time_zone_daylight_savings_utc_offset: Optional[str] = Field(frozen=True, default=None)
    time_zone_description: Optional[str] = Field(frozen=True, default=None)
    time_zone_name: Optional[str] = Field(frozen=True, default=None)
    time_zone_utc_offset: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "time_zone_daylight_savings_time_code": self.time_zone_daylight_savings_time_code,
            "time_zone_daylight_savings_time_name": self.time_zone_daylight_savings_time_name,
            "time_zone_daylight_savings_utc_offset": self.time_zone_daylight_savings_utc_offset,
            "time_zone_description": self.time_zone_description,
            "time_zone_name": self.time_zone_name,
            "time_zone_utc_offset": self.time_zone_utc_offset,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}

class TopographicCodesRequest(BaseModel):
    """
    The code that best describes the topographic setting in which the site
    is located. Topographic setting refers to the geomorphic features in
    the vicinity of the site.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None)
    bbox_crs: Optional[URL] = Field(frozen=True, default=None)
    crs: Optional[URL] = Field(frozen=True, default=None)
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json")
    full_topography_description: Optional[str] = Field(frozen=True, default=None)
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000)
    offset: Optional[int] = Field(frozen=True, default=0, ge=0)
    properties: Optional[Sequence[Literal["id", "topography_name", "short_topography_description", "full_topography_description"]]] = Field(frozen=True, default=None)
    query_filter: Optional[str] = Field(frozen=True, default=None)
    query_id: Optional[str] = Field(frozen=True, default=None)
    short_topography_description: Optional[str] = Field(frozen=True, default=None)
    skipgeometry: Optional[bool] = Field(frozen=True, default=False)
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None)
    topography_name: Optional[str] = Field(frozen=True, default=None)

    def generate_query(self) -> dict[str, Any]:
        """Translates class attributes to valid API parameters. Returns a URL
        builder compatible query.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": self.bbox,
            "bbox-crs": self.bbox_crs,
            "crs": self.crs,
            "f": self.f,
            "full_topography_description": self.full_topography_description,
            "lang": self.lang,
            "limit": self.limit,
            "offset": self.offset,
            "properties": self.properties,
            "filter": self.query_filter,
            "id": self.query_id,
            "short_topography_description": self.short_topography_description,
            "skipGeometry": self.skipgeometry,
            "sortby": self.sortby,
            "topography_name": self.topography_name,
        }

        # Ignore None
        return {k: v for k, v in query.items() if v is not None}


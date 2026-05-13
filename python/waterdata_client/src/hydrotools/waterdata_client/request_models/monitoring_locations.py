# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
"""This is a Jinja2 auto-generated module. This module contains individual
pydantic request models for USGS OGC API items endpoints. These classes are generated
by inspecting the USGS OGC API JSON schema and identifying all "items" endpoints.

Package version: 0.8.0a0
Generation script: build_request_models.py
Generated: 2026-05-13 17:31:40 Z
JSON Schema source: https://api.waterdata.usgs.gov/ogcapi/v0/openapi?f=json
JSON Schema version: 0.49.2
OpenAPI version: 3.0.2
"""
from typing import Sequence, Literal, Optional, Any
from yarl import URL
from pydantic import BaseModel, Field

class MonitoringLocationsRequest(BaseModel):
    """
    Location information is basic information about the monitoring
    location including the name, identifier, agency responsible for data
    collection, and the date the location was established. It also
    includes information about the type of location, such as stream, lake,
    or groundwater, and geographic information about the location, such as
    state, county, latitude and longitude, and hydrologic unit code (HUC).
    """
    agency_code: Optional[str] = Field(frozen=True, default=None, description="The agency that is reporting the data.")
    agency_name: Optional[str] = Field(frozen=True, default=None, description="The name of the agency that is reporting the data.")
    altitude: Optional[float] = Field(frozen=True, default=None, description="Altitude of the monitoring location referenced to the specified Vertical Datum.")
    altitude_accuracy: Optional[float] = Field(frozen=True, default=None, description="Accuracy of the altitude, in feet.")
    altitude_method_code: Optional[str] = Field(frozen=True, default=None, description="Codes representing the method used to measure altitude.")
    altitude_method_name: Optional[str] = Field(frozen=True, default=None, description="The name of the method used to measure altitude.")
    aquifer_code: Optional[str] = Field(frozen=True, default=None, description="Local aquifers in the USGS water resources data base are identified by a geohydrologic unit code (a three-digit number related to the age of the formation, followed by a 4 or 5 character abbreviation for the geologic unit or aquifer name).")
    aquifer_type_code: Optional[str] = Field(frozen=True, default=None, description="Describes the confinement status of an aquifer at the monitoring location.")
    basin_code: Optional[str] = Field(frozen=True, default=None, description="The Basin Code or  drainage basin code  is a two-digit code that further subdivides the 8-digit hydrologic-unit code.")
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None, description="Only features that have a geometry that intersects the bounding box are selected.")
    bbox_crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the given bbox coordinates.")
    construction_date: Optional[str] = Field(frozen=True, default=None, description="Date the well was completed.")
    contributing_drainage_area: Optional[float] = Field(frozen=True, default=None, description="The contributing drainage area of a lake, stream, wetland, or estuary monitoring location, in square miles.")
    country_code: Optional[str] = Field(frozen=True, default=None, description="The code for the country in which the monitoring location is located.")
    country_name: Optional[str] = Field(frozen=True, default=None, description="The name of the country in which the monitoring location is located.")
    county_code: Optional[str] = Field(frozen=True, default=None, description="The code for the county or county equivalent (parish, borough, etc.")
    county_name: Optional[str] = Field(frozen=True, default=None, description="The name of the county or county equivalent (parish, borough, etc.")
    crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the results.")
    depth_source_code: Optional[str] = Field(frozen=True, default=None, description="A code indicating the source of water-level data.")
    district_code: Optional[str] = Field(frozen=True, default=None, description="The Water Science Centers (WSCs) across the United States use the FIPS state code as the district code.")
    drainage_area: Optional[float] = Field(frozen=True, default=None, description="The area enclosed by a topographic divide from which direct surface runoff from precipitation normally drains by gravity into the stream above that point.")
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json", description="The optional f parameter indicates the output format which the server shall provide as part of the response document.")
    hole_constructed_depth: Optional[float] = Field(frozen=True, default=None, description="The total depth to which the hole is drilled, in feet below land surface datum.")
    horizontal_position_method_code: Optional[str] = Field(frozen=True, default=None, description="Indicates the method used to determine latitude longitude values.")
    horizontal_position_method_name: Optional[str] = Field(frozen=True, default=None, description="Indicates the method used to determine latitude longitude values.")
    horizontal_positional_accuracy: Optional[str] = Field(frozen=True, default=None, description="Indicates the accuracy of the latitude longitude values.")
    horizontal_positional_accuracy_code: Optional[str] = Field(frozen=True, default=None, description="Indicates the accuracy of the latitude longitude values.")
    hydrologic_unit_code: Optional[str] = Field(frozen=True, default=None, description="The United States is divided and sub-divided into successively smaller hydrologic units which are classified into four levels: regions, sub-regions, accounting units, and cataloging units.")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US", description="The optional lang parameter instructs the server return a response in a certain language, if supported.")
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000, description="The optional limit parameter limits the number of items that are presented in the response document (maximum=50000, default=10).")
    minor_civil_division_code: Optional[str] = Field(frozen=True, default=None, description="Codes for primary governmental or administrative divisions of the county or county equivalent in which the monitoring location is located.")
    monitoring_location_name: Optional[str] = Field(frozen=True, default=None, description="This is the official name of the monitoring location in the database.")
    monitoring_location_number: Optional[str] = Field(frozen=True, default=None, description="Each monitoring location in the USGS data base has a unique 8- to 15-digit identification number.")
    national_aquifer_code: Optional[str] = Field(frozen=True, default=None, description="National aquifers are the principal aquifers or aquifer systems in the United States, defined as regionally extensive aquifers or aquifer systems that have the potential to be used as a source of potable water.")
    offset: Optional[int] = Field(frozen=True, default=0, ge=0, description="The optional offset parameter indicates the index within the result set from which the server shall begin presenting results in the response document.")
    original_horizontal_datum: Optional[str] = Field(frozen=True, default=None, description="Coordinates are published in EPSG:4326 / WGS84 / World Geodetic System 1984.")
    original_horizontal_datum_name: Optional[str] = Field(frozen=True, default=None, description="Coordinates are published in EPSG:4326 / WGS84 / World Geodetic System 1984.")
    properties: Optional[Sequence[Literal["id", "agency_code", "agency_name", "monitoring_location_number", "monitoring_location_name", "district_code", "country_code", "country_name", "state_code", "state_name", "county_code", "county_name", "minor_civil_division_code", "site_type_code", "site_type", "hydrologic_unit_code", "basin_code", "altitude", "altitude_accuracy", "altitude_method_code", "altitude_method_name", "vertical_datum", "vertical_datum_name", "horizontal_positional_accuracy_code", "horizontal_positional_accuracy", "horizontal_position_method_code", "horizontal_position_method_name", "original_horizontal_datum", "original_horizontal_datum_name", "drainage_area", "contributing_drainage_area", "time_zone_abbreviation", "uses_daylight_savings", "construction_date", "aquifer_code", "national_aquifer_code", "aquifer_type_code", "well_constructed_depth", "hole_constructed_depth", "depth_source_code", "revision_note", "revision_created", "revision_modified"]]] = Field(frozen=True, default=None, description="The properties that should be included.")
    query_filter: Optional[str] = Field(frozen=True, default=None, description="CQL Text filter expression.")
    query_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single monitoring location.")
    revision_created: Optional[str] = Field(frozen=True, default=None, description="The date a revision statement was created.")
    revision_modified: Optional[str] = Field(frozen=True, default=None, description="The most recent date a revision statement was modified.")
    revision_note: Optional[str] = Field(frozen=True, default=None, description="Approved water data are considered published record, but on occasion changes or deletions (revisions) must be made to data after they are approved.")
    site_type: Optional[str] = Field(frozen=True, default=None, description="A description of the hydrologic setting of the monitoring location.")
    site_type_code: Optional[str] = Field(frozen=True, default=None, description="A code describing the hydrologic setting of the monitoring location.")
    skipgeometry: Optional[bool] = Field(frozen=True, default=False, description="This option can be used to skip response geometries for each feature.")
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None, description="Specifies a comma-separated list of property names by which the response shall be sorted.")
    state_code: Optional[str] = Field(frozen=True, default=None, description="State code.")
    state_name: Optional[str] = Field(frozen=True, default=None, description="The name of the state or state equivalent in which the monitoring location is located.")
    time_zone_abbreviation: Optional[str] = Field(frozen=True, default=None, description="A short code describing the time zone used by a monitoring location.")
    uses_daylight_savings: Optional[str] = Field(frozen=True, default=None, description="A flag indicating whether or not a monitoring location uses daylight savings.")
    vertical_datum: Optional[str] = Field(frozen=True, default=None, description="The datum used to determine altitude and vertical position at the monitoring location.")
    vertical_datum_name: Optional[str] = Field(frozen=True, default=None, description="The datum used to determine altitude and vertical position at the monitoring location.")
    well_constructed_depth: Optional[float] = Field(frozen=True, default=None, description="The depth of the finished well, in feet below land surface datum.")

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

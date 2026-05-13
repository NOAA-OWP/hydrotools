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

class ChannelMeasurementsRequest(BaseModel):
    """
    Channel measurements taken as part of streamflow field measurements.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None, description="Only features that have a geometry that intersects the bounding box are selected.")
    bbox_crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the given bbox coordinates.")
    channel_area: Optional[str] = Field(frozen=True, default=None, description="The channel area.")
    channel_area_unit: Optional[str] = Field(frozen=True, default=None, description="The units for channel area.")
    channel_evenness: Optional[str] = Field(frozen=True, default=None, description="The channel evenness from bank to bank.")
    channel_flow: Optional[str] = Field(frozen=True, default=None, description="Channel discharge.")
    channel_flow_unit: Optional[str] = Field(frozen=True, default=None, description="The units for channel discharge.")
    channel_location_direction: Optional[str] = Field(frozen=True, default=None, description="Location of the measurement from the gage.")
    channel_location_distance: Optional[str] = Field(frozen=True, default=None, description="The channel location distance.")
    channel_location_distance_unit: Optional[str] = Field(frozen=True, default=None, description="The units for channel location distance.")
    channel_material: Optional[str] = Field(frozen=True, default=None, description="The channel material.")
    channel_measurement_type: Optional[str] = Field(frozen=True, default=None, description="The channel measurement type.")
    channel_name: Optional[str] = Field(frozen=True, default=None, description="The channel name.")
    channel_stability: Optional[str] = Field(frozen=True, default=None, description="The stability of the channel material.")
    channel_velocity: Optional[str] = Field(frozen=True, default=None, description="The mean channel velocity.")
    channel_velocity_unit: Optional[str] = Field(frozen=True, default=None, description="The units for channel velocity.")
    channel_width: Optional[str] = Field(frozen=True, default=None, description="The channel width.")
    channel_width_unit: Optional[str] = Field(frozen=True, default=None, description="The units for channel width.")
    crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the results.")
    datetime: Optional[str] = Field(frozen=True, default=None, description="Either a date-time or an interval.")
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json", description="The optional f parameter indicates the output format which the server shall provide as part of the response document.")
    field_visit_id: Optional[str] = Field(frozen=True, default=None, description="A universally unique identifier (UUID) for the field visit.")
    horizontal_velocity_description: Optional[str] = Field(frozen=True, default=None, description="The horizontal velocity description.")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US", description="The optional lang parameter instructs the server return a response in a certain language, if supported.")
    last_modified: Optional[str] = Field(frozen=True, default=None, description="The last time a record was refreshed in our database.")
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000, description="The optional limit parameter limits the number of items that are presented in the response document (maximum=50000, default=10).")
    longitudinal_velocity_description: Optional[str] = Field(frozen=True, default=None, description="The longitudinal velocity description.")
    measurement_number: Optional[str] = Field(frozen=True, default=None, description="Measurement number.")
    measurement_type: Optional[str] = Field(frozen=True, default=None, description="The measurement type.")
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single monitoring location.")
    offset: Optional[int] = Field(frozen=True, default=0, ge=0, description="The optional offset parameter indicates the index within the result set from which the server shall begin presenting results in the response document.")
    properties: Optional[Sequence[Literal["id", "monitoring_location_id", "field_visit_id", "measurement_number", "time", "channel_name", "channel_flow", "channel_flow_unit", "channel_width", "channel_width_unit", "channel_area", "channel_area_unit", "channel_velocity", "channel_velocity_unit", "channel_location_distance", "channel_location_distance_unit", "channel_stability", "channel_material", "channel_evenness", "horizontal_velocity_description", "vertical_velocity_description", "longitudinal_velocity_description", "measurement_type", "last_modified", "channel_measurement_type", "channel_location_direction"]]] = Field(frozen=True, default=None, description="The properties that should be included.")
    query_filter: Optional[str] = Field(frozen=True, default=None, description="CQL Text filter expression.")
    query_id: Optional[str] = Field(frozen=True, default=None, description="A universally unique identifier (UUID) representing a single version of a record.")
    skipgeometry: Optional[bool] = Field(frozen=True, default=False, description="This option can be used to skip response geometries for each feature.")
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None, description="Specifies a comma-separated list of property names by which the response shall be sorted.")
    time: Optional[str] = Field(frozen=True, default=None, description="The date an observation represents.")
    vertical_velocity_description: Optional[str] = Field(frozen=True, default=None, description="The vertical velocity description.")

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

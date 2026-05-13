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
    approval_status: Optional[Literal["Provisional", "Approved"]] = Field(frozen=True, default=None, description="Some of the data that you have obtained from this U.")
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None, description="Only features that have a geometry that intersects the bounding box are selected.")
    bbox_crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the given bbox coordinates.")
    control_condition: Optional[str] = Field(frozen=True, default=None, description="The state of the control feature at the time of observation.")
    crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the results.")
    datetime: Optional[str] = Field(frozen=True, default=None, description="Either a date-time or an interval.")
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json", description="The optional f parameter indicates the output format which the server shall provide as part of the response document.")
    field_measurements_series_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single collection series.")
    field_visit_id: Optional[str] = Field(frozen=True, default=None, description="A universally unique identifier (UUID) for the field visit.")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US", description="The optional lang parameter instructs the server return a response in a certain language, if supported.")
    last_modified: Optional[str] = Field(frozen=True, default=None, description="The last time a record was refreshed in our database.")
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000, description="The optional limit parameter limits the number of items that are presented in the response document (maximum=50000, default=10).")
    measurement_rated: Optional[str] = Field(frozen=True, default=None, description="A qualitative estimate of the quality of a measurement.")
    measuring_agency: Optional[str] = Field(frozen=True, default=None, description="The agency performing the measurement.")
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single monitoring location.")
    observing_procedure: Optional[str] = Field(frozen=True, default=None, description="Water measurement or water-quality observing procedure descriptions.")
    observing_procedure_code: Optional[str] = Field(frozen=True, default=None, description="A short code corresponding to the observing procedure for the field measurement.")
    offset: Optional[int] = Field(frozen=True, default=0, ge=0, description="The optional offset parameter indicates the index within the result set from which the server shall begin presenting results in the response document.")
    parameter_code: Optional[str] = Field(frozen=True, default=None, description="Parameter codes are 5-digit codes used to identify the constituent measured and the units of measure.")
    properties: Optional[Sequence[Literal["id", "field_measurements_series_id", "field_visit_id", "parameter_code", "monitoring_location_id", "observing_procedure_code", "observing_procedure", "value", "unit_of_measure", "time", "qualifier", "vertical_datum", "approval_status", "measuring_agency", "last_modified", "control_condition", "measurement_rated"]]] = Field(frozen=True, default=None, description="The properties that should be included.")
    qualifier: Optional[str] = Field(frozen=True, default=None, description="This field indicates any qualifiers associated with an observation, for instance if a sensor may have been impacted by ice or if values were estimated.")
    query_filter: Optional[str] = Field(frozen=True, default=None, description="CQL Text filter expression.")
    query_id: Optional[str] = Field(frozen=True, default=None, description="A universally unique identifier (UUID) representing a single version of a record.")
    skipgeometry: Optional[bool] = Field(frozen=True, default=False, description="This option can be used to skip response geometries for each feature.")
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None, description="Specifies a comma-separated list of property names by which the response shall be sorted.")
    time: Optional[str] = Field(frozen=True, default=None, description="The date an observation represents.")
    unit_of_measure: Optional[str] = Field(frozen=True, default=None, description="A human-readable description of the units of measurement associated with an observation.")
    value: Optional[str] = Field(frozen=True, default=None, description="The value of the observation.")
    vertical_datum: Optional[str] = Field(frozen=True, default=None, description="The datum used to determine altitude and vertical position at the monitoring location.")

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

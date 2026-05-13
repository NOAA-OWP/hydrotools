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
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None, description="Only features that have a geometry that intersects the bounding box are selected.")
    bbox_crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the given bbox coordinates.")
    begin: Optional[str] = Field(frozen=True, default=None, description="This field contains the same information as  begin_utc , but in the local time of the monitoring location.")
    begin_utc: Optional[str] = Field(frozen=True, default=None, description="The datetime of the earliest observation in the time series.")
    computation_identifier: Optional[str] = Field(frozen=True, default=None, description="Indicates the computation performed to calculate this time series.")
    computation_period_identifier: Optional[str] = Field(frozen=True, default=None, description="Indicates the period of data used for any statistical computations.")
    crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the results.")
    end: Optional[str] = Field(frozen=True, default=None, description="This field contains the same information as  end_utc , but in the local time of the monitoring location.")
    end_utc: Optional[str] = Field(frozen=True, default=None, description="The datetime of the most recent observation in the time series.")
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json", description="The optional f parameter indicates the output format which the server shall provide as part of the response document.")
    hydrologic_unit_code: Optional[str] = Field(frozen=True, default=None, description="The United States is divided and sub-divided into successively smaller hydrologic units which are classified into four levels: regions, sub-regions, accounting units, and cataloging units.")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US", description="The optional lang parameter instructs the server return a response in a certain language, if supported.")
    last_modified: Optional[str] = Field(frozen=True, default=None, description="The last time a record was refreshed in our database.")
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000, description="The optional limit parameter limits the number of items that are presented in the response document (maximum=50000, default=10).")
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single monitoring location.")
    offset: Optional[int] = Field(frozen=True, default=0, ge=0, description="The optional offset parameter indicates the index within the result set from which the server shall begin presenting results in the response document.")
    parameter_code: Optional[str] = Field(frozen=True, default=None, description="Parameter codes are 5-digit codes used to identify the constituent measured and the units of measure.")
    parameter_description: Optional[str] = Field(frozen=True, default=None, description="A description of what the parameter code represents, as used by WDFN and other USGS data dissemination products.")
    parameter_name: Optional[str] = Field(frozen=True, default=None, description="A human-understandable name corresponding to `parameter_code`.")
    parent_time_series_id: Optional[str] = Field(frozen=True, default=None, description="The unique identifier representing the parent or  upchain  time series that a daily values time series is generated from.")
    primary: Optional[str] = Field(frozen=True, default=None, description="A flag identifying if the time series is a  primary  time series.")
    properties: Optional[Sequence[Literal["id", "unit_of_measure", "parameter_name", "parameter_code", "statistic_id", "hydrologic_unit_code", "state_name", "last_modified", "begin", "end", "begin_utc", "end_utc", "computation_period_identifier", "computation_identifier", "thresholds", "sublocation_identifier", "primary", "monitoring_location_id", "web_description", "parameter_description", "parent_time_series_id"]]] = Field(frozen=True, default=None, description="The properties that should be included.")
    query_filter: Optional[str] = Field(frozen=True, default=None, description="CQL Text filter expression.")
    query_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single time series.")
    skipgeometry: Optional[bool] = Field(frozen=True, default=False, description="This option can be used to skip response geometries for each feature.")
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None, description="Specifies a comma-separated list of property names by which the response shall be sorted.")
    state_name: Optional[str] = Field(frozen=True, default=None, description="The name of the state or state equivalent in which the monitoring location is located.")
    statistic_id: Optional[str] = Field(frozen=True, default=None, description="A code corresponding to the statistic an observation represents.")
    sublocation_identifier: Optional[str] = Field(frozen=True, default=None, description="An optional human-readable identifier used to specify where measurements are recorded at a monitoring location.")
    thresholds: Optional[str] = Field(frozen=True, default=None, description="Thresholds represent known numeric limits for a time series, for example the historic maximum value for a parameter or a level below which a sensor is non-operative.")
    unit_of_measure: Optional[str] = Field(frozen=True, default=None, description="A human-readable description of the units of measurement associated with an observation.")
    web_description: Optional[str] = Field(frozen=True, default=None, description="An optional description of the time series.")

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

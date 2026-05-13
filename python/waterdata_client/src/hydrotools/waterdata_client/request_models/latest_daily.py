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
    approval_status: Optional[Literal["Provisional", "Approved"]] = Field(frozen=True, default=None, description="Some of the data that you have obtained from this U.")
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None, description="Only features that have a geometry that intersects the bounding box are selected.")
    bbox_crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the given bbox coordinates.")
    crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the results.")
    datetime: Optional[str] = Field(frozen=True, default=None, description="Either a date-time or an interval.")
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json", description="The optional f parameter indicates the output format which the server shall provide as part of the response document.")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US", description="The optional lang parameter instructs the server return a response in a certain language, if supported.")
    last_modified: Optional[str] = Field(frozen=True, default=None, description="The last time a record was refreshed in our database.")
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000, description="The optional limit parameter limits the number of items that are presented in the response document (maximum=50000, default=10).")
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single monitoring location.")
    offset: Optional[int] = Field(frozen=True, default=0, ge=0, description="The optional offset parameter indicates the index within the result set from which the server shall begin presenting results in the response document.")
    parameter_code: Optional[str] = Field(frozen=True, default=None, description="Parameter codes are 5-digit codes used to identify the constituent measured and the units of measure.")
    properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = Field(frozen=True, default=None, description="The properties that should be included.")
    qualifier: Optional[str] = Field(frozen=True, default=None, description="This field indicates any qualifiers associated with an observation, for instance if a sensor may have been impacted by ice or if values were estimated.")
    query_filter: Optional[str] = Field(frozen=True, default=None, description="CQL Text filter expression.")
    query_id: Optional[str] = Field(frozen=True, default=None, description="A universally unique identifier (UUID) representing a single version of a record.")
    skipgeometry: Optional[bool] = Field(frozen=True, default=False, description="This option can be used to skip response geometries for each feature.")
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None, description="Specifies a comma-separated list of property names by which the response shall be sorted.")
    statistic_id: Optional[str] = Field(frozen=True, default=None, description="A code corresponding to the statistic an observation represents.")
    time: Optional[str] = Field(frozen=True, default=None, description="The date an observation represents.")
    time_series_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single time series.")
    unit_of_measure: Optional[str] = Field(frozen=True, default=None, description="A human-readable description of the units of measurement associated with an observation.")
    value: Optional[str] = Field(frozen=True, default=None, description="The value of the observation.")

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

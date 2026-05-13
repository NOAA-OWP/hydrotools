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

class PeaksRequest(BaseModel):
    """
    Annual peak flow values are the maximum instantaneous streamflow
    values recorded at a particular site for the entire water year from
    October 1 to September 30. Note that the annual peak flow value may
    not occur at the same time the maximum water level occurs due to
    conditions such as backwater, tidal fluctuations, etc.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None, description="Only features that have a geometry that intersects the bounding box are selected.")
    bbox_crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the given bbox coordinates.")
    crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the results.")
    day: Optional[int] = Field(frozen=True, default=None, description="The day of the month a peak occurred.")
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json", description="The optional f parameter indicates the output format which the server shall provide as part of the response document.")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US", description="The optional lang parameter instructs the server return a response in a certain language, if supported.")
    last_modified: Optional[str] = Field(frozen=True, default=None, description="The last time a record was refreshed in our database.")
    limit: Optional[int] = Field(frozen=True, default=10, ge=1, le=50000, description="The optional limit parameter limits the number of items that are presented in the response document (maximum=50000, default=10).")
    monitoring_location_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single monitoring location.")
    month: Optional[int] = Field(frozen=True, default=None, description="The calendar month a peak occurred.")
    offset: Optional[int] = Field(frozen=True, default=0, ge=0, description="The optional offset parameter indicates the index within the result set from which the server shall begin presenting results in the response document.")
    parameter_code: Optional[str] = Field(frozen=True, default=None, description="Parameter codes are 5-digit codes used to identify the constituent measured and the units of measure.")
    peak_since: Optional[int] = Field(frozen=True, default=None, description="If not null, this record represents the peak value for the parameter code since the year contained in  peak_since.")
    properties: Optional[Sequence[Literal["time_series_id", "monitoring_location_id", "parameter_code", "id", "unit_of_measure", "value", "last_modified", "time", "water_year", "year", "month", "day", "time_of_day", "peak_since"]]] = Field(frozen=True, default=None, description="The properties that should be included.")
    query_filter: Optional[str] = Field(frozen=True, default=None, description="CQL Text filter expression.")
    query_id: Optional[str] = Field(frozen=True, default=None, description="Split parameters are enabled for this field, so you can supply multiple values separated by commas.")
    skipgeometry: Optional[bool] = Field(frozen=True, default=False, description="This option can be used to skip response geometries for each feature.")
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None, description="Specifies a comma-separated list of property names by which the response shall be sorted.")
    time: Optional[str] = Field(frozen=True, default=None, description="The date an observation represents.")
    time_of_day: Optional[str] = Field(frozen=True, default=None, description="The time of day a peak occurred.")
    time_series_id: Optional[str] = Field(frozen=True, default=None, description="A unique identifier representing a single time series.")
    unit_of_measure: Optional[str] = Field(frozen=True, default=None, description="A human-readable description of the units of measurement associated with an observation.")
    value: Optional[str] = Field(frozen=True, default=None, description="The value of the observation.")
    water_year: Optional[int] = Field(frozen=True, default=None, description="The water year (running from October 1st to September 30th) a peak occurred.")
    year: Optional[int] = Field(frozen=True, default=None, description="The calendar year a peak occurred.")

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

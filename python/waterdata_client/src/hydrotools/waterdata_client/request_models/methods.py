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

class MethodsRequest(BaseModel):
    """
    Water measurement or water-quality analytical methods. Codes and
    descriptions defining a method for calculating or measuring the value
    of a water quality or quantity parameter. Method codes are associated
    with one or many parameter codes.
    """
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None, description="Only features that have a geometry that intersects the bounding box are selected.")
    bbox_crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the given bbox coordinates.")
    crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the results.")
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json", description="The optional f parameter indicates the output format which the server shall provide as part of the response document.")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US", description="The optional lang parameter instructs the server return a response in a certain language, if supported.")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000, description="The optional limit parameter limits the number of items that are presented in the response document (maximum=50000, default=10000).")
    method_category: Optional[str] = Field(frozen=True, default=None, description="Code representing the method category standard.")
    method_description: Optional[str] = Field(frozen=True, default=None, description="A long name that fully describes a method.")
    method_name: Optional[str] = Field(frozen=True, default=None, description="A short name that partially describes a method.")
    method_type: Optional[str] = Field(frozen=True, default=None, description="Method type for measured or collected data.")
    offset: Optional[int] = Field(frozen=True, default=0, ge=0, description="The optional offset parameter indicates the index within the result set from which the server shall begin presenting results in the response document.")
    properties: Optional[Sequence[Literal["id", "method_type", "method_category", "method_name", "method_description"]]] = Field(frozen=True, default=None, description="The properties that should be included.")
    query_filter: Optional[str] = Field(frozen=True, default=None, description="CQL Text filter expression.")
    query_id: Optional[str] = Field(frozen=True, default=None, description="Water measurement or water-quality analytical method code.")
    skipgeometry: Optional[bool] = Field(frozen=True, default=False, description="This option can be used to skip response geometries for each feature.")
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None, description="Specifies a comma-separated list of property names by which the response shall be sorted.")

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

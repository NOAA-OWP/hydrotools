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
    bbox: Optional[Sequence[float]] = Field(frozen=True, default=None, description="Only features that have a geometry that intersects the bounding box are selected.")
    bbox_crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the given bbox coordinates.")
    crs: Optional[URL] = Field(frozen=True, default=None, description="Indicates the coordinate reference system for the results.")
    epa_equivalence: Optional[str] = Field(frozen=True, default=None, description="Indicates the relationship of the USGS parameter code to the EPA code.")
    f: Optional[Literal["json", "html", "jsonld", "csv"]] = Field(frozen=True, default="json", description="The optional f parameter indicates the output format which the server shall provide as part of the response document.")
    lang: Optional[Literal["en-US"]] = Field(frozen=True, default="en-US", description="The optional lang parameter instructs the server return a response in a certain language, if supported.")
    limit: Optional[int] = Field(frozen=True, default=10000, ge=1, le=50000, description="The optional limit parameter limits the number of items that are presented in the response document (maximum=50000, default=10000).")
    medium: Optional[str] = Field(frozen=True, default=None, description="Parameter medium.")
    offset: Optional[int] = Field(frozen=True, default=0, ge=0, description="The optional offset parameter indicates the index within the result set from which the server shall begin presenting results in the response document.")
    parameter_description: Optional[str] = Field(frozen=True, default=None, description="Parameter description.")
    parameter_group_code: Optional[str] = Field(frozen=True, default=None, description="Categorical groupings of parameters by water-quality data type for display and report ordering.")
    parameter_name: Optional[str] = Field(frozen=True, default=None, description="Parameter short name.")
    particle_size_basis: Optional[str] = Field(frozen=True, default=None, description="Parameter particle-size basis.")
    properties: Optional[Sequence[Literal["id", "parameter_name", "unit_of_measure", "parameter_group_code", "parameter_description", "medium", "statistical_basis", "time_basis", "weight_basis", "particle_size_basis", "sample_fraction", "temperature_basis", "epa_equivalence"]]] = Field(frozen=True, default=None, description="The properties that should be included.")
    query_filter: Optional[str] = Field(frozen=True, default=None, description="CQL Text filter expression.")
    query_id: Optional[str] = Field(frozen=True, default=None, description="Parameter code.")
    sample_fraction: Optional[str] = Field(frozen=True, default=None, description="Parameter fraction.")
    skipgeometry: Optional[bool] = Field(frozen=True, default=False, description="This option can be used to skip response geometries for each feature.")
    sortby: Optional[Sequence[str]] = Field(frozen=True, default=None, description="Specifies a comma-separated list of property names by which the response shall be sorted.")
    statistical_basis: Optional[str] = Field(frozen=True, default=None, description="Parameter statistical basis.")
    temperature_basis: Optional[str] = Field(frozen=True, default=None, description="Parameter temperature basis.")
    time_basis: Optional[str] = Field(frozen=True, default=None, description="Parameter time basis.")
    unit_of_measure: Optional[str] = Field(frozen=True, default=None, description="Parameter reporting units defined to cooperate with descriptions by USEPA.")
    weight_basis: Optional[str] = Field(frozen=True, default=None, description="Parameter weight basis.")

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

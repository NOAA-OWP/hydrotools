# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
"""This is a Jinja2 auto-generated module. These modules contain individual
client classes for USGS OGC API items endpoints. These classes are generated
by inspecting the USGS OGC API JSON schema and identifying all "items" endpoints.

Package version: 0.8.0a0
Generation script: build_clients.py
Generated: 2026-05-13 16:08:08 Z
JSON Schema source: https://api.waterdata.usgs.gov/ogcapi/v0/openapi?f=json
JSON Schema version: 0.49.2
OpenAPI version: 3.0.2
"""
from typing import Sequence, Literal, Optional
from yarl import URL
from ..base_client import BaseClient
from ..constants import USGSCollection
from ..transformers import TransformedResponseT_co
from .. import request_models as rm

class ParameterCodesClient(BaseClient[TransformedResponseT_co]):
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
    _endpoint = USGSCollection.PARAMETER_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        epa_equivalence: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        medium: Optional[str] = None,
        offset: Optional[int] = 0,
        parameter_description: Optional[str] = None,
        parameter_group_code: Optional[str] = None,
        parameter_name: Optional[str] = None,
        particle_size_basis: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "parameter_name", "unit_of_measure", "parameter_group_code", "parameter_description", "medium", "statistical_basis", "time_basis", "weight_basis", "particle_size_basis", "sample_fraction", "temperature_basis", "epa_equivalence"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        sample_fraction: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        statistical_basis: Optional[str] = None,
        temperature_basis: Optional[str] = None,
        time_basis: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        weight_basis: Optional[str] = None,
        ) -> TransformedResponseT_co:
        """Retrieve items from parameter-codes.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            crs: Indicates the coordinate reference system for the results.
            epa_equivalence: Indicates the relationship of the USGS parameter code to the EPA code.
            f: The optional f parameter indicates the output format which the server
                shall provide as part of the response document.  The default format is
                GeoJSON.
            lang: The optional lang parameter instructs the server return a response in
                a certain language, if supported.  If the language is not among the
                available values, the Accept-Language header language will be used if
                it is supported. If the header is missing, the default server language
                is used. Note that providers may only support a single language (or
                often no language at all), that can be different from the server
                language.  Language strings can be written in a complex (e.g. "fr-
                CA,fr;q=0.9,en-US;q=0.8,en;q=0.7"), simple (e.g. "de") or locale-like
                (e.g. "de-CH" or "fr_BE") fashion.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10000).
            medium: Parameter medium.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            parameter_description: Parameter description.
            parameter_group_code: Categorical groupings of parameters by water-quality data type for
                display and report ordering
            parameter_name: Parameter short name.
            particle_size_basis: Parameter particle-size basis.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: Parameter code.
            sample_fraction: Parameter fraction.
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall
                be sorted.  If the property name is preceded by a plus (+) sign it
                indicates
                an ascending sort for that property.  If the property name is preceded
                by a
                minus (-) sign it indicates a descending sort for that property.  If
                the
                property is not preceded by a plus or minus, then the default sort
                order
                implied is ascending (+).
            statistical_basis: Parameter statistical basis.
            temperature_basis: Parameter temperature basis.
            time_basis: Parameter time basis.
            unit_of_measure: Parameter reporting units defined to cooperate with descriptions by
                USEPA.
            weight_basis: Parameter weight basis.
        """
        # Validate query
        query = rm.ParameterCodesRequest(
            bbox=bbox,
            bbox_crs=bbox_crs,
            crs=crs,
            epa_equivalence=epa_equivalence,
            f=f,
            lang=lang,
            limit=limit,
            medium=medium,
            offset=offset,
            parameter_description=parameter_description,
            parameter_group_code=parameter_group_code,
            parameter_name=parameter_name,
            particle_size_basis=particle_size_basis,
            properties=properties,
            query_filter=query_filter,
            query_id=query_id,
            sample_fraction=sample_fraction,
            skipgeometry=skipgeometry,
            sortby=sortby,
            statistical_basis=statistical_basis,
            temperature_basis=temperature_basis,
            time_basis=time_basis,
            unit_of_measure=unit_of_measure,
            weight_basis=weight_basis,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

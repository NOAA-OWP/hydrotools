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

class MediumCodesClient(BaseClient[TransformedResponseT_co]):
    """
    Medium refers to the specific environmental medium from which the
    sample was collected. Medium type differs from site type because one
    site type, such as surface water, could have data for several media,
    such as water, bottom sediment, fish tissue, and others.
    """
    _endpoint = USGSCollection.MEDIUM_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        legacy_medium_code: Optional[str] = None,
        limit: Optional[int] = 10000,
        medium_description: Optional[str] = None,
        medium_name: Optional[str] = None,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "medium_name", "medium_description", "legacy_medium_code"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponseT_co:
        """Retrieve items from medium-codes.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            crs: Indicates the coordinate reference system for the results.
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
            legacy_medium_code: Historical 1-char medium code that corresponds to the 3-char code.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10000).
            medium_description: The medium description is a short string of words that explains the
                associated medium code. See qwmed for examples of codes, names, and
                descriptions.
            medium_name: The medium name is a short identifying appellation that explains the
                associated medium code. See qwmed for examples of codes, names, and
                descriptions.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: The medium code is the 3-character alpha code that identifies the
                material type and quality-assurance type of the sample. The first
                character of the code is the \"super\" medium, which describes the
                primary matrix of the sample. The second character is the sub-medium,
                which characterizes the sample type as a unique entity within the
                \"super\" medium category. The third character is used to designate
                whether a sample is an environmental or QC sample. A blank in position
                three denotes an environmental sample; a \"Q\" in position three
                denotes a QC sample.
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
        """
        # Validate query
        query = rm.MediumCodesRequest(
            bbox=bbox,
            bbox_crs=bbox_crs,
            crs=crs,
            f=f,
            lang=lang,
            legacy_medium_code=legacy_medium_code,
            limit=limit,
            medium_description=medium_description,
            medium_name=medium_name,
            offset=offset,
            properties=properties,
            query_filter=query_filter,
            query_id=query_id,
            skipgeometry=skipgeometry,
            sortby=sortby,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

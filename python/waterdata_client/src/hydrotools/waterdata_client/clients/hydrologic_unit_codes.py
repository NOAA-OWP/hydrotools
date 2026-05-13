# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
"""This is a Jinja2 auto-generated module. These modules contain individual
client classes for USGS OGC API items endpoints. These classes are generated
by inspecting the USGS OGC API JSON schema and identifying all "items" endpoints.

Package version: 0.8.0a0
Generation script: build_clients.py
Generated: 2026-05-13 17:38:51 Z
JSON Schema source: https://api.waterdata.usgs.gov/ogcapi/v0/openapi?f=json
JSON Schema version: 0.49.2
OpenAPI version: 3.0.2
"""
from typing import Sequence, Literal, Optional
from yarl import URL
from ..base_client import BaseClient
from ..constants import USGSCollection
from ..transformers import TransformedResponseT_co
from ..request_models.hydrologic_unit_codes import HydrologicUnitCodesRequest

class HydrologicUnitCodesClient(BaseClient[TransformedResponseT_co]):
    """
    Hydrologic units are geographic areas representing part or all of a
    surface drainage basin or distinct hydrologic feature identified by a
    unique number (HUC), and a name. The United States is divided and sub-
    divided into successively smaller hydrologic units which are
    classified into four levels: regions, sub-regions, accounting units,
    and cataloging units. Each unit consists of two to eight digits based
    on the four levels of classification in the hydrologic unit system.
    Additional information can be found at
    <https://water.usgs.gov/GIS/huc.html>.
    """
    _endpoint = USGSCollection.HYDROLOGIC_UNIT_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        hydrologic_unit_classification_code: Optional[str] = None,
        hydrologic_unit_name: Optional[str] = None,
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "hydrologic_unit_name", "hydrologic_unit_classification_code"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponseT_co:
        """Retrieve items from hydrologic-unit-codes.

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
            hydrologic_unit_classification_code: Hydrologic unit classification code.
            hydrologic_unit_name: Hydrologic unit name.
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
            query_id: Hydrologic unit code. The format of the code is ('RRSSBBUUWWXX')
                where: 'RR' is the 2-digit code for the region. 'SS' is the 2-digit
                code for the sub-region. 'BB' is the 2-digit code for the basin. 'UU'
                is the 2-digit code for the sub-basin. 'WW' is the 2-digit code for
                the watershed. 'XX' is the 2-digit code for the sub-watershed.
                Watersheds are delineated by USGS using a nationwide system based on
                surface hydrologic features. This system divides the country into 22
                regions (2-digit), 245 subregions (4-digit), 405 basins (6-digit),
                ~2,400 subbasins (8-digit), ~19,000 watersheds (10-digit), and
                ~105,000 subwatersheds (12-digit). A hierarchical hydrologic unit code
                (HUC) consisting of 2 additional digits for each level in the
                hydrologic unit system is used to identify any hydrologic area (see
                Federal Standards and Procedures for the National Watershed Boundary
                Dataset - https://pubs.usgs.gov/tm/11/a3/).
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
        query = HydrologicUnitCodesRequest(
            bbox=bbox,
            bbox_crs=bbox_crs,
            crs=crs,
            f=f,
            hydrologic_unit_classification_code=hydrologic_unit_classification_code,
            hydrologic_unit_name=hydrologic_unit_name,
            lang=lang,
            limit=limit,
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

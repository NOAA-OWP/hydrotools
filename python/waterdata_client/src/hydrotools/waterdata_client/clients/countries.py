# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
"""This is a Jinja2 auto-generated module. These modules contain individual
client classes for USGS OGC API items endpoints. These classes are generated
by inspecting the USGS OGC API JSON schema and identifying all "items" endpoints.

Package version: 0.8.0a0
Generation script: build_clients.py
Generated: 2026-05-20 18:31:11 Z
JSON Schema source: https://api.waterdata.usgs.gov/ogcapi/v0/openapi?f=json
JSON Schema version: 0.49.2
OpenAPI version: 3.0.2
"""
from typing import Sequence, Literal, Optional
from yarl import URL
from hydrotools.waterdata_client.client_config import SETTINGS
from hydrotools.waterdata_client.base_client import BaseClient
from hydrotools.waterdata_client.constants import USGSCollection
from hydrotools.waterdata_client.transformers import TransformedResponseT_co
from hydrotools.waterdata_client.request_models.countries import CountriesRequest

class CountriesClient(BaseClient[TransformedResponseT_co]):
    """
    FIPS country codes and names.
    """
    _endpoint = USGSCollection.COUNTRIES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        country_name: Optional[str] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "country_name"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        api_key: Optional[str] = None
        ) -> TransformedResponseT_co:
        """Retrieve items from countries.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            country_name: Country name.
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
            query_id: FIPS country code as defined by FIPS PUB 10-4: Countries,
                Dependencies, Areas of Special Sovereignty, and Their Principal
                Administrative Divisions.
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
            api_key: Providing your API key gives you higher rate limits when querying
                our APIs. You can obtain an API key at https://api.waterdata.usgs.gov/signup
        """
        # Validate query
        query = CountriesRequest(
            bbox=bbox,
            bbox_crs=bbox_crs,
            country_name=country_name,
            crs=crs,
            f=f,
            lang=lang,
            limit=limit,
            offset=offset,
            properties=properties,
            query_filter=query_filter,
            query_id=query_id,
            skipgeometry=skipgeometry,
            sortby=sortby,
            api_key=api_key if api_key else SETTINGS.usgs_api_key
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

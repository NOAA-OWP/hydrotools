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

class TimeZoneCodesClient(BaseClient[TransformedResponseT_co]):
    """
    The ISO 8601 standard defines time zone offsets as a numerical value
    added to a local time to convert it to Coordinated Universal Time
    (UTC), either as +hh:mm or -hh:mm, or represented by the letter Z to
    explicitly indicate UTC. For example, +05:30 means 5 hours and 30
    minutes ahead of UTC, while -08:00 means 8 hours behind UTC. The
    offset Z specifically signifies UTC.
    """
    _endpoint = USGSCollection.TIME_ZONE_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "time_zone_name", "time_zone_description", "time_zone_utc_offset", "time_zone_daylight_savings_time_code", "time_zone_daylight_savings_time_name", "time_zone_daylight_savings_utc_offset"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        time_zone_daylight_savings_time_code: Optional[str] = None,
        time_zone_daylight_savings_time_name: Optional[str] = None,
        time_zone_daylight_savings_utc_offset: Optional[str] = None,
        time_zone_description: Optional[str] = None,
        time_zone_name: Optional[str] = None,
        time_zone_utc_offset: Optional[str] = None,
        ) -> TransformedResponseT_co:
        """Retrieve items from time-zone-codes.

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
            query_id: Time zone code. An NWIS time zone code.
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
            time_zone_daylight_savings_time_code: Time zone Daylight Saving Time code.
            time_zone_daylight_savings_time_name: Time zone Daylight Saving Time name.
            time_zone_daylight_savings_utc_offset: Daylight Saving Time offset time. The number of hours offset from UTC
                time when Daylight Saving Time is in effect, in ISO format.
            time_zone_description: Time zone description.
            time_zone_name: Time zone name. An English name for a world time zone.
            time_zone_utc_offset: Coordinated Universal Time (UTC) offset time. The number of hours
                offset from UTC time, in ISO format.
        """
        # Validate query
        query = rm.TimeZoneCodesRequest(
            bbox=bbox,
            bbox_crs=bbox_crs,
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
            time_zone_daylight_savings_time_code=time_zone_daylight_savings_time_code,
            time_zone_daylight_savings_time_name=time_zone_daylight_savings_time_name,
            time_zone_daylight_savings_utc_offset=time_zone_daylight_savings_utc_offset,
            time_zone_description=time_zone_description,
            time_zone_name=time_zone_name,
            time_zone_utc_offset=time_zone_utc_offset,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

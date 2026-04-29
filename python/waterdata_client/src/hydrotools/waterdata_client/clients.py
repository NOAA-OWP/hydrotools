# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.
"""This is a Jinja2 auto-generated module. This module contains individual
client classes for USGS OGC API items endpoints. These classes are generated
by inspecting the USGS OGC API JSON schema and identifying all "items" endpoints.

Package version: 0.8.0a0
Generation script: build_clients.py
Generated: 2026-04-29 12:26:54 Z
JSON Schema source: https://api.waterdata.usgs.gov/ogcapi/v0/openapi?f=json
JSON Schema version: 0.47.0
OpenAPI version: 3.0.2
"""
from typing import Any, Sequence, Literal, Optional
from yarl import URL
from .base_client import BaseClient
from .constants import USGSCollection
from .transformers import TransformedResponse_co

__all__ = [
    "AgencyCodesClient",
    "AltitudeDatumsClient",
    "AquiferCodesClient",
    "AquiferTypesClient",
    "ChannelMeasurementsClient",
    "CitationsClient",
    "CombinedMetadataClient",
    "ContinuousClient",
    "CoordinateAccuracyCodesClient",
    "CoordinateDatumCodesClient",
    "CoordinateMethodCodesClient",
    "CountiesClient",
    "CountriesClient",
    "DailyClient",
    "FieldMeasurementsClient",
    "FieldMeasurementsMetadataClient",
    "HydrologicUnitCodesClient",
    "LatestContinuousClient",
    "LatestDailyClient",
    "MediumCodesClient",
    "MethodCategoriesClient",
    "MethodCitationsClient",
    "MethodsClient",
    "MonitoringLocationsClient",
    "NationalAquiferCodesClient",
    "ParameterCodesClient",
    "ReliabilityCodesClient",
    "SiteTypesClient",
    "StatesClient",
    "StatisticCodesClient",
    "TimeSeriesMetadataClient",
    "TimeZoneCodesClient",
    "TopographicCodesClient",
]

class AgencyCodesClient(BaseClient[TransformedResponse_co]):
    """
    Code identifying the agency or organization used for site information,
    data sources, and permitting agencies. Agency codes are fixed values
    assigned by the National Water Information System (NWIS).
    """
    _endpoint = USGSCollection.AGENCY_CODES

    def get(
        self,
        agency_name: Optional[str] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "agency_name"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from agency-codes.

        Args:
            agency_name: Agency name.
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
            query_id: Agency code identification number.
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
        # Translate Python parameters to API parameters
        query = {
            "agency_name": agency_name,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class AltitudeDatumsClient(BaseClient[TransformedResponse_co]):
    """
    The recommended vertical datum is NAVD88 (North American Vertical
    Datum of 1988) where applicable as stated in Office of Information
    Technical Memo 2002.01. NGVD29 (National Geodetic Vertical Datum of
    1929) and NAVD88 are the only datums that can be converted on output.
    NWIS uses the North American Vertical Datum Conversions (VERTCON) of
    the National Geodetic Survey to convert from NGVD29 to NAVD88 or vice
    versa. Conversions to or from other vertical datums are not available.
    """
    _endpoint = USGSCollection.ALTITUDE_DATUMS

    def get(
        self,
        altitude_datum_description: Optional[str] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "altitude_datum_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from altitude-datums.

        Args:
            altitude_datum_description: 
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
            query_id: 
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
        # Translate Python parameters to API parameters
        query = {
            "altitude_datum_description": altitude_datum_description,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class AquiferCodesClient(BaseClient[TransformedResponse_co]):
    """
    Local aquifers in USGS data are identified by an aquifer name and
    geohydrologic unit code (a three-digit number related to the age of
    the formation, followed by a 4 or 5 character abbreviation for the
    geologic unit or aquifer name). For the age of formation (aquifer
    age), generally the smaller the number represents the younger the
    geohydrologic unit. Aquifer names and the definition of an aquifer can
    be very subjective. One rock unit may be called different aquifer
    names by different people. Local aquifers and layered aquifers are
    often grouped into larger named regional aquifers or aquifer systems.
    For example, the National Northern Atlantic Coastal Plain aquifer
    system (National aquifer) consists of five layered regional aquifers.
    Each regional aquifer is divided into two or more aquifers which may
    have a different name in each of the states in which the aquifer is
    found.
    """
    _endpoint = USGSCollection.AQUIFER_CODES

    def get(
        self,
        aquifer_name: Optional[str] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "aquifer_name"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from aquifer-codes.

        Args:
            aquifer_name: Aquifer name. Aquifer names are defined by the \"Catalog of Aquifer
                Names and Geologic Unit Codes used by the Water Resources Division.\"
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
            query_id: Aquifer code. The eight-character string identifying an aquifer. Codes
                are defined by the \"Catalog of Aquifer Names and Geologic Unit Codes
                used by the Water Resources Division.\"
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
        # Translate Python parameters to API parameters
        query = {
            "aquifer_name": aquifer_name,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class AquiferTypesClient(BaseClient[TransformedResponse_co]):
    """
    Groundwater occurs in aquifers under two different conditions. Where
    water only partly fills an aquifer, the upper surface is free to rise
    and decline. These aquifers are referred to as unconfined (or water-
    table) aquifers. Where water completely fills an aquifer that is
    overlain by a confining bed, the aquifer is referred to as a confined
    (or artesian) aquifer. When a confined aquifer is penetrated by a
    well, the water level in the well will rise above the top of the
    aquifer (but not necessarily above land surface).
    """
    _endpoint = USGSCollection.AQUIFER_TYPES

    def get(
        self,
        aquifer_type_description: Optional[str] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "aquifer_type_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from aquifer-types.

        Args:
            aquifer_type_description: Longer description of the aquifer type.
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
            query_id: The single-character code identifying the type of aquifer
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
        # Translate Python parameters to API parameters
        query = {
            "aquifer_type_description": aquifer_type_description,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class ChannelMeasurementsClient(BaseClient[TransformedResponse_co]):
    """
    Channel measurements taken as part of streamflow field measurements.
    """
    _endpoint = USGSCollection.CHANNEL_MEASUREMENTS

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        channel_area: Optional[str] = None,
        channel_area_unit: Optional[str] = None,
        channel_evenness: Optional[str] = None,
        channel_flow: Optional[str] = None,
        channel_flow_unit: Optional[str] = None,
        channel_location_direction: Optional[str] = None,
        channel_location_distance: Optional[str] = None,
        channel_location_distance_unit: Optional[str] = None,
        channel_material: Optional[str] = None,
        channel_measurement_type: Optional[str] = None,
        channel_name: Optional[str] = None,
        channel_stability: Optional[str] = None,
        channel_velocity: Optional[str] = None,
        channel_velocity_unit: Optional[str] = None,
        channel_width: Optional[str] = None,
        channel_width_unit: Optional[str] = None,
        crs: Optional[URL] = None,
        datetime: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        field_visit_id: Optional[str] = None,
        horizontal_velocity_description: Optional[str] = None,
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        longitudinal_velocity_description: Optional[str] = None,
        measurement_number: Optional[str] = None,
        measurement_type: Optional[str] = None,
        monitoring_location_id: Optional[str] = None,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "monitoring_location_id", "field_visit_id", "measurement_number", "time", "channel_name", "channel_flow", "channel_flow_unit", "channel_width", "channel_width_unit", "channel_area", "channel_area_unit", "channel_velocity", "channel_velocity_unit", "channel_location_distance", "channel_location_distance_unit", "channel_stability", "channel_material", "channel_evenness", "horizontal_velocity_description", "vertical_velocity_description", "longitudinal_velocity_description", "measurement_type", "last_modified", "channel_measurement_type", "channel_location_direction"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        time: Optional[str] = None,
        vertical_velocity_description: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from channel-measurements.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            channel_area: The channel area.
            channel_area_unit: The units for channel area.
            channel_evenness: The channel evenness from bank to bank.
            channel_flow: Channel discharge.
            channel_flow_unit: The units for channel discharge.
            channel_location_direction: Location of the measurement from the gage.
            channel_location_distance: The channel location distance.
            channel_location_distance_unit: The units for channel location distance.
            channel_material: The channel material.
            channel_measurement_type: The channel measurement type.
            channel_name: The channel name.
            channel_stability: The stability of the channel material.
            channel_velocity: The mean channel velocity.
            channel_velocity_unit: The units for channel velocity.
            channel_width: The channel width.
            channel_width_unit: The units for channel width.
            crs: Indicates the coordinate reference system for the results.
            datetime: Either a date-time or an interval. Date and time expressions adhere to
                RFC 3339.
                Intervals may be bounded or half-bounded (double-dots at start or
                end).

                Examples:

                * A date-time: "2018-02-12T23:20:50Z"
                * A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                * Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"

                Only features that have a temporal property that intersects the value
                of
                `datetime` are selected.

                If a feature has multiple temporal properties, it is the decision of
                the
                server whether only a single temporal property is used to determine
                the extent or all relevant temporal properties.
            f: The optional f parameter indicates the output format which the server
                shall provide as part of the response document.  The default format is
                GeoJSON.
            field_visit_id: A universally unique identifier (UUID) for the field visit. Multiple
                measurements may be made during a single field visit.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            horizontal_velocity_description: The horizontal velocity description.
            lang: The optional lang parameter instructs the server return a response in
                a certain language, if supported.  If the language is not among the
                available values, the Accept-Language header language will be used if
                it is supported. If the header is missing, the default server language
                is used. Note that providers may only support a single language (or
                often no language at all), that can be different from the server
                language.  Language strings can be written in a complex (e.g. "fr-
                CA,fr;q=0.9,en-US;q=0.8,en;q=0.7"), simple (e.g. "de") or locale-like
                (e.g. "de-CH" or "fr_BE") fashion.
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            longitudinal_velocity_description: The longitudinal velocity description.
            measurement_number: Measurement number.
            measurement_type: The measurement type.
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
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
            query_id: A universally unique identifier (UUID) representing a single version
                of a record. It is not stable over time. Every time the record is
                refreshed in our database (which may happen as part of normal
                operations and does not imply any change to the data itself) a new ID
                will be generated. To uniquely identify a single observation over
                time, compare the `time` and `time_series_id` fields; each time series
                will only have a single observation at a given `time`.
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            time: The date an observation represents. You can query this field using
                date-times or intervals, adhering to RFC 3339, or using ISO 8601
                duration objects. Intervals may be bounded or half-bounded (double-
                dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `time` that intersects the value of datetime
                are selected. If a feature has multiple temporal properties, it is the
                decision of the server whether only a single temporal property is used
                to determine the extent or all relevant temporal properties.
            vertical_velocity_description: The vertical velocity description.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "channel_area": channel_area,
            "channel_area_unit": channel_area_unit,
            "channel_evenness": channel_evenness,
            "channel_flow": channel_flow,
            "channel_flow_unit": channel_flow_unit,
            "channel_location_direction": channel_location_direction,
            "channel_location_distance": channel_location_distance,
            "channel_location_distance_unit": channel_location_distance_unit,
            "channel_material": channel_material,
            "channel_measurement_type": channel_measurement_type,
            "channel_name": channel_name,
            "channel_stability": channel_stability,
            "channel_velocity": channel_velocity,
            "channel_velocity_unit": channel_velocity_unit,
            "channel_width": channel_width,
            "channel_width_unit": channel_width_unit,
            "crs": crs,
            "datetime": datetime,
            "f": f,
            "field_visit_id": field_visit_id,
            "horizontal_velocity_description": horizontal_velocity_description,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "longitudinal_velocity_description": longitudinal_velocity_description,
            "measurement_number": measurement_number,
            "measurement_type": measurement_type,
            "monitoring_location_id": monitoring_location_id,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "time": time,
            "vertical_velocity_description": vertical_velocity_description,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class CitationsClient(BaseClient[TransformedResponse_co]):
    """
    Citations associated with water measurement methods.
    """
    _endpoint = USGSCollection.CITATIONS

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        citation_description: Optional[str] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "citation_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from citations.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            citation_description: Method citation description.
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
            query_id: Method citation name. An abbreviated citation that describes the
                reference.
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "citation_description": citation_description,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class CombinedMetadataClient(BaseClient[TransformedResponse_co]):
    """
    This endpoint combines metadata from timeseries and field measurements
    collections by site.
    """
    _endpoint = USGSCollection.COMBINED_METADATA

    def get(
        self,
        agency_code: Optional[str] = None,
        agency_name: Optional[str] = None,
        altitude: Optional[float] = None,
        altitude_accuracy: Optional[float] = None,
        altitude_method_code: Optional[str] = None,
        altitude_method_name: Optional[str] = None,
        aquifer_code: Optional[str] = None,
        aquifer_type_code: Optional[str] = None,
        basin_code: Optional[str] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        begin: Optional[str] = None,
        computation_identifier: Optional[str] = None,
        construction_date: Optional[str] = None,
        contributing_drainage_area: Optional[float] = None,
        country_code: Optional[str] = None,
        country_name: Optional[str] = None,
        county_code: Optional[str] = None,
        county_name: Optional[str] = None,
        crs: Optional[URL] = None,
        data_type: Optional[str] = None,
        depth_source_code: Optional[str] = None,
        district_code: Optional[str] = None,
        drainage_area: Optional[float] = None,
        end: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        hole_constructed_depth: Optional[float] = None,
        horizontal_position_method_code: Optional[str] = None,
        horizontal_position_method_name: Optional[str] = None,
        horizontal_positional_accuracy: Optional[str] = None,
        horizontal_positional_accuracy_code: Optional[str] = None,
        hydrologic_unit_code: Optional[str] = None,
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        minor_civil_division_code: Optional[str] = None,
        monitoring_location_id: Optional[str] = None,
        monitoring_location_name: Optional[str] = None,
        monitoring_location_number: Optional[str] = None,
        national_aquifer_code: Optional[str] = None,
        offset: Optional[int] = 0,
        original_horizontal_datum: Optional[str] = None,
        original_horizontal_datum_name: Optional[str] = None,
        parameter_code: Optional[str] = None,
        parameter_description: Optional[str] = None,
        parameter_name: Optional[str] = None,
        parent_time_series_id: Optional[str] = None,
        primary: Optional[str] = None,
        properties: Optional[Sequence[Literal["monitoring_location_id", "agency_code", "agency_name", "monitoring_location_number", "monitoring_location_name", "district_code", "country_code", "country_name", "state_code", "state_name", "county_code", "county_name", "minor_civil_division_code", "site_type_code", "site_type", "hydrologic_unit_code", "basin_code", "altitude", "altitude_accuracy", "altitude_method_code", "altitude_method_name", "vertical_datum", "vertical_datum_name", "horizontal_positional_accuracy_code", "horizontal_positional_accuracy", "horizontal_position_method_code", "horizontal_position_method_name", "original_horizontal_datum", "original_horizontal_datum_name", "drainage_area", "contributing_drainage_area", "time_zone_abbreviation", "uses_daylight_savings", "construction_date", "aquifer_code", "national_aquifer_code", "aquifer_type_code", "well_constructed_depth", "hole_constructed_depth", "depth_source_code", "id", "unit_of_measure", "parameter_name", "parameter_code", "statistic_id", "last_modified", "begin", "end", "data_type", "computation_identifier", "thresholds", "sublocation_identifier", "primary", "web_description", "parameter_description", "parent_time_series_id"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        site_type: Optional[str] = None,
        site_type_code: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        state_code: Optional[str] = None,
        state_name: Optional[str] = None,
        statistic_id: Optional[str] = None,
        sublocation_identifier: Optional[str] = None,
        thresholds: Optional[str] = None,
        time_zone_abbreviation: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        uses_daylight_savings: Optional[str] = None,
        vertical_datum: Optional[str] = None,
        vertical_datum_name: Optional[str] = None,
        web_description: Optional[str] = None,
        well_constructed_depth: Optional[float] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from combined-metadata.

        Args:
            agency_code: The agency that is reporting the data. Agency codes are fixed values
                assigned by the National Water Information System (NWIS). A list of
                agency codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/agency-codes/ite
                ms](https://api.waterdata.usgs.gov/ogcapi/v0/collections/agency-
                codes/items).
            agency_name: The name of the agency that is reporting the data.
            altitude: Altitude of the monitoring location referenced to the specified
                Vertical Datum.
            altitude_accuracy: Accuracy of the altitude, in feet. An accuracy of +/- 0.1 foot would
                be entered as “.1”. Many altitudes are interpolated from the contours
                on topographic maps; accuracies determined in this way are generally
                entered as one-half of the contour interval.
            altitude_method_code: Codes representing the method used to measure altitude.
            altitude_method_name: The name of the method used to measure altitude.
            aquifer_code: Local aquifers in the USGS water resources data base are identified by
                a geohydrologic unit code (a three-digit number related to the age of
                the formation, followed by a 4 or 5 character abbreviation for the
                geologic unit or aquifer name).
            aquifer_type_code: Describes the confinement status of an aquifer at the monitoring
                location. A confined aquifer is an aquifer below the land surface that
                is saturated with water. A water table--or unconfined--aquifer is an
                aquifer whose upper water surface (water table) is at atmospheric
                pressure, and thus is able to rise and fall.
            basin_code: The Basin Code or "drainage basin code" is a two-digit code that
                further subdivides the 8-digit hydrologic-unit code. The drainage
                basin code is defined by the USGS State Office where the monitoring
                location is located.
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            begin: The datetime of the earliest observation in the time series. Together
                with `end`, this field represents the period of record of a time
                series. Note that some time series may have large gaps in their
                collection record.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `begin` that intersects the value of
                datetime are selected.
            computation_identifier: Indicates whether the data from this time series represent a specific
                statistical computation. Split parameters are enabled for this field,
                so you can supply multiple values separated by commas.
            construction_date: Date the well was completed.
            contributing_drainage_area: The contributing drainage area of a lake, stream, wetland, or estuary
                monitoring location, in square miles. This item should be present only
                if the contributing area is different from the total drainage area.
                This situation can occur when part of the drainage area consists of
                very porous soil or depressions that either allow all runoff to enter
                the groundwater or traps the water in ponds so that rainfall does not
                contribute to runoff. A transbasin diversion can also affect the total
                drainage area.
            country_code: The code for the country in which the monitoring location is located.
            country_name: The name of the country in which the monitoring location is located.
            county_code: The code for the county or county equivalent (parish, borough, etc.)
                in which the monitoring location is located. A list of codes is
                available at [https://api.waterdata.usgs.gov/ogcapi/v0/collections/cou
                nties/items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/coun
                ties/items).
            county_name: The name of the county or county equivalent (parish, borough, etc.) in
                which the monitoring location is located. [A list of codes is
                available at [https://api.waterdata.usgs.gov/ogcapi/v0/collections/cou
                nties/items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/coun
                ties/items).
            crs: Indicates the coordinate reference system for the results.
            data_type: The computational period type of data collected at the monitoring
                location.
            depth_source_code: A code indicating the source of water-level data.
            district_code: The Water Science Centers (WSCs) across the United States use the FIPS
                state code as the district code. In some case, monitoring locations
                and samples may be managed by a water science center that is adjacent
                to the state in which the monitoring location actually resides. For
                example a monitoring location may have a district code of 30 which
                translates to Montana, but the state code could be 56 for Wyoming
                because that is where the monitoring location actually is located.
            drainage_area: The area enclosed by a topographic divide from which direct surface
                runoff from precipitation normally drains by gravity into the stream
                above that point.
            end: The datetime of the most recent observation in the time series. Data
                returned by this endpoint updates at most once per day, and
                potentially less frequently than that, and as such there may be more
                recent observations within a time series than the time series `end`
                value reflects. Together with `begin`, this field represents the
                period of record of a time series. It is additionally used to
                determine whether a time series is "active".
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `end` that intersects the value of datetime
                are selected.
            f: The optional f parameter indicates the output format which the server
                shall provide as part of the response document.  The default format is
                GeoJSON.
            hole_constructed_depth: The total depth to which the hole is drilled, in feet below land
                surface datum. Note: Not all groundwater monitoring locations have
                information on Hole Depth. Such monitoring locations will not be
                retrieved using this search criteria.
            horizontal_position_method_code: Indicates the method used to determine latitude longitude values. A
                list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                method-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collectio
                ns/coordinate-method-codes/items).
            horizontal_position_method_name: Indicates the method used to determine latitude longitude values. A
                list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                method-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collectio
                ns/coordinate-method-codes/items).
            horizontal_positional_accuracy: Indicates the accuracy of the latitude longitude values. A list of
                codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                accuracy-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collect
                ions/coordinate-accuracy-codes/items).
            horizontal_positional_accuracy_code: Indicates the accuracy of the latitude longitude values. A list of
                codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                accuracy-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collect
                ions/coordinate-accuracy-codes/items).
            hydrologic_unit_code: The United States is divided and sub-divided into successively smaller
                hydrologic units which are classified into four levels: regions, sub-
                regions, accounting units, and cataloging units. The hydrologic units
                are arranged within each other, from the smallest (cataloging units)
                to the largest (regions). Each hydrologic unit is identified by a
                unique hydrologic unit code (HUC) consisting of two to eight digits
                based on the four levels of classification in the hydrologic unit
                system.
                 Search will match partial HUCs.
            lang: The optional lang parameter instructs the server return a response in
                a certain language, if supported.  If the language is not among the
                available values, the Accept-Language header language will be used if
                it is supported. If the header is missing, the default server language
                is used. Note that providers may only support a single language (or
                often no language at all), that can be different from the server
                language.  Language strings can be written in a complex (e.g. "fr-
                CA,fr;q=0.9,en-US;q=0.8,en;q=0.7"), simple (e.g. "de") or locale-like
                (e.g. "de-CH" or "fr_BE") fashion.
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            minor_civil_division_code: Codes for primary governmental or administrative divisions of the
                county or county equivalent in which the monitoring location is
                located.
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            monitoring_location_name: This is the official name of the monitoring location in the database.
                For well information this can be a district-assigned local number.
            monitoring_location_number: Each monitoring location in the USGS data base has a unique 8- to
                15-digit identification number.
            national_aquifer_code: National aquifers are the principal aquifers or aquifer systems in the
                United States, defined as regionally extensive aquifers or aquifer
                systems that have the potential to be used as a source of potable
                water. Not all groundwater monitoring locations can be associated with
                a National Aquifer. Such monitoring locations will not be retrieved
                using this search criteria. A list of National aquifer codes and names
                is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/national-
                aquifer-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collecti
                ons/national-aquifer-codes/items).
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            original_horizontal_datum: Coordinates are published in EPSG:4326 / WGS84 / World Geodetic System
                1984. This field indicates the original datum used to determine
                coordinates before they were converted. A list of codes is available
                at [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                datum-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collection
                s/coordinate-datum-codes/items).
            original_horizontal_datum_name: Coordinates are published in EPSG:4326 / WGS84 / World Geodetic System
                1984. This field indicates the original datum used to determine
                coordinates before they were converted. A list of codes is available
                at [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                datum-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collection
                s/coordinate-datum-codes/items).
            parameter_code: Parameter codes are 5-digit codes used to identify the constituent
                measured and the units of measure. A complete list of parameter codes
                and associated groupings can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            parameter_description: A description of what the parameter code represents, as used by WDFN
                and other USGS data dissemination products.
            parameter_name: A human-understandable name corresponding to `parameter_code`.
            parent_time_series_id: The unique identifier representing the parent or "upchain" time series
                that a daily values time series is generated from. Daily values time
                series have one and only one parent time series.
            primary: A flag identifying if the time series is a "primary" time series.
                "Primary" time series (which have this flag) are standard observations
                which undergo [Bureau review and approval
                processes](https://www.usgs.gov/survey-manual/5028-fundamental-
                science-practices-review-and-approval-scientific-data-release). Non-
                primary time series, which will have missing values for "primary", are
                provisional datasets made available to meet the need for timely best
                science and to assist with daily operations which need real-time
                information. Non-primary time series data are only retained by this
                system for 120 days. See the [USGS Provisional Data
                Statement](https://waterdata.usgs.gov/provisional-data-statement/) for
                more information.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: The ID of the time series or field measurement series (identified by
                `data_type`) that collection metadata corresponds to. Split parameters
                are enabled for this field, so you can supply multiple values
                separated by commas.
            site_type: A description of the hydrologic setting of the monitoring location. A
                list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/site-types/items
                ](https://api.waterdata.usgs.gov/ogcapi/v0/collections/site-
                types/items).
            site_type_code: A code describing the hydrologic setting of the monitoring location. A
                list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/site-types/items
                ](https://api.waterdata.usgs.gov/ogcapi/v0/collections/site-
                types/items).
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            state_code: State code. A [two-digit ANSI
                code](https://www2.census.gov/geo/docs/reference/state.txt) (formerly
                FIPS code) as defined by the American National Standards Institute, to
                define States and equivalents. A three-digit ANSI code is used to
                define counties and county equivalents. [A lookup table is
                available.](https://www.census.gov/library/reference/code-
                lists/ansi.html#states) The only countries with political subdivisions
                other than the US are Mexico and Canada. The Mexican states have US
                state codes ranging from 81-86 and Canadian provinces have state codes
                ranging from 90-98.
            state_name: The name of the state or state equivalent in which the monitoring
                location is located.
            statistic_id: A code corresponding to the statistic an observation represents.
                Example codes include 00001 (max), 00002 (min), and 00003 (mean). A
                complete list of codes and their descriptions can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            sublocation_identifier: An optional human-readable identifier used to specify where
                measurements are recorded at a monitoring location.
            thresholds: Thresholds represent known numeric limits for a time series, for
                example the historic maximum value for a parameter or a level below
                which a sensor is non-operative. These thresholds are sometimes used
                to automatically determine if an observation is erroneous due to
                sensor error, and therefore shouldn't be included in the time series.
            time_zone_abbreviation: A short code describing the time zone used by a monitoring location.
            unit_of_measure: A human-readable description of the units of measurement associated
                with an observation.
            uses_daylight_savings: A flag indicating whether or not a monitoring location uses daylight
                savings.
            vertical_datum: The datum used to determine altitude and vertical position at the
                monitoring location. A list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-datums/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-
                datums/items).
            vertical_datum_name: The datum used to determine altitude and vertical position at the
                monitoring location. A list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-datums/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-
                datums/items).
            web_description: A description of what this time series represents, as used by WDFN and
                other USGS data dissemination products.
            well_constructed_depth: The depth of the finished well, in feet below land surface datum.
                Note: Not all groundwater monitoring locations have information on
                Well Depth. Such monitoring locations will not be retrieved using this
                search criteria.
        """
        # Translate Python parameters to API parameters
        query = {
            "agency_code": agency_code,
            "agency_name": agency_name,
            "altitude": altitude,
            "altitude_accuracy": altitude_accuracy,
            "altitude_method_code": altitude_method_code,
            "altitude_method_name": altitude_method_name,
            "aquifer_code": aquifer_code,
            "aquifer_type_code": aquifer_type_code,
            "basin_code": basin_code,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "begin": begin,
            "computation_identifier": computation_identifier,
            "construction_date": construction_date,
            "contributing_drainage_area": contributing_drainage_area,
            "country_code": country_code,
            "country_name": country_name,
            "county_code": county_code,
            "county_name": county_name,
            "crs": crs,
            "data_type": data_type,
            "depth_source_code": depth_source_code,
            "district_code": district_code,
            "drainage_area": drainage_area,
            "end": end,
            "f": f,
            "hole_constructed_depth": hole_constructed_depth,
            "horizontal_position_method_code": horizontal_position_method_code,
            "horizontal_position_method_name": horizontal_position_method_name,
            "horizontal_positional_accuracy": horizontal_positional_accuracy,
            "horizontal_positional_accuracy_code": horizontal_positional_accuracy_code,
            "hydrologic_unit_code": hydrologic_unit_code,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "minor_civil_division_code": minor_civil_division_code,
            "monitoring_location_id": monitoring_location_id,
            "monitoring_location_name": monitoring_location_name,
            "monitoring_location_number": monitoring_location_number,
            "national_aquifer_code": national_aquifer_code,
            "offset": offset,
            "original_horizontal_datum": original_horizontal_datum,
            "original_horizontal_datum_name": original_horizontal_datum_name,
            "parameter_code": parameter_code,
            "parameter_description": parameter_description,
            "parameter_name": parameter_name,
            "parent_time_series_id": parent_time_series_id,
            "primary": primary,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "site_type": site_type,
            "site_type_code": site_type_code,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "state_code": state_code,
            "state_name": state_name,
            "statistic_id": statistic_id,
            "sublocation_identifier": sublocation_identifier,
            "thresholds": thresholds,
            "time_zone_abbreviation": time_zone_abbreviation,
            "unit_of_measure": unit_of_measure,
            "uses_daylight_savings": uses_daylight_savings,
            "vertical_datum": vertical_datum,
            "vertical_datum_name": vertical_datum_name,
            "web_description": web_description,
            "well_constructed_depth": well_constructed_depth,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class ContinuousClient(BaseClient[TransformedResponse_co]):
    """
    Continuous data are collected via automated sensors installed at a
    monitoring location. They are collected at a high frequency and often
    at a fixed 15-minute interval. Depending on the specific monitoring
    location, the data may be transmitted automatically via telemetry and
    be available on WDFN within minutes of collection, while other times
    the delivery of data may be delayed if the monitoring location does
    not have the capacity to automatically transmit data. Continuous data
    are described by parameter name and parameter code (pcode). These data
    might also be referred to as "instantaneous values" or "IV".
    """
    _endpoint = USGSCollection.CONTINUOUS

    def get(
        self,
        approval_status: Optional[Literal["Provisional", "Approved"]] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        datetime: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        monitoring_location_id: Optional[str] = None,
        offset: Optional[int] = 0,
        parameter_code: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = None,
        qualifier: Optional[str] = None,
        query_filter: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        statistic_id: Optional[str] = None,
        time: Optional[str] = None,
        time_series_id: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        value: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from continuous.

        Args:
            approval_status: Some of the data that you have obtained from this U.S. Geological
                Survey database may not have received Director's approval.  Any such
                data values are qualified as provisional and are subject to revision.
                Provisional data are released on the condition that neither the USGS
                nor the United States Government may be held liable for any damages
                resulting from its use. This field reflects the approval status of
                each record, and is either "Approved", meaining processing review has
                been completed and the data is approved for publication, or
                "Provisional" and subject to revision. For more information about
                provisional data, go to [https://waterdata.usgs.gov/provisional-data-
                statement/](https://waterdata.usgs.gov/provisional-data-statement/).
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            crs: Indicates the coordinate reference system for the results.
            datetime: Either a date-time or an interval. Date and time expressions adhere to
                RFC 3339.
                Intervals may be bounded or half-bounded (double-dots at start or
                end).

                Examples:

                * A date-time: "2018-02-12T23:20:50Z"
                * A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                * Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"

                Only features that have a temporal property that intersects the value
                of
                `datetime` are selected.

                If a feature has multiple temporal properties, it is the decision of
                the
                server whether only a single temporal property is used to determine
                the extent or all relevant temporal properties.
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
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            parameter_code: Parameter codes are 5-digit codes used to identify the constituent
                measured and the units of measure. A complete list of parameter codes
                and associated groupings can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            qualifier: This field indicates any qualifiers associated with an observation,
                for instance if a sensor may have been impacted by ice or if values
                were estimated.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            statistic_id: A code corresponding to the statistic an observation represents.
                Example codes include 00001 (max), 00002 (min), and 00003 (mean). A
                complete list of codes and their descriptions can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-
                codes/items).
            time: The date an observation represents. You can query this field using
                date-times or intervals, adhering to RFC 3339, or using ISO 8601
                duration objects. Intervals may be bounded or half-bounded (double-
                dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `time` that intersects the value of datetime
                are selected. If a feature has multiple temporal properties, it is the
                decision of the server whether only a single temporal property is used
                to determine the extent or all relevant temporal properties.
            time_series_id: A unique identifier representing a single time series. This
                corresponds to the `id` field in the `time-series-metadata` endpoint.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            unit_of_measure: A human-readable description of the units of measurement associated
                with an observation.
            value: The value of the observation. Values are transmitted as strings in the
                JSON response format in order to preserve precision.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": approval_status,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "datetime": datetime,
            "f": f,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "monitoring_location_id": monitoring_location_id,
            "offset": offset,
            "parameter_code": parameter_code,
            "properties": properties,
            "qualifier": qualifier,
            "filter": query_filter,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "statistic_id": statistic_id,
            "time": time,
            "time_series_id": time_series_id,
            "unit_of_measure": unit_of_measure,
            "value": value,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class CoordinateAccuracyCodesClient(BaseClient[TransformedResponse_co]):
    """
    Appropriate code on the schedule to indicate the accuracy of the
    latitude-longitude values.
    """
    _endpoint = USGSCollection.COORDINATE_ACCURACY_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        coordinate_accuracy_description: Optional[str] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "coordinate_accuracy_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from coordinate-accuracy-codes.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            coordinate_accuracy_description: 
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
            query_id: 
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "coordinate_accuracy_description": coordinate_accuracy_description,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class CoordinateDatumCodesClient(BaseClient[TransformedResponse_co]):
    """
    Horizontal datum code for the latitude/longitude coordinates. There
    are currently more than 300 horizontal datums available for entry.
    """
    _endpoint = USGSCollection.COORDINATE_DATUM_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        coordinate_datum_description: Optional[str] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "coordinate_datum_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from coordinate-datum-codes.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            coordinate_datum_description: 
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
            query_id: 
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "coordinate_datum_description": coordinate_datum_description,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class CoordinateMethodCodesClient(BaseClient[TransformedResponse_co]):
    """
    Methods used to determine latitude-longitude values.
    """
    _endpoint = USGSCollection.COORDINATE_METHOD_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        coordinate_method_description: Optional[str] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "coordinate_method_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from coordinate-method-codes.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            coordinate_method_description: 
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
            query_id: 
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "coordinate_method_description": coordinate_method_description,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class CountiesClient(BaseClient[TransformedResponse_co]):
    """
    The name of the county or county equivalent (parish, borough, planning
    reagion, etc.) in which the site is located. List includes Census
    Bureau FIPS county codes, names and associated Country and State.
    """
    _endpoint = USGSCollection.COUNTIES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        country_code: Optional[str] = None,
        county_fips_code: Optional[str] = None,
        county_name: Optional[str] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "country_code", "state_fips_code", "county_fips_code", "county_name"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        state_fips_code: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from counties.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            country_code: FIPS country code as defined by FIPS PUB 10-4: Countries,
                Dependencies, Areas of Special Sovereignty, and Their Principal
                Administrative Divisions.
            county_fips_code: County FIPS code. A two digit code indicating a U.S. county as defined
                by FIPS 5-2.
            county_name: County name. The name of a U.S. county as defined by FIPS 5-2.
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
            query_id: 
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
            state_fips_code: State FIPS code.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "country_code": country_code,
            "county_fips_code": county_fips_code,
            "county_name": county_name,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "state_fips_code": state_fips_code,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class CountriesClient(BaseClient[TransformedResponse_co]):
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
        ) -> TransformedResponse_co | list[dict[str, Any]]:
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
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "country_name": country_name,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class DailyClient(BaseClient[TransformedResponse_co]):
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
    _endpoint = USGSCollection.DAILY

    def get(
        self,
        approval_status: Optional[Literal["Provisional", "Approved"]] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        datetime: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        monitoring_location_id: Optional[str] = None,
        offset: Optional[int] = 0,
        parameter_code: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = None,
        qualifier: Optional[str] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        statistic_id: Optional[str] = None,
        time: Optional[str] = None,
        time_series_id: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        value: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from daily.

        Args:
            approval_status: Some of the data that you have obtained from this U.S. Geological
                Survey database may not have received Director's approval.  Any such
                data values are qualified as provisional and are subject to revision.
                Provisional data are released on the condition that neither the USGS
                nor the United States Government may be held liable for any damages
                resulting from its use. This field reflects the approval status of
                each record, and is either "Approved", meaining processing review has
                been completed and the data is approved for publication, or
                "Provisional" and subject to revision. For more information about
                provisional data, go to [https://waterdata.usgs.gov/provisional-data-
                statement/](https://waterdata.usgs.gov/provisional-data-statement/).
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            crs: Indicates the coordinate reference system for the results.
            datetime: Either a date-time or an interval. Date and time expressions adhere to
                RFC 3339.
                Intervals may be bounded or half-bounded (double-dots at start or
                end).

                Examples:

                * A date-time: "2018-02-12T23:20:50Z"
                * A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                * Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"

                Only features that have a temporal property that intersects the value
                of
                `datetime` are selected.

                If a feature has multiple temporal properties, it is the decision of
                the
                server whether only a single temporal property is used to determine
                the extent or all relevant temporal properties.
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
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            parameter_code: Parameter codes are 5-digit codes used to identify the constituent
                measured and the units of measure. A complete list of parameter codes
                and associated groupings can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            qualifier: This field indicates any qualifiers associated with an observation,
                for instance if a sensor may have been impacted by ice or if values
                were estimated.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: A universally unique identifier (UUID) representing a single version
                of a record. It is not stable over time. Every time the record is
                refreshed in our database (which may happen as part of normal
                operations and does not imply any change to the data itself) a new ID
                will be generated. To uniquely identify a single observation over
                time, compare the `time` and `time_series_id` fields; each time series
                will only have a single observation at a given `time`.
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            statistic_id: A code corresponding to the statistic an observation represents.
                Example codes include 00001 (max), 00002 (min), and 00003 (mean). A
                complete list of codes and their descriptions can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            time: The date an observation represents. You can query this field using
                date-times or intervals, adhering to RFC 3339, or using ISO 8601
                duration objects. Intervals may be bounded or half-bounded (double-
                dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `time` that intersects the value of datetime
                are selected. If a feature has multiple temporal properties, it is the
                decision of the server whether only a single temporal property is used
                to determine the extent or all relevant temporal properties.
            time_series_id: A unique identifier representing a single time series. This
                corresponds to the `id` field in the `time-series-metadata` endpoint.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            unit_of_measure: A human-readable description of the units of measurement associated
                with an observation.
            value: The value of the observation. Values are transmitted as strings in the
                JSON response format in order to preserve precision.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": approval_status,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "datetime": datetime,
            "f": f,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "monitoring_location_id": monitoring_location_id,
            "offset": offset,
            "parameter_code": parameter_code,
            "properties": properties,
            "qualifier": qualifier,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "statistic_id": statistic_id,
            "time": time,
            "time_series_id": time_series_id,
            "unit_of_measure": unit_of_measure,
            "value": value,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class FieldMeasurementsClient(BaseClient[TransformedResponse_co]):
    """
    Field measurements are physically measured values collected during a
    visit to the monitoring location. Field measurements consist of
    measurements of gage height and discharge, and readings of groundwater
    levels, and are primarily used as calibration readings for the
    automated sensors collecting continuous data. They are collected at a
    low frequency, and delivery of the data in WDFN may be delayed due to
    data processing time.
    """
    _endpoint = USGSCollection.FIELD_MEASUREMENTS

    def get(
        self,
        approval_status: Optional[Literal["Provisional", "Approved"]] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        control_condition: Optional[str] = None,
        crs: Optional[URL] = None,
        datetime: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        field_measurements_series_id: Optional[str] = None,
        field_visit_id: Optional[str] = None,
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        measurement_rated: Optional[str] = None,
        measuring_agency: Optional[str] = None,
        monitoring_location_id: Optional[str] = None,
        observing_procedure: Optional[str] = None,
        observing_procedure_code: Optional[str] = None,
        offset: Optional[int] = 0,
        parameter_code: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "field_measurements_series_id", "field_visit_id", "parameter_code", "monitoring_location_id", "observing_procedure_code", "observing_procedure", "value", "unit_of_measure", "time", "qualifier", "vertical_datum", "approval_status", "measuring_agency", "last_modified", "control_condition", "measurement_rated"]]] = None,
        qualifier: Optional[str] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        time: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        value: Optional[str] = None,
        vertical_datum: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from field-measurements.

        Args:
            approval_status: Some of the data that you have obtained from this U.S. Geological
                Survey database may not have received Director's approval.  Any such
                data values are qualified as provisional and are subject to revision.
                Provisional data are released on the condition that neither the USGS
                nor the United States Government may be held liable for any damages
                resulting from its use. This field reflects the approval status of
                each record, and is either "Approved", meaining processing review has
                been completed and the data is approved for publication, or
                "Provisional" and subject to revision. For more information about
                provisional data, go to [https://waterdata.usgs.gov/provisional-data-
                statement/](https://waterdata.usgs.gov/provisional-data-statement/).
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            control_condition: 
            crs: Indicates the coordinate reference system for the results.
            datetime: Either a date-time or an interval. Date and time expressions adhere to
                RFC 3339.
                Intervals may be bounded or half-bounded (double-dots at start or
                end).

                Examples:

                * A date-time: "2018-02-12T23:20:50Z"
                * A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                * Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"

                Only features that have a temporal property that intersects the value
                of
                `datetime` are selected.

                If a feature has multiple temporal properties, it is the decision of
                the
                server whether only a single temporal property is used to determine
                the extent or all relevant temporal properties.
            f: The optional f parameter indicates the output format which the server
                shall provide as part of the response document.  The default format is
                GeoJSON.
            field_measurements_series_id: A unique identifier representing a single collection series. This
                corresponds to the `id` field in the  `field-measurements-metadata`
                endpoint.
            field_visit_id: A universally unique identifier (UUID) for the field visit. Multiple
                measurements may be made during a single field visit.
            lang: The optional lang parameter instructs the server return a response in
                a certain language, if supported.  If the language is not among the
                available values, the Accept-Language header language will be used if
                it is supported. If the header is missing, the default server language
                is used. Note that providers may only support a single language (or
                often no language at all), that can be different from the server
                language.  Language strings can be written in a complex (e.g. "fr-
                CA,fr;q=0.9,en-US;q=0.8,en;q=0.7"), simple (e.g. "de") or locale-like
                (e.g. "de-CH" or "fr_BE") fashion.
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            measurement_rated: 
            measuring_agency: The agency performing the measurement.
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            observing_procedure: Water measurement or water-quality observing procedure descriptions.
            observing_procedure_code: A short code corresponding to the observing procedure for the field
                measurement.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            parameter_code: Parameter codes are 5-digit codes used to identify the constituent
                measured and the units of measure. A complete list of parameter codes
                and associated groupings can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            qualifier: This field indicates any qualifiers associated with an observation,
                for instance if a sensor may have been impacted by ice or if values
                were estimated.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: A universally unique identifier (UUID) representing a single version
                of a record. It is not stable over time. Every time the record is
                refreshed in our database (which may happen as part of normal
                operations and does not imply any change to the data itself) a new ID
                will be generated. To uniquely identify a single observation over
                time, compare the `time` and `time_series_id` fields; each time series
                will only have a single observation at a given `time`.
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            time: The date an observation represents. You can query this field using
                date-times or intervals, adhering to RFC 3339, or using ISO 8601
                duration objects. Intervals may be bounded or half-bounded (double-
                dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `time` that intersects the value of datetime
                are selected. If a feature has multiple temporal properties, it is the
                decision of the server whether only a single temporal property is used
                to determine the extent or all relevant temporal properties.
            unit_of_measure: A human-readable description of the units of measurement associated
                with an observation.
            value: The value of the observation. Values are transmitted as strings in the
                JSON response format in order to preserve precision.
            vertical_datum: The datum used to determine altitude and vertical position at the
                monitoring location. A list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-datums/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-
                datums/items).
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": approval_status,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "control_condition": control_condition,
            "crs": crs,
            "datetime": datetime,
            "f": f,
            "field_measurements_series_id": field_measurements_series_id,
            "field_visit_id": field_visit_id,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "measurement_rated": measurement_rated,
            "measuring_agency": measuring_agency,
            "monitoring_location_id": monitoring_location_id,
            "observing_procedure": observing_procedure,
            "observing_procedure_code": observing_procedure_code,
            "offset": offset,
            "parameter_code": parameter_code,
            "properties": properties,
            "qualifier": qualifier,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "time": time,
            "unit_of_measure": unit_of_measure,
            "value": value,
            "vertical_datum": vertical_datum,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class FieldMeasurementsMetadataClient(BaseClient[TransformedResponse_co]):
    """
    This endpoint provides metadata about field measurement collections,
    including when the earliest and most recent observations for a
    parameter occurred at a monitoring location and its units.
    """
    _endpoint = USGSCollection.FIELD_MEASUREMENTS_METADATA

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        begin: Optional[str] = None,
        crs: Optional[URL] = None,
        end: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        monitoring_location_id: Optional[str] = None,
        offset: Optional[int] = 0,
        parameter_code: Optional[str] = None,
        parameter_description: Optional[str] = None,
        parameter_name: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "monitoring_location_id", "parameter_code", "parameter_name", "parameter_description", "begin", "end", "last_modified"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from field-measurements-metadata.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            begin: The datetime of the earliest observation in the time series. Together
                with `end`, this field represents the period of record of a time
                series. Note that some time series may have large gaps in their
                collection record.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `begin` that intersects the value of
                datetime are selected.
            crs: Indicates the coordinate reference system for the results.
            end: The datetime of the most recent observation in the time series. Data
                returned by this endpoint updates at most once per day, and
                potentially less frequently than that, and as such there may be more
                recent observations within a time series than the time series `end`
                value reflects. Together with `begin`, this field represents the
                period of record of a time series. It is additionally used to
                determine whether a time series is "active".
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `end` that intersects the value of datetime
                are selected.
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
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            parameter_code: Parameter codes are 5-digit codes used to identify the constituent
                measured and the units of measure. A complete list of parameter codes
                and associated groupings can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            parameter_description: A description of what the parameter code represents, as used by WDFN
                and other USGS data dissemination products.
            parameter_name: A human-understandable name corresponding to `parameter_code`.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: A universally unique identifier (UUID) representing a single version
                of a record. It is not stable over time. Every time the record is
                refreshed in our database (which may happen as part of normal
                operations and does not imply any change to the data itself) a new ID
                will be generated. To uniquely identify a single observation over
                time, compare the `time` and `time_series_id` fields; each time series
                will only have a single observation at a given `time`.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "begin": begin,
            "crs": crs,
            "end": end,
            "f": f,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "monitoring_location_id": monitoring_location_id,
            "offset": offset,
            "parameter_code": parameter_code,
            "parameter_description": parameter_description,
            "parameter_name": parameter_name,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class HydrologicUnitCodesClient(BaseClient[TransformedResponse_co]):
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
        ) -> TransformedResponse_co | list[dict[str, Any]]:
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "hydrologic_unit_classification_code": hydrologic_unit_classification_code,
            "hydrologic_unit_name": hydrologic_unit_name,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class LatestContinuousClient(BaseClient[TransformedResponse_co]):
    """
    This endpoint provides the most recent observation for each time
    series of continuous data. Continuous data are collected via automated
    sensors installed at a monitoring location. They are collected at a
    high frequency and often at a fixed 15-minute interval. Depending on
    the specific monitoring location, the data may be transmitted
    automatically via telemetry and be available on WDFN within minutes of
    collection, while other times the delivery of data may be delayed if
    the monitoring location does not have the capacity to automatically
    transmit data. Continuous data are described by parameter name and
    parameter code. These data might also be referred to as "instantaneous
    values" or "IV"
    """
    _endpoint = USGSCollection.LATEST_CONTINUOUS

    def get(
        self,
        approval_status: Optional[Literal["Provisional", "Approved"]] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        datetime: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        monitoring_location_id: Optional[str] = None,
        offset: Optional[int] = 0,
        parameter_code: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = None,
        qualifier: Optional[str] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        statistic_id: Optional[str] = None,
        time: Optional[str] = None,
        time_series_id: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        value: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from latest-continuous.

        Args:
            approval_status: Some of the data that you have obtained from this U.S. Geological
                Survey database may not have received Director's approval.  Any such
                data values are qualified as provisional and are subject to revision.
                Provisional data are released on the condition that neither the USGS
                nor the United States Government may be held liable for any damages
                resulting from its use. This field reflects the approval status of
                each record, and is either "Approved", meaining processing review has
                been completed and the data is approved for publication, or
                "Provisional" and subject to revision. For more information about
                provisional data, go to [https://waterdata.usgs.gov/provisional-data-
                statement/](https://waterdata.usgs.gov/provisional-data-statement/).
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            crs: Indicates the coordinate reference system for the results.
            datetime: Either a date-time or an interval. Date and time expressions adhere to
                RFC 3339.
                Intervals may be bounded or half-bounded (double-dots at start or
                end).

                Examples:

                * A date-time: "2018-02-12T23:20:50Z"
                * A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                * Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"

                Only features that have a temporal property that intersects the value
                of
                `datetime` are selected.

                If a feature has multiple temporal properties, it is the decision of
                the
                server whether only a single temporal property is used to determine
                the extent or all relevant temporal properties.
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
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            parameter_code: Parameter codes are 5-digit codes used to identify the constituent
                measured and the units of measure. A complete list of parameter codes
                and associated groupings can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            qualifier: This field indicates any qualifiers associated with an observation,
                for instance if a sensor may have been impacted by ice or if values
                were estimated.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: A universally unique identifier (UUID) representing a single version
                of a record. It is not stable over time. Every time the record is
                refreshed in our database (which may happen as part of normal
                operations and does not imply any change to the data itself) a new ID
                will be generated. To uniquely identify a single observation over
                time, compare the `time` and `time_series_id` fields; each time series
                will only have a single observation at a given `time`.
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            statistic_id: A code corresponding to the statistic an observation represents.
                Example codes include 00001 (max), 00002 (min), and 00003 (mean). A
                complete list of codes and their descriptions can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-
                codes/items).
            time: The date an observation represents. You can query this field using
                date-times or intervals, adhering to RFC 3339, or using ISO 8601
                duration objects. Intervals may be bounded or half-bounded (double-
                dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `time` that intersects the value of datetime
                are selected. If a feature has multiple temporal properties, it is the
                decision of the server whether only a single temporal property is used
                to determine the extent or all relevant temporal properties.
            time_series_id: A unique identifier representing a single time series. This
                corresponds to the `id` field in the `time-series-metadata` endpoint.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            unit_of_measure: A human-readable description of the units of measurement associated
                with an observation.
            value: The value of the observation. Values are transmitted as strings in the
                JSON response format in order to preserve precision.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": approval_status,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "datetime": datetime,
            "f": f,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "monitoring_location_id": monitoring_location_id,
            "offset": offset,
            "parameter_code": parameter_code,
            "properties": properties,
            "qualifier": qualifier,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "statistic_id": statistic_id,
            "time": time,
            "time_series_id": time_series_id,
            "unit_of_measure": unit_of_measure,
            "value": value,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class LatestDailyClient(BaseClient[TransformedResponse_co]):
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
    _endpoint = USGSCollection.LATEST_DAILY

    def get(
        self,
        approval_status: Optional[Literal["Provisional", "Approved"]] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        datetime: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        monitoring_location_id: Optional[str] = None,
        offset: Optional[int] = 0,
        parameter_code: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "time_series_id", "monitoring_location_id", "parameter_code", "statistic_id", "time", "value", "unit_of_measure", "approval_status", "qualifier", "last_modified"]]] = None,
        qualifier: Optional[str] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        statistic_id: Optional[str] = None,
        time: Optional[str] = None,
        time_series_id: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        value: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from latest-daily.

        Args:
            approval_status: Some of the data that you have obtained from this U.S. Geological
                Survey database may not have received Director's approval.  Any such
                data values are qualified as provisional and are subject to revision.
                Provisional data are released on the condition that neither the USGS
                nor the United States Government may be held liable for any damages
                resulting from its use. This field reflects the approval status of
                each record, and is either "Approved", meaining processing review has
                been completed and the data is approved for publication, or
                "Provisional" and subject to revision. For more information about
                provisional data, go to [https://waterdata.usgs.gov/provisional-data-
                statement/](https://waterdata.usgs.gov/provisional-data-statement/).
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            crs: Indicates the coordinate reference system for the results.
            datetime: Either a date-time or an interval. Date and time expressions adhere to
                RFC 3339.
                Intervals may be bounded or half-bounded (double-dots at start or
                end).

                Examples:

                * A date-time: "2018-02-12T23:20:50Z"
                * A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                * Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"

                Only features that have a temporal property that intersects the value
                of
                `datetime` are selected.

                If a feature has multiple temporal properties, it is the decision of
                the
                server whether only a single temporal property is used to determine
                the extent or all relevant temporal properties.
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
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            parameter_code: Parameter codes are 5-digit codes used to identify the constituent
                measured and the units of measure. A complete list of parameter codes
                and associated groupings can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            qualifier: This field indicates any qualifiers associated with an observation,
                for instance if a sensor may have been impacted by ice or if values
                were estimated.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: A universally unique identifier (UUID) representing a single version
                of a record. It is not stable over time. Every time the record is
                refreshed in our database (which may happen as part of normal
                operations and does not imply any change to the data itself) a new ID
                will be generated. To uniquely identify a single observation over
                time, compare the `time` and `time_series_id` fields; each time series
                will only have a single observation at a given `time`.
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            statistic_id: A code corresponding to the statistic an observation represents.
                Example codes include 00001 (max), 00002 (min), and 00003 (mean). A
                complete list of codes and their descriptions can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            time: The date an observation represents. You can query this field using
                date-times or intervals, adhering to RFC 3339, or using ISO 8601
                duration objects. Intervals may be bounded or half-bounded (double-
                dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `time` that intersects the value of datetime
                are selected. If a feature has multiple temporal properties, it is the
                decision of the server whether only a single temporal property is used
                to determine the extent or all relevant temporal properties.
            time_series_id: A unique identifier representing a single time series. This
                corresponds to the `id` field in the `time-series-metadata` endpoint.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            unit_of_measure: A human-readable description of the units of measurement associated
                with an observation.
            value: The value of the observation. Values are transmitted as strings in the
                JSON response format in order to preserve precision.
        """
        # Translate Python parameters to API parameters
        query = {
            "approval_status": approval_status,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "datetime": datetime,
            "f": f,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "monitoring_location_id": monitoring_location_id,
            "offset": offset,
            "parameter_code": parameter_code,
            "properties": properties,
            "qualifier": qualifier,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "statistic_id": statistic_id,
            "time": time,
            "time_series_id": time_series_id,
            "unit_of_measure": unit_of_measure,
            "value": value,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class MediumCodesClient(BaseClient[TransformedResponse_co]):
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
        ) -> TransformedResponse_co | list[dict[str, Any]]:
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "legacy_medium_code": legacy_medium_code,
            "limit": limit,
            "medium_description": medium_description,
            "medium_name": medium_name,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class MethodCategoriesClient(BaseClient[TransformedResponse_co]):
    """
    Categorical standards for methods describing the associated data's
    appropriateness for an intended use.
    """
    _endpoint = USGSCollection.METHOD_CATEGORIES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        method_category_description: Optional[str] = None,
        method_category_name: Optional[str] = None,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "method_category_name", "method_category_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from method-categories.

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
            method_category_description: Full description of the method category as defined by the USGS Water
                Mission Area standards for field and analytical methods and their fit-
                for-purpose use internally and for public delivery
            method_category_name: Name representing the method category standard.
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
            query_id: Code representing the method category standard.
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "method_category_description": method_category_description,
            "method_category_name": method_category_name,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class MethodCitationsClient(BaseClient[TransformedResponse_co]):
    """
    Citation identifiers for water measurement methods.
    """
    _endpoint = USGSCollection.METHOD_CITATIONS

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        citation_method_number: Optional[str] = None,
        citation_name: Optional[str] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        method_id: Optional[str] = None,
        method_source: Optional[str] = None,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "method_id", "citation_name", "citation_method_number", "method_source"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[int] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from method-citations.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            citation_method_number: Citation method number. A number assigned to a method within a cited
                reference.
            citation_name: Method citation name. An abbreviated citation that describes the
                reference.
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
            method_id: USGS Central Laboratory method code. The lab method used to determine
                a parameter value.
            method_source: Protocol organization code.
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
            query_id: Citation method identification number.
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "citation_method_number": citation_method_number,
            "citation_name": citation_name,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "method_id": method_id,
            "method_source": method_source,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class MethodsClient(BaseClient[TransformedResponse_co]):
    """
    Water measurement or water-quality analytical methods. Codes and
    descriptions defining a method for calculating or measuring the value
    of a water quality or quantity parameter. Method codes are associated
    with one or many parameter codes.
    """
    _endpoint = USGSCollection.METHODS

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        method_category: Optional[str] = None,
        method_description: Optional[str] = None,
        method_name: Optional[str] = None,
        method_type: Optional[str] = None,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "method_type", "method_category", "method_name", "method_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from methods.

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
            method_category: Code representing the method category standard.
            method_description: A long name that fully describes a method.
            method_name: A short name that partially describes a method.
            method_type: Method type for measured or collected data
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
            query_id: Water measurement or water-quality analytical method code. The method
                used to determine a parameter value.
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "method_category": method_category,
            "method_description": method_description,
            "method_name": method_name,
            "method_type": method_type,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class MonitoringLocationsClient(BaseClient[TransformedResponse_co]):
    """
    Location information is basic information about the monitoring
    location including the name, identifier, agency responsible for data
    collection, and the date the location was established. It also
    includes information about the type of location, such as stream, lake,
    or groundwater, and geographic information about the location, such as
    state, county, latitude and longitude, and hydrologic unit code (HUC).
    """
    _endpoint = USGSCollection.MONITORING_LOCATIONS

    def get(
        self,
        agency_code: Optional[str] = None,
        agency_name: Optional[str] = None,
        altitude: Optional[float] = None,
        altitude_accuracy: Optional[float] = None,
        altitude_method_code: Optional[str] = None,
        altitude_method_name: Optional[str] = None,
        aquifer_code: Optional[str] = None,
        aquifer_type_code: Optional[str] = None,
        basin_code: Optional[str] = None,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        construction_date: Optional[str] = None,
        contributing_drainage_area: Optional[float] = None,
        country_code: Optional[str] = None,
        country_name: Optional[str] = None,
        county_code: Optional[str] = None,
        county_name: Optional[str] = None,
        crs: Optional[URL] = None,
        depth_source_code: Optional[str] = None,
        district_code: Optional[str] = None,
        drainage_area: Optional[float] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        hole_constructed_depth: Optional[float] = None,
        horizontal_position_method_code: Optional[str] = None,
        horizontal_position_method_name: Optional[str] = None,
        horizontal_positional_accuracy: Optional[str] = None,
        horizontal_positional_accuracy_code: Optional[str] = None,
        hydrologic_unit_code: Optional[str] = None,
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10,
        minor_civil_division_code: Optional[str] = None,
        monitoring_location_name: Optional[str] = None,
        monitoring_location_number: Optional[str] = None,
        national_aquifer_code: Optional[str] = None,
        offset: Optional[int] = 0,
        original_horizontal_datum: Optional[str] = None,
        original_horizontal_datum_name: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "agency_code", "agency_name", "monitoring_location_number", "monitoring_location_name", "district_code", "country_code", "country_name", "state_code", "state_name", "county_code", "county_name", "minor_civil_division_code", "site_type_code", "site_type", "hydrologic_unit_code", "basin_code", "altitude", "altitude_accuracy", "altitude_method_code", "altitude_method_name", "vertical_datum", "vertical_datum_name", "horizontal_positional_accuracy_code", "horizontal_positional_accuracy", "horizontal_position_method_code", "horizontal_position_method_name", "original_horizontal_datum", "original_horizontal_datum_name", "drainage_area", "contributing_drainage_area", "time_zone_abbreviation", "uses_daylight_savings", "construction_date", "aquifer_code", "national_aquifer_code", "aquifer_type_code", "well_constructed_depth", "hole_constructed_depth", "depth_source_code", "revision_note", "revision_created", "revision_modified"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        revision_created: Optional[str] = None,
        revision_modified: Optional[str] = None,
        revision_note: Optional[str] = None,
        site_type: Optional[str] = None,
        site_type_code: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        state_code: Optional[str] = None,
        state_name: Optional[str] = None,
        time_zone_abbreviation: Optional[str] = None,
        uses_daylight_savings: Optional[str] = None,
        vertical_datum: Optional[str] = None,
        vertical_datum_name: Optional[str] = None,
        well_constructed_depth: Optional[float] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from monitoring-locations.

        Args:
            agency_code: The agency that is reporting the data. Agency codes are fixed values
                assigned by the National Water Information System (NWIS). A list of
                agency codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/agency-codes/ite
                ms](https://api.waterdata.usgs.gov/ogcapi/v0/collections/agency-
                codes/items).
            agency_name: The name of the agency that is reporting the data.
            altitude: Altitude of the monitoring location referenced to the specified
                Vertical Datum.
            altitude_accuracy: Accuracy of the altitude, in feet. An accuracy of +/- 0.1 foot would
                be entered as “.1”. Many altitudes are interpolated from the contours
                on topographic maps; accuracies determined in this way are generally
                entered as one-half of the contour interval.
            altitude_method_code: Codes representing the method used to measure altitude.
            altitude_method_name: The name of the method used to measure altitude.
            aquifer_code: Local aquifers in the USGS water resources data base are identified by
                a geohydrologic unit code (a three-digit number related to the age of
                the formation, followed by a 4 or 5 character abbreviation for the
                geologic unit or aquifer name).
            aquifer_type_code: Describes the confinement status of an aquifer at the monitoring
                location. A confined aquifer is an aquifer below the land surface that
                is saturated with water. A water table--or unconfined--aquifer is an
                aquifer whose upper water surface (water table) is at atmospheric
                pressure, and thus is able to rise and fall.
            basin_code: The Basin Code or "drainage basin code" is a two-digit code that
                further subdivides the 8-digit hydrologic-unit code. The drainage
                basin code is defined by the USGS State Office where the monitoring
                location is located.
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            construction_date: Date the well was completed.
            contributing_drainage_area: The contributing drainage area of a lake, stream, wetland, or estuary
                monitoring location, in square miles. This item should be present only
                if the contributing area is different from the total drainage area.
                This situation can occur when part of the drainage area consists of
                very porous soil or depressions that either allow all runoff to enter
                the groundwater or traps the water in ponds so that rainfall does not
                contribute to runoff. A transbasin diversion can also affect the total
                drainage area.
            country_code: The code for the country in which the monitoring location is located.
            country_name: The name of the country in which the monitoring location is located.
            county_code: The code for the county or county equivalent (parish, borough, etc.)
                in which the monitoring location is located. A list of codes is
                available at [https://api.waterdata.usgs.gov/ogcapi/v0/collections/cou
                nties/items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/coun
                ties/items).
            county_name: The name of the county or county equivalent (parish, borough, etc.) in
                which the monitoring location is located. [A list of codes is
                available at [https://api.waterdata.usgs.gov/ogcapi/v0/collections/cou
                nties/items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/coun
                ties/items).
            crs: Indicates the coordinate reference system for the results.
            depth_source_code: A code indicating the source of water-level data.
            district_code: The Water Science Centers (WSCs) across the United States use the FIPS
                state code as the district code. In some case, monitoring locations
                and samples may be managed by a water science center that is adjacent
                to the state in which the monitoring location actually resides. For
                example a monitoring location may have a district code of 30 which
                translates to Montana, but the state code could be 56 for Wyoming
                because that is where the monitoring location actually is located.
            drainage_area: The area enclosed by a topographic divide from which direct surface
                runoff from precipitation normally drains by gravity into the stream
                above that point.
            f: The optional f parameter indicates the output format which the server
                shall provide as part of the response document.  The default format is
                GeoJSON.
            hole_constructed_depth: The total depth to which the hole is drilled, in feet below land
                surface datum. Note: Not all groundwater monitoring locations have
                information on Hole Depth. Such monitoring locations will not be
                retrieved using this search criteria.
            horizontal_position_method_code: Indicates the method used to determine latitude longitude values. A
                list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                method-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collectio
                ns/coordinate-method-codes/items).
            horizontal_position_method_name: Indicates the method used to determine latitude longitude values. A
                list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                method-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collectio
                ns/coordinate-method-codes/items).
            horizontal_positional_accuracy: Indicates the accuracy of the latitude longitude values. A list of
                codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                accuracy-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collect
                ions/coordinate-accuracy-codes/items).
            horizontal_positional_accuracy_code: Indicates the accuracy of the latitude longitude values. A list of
                codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                accuracy-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collect
                ions/coordinate-accuracy-codes/items).
            hydrologic_unit_code: The United States is divided and sub-divided into successively smaller
                hydrologic units which are classified into four levels: regions, sub-
                regions, accounting units, and cataloging units. The hydrologic units
                are arranged within each other, from the smallest (cataloging units)
                to the largest (regions). Each hydrologic unit is identified by a
                unique hydrologic unit code (HUC) consisting of two to eight digits
                based on the four levels of classification in the hydrologic unit
                system.
                 Search will match partial HUCs.
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
                presented in the response document (maximum=50000, default=10).
            minor_civil_division_code: Codes for primary governmental or administrative divisions of the
                county or county equivalent in which the monitoring location is
                located.
            monitoring_location_name: This is the official name of the monitoring location in the database.
                For well information this can be a district-assigned local number.
            monitoring_location_number: Each monitoring location in the USGS data base has a unique 8- to
                15-digit identification number.
            national_aquifer_code: National aquifers are the principal aquifers or aquifer systems in the
                United States, defined as regionally extensive aquifers or aquifer
                systems that have the potential to be used as a source of potable
                water. Not all groundwater monitoring locations can be associated with
                a National Aquifer. Such monitoring locations will not be retrieved
                using this search criteria. A list of National aquifer codes and names
                is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/national-
                aquifer-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collecti
                ons/national-aquifer-codes/items).
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            original_horizontal_datum: Coordinates are published in EPSG:4326 / WGS84 / World Geodetic System
                1984. This field indicates the original datum used to determine
                coordinates before they were converted. A list of codes is available
                at [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                datum-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collection
                s/coordinate-datum-codes/items).
            original_horizontal_datum_name: Coordinates are published in EPSG:4326 / WGS84 / World Geodetic System
                1984. This field indicates the original datum used to determine
                coordinates before they were converted. A list of codes is available
                at [https://api.waterdata.usgs.gov/ogcapi/v0/collections/coordinate-
                datum-codes/items](https://api.waterdata.usgs.gov/ogcapi/v0/collection
                s/coordinate-datum-codes/items).
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            revision_created: 
            revision_modified: 
            revision_note: 
            site_type: A description of the hydrologic setting of the monitoring location. A
                list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/site-types/items
                ](https://api.waterdata.usgs.gov/ogcapi/v0/collections/site-
                types/items).
            site_type_code: A code describing the hydrologic setting of the monitoring location. A
                list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/site-types/items
                ](https://api.waterdata.usgs.gov/ogcapi/v0/collections/site-
                types/items).
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            state_code: State code. A [two-digit ANSI
                code](https://www2.census.gov/geo/docs/reference/state.txt) (formerly
                FIPS code) as defined by the American National Standards Institute, to
                define States and equivalents. A three-digit ANSI code is used to
                define counties and county equivalents. [A lookup table is
                available.](https://www.census.gov/library/reference/code-
                lists/ansi.html#states) The only countries with political subdivisions
                other than the US are Mexico and Canada. The Mexican states have US
                state codes ranging from 81-86 and Canadian provinces have state codes
                ranging from 90-98.
            state_name: The name of the state or state equivalent in which the monitoring
                location is located.
            time_zone_abbreviation: A short code describing the time zone used by a monitoring location.
            uses_daylight_savings: A flag indicating whether or not a monitoring location uses daylight
                savings.
            vertical_datum: The datum used to determine altitude and vertical position at the
                monitoring location. A list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-datums/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-
                datums/items).
            vertical_datum_name: The datum used to determine altitude and vertical position at the
                monitoring location. A list of codes is available at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-datums/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/altitude-
                datums/items).
            well_constructed_depth: The depth of the finished well, in feet below land surface datum.
                Note: Not all groundwater monitoring locations have information on
                Well Depth. Such monitoring locations will not be retrieved using this
                search criteria.
        """
        # Translate Python parameters to API parameters
        query = {
            "agency_code": agency_code,
            "agency_name": agency_name,
            "altitude": altitude,
            "altitude_accuracy": altitude_accuracy,
            "altitude_method_code": altitude_method_code,
            "altitude_method_name": altitude_method_name,
            "aquifer_code": aquifer_code,
            "aquifer_type_code": aquifer_type_code,
            "basin_code": basin_code,
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "construction_date": construction_date,
            "contributing_drainage_area": contributing_drainage_area,
            "country_code": country_code,
            "country_name": country_name,
            "county_code": county_code,
            "county_name": county_name,
            "crs": crs,
            "depth_source_code": depth_source_code,
            "district_code": district_code,
            "drainage_area": drainage_area,
            "f": f,
            "hole_constructed_depth": hole_constructed_depth,
            "horizontal_position_method_code": horizontal_position_method_code,
            "horizontal_position_method_name": horizontal_position_method_name,
            "horizontal_positional_accuracy": horizontal_positional_accuracy,
            "horizontal_positional_accuracy_code": horizontal_positional_accuracy_code,
            "hydrologic_unit_code": hydrologic_unit_code,
            "lang": lang,
            "limit": limit,
            "minor_civil_division_code": minor_civil_division_code,
            "monitoring_location_name": monitoring_location_name,
            "monitoring_location_number": monitoring_location_number,
            "national_aquifer_code": national_aquifer_code,
            "offset": offset,
            "original_horizontal_datum": original_horizontal_datum,
            "original_horizontal_datum_name": original_horizontal_datum_name,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "revision_created": revision_created,
            "revision_modified": revision_modified,
            "revision_note": revision_note,
            "site_type": site_type,
            "site_type_code": site_type_code,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "state_code": state_code,
            "state_name": state_name,
            "time_zone_abbreviation": time_zone_abbreviation,
            "uses_daylight_savings": uses_daylight_savings,
            "vertical_datum": vertical_datum,
            "vertical_datum_name": vertical_datum_name,
            "well_constructed_depth": well_constructed_depth,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class NationalAquiferCodesClient(BaseClient[TransformedResponse_co]):
    """
    National aquifers are the principal aquifers or aquifer systems in the
    United States, defined as regionally extensive aquifers or aquifer
    systems that have the potential to be used as a source of potable
    water.
    """
    _endpoint = USGSCollection.NATIONAL_AQUIFER_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        national_aquifer_name: Optional[str] = None,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "national_aquifer_name"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from national-aquifer-codes.

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
            national_aquifer_name: National aquifer name.
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
            query_id: National aquifer code.
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "national_aquifer_name": national_aquifer_name,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class ParameterCodesClient(BaseClient[TransformedResponse_co]):
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
        ) -> TransformedResponse_co | list[dict[str, Any]]:
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "epa_equivalence": epa_equivalence,
            "f": f,
            "lang": lang,
            "limit": limit,
            "medium": medium,
            "offset": offset,
            "parameter_description": parameter_description,
            "parameter_group_code": parameter_group_code,
            "parameter_name": parameter_name,
            "particle_size_basis": particle_size_basis,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "sample_fraction": sample_fraction,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "statistical_basis": statistical_basis,
            "temperature_basis": temperature_basis,
            "time_basis": time_basis,
            "unit_of_measure": unit_of_measure,
            "weight_basis": weight_basis,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class ReliabilityCodesClient(BaseClient[TransformedResponse_co]):
    """
    Code indicating the reliability of the data available for the site.
    """
    _endpoint = USGSCollection.RELIABILITY_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "reliability_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        reliability_description: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from reliability-codes.

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
            query_id: 
            reliability_description: 
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "reliability_description": reliability_description,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class SiteTypesClient(BaseClient[TransformedResponse_co]):
    """
    The hydrologic cycle setting or a man-made feature thought to affect
    the hydrologic conditions measured at a site. Primary and secondary
    site types associated with data collection sites. All sites have a
    primary site type, and may additionally have a secondary site type
    that further describes the location.
    """
    _endpoint = USGSCollection.SITE_TYPES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "site_type_primary_flag", "site_type_name", "site_type_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        site_type_description: Optional[str] = None,
        site_type_name: Optional[str] = None,
        site_type_primary_flag: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from site-types.

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
            query_id: An acronym specifying the primary or secondary site type.
            site_type_description: Site type description.
            site_type_name: A long name for the site type used in retrieved output.
            site_type_primary_flag: Identifies which site types are primary.
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "site_type_description": site_type_description,
            "site_type_name": site_type_name,
            "site_type_primary_flag": site_type_primary_flag,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class StatesClient(BaseClient[TransformedResponse_co]):
    """
    State name or territory. Includes U.S. states and foreign entities
    classified under FIPS as 'Principal Administrative Divisions'.
    """
    _endpoint = USGSCollection.STATES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        country_code: Optional[str] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "country_code", "state_fips_code", "state_name", "state_postal_code"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        state_fips_code: Optional[str] = None,
        state_name: Optional[str] = None,
        state_postal_code: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from states.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            country_code: FIPS country code as defined by FIPS PUB 10-4: Countries,
                Dependencies, Areas of Special Sovereignty, and Their Principal
                Administrative Divisions.
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
            query_id: 
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
            state_fips_code: State FIPS code.
            state_name: State name.
            state_postal_code: State postal abbreviation. A two-letter USPS state postal
                abbreviation.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "country_code": country_code,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "state_fips_code": state_fips_code,
            "state_name": state_name,
            "state_postal_code": state_postal_code,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class StatisticCodesClient(BaseClient[TransformedResponse_co]):
    """
    Statistic codes.
    """
    _endpoint = USGSCollection.STATISTIC_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "statistic_name", "statistic_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        statistic_description: Optional[str] = None,
        statistic_name: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from statistic-codes.

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
            query_id: Statistic code.
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
            statistic_description: Statistic description.
            statistic_name: Statistic name.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "statistic_description": statistic_description,
            "statistic_name": statistic_name,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class TimeSeriesMetadataClient(BaseClient[TransformedResponse_co]):
    """
    Daily data and continuous measurements are grouped into time series,
    which represent a collection of observations of a single parameter,
    potentially aggregated using a standard statistic, at a single
    monitoring location. This endpoint provides metadata about those time
    series, including their operational thresholds, units of measurement,
    and when the earliest and most recent observations in a time series
    occurred.
    """
    _endpoint = USGSCollection.TIME_SERIES_METADATA

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        begin: Optional[str] = None,
        begin_utc: Optional[str] = None,
        computation_identifier: Optional[str] = None,
        computation_period_identifier: Optional[str] = None,
        crs: Optional[URL] = None,
        end: Optional[str] = None,
        end_utc: Optional[str] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        hydrologic_unit_code: Optional[str] = None,
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        monitoring_location_id: Optional[str] = None,
        offset: Optional[int] = 0,
        parameter_code: Optional[str] = None,
        parameter_description: Optional[str] = None,
        parameter_name: Optional[str] = None,
        parent_time_series_id: Optional[str] = None,
        primary: Optional[str] = None,
        properties: Optional[Sequence[Literal["id", "unit_of_measure", "parameter_name", "parameter_code", "statistic_id", "hydrologic_unit_code", "state_name", "last_modified", "begin", "end", "begin_utc", "end_utc", "computation_period_identifier", "computation_identifier", "thresholds", "sublocation_identifier", "primary", "monitoring_location_id", "web_description", "parameter_description", "parent_time_series_id"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        state_name: Optional[str] = None,
        statistic_id: Optional[str] = None,
        sublocation_identifier: Optional[str] = None,
        thresholds: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        web_description: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from time-series-metadata.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            begin: This field contains the same information as "begin_utc", but in the
                local time of the monitoring location. It is retained for backwards
                compatibility, but will be removed in V1 of these APIs.
            begin_utc: The datetime of the earliest observation in the time series. Together
                with `end`, this field represents the period of record of a time
                series. Note that some time series may have large gaps in their
                collection record.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `begin` that intersects the value of
                datetime are selected.
            computation_identifier: Indicates whether the data from this time series represent a specific
                statistical computation. Split parameters are enabled for this field,
                so you can supply multiple values separated by commas.
            computation_period_identifier: Indicates the period of data used for any statistical computations.
                Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            crs: Indicates the coordinate reference system for the results.
            end: This field contains the same information as "end_utc", but in the
                local time of the monitoring location. It is retained for backwards
                compatibility, but will be removed in V1 of these APIs.
            end_utc: The datetime of the most recent observation in the time series. Data
                returned by this endpoint updates at most once per day, and
                potentially less frequently than that, and as such there may be more
                recent observations within a time series than the time series `end`
                value reflects. Together with `begin`, this field represents the
                period of record of a time series. It is additionally used to
                determine whether a time series is "active".
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `end` that intersects the value of datetime
                are selected.
            f: The optional f parameter indicates the output format which the server
                shall provide as part of the response document.  The default format is
                GeoJSON.
            hydrologic_unit_code: The United States is divided and sub-divided into successively smaller
                hydrologic units which are classified into four levels: regions, sub-
                regions, accounting units, and cataloging units. The hydrologic units
                are arranged within each other, from the smallest (cataloging units)
                to the largest (regions). Each hydrologic unit is identified by a
                unique hydrologic unit code (HUC) consisting of two to eight digits
                based on the four levels of classification in the hydrologic unit
                system.
                 Search will match partial HUCs.
            lang: The optional lang parameter instructs the server return a response in
                a certain language, if supported.  If the language is not among the
                available values, the Accept-Language header language will be used if
                it is supported. If the header is missing, the default server language
                is used. Note that providers may only support a single language (or
                often no language at all), that can be different from the server
                language.  Language strings can be written in a complex (e.g. "fr-
                CA,fr;q=0.9,en-US;q=0.8,en;q=0.7"), simple (e.g. "de") or locale-like
                (e.g. "de-CH" or "fr_BE") fashion.
            last_modified: The last time a record was refreshed in our database. This may happen
                due to regular operational processes and does not necessarily indicate
                anything about the measurement has changed.
                You can query this field using date-times or intervals, adhering to
                RFC 3339, or using ISO 8601 duration objects. Intervals may be bounded
                or half-bounded (double-dots at start or end).
                Examples:

                  - A date-time: "2018-02-12T23:20:50Z"
                  - A bounded interval: "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
                  - Half-bounded intervals: "2018-02-12T00:00:00Z/.." or
                "../2018-03-18T12:31:12Z"
                  - Duration objects: "P1M" for data from the past month or "PT36H"
                for the last 36 hours

                Only features that have a `last_modified` that intersects the value of
                datetime are selected.
            limit: The optional limit parameter limits the number of items that are
                presented in the response document (maximum=50000, default=10).
            monitoring_location_id: A unique identifier representing a single monitoring location. This
                corresponds to the `id` field in the `monitoring-locations` endpoint.
                Monitoring location IDs are created by combining the agency code of
                the agency responsible for the monitoring location (e.g. USGS) with
                the ID number of the monitoring location (e.g. 02238500), separated by
                a hyphen (e.g. USGS-02238500).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            offset: The optional offset parameter indicates the index within the result
                set from which the server shall begin presenting results in the
                response document.  The first element has an index of 0 (default).
            parameter_code: Parameter codes are 5-digit codes used to identify the constituent
                measured and the units of measure. A complete list of parameter codes
                and associated groupings can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            parameter_description: A description of what the parameter code represents, as used by WDFN
                and other USGS data dissemination products.
            parameter_name: A human-understandable name corresponding to `parameter_code`.
            parent_time_series_id: The unique identifier representing the parent or "upchain" time series
                that a daily values time series is generated from. Daily values time
                series have one and only one parent time series.
            primary: A flag identifying if the time series is a "primary" time series.
                "Primary" time series (which have this flag) are standard observations
                which undergo [Bureau review and approval
                processes](https://www.usgs.gov/survey-manual/5028-fundamental-
                science-practices-review-and-approval-scientific-data-release). Non-
                primary time series, which will have missing values for "primary", are
                provisional datasets made available to meet the need for timely best
                science and to assist with daily operations which need real-time
                information. Non-primary time series data are only retained by this
                system for 120 days. See the [USGS Provisional Data
                Statement](https://waterdata.usgs.gov/provisional-data-statement/) for
                more information.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: A unique identifier representing a single time series. This
                corresponds to the `id` field in the `time-series-metadata` endpoint.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            skipgeometry: This option can be used to skip response geometries for each feature.
            sortby: Specifies a comma-separated list of property names by which the
                response shall be sorted.  If the property name is preceded by a plus
                (+) sign it indicates an ascending sort for that property.  If the
                property name is preceded by a minus (-) sign it indicates a
                descending sort for that property.  If the property is not preceded by
                a plus or minus, then the default sort order implied is ascending (+).

                Only a single page of data can be returned when specifying sortby. If
                you need more than a single page of data, don't specify a sortby value
                and sort the full data set after it's been downloaded.
            state_name: The name of the state or state equivalent in which the monitoring
                location is located.
            statistic_id: A code corresponding to the statistic an observation represents.
                Example codes include 00001 (max), 00002 (min), and 00003 (mean). A
                complete list of codes and their descriptions can be found at
                [https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-codes/
                items](https://api.waterdata.usgs.gov/ogcapi/v0/collections/statistic-
                codes/items).
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            sublocation_identifier: An optional human-readable identifier used to specify where
                measurements are recorded at a monitoring location.
            thresholds: Thresholds represent known numeric limits for a time series, for
                example the historic maximum value for a parameter or a level below
                which a sensor is non-operative. These thresholds are sometimes used
                to automatically determine if an observation is erroneous due to
                sensor error, and therefore shouldn't be included in the time series.
            unit_of_measure: A human-readable description of the units of measurement associated
                with an observation.
            web_description: A description of what this time series represents, as used by WDFN and
                other USGS data dissemination products.
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "begin": begin,
            "begin_utc": begin_utc,
            "computation_identifier": computation_identifier,
            "computation_period_identifier": computation_period_identifier,
            "crs": crs,
            "end": end,
            "end_utc": end_utc,
            "f": f,
            "hydrologic_unit_code": hydrologic_unit_code,
            "lang": lang,
            "last_modified": last_modified,
            "limit": limit,
            "monitoring_location_id": monitoring_location_id,
            "offset": offset,
            "parameter_code": parameter_code,
            "parameter_description": parameter_description,
            "parameter_name": parameter_name,
            "parent_time_series_id": parent_time_series_id,
            "primary": primary,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "state_name": state_name,
            "statistic_id": statistic_id,
            "sublocation_identifier": sublocation_identifier,
            "thresholds": thresholds,
            "unit_of_measure": unit_of_measure,
            "web_description": web_description,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class TimeZoneCodesClient(BaseClient[TransformedResponse_co]):
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
        ) -> TransformedResponse_co | list[dict[str, Any]]:
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
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "time_zone_daylight_savings_time_code": time_zone_daylight_savings_time_code,
            "time_zone_daylight_savings_time_name": time_zone_daylight_savings_time_name,
            "time_zone_daylight_savings_utc_offset": time_zone_daylight_savings_utc_offset,
            "time_zone_description": time_zone_description,
            "time_zone_name": time_zone_name,
            "time_zone_utc_offset": time_zone_utc_offset,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)

class TopographicCodesClient(BaseClient[TransformedResponse_co]):
    """
    The code that best describes the topographic setting in which the site
    is located. Topographic setting refers to the geomorphic features in
    the vicinity of the site.
    """
    _endpoint = USGSCollection.TOPOGRAPHIC_CODES

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        full_topography_description: Optional[str] = None,
        lang: Optional[Literal["en-US"]] = "en-US",
        limit: Optional[int] = 10000,
        offset: Optional[int] = 0,
        properties: Optional[Sequence[Literal["id", "topography_name", "short_topography_description", "full_topography_description"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        short_topography_description: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        topography_name: Optional[str] = None,
        ) -> TransformedResponse_co | list[dict[str, Any]]:
        """Retrieve items from topographic-codes.

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
            full_topography_description: 
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
            query_id: 
            short_topography_description: 
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
            topography_name: 
        """
        # Translate Python parameters to API parameters
        query = {
            "bbox": bbox,
            "bbox-crs": bbox_crs,
            "crs": crs,
            "f": f,
            "full_topography_description": full_topography_description,
            "lang": lang,
            "limit": limit,
            "offset": offset,
            "properties": properties,
            "filter": query_filter,
            "id": query_id,
            "short_topography_description": short_topography_description,
            "skipGeometry": skipgeometry,
            "sortby": sortby,
            "topography_name": topography_name,
        }

        # Ignore None
        valid_query = {k: v for k, v in query.items() if v is not None}

        # Get responses
        data = self._get_json_responses(queries=[valid_query])

        # Transform
        return self._handle_response(data)


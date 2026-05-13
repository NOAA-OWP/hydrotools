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

class ChannelMeasurementsClient(BaseClient[TransformedResponseT_co]):
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
        ) -> TransformedResponseT_co:
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
        # Validate query
        query = rm.ChannelMeasurementsRequest(
            bbox=bbox,
            bbox_crs=bbox_crs,
            channel_area=channel_area,
            channel_area_unit=channel_area_unit,
            channel_evenness=channel_evenness,
            channel_flow=channel_flow,
            channel_flow_unit=channel_flow_unit,
            channel_location_direction=channel_location_direction,
            channel_location_distance=channel_location_distance,
            channel_location_distance_unit=channel_location_distance_unit,
            channel_material=channel_material,
            channel_measurement_type=channel_measurement_type,
            channel_name=channel_name,
            channel_stability=channel_stability,
            channel_velocity=channel_velocity,
            channel_velocity_unit=channel_velocity_unit,
            channel_width=channel_width,
            channel_width_unit=channel_width_unit,
            crs=crs,
            datetime=datetime,
            f=f,
            field_visit_id=field_visit_id,
            horizontal_velocity_description=horizontal_velocity_description,
            lang=lang,
            last_modified=last_modified,
            limit=limit,
            longitudinal_velocity_description=longitudinal_velocity_description,
            measurement_number=measurement_number,
            measurement_type=measurement_type,
            monitoring_location_id=monitoring_location_id,
            offset=offset,
            properties=properties,
            query_filter=query_filter,
            query_id=query_id,
            skipgeometry=skipgeometry,
            sortby=sortby,
            time=time,
            vertical_velocity_description=vertical_velocity_description,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

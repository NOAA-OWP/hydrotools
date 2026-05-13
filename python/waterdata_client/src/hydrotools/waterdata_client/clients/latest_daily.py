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
from ..request_models.latest_daily import LatestDailyRequest

class LatestDailyClient(BaseClient[TransformedResponseT_co]):
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
        ) -> TransformedResponseT_co:
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
        # Validate query
        query = LatestDailyRequest(
            approval_status=approval_status,
            bbox=bbox,
            bbox_crs=bbox_crs,
            crs=crs,
            datetime=datetime,
            f=f,
            lang=lang,
            last_modified=last_modified,
            limit=limit,
            monitoring_location_id=monitoring_location_id,
            offset=offset,
            parameter_code=parameter_code,
            properties=properties,
            qualifier=qualifier,
            query_filter=query_filter,
            query_id=query_id,
            skipgeometry=skipgeometry,
            sortby=sortby,
            statistic_id=statistic_id,
            time=time,
            time_series_id=time_series_id,
            unit_of_measure=unit_of_measure,
            value=value,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

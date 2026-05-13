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
from ..request_models.time_series_metadata import TimeSeriesMetadataRequest

class TimeSeriesMetadataClient(BaseClient[TransformedResponseT_co]):
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
        ) -> TransformedResponseT_co:
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
                with `end_utc`, this field represents the period of record of a time
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

                Only features that have a `begin_utc` that intersects the value of
                datetime are selected.
            computation_identifier: Indicates the computation performed to calculate this time series.
                Values of "Instantaneous" reflect point measurements. Split parameters
                are enabled for this field, so you can supply multiple values
                separated by commas.
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
                recent observations within a time series than the time series
                `end_utc` value reflects. Together with `begin_utc`, this field
                represents the period of record of a time series. It is additionally
                used to determine whether a time series is "active".
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

                Only features that have a `end_utc` that intersects the value of
                datetime are selected.
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
                corresponds to the "time_series_id" field in other endpoints. Split
                parameters are enabled for this field, so you can supply multiple
                values separated by commas.
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
            web_description: An optional description of the time series. WDFN and other USGS data
                dissemination products use this field, in combination with
                sublocation_identifier, to distinguish the differences between
                multiple time series for the same parameter code, statistic code, and
                monitoring location.
        """
        # Validate query
        query = TimeSeriesMetadataRequest(
            bbox=bbox,
            bbox_crs=bbox_crs,
            begin=begin,
            begin_utc=begin_utc,
            computation_identifier=computation_identifier,
            computation_period_identifier=computation_period_identifier,
            crs=crs,
            end=end,
            end_utc=end_utc,
            f=f,
            hydrologic_unit_code=hydrologic_unit_code,
            lang=lang,
            last_modified=last_modified,
            limit=limit,
            monitoring_location_id=monitoring_location_id,
            offset=offset,
            parameter_code=parameter_code,
            parameter_description=parameter_description,
            parameter_name=parameter_name,
            parent_time_series_id=parent_time_series_id,
            primary=primary,
            properties=properties,
            query_filter=query_filter,
            query_id=query_id,
            skipgeometry=skipgeometry,
            sortby=sortby,
            state_name=state_name,
            statistic_id=statistic_id,
            sublocation_identifier=sublocation_identifier,
            thresholds=thresholds,
            unit_of_measure=unit_of_measure,
            web_description=web_description,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

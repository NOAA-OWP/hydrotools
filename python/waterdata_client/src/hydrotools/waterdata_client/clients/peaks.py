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

class PeaksClient(BaseClient[TransformedResponseT_co]):
    """
    Annual peak flow values are the maximum instantaneous streamflow
    values recorded at a particular site for the entire water year from
    October 1 to September 30. Note that the annual peak flow value may
    not occur at the same time the maximum water level occurs due to
    conditions such as backwater, tidal fluctuations, etc.
    """
    _endpoint = USGSCollection.PEAKS

    def get(
        self,
        bbox: Optional[Sequence[float]] = None,
        bbox_crs: Optional[URL] = None,
        crs: Optional[URL] = None,
        day: Optional[int] = None,
        f: Optional[Literal["json", "html", "jsonld", "csv"]] = "json",
        lang: Optional[Literal["en-US"]] = "en-US",
        last_modified: Optional[str] = None,
        limit: Optional[int] = 10,
        monitoring_location_id: Optional[str] = None,
        month: Optional[int] = None,
        offset: Optional[int] = 0,
        parameter_code: Optional[str] = None,
        peak_since: Optional[int] = None,
        properties: Optional[Sequence[Literal["time_series_id", "monitoring_location_id", "parameter_code", "id", "unit_of_measure", "value", "last_modified", "time", "water_year", "year", "month", "day", "time_of_day", "peak_since"]]] = None,
        query_filter: Optional[str] = None,
        query_id: Optional[str] = None,
        skipgeometry: Optional[bool] = False,
        sortby: Optional[Sequence[str]] = None,
        time: Optional[str] = None,
        time_of_day: Optional[str] = None,
        time_series_id: Optional[str] = None,
        unit_of_measure: Optional[str] = None,
        value: Optional[str] = None,
        water_year: Optional[int] = None,
        year: Optional[int] = None,
        ) -> TransformedResponseT_co:
        """Retrieve items from peaks.

        Args:
            bbox: Only features that have a geometry that intersects the bounding box
                are selected.The bounding box is provided as four or six numbers,
                depending on whether the coordinate reference system includes a
                vertical axis (height or depth).
            bbox_crs: Indicates the coordinate reference system for the given bbox
                coordinates.
            crs: Indicates the coordinate reference system for the results.
            day: The day of the month a peak occurred. If null, the day a peak occurred
                is unknown.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
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
            month: The calendar month a peak occurred. If null, the month a peak occurred
                is unknown.
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
            peak_since: If not null, this record represents the peak value for the parameter
                code since the year contained in "peak_since".
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            properties: The properties that should be included. The parameter value is a
                comma-separated list of property names.
            query_filter: CQL Text filter expression.  CQL JSON cannot be used here, only in the
                body.
                See also: https://docs.pygeoapi.io/en/latest/cql.html

                Example: time_series_id IN ('64ee32f5350a4ec4967435dcd2e364ea',
                '3e55d9c2d8a54bec9ca5e292b07d5a96')
            query_id: Split parameters are enabled for this field, so you can supply
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
            time_of_day: The time of day a peak occurred. If null, the time of day a peak
                occurred is unknown.
            time_series_id: A unique identifier representing a single time series. This
                corresponds to the `id` field in the `time-series-metadata` endpoint.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            unit_of_measure: A human-readable description of the units of measurement associated
                with an observation.
            value: The value of the observation. Values are transmitted as strings in the
                JSON response format in order to preserve precision.
            water_year: The water year (running from October 1st to September 30th) a peak
                occurred.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
            year: The calendar year a peak occurred.
                 Split parameters are enabled for this field, so you can supply
                multiple values separated by commas.
        """
        # Validate query
        query = rm.PeaksRequest(
            bbox=bbox,
            bbox_crs=bbox_crs,
            crs=crs,
            day=day,
            f=f,
            lang=lang,
            last_modified=last_modified,
            limit=limit,
            monitoring_location_id=monitoring_location_id,
            month=month,
            offset=offset,
            parameter_code=parameter_code,
            peak_since=peak_since,
            properties=properties,
            query_filter=query_filter,
            query_id=query_id,
            skipgeometry=skipgeometry,
            sortby=sortby,
            time=time,
            time_of_day=time_of_day,
            time_series_id=time_series_id,
            unit_of_measure=unit_of_measure,
            value=value,
            water_year=water_year,
            year=year,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

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
from ..request_models.field_measurements import FieldMeasurementsRequest

class FieldMeasurementsClient(BaseClient[TransformedResponseT_co]):
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
        ) -> TransformedResponseT_co:
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
            control_condition: The state of the control feature at the time of observation.
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
                corresponds to the `id` field in the `field-measurements-metadata`
                endpoint. Collection series are defined as the set of field
                measurements at a given monitoring location for a single parameter
                code using a single reading type.
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
            measurement_rated: A qualitative estimate of the quality of a measurement.
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
                will be generated. There may be multiple readings occurring at
                identical times during a single field visit; to uniquely identify a
                set of readings over time, use the `field_visit_id` field.
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
        # Validate query
        query = FieldMeasurementsRequest(
            approval_status=approval_status,
            bbox=bbox,
            bbox_crs=bbox_crs,
            control_condition=control_condition,
            crs=crs,
            datetime=datetime,
            f=f,
            field_measurements_series_id=field_measurements_series_id,
            field_visit_id=field_visit_id,
            lang=lang,
            last_modified=last_modified,
            limit=limit,
            measurement_rated=measurement_rated,
            measuring_agency=measuring_agency,
            monitoring_location_id=monitoring_location_id,
            observing_procedure=observing_procedure,
            observing_procedure_code=observing_procedure_code,
            offset=offset,
            parameter_code=parameter_code,
            properties=properties,
            qualifier=qualifier,
            query_filter=query_filter,
            query_id=query_id,
            skipgeometry=skipgeometry,
            sortby=sortby,
            time=time,
            unit_of_measure=unit_of_measure,
            value=value,
            vertical_datum=vertical_datum,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

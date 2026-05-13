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

class CombinedMetadataClient(BaseClient[TransformedResponseT_co]):
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
        ) -> TransformedResponseT_co:
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
                location. Split parameters are enabled for this field, so you can
                supply multiple values separated by commas.
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
            web_description: An optional description of the time series. WDFN and other USGS data
                dissemination products use this field, in combination with
                sublocation_identifier, to distinguish the differences between
                multiple time series for the same parameter code, statistic code, and
                monitoring location.
            well_constructed_depth: The depth of the finished well, in feet below land surface datum.
                Note: Not all groundwater monitoring locations have information on
                Well Depth. Such monitoring locations will not be retrieved using this
                search criteria.
        """
        # Validate query
        query = rm.CombinedMetadataRequest(
            agency_code=agency_code,
            agency_name=agency_name,
            altitude=altitude,
            altitude_accuracy=altitude_accuracy,
            altitude_method_code=altitude_method_code,
            altitude_method_name=altitude_method_name,
            aquifer_code=aquifer_code,
            aquifer_type_code=aquifer_type_code,
            basin_code=basin_code,
            bbox=bbox,
            bbox_crs=bbox_crs,
            begin=begin,
            computation_identifier=computation_identifier,
            construction_date=construction_date,
            contributing_drainage_area=contributing_drainage_area,
            country_code=country_code,
            country_name=country_name,
            county_code=county_code,
            county_name=county_name,
            crs=crs,
            data_type=data_type,
            depth_source_code=depth_source_code,
            district_code=district_code,
            drainage_area=drainage_area,
            end=end,
            f=f,
            hole_constructed_depth=hole_constructed_depth,
            horizontal_position_method_code=horizontal_position_method_code,
            horizontal_position_method_name=horizontal_position_method_name,
            horizontal_positional_accuracy=horizontal_positional_accuracy,
            horizontal_positional_accuracy_code=horizontal_positional_accuracy_code,
            hydrologic_unit_code=hydrologic_unit_code,
            lang=lang,
            last_modified=last_modified,
            limit=limit,
            minor_civil_division_code=minor_civil_division_code,
            monitoring_location_id=monitoring_location_id,
            monitoring_location_name=monitoring_location_name,
            monitoring_location_number=monitoring_location_number,
            national_aquifer_code=national_aquifer_code,
            offset=offset,
            original_horizontal_datum=original_horizontal_datum,
            original_horizontal_datum_name=original_horizontal_datum_name,
            parameter_code=parameter_code,
            parameter_description=parameter_description,
            parameter_name=parameter_name,
            parent_time_series_id=parent_time_series_id,
            primary=primary,
            properties=properties,
            query_filter=query_filter,
            query_id=query_id,
            site_type=site_type,
            site_type_code=site_type_code,
            skipgeometry=skipgeometry,
            sortby=sortby,
            state_code=state_code,
            state_name=state_name,
            statistic_id=statistic_id,
            sublocation_identifier=sublocation_identifier,
            thresholds=thresholds,
            time_zone_abbreviation=time_zone_abbreviation,
            unit_of_measure=unit_of_measure,
            uses_daylight_savings=uses_daylight_savings,
            vertical_datum=vertical_datum,
            vertical_datum_name=vertical_datum_name,
            web_description=web_description,
            well_constructed_depth=well_constructed_depth,
        ).generate_query()

        # Get responses
        data = self._get_json_responses(queries=[query])

        # Transform
        return self._handle_response(data)

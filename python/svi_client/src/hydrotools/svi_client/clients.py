from http import HTTPStatus
from hydrotools._restclient import RestClient
import geopandas as gpd

# local imports
from . import url_builders
from .types import GeographicScale, Year, utilities, field_name_map


class SVIClient:
    def __init__(self, enable_cache: bool = True) -> None:
        self._rest_client = RestClient(
            cache_filename="svi_client_cache",
            enable_cache=enable_cache,
        )

    def get(
        self, location: str, geographic_scale: GeographicScale, year: Year
    ) -> gpd.GeoDataFrame:
        """[summary]

        Parameters
        ----------
        location : str
            state / national name or abbreviation (e.g. "AL", "US", "Wyoming", "new york")
        geographic_scale : GeographicScale "census_tract" or "county"
            "county" scale data *not* available in 2000 or 2010
        year : Year
            2000, 2010, 2014, 2016, or 2018

        Returns
        -------
        pd.DataFrame
            Dataframe of Social Vulnerability Index values at the census tract or county scale

        Examples
        --------
        >>> client = SVIClient()
        ... df = client.get("AL", "census_tract", "2018")
                    ST    STATE ST_ABBR  STCNTY  ... M_UNINSUR  EP_UNINSUR MP_UNINSUR  E_DAYPOP
        0      1  ALABAMA      AL    1015  ...        12      -999.0     -999.0       656
        1      1  ALABAMA      AL    1015  ...        12      -999.0     -999.0       146
        ...   ..      ...     ...     ...  ...       ...         ...        ...       ...
        1178   1  ALABAMA      AL    1015  ...       129        10.0        4.0      1832
        1179   1  ALABAMA      AL    1069  ...        98        17.7        4.4      2566

        """
        url_path = url_builders.build_feature_server_url(
            location=location, geographic_scale=geographic_scale, year=year
        )

        request = self._rest_client.get(url_path)

        if request.status != HTTPStatus.OK:  # 200
            ...

        # create geodataframe from geojson response
        df = gpd.GeoDataFrame.from_features(request.json())  # type: ignore

        fnm = field_name_map.CdcEsriFieldNameMapFactory(geographic_scale, year)

        # map of dataset field names to canonical field names
        field_names = {
            v: k
            for k, v in fnm.dict(exclude_unset=True, exclude={"svi_edition"}).items()
        }

        df = df.rename(columns=field_names)

        # create missing fields if required
        df = fnm.create_missing_fields(df)

        df["svi_edition"] = fnm.svi_edition

        # wide to long format
        rank_col_names = df.columns.str.contains("rank$")

        df = df.melt(
            id_vars=df.columns[~rank_col_names],
            value_vars=df.columns[rank_col_names],
            var_name="rank_theme",
            value_name="rank",
        )

        value_col_names = df.columns.str.contains("value$")
        # some datasources do not include summed theme values
        if not (value_col_names == False).all():
            df = df.melt(
                id_vars=df.columns[~value_col_names],
                value_vars=df.columns[value_col_names],
                var_name="value_theme",
                value_name="value",
            )
        # create theme column by truncating rank_theme's _rank suffix
        df["theme"] = df["rank_theme"].str.rstrip("_rank")

        # drop unnecessary cols
        # value_theme column might not exist, so ignore errors when trying to drop
        df = df.drop(columns=["rank_theme", "value_theme"], errors="ignore")

        output_column_order = [
            "state_name",
            "state_abbreviation",
            "county_name",
            "state_fips",
            "county_fips",
            "fips",
            "theme",
            "rank",
            "value",
            "svi_edition",
            "geometry",
        ]

        # reorder dataframe columns
        # note, during reindex, if there are columns not present in dataframe, they will be created
        # with NaN row values
        df = df.reindex(columns=output_column_order)

        return df

    @staticmethod
    def svi_documentation_url(year: Year) -> str:
        year = utilities.validate_year(year)

        urls = {
            "2000": "https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI2000Documentation-H.pdf",
            "2010": "https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI-2010-Documentation-H.pdf",
            "2014": "https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI2014Documentation_01192022.pdf",
            "2016": "https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI2016Documentation_01192022.pdf",
            "2018": "https://www.atsdr.cdc.gov/placeandhealth/svi/documentation/pdf/SVI2018Documentation_01192022_1.pdf",
        }

        url = urls.get(year, None)

        # raise error if valid year not in urls.
        # when new svi releases are added, this will purposefully break.
        if url is None:
            # raise error
            error_message = (
                f"documentation for year: {year} has not been added to SVIClient."
            )
            raise ValueError(error_message)

        return url

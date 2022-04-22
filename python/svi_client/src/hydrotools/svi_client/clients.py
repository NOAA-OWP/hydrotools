from hydrotools._restclient import RestClient
import geopandas as gpd

# local imports
from . import url_builders
from .types import GeographicScale, GeographicContext, Year, utilities, field_name_map

# typing imports
from typing import Union
from pathlib import Path


class SVIClient:
    def __init__(
        self,
        enable_cache: bool = True,
        cache_filename: Union[str, Path] = "svi_client_cache",
    ) -> None:
        self._rest_client = RestClient(
            cache_filename=cache_filename,
            enable_cache=enable_cache,
        )

    def get(
        self,
        location: str,
        geographic_scale: GeographicScale,
        year: Year,
        geographic_context: GeographicContext = "national",
    ) -> gpd.GeoDataFrame:
        """Retrieve social vulnerability index thematic rankings and values for a given state or the
        U.S..

        SVI values are available for the following years: 2000, 2010, 2014, 2016, and 2018.  The CDC
        calculates the SVI at the census tract or county geographic scale. Likewise, the CDC
        calculates SVI rankings in two geographic contexts: (1) relative to a given state's SVI
        values or (2) relative to the U.S.. (1) permits interastate comparison and (2) permits
        national comparison.

        Note: `state` geographic_context is not supported at this time.

        Parameters
        ----------
        location : str
            state / national name or abbreviation (e.g. "AL", "US", "Wyoming", "new york")
        geographic_scale : GeographicScale "census_tract" or "county"
            geographic scale at which theme values were calculated
        year : Year
            2000, 2010, 2014, 2016, or 2018
        geographic_context : GeographicContext "national" or "state", optional
            svi rankings calculated at the national or state level. use state for intrastate comparisons, by default "national"
            Note: `state` not supported at this time. will raise NotImplimented Error

        Returns
        -------
        pd.DataFrame
            Dataframe of Social Vulnerability Index values at the census tract or county scale

            columns names:
                state_name: str
                state_abbreviation: str
                county_name: str
                state_fips: str
                county_fips: str
                fips: str
                theme: str
                rank: float
                value: float
                svi_edition: str
                geometry: gpd.array.GeometryDtype


        Examples
        --------
        >>> client = SVIClient()
        ... df = client.get("AL", "census_tract", "2018")
                    state_name state_abbreviation  ... svi_edition                                           geometry
        0        ALABAMA                 AL  ...        2018  POLYGON ((-87.21230 32.83583, -87.20970 32.835...
        1        ALABAMA                 AL  ...        2018  POLYGON ((-86.45640 31.65556, -86.44864 31.655...
        ...          ...                ...  ...         ...                                                ...
        29498    ALABAMA                 AL  ...        2018  POLYGON ((-85.99487 31.84424, -85.99381 31.844...
        29499    ALABAMA                 AL  ...        2018  POLYGON ((-86.19941 31.80787, -86.19809 31.808...

        """
        url_path = url_builders.build_feature_server_url(
            location=location,
            geographic_scale=geographic_scale,
            year=year,
            geographic_context=geographic_context,
        )

        # RestClient only allows 200 response code or an aiohttp.client_exceptions.ClientConnectorError is raised
        request = self._rest_client.get(url_path)

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

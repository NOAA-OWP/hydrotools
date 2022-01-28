import io
from http import HTTPStatus
from hydrotools._restclient import RestClient
import pandas as pd

# local imports
from . import url_builders
from .types import GeographicScale, Year, utilities


class SVIClient:
    _base_url = "https://svi.cdc.gov/"

    def __init__(self) -> None:
        self._rest_client = RestClient(
            base_url=self._base_url, cache_filename="svi_client_cache"
        )

    def get(
        self, location: str, geographic_scale: GeographicScale, year: Year
    ) -> pd.DataFrame:
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

        url_path = url_builders.build_csv_url(
            location=location, geographic_scale=geographic_scale, year=year
        )

        request = self._rest_client.get(url_path)

        if request.status != HTTPStatus.OK:  # 200
            ...

        serialized_text = io.StringIO(request.text())

        return pd.read_csv(serialized_text)

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

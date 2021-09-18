from nwm_client.NWMClient import NWMFileClient
from nwm_client.NWMFileCatalog import HTTPFileCatalog

if __name__ == "__main__":
    # Setup catalog
    catalog = HTTPFileCatalog(
        server="https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"
    )

    # Setup client
    client = NWMFileClient(catalog=catalog)

    # Retrieve data
    df = client.get(
        configuration="analysis_assim",
        reference_times=["20210918T00Z"],
        compute=False
        )

    # Look at data
    print(df)

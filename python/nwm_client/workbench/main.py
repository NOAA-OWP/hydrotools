from nwm_client.NWMClient import NWMFileClient
from nwm_client.NWMFileCatalog import HTTPFileCatalog

def main():
    # Setup client with default catalog (GCP)
    client = NWMFileClient()

    # # Use HTTP catalog (local)
    # catalog = HTTPFileCatalog(
    #     server="http://0.0.0.0:8000/"
    #     )
    # client = NWMFileClient(catalog=catalog)

    # # Get options
    # configuration = "short_range"
    # reference_time = "20210819T00Z"

    # # Use HTTP catalog
    # catalog = HTTPFileCatalog(
    #     server="https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/",
    #     verify=None
    #     )
    # client = NWMFileClient(catalog=catalog, verify=None)

    # Get options
    configuration = "analysis_assim"
    reference_time = "20210914T10Z"

    # Retrieve data
    df = client.get(
        configuration=configuration,
        reference_time=reference_time
    )

    # Find maximum flows
    df_sub = df[["feature_id", "streamflow"]]
    df_max = df_sub.groupby("feature_id").max()
    df_max = df_max[df_max > 0.0].dropna()
    print(df_max.compute())

if __name__ == "__main__":
    main()

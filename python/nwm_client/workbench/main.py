from nwm_client.NWMClient import NWMFileClient

if __name__ == "__main__":
    client = NWMFileClient()

    df = client.get(
        configuration="medium_range_mem1",
        reference_times=["20210917T00Z"],
        compute=False
        )

    print(df)

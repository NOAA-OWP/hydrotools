from nwm_client.FileDownloader import FileDownloader
from nwm_client.NWMFileProcessor import NWMFileProcessor
from nwm_client.NWMFileCatalog import HTTPFileCatalog

import tempfile

def main():
    verify = None
    # Get list of files
    catalog = HTTPFileCatalog(
        server="https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/",
        # verify=verify
        )
    urls = catalog.list_blobs(
        configuration="analysis_assim",
        reference_time="20210910T00Z"
    )

    # Download and process files
    with tempfile.TemporaryDirectory() as dir:
        # Download files
        downloader = FileDownloader(output_directory=dir,
        # verify=verify
        )
        downloader.get(urls)

        # Process files
        df = NWMFileProcessor.get_dataframe(dir)

    print(df.info(memory_usage="deep"))
    print(df)

if __name__ == "__main__":
    main()

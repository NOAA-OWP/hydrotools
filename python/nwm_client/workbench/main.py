from nwm_client.FileDownloader import FileDownloader
from nwm_client.NWMFileProcessor import NWMFileProcessor
from nwm_client.NWMFileCatalog import HTTPFileCatalog

import tempfile
from pathlib import Path
import dask.dataframe as dd

def main():
    verify = None
    configuration = "short_range"
    reference_time = "20210910T00Z"
    server = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"

    # Check local file cache
    local_file = Path(f"nwm_cache.parquet/{configuration}/RT{reference_time}")
    if local_file.exists():
        df = dd.read_parquet(local_file, write_index=False, compression="snappy")
    else:
        # Get list of files
        catalog = HTTPFileCatalog(
            server=server,
            verify=verify
            )
        urls = catalog.list_blobs(
            configuration=configuration,
            reference_time=reference_time
        )

        # Download and process files
        with tempfile.TemporaryDirectory() as dir:
            # Download files
            downloader = FileDownloader(output_directory=dir,
            verify=verify
            )
            downloader.get(urls)

            # Process files
            df = NWMFileProcessor.get_dask_dataframe(dir)

        # Save dataframe
        df.to_parquet(local_file)

    df_sub = df[["feature_id", "streamflow"]]
    df_max = df_sub.groupby("feature_id").max()
    print(df_max.compute())

if __name__ == "__main__":
    main()

from nwm_client.FileDownloader import FileDownloader
from nwm_client.NWMFileProcessor import NWMFileProcessor
from nwm_client.NWMFileCatalog import HTTPFileCatalog
from nwm_client.NWMFileCatalog import GCPFileCatalog
from nwm_client.parquet_cache import ParquetCache

import tempfile
from pathlib import Path
import dask.dataframe as dd
import pandas as pd
from time import sleep

def get_cycle(catalog, configuration, reference_time, verify):
    # Get list of files
    urls = catalog.list_blobs(
        configuration=configuration,
        reference_time=reference_time
    )

    # Download and process files
    with tempfile.TemporaryDirectory() as dir:
        # Download files
        downloader = FileDownloader(
            output_directory=dir,
            verify=verify
            )
        downloader.get(urls)

        # Process files
        return NWMFileProcessor.get_dask_dataframe(dir)

def main():
    # Use HTTP catalog
    server = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/"
    verify = None
    catalog = HTTPFileCatalog(
        server=server,
        verify=verify
        )

    # Use GCP Catalog
    # catalog = GCPFileCatalog()

    # Get options
    configuration = "analysis_assim"
    reference_time = "20210914T10Z"

    # Cache options
    root = "nwm_cache.parquet"
    key = f"{configuration}/RT{reference_time}"

    with ParquetCache(root) as cache:
        df = cache.get(
            get_cycle,
            key,
            catalog=catalog,
            configuration=configuration,
            reference_time=reference_time,
            verify=verify
            )

    # Find maximum flows
    df_sub = df[["feature_id", "streamflow"]]
    df_max = df_sub.groupby("feature_id").max()
    df_max = df_max[df_max > 0.0].dropna()
    print(df_max.compute())

if __name__ == "__main__":
    main()

from dataclasses import dataclass
from abc import ABC, abstractmethod
import pandas as pd
import dask
import dask.dataframe as dd
from io import BytesIO
import xarray as xr
from pathlib import Path
import dask.bag as db
from dask.distributed import Client

# class DataClient(ABC):
#     """OWPHydroTools data client abstract base class."""

#     @abstractmethod
#     def get() -> pd.DataFrame:
#         pass

# class NWMDataClient(DataClient):
#     """OWPHydroTools NWM data client abstract base class."""

#     @abstractmethod
#     def get_raw_bytes(self, configuration, reference_time) -> bytes:
#         pass

#     def convert_to_pandas(self):
#         print("Processing data")
        
#         return dask.datasets.timeseries().head()

#     def get(self, configuration, reference_time) -> pd.DataFrame:
#         # Get raw bytes
#         data = self.get_raw_bytes(configuration, reference_time)

#         # Get dataframe
#         df = self.convert_to_pandas()

#         return df

# @dataclass
# class GCPNWMDataClient(NWMDataClient):
#     """OWPHydroTools class for retrieving NWM data from Google Cloud Platform."""
#     bucket: str = "national-water-model"

#     def get_raw_bytes(self, configuration, reference_time) -> bytes:
#         print("Retrieving raw data from GCP")
#         return b'gcp_data'

# @dataclass
# class HTTPNWMDataClient(NWMDataClient):
#     """OWPHydroTools class for retrieving NWM data from generic HTTP servers."""
#     server: str = "NOMADS"

#     def get_raw_bytes(self, configuration, reference_time) -> bytes:
#         print(f"Retrieving raw data from {self.server}")
#         return b'http_data'

# def main():
#     """Main function."""
#     # Retrieve data
#     client = GCPNWMDataClient()
#     df = client.get("config", "ref_time")
#     print(df)

#     # Retrieve HTTP data
#     # client = HTTPNWMDataClient(server="dstore")
#     client = HTTPNWMDataClient()
#     df = client.get("config", "ref_time")
#     print(df)

def process(ifile):
    with open(ifile, 'rb') as f:
        raw_bytes = f.read()

    # Create Dataset
    ds = xr.load_dataset(
        BytesIO(raw_bytes),
        engine='h5netcdf',
        mask_and_scale=True
        )

    # ds = ds.sel(feature_id=[101, 179])

    df = ds[['reference_time', 'time', 'streamflow']].to_dask_dataframe()
    
    return df

def main():
    # Set query parameters
    reference_time = "20210819T00Z"
    configuration = "short_range"

    # Break-up reference time
    tokens = reference_time.split('T')
    issue_date = tokens[0]
    issue_time = tokens[1].lower()

    # Set root directory
    root = Path("~/Projects/NWM_DATA").expanduser().resolve()

    # Set path to subdirectory
    subdirectory = root / f"nwm.{issue_date}/{configuration}/"

    # Get filepaths
    filepaths = subdirectory.glob(f"nwm.t{issue_time}.*")

    pth = str(subdirectory / f"nwm.t{issue_time}.*.channel_rt.*")
    ds = xr.open_mfdataset(pth)
    df = ds[['time', 'streamflow']].to_dataframe()
    ds.close()
    # Save
    df['streamflow'] = pd.to_numeric(df["streamflow"], downcast="float")
    print(df.info(memory_usage="deep"))
    df.to_hdf(
        f"short_range.h5",
        key="data",
        complevel=1,
        format="table"
    )
    quit()

    # Generate list
    blob_list = [p for p in filepaths if "channel_rt" in p.name]

    # Load data and write to parquet
    dfs = db.from_sequence(blob_list).map(process).compute()

    # Concatenate
    df = dd.concat(dfs).compute()

    # Optimize
    df["streamflow"] = pd.to_numeric(df["streamflow"], downcast="float")

    # Save
    for fid, df2 in df.groupby("feature_id"):

    # df = df.sort_values(by=["feature_id", "reference_time", "time"])
    # df = df.reset_index(drop=True)

        # Save
        df2.to_hdf(
            f"converted/short_range_{fid}.h5",
            key="data",
            complevel=1,
            format="table"
        )

if __name__ == "__main__":
    main()

from nwm_client.FileDownloader import FileDownloader
from nwm_client.NWMDataProcessor import NWMDataProcessor as NWM
from pathlib import Path
import xarray as xr

def main():
    url1 = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/nwm.20210908/analysis_assim/nwm.t00z.analysis_assim.channel_rt.tm00.conus.nc"
    url2 = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/nwm.20210908/analysis_assim/nwm.t00z.analysis_assim.channel_rt.tm01.conus.nc"
    urls = [url1, url2]

    odir = Path("./output")
    # downloader = FileDownloader(odir, True)
    # downloader.get(urls)

    # Process data
    df = NWM.get_dataframe(odir)
    print(df.info(memory_usage="deep"))
    print(df)

if __name__ == "__main__":
    main()

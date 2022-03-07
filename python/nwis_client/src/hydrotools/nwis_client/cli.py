import click
from hydrotools.nwis_client import IVDataService
from hydrotools.nwis_client import _version as CLIENT_VERSION
from typing import Tuple
from pathlib import Path
import pandas as pd

class TimestampParamType(click.ParamType):
    name = "timestamp"

    def convert(self, value, param, ctx):
        if isinstance(value, pd.Timestamp):
            return value

        try:
            return pd.Timestamp(value)
        except ValueError:
            self.fail(f"{value!r} is not a valid timestamp", param, ctx)

def write_to_csv(
    data: pd.DataFrame,
    ofile: Path,
    comments: bool = True,
    header: bool = True
    ) -> None:
    # Start building output
    output = ''

    # Comments
    if comments:
        output += """# USGS IV Service Data
# 
# value_date: Datetime of measurement (UTC) (character string)
# variable: USGS variable name (character string)
# usgs_site_code: USGS Gage Site Code (character string)
# measurement_unit: Units of measurement (character string)
# value: Measurement value (float)
# qualifiers: Qualifier string (character string)
# series: Series number in case multiple time series are returned (integer)
# 
"""
        # Add version, link, and write time
        now = pd.Timestamp.utcnow()
        output += f"# Generated at {now}\n"
        output += f"# nwis_client version: {CLIENT_VERSION.__version__}\n"
        output += "# Source code: https://github.com/NOAA-OWP/hydrotools\n# \n"

    # Write to file
    output += data.to_csv(index=False, float_format="{:.2f}".format, header=header)
    with ofile.open("w") as of:
        of.write(output)

@click.command()
@click.argument("sites", nargs=-1)
@click.argument("ofile", nargs=1, type=click.Path(path_type=Path))
@click.option("-s", "--startDT", "startDT", nargs=1, type=TimestampParamType(), help="Start datetime")
@click.option("-e", "--endDT", "endDT", nargs=1, type=TimestampParamType(), help="End datetime")
@click.option("-p", "--parameterCd", "parameterCd", nargs=1, type=str, default="00060", help="Parameter code")
@click.option('--comments/--no-comments', default=True, help="Enable/disable comments in output, enabled by default")
@click.option('--header/--no-header', default=True, help="Enable/disable header in output, enabled by default")
def run(
    sites: Tuple[str], 
    ofile: Path, 
    startDT: pd.Timestamp = None,
    endDT: pd.Timestamp = None,
    parameterCd: str = "00060",
    comments: bool = True,
    header: bool = True
    ) -> None:
    """Retrieve data from the USGS IV Web Service API and write to CSV.
    Writes data for all SITES to OFILE.

    Example:
    
    nwis-client 01013500 02146470 my_output.csv
    """
    # Setup client
    client = IVDataService(value_time_label="value_time")

    # Retrieve data
    df = client.get(
        sites=sites,
        startDT=startDT,
        endDT=endDT,
        parameterCd=parameterCd
    )
    
    # Write to CSV
    write_to_csv(data=df, ofile=ofile, comments=comments, header=header)

if __name__ == "__main__":
    run()

from hydrotools.events.baseflow import eckhardt as bf
from hydrotools.nwis_client.iv import IVDataService

# Get some streamflow data
client = IVDataService()
df = client.get(
    startDT="2020-10-01",
    endDT="2021-09-30T23:55",
    sites="02146470"
)

# Important: Streamflow data should be continuous with
#   no missing data and a DateTimeIndex
TIME_SCALE = "1h"
df = df.set_index("value_time").resample(TIME_SCALE).first().ffill()

# Let's rename 'value' to 'total_flow'
df = df.rename(columns={"value": "total_flow"})

# Perform baseflow separation
#   This catchment is pretty small, so we'll use a
#   12-hour recession time-scale
results = bf.separate_baseflow(
    df["total_flow"],
    output_time_scale = TIME_SCALE,
    recession_time_scale = "12h"
    )

# Look at the 12-hour filter parameters
print(f"Recession constant, a: {results.recession_constant:.4f}")
print(f"Maximum baseflow index, bfi_max: {results.maximum_baseflow_index:.4f}")

# Store the resulting baseflow in original DataFrame
df["baseflow"] = results.values
print(df.head())

import plotly.graph_objects as go

df2 = df.loc["2021-02-11":"2021-02-17"]
fig = go.Figure()
fig.add_trace(go.Scatter(x=df2.index, y=df2.total_flow))
fig.add_trace(go.Scatter(x=df2.index, y=df2.baseflow))
fig.show()

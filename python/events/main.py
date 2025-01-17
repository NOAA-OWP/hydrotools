from hydrotools.events.baseflow import eckhardt as bf
from hydrotools.nwis_client.iv import IVDataService
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def main():
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

    df2 = df.loc["2021-02-11":"2021-02-17"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df2.index, y=df2.total_flow, name="Total Flow"))
    fig.add_trace(go.Scatter(x=df2.index, y=df2.baseflow, name="Baseflow"))
    fig.update_layout(
        yaxis=dict(
            title=dict(
                text=r"$\text{ Discharge } \text{ (foot }^3 \text{ s }^{-1})$"
            ),
            showline=True,
            linecolor="black",
            tickmode="array",
            tickvals=np.arange(0.0, 400.0, 50.0),
            linewidth=2,
            ticks="outside",
            range=[0.0, 351.0],
            tickwidth=2
        ),
        xaxis=dict(
            showline=True,
            linecolor="black",
            linewidth=2,
            ticks="outside",
            tickmode="array",
            tickvals=pd.date_range("2021-02-11", periods=8),
            range=["2021-02-11", "2021-02-17T00:15"],
            tickwidth=2
        ),
        plot_bgcolor="white",
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=10
        )
    )
    fig.write_image("baseflow_hydrograph.png", width=960, height=540, scale=2)

if __name__ == "__main__":
    main()

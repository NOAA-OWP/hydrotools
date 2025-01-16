from hydrotools.nwis_client.iv import IVDataService
import plotly.graph_objects as go

from hydrotools.events.baseflow import eckhardt as bf

def main():
    client = IVDataService()
    df = client.get(
        startDT="2020-10-01",
        endDT="2021-09-30T23:55",
        sites="02146470"
    )
    df = df[["value_time", "value"]].set_index("value_time").resample("15min").first().ffill()

    b = bf.separate_baseflow(df["value"], "15min", "12h")
    df["baseflow"] = b.values

    print(df.head())
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.value))
    fig.add_trace(go.Scatter(x=df.index, y=df.baseflow))
    fig.show()

if __name__ == "__main__":
    main()

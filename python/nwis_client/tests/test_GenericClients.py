from hydrotools.nwis_client import GenericClients as gc
from pathlib import Path
import numpy as np
import json

class MockResponse:
    services = {
        "Site": "site_response.tsv",
        "Peak": "peak_response.tsv",
        "Stat": "stat_response.tsv",
        "RatingCurve": "rating_curve_response.tsv",
        "FloodStage": "flood_stage_response.json"
    }

    def __init__(self, service) -> None:
        self.service = service

    def text(self):
        idir = Path(__file__).parent
        with open(idir / self.services[self.service], "r") as fi:
            return fi.read()

    def json(self):
        idir = Path(__file__).parent
        with open(idir / self.services[self.service], "r") as fi:
            return json.loads(fi.read())

class MockRestClient:
    def __init__(
        self,
        service,
        base_url,
        headers,
        enable_cache,
        cache_filename,
        cache_expire_after
        ) -> None:
        self.service = service

    def get(self, **kw):
        return MockResponse(self.service)

    def mget(self, **kw):
        return [MockResponse(self.service)]

def test_SiteClient(monkeypatch):
    monkeypatch.setattr(gc, "RestClient", lambda **kw: MockRestClient("Site", **kw))

    client = gc.NWISSiteClient()
    df = client.get(sites="01646500")
    assert df["usgs_site_code"].iloc[0] == "01646500"

def test_PeakClient(monkeypatch):
    monkeypatch.setattr(gc, "RestClient", lambda **kw: MockRestClient("Peak", **kw))

    client = gc.NWISPeakClient()
    df = client.get(sites=["01013500", "02146470"])
    assert np.all(np.isin(["01013500", "02146470"], df["usgs_site_code"]))

def test_StatClient(monkeypatch):
    monkeypatch.setattr(gc, "RestClient", lambda **kw: MockRestClient("Stat", **kw))

    client = gc.NWISStatClient()
    df = client.get(sites=["02146470"])
    assert (df["parameter_cd"] == "00060").all()

def test_RatingCurveClient(monkeypatch):
    monkeypatch.setattr(gc, "RestClient", lambda **kw: MockRestClient("RatingCurve", **kw))

    client = gc.NWISRatingCurveClient()
    df = client.get(sites=["01010000"])
    assert (df["usgs_site_code"] == "01010000").all()

def test_FloodStageClient(monkeypatch):
    monkeypatch.setattr(gc, "RestClient", lambda **kw: MockRestClient("FloodStage", **kw))

    client = gc.NWISFloodStageClient()
    df = client.get(sites=["01010000"])
    assert (df["usgs_site_code"] == "01010000").all()

import pytest
from evaluation_tools.nwis_client import iv

# Datetime test related imports
from datetime import datetime
import numpy as np
import pandas as pd


class MockRequests:
    """Mock of requests object

    Key words passed will be set as instance variable at construction.
    Requests methods can be added, convention is to return _ kwarg of the
    method name. i.e. requests.json() -> _json. This allows for values to be
    passed at test run time.

    functools partial can be used to bind these to the class before passing
    to the mocker.

    Example
    -------
    def test_requests_get(monkeypatch):
        # Uses monkeypatch from `pytest`
        import requests
        from functools import partial

        requests_testable_attributes = {"status_code": 200, "_json": {"status": "pass"}}
        mock_request = partial(MockRequests, **requests_testable_attributes)

        mocker.setattr(requests, 'get', mock_requests)

        assert function_that_calls_requests_get() == requests_testable_attributes['_json']
    """

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def json(self):
        return self._json

    def text(self):
        return self._text


@pytest.fixture
def setup_iv():
    return iv.IVDataService()


simplify_variable_test_data = [
    ("test", ",", "test"),
    ("TEST", ",", "test"),
    ("TEST,test", ",", "test"),
    ("TEST:ts::et::", "::", "test:ts"),
]


@pytest.mark.parametrize("variable,delimiter,expected", simplify_variable_test_data)
def test_simplify_variable_name_1(variable, delimiter, expected, setup_iv):
    assert setup_iv.simplify_variable_name(variable, delimiter) == expected


# Test properties
def test_get_base_url(setup_iv):
    assert (setup_iv.base_url) == "https://waterservices.usgs.gov/nwis/iv/"


def test_get_headers(setup_iv):
    assert (setup_iv.headers) == {"Accept-Encoding": "gzip, compress"}


def request_status_setter(status: int = 404):
    import requests
    from functools import partial

    requests_testable_attributes = {"status_code": status}
    return partial(MockRequests, **requests_testable_attributes)


def test_get_throw_warning(monkeypatch):
    def wrapper(*args, **kwargs):
        return []

    # Monkey patch get_raw method to return []
    monkeypatch.setattr(iv.IVDataService, "get_raw", wrapper)

    with pytest.warns(UserWarning):
        assert iv.IVDataService.get(sites="04233255").empty is True


@pytest.mark.slow
def test_get(setup_iv):
    # TODO
    """Test data retrieval and parsing"""
    df = setup_iv.get(sites="01646500,02140991", parameterCd="00060,00065")
    assert "01646500" in df["usgs_site_code"].values
    assert "02140991" in df["usgs_site_code"].values


def test_get_raw_with_mock(setup_iv, monkeypatch):
    """Test data retrieval and parsing"""
    import json
    from pathlib import Path
    from evaluation_tools._restclient import RestClient

    def requests_mock(*args, **kwargs):
        json_text = json.loads(
            (Path(__file__).resolve().parent / "nwis_test_data.json").read_text()
        )
        # key_word_args = {"_json": json_text}
        return MockRequests(_json=json_text)

    monkeypatch.setattr(RestClient, "get", requests_mock)

    data = setup_iv.get_raw(sites="01646500", parameterCd="00060,00065")
    assert data[0]["usgs_site_code"] == "01646500"


@pytest.mark.parametrize("unchunked", [list(range(200)), str(list(range(200)))[1:-1]])
def test_chunk_request(setup_iv, unchunked):

    assert len(setup_iv._chunk_request(unchunked)) == 3


def test_handle_response(setup_iv, monkeypatch):
    import json
    from pathlib import Path
    import requests

    def mock_json(*args, **kwargs):
        return json.loads(
            (Path(__file__).resolve().parent / "nwis_test_data.json").read_text()
        )

    monkeypatch.setattr(requests.Response, "json", mock_json)

    assert (
        setup_iv._handle_response(requests.Response)[0]["usgs_site_code"] == "01646500"
    )


def test_get_and_handle_response(setup_iv, monkeypatch):
    import json
    from pathlib import Path
    from evaluation_tools._restclient import RestClient
    import requests

    def mock_json(*args, **kwargs):
        json_text = json.loads(
            (Path(__file__).resolve().parent / "nwis_test_data.json").read_text()
        )
        key_word_args = {"_json": json_text}
        return MockRequests(**key_word_args)

    monkeypatch.setattr(RestClient, "get", mock_json)

    assert (
        setup_iv._get_and_handle_response(requests.Response)[0]["usgs_site_code"]
        == "01646500"
    )


@pytest.mark.slow
def test_multiprocessing_get(setup_iv, monkeypatch):
    import json
    from pathlib import Path
    from evaluation_tools._restclient import RestClient
    import requests

    sites = [
        "01646500",
        "01646500",
        "01646500",
    ]
    parameters = {
        "parameterCd": "00060",
        "siteStatus": "active",
        "format": "json",
    }

    def mock_json(*args, **kwargs):
        json_text = json.loads(
            (Path(__file__).resolve().parent / "nwis_test_data.json").read_text()
        )
        key_word_args = {"_json": json_text}
        return MockRequests(**key_word_args)

    monkeypatch.setattr(RestClient, "get", mock_json)
    print(
        setup_iv._multiprocessing_get(
            sites, parameters=parameters, partition_max_size=2
        )
    )


unique_test_data = [
    ([1, 2, 3], [1, 2, 3]),
    ([2, 1, 3], [1, 2, 3]),
    ([3, 2, 1], [1, 2, 3]),
    ([1, 3, 2], [1, 2, 3]),
    ([2, 3, 1], [1, 2, 3]),
    ([3, 1, 2], [1, 2, 3]),
    ([3, 3, 3], [3]),
    (["4"], ["4"]),
]


@pytest.mark.parametrize("collection,validation", unique_test_data)
def test_unique(setup_iv, collection, validation):
    assert setup_iv._unique(collection) == validation


test_get_startDT_endDT_scenarios = [
    # Straight path
    ("2020-08-10", "2020-08-10T00:00+0000"),
    (datetime(2020, 8, 10), "2020-08-10T00:00+0000"),
    (np.datetime64("2020-08-10"), "2020-08-10T00:00+0000"),
    (pd.to_datetime("2020-08-10"), "2020-08-10T00:00+0000"),
    # Non green light test
    ("2020-08-10T04:15-05:00", "2020-08-10T09:15+0000"),
    # Strange behavior here in #6. np converts dt string w/ tzinfo to UTC by default
    (pd.to_datetime("2020-08-10T04:15-05:00"), "2020-08-10T09:15+0000"),
]


@pytest.mark.parametrize("test,validation", test_get_startDT_endDT_scenarios)
def test_handle_dates(setup_iv, test, validation):
    """ Input dates should be output as strings in UTC tz """
    date = setup_iv._handle_date(test)
    assert date == validation


test_get_startDT_endDT_scenarios_as_list = [
    (["2020-01-01", "2020-02-01"], ["2020-01-01T00:00+0000", "2020-02-01T00:00+0000"]),
    (
        ["2020-01-01", pd.to_datetime("2020-02-01").timestamp()],
        np.array(["2020-01-01T00:00+0000", "2020-02-01T00:00+0000"]),
    ),
]


@pytest.mark.parametrize("test,validation", test_get_startDT_endDT_scenarios_as_list)
def test_handle_dates_list_of_dates(setup_iv, test, validation):
    """ Input dates should be output as strings in UTC tz """
    date = setup_iv._handle_date(test)
    assert np.array_equal(date, validation)


@pytest.mark.slow
def test_get_slow(setup_iv):
    site = "01646500"
    start, end = "2020-01-01", "2020-01-01T06:15"
    df = setup_iv.get(site, startDT=start, endDT=end)
    assert df["value_date"][0].isoformat() == f"{start}T00:00:00"


datetime_keyword_test_data = [
    {"startDT": "2020-08-20"},
    {"startDT": "2020-08-20", "endDT": "2020-08-21"},
    {"period": "P2D"},
]


@pytest.mark.parametrize("test_data", datetime_keyword_test_data)
def test_startDT_endDT_period_in_get_raw(setup_iv, monkeypatch, test_data):
    """ Test datetime keyword argument behavior in `get_raw` """

    def handler(*args, **kwargs):
        return 1

    monkeypatch.setattr(iv.IVDataService, "_get_and_handle_response", handler)
    assert setup_iv.get_raw(sites="01646500", **test_data) == 1


datetime_keyword_test_data_should_fail = [
    {"endDT": "2020-08-21"},
    {"startDT": "2020-08-21", "period": "P2D"},
    {"endDT": "2020-08-20", "period": "P2D"},
    {"startDT": "2020-08-20", "endDT": "2020-08-20", "period": "P2D"},
]


@pytest.mark.parametrize("test_data", datetime_keyword_test_data_should_fail)
def test_startDT_endDT_period_in_get_raw_should_fail(setup_iv, monkeypatch, test_data):
    """ Test datetime keyword argument behavior in `get_raw` """

    def handler(*args, **kwargs):
        return 1

    with pytest.raises(KeyError):
        monkeypatch.setattr(iv.IVDataService, "_get_and_handle_response", handler)
        setup_iv.get_raw(sites="01646500", **test_data)


period_testing_set = [
    "P1Y",
    "P1M",
    "P1D",
    "P1W",
    "PT1H",
    "PT1M",
    "PT1S",
]


@pytest.mark.parametrize("testing", period_testing_set)
def test_validate_period_string(setup_iv, testing):
    """ Verify if strings adhere to ISO 8601 """
    assert setup_iv._validate_period_string(testing) is True


period_testing_set_should_be_false = [
    "PY",
    "PM1",
    "failure",
    "P1W2D",
    "PT1s",
]


@pytest.mark.parametrize("testing", period_testing_set_should_be_false)
def test_validate_period_string_is_false(setup_iv, testing):
    """ Verify if strings adhere to ISO 8601. Failure cases"""
    assert setup_iv._validate_period_string(testing) is False


HANDLE_START_END_PERIOD_URL_PARAMS_PARAMETRIZATION = [
    # Straight forward tests
    ({"startDT": None, "endDT": None, "period": None}, {}),
    (
        {"startDT": "2020-01-01", "endDT": "2020-01-01", "period": None},
        {"startDT": "2020-01-01T00:00+0000", "endDT": "2020-01-01T00:00+0000"},
    ),
    (
        {"startDT": None, "endDT": None, "period": "P1D"},
        {"period": "P1D"},
    ),
    (
        {"startDT": datetime(2020, 1, 1)},
        {"startDT": "2020-01-01T00:00+0000"},
    ),
    (
        {"startDT": pd.to_datetime("2020-01-01").timestamp()},
        {"startDT": "2020-01-01T00:00+0000"},
    ),
    # (
    #     {"startDT": ["2020-01-01"], "endDT": None, "period": None},
    #     {"startDT": [""]},
    # ),
]


@pytest.mark.parametrize(
    "input, validation", HANDLE_START_END_PERIOD_URL_PARAMS_PARAMETRIZATION
)
def test__handle_start_end_period_url_params(setup_iv, input, validation):
    assert setup_iv._handle_start_end_period_url_params(**input) == validation


HANDLE_START_END_PERIOD_URL_PARAMS_PARAMETRIZATION_ERROR = [
    # Should raise KeyError
    (
        {"startDT": None, "endDT": "2020-01-01"},
        KeyError,
    ),
    (
        {"startDT": "2020-01-01", "endDT": "2020-01-01", "period": "P1D"},
        KeyError,
    ),
    (
        {"startDT": None, "endDT": "2020-01-01", "period": "P1D"},
        KeyError,
    ),
    (
        {"startDT": "2020-01-01", "endDT": None, "period": "P1D"},
        KeyError,
    ),
    (
        {"period": "TP1D"},
        KeyError,
    ),
    (
        {"startDT": ["2020-01-01", "2020-01-02"]},
        TypeError,
    ),
]


@pytest.mark.parametrize(
    "input,error_type", HANDLE_START_END_PERIOD_URL_PARAMS_PARAMETRIZATION_ERROR
)
def test__handle_start_end_period_url_params_should_throw(setup_iv, input, error_type):
    with pytest.raises(error_type):
        setup_iv._handle_start_end_period_url_params(**input)


@pytest.mark.slow
def test_get_raw_stateCd(setup_iv):
    """Test data retrieval and parsing"""
    df = setup_iv.get_raw_stateCd(stateCd="AL", parameterCd="00060")
    sites = {item["usgs_site_code"] for item in df}
    assert "02339495" in sites


def test_get_raw_stateCd_invalid_state_value_error(setup_iv):
    """Test data retrieval and parsing"""
    with pytest.raises(ValueError):
        # Invalid stateCd name
        setup_iv.get_raw_stateCd(stateCd="NA", parameterCd="00060")


@pytest.mark.slow
def test_get_raw_huc(setup_iv):
    """Test data retrieval and parsing"""
    df = setup_iv.get_raw_huc(huc="02070010", parameterCd="00060")
    sites = {item["usgs_site_code"] for item in df}
    assert "01647850" in sites


RAW_BBOX_PARAMS = [
    ("-83.000000,36.500000,-81.000000,38.500000", "03177710"),
    (["-83.000000", "36.500000", "-81.000000", "38.500000"], "03177710"),
    ([-83.000000, 36.500000, -81.000000, 38.500000], "03177710"),
]


@pytest.mark.slow
@pytest.mark.parametrize("test,validation", RAW_BBOX_PARAMS)
def test_get_raw_bBox(setup_iv, test, validation):
    """Test data retrieval and parsing"""
    df = setup_iv.get_raw_bBox(bBox=test, parameterCd="00060")
    sites = {item["usgs_site_code"] for item in df}
    assert validation in sites


@pytest.mark.slow
def test_get_raw_countyCd(setup_iv):
    """Test data retrieval and parsing"""
    df = setup_iv.get_raw_countyCd(countyCd=51059, parameterCd="00060")
    sites = {item["usgs_site_code"] for item in df}
    assert "01645704" in sites

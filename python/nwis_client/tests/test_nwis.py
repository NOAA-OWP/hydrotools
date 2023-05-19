import pytest
from hydrotools import nwis_client
from hydrotools.nwis_client import iv

# Datetime test related imports
from datetime import datetime
import numpy as np
import pandas as pd


split_params = [
    ("key", [1, 2, 3], 4, None, [{"key": ["1", "2", "3"]}]),
    ("key", [1, 2, 3], 4, ",", [{"key": "1,2,3"}]),
    (
        "key",
        [1, 2, 3, 4],
        2,
        None,
        [{"key": ["1", "2"]}, {"key": ["3", "4"]}],
    ),
    ("key", [1, 2, 3, 4], 2, ",", [{"key": "1,2"}, {"key": "3,4"}]),
]


@pytest.mark.parametrize("key,values,split_threshold,join_on,validation", split_params)
def test_split(key, values, split_threshold, join_on, validation):
    r = iv.split(
        key=key, values=values, split_threshold=split_threshold, join_on=join_on
    )  # type: list[dict]

    for idx, item in enumerate(validation):
        for k, v in item.items():
            a = r[idx][k]
            if isinstance(a, np.ndarray):
                assert (a == v).all()
            else:
                assert a == v

##### MOCK OBJECTS #####

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

##### FIXTURES #####

@pytest.fixture(name="IVDataServiceWithTempCache")
def wrap_iv_cache_location_to_temp(loop):
    from tempfile import TemporaryDirectory
    from pathlib import Path
    from functools import partial

    with TemporaryDirectory() as temp:
        cache_file = Path(temp) / "cache.sqlite"

        o = partial(iv.IVDataService, cache_filename=cache_file)
        return o
    

@pytest.fixture
def setup_iv(IVDataServiceWithTempCache):
    """Setup IVDataService client. Cache file is """
    o = IVDataServiceWithTempCache()
    yield o
    o._restclient.close()

@pytest.fixture
def setup_iv_value_time(IVDataServiceWithTempCache):
    o = IVDataServiceWithTempCache(value_time_label="value_time")
    yield o
    o._restclient.close()

@pytest.fixture
def mock_iv(setup_iv, monkeypatch):
    """mock `iv.IVDataService`. `iv.IVDataService`'s `get_raw` method has been mocked to return an
    empty list.
    """
    def wrapper(*args, **kwargs):
        return []

    # Monkey patch get_raw method to return []
    monkeypatch.setattr(iv.IVDataService, "get_raw", wrapper)

@pytest.fixture
def mocked_iv(mock_iv, setup_iv):
    """return mocked and setup `iv.IVDataService`. 
    `iv.IVDataService`'s `get_raw` method has been mocked to return an empty list.
    """
    return setup_iv
    

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
    from functools import partial

    requests_testable_attributes = {"status_code": status}
    return partial(MockRequests, **requests_testable_attributes)


def test_get_throw_warning(setup_iv, monkeypatch):
    def wrapper(*args, **kwargs):
        return []

    # Monkey patch get_raw method to return []
    monkeypatch.setattr(iv.IVDataService, "get_raw", wrapper)

    with pytest.warns(UserWarning):
        assert setup_iv.get(sites="04233255").empty is True


GET_PARAM_SITES = [
    ("01646500,02140991", ["01646500", "02140991"]),
    (["01646500", "02140991"], ["01646500", "02140991"]),
    (np.array(["01646500", "02140991"]), ["01646500", "02140991"]),
    (pd.Series(["01646500", "02140991"]), ["01646500", "02140991"]),
]


@pytest.mark.slow
@pytest.mark.parametrize("sites,validation", GET_PARAM_SITES)
def test_get(setup_iv, sites, validation):
    """Test data retrieval and parsing"""
    df = setup_iv.get(sites=sites, parameterCd="00060")
    assert df["usgs_site_code"].isin(validation).all()

@pytest.mark.slow
@pytest.mark.parametrize("sites,validation", GET_PARAM_SITES)
def test_get_value_time(setup_iv_value_time, sites, validation):
    """Test data retrieval and parsing"""
    df = setup_iv_value_time.get(sites=sites, parameterCd="00060")
    assert df["usgs_site_code"].isin(validation).all()
    assert "value_time" in df


@pytest.mark.slow
def test_get_with_expanded_metadata(setup_iv):
    """Test expanded metadata option"""
    df = setup_iv.get(sites=["01646500"], parameterCd="00060", include_expanded_metadata=True)
    assert (df["huc_code"] == "02070008").all()

def test_get_raw_with_mock(setup_iv, monkeypatch):
    """Test data retrieval and parsing"""
    import json
    from pathlib import Path
    from hydrotools._restclient import RestClient

    def requests_mock(*args, **kwargs):
        json_text = json.loads(
            (Path(__file__).resolve().parent / "nwis_test_data.json").read_text()
        )
        # key_word_args = {"_json": json_text}
        return MockRequests(_json=json_text)

    monkeypatch.setattr(RestClient, "get", requests_mock)

    data = setup_iv.get_raw(sites="01646500", parameterCd="00060,00065")
    assert data[0]["usgs_site_code"] == "01646500"

def test_expanded_metadata(setup_iv, monkeypatch):
    """Test data retrieval and parsing"""
    import json
    from pathlib import Path
    from hydrotools._restclient import RestClient

    def requests_mock(*args, **kwargs):
        json_text = json.loads(
            (Path(__file__).resolve().parent / "nwis_test_data.json").read_text()
        )
        # key_word_args = {"_json": json_text}
        return MockRequests(_json=json_text)

    monkeypatch.setattr(RestClient, "get", requests_mock)

    data = setup_iv.get_raw(sites="01646500", parameterCd="00060,00065", include_expanded_metadata=True)
    assert data[0]["hucCd"] == "02070008"

def test_expanded_metadata_columns(setup_iv, monkeypatch):
    """Test data retrieval and parsing"""
    import json
    from pathlib import Path
    from hydrotools._restclient import RestClient

    def requests_mock(*args, **kwargs):
        json_text = json.loads(
            (Path(__file__).resolve().parent / "nwis_test_data.json").read_text()
        )
        # key_word_args = {"_json": json_text}
        return MockRequests(_json=json_text)

    monkeypatch.setattr(RestClient, "get", requests_mock)

    data = setup_iv.get(sites="01646500", parameterCd="00060,00065", include_expanded_metadata=True)
    extra_columns = [
        "site_type_code",
        "huc_code",
        "county_code",
        "state_code",
        "site_name",
        "latitude",
        "longitude"
        ]
    for c in extra_columns:
        assert c in data.columns


def test_handle_response(setup_iv, monkeypatch):
    import json
    from pathlib import Path
    import aiohttp

    def mock_json(*args, **kwargs):
        return json.loads(
            (Path(__file__).resolve().parent / "nwis_test_data.json").read_text()
        )

    monkeypatch.setattr(aiohttp.ClientResponse, "json", mock_json)

    assert (
        setup_iv._handle_response(aiohttp.ClientResponse)[0]["usgs_site_code"] == "01646500"
    )


test_get_startDT_endDT_scenarios = [
    # Straight path
    ("2020-08-10", "2020-08-10T00:00+0000"),
    (datetime(2020, 8, 10), "2020-08-10T00:00+0000"),
    (np.datetime64("2020-08-10"), "2020-08-10T00:00+0000"),
    (pd.to_datetime("2020-08-10"), "2020-08-10T00:00+0000"),
]


@pytest.mark.parametrize("test,validation", test_get_startDT_endDT_scenarios)
def test_handle_dates(setup_iv, test, validation):
    """ Input dates should be output as strings in UTC tz """
    date = setup_iv._handle_date(test)
    assert date == validation

test_get_startDT_endDT_scenarios_should_warn = [
    # Non green light test
    ("2020-08-10T04:15-05:00", "2020-08-10T09:15+0000"),
    # Strange behavior here in #6. np converts dt string w/ tzinfo to UTC by default
    (pd.to_datetime("2020-08-10T04:15-05:00"), "2020-08-10T09:15+0000"),
]

@pytest.mark.parametrize("test,validation", test_get_startDT_endDT_scenarios_should_warn)
def test_handle_dates_raise_deprecation_warning(setup_iv, test, validation):
    """ Input dates should be output as strings in UTC tz """
    with pytest.warns(DeprecationWarning):
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
    # IV api seems to send different start based on daylights saving time.
    # Test is less prescriptive, but still should suffice
    assert df["value_time"][0].isoformat().startswith(start)


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
    df = setup_iv.get_raw(stateCd="AL", parameterCd="00060")
    sites = {item["usgs_site_code"] for item in df}
    assert "02339495" in sites


@pytest.mark.slow
def test_get_raw_huc(setup_iv):
    """Test data retrieval and parsing"""
    df = setup_iv.get_raw(huc="02070010", parameterCd="00060")
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
    df = setup_iv.get_raw(bBox=test, parameterCd="00060")
    sites = {item["usgs_site_code"] for item in df}
    assert validation in sites


@pytest.mark.slow
def test_get_raw_countyCd(setup_iv):
    """Test data retrieval and parsing"""
    df = setup_iv.get_raw(countyCd="51059", parameterCd="00060")
    sites = {item["usgs_site_code"] for item in df}
    assert "01645704" in sites


SPLITTING_BBOX_PARAMS = (
    ("3,3,3,3", ["3,3,3,3"]),
    (("3", "3", "3", "3"), ["3,3,3,3"]),
    ((3, 3, 3, 3), ["3,3,3,3"]),
    [np.array((3, 3, 3, 3)), ["3,3,3,3"]],
    [pd.Series((3, 3, 3, 3)), ["3,3,3,3"]],
    ("3,3,3,3,3,3,3,3", ["3,3,3,3", "3,3,3,3"]),
    (("3,3,3,3", "3,3,3,3"), ["3,3,3,3", "3,3,3,3"]),
    (np.array(("3,3,3,3", "3,3,3,3")), ["3,3,3,3", "3,3,3,3"]),
    (pd.Series(("3,3,3,3", "3,3,3,3")), ["3,3,3,3", "3,3,3,3"]),
    (pd.Series((["3,3,3,3"], [3, 3, 3, 3])), ["3,3,3,3", "3,3,3,3"]),
    (["3,3,3,3"], ["3,3,3,3"]),
    ((["3,3,3,3"], [3, 3, 3, 3]), ["3,3,3,3", "3,3,3,3"]),
    ((["3,3,3,3"], ["3,3,3,3"]), ["3,3,3,3", "3,3,3,3"]),
    ((["3,3,3,3", 3, 3, 3, 3], ["3,3,3,3"]), ["3,3,3,3", "3,3,3,3", "3,3,3,3"]),
)


@pytest.mark.parametrize("test,validation", SPLITTING_BBOX_PARAMS)
def test_splitting_bbox(test, validation):
    v = iv._bbox_split(test)
    assert v == validation


def test_get_returns_empty_canonical_dataframe(setup_iv_value_time, monkeypatch):
    """Verify that `get` can returns an empty canonical dataframe."""

    with pytest.warns(UserWarning):
        def get_raw_mock(*args, **kwargs):
            return [{"values": []}]

        monkeypatch.setattr(iv.IVDataService, "get_raw", get_raw_mock)
        df = setup_iv_value_time.get(
            sites=["01189000"], startDT="2015-12-01T00:00", endDT="2015-12-31T23:45"
        )
        canonical_df = iv._create_empty_canonical_df()
        assert df.equals(canonical_df)

def test_nwis_client_get_throws_warning_for_kwargs(mocked_iv):
    from packaging import version
    version = version.parse(nwis_client.__version__)
    version = (version.major, version.minor)

    # versions > 3.1 should throw an exception instead of a warning
    assert version > (3, 1)

    with pytest.raises(RuntimeError):
        # startDt should be startDT
        mocked_iv.get(sites=["01189000"], startDt="2022-01-01")

@pytest.mark.slow
def test_nwis_client_cache_path(loop):
    """verify that cache directory has configurable location"""
    from tempfile import TemporaryDirectory
    from pathlib import Path

    with TemporaryDirectory() as temp:
        cache_file = Path(temp) / "cache.sqlite"

        service = iv.IVDataService(cache_filename=cache_file)
        service.get(sites=["01189000"], startDT="2022-01-01")

        assert cache_file.exists()

        # close resources
        service._restclient.close()

def test_fixes_209(loop, monkeypatch):
    """
    verify that pandas FutureWarning is not raised by `IVDataService.get`. This FutureWarning was
    introduced in 1.5.1. see pandas changelog
    https://pandas.pydata.org/docs/whatsnew/v1.5.0.html#inplace-operation-when-setting-values-with-loc-and-iloc
    for more information.
    """
    import warnings

    def mock_get_raw(*args, **kwargs):
        return [{'usgs_site_code': '01646500', 'variableName': 'streamflow', 'measurement_unit': 'ft3/s', 'values': [{'value': '18300', 'qualifiers': ['A'], 'dateTime': '2020-12-31T20:00:00.000-05:00'}, {'value': '18200', 'qualifiers': ['A'], 'dateTime': '2020-12-31T20:15:00.000-05:00'}], 'series': 0}]

    monkeypatch.setattr(iv.IVDataService, "get_raw", mock_get_raw)
    client = iv.IVDataService(enable_cache=False)

    # fail if ANY warning. this should probably be more specific, but if we get any warnings, we
    # should resolve them.
    with warnings.catch_warnings():
        # warning will be raised to exception if caught
        warnings.simplefilter("error")
        client.get(sites='01646500', startDT="2021-01-01T01:00", endDT="2021-01-01T01:15")

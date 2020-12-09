import pytest
from evaluation_tools._restclient import RestClient


@pytest.mark.parametrize(
    "base,headers,rcf,ea,retries",
    [
        ("", None, None, 34, 1),
        ("", None, None, 34, -1),
        (
            "http://www.google.com/",
            {"Accept-Encoding": "gzip, compress"},
            None,
            None,
            1,
        ),
        ("", None, "test", 34, 1),
        ("", None, "test", 34, 3),
    ],
)
def test_construction(base, headers, rcf, ea, retries):
    """ Test RestClient construction """
    return RestClient(
        base_url=base,
        headers=headers,
        requests_cache_filename=rcf,
        requests_cache_expire_after=ea,
        retries=retries,
    )


@pytest.fixture
def empty_restclient():
    return RestClient()


@pytest.mark.slow
@pytest.fixture
def restclient():
    return RestClient(
        base_url="https://jsonplaceholder.typicode.com/",
        headers=None,
        requests_cache_filename="test_google",
    )


@pytest.mark.slow
def test_get_with_parameter(restclient):
    url = "https://jsonplaceholder.typicode.com/comments"
    parameters = {"postId": "1"}
    verify = "https://jsonplaceholder.typicode.com/comments?postId=1"
    assert restclient.get(url=url, parameters=parameters).url == verify


def test_get_empty_constructor(empty_restclient):
    """  test get empty constructor """
    with pytest.raises(AttributeError):
        empty_restclient.get()


@pytest.mark.parametrize(
    "provided,expected",
    [
        ({"url": "http://test-url.test",}, "http://test-url.test/"),
        (
            {
                "url": "http://test-url.test",
                "parameters": {"test": [1, "2"]},
                "parameter_delimiter": "",
                "headers": "",
            },
            "http://test-url.test/?test=1&test=2",
        ),
        (
            {
                "url": "http://test-url.test",
                "parameters": {"test": [1, 2]},
                "parameter_delimiter": ",",
                "headers": {},
            },
            "http://test-url.test/?test=1%2C2",
        ),
    ],
)
def test_url_generation(empty_restclient, provided, expected):
    assert empty_restclient.Request(**provided).url == expected


class MockPreparedRequests:
    """ Mock Prepared Requests Object """

    status_code: int = 404
    url: str = "http://test-url.test/"


def prepared_request_patch(*args, status_code=404, **kwargs):
    def wrap(*args, status_code=status_code, **kwargs):
        mocker_object = MockPreparedRequests()
        mocker_object.status_code = status_code
        return mocker_object

    return wrap


@pytest.mark.parametrize("status_code", [200, 201])
def test_get_request(empty_restclient, monkeypatch, status_code):
    import requests

    monkeypatch.setattr(
        requests.Session, "send", prepared_request_patch(status_code=status_code)
    )

    assert empty_restclient.Get(None).status_code == status_code


@pytest.mark.parametrize("status_code", [304, 400, 403, 404, 500, 503])
def test_get_request_exceptions(empty_restclient, monkeypatch, status_code):
    """ Verify that requests.exceptions.ConnectionError is raised """
    import requests

    with pytest.raises(requests.exceptions.ConnectionError):
        req = requests.Request("GET", "http://test-url.test/")

        monkeypatch.setattr(
            requests.Session, "send", prepared_request_patch(status_code=status_code)
        )
        empty_restclient.Get(req)

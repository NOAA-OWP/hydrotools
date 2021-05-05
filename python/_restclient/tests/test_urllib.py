#!/usr/bin/env python3
import pytest

from hydrotools._restclient.urllib import Url


@pytest.mark.parametrize("url", ["http://www.fake.gov", "https://www.fake.gov"])
def test_construction(url):
    inst = Url(url)
    assert repr(inst) == url
    assert inst.url == url
    assert str(inst) == url


def test_failed_construction():
    """ should fail if netloc not passed """
    url = "https://"
    with pytest.raises(ValueError):
        Url(url)


def test_implict_https_scheme():
    """ https scheme assumed if none passed at construction """
    url = "www.test.gov"
    inst = Url(url)
    assert repr(inst) == f"https://{url}"


def test_joinurl():
    url = "https://www.test.gov"
    path = "api"
    inst = Url(url)
    inst1 = inst.joinurl(path)
    inst2 = inst / path

    assert repr(inst1) == f"{url}/{path}"
    assert repr(inst2) == f"{url}/{path}"
    assert isinstance(inst1, Url)
    assert isinstance(inst2, Url)


def test_repeated_joinurl_with_truedivide():
    url = "https://www.test.gov"
    path = "api"
    inst = Url(url)

    inst1 = inst / path / path
    inst1

    assert inst1 == f"{url}/{path}/{path}"


def test_add_query():
    url = "https://www.test.gov"
    query = {"this": "that"}
    inst = Url(url)

    inst1 = inst.add(query)
    inst2 = inst + query
    inst3 = inst2 + query

    assert inst1 == f"{url}?this=that"
    assert inst2 == f"{url}?this=that"
    assert inst3 == f"{url}?this=that&this=that"

    query2 = {"n": [1, "2", 3]}
    inst4 = inst2 + query2
    assert inst4 == f"{url}?this=that&n=1&n=2&n=3"


def test_equivalency_between_quoted_url_and_unquoted_url():
    url = "https://www.test.gov/?this='12'"
    inst = Url(url)

    url2 = "https://www.test.gov/?this=%2712%27"
    inst2 = Url(url2)
    assert inst == inst2

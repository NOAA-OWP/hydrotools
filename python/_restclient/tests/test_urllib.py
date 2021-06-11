#!/usr/bin/env python3
from urllib import parse
import pytest

from hydrotools._restclient.urllib import Url, Variadic
from hydrotools._restclient.urllib_types import Quote


@pytest.mark.parametrize("url", ["http://www.fake.gov", "https://www.fake.gov"])
def test_construction(url):
    inst = Url(url)
    assert repr(inst) == f"'{url}'"
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
    assert repr(inst) == f"'https://{url}'"


def test_joinurl():
    url = "https://www.test.gov"
    path = "api"
    inst = Url(url)
    inst1 = inst.joinurl(path)
    inst2 = inst / path

    assert repr(inst1) == f"'{url}/{path}'"
    assert repr(inst2) == f"'{url}/{path}'"
    assert isinstance(inst1, Url)
    assert isinstance(inst2, Url)


def test_repeated_joinurl_with_truedivide():
    url = "https://www.test.gov"
    path = "api"
    inst = Url(url)

    inst1 = inst / path / path

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


def test_contains():
    url = "https://www.test.gov/?this='12'"
    inst = Url(url)

    assert "test" in inst


variadic_test_input = [
    [1, 2, 3],
    ["1", "2", "3"],
    [1, "2", "3"],
    [1.0, 2, 3],
    [True, False],
]

variadic_test_validation = [
    "1,2,3",
    "1,2,3",
    "1,2,3",
    "1.0,2,3",
    "True,False",
]


@pytest.mark.parametrize("values", variadic_test_input)
def test_variadic_construction(values):
    assert isinstance(Variadic(values), Variadic)


def test_variadic_is_string_subclass():
    assert isinstance(Variadic([1]), str)


@pytest.mark.parametrize(
    "values, validation", zip(variadic_test_input, variadic_test_validation)
)
def test_variadic_str_and_repr(values, validation):
    assert str(Variadic(values)) == validation
    assert repr(Variadic(values)) == repr(validation)


def test_variadic_contains():
    inst = Variadic([1])
    assert "1" in inst


def test_variadic_integration_with_url():
    validation = "http://www.google.com?key=a,b,c"
    url = Url("http://www.google.com") + {"key": Variadic(["a", "b", "c"])}

    assert url == validation


def test_construct_url_with_unquote_treatment():
    base_url = "http://www.fake.gov/"
    suffix = "?key="
    url = base_url + suffix + "a+b"
    url_with_space = base_url + suffix + "a b"
    url_with_quoted_space = base_url + suffix + "a%20b"

    inst = Url(url, quote_treatment=Quote.QUOTE)
    assert inst.url == url
    assert inst.quote_url == url_with_quoted_space

    inst2 = Url(inst, quote_treatment=Quote.QUOTE_PLUS)
    assert inst2.url == url_with_space
    assert inst2.quote_url == url

    assert inst.quote_treatment == Quote.QUOTE
    assert inst2.quote_treatment == Quote.QUOTE_PLUS


def test_safe():
    base_url = "http://www.fake.gov"
    safe = "/:"
    path = "pa:th"
    url = Url(base_url, safe=safe)
    url2 = Url(url)
    url3 = url2 / path
    url4 = url2 + {"key": "1:2"}
    url5 = url4 / path
    url6 = url2 / path + {"key": "1:2"}

    assert url._safe == safe
    assert url2._safe == safe
    assert url3._safe == safe
    assert url4._safe == safe

    assert url3.quote_url == f"{base_url}/{path}"
    assert url4.quote_url == f"{base_url}?key=1:2"
    assert url5.quote_url == f"{base_url}/{path}?key=1:2"
    assert url6.quote_url == f"{base_url}/{path}?key=1:2"


def test_safe_reinstantiate_with_new_safe():
    base_url = "http://www.test.gov"
    o = Url(base_url, safe="/:") / "te:st"
    assert o.quote_url == "http://www.test.gov/te:st"

    o2 = Url(o, safe="/")

    assert o2.quote_url == "http://www.test.gov/te%3Ast"


def test_quote_treatment():
    base_url = "http://www.fake.gov"
    path = "office of water prediction"
    params = {"key": "+12"}

    url = Url(base_url, quote_treatment=Quote.QUOTE) / path
    url2 = Url(base_url, quote_treatment=Quote.QUOTE_PLUS) / path

    assert url == url2
    assert url.quote_url != url2.quote_url

    url += params
    url2 += params

    assert url == url2
    assert url.quote_url != url2.quote_url


def test_plus():
    base_url = "http://www.fake.gov"
    params = {"key": "+12"}
    url = Url(base_url, quote_treatment=Quote.QUOTE) + params
    print(url.quote_url)


def test_quote_overide_map():
    base_url = "http://www.fake.gov"
    params = {"key": "+12"}
    quote_remap = {"+": "%2B"}
    url = Url(base_url, quote_overide_map=quote_remap) + params
    assert url.quote_url == f"{base_url}?key=%2B12"

from aiohttp import web
import pytest
from hydrotools._restclient import RestClient


@pytest.fixture
async def naked_server(aiohttp_raw_server):
    async def wrap(handler):
        server = await aiohttp_raw_server(handler)
        return server

    return wrap


@pytest.fixture
async def basic_test_server(naked_server):
    import json

    data = {"this": "is a test"}

    async def handler(request):
        return web.Response(
            status=200,
            text=json.dumps(data),
            headers=request.headers,
            content_type="application/json",
        )

    server = await naked_server(handler)

    # return server uri, data served by server
    return str(server.make_url("/")), data


@pytest.fixture
def temp_sqlite_db():
    """ Yield a temp file with suffix .sqlite """
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".sqlite") as temp_db:
        yield temp_db.name


def test_get_without_cache(basic_test_server):
    uri, data = basic_test_server
    import json

    client = RestClient(enable_cache=False)
    r = client.get(uri)

    r_json = r.json()
    r_text = r.text()
    assert r_json == data
    assert r_text == json.dumps(data)
    # needs to be explicitly closed for pytest. Each test gets it's own loop
    client.close()


def test_get_without_cache_using_context_manager(basic_test_server):
    uri, data = basic_test_server
    import json

    with RestClient(enable_cache=False) as client:
        r = client.get(uri)

        r_json = r.json()
        r_text = r.text()
        assert r_json == data
        assert r_text == json.dumps(data)


def test_get_with_cache_using_context_manager(basic_test_server, temp_sqlite_db):
    uri, data = basic_test_server
    # import tempfile

    with RestClient(
        enable_cache=True, cache_filename=temp_sqlite_db, cache_expire_after=-1
    ) as client:
        r = client.get(uri)
        r2 = client.get(uri)
        r_json = r.json()
        r2_json = r2.json()

        assert r_json == data
        assert r_json == r2_json

    import sqlite3

    with sqlite3.connect(temp_sqlite_db) as con:
        cur = con.cursor()
        response = cur.execute("SELECT * FROM responses").fetchall()

        # There should only be one response in the db
        assert len(response) == 1


def test_mget_without_cache(basic_test_server):
    uri, data = basic_test_server

    with RestClient(enable_cache=False) as client:
        rs = client.mget([uri for _ in range(10)])

        assert all([x.json() == rs[0].json() for x in rs[1:]])


def test_mget_with_cache_using_context_manager(basic_test_server, temp_sqlite_db):
    uri, data = basic_test_server

    with RestClient(
        enable_cache=True, cache_filename=temp_sqlite_db, cache_expire_after=-1
    ) as client:
        rs = client.mget([uri for _ in range(10)])
        assert all([x.json() == rs[0].json() for x in rs[1:]])

    import sqlite3

    with sqlite3.connect(temp_sqlite_db) as con:
        cur = con.cursor()
        response = cur.execute("SELECT * FROM responses").fetchall()

        # There should only be one response in the db
        assert len(response) == 1


def test_headers(basic_test_server):
    uri, _ = basic_test_server
    headers = {"some": "headers"}

    with RestClient(enable_cache=False, headers=headers) as client:
        r = client.get(uri)
        assert all(k_v_pair in r.headers.items() for k_v_pair in headers.items())


def test_get_headers_have_precedent_over_instance(basic_test_server):
    uri, _ = basic_test_server
    instance_headers = {"some": "headers"}
    method_headers = {"some": "other_header"}

    with RestClient(enable_cache=False, headers=instance_headers) as client:
        r = client.get(uri, headers=method_headers)

        # verify in key, "some", "other_header" value in headers not "headers"
        assert all(k_v_pair in r.headers.items() for k_v_pair in method_headers.items())


def test_build_url(loop):
    base_url = "http://www.test.gov/"
    query_params = {"key": "value"}
    with RestClient(enable_cache=False, loop=loop) as client:

        assert client.build_url(base_url) == base_url
        assert client.build_url(base_url, query_params) == f"{base_url}?key=value"

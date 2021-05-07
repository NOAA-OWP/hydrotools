#!/usr/bin/env python3
import pytest
from aiohttp import web

from hydrotools._restclient.async_client import ClientSession


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
            status=200, text=json.dumps(data), content_type="application/json"
        )

    server = await naked_server(handler)
    # return uri to server
    return {"data": data, "uri": server.make_url("/")}


@pytest.fixture
async def mirror_server(naked_server):
    """ query strings passed in url as serialized and returned as json content """
    import json
    from urllib import parse

    async def handler(request):
        query = parse.parse_qs(request.query_string) if request.query_string else {}

        return web.Response(
            status=200, text=json.dumps(query), content_type="application/json"
        )

    server = await naked_server(handler)

    # return uri to server
    return server.make_url("/")


async def test_get(basic_test_server):
    async with ClientSession() as client:
        async with client.get(basic_test_server["uri"]) as resp:
            assert await resp.json() == basic_test_server["data"]


def test_get_non_async(basic_test_server, loop):
    with pytest.warns(DeprecationWarning):
        # throws DeprecationWarning b.c. session not create in async func
        session = ClientSession()
        resp_coro = session.get(basic_test_server["uri"])
        resp = loop.run_until_complete(resp_coro)
        assert loop.run_until_complete(resp.json()) == basic_test_server["data"]


@pytest.fixture
async def backoff_server(naked_server):
    import json

    class context:
        data = {"this": "is a test"}
        n = 3
        called = 0

        async def handler(self, request):
            self.called += 1
            self.n -= 1
            if self.n < 1:
                status = 200
            else:
                status = 503  # retry status code

            self.data["called"] = self.called
            return web.Response(
                status=status,
                text=json.dumps(self.data),
                content_type="application/json",
            )

    server_context = context()
    server = await naked_server(server_context.handler)
    return {"uri": server.make_url("/"), "data": server_context.data}


async def test_backoff_server(backoff_server):
    async with ClientSession() as client:
        async with client.get(backoff_server["uri"]) as resp:
            data = await resp.json()
            assert data["called"] == 3  # 1 standard get, 2 backoff


async def test_backoff_server_turnoff_retry_in_init(backoff_server):
    async with ClientSession(retry=False) as client:
        async with client.get(backoff_server["uri"]) as resp:
            data = await resp.json()
            assert data["called"] == 1  # 1 standard get


async def test_backoff_server_n_retries_2_in_init(backoff_server):
    async with ClientSession(n_retries=1) as client:
        async with client.get(backoff_server["uri"]) as resp:
            data = await resp.json()
            assert data["called"] == 2  # 1 standard get, 1 backoff


def test_verify_client_session_signature():
    """Verify ClientSession signature was forged correctly. Note: does not check all
    valid params"""
    import forge

    sig = forge.fsignature(ClientSession)
    assert {"retry", "n_retries", "cache", "headers"}.issubset(set(sig.parameters))


########### Integration tests with _restclient.urllib ###########
from hydrotools._restclient.urllib import Url, Variadic


async def test_variadic_get(mirror_server):
    params = {"hey": ["there"], "this": [Variadic(["that", "the", "other"])]}

    async with ClientSession() as session:
        async with session.get(
            mirror_server,
            params=params,
        ) as req:
            assert await req.json() == params


async def test_variadic_get(mirror_server):

    params = {"hey": ["there"], "this": [Variadic(["that", "the", "other"])]}
    # mirror_server is type: yarl.URL which does not subclass str. requires cast
    url = Url(str(mirror_server)) + params

    async with ClientSession() as session:
        async with session.get(url) as req:
            assert await req.json() == params

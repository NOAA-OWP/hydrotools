"""Unit tests for the AsyncWebClient module.

This module uses pytest and pytest-aiohttp to verify the asynchronous 
request logic, retry mechanisms, and semaphore throttling of the 
AsyncWebClient.

Example:
    $ pytest test_async_web_client.py
"""
import asyncio
import time
import threading

import pytest
from aiohttp import web
from yarl import URL

from hydrotools.waterdata_client import get_all
from hydrotools.waterdata_client.async_web_client import AsyncWebClient
from hydrotools.waterdata_client.async_web_client import ResponseContentType

def create_web_application() -> web.Application:
    """Creates a mock aiohttp application for testing.

    Returns:
        A web application with JSON and binary endpoints.
    """
    async def json_handler(request: web.Request) -> web.Response:
        if request.path != "/json":
            return web.Response(status=400)
        return web.json_response({"status": "ok", "data": 123})

    async def json2_handler(request: web.Request) -> web.Response:
        if request.path != "/json2":
            return web.Response(status=400)
        return web.json_response({"status": "ok", "data": 456})

    async def binary_handler(request: web.Request) -> web.Response:
        if request.path != "/binary":
            return web.Response(status=400)
        return web.Response(body=b"binary_data", content_type="application/octet-stream")

    async def error_handler(request: web.Request) -> web.Response:
        if request.path != "/error":
            return web.Response(status=400)
        return web.Response(status=500)

    async def malformed_json_handler(request: web.Request) -> web.Response:
        if request.path != "/binary":
            return web.Response(status=400)
        return web.Response(body="{'invalid': json", content_type="application/json")

    app = web.Application()
    app.router.add_get("/json", json_handler)
    app.router.add_get("/json2", json2_handler)
    app.router.add_get("/binary", binary_handler)
    app.router.add_get("/error", error_handler)
    app.router.add_get("/malformed", malformed_json_handler)
    return app

async def test_fetch_json(aiohttp_client):
    """Tests that fetch correctly parses JSON responses.

    Args:
        aiohttp_client: The pytest-aiohttp client fixture.
    """
    mock_client = await aiohttp_client(create_web_application())
    url = URL(f"http://{mock_client.host}:{mock_client.port}/json")

    async with AsyncWebClient() as client:
        result = await client.fetch(url)
    assert result == {"status": "ok", "data": 123}

async def test_fetch_binary(aiohttp_client):
    """Tests that fetch correctly returns bytes for non-JSON content.

    Args:
        aiohttp_client: The pytest-aiohttp client fixture.
    """
    mock_client = await aiohttp_client(create_web_application())
    url = URL(f"http://{mock_client.host}:{mock_client.port}/binary")

    async with AsyncWebClient() as client:
        result = await client.fetch(url, ResponseContentType.BYTES)
    assert result == b"binary_data"

async def test_fetch_all_order(aiohttp_client) -> None:
    """Tests that fetch_all preserves the order of input URLs.

    Args:
        aiohttp_client: The pytest-aiohttp client fixture.
    """
    mock_client = await aiohttp_client(create_web_application())
    base = f"http://{mock_client.host}:{mock_client.port}"
    urls = [URL(f"{base}/json"), URL(f"{base}/json2"), URL(f"{base}/json")]

    async with AsyncWebClient() as client:
        results = await client.fetch_all(urls)

    assert len(results) == 3
    assert results[0] == {"status": "ok", "data": 123}
    assert results[1] == {"status": "ok", "data": 456}
    assert results[2] == {"status": "ok", "data": 123}

async def test_uninitialized_session_raises_error() -> None:
    """Tests that calling fetch outside of a context manager raises RuntimeError.

    Args:
        None.
    """
    client = AsyncWebClient()
    with pytest.raises(RuntimeError, match="AsyncWebClient must be used within"):
        await client.fetch(URL("https://example.com"))

async def test_retry_exhaustion_returns_none(aiohttp_client) -> None:
    """Tests that return_none_on_failure works after retries are exhausted.

    Args:
        aiohttp_client: The pytest-aiohttp client fixture.
        mock_server_app: The mock web application fixture.
    """
    mock_client = await aiohttp_client(create_web_application())
    url = URL(f"http://{mock_client.host}:{mock_client.port}/error")

    async with AsyncWebClient(max_retries=1) as client:
        result = await client.fetch(url)
    assert result is None

SYNCHRONOUS_HOST: str = "127.0.0.1"
"""Default host to use for testing sycnhronous get_all method."""

SYCHNRONOUS_PORT: int = 35683
"""Default server port to use for testing synchronous get_all method."""

def run_server(
        app: web.Application,
        host: str = SYNCHRONOUS_HOST,
        port: int = SYCHNRONOUS_PORT
    ) -> None:
    """Helper to run a server in a separate thread for testing get_all."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, host, port)
    loop.run_until_complete(site.start())
    loop.run_forever()

@pytest.fixture(scope="module")
def persistent_server():
    """Starts a mock server in a background thread that doesn't share the test loop."""
    app = create_web_application()

    thread = threading.Thread(target=run_server, args=(app,), daemon=True)
    thread.start()

    # Give the server a moment to spin up
    time.sleep(1)
    yield f"http://{SYNCHRONOUS_HOST}:{SYCHNRONOUS_PORT}"

def test_get_all_json(persistent_server) -> None:
    """Tests get_all against an independent server thread."""
    urls = [f"{persistent_server}/json", f"{persistent_server}/json"]

    results = get_all(urls, max_retries=1)

    assert results[0] == {"status": "ok", "data": 123}
    assert results[1] == {"status": "ok", "data": 123}

def test_get_all_bytes(persistent_server) -> None:
    """Tests get_all against an independent server thread."""
    urls = [f"{persistent_server}/binary", f"{persistent_server}/binary"]

    results = get_all(urls, max_retries=1, content_type=ResponseContentType.BYTES)

    assert results[0] == b"binary_data"
    assert results[1] == b"binary_data"

async def test_fetch_invalid_json(aiohttp_client):
    """Verifies that malformed JSON returns None rather than raising an error."""
    mock_client = await aiohttp_client(create_web_application())
    url = URL(f"http://{mock_client.host}:{mock_client.port}/malformed")

    async with AsyncWebClient() as client:
        result = await client.fetch(url)
    assert result is None

async def test_fetch_status_404_returns_none(aiohttp_client):
    """Verifies that 4xx errors (non-retriable) return None immediately."""
    mock_client = await aiohttp_client(create_web_application())
    url = URL(f"http://{mock_client.host}:{mock_client.port}/missing_path")

    async with AsyncWebClient() as client:
        result = await client.fetch(url)
    assert result is None

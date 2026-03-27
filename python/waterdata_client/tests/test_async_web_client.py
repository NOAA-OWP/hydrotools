"""Unit tests for the AsyncWebClient module.

This module uses pytest and pytest-aiohttp to verify the asynchronous 
request logic, retry mechanisms, and semaphore throttling of the 
AsyncWebClient.

Example:
    $ pytest test_async_web_client.py
"""
import pytest
from aiohttp import web
from yarl import URL

from hydrotools.waterdata_client import AsyncWebClient

def create_web_application() -> web.Application:
    """Creates a mock aiohttp application for testing.

    Returns:
        A web application with JSON and binary endpoints.
    """
    async def json_handler(request: web.Request) -> web.Response:
        if request.path != "/json":
            return web.Response(status=400)
        return web.json_response({"status": "ok", "data": 123})

    async def binary_handler(request: web.Request) -> web.Response:
        if request.path != "/binary":
            return web.Response(status=400)
        return web.Response(body=b"binary_data", content_type="application/octet-stream")

    async def error_handler(request: web.Request) -> web.Response:
        if request.path != "/error":
            return web.Response(status=400)
        return web.Response(status=500)

    app = web.Application()
    app.router.add_get("/json", json_handler)
    app.router.add_get("/binary", binary_handler)
    app.router.add_get("/error", error_handler)
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
        result = await client.fetch(url)
    assert result == b"binary_data"

async def test_fetch_all_order(aiohttp_client) -> None:
    """Tests that fetch_all preserves the order of input URLs.

    Args:
        aiohttp_client: The pytest-aiohttp client fixture.
    """
    mock_client = await aiohttp_client(create_web_application())
    base = f"http://{mock_client.host}:{mock_client.port}"
    urls = [URL(f"{base}/json"), URL(f"{base}/binary"), URL(f"{base}/json")]

    async with AsyncWebClient() as client:
        results = await client.fetch_all(urls)

    assert len(results) == 3
    assert results[0] == {"status": "ok", "data": 123}
    assert results[1] == b"binary_data"
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

    async with AsyncWebClient() as client:
        result = await client.fetch(url)
    assert result is None

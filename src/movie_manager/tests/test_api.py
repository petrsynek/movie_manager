import json
import time

import aiohttp
import pytest
import pytest_httpserver

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def data():
    with open("tests/data/videos.json") as f:
        data = f.read()
    return json.loads(data)


@pytest.fixture()
def serve_data(httpserver: pytest_httpserver.HTTPServer, data):
    httpserver.expect_request("/external_data").respond_with_json(data)
    # Wait for the server to fetch the data
    time.sleep(2)


@pytest.mark.asyncio
async def test_fetch_data_from_server(httpserver, serve_data):
    """
    Test that the data is fetched from the server and that
    the data is the same as the data from the server.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(httpserver.url_for("/external_data")) as resp:
            movies_data_origin = await resp.json()

    async with aiohttp.ClientSession() as session:
        async with session.get("http://movie_manager:80/api/search") as resp:
            movies_data = await resp.json()

    assert len(movies_data) == len(movies_data_origin)


@pytest.mark.asyncio
async def test_fetch_data_from_server_search_term():
    """Test that filetering by search term is working"""

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://movie_manager:80/api/search?search_term=alp"
        ) as resp:
            movies_data = await resp.json()

    assert len(movies_data) == 2


@pytest.mark.asyncio
async def test_fetch_data_from_server_ordering():
    """Test that ordering is working"""

    async with aiohttp.ClientSession() as session:
        async with session.get("http://movie_manager:80/api/search?order=true") as resp:
            movies_data_asc = await resp.json()

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://movie_manager:80/api/search?order=false"
        ) as resp:
            movies_data_desc = await resp.json()

    assert movies_data_asc[0]["name"] != movies_data_desc[0]["name"]


@pytest.mark.asyncio
async def test_fetch_data_from_server_filtering():
    """Test that using filters is working"""

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://movie_manager:80/api/search?filters={%22features%22:[%22TEST_FEATURE%22]}"  # noqa E501
        ) as resp:
            movies_data = await resp.json()

    assert len(movies_data) == 2


@pytest.mark.asyncio
async def test_provide_filters():
    """Test that the filters are provided according to data in the database"""

    async with aiohttp.ClientSession() as session:
        async with session.get("http://movie_manager:80/api/searchfields") as resp:
            filters = await resp.json()

    expected_filters = {
        "drm": ["TEST_DRM", "TEST_DRM2", "TEST_DRM3"],
        "features": ["TEST_FEATURE"],
        "source": ["TEST_SOURCE", "TEST_SOURCE2", "TEST_SOURCE3"],
    }

    assert filters == expected_filters


@pytest.mark.asyncio
async def test_fetch_movie_detail(data):
    """Test that the filters are provided according to data in the database"""

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://movie_manager:80/api/moviedetail?movie_name=Gamma"
        ) as resp:
            movie_detail = await resp.json()

    assert data[2] == movie_detail

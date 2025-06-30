import os
import pytest
import respx
from httpx import HTTPStatusError, Response

from app.services import fetch_all_swapi_resource, fetch_swapi_resource_by_url

BASE_SWAPI_URL = os.getenv("SWAPI_BASE_URL", "https://swapi.info/api")


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_swapi_resource_with_cache_and_rate_limit():
    resource = "people"
    url = f"{BASE_SWAPI_URL}/{resource}"

    # Mock first response
    respx.get(url).mock(return_value=Response(
        200,
        json={"results": [{"name": "Luke Skywalker"}]
              }
    ))

    # First call should hit the mocked HTTP endpoint and cache result
    data = await fetch_all_swapi_resource(resource)
    assert isinstance(data, list)
    assert data[0]["name"] == "Luke Skywalker"

    # Clear respx mocks to ensure next call uses cache (no HTTP request)
    respx.reset()

    # Second call returns from cache
    cached_data = await fetch_all_swapi_resource(resource)
    assert cached_data == data


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_swapi_resource_paginated_response():
    resource = "planets"
    url = f"{BASE_SWAPI_URL}/{resource}"

    # Mock a paginated response with "results" key
    respx.get(url).mock(
        return_value=Response(
            200,
            json={
                "count": 1,
                "results": [{"name": "Tatooine"}]
            }
        )
    )

    data = await fetch_all_swapi_resource(resource)
    assert isinstance(data, list)
    assert data[0]["name"] == "Tatooine"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_swapi_resource_raises_on_error():
    resource = "unicorns"  # Non-existent resource
    url = f"{BASE_SWAPI_URL}/{resource}"

    # Mock a 404 error
    respx.get(url).mock(return_value=Response(404))

    with pytest.raises(HTTPStatusError):
        await fetch_all_swapi_resource(resource)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_swapi_resource_by_url_success():
    test_url = f"{BASE_SWAPI_URL}/planets/1"
    expected_data = {"name": "Tatooine"}

    # Mock the request
    respx.get(test_url).mock(
        return_value=Response(200, json=expected_data)
    )

    result = await fetch_swapi_resource_by_url(test_url)
    assert result == expected_data
    assert result["name"] == "Tatooine"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_swapi_resource_by_url_not_found():
    test_url = f"{BASE_SWAPI_URL}/planets/9999"

    respx.get(test_url).mock(return_value=Response(404))

    result = await fetch_swapi_resource_by_url(test_url)
    assert result is None

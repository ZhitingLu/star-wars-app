import pytest
import respx
from httpx import HTTPStatusError, Response

from app.services import fetch_all_swapi_resource, fetch_swapi_resource_by_url


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_swapi_resource_list_response():
    resource = "people"
    url = f"https://swapi.info/api/{resource}"

    # Mock a response that returns a list directly
    respx.get(url).mock(
        return_value=Response(200, json=[{"name": "Luke Skywalker"}])
    )

    data = await fetch_all_swapi_resource(resource)
    assert isinstance(data, list)
    assert data[0]["name"] == "Luke Skywalker"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_swapi_resource_paginated_response():
    resource = "planets"
    url = f"https://swapi.info/api/{resource}"

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
    url = f"https://swapi.info/api/{resource}"

    # Mock a 404 error
    respx.get(url).mock(return_value=Response(404))

    with pytest.raises(HTTPStatusError):
        await fetch_all_swapi_resource(resource)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_swapi_resource_by_url_success():
    test_url = "https://swapi.info/api/planets/1"
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
    test_url = "https://swapi.info/api/planets/9999"

    respx.get(test_url).mock(return_value=Response(404))

    result = await fetch_swapi_resource_by_url(test_url)
    assert result is None

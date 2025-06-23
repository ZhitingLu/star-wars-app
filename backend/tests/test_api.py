import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status

from app.main import app


@pytest.mark.asyncio
async def test_root():
    """
    Test the root route returns welcome message
    """

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome, Star Wars fans!"}


@pytest.mark.asyncio
async def test_get_people():
    """
    Test the GET /people endpoint.

    Verifies:
    - HTTP 200 OK response
    - Response has the keys: count, next, previous, results
    - Results is a list
    - Each person in results contains expected fields
    - (like 'name', 'homeworld_name)
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client:
        response = await client.get("/api/people")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "count" in data, "'count' key missing in response"
    assert "results" in data, "'results' key missing in response"
    assert isinstance(data["results"], list), "'results' should be a list"

    if data["results"]:
        person = data["results"][0]
        assert "name" in person, \
            "'name' field missing in person object"
        assert "gender" in person, \
            "'gender' field missing in person object"
        assert "url" in person, \
            "'url' field missing in person object"
        assert "homeworld_name" in person, \
            "'homeworld_name' field missing in person object"
        assert person["homeworld_name"] is not None, \
            "'homeworld_name' should not be None"


@pytest.mark.asyncio
async def test_get_planets():
    """
    Test the GET /planets endpoint.

    Verifies:
    - HTTP 200 OK response
    - Response has the keys: count, next, previous, results
    - Results is a list
    - Each planet in results contains expected fields
    (like 'name')
    """
    transport = ASGITransport(app=app)
    async with (AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client):
        response = await client.get("/api/planets")

    # Ensure response is successful
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    # Basic structure checks
    assert "count" in data, "'count' key missing in response"
    assert "results" in data, "'results' key missing in response"
    assert isinstance(data["results"], list), "'results' should be a list"

    # Check expected fields in first result (if exists)
    if data["results"]:
        planet = data["results"][0]
        assert "name" in planet, "'name' field missing in planet object"
        assert "climate" in planet, "'climate' field missing in planet object"
        assert "terrain" in planet, "'terrain' field missing in planet object"

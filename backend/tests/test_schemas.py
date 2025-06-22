import pytest
from datetime import datetime
from pydantic import ValidationError, HttpUrl

from app.schemas import (
    Person,
    Planet,
    SortFields,
    SortOrder,
    PaginatedResponse,
)


def test_person_model_valid():
    """
    Test that a valid Person model instance can be created from correct data.
    Checks field parsing, including datetime and HttpUrl types.
    """

    data = {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.info/api/planets/1/",
        "films": ["https://swapi.info/api/films/1/"],
        "species": [],
        "vehicles": [],
        "starships": [],
        "created": "2014-12-09T13:50:51.644000Z",
        "edited": "2014-12-20T21:17:56.891000Z",
        "url": "https://swapi.info/api/people/1/",
    }

    person = Person.model_validate(data)
    assert person.name == "Luke Skywalker"
    assert isinstance(person.created, datetime)
    assert person.homeworld == HttpUrl("https://swapi.info/api/planets/1/")


def test_person_model_missing_required():
    """
    Test that validation error is raised when required fields are missing.
    'name' and 'created' are mandatory fields for Person model.
    """
    with pytest.raises(ValidationError):
        Person(name=None, created=None)


def test_planet_model_valid():
    """
    Test successful creation of a Planet model from valid data.
    Includes fields like lists (residents, films) and datetime parsing.
    """
    data = {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": ["https://swapi.info/api/people/1/"],
        "films": ["https://swapi.info/api/films/1/"],
        "created": "2014-12-09T13:50:49.641000Z",
        "edited": "2014-12-20T20:58:18.411000Z",
        "url": "https://swapi.info/api/planets/1/",
    }
    planet = Planet.model_validate(data)
    assert planet.name == "Tatooine"
    assert len(planet.residents) == 1
    assert isinstance(planet.created, datetime)


def test_sort_fields_enum():
    """
    Verify that SortFields enum accepts valid values and rejects invalid ones.
    """
    assert SortFields.name == "name"
    assert SortFields.created == "created"
    with pytest.raises(ValueError):
        SortFields("invalid_field")
        # Should raise because 'invalid_field' is not allowed


def test_sort_order_enum():
    """
    Verify that SortOrder enum only accepts 'asc' or 'desc'.
    """
    assert SortOrder.asc == "asc"
    assert SortOrder.desc == "desc"
    with pytest.raises(ValueError):
        SortOrder("upwards")  # Invalid order value


def test_paginated_response():
    """
    Test the generic PaginatedResponse model
    using Planet as the type parameter.
    Ensures the nested results are parsed correctly as Planet objects.
    """
    example_planet = {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "created": "2014-12-09T13:50:49.641000Z",
        "edited": "2014-12-20T20:58:18.411000Z",
        "url": "https://swapi.info/api/planets/1/",
        "residents": [],
        "films": [],
    }
    data = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [example_planet]
    }
    paginated = PaginatedResponse[Planet].model_validate(data)
    assert paginated.count == 1
    assert len(paginated.results) == 1
    assert paginated.results[0].name == "Tatooine"

# Pydantic models (documented)

from datetime import datetime
from enum import Enum
from typing import Optional, List, TypeVar, Generic

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl)

# ----------------------------------------
# Generic type used for PaginatedResponse
# ----------------------------------------
T = TypeVar("T")


# ----------------------------------------
# Enum for sorting fields and order
# used to validate and restrict input values for sorting
# ----------------------------------------
class SortFields(str, Enum):
    """Allowed fields to sort by."""
    name = "name"
    created = "created"


class SortOrder(str, Enum):
    """Sort order: ascending or descending."""
    asc = "asc"
    desc = "desc"


# ----------------------------------------
# Person model for the /people endpoint
# ----------------------------------------
class Person(BaseModel):
    """
    Represents a person from the Star Wars universe.
    Matches the SWAPI /people data structure.
    """
    name: str = Field(
        ...,
        description="Name of the person")
    height: Optional[str] = Field(
        None,
        description="Height in centimeters")
    mass: Optional[str] = Field(
        None,
        description="Mass in kilograms")
    hair_color: Optional[str] = Field(
        None,
        description="Hair color")
    skin_color: Optional[str] = Field(
        None,
        description="Skin color")
    eye_color: Optional[str] = Field(
        None,
        description="Eye color")
    birth_year: Optional[str] = Field(
        None,
        description="Birth year")
    gender: Optional[str] = Field(
        None,
        description="Gender identity")
    homeworld: Optional[HttpUrl] = Field(
        None,
        description="URL of the person's homeworld (internal use)"
    )
    homeworld_name: Optional[str] = Field(
        None,
        description="Name of the person's homeworld planet"
    )
    films: List[HttpUrl] = Field(
        default_factory=list,
        description="List of film URLs")
    species: List[HttpUrl] = Field(
        default_factory=list,
        description="List of species URLs")
    vehicles: List[HttpUrl] = Field(
        default_factory=list,
        description="List of vehicle URLs")
    starships: List[HttpUrl] = Field(
        default_factory=list,
        description="List of starship URLs")

    created: datetime = Field(
        ..., description="Record creation timestamp")
    edited: Optional[datetime] = Field(
        None,
        description="Last edited timestamp")
    url: Optional[HttpUrl] = Field(
        None,
        description="Canonical URL of this resource")

    model_config = ConfigDict(from_attributes=True)
    # Enables compatibility with ORM objects (optional)


# ----------------------------------------
# Planet model for the /planets endpoint
# ----------------------------------------
class Planet(BaseModel):
    """
    Represents a planet object as returned by the SWAPI.
    Matches the SWAPI /planets data structure.
    """
    name: str = Field(..., description="Name of the planet")
    rotation_period: Optional[str] = Field(
        None,
        description="Rotation period in hours")
    orbital_period: Optional[str] = Field(
        None,
        description="Orbital period in days")
    diameter: Optional[str] = Field(
        None,
        description="Diameter in kilometers")
    climate: Optional[str] = Field(
        None,
        description="Climate type(s)")
    gravity: Optional[str] = Field(
        None,
        description="Gravity level")
    terrain: Optional[str] = Field(
        None,
        description="Terrain type(s)")
    surface_water: Optional[str] = Field(
        None,
        description="Percentage of surface water")
    population: Optional[str] = Field(
        None,
        description="Population count")
    residents: List[HttpUrl] = Field(
        default_factory=list,
        description="List of URLs to resident people")
    films: List[HttpUrl] = Field(
        default_factory=list,
        description="List of URLs to films featuring the planet")
    created: datetime = Field(
        ...,
        description="Record creation timestamp")
    edited: Optional[datetime] = Field(
        None,
        description="Last edited timestamp")
    url: Optional[HttpUrl] = Field(
        None,
        description="Canonical URL of this planet resource")

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------
# Generic paginated response model
# ----------------------------------------
class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic model for paginated API responses.

    Attributes:
        count: Total number of items available.
        next: URL to the next page of results, if any.
        previous: URL to the previous page of results, if any.
        results: List of items on the current page.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 60,
                "next": "https://swapi.info/api/planets?page=2",
                "previous": None,
                "results": [{
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
                    "url": "https://swapi.info/api/planets/1",
                    "residents": [
                        "https://swapi.info/api/people/1",
                        "https://swapi.info/api/people/2"
                    ],
                    "films": [
                        "https://swapi.info/api/films/1"
                    ]
                }],  # planet model sample
            }
        }
    )

    count: int = Field(
        ..., description="Total items count")
    next: Optional[str] = Field(
        None,
        description="URL for the next page of results")
    previous: Optional[str] = Field(
        None,
        description="URL for the previous page of results")
    results: List[T] = Field(
        ...,
        description="List of results for the current page")

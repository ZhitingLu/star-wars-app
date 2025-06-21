# Pydantic models (documented)
# This module defines Pydantic models for the Star Wars API (SWAPI) data structures.

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import Optional, List, TypeVar, Generic
from enum import Enum
from datetime import datetime

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
    name = str = Field(..., description="Name of the person")
    height: Optional[str] = None
    mass: Optional[str] = None
    hair_color: Optional[str] = None
    skin_color: Optional[str] = None
    eye_color: Optional[str] = None
    birth_year: Optional[str] = None
    gender: Optional[str] = None
    created: datetime = Field(..., description="Record creation timestamp")
    
    class Config:
        orm_mode = True # Enables compatibility with ORM objects (optional)
    
# ----------------------------------------
# Planet model for the /planets endpoint
# ----------------------------------------
class Planet(BaseModel):
    """
    Represents a planet object as returned by the SWAPI.
    Matches the SWAPI /planets data structure.
    """
    name: str = Field(..., description="Name of the planet")
    rotation_period: Optional[str] = None
    orbital_period: Optional[str] = None
    diameter: Optional[str] = None
    climate: Optional[str] = None
    gravity: Optional[str] = None
    terrain: Optional[str] = None
    surface_water: Optional[str] = None
    population: Optional[str] = None
    created: datetime = Field(..., description="Record creation timestamp")
    
    class Config:
        orm_mode = True

# ----------------------------------------
# Generic paginated response model
# ----------------------------------------
class PaginatedResponse(GenericModel, Generic[T]):
    """
    Generic model for paginated API responses.
    
    Attributes:
        count: Total number of items available.
        next: URL to the next page of results, if any.
        previous: URL to the previous page of results, if any.
        results: List of items on the current page.
    """
    count: int = Field(..., description="Total items count")
    next: Optional[str] = Field(None, description="URL for the next page of results")
    previous: Optional[str] = Field(None, description="URL for the previous page of results")
    results: List[T] = Field(..., description="List of results for the current page")
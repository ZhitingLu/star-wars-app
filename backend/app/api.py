# API router, endpoints

import asyncio
from typing import Optional
import app.services as services

from app.schemas import (
    PaginatedResponse,
    Person,
    Planet,
    SortFields,
    SortOrder)

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
async def read_root():
    """
    Root route for health check or welcome message.
    """
    return {"message": "Welcome, Star Wars fans!"}


@router.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}


# ----------------------------------------
# Fetches a paginated, searchable, and sortable list of people from SWAPI.
# ----------------------------------------
@router.get("/people", response_model=PaginatedResponse[Person])
async def get_people(
        page: int = Query(1, ge=1),  # Page number, default 1, must be >=1
        search: Optional[str] = None,
        # Optional search query for filtering by name
        sort_by: SortFields = SortFields.name,
        order: SortOrder = SortOrder.asc,
):
    data = await services.get_filtered_sorted_paginated_items(
        resource="people",
        page=page,
        per_page=15,
        search=search,
        sort_by=sort_by.value,  # convert Enum to str
        descending=(order == SortOrder.desc),
    )

    # Extract unique homeworld URLs
    unique_homeworlds = {
        person.get("homeworld") for person in data["results"]
        if person.get("homeworld")
    }

    # Fetch each homeworld in parallel using fetch by URL service
    # This avoids fetching the same homeworld multiple times
    homeworld_map = {}
    tasks = [
        services.fetch_swapi_resource_by_url(url)
        for url in unique_homeworlds
    ]

    # Execute all fetches concurrently
    results = await asyncio.gather(*tasks)

    # Build a mapping of homeworld URL → homeworld name
    for url, result in zip(unique_homeworlds, results):
        homeworld_map[url] = result.get("name") if result else "Unknown"
    print(homeworld_map)
    # Inject the resolved homeworld name into each person
    for person in data["results"]:
        url = person.get("homeworld")
        person["homeworld_name"] = homeworld_map.get(url) or "Unknown"

    return data


@router.get("/planets", response_model=PaginatedResponse[Planet])
async def get_planets(
        page: int = Query(1, ge=1),
        search: Optional[str] = None,
        sort_by: SortFields = SortFields.name,
        order: SortOrder = SortOrder.asc,
):
    data = await services.get_filtered_sorted_paginated_items(
        resource="planets",
        page=page,
        per_page=15,
        search=search,
        sort_by=sort_by.value,
        descending=(order == SortOrder.desc),
    )
    return data


# It takes a required query parameter 'name'
# representing the person or planet to analyze.
@router.get("/simulate-ai-insight")
async def simulate_ai_insight(name: str = Query(
    ...,
    description="Person or planet name"
)):
    # This is a quick mock response for demonstration.
    fake_description = (
        f"AI Insight for '{name}': "
        "This entity exhibits fascinating characteristics "
        "and plays a pivotal role "
        "in the Star Wars universe according to our advanced simulations."
    )
    return {"name": name, "description": fake_description}

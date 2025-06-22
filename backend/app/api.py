# API router, endpoints

from typing import Optional

from app.schemas import (
    PaginatedResponse,
    Person,
    Planet,
    SortFields,
    SortOrder)
from app.services import get_filtered_sorted_paginated_items

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
async def read_root():
    """
    Root route for health check or welcome message.
    """
    return {"message": "Welcome, Star Wars fans!"}


@router.get("/api")
async def health_check():
    return {"status": "ok"}


# ----------------------------------------
# Fetches a paginated, searchable, and sortable list of people from SWAPI.
# ----------------------------------------
@router.get("/people", response_model=PaginatedResponse[Person])
async def get_people(
        page: int = Query(1, ge=1),
        search: Optional[str] = None,
        sort_by: SortFields = SortFields.name,
        order: SortOrder = SortOrder.asc,
):
    data = await get_filtered_sorted_paginated_items(
        resource="people",
        page=page,
        per_page=15,
        search=search,
        sort_by=sort_by.value,
        descending=(order == SortOrder.desc),
    )
    return data


@router.get("/planets", response_model=PaginatedResponse[Planet])
async def get_planets(
        page: int = Query(1, ge=1),
        search: Optional[str] = None,
        sort_by: SortFields = SortFields.name,
        order: SortOrder = SortOrder.asc,
):
    data = await get_filtered_sorted_paginated_items(
        resource="planets",
        page=page,
        per_page=15,
        search=search,
        sort_by=sort_by.value,
        descending=(order == SortOrder.desc),
    )
    return data

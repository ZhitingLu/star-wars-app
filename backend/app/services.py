# For business logic and external API calls

from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

BASE_SWAPI_URL = "https://swapi.info/api"


async def fetch_all_swapi_resource(resource: str) -> List[Dict[str, Any]]:
    url = f"{BASE_SWAPI_URL}/{resource}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        # If data is list, return it directly; else try "results"
        if isinstance(data, list):
            return data
        return data.get("results", [])


async def get_filtered_sorted_paginated_items(
        resource: str,
        page: int,
        per_page: int = 15,
        search: Optional[str] = None,
        sort_by: str = "name",
        descending: bool = False,
) -> Dict[str, Any]:
    # Fetch entire dataset
    all_items = await fetch_all_swapi_resource(resource)

    # Filter by search term if present
    filtered_items = filter_items_by_name(all_items, search)

    # Sort filtered items
    sorted_items = sort_items(filtered_items, sort_by, descending)

    # Paginate locally
    total_count = len(sorted_items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = sorted_items[start:end]

    # Build next/previous URLs or None
    next_page = f"/{resource}?page={page + 1}" if end < total_count else None
    prev_page = f"/{resource}?page={page - 1}" if page > 1 else None

    return {
        "count": total_count,
        "next": next_page,
        "previous": prev_page,
        "results": paginated_items,
    }


def filter_items_by_name(
        items: List[Dict[str, Any]],
        search: Optional[str]) -> List[Dict[str, Any]]:
    """
    Filters items by name with case-insensitive partial match.
    If search is None or empty, returns all items.
    """
    if not search:
        return items
    search_lower = search.lower()
    return [
        item for item in items if search_lower in item.get("name", "").lower()
    ]


def sort_items(
        items: List[Dict[str, Any]],
        sort_by: str,
        descending: bool = False,
        allowed_fields: set = {"name", "created"}  # configurable
) -> List[Dict[str, Any]]:
    """
    Sort a list of items by a given key.

    Args:
        items (List[Dict[str, Any]]): List of items to sort.
        sort_by (str): The key to sort by.
        descending (bool): Whether to sort in descending order.
        allowed_fields (set): Optional set of allowed sort fields.

    Returns:
        List[Dict[str, Any]]: Sorted list of items.

    Raises:
        ValueError: If sort_by is not in allowed_fields.

    Notes:
        - Missing keys in items are treated as empty strings..
    """
    if sort_by not in allowed_fields:
        raise ValueError(
            f"Invalid sort field: {sort_by}. "
            f"Allowed fields are: {allowed_fields}"
        )

    def get_sort_key(item: Dict[str, Any]):
        val = item.get(sort_by, "")
        # Optional: Normalize datetime strings
        # for sorting by converting to datetime
        if sort_by == "created" and isinstance(val, str):
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except Exception:
                return val  # fallback to string if parsing fails
        return val

    return sorted(items, key=get_sort_key, reverse=descending)

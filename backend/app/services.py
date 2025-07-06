# For business logic and external API calls

from datetime import datetime
import os
from typing import Any, Dict, List, Optional
from aiocache import Cache
from aiolimiter import AsyncLimiter
import httpx

# Base URL for SWAPI, can be overridden by environment variable
BASE_SWAPI_URL = os.getenv("SWAPI_BASE_URL", "https://swapi.info/api")
ALLOWED_SORT_FIELDS = {"name", "created"}

# Initialize cache and rate limiter
# Use aiocache with memory backend for local development
# In production, use Redis or another persistent cache
cache = Cache(Cache.MEMORY)  # Use Redis in production
rate_limiter = AsyncLimiter(max_rate=5, time_period=1.0)  # 5 requests/second


async def fetch_all_swapi_resource(resource: str) -> List[Dict[str, Any]]:
    url = f"{BASE_SWAPI_URL}/{resource}"

    # Try cache first
    cached = await cache.get(url)
    if cached:
        return cached

    # Wait here if we've reached the rate limit (5 requests/sec).
    # Helps prevent being blocked by SWAPI or causing server overload.
    async with rate_limiter:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                results = data
            else:
                results = data.get("results", [])

            # Cache for 1 week (7 days * 24h * 3600s)
            await cache.set(url, results, ttl=604800)
            return results


async def fetch_swapi_resource_by_url(url: str) -> Optional[Dict[str, Any]]:
    # Fetch a single resource by URL
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            json_data = response.json()
            print(f"Fetched {url}: {json_data.get('name', 'No name found')}")
            return json_data
        except httpx.HTTPStatusError as e:
            print(f"HTTP error fetching {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching {url}: {e}")
            return None


async def get_filtered_sorted_paginated_items(
        resource: str,
        page: int,  # current page number (1-based)
        per_page: int = 15,  # items per page
        search: Optional[str] = None,
        sort_by: str = "name",
        descending: bool = False,
) -> Dict[str, Any]:
    # Fetch entire dataset
    all_items = await fetch_all_swapi_resource(resource)

    # Filter by search term if present
    filtered_items = filter_items_by_name(all_items, search)

    # Sort filtered items
    # Will raise ValueError if sort_by not allowed.
    sorted_items = sort_items(filtered_items, sort_by, descending)

    # Paginate locally
    # total_count: total number of items after filtering.
    # start: starting index in the sorted list.
    total_count = len(sorted_items)
    start = (page - 1) * per_page

    # handle the case where page requested is beyond available pages gracefully
    # If start index exceeds total items, return empty results.
    # Otherwise, slice the list for current page.
    if start >= total_count:
        paginated_items = []
    else:
        paginated_items = sorted_items[start:start + per_page]

    # Helper function to build URL for given page.
    # Includes query params: page, search, sort_by, order.
    # Returns None if page out of valid range.
    # returned example: /people?page=2&search=Luke&sort_by=name&order=asc
    def build_page_url(p):
        # calculate maximum valid page number
        if p < 1 or p > (total_count + per_page - 1) // per_page:
            return None
        params = [f"page={p}"]
        if search:
            params.append(f"search={search}")
        if sort_by:
            params.append(f"sort_by={sort_by}")
        if descending:
            params.append("order=desc")
        else:
            params.append("order=asc")
        return f"/{resource}?" + "&".join(params)

    # next_page: present if more items exist ahead.
    # prev_page: present if not on first page.
    next_page = (
        build_page_url(page + 1)
        if start + per_page < total_count
        else None
    )
    prev_page = build_page_url(page - 1) if page > 1 else None

    # Return response in standard paginated format.
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
        allowed_fields: set = ALLOWED_SORT_FIELDS,  # configurable
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

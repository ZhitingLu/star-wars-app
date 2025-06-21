# For business logic and external API calls

import httpx
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

BASE_SWAPI_URL = "https://swapi.dev/api"

async def fetch_swapi_resource(resource: str, page: int =1, search: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch paginated resource from SWAPI with optional search filter.
    Supports 'people' and 'planets' as resources.

    Args:
        resource (str): The SWAPI resource to fetch (e.g., 'people', 'planets').
        page (int): The page number to retrieve.
        search (Optional[str]): Optional search query for filtering results.

    Returns:
        Dict[str, Any]: The JSON response from the SWAPI.
    """
    url = f"{BASE_SWAPI_URL}/{resource}/"
    params = {"page": page}
    
    if search:
        params["search"] = search

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()  
        return response.json()  

# ----------------------------------------
# SWAPI’s default pagination is 10 items per page
# Fetching multiple SWAPI pages lets you aggregate 15+ items server-side, 
# so the frontend always receives exactly 15 items per page
# it reduces frontend complexity, gives a consistent UX and allows
# more scalability & control,
# as you are not limited by external API pagination.
# ----------------------------------------
async def fetch_multiple_swapi_pages(
    resource: str,
    page: int,
    per_page: int = 15, # To match frontend pagination (displaying 15 items per page.)
    search: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch enough SWAPI pages to return at least `per_page` items for the requested frontend page.

    Args:
        resource (str): 'people' or 'planets'.
        page (int): Frontend page number (1-based).
        per_page (int): Number of items per frontend page (15).
        search (Optional[str]): Optional search term.

    Returns:
        Dict[str, Any]: Aggregated data with keys: count, results (list)
    """
    items_needed = page * per_page  # total items needed up to current page
    items_per_swapi_page = 10  # SWAPI returns max 10 per page
    
    # Calculate how many SWAPI pages needed to fetch to have at least `items_needed`
    swapi_pages_to_fetch = (items_needed // items_per_swapi_page) + 1
    
    tasks = [
        fetch_swapi_resource(resource, page=swapi_page, search=search)
        for swapi_page in range(1, swapi_pages_to_fetch + 1)
    ]
    
    results = await asyncio.gather(*tasks)
    
    all_items = []
    total_count = 0
    
    for res in results:
        total_count = res.get("count", total_count)  # total count is same for all pages
        all_items.extend(res.get("results", []))
    
    # Slice locally to return only the items for the requested frontend page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = all_items[start:end]
    
    return {
        "count": total_count,
        "results": paginated_items,
    }

    
    
def filter_items_by_name(items: List[Dict[str, Any]], search: Optional[str]) -> List[Dict[str, Any]]:
    """
    Filters items by name with case-insensitive partial match.
    If search is None or empty, returns all items.
    """
    if not search:
        return items
    search_lower = search.lower()
    return [item for item in items if search_lower in item.get("name", "").lower()]
    

def sort_items(
    items: List[Dict[str, Any]], 
    sort_by: str, 
    descending: bool = False, 
    allowed_fields: set = {"name", "created"} # Allowed fields are configurable
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
        raise ValueError(f"Invalid sort field: {sort_by}. Allowed fields are: {allowed_fields}")

    def get_sort_key(item: Dict[str, Any]):
        val = item.get(sort_by, "")
        # Optional: Normalize datetime strings for sorting by converting to datetime
        if sort_by == "created" and isinstance(val, str):
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except Exception:
                return val  # fallback to string if parsing fails
        return val

    return sorted(items, key=get_sort_key, reverse=descending)
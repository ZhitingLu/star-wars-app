// custom hook for managing SWAPI table data
import { useState, useEffect } from "react";

export function useSwapiTable(fetchFunction, defaultSortBy = "name") {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState(defaultSortBy);
  const [order, setOrder] = useState("asc");

  useEffect(() => {
    async function load() {
      setLoading(true);
      const minLoadingTime = 500; // ms
      const start = Date.now();

      try {
        const data = await fetchFunction({
          page,
          search: searchQuery,
          sort_by: sortBy,
          order,
        });

        // wait if request was too fast
        const elapsed = Date.now() - start;
        if (elapsed < minLoadingTime) {
          await new Promise((r) => setTimeout(r, minLoadingTime - elapsed));
        }

        setItems(data.results);
        setTotal(data.count);
      } catch (e) {
        console.error("Error fetching data", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [page, searchQuery, sortBy, order, fetchFunction]);

  const handleSearch = (query) => {
    if (query === searchQuery) return;
    setPage(1);
    setSearchQuery(query);
  };

  const handleSort = (column) => {
    if (sortBy === column) {
      setOrder(order === "asc" ? "desc" : "asc");
    } else {
      setSortBy(column);
      setOrder("asc");
    }
    setPage(1);
  };

  return {
    items,
    page,
    total,
    loading,
    searchQuery,
    sortBy,
    order,
    setPage,
    handleSearch,
    handleSort,
  };
}

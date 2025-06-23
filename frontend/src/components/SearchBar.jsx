"use client";

import React, { useState, useEffect } from "react";

export default function SearchBar({ placeholder = "Search...", onSearch, debounceTime = 300 }) {
  const [input, setInput] = useState("");
  useEffect(() => {
    const handler = setTimeout(() => {
      onSearch(input.trim());
    }, debounceTime);

    return () => {
      clearTimeout(handler);
    };
  }, [input, debounceTime, onSearch]);

  return (
    <div className="mb-4 w-full max-w-md">
      <input
        type="search"
        className="w-full rounded-md border border-gray-600 bg-gray-800 px-4 py-2 text-white placeholder-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        placeholder={placeholder}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        aria-label="Search"
      />
    </div>
  );
}

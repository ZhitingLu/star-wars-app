// lib/swapiClient.js

import { fetcher } from "./fetcher";

const BASE_API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "/api";

function makeUrl(path) {
  // If BASE_API_URL is absolute (starts with http), join directly
  if (BASE_API_URL.startsWith("http")) {
    return new URL(`${BASE_API_URL}${path}`);
  }
  // If relative, provide the browser origin as base for URL constructor
  return new URL(`${BASE_API_URL}${path}`, window.location.origin);
}

/**
 * Fetch paginated, searchable, sortable people list
 * @param {object} params - page, search, sort_by, order
 */
export async function fetchPeople(params = {}) {
  const url = makeUrl("/people");
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      url.searchParams.append(key, value);
    }
  });

  return fetcher(url.toString()); // This returns { count, next, previous, results }
}

/**
 * Fetch paginated, searchable, sortable planets list
 * @param {object} params - page, search, sort_by, order
 */
export async function fetchPlanets(params = {}) {
  const url = makeUrl("/planets");
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      url.searchParams.append(key, value);
    }
  });

  return fetcher(url.toString()); // This returns { count, next, previous, results }
}

/**
 * Fetch AI-generated insight for a person or planet by name
 * @param {string} name
 */
export async function fetchAiInsight(name) {
  if (!name) return null;
  const url = makeUrl("/simulate-ai-insight");
  url.searchParams.append("name", name);
  return fetcher(url.toString());
}

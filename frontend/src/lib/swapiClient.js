// lib/swapiClient.js

import { fetcher } from "./fetcher";

const BASE_API_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000/api";

/**
 * Fetch paginated, searchable, sortable people list
 * @param {object} params - page, search, sort_by, order
 */
export async function fetchPeople(params = {}) {
  const url = new URL(`${BASE_API_URL}/people`);

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
  const url = new URL(`${BASE_API_URL}/planets`);
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
  const url = new URL(`${BASE_API_URL}/simulate-ai-insight`);
  url.searchParams.append("name", name);
  return fetcher(url.toString());
}
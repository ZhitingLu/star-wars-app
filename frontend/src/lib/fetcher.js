// lib/fetcher.js

export async function fetcher(url, options = {}) {
  const res = await fetch(url, options);

  // Throws an error if the response is not OK.
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(
      `Fetch error: ${res.status} ${res.statusText} - ${errorText}`
    );
  }
  // Parses and returns JSON otherwise
  return res.json();
}

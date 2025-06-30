"use client";

import React, { useState } from "react";
import { fetchPlanets, fetchAiInsight } from "@/lib/swapiClient";
import Pagination from "./Pagination";
import SearchBar from "./SearchBar";
import SkeletonRow from "./SkeletonRow";
import { useSwapiTable } from "@/lib/useSwapiTable";
import { SortArrow } from "./SortArrow";
import AiInsightModal from "./AiInsightModal";

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export default function PlanetsTable() {
  const {
    items: planets,
    page,
    total,
    loading,
    searchQuery,
    sortBy,
    order,
    setPage,
    handleSearch,
    handleSort,
  } = useSwapiTable(fetchPlanets, "name");

  const getPlanetUrl = (planetUrl) => {
    // Use regex to extract the numeric ID from the personUrl
    // Matches "/people/" followed by one or more digits (\d+)
    // and either a trailing slash (/) or end of string ($)
    const idMatch = planetUrl.match(/\/planets\/(\d+)(\/|$)/);
    const id = idMatch ? idMatch[1] : null;
    return id ? `/planets/${id}.jpeg` : "/galaxy.jpg"; // fallback to default if no id
  };

  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [insightDescription, setInsightDescription] = useState("");
  const [loadingInsight, setLoadingInsight] = useState(false);

  async function handleFetchAiInsight(planetName) {
    setLoadingInsight(true);
    try {
      setInsightDescription("");
      const insight = await fetchAiInsight(planetName);
      setInsightDescription(insight.description || "No AI insight available.");

      const planet = planets.find((p) => p.name === planetName);
      setSelectedPlanet(planet);
    } catch (e) {
      console.error("Error fetching AI insight:", e);
      setInsightDescription("Failed to load AI insight.");
      setSelectedPlanet({ name: planetName, url: null });
    } finally {
      setLoadingInsight(false);
    }
  }

  return (
    <div className="bg-slate-900 py-8 max-w-7xl mx-auto sm:mx-auto sm:px-0 lg:px-8 w-full rounded">
      <div className="flex items-center justify-between border-b border-white/10 py-3">
        <h2 className="px-4 text-base font-semibold text-white sm:px-6 lg:px-8">
          Planets
        </h2>
        <div className="px-4 sm:px-6 lg:px-8">
          <SearchBar
            placeholder="Search planets by name..."
            onSearch={handleSearch}
          />
        </div>
      </div>

      <div className="overflow-x-auto w-full" style={{ minHeight: `768px` }}>
        {loading ? (
          <table className="mt-6 w-full text-left whitespace-nowrap">
            <colgroup>
              <col className="w-full sm:w-4/12" />
              <col className="lg:w-2/12" />
              <col className="lg:w-2/12" />
              <col className="lg:w-2/12" />
            </colgroup>
            <thead className="border-b border-white/10 text-sm text-white">
              <tr>
                <th className="py-2 pr-8 pl-4 font-semibold sm:pl-6 lg:pl-8">
                  Name
                </th>
                <th className="py-2 pr-4 pl-0 font-semibold">Climate</th>
                <th className="py-2 pr-4 pl-0 font-semibold">Terrain</th>
                <th
                  className="py-2 pr-6 pl-0 font-semibold text-right cursor-pointer"
                  onClick={() => handleSort("created")}
                >
                  Created{" "}
                  <SortArrow column="created" sortBy={sortBy} order={order} />
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {[...Array(15)].map((_, i) => (
                <SkeletonRow key={i} columns={4} height="h-[32px]" />
              ))}
            </tbody>
          </table>
        ) : (
          <>
            <table className="mt-6 w-full text-left whitespace-nowrap table-auto">
              <colgroup>
                <col className="w-full sm:w-4/12" />
                <col className="lg:w-2/12" />
                <col className="lg:w-2/12" />
                <col className="lg:w-2/12" />
              </colgroup>
              <thead className="border-b border-white/10 text-sm text-white">
                <tr>
                  <th
                    onClick={() => handleSort("name")}
                    className="py-2 pr-8 pl-4 font-semibold sm:pl-6 lg:pl-8 cursor-pointer"
                  >
                    Name{" "}
                    <SortArrow column="name" sortBy={sortBy} order={order} />
                  </th>
                  <th className="py-2 pr-4 pl-0 font-semibold">Climate</th>
                  <th className="py-2 pr-4 pl-0 font-semibold">Terrain</th>
                  <th
                    onClick={() => handleSort("created")}
                    className="py-2 pr-6 pl-0 font-semibold text-right cursor-pointer"
                  >
                    Created{" "}
                    <SortArrow column="created" sortBy={sortBy} order={order} />
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {planets.map((planet) => (
                  <tr
                    key={planet.url}
                    className="group lightsaber-hover transition duration-300 ease-in-out"
                  >
                    <td className="py-3 pr-8 pl-4 sm:pl-6 lg:pl-8">
                      <div className="flex items-center gap-x-4">
                        <img
                          alt={planet.name}
                          src={getPlanetUrl(planet.url)}
                          className="w-8 h-8 rounded-full bg-gray-800"
                        />
                        <div className="truncate text-sm font-medium text-white">
                          {planet.name}
                          <button
                            disabled={loadingInsight}
                            onClick={() => handleFetchAiInsight(planet.name)}
                            className="ml-2 text-xs text-blue-400 hover:underline"
                            title="Get AI Insight"
                          >
                            {loadingInsight ? "Loading..." : "AI Insight"}
                          </button>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 text-sm text-gray-300">
                      {planet.climate}
                    </td>
                    <td className="py-3 text-sm text-gray-300">
                      {planet.terrain}
                    </td>
                    <td className="py-3 pr-6 text-sm text-gray-400 text-right">
                      <time dateTime={planet.created}>
                        {new Date(planet.created).toLocaleDateString()}
                      </time>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <Pagination
              page={page}
              total={total}
              pageSize={15}
              onPageChange={setPage}
            />

            <AiInsightModal
              name={selectedPlanet?.name}
              description={insightDescription}
              onClose={() => setSelectedPlanet(null)}
            />
          </>
        )}
      </div>
    </div>
  );
}

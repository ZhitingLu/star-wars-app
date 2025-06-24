"use client";

import React from "react";
import { fetchPlanets } from "@/lib/swapiClient";
import Pagination from "./Pagination";
import SearchBar from "./SearchBar";
import SkeletonRow from "./SkeletonRow";
import { useSwapiTable } from "@/lib/useSwapiTable";
import { SortArrow } from "./SortArrow";

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

  return (
    <div className="bg-slate-900 py-8 mx-auto max-w-7xl rounded">
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

      <div style={{ minHeight: `768px` }}>
        {loading ? (
          <table className="mt-6 w-full text-left whitespace-nowrap table-auto">
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
                  <tr key={planet.url}
                  className="group lightsaber-hover transition duration-300 ease-in-out"
                  >
                    <td className="py-3 pr-8 pl-4 sm:pl-6 lg:pl-8">
                      <div className="truncate text-sm font-medium text-white">
                        {planet.name}
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
          </>
        )}
      </div>
    </div>
  );
}

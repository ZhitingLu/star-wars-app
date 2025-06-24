"use client";

import React from "react";
import { fetchPeople } from "@/lib/swapiClient";
import { useSwapiTable } from "@/lib/useSwapiTable";
import SkeletonRow from "./SkeletonRow";
import Pagination from "./Pagination";
import SearchBar from "./SearchBar";
import { SortArrow } from "./SortArrow";

export default function PeopleTable() {
  const {
    items: people,
    page,
    total,
    loading,
    searchQuery,
    sortBy,
    order,
    setPage,
    handleSearch,
    handleSort,
  } = useSwapiTable(fetchPeople, "name");

  const getAvatarUrl = (personUrl) => {
     // Use regex to extract the numeric ID from the personUrl
  // Matches "/people/" followed by one or more digits (\d+)
  // and either a trailing slash (/) or end of string ($)
    const idMatch = personUrl.match(/\/people\/(\d+)(\/|$)/);
    const id = idMatch ? idMatch[1] : null;
    return id ? `/avatars/${id}.jpeg` : "/avatars/default.jpg"; // fallback to default if no id
  };

  return (
    <div className="bg-slate-900 py-10 mx-auto max-w-7xl rounded">
      <div className="flex items-center justify-between border-b border-white/10 py-3">
        <h2 className="px-4 text-base font-semibold text-white sm:px-6 lg:px-8">
          People
        </h2>
        <div className="px-4 sm:px-6 lg:px-8">
          <SearchBar
            placeholder="Search people by name..."
            onSearch={handleSearch}
          />
        </div>
      </div>
      <div className="" style={{ minHeight: `768px` }}>
        {loading ? (
          // Show skeleton rows while loading
          <table className="mt-6 w-full text-left whitespace-nowrap table-auto">
            <colgroup>
              <col className="w-full sm:w-4/12" />
              <col className="lg:w-2/12" />
              <col className="lg:w-2/12" />
              <col className="lg:w-2/12" />
              <col className="lg:w-2/12" />
            </colgroup>
            <thead className="border-b border-white/10 text-sm text-white">
              <tr>
                <th className="py-2 pr-8 pl-4 font-semibold sm:pl-6 lg:pl-8">
                  Name
                </th>
                <th className="py-2 pr-4 pl-0 font-semibold">Birth Year</th>
                <th className="py-2 pr-4 pl-0 font-semibold">Gender</th>
                <th className="py-2 pr-4 pl-0 font-semibold">Homeworld</th>
                <th className="py-2 pr-6 pl-0 font-semibold text-right">
                  Created
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {[...Array(people.length || 15)].map((_, i) => (
                <SkeletonRow key={i} columns={5} height="h-[32px]" />
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
                  <th className="py-2 pr-4 pl-0 font-semibold">Birth Year</th>
                  <th className="py-2 pr-4 pl-0 font-semibold">Gender</th>
                  <th className="py-2 pr-4 pl-0 font-semibold">Homeworld</th>
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
                {people.map((person) => (
                  <tr key={person.url}
                  className="group lightsaber-hover transition duration-300 ease-in-out">
                    <td className="py-3 pr-8 pl-4 sm:pl-6 lg:pl-8">
                      <div className="flex items-center gap-x-4">
                        <img
                          alt={person.name}
                          src={getAvatarUrl(person.url)}
                          className="w-8 h-8 rounded-full bg-gray-800"
                        />
                        <div className="truncate text-sm font-medium text-white">
                          {person.name}
                        </div>
                      </div>
                    </td>
                    <td className="py-3 text-sm text-gray-300">
                      {person.birth_year}
                    </td>
                    <td className="py-3 text-sm capitalize text-gray-300">
                      {person.gender}
                    </td>
                    <td className="py-3 text-sm text-gray-300">
                      {person.homeworld_name}
                    </td>
                    <td className="py-3 pr-6 text-sm text-gray-400 text-right">
                      <time dateTime={person.created}>
                        {new Date(person.created).toLocaleDateString()}
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
              onPageChange={(newPage) => {
                console.log("Page changed to:", newPage);
                setPage(newPage);
              }}
            />
          </>
        )}
      </div>
    </div>
  );
}

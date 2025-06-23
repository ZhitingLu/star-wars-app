"use client";

import React, { useEffect, useState } from "react";
import { fetchPeople } from "@/lib/swapiClient";
import SkeletonRow from "./SkeletonRow";
import Pagination from "./Pagination";

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export default function PeopleTable() {
  const [people, setPeople] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPeople() {
      setLoading(true);
      try {
        const data = await fetchPeople({ page });
        setPeople(data.results);
        setTotal(data.count);
      } catch (err) {
        console.error("Error fetching people:", err);
      } finally {
        setLoading(false);
      }
    }

    loadPeople();
  }, [page]);

  return (
    <div className="bg-slate-900 py-10 mx-auto max-w-7xl rounded">
      <h2 className="px-4 text-base font-semibold text-white sm:px-6 lg:px-8">
        People
      </h2>
      <div className="" style={{ minHeight: `768px` }}>
        {loading ? (
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
                {people.map((person) => (
                  <tr key={person.url}>
                    <td className="py-3 pr-8 pl-4 sm:pl-6 lg:pl-8">
                      <div className="flex items-center gap-x-4">
                        <img
                          alt={person.name}
                          src={person.imageUrl}
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
            {/* 
            <div className="mt-4 flex justify-between items-center">
              <button
                className="bg-gray-700 px-4 py-2 rounded text-white disabled:opacity-50"
                onClick={() => setPage((p) => p - 1)}
                disabled={!hasPrev}
              >
                Previous
              </button>
              <span>Page {page}</span>
              <button
                className="bg-gray-700 px-4 py-2 rounded text-white disabled:opacity-50"
                onClick={() => setPage((p) => p + 1)}
                disabled={!hasNext}
              >
                Next
              </button>
            </div> */}

              <Pagination
                page={page}
                total={total}
                pageSize={15} 
                onPageChange={(newPage) => setPage(newPage)}
              />
            
          </>
        )}
      </div>
    </div>
  );
}

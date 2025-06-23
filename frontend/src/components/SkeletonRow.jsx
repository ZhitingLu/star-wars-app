// components/SkeletonRow.jsx
import React from "react";

export default function SkeletonRow({ columns = 5, height = "h-[32px]" }) {
  return (
    <tr className={`border-b border-white/10`}>
      {Array.from({ length: columns }).map((_, i) => (
        <td key={i} className="py-3 pr-8 pl-4 sm:pl-6 lg:pl-8">
          <div
            className={`w-full ${height} rounded bg-gray-700 animate-[pulse_4s_ease-in-out_infinite] transition duration-300`}
          />
        </td>
      ))}
    </tr>
  );
}

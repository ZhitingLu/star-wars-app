import { BiSolidUpArrow, BiSolidDownArrow } from "react-icons/bi";

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

// Render arrow icon for sort indication
export function SortArrow({ column, sortBy, order }) {
  const isActive = sortBy === column;
  const arrowUp = <BiSolidUpArrow className={classNames("inline ml-1", isActive ? "text-white" : "text-gray-600")} />;
  const arrowDown = <BiSolidDownArrow className={classNames("inline ml-1", isActive ? "text-white" : "text-gray-600")} />;

  if (!isActive) {
    return arrowUp;
  }
  // If active column, show arrow corresponding to current order
  return order === "asc" ? arrowUp : arrowDown;
}
// This component renders the sort arrow based on the current sort state
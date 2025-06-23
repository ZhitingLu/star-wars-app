/// <reference types="vitest" />
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import HeroPage from "../components/HeroPage";


describe("HeroPage component", () => {
  it("renders the main title", () => {
    render(<HeroPage />);

    // Check if main title is in the document
    expect(screen.getByText(/Explore the Star Wars Galaxy/i)).toBeInTheDocument();

    // // Check for a navigation link
    // expect(screen.getAllByRole("link", { name: /People/i })[0]).toBeInTheDocument();
  });

//   it("opens and closes the mobile menu", () => {
//     render(<HeroPage />);

//     // Find the button that opens mobile menu (hamburger button)
//     const openButton = screen.getByRole("button", { name: /open main menu/i });
//     fireEvent.click(openButton);

//     // After clicking, the close button should appear
//     const closeButton = screen.getByRole("button", { name: /close menu/i });
//     expect(closeButton).toBeInTheDocument();

//     // Click the close button
//     fireEvent.click(closeButton);

//     // The close button should no longer be in the document
//     expect(screen.queryByRole("button", { name: /close menu/i })).not.toBeInTheDocument();
//   });
});


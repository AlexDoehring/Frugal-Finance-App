/*
Author: Drew Meyer
Date: Nov 23, 2024
File: RevenueForm.jsx
Purpose: Allow users to input and submit revenue data to the backend, updating the transactions list in the parent component.
*/

import React, { useState } from "react";

function RevenueForm({ onAddTransaction }) {
  const [category, setCategory] = useState("");
  const [amount, setAmount] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send data to the backend
      const response = await fetch("http://127.0.0.1:5000/income", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category, amount }),
      });

      if (response.ok) {
        const newRevenue = await response.json();
        onAddTransaction(newRevenue); // Update transactions in parent component
        setCategory("");
        setAmount("");
      } else {
        console.error("Failed to add revenue");
      }
    } catch (err) {
      console.error("Error adding revenue:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="revenue-form">
      <h3>Add Revenue</h3>
      <input
        type="text"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
      />
      <button type="submit">Add Revenue</button>
    </form>
  );
}

export default RevenueForm;

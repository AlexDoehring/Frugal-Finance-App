/*
Author: Drew Meyer
Date: Nov 23, 2024
File: ExpenseForm.jsx
Purpose: Allow users to input and submit expense data to the backend, updating the transactions list in the parent component.
*/

// TESTING DOES NOT WORK YET

import React, { useState } from "react";

function ExpenseForm({ onAddTransaction }) {
  const [category, setCategory] = useState("");
  const [amount, setAmount] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send data to the backend
      const response = await fetch("http://127.0.0.1:5000/expenses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category, amount }),
      });

      if (response.ok) {
        const newExpense = await response.json();
        onAddTransaction(newExpense); // Update transactions in parent component
        setCategory("");
        setAmount("");
      } else {
        console.error("Failed to add expense");
      }
    } catch (err) {
      console.error("Error adding expense:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="expense-form">
      <h3>Add Expense</h3>
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
      <button type="submit">Add Expense</button>
    </form>
  );
}

export default ExpenseForm;

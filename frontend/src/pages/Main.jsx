/*
Author: Drew Meyer
Date: Nov 20, 2024
File: Main.jsx
Purpose: Serves as the primary dashboard or landing page after a user successfully logs in.
*/

import React, { useState, useEffect } from "react";
import axios from "../axiosConfig"; // Import the configured Axios instance
import "../styles/Main.css";

function Main() {
  // Hardcoded expenses data
  const expenses = [
    {
      id: 1,
      amount: 50.0,
      category: "Food",
      date: "2024-11-01",
      description: "Groceries",
    },
    {
      id: 2,
      amount: 30.0,
      category: "Transportation",
      date: "2024-11-05",
      description: "Gas refill",
    },
    {
      id: 3,
      amount: 120.0,
      category: "Entertainment",
      date: "2024-11-10",
      description: "Concert ticket",
    },
    {
      id: 4,
      amount: 200.0,
      category: "Rent",
      date: "2024-11-15",
      description: "Monthly rent payment",
    },
  ];

  return (
    <div className="dashboard-container">
      <h1>Welcome to Frugal Finance</h1>
      <p>This is your dashboard. Here’s your expense overview:</p>

      <div className="expenses-container">
        {expenses.map((expense) => (
          <div key={expense.id} className="expense-card">
            <p>
              <strong>Category:</strong> {expense.category}
            </p>
            <p>
              <strong>Amount:</strong> ${expense.amount.toFixed(2)}
            </p>
            <p>
              <strong>Date:</strong> {expense.date}
            </p>
            {expense.description && (
              <p>
                <strong>Description:</strong> {expense.description}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Main;

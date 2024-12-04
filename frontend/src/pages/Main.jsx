import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // For navigation
import "../styles/Main.css";
import axios from "axios";

function Main() {
  const [authenticated, setAuthenticated] = useState(false); // Track authentication status
  const [loading, setLoading] = useState(true); // Track loading status
  const navigate = useNavigate(); // Navigation for redirects

  useEffect(() => {
    const verifyAuth = async () => {
      try {
        console.log("Sending request to /auth/verify...");
        const response = await axios.get("/auth/verify", { withCredentials: true });
        console.log("Response from /auth/verify:", response);
        if (response.status === 200) {
          setAuthenticated(true);
        }
      } catch (error) {
        console.error("Authentication failed:", error.response?.data || error.message);
        setAuthenticated(false);
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };
  
    verifyAuth();
  }, [navigate]);

  // Show a loading message while verifying authentication
  if (loading) {
    return <div>Loading...</div>;
  }

  // If authenticated, render the dashboard content
  if (authenticated) {
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

  // Fallback (just in case) - should not occur due to redirect
  return <div>Unauthorized</div>;
}

export default Main;

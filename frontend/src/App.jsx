/*
Author: Drew Meyer
Date: Nov 20, 2024
File: App.jsx
Purpose: Defines the main routing structure of the application, connecting each page.
*/

import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login"; // Import login functionality
import Register from "./pages/Register"; // Import new user registration functionality
import ForgotPassword from "./pages/ForgotPassword";
import Main from "./pages/Main";
import ProtectedRoute from "./components/ProtectedRoute"; // Import the ProtectedRoute component
import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Check authentication status on app load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get("/auth/verify", { withCredentials: true });
        if (response.status === 200) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error("Failed to verify authentication:", error.response?.data || error.message);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Routes>
      {/* Redirect root to /login */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route
        path="/main"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <Main />
          </ProtectedRoute>
        }
      />
      {/* Fallback route for undefined paths */}
      <Route path="*" element={<div>404 - Page Not Found</div>} />
    </Routes>
  );
}

export default App;

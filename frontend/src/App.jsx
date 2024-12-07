/*
Author: Drew Meyer
Date: Nov 20, 2024
File: App.jsx
Purpose: Defines the main routing structure of the application, connecting each page.
*/

import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login"; // Import login functionality
import Register from "./pages/Register"; // Import new user registration functionality
import ForgotPassword from "./pages/ForgotPassword"; // Placeholder for the forgot password page
import Main from "./pages/Main"; // Placeholder for the main page

function App() {
  return (
    <Routes>
      {/* Redirect root to /login */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/main" element={<Main />} />
      {/* Fallback route for undefined paths */}
      <Route path="*" element={<div>404 - Page Not Found</div>} />
    </Routes>
  );
}

export default App;

/*
Author: Drew Meyer
Date: Nov 20, 2024
File: App.jsx
Purpose: Defines the main routing structure of the application, connecting each page.
*/

import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login"; // Import login functionality
import Register from "./pages/Register";  // Import new user registration functionality
import ForgotPassword from "./pages/ForgotPassword"; // Placeholder for the forgot password page
import Main from "./pages/Main"; // Placeholder for the main page

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/main" element={<Main />} />
    </Routes>
  );
}

export default App;

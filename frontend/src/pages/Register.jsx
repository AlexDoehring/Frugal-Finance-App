/*
Author: Drew Meyer
Date: Nov 21, 2024
File: Register.jsx
Purpose: Displays a page for users to create a new account and integrates with the backend /register route.
*/

import React, { useState } from "react";
import "../styles/Register.css"; // Import the CSS file

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Reset error state
    setSuccess(null); // Reset success state

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess("User registered successfully!"); // Display success message
        setUsername(""); // Clear form inputs
        setEmail("");
        setPassword("");
      } else {
        setError(data.error || "Failed to register user."); // Display error message
      }
    } catch (err) {
      console.error("Error registering user:", err);
      setError("An unexpected error occurred. Please try again later.");
    }
  };

  return (
    <div className="register-container">
      <div className="register-header">
        <h1>Register New User</h1>
      </div>
      <form className="register-form" onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
      {success && <p style={{ color: "green" }}>{success}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Register;

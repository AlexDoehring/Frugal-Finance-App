import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";      // import css file
import Logo from "../assets/black_logo.svg"  // import svg logo

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message);
        navigate("/main");
      } else {
        setError(data.error || "Login failed. Please try again.");
      }
    } catch (err) {
      console.error("Error logging in:", err);
      setError("An error occurred. Please try again later.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-header">
        <h1 className="app-name">Frugal</h1>
        <img src={Logo} alt="Frugal Logo" className="login-logo" />
      </div>
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
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
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
        {error && <p style={{ color: "var(--dark-grey)" }}>{error}</p>}
        <div style={{ marginTop: "1rem" }}>
          <button
            onClick={() => navigate("/register")}
            className="secondary-button"
          >
            Register
          </button>
          <button
            onClick={() => navigate("/forgot-password")}
            className="secondary-button"
          >
            Forgot Password
          </button>
        </div>
      </form>
    </div>
  );
}

export default Login;
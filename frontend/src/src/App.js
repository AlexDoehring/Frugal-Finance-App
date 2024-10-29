import React, { useState } from 'react';
import axios from 'axios';
import ExpenseTracker from './ExpenseTracker';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track login status

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://127.0.0.1:5000/login',
        {
          username: formData.username,
          password: formData.password
        },
        { withCredentials: true } // Include credentials in the login request
      );

      if (response.status === 200) {
        setIsLoggedIn(true); // Set login status to true if authentication is successful
        console.log('Login successful');
      } else {
        alert('Invalid credentials');
      }
    } catch (error) {
      console.error('Error logging in:', error);
      alert('Login failed');
    }
  };

  return (
    <div className="App" style={{ fontFamily: 'Arial, sans-serif', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#E9EED9' }}>
      {isLoggedIn ? (
        <ExpenseTracker /> // Render ExpenseTracker if logged in
      ) : (
        <div className="login-form" style={{ background: '#CBD2A4', padding: '40px', borderRadius: '15px', boxShadow: '0 2px 4px rgba(0,0,0,0.2)', textAlign: 'center' }}>
          <h1 style={{ color: '#9A7E6F', marginBottom: '10px' }}>Frugal</h1>
          <p style={{ color: '#54473F', marginBottom: '30px' }}>The best expense tracker available. Be Frugal.</p>
          <form onSubmit={handleSubmit}>
            <div className="form-group" style={{ marginBottom: '20px' }}>
              <label htmlFor="username" style={{ display: 'block', marginBottom: '5px', color: '#54473F', fontWeight: 'bold' }}>Username:</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                required
                style={{ width: '100%', padding: '10px', border: '1px solid #9A7E6F', borderRadius: '10px', boxSizing: 'border-box' }}
              />
            </div>

            <div className="form-group" style={{ marginBottom: '20px' }}>
              <label htmlFor="password" style={{ display: 'block', marginBottom: '5px', color: '#54473F', fontWeight: 'bold' }}>Password:</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                required
                style={{ width: '100%', padding: '10px', border: '1px solid #9A7E6F', borderRadius: '10px', boxSizing: 'border-box' }}
              />
            </div>

            <button type="submit" style={{ backgroundColor: '#54473F', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '10px', cursor: 'pointer', fontSize: '16px' }}>Login</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;

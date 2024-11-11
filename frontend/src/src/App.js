// Import React and necessary modules
import React, { useState } from 'react';
import axios from 'axios';
import ExpenseTracker from './ExpenseTracker';
import './App.css';

/**
 * App Component
 * 
 * This component manages the login functionality and, upon successful login, 
 * renders the `ExpenseTracker` component for tracking expenses.
 * 
 * State:
 * - `formData`: Holds the login form input values (username and password).
 * - `isLoggedIn`: Boolean to track the user's login status.
 * 
 * Functions:
 * - `handleInputChange`: Updates `formData` state with user input for login form fields.
 * - `handleSubmit`: Sends login credentials to the backend for authentication and sets 
 *    login status upon successful authentication.
 */

function App() {
  // State to manage form data and login status
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track login status
  const [registerMode, setRegisterMode] = useState(false);

  /**
   * handleInputChange
   * Updates the `formData` state with the user input.
   * 
   * @param {Object} e - The event object from the input change
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  /**
   * handleSubmit
   * Handles form submission for login. Sends a POST request to the backend API with the 
   * login credentials. If successful, sets `isLoggedIn` to true.
   * 
   * @param {Object} e - The event object from the form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (registerMode) {
      const response = await axios.post(
        'http://127.0.0.1:5000/register',
        {
          username: formData.username,
          password: formData.password
        },
        { withCredentials: true } // Include credentials in the login request
      );
    }

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

  /**
   * Render
   * - If the user is logged in (`isLoggedIn` is true), the `ExpenseTracker` component 
   *   is rendered for managing expenses.
   * - If the user is not logged in, the login form is displayed.
   */
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
            <div>
            <label for="register">register</label><br></br>
            <input type="checkbox" id="register" onChange={() => setRegisterMode(!registerMode)}/>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;

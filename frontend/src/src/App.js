import React, { useState, useEffect } from 'react';
import './App.css';
import LoginPage from './LoginPage';
import ExpenseTracker from './ExpenseTracker';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = (username, password) => {
    // Placeholder logic for login validation
    if (username === 'user' && password === 'password') {
      setIsLoggedIn(true);
    } else {
      alert('Invalid credentials');
    }
  };

  return (
    <div className="App">
      {isLoggedIn ? <ExpenseTracker /> : <LoginPage onLogin={handleLogin} />}
    </div>
  );
}

export default App;
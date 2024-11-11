// Import React components
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// ExpenseTracker Component
function ExpenseTracker() {
  const [expenses, setExpenses] = useState([]);       // Store array of expense objects from backend
  const [income, setIncome] = useState([]);           // Store array of income objects from backend
  const [view, setView] = useState('expenses');       // Track whether to show 'expenses' or 'income'
  const [formData, setFormData] = useState({          // Track input values in the form
    amount: '',
    category: '',
    description: ''
  });

  // Fetch expenses or income based on current view
  useEffect(() => {
    const fetchData = async () => {
      try {
        const endpoint = view === 'expenses' ? 'expenses' : 'income';
        const response = await axios.get(`http://127.0.0.1:5000/${endpoint}`, { withCredentials: true });
        if (view === 'expenses') {
          setExpenses(response.data[endpoint]);
        } else {
          setIncome(response.data[endpoint]);
        }
      } catch (error) {
        console.error(`Error fetching ${view}:`, error.response ? error.response.data : error.message);
      }
    };

    fetchData();
  }, [view]); // Re-run effect when 'view' changes

  // Handles change in input fields
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handles form submission to add a new expense or income
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Prepare new entry object
    const newEntry = {
      amount: parseFloat(formData.amount),
      category: formData.category,
      date: new Date().toISOString().split('T')[0], // Format to 'YYYY-MM-DD'
      description: formData.description
    };

    // Optimistically update local list
    if (view === 'expenses') {
      setExpenses(prevExpenses => [...prevExpenses, { id: Date.now(), ...newEntry }]);
    } else {
      setIncome(prevIncome => [...prevIncome, { id: Date.now(), ...newEntry }]);
    }
    setFormData({ amount: '', category: '', description: '' }); // Reset form data

    // Send new data to the backend
    try {
      const endpoint = view === 'expenses' ? 'expenses' : 'income';
      const response = await axios.post(`http://127.0.0.1:5000/${endpoint}`, newEntry, { withCredentials: true });
      console.log(`${view.charAt(0).toUpperCase() + view.slice(1)} added to backend successfully:`, response.data);
      // Optionally refresh the list or update state with response data
    } catch (error) {
      console.error(`Error adding ${view} to backend:`, error.response ? error.response.data : error.message);
      // Optionally revert optimistic update if POST fails
      if (view === 'expenses') {
        setExpenses(prevExpenses => prevExpenses.filter(entry => entry.id !== newEntry.id));
      } else {
        setIncome(prevIncome => prevIncome.filter(entry => entry.id !== newEntry.id));
      }
    }
  };

  // Handle view switch between expenses and income
  const handleViewSwitch = (newView) => {
    setView(newView);
  };

  return (
    <div className="expense-tracker">
      <div className="view-switch">
        <button
          className={view === 'expenses' ? 'active' : ''}
          onClick={() => handleViewSwitch('expenses')}
        >
          Expenses
        </button>
        <button
          className={view === 'income' ? 'active' : ''}
          onClick={() => handleViewSwitch('income')}
        >
          Income
        </button>
      </div>

      <div className="expense-form">
        <h2>Add New {view === 'expenses' ? 'Expense' : 'Income'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="amount">Amount ($)</label>
            <input
              type="number"
              id="amount"
              name="amount"
              step="0.01"
              value={formData.amount}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">Category</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              required
            >
              <option value="">Select a category</option>
              {view === 'expenses' ? (
                <>
                  <option value="food">Food</option>
                  <option value="transportation">Transportation</option>
                  <option value="utilities">Utilities</option>
                  <option value="entertainment">Entertainment</option>
                  <option value="other">Other</option>
                </>
              ) : (
                <>
                  <option value="salary">Salary</option>
                  <option value="freelance">Freelance</option>
                  <option value="investments">Investments</option>
                  <option value="gifts">Gifts</option>
                  <option value="other">Other</option>
                </>
              )}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <input
              type="text"
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              required
            />
          </div>

          <button type="submit">Add {view === 'expenses' ? 'Expense' : 'Income'}</button>
        </form>
      </div>

      <div className="expense-list">
        <h3>Recent {view === 'expenses' ? 'Expenses' : 'Income'}</h3>
        {(view === 'expenses' ? expenses : income).map(entry => (
          <div key={entry.id} className="expense-item">
            <strong>${entry.amount.toFixed(2)}</strong> - {entry.category} <br />
            {entry.description} <br />
            <small>{new Date(entry.date).toLocaleDateString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ExpenseTracker;

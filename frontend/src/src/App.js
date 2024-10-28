import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [expenses, setExpenses] = useState([]);
  const [formData, setFormData] = useState({
    amount: '',
    category: '',
    description: ''
  });

  useEffect(() => {
    // Load expenses from local storage on initial render
    const storedExpenses = JSON.parse(localStorage.getItem('expenses') || '[]');
    setExpenses(storedExpenses);
  }, []);

  useEffect(() => {
    // Store expenses in local storage whenever they change
    localStorage.setItem('expenses', JSON.stringify(expenses));
  }, [expenses]);

  const handleInputChange = (e) => {
    // Handle changes to form input fields
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    // Handle form submission
    e.preventDefault();
    const newExpense = {
      id: Date.now(), // Generate a unique ID based on the current timestamp
      amount: parseFloat(formData.amount), // Convert amount to a floating point number
      category: formData.category,
      date: new Date().toISOString().split('T')[0], // Format the current date as YYYY-MM-DD
      description: formData.description
    };
    setExpenses([...expenses, newExpense]); // Add the new expense to the existing list
    setFormData({ amount: '', category: '', description: '' }); // Reset the form fields
  };

  return (
    <div className="App">
      <div className="expense-form">
        <h2>Add New Expense</h2>
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
              <option value="food">Food</option>
              <option value="transportation">Transportation</option>
              <option value="utilities">Utilities</option>
              <option value="entertainment">Entertainment</option>
              <option value="other">Other</option>
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

          <button type="submit">Add Expense</button>
        </form>
      </div>

      <div className="expense-list">
        <h3>Recent Expenses</h3>
        {expenses.map(expense => (
          <div key={expense.id} className="expense-item">
            <strong>${expense.amount.toFixed(2)}</strong> - {expense.category} <br />
            {expense.description} <br />
            <small>{new Date(expense.date).toLocaleDateString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
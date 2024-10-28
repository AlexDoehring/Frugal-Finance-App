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
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newExpense = {
      id: Date.now(),
      amount: parseFloat(formData.amount),
      category: formData.category,
      date: new Date().toISOString().split('T')[0],
      description: formData.description
    };
    setExpenses([...expenses, newExpense]);
    setFormData({ amount: '', category: '', description: '' });
  };

  return (
    <div className="App" style={{ fontFamily: 'Arial, sans-serif', maxWidth: '100%', margin: '40px auto', padding: '0 20px', backgroundColor: '#E9EED9' }}>
      <div className="expense-form" style={{ background: '#CBD2A4', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', width: '100%' }}>
        <h2 style={{ color: 'white' }}>Add New Expense</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group" style={{ marginBottom: '15px' }}>
            <label htmlFor="amount" style={{ display: 'block', marginBottom: '5px', color: '#54473F', fontWeight: 'bold' }}>Amount ($)</label>
            <input
              type="number"
              id="amount"
              name="amount"
              step="0.01"
              value={formData.amount}
              onChange={handleInputChange}
              required
              style={{ width: '100%', padding: '8px', border: '1px solid #9A7E6F', borderRadius: '4px', boxSizing: 'border-box' }}
            />
          </div>

          <div className="form-group" style={{ marginBottom: '15px' }}>
            <label htmlFor="category" style={{ display: 'block', marginBottom: '5px', color: '#54473F', fontWeight: 'bold' }}>Category</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              required
              style={{ width: '100%', padding: '8px', border: '1px solid #9A7E6F', borderRadius: '4px', boxSizing: 'border-box' }}
            >
              <option value="">Select a category</option>
              <option value="food">Food</option>
              <option value="transportation">Transportation</option>
              <option value="utilities">Utilities</option>
              <option value="entertainment">Entertainment</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="form-group" style={{ marginBottom: '15px' }}>
            <label htmlFor="description" style={{ display: 'block', marginBottom: '5px', color: '#54473F', fontWeight: 'bold' }}>Description</label>
            <input
              type="text"
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              required
              style={{ width: '100%', padding: '8px', border: '1px solid #9A7E6F', borderRadius: '4px', boxSizing: 'border-box' }}
            />
          </div>

          <button type="submit" style={{ backgroundColor: '#54473F', color: 'white', padding: '10px 15px', border: 'none', borderRadius: '4px', cursor: 'pointer', width: '100%', fontSize: '16px' }}>Add Expense</button>
        </form>
      </div>

      <div className="expense-list" style={{ marginTop: '20px' }}>
        <h3 style={{ color: '#54473F' }}>Recent Expenses</h3>
        {expenses.map(expense => (
          <div key={expense.id} style={{ background: '#CBD2A4', padding: '10px', margin: '10px 0', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <strong style={{ color: '#9A7E6F' }}>${expense.amount.toFixed(2)}</strong> - {expense.category} <br />
            {expense.description} <br />
            <small style={{ color: '#54473F' }}>{new Date(expense.date).toLocaleDateString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

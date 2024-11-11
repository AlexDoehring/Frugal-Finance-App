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
  const [editFormData, setEditFormData] = useState({          // Track input values in the form
    amount: '',
    category: '',
    description: ''
  });
  const [expenseCtxMenu, setExpenseCtxMenu] = useState([]);

  // Fetch expenses or income based on current view
  useEffect(() => {
    const fetchData = async () => {
      try {
        const endpoint = view === 'expenses' ? 'expenses' : 'income';
        const response = await axios.get(`http://127.0.0.1:5000/${endpoint}`, { withCredentials: true });
        if (view === 'expenses') {
          setExpenses(response.data[endpoint]);
          setExpenseCtxMenu(response.data.expenses.map(expense => {
            return {hidden: true, editMenuHidden: true};
          }));
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

  const handleEditInputChange = (e) => {
    const { name, value } = e.target;
    setEditFormData({ ...editFormData, [name]: value });
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
      setExpenseCtxMenu(prevCtx => [...prevCtx, {hidden: true, editMenuHidden: true}]);
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

  const handleEditSubmit = async (e, id, index) => {
    e.preventDefault();

    // Prepare new entry object
    const newEntry = {
      amount: parseFloat(editFormData.amount),
      category: editFormData.category,
      description: editFormData.description
    };

    

    // Send new data to the backend
    try {
      const response = await axios.put(`http://127.0.0.1:5000/expenses/${id}`, newEntry, { withCredentials: true });
      console.log(`${view.charAt(0).toUpperCase() + view.slice(1)} updated on backend successfully:`, response.data);
      // Optionally refresh the list or update state with response data
    } catch (error) {
      console.error(`Error updating ${view} to backend:`, error.response ? error.response.data : error.message);
      // Optionally revert optimistic update if POST fails
      setExpenses(prevExpenses => prevExpenses.filter(entry => entry.id !== newEntry.id));
    }

    setEditFormData({ amount: '', category: '', description: '' }); // Reset form data

    setExpenseCtxMenu(
      expenseCtxMenu.map( (ctx, idx2) => {
        if (idx2 == index) {
          return {hidden: true, editMenuHidden: true};
        }
        else {
          return {hidden: ctx.hidden, editMenuHidden: true};
        }
      })
    );
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
        <h2>Edit Expense</h2>
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
        <h3 style={{display: "flex", justifyContent: "space-between"}}>Recent Expenses 
        <button style={{width: "20%"}} 
        onClick={async () => {
            const result = await axios.get('http://127.0.0.1:5000/export_csv', { withCredentials: true });
            let a = document.createElement("a");
            var data = new Blob([result.data]);
            a.href = URL.createObjectURL(data);
            a.download = "report.csv";
            a.click();
          }}>CSV</button>
          <button style={{width: "20%"}} onClick={async () => {
            const result = await axios.get('http://127.0.0.1:5000/export_pdf', { withCredentials: true });
            let a = document.createElement("a");
            var data = new Blob([result.data]);
            a.href = URL.createObjectURL(data);
            a.download = "report.pdf";
            a.click();
          }}>PDF</button>
        </h3>
        {expenses.map((expense, index) => (
            <div key={expense.id} className="expense-item">
              <div className='ctx-menu-holder' >
                <div className='ctx-menu-btn' onClick={() => 
                  {
                  setExpenseCtxMenu(
                    expenseCtxMenu.map( (ctx, idx2) => {
                      if (idx2 == index) {
                        return {hidden: !ctx.hidden, editMenuHidden: true};
                      }
                      else {
                        return ctx;
                      }
                    })
                  );
                }
                }
                >⋮</div>
                { expenseCtxMenu[index].hidden ?
                <></>
                : 
                <div className='ctx-menu-items' >
                  <div className='ctx-menu-item' 
                    onClick={() => 
                      {
                      setExpenseCtxMenu(
                        expenseCtxMenu.map( (ctx, idx2) => {
                          if (idx2 == index) {
                            return {hidden: true, editMenuHidden: false};
                          }
                          else {
                            return {hidden: ctx.hidden, editMenuHidden: true};
                          }
                        }));
                      }
                    }>edit</div>
                  <div className='ctx-menu-item' onClick={async () =>
                    {
                      const response = await axios.delete(`http://127.0.0.1:5000/expenses/${expense.id}`, { withCredentials: true });
                      setExpenseCtxMenu(expenseCtxMenu.filter((ctx, idx) =>  idx != index ));
                      setExpenses(expenses.filter((exp, idx) =>  idx != index  ));
                    }
                  }
                  >delete</div>
                </div>
                }
              </div>
              { 
              expenseCtxMenu[index].editMenuHidden ?  
              <>
                <strong>${expense.amount.toFixed(2)}</strong> - {expense.category} <br />
                {expense.description} <br />
                <small>{new Date(expense.date).toLocaleDateString()}</small>
              </>
              : 
              <form onSubmit={(e) => handleEditSubmit(e, expense.id)}>
          <div className="form-group">
            <label htmlFor="amount">Amount ($)</label>
            <input
              type="number"
              name="amount"
              step="0.01"
              value={editFormData.amount}
              onChange={handleEditInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">Category</label>
            <select
              name="category"
              onChange={handleEditInputChange}
              value={editFormData.category}
              required
            >
              <option value=''>Select a category</option>
                <>
                  <option value="food">Food</option>
                  <option value="transportation">Transportation</option>
                  <option value="utilities">Utilities</option>
                  <option value="entertainment">Entertainment</option>
                  <option value="other">Other</option>
                </>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <input
              type="text"
              name="description"
              value={editFormData.description}
              onChange={handleEditInputChange}
              required
            />
          </div>

          <button type="submit">Save</button>
          <button onClick={() => {
            setExpenseCtxMenu(
              expenseCtxMenu.map( (ctx, idx2) => {
                if (idx2 == index) {
                  return {hidden: true, editMenuHidden: true};
                }
                else {
                  return ctx;
                }
              })
            );
          }
          }>Cancel</button>
        </form>
              }
            </div>
        ))}
      </div>
    </div>
  );
}

export default ExpenseTracker;

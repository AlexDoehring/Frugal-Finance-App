import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Main.css";
import "../styles/global.css"
import axios from "axios";
import { Table, DataType } from "ka-table";
import "ka-table/style.css";

function Main() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [expenses, setExpenses] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newExpense, setNewExpense] = useState({
    amount: "",
    category: "",
    date: "",
    description: "",
  });

  const navigate = useNavigate();

  useEffect(() => {
    const verifyAuth = async () => {
      try {
        const response = await axios.get("/auth/verify", { withCredentials: true });
        if (response.status === 200) {
          setAuthenticated(true);
          fetchExpenses();
        }
      } catch (error) {
        console.error("Authentication failed:", error.response?.data || error.message);
        setAuthenticated(false);
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    verifyAuth();
  }, [navigate]);

  const fetchExpenses = async () => {
    try {
      const response = await axios.get("/expenses", { withCredentials: true });
      setExpenses(response.data.expenses);
    } catch (error) {
      console.error("Failed to fetch expenses:", error);
    }
  };

  const handleAddExpense = async () => {
    try {
      const response = await axios.post("http://localhost:5000/expenses", newExpense, { withCredentials: true });
      if (response.status === 201) {
        fetchExpenses(); // Refresh the expense list after successful addition
        setShowModal(false); // Close the modal
        setNewExpense({ amount: "", category: "", date: "", description: "" }); // Reset the form
        alert(response.data.message); // Show success or warning message
      }
    } catch (error) {
      console.error("Failed to add expense:", error.response?.data || error.message);
      alert(error.response?.data?.error || "An error occurred while adding the expense.");
    }
  };

  const handleLogout = async () => {
    try {
      // Optional: Call a logout endpoint if you have one
      await axios.post("/auth/logout", {}, { withCredentials: true });
    } catch (error) {
      console.error("Logout failed:", error.response?.data || error.message);
    } finally {
      // Redirect to login page
      navigate("/login");
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (authenticated) {
    const tableProps = {
      columns: [
        { key: "date", title: "Date", dataType: DataType.String },
        { key: "category", title: "Category", dataType: DataType.String },
        { key: "amount", title: "Amount", dataType: DataType.Number },
        { key: "description", title: "Description", dataType: DataType.String },
        {
          key: "actions",
          title: "Actions",
          isSortable: false,
          cell: ({ rowData }) => (
            <div>
              <button onClick={() => console.log("Edit", rowData)}>Edit</button>
              <button onClick={() => console.log("Delete", rowData)}>Delete</button>
            </div>
          ),
        },
      ],
      data: expenses,
      rowKeyField: "id",
    };

    return (
      <div className="dashboard-container">
        <header className="dashboard-header">
          <h1>Welcome to Frugal Finance</h1>
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </header>
        <p>This is your dashboard. Here’s your expense overview:</p>
        <button onClick={() => setShowModal(true)}>Add Expense</button>
        <Table {...tableProps} />

        {/* Modal for Adding Expense */}
        {showModal && (
          <div className="modal">
            <div className="modal-content">
              <h2>Add Expense</h2>
              <form
                onSubmit={(e) => {
                  e.preventDefault(); // Prevent page reload
                  handleAddExpense(); // Call the function to send the data
                }}
              >
                <label>
                  Amount:
                  <input
                    type="number"
                    step="0.01"
                    value={newExpense.amount}
                    onChange={(e) => setNewExpense({ ...newExpense, amount: e.target.value })}
                    required
                  />
                </label>
                <label>
                  Category:
                  <input
                    type="text"
                    value={newExpense.category}
                    onChange={(e) => setNewExpense({ ...newExpense, category: e.target.value })}
                    required
                  />
                </label>
                <label>
                  Date:
                  <input
                    type="date"
                    value={newExpense.date}
                    onChange={(e) => setNewExpense({ ...newExpense, date: e.target.value })}
                    required
                  />
                </label>
                <label>
                  Description:
                  <textarea
                    value={newExpense.description}
                    onChange={(e) => setNewExpense({ ...newExpense, description: e.target.value })}
                  />
                </label>
                <button type="submit">Add Expense</button>
                <button type="button" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    );
  }

  return <div>Unauthorized</div>;
}

export default Main;

import React from 'react';
import Header from './components/Header';
import ExpenseList from './components/ExpenseList';
import ExpenseFilter from './components/ExpenseFilter';
import './styles/main.css';

function App() {
    return (
        <div className="App">
            <Header />
            <ExpenseFilter />
            <ExpenseList />
        </div>
    );
}

export default App;

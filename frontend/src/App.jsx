// frontend/src/App.jsx

import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";  // Placeholder for the new user registration page
import ForgotPassword from "./pages/ForgotPassword"; // Placeholder for the forgot password page
import Main from "./pages/Main"; // Placeholder for the main page

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/main" element={<Main />} />
    </Routes>
  );
}

export default App;

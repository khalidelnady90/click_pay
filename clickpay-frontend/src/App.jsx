import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from 'react';
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<h1 className="text-2xl text-center mt-10">مرحبًا بك في Click Pay 👋</h1>} />
      </Routes>
    </Router>
  );
}

export default App;

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Account from './pages/Account';
import SmartContract from './pages/SmartContract';
import Whitepaper from './pages/Whitepaper';
import Tutorial from './pages/Tutorial';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container bg-gray-900 text-white min-h-screen">
        <Header />
        <main className="container mx-auto px-4 py-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/account" element={<Account />} />
            <Route path="/smart-contract" element={<SmartContract />} />
            <Route path="/whitepaper" element={<Whitepaper />} />
            <Route path="/tutorial" element={<Tutorial />} />
          </Routes>
        </main>
        <footer className="text-center py-4 text-gray-500 text-sm">
          © 2025 Sodh Explorer - A Solana Blockchain Explorer
        </footer>
      </div>
    </Router>
  );
}

export default App;
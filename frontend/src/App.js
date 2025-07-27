// /src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Suppliers from './pages/Suppliers';
import Orders from './pages/Orders';
import Inventory from './pages/Inventory';
import Help from './pages/Help';
import SupplierDetail from "./pages/SupplierDetail";


function App() {
  return (
    <Router>
      <div className="bg-gray-50 min-h-screen">
        <Navbar />
        <div className="p-4">
          <Routes>
            {/* Home route can go to Suppliers or to a separate Home component if you create one */}
            <Route path="/" element={<Suppliers />} />

            {/* Explicit suppliers route to fix "No routes matched location '/suppliers'" */}
            <Route path="/suppliers" element={<Suppliers />} />
            
<Route path="/supplier/:id" element={<SupplierDetail />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/inventory" element={<Inventory />} />
            <Route path="/help" element={<Help />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

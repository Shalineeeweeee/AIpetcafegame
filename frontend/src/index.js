import React from 'react';
import Navbar from "./components/Navbar"; 


function Dashboard() {
  return (
    <div className="dashboard">
      <Navbar />
      <div className="dashboard-content">
        <h1>Dashboard</h1>
        <p>Welcome to your AI Pet Game Dashboard!</p>
      </div>
    </div>
  );
}

export default Dashboard;
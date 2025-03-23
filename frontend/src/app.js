import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Mainmenu from "./pages/Mainmenu";
import Login from "./pages/Login"; // Ensure file name and import match

function App() {
  return (
    <Router>
      <Routes>
        {/* Set Login as the default page */}
        <Route path="/" element={<Login />} />
        <Route path="/mainmenu" element={<Mainmenu />} />
      </Routes>
    </Router>
  );
}

export default App;
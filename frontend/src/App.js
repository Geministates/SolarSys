import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PlanetarySystem from "./components/PlanetarySystem";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<PlanetarySystem />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
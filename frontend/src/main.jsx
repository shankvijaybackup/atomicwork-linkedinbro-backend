import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx'; // ✅ correct // or './App.jsx' depending on your structure
import './index.css';
    
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

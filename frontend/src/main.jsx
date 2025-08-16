// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import { AuthProvider } from './contexts/AuthContext.js';
import { PointProvider } from './contexts/PointContext.js';
import './index.css'; // Importing global styles

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* 1. BrowserRouter enables page routing for the entire app. */}
    <BrowserRouter>
      {/* 2. AuthProvider makes user data available to all components. */}
      <AuthProvider>
        {/* 3. PointProvider makes point data available, and must be inside AuthProvider. */}
        <PointProvider>
          <App />
        </PointProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
// src/App.jsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';

// Import Layout Components
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// Import Page Components
import HomePage from './pages/HomePage';
import Marketplace from './pages/Marketplace';
import ProductView from './pages/ProductView';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardUploader from './pages/DashboardUploader';
import DashboardUpcycler from './pages/DashboardUpcycler';

// --- Protected Route Component ---
// This is a wrapper component that checks if a user is authenticated.
// If they are, it renders the requested page.
// If not, it redirects them to the login page.
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    // You can show a loading spinner here while checking auth status
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    // Redirect to the login page
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <div className="app-container">
      <Navbar />
      <main className="main-content">
        <Routes>
          {/* --- Public Routes --- */}
          <Route path="/" element={<HomePage />} />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/product/:id" element={<ProductView />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* --- Protected Routes --- */}
          <Route
            path="/dashboard-uploader"
            element={
              <ProtectedRoute>
                <DashboardUploader />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard-upcycler"
            element={
              <ProtectedRoute>
                <DashboardUpcycler />
              </ProtectedRoute>
            }
          />

          {/* A catch-all route for pages that don't exist */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
// src/components/layout/Navbar.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import logo from '../../assets/ecomorph-logo.svg';
import './Navbar.css';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/'); // Redirect to homepage after logout
  };

  return (
    <header className="navbar">
      <Link to="/" className="navbar-logo">
        <img src={logo} alt="EcoMorph Logo" />
        <span>EcoMorph</span>
      </Link>

      <nav className="navbar-links">
        <Link to="/marketplace">Marketplace</Link>
        {/* Add more general links here */}
      </nav>

      <div className="navbar-actions">
        {user ? (
          <>
            <span>Welcome, {user.email}</span>
            <Link to={user.role === 'upcycler' ? '/dashboard-upcycler' : '/dashboard-uploader'}>
              Dashboard
            </Link>
            <button onClick={handleLogout} className="logout-btn">
              Log Out
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Log In</Link>
            <Link to="/register" className="signup-btn">Sign Up</Link>
          </>
        )}
      </div>
    </header>
  );
}

export default Navbar;
// src/contexts/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import authService from '../api/authService';

// 1. Create the context
export const AuthContext = createContext(null);

// 2. Create the provider component
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // To handle initial auth check

  // Check if the user is already logged in when the app loads
  useEffect(() => {
    const checkLoggedIn = async () => {
      const token = localStorage.getItem('authToken');
      if (token) {
        try {
          // Verify the token by fetching the user's profile
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
        } catch (error) {
          // Token is invalid or expired, so log them out
          console.error("Session expired, please log in again.", error);
          authService.logout();
          setUser(null);
        }
      }
      setLoading(false);
    };

    checkLoggedIn();
  }, []);

  const login = async (email, password) => {
    try {
      await authService.login(email, password);
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
      return currentUser; // Return user on success
    } catch (error) {
      console.error('Login failed:', error);
      throw error; // Re-throw error to be handled by the login form
    }
  };

  const register = async (userData) => {
    try {
      const newUser = await authService.register(userData);
      // Optional: automatically log in the user after they register
      await login(userData.email, userData.password);
      return newUser;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  // 3. The value to be passed to consuming components
  const value = {
    user,
    isAuthenticated: !!user,
    loading,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}
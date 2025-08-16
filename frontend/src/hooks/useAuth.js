// src/hooks/useAuth.js
import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

/**
 * A custom hook for accessing the AuthContext.
 * @returns The value of the AuthContext (e.g., { user, login, logout }).
 */
export const useAuth = () => {
  return useContext(AuthContext);
};
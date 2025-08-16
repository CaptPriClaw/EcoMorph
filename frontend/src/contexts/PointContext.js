// src/contexts/PointContext.js
import React, { createContext, useState, useEffect, useCallback, useContext } from 'react';
import pointService from '../api/pointService';
import { useAuth } from '../hooks/useAuth'; // We need to know who the user is

// 1. Create the context
export const PointContext = createContext(null);

// 2. Create the provider component
export function PointProvider({ children }) {
  const [points, setPoints] = useState(0);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth(); // Get the current user from AuthContext

  // A function to fetch/refresh the point balance
  const fetchPoints = useCallback(async () => {
    if (!user) {
      setPoints(0);
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      const data = await pointService.getMyBalance();
      setPoints(data.current_balance || 0);
    } catch (error) {
      console.error("Failed to fetch points:", error);
      setPoints(0); // Reset points on error
    } finally {
      setLoading(false);
    }
  }, [user]); // This function depends on the user object

  // Automatically fetch points when the user logs in or the app loads
  useEffect(() => {
    fetchPoints();
  }, [fetchPoints]); // Run whenever fetchPoints changes (i.e., when user changes)


  // 3. The value to be passed to consuming components
  const value = {
    points,
    loading,
    refreshPoints: fetchPoints, // Expose a function to manually refresh points
  };

  return (
    <PointContext.Provider value={value}>
      {children}
    </PointContext.Provider>
  );
}

// A simple hook for easy access to the PointContext
export const usePoints = () => {
    return useContext(PointContext);
}
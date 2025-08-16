// src/api/pointService.js
import apiClient from './apiClient';

const pointService = {
  /**
   * Fetches the current authenticated user's point balance.
   * @returns {Promise<object>} An object containing the user's current balance.
   */
  getMyBalance: async () => {
    // The apiClient will automatically add the auth token.
    const response = await apiClient.get('/points/my-balance');
    return response.data;
  },

  /**
   * Fetches the current authenticated user's point transaction history.
   * @returns {Promise<Array<object>>} A list of point ledger entries.
   */
  getMyHistory: async () => {
    const response = await apiClient.get('/points/my-history');
    return response.data;
  },
};

export default pointService;
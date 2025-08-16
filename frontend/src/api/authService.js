// src/api/authService.js
import apiClient from './apiClient';

const authService = {
  /**
   * Logs in a user and stores the auth token.
   * @param {string} email The user's email.
   * @param {string} password The user's password.
   * @returns {Promise<object>} The response data from the server.
   */
  login: async (email, password) => {
    // The backend's /token endpoint expects form data, not JSON.
    // We use URLSearchParams to format the data correctly.
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    const response = await apiClient.post('/token', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    // If the login is successful, store the token in local storage.
    if (response.data.access_token) {
      localStorage.setItem('authToken', response.data.access_token);
    }
    return response.data;
  },

  /**
   * Registers a new user.
   * @param {object} userData - Contains fullName, email, and password.
   * @returns {Promise<object>} The newly created user's data.
   */
  register: async (userData) => {
    const response = await apiClient.post('/users/', userData);
    return response.data;
  },

  /**
   * Logs out the current user by removing the auth token.
   */
  logout: () => {
    localStorage.removeItem('authToken');
    // Here you would also typically clear any user state in your app.
  },

  /**
   * Gets the current user's profile from the backend.
   * Useful for verifying a token when the app loads.
   * @returns {Promise<object>} The current user's data.
   */
  getCurrentUser: async () => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },
};

export default authService;
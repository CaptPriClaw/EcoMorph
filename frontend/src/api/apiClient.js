// src/api/apiClient.js
import axios from 'axios';

// The base URL of your FastAPI backend
const API_BASE_URL = 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Request Interceptor ---
// This function will run before every single request is sent.
apiClient.interceptors.request.use(
  (config) => {
    // Get the auth token from local storage
    const token = localStorage.getItem('authToken');

    // If the token exists, add the Authorization header to the request
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    // Handle any errors that occur during the request setup
    return Promise.reject(error);
  }
);

export default apiClient;
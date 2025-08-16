// src/api/apiClient.js

const API_BASE_URL = 'http://127.0.0.1:8000'; // Your FastAPI backend URL

const request = async (endpoint, options = {}) => {
  const token = localStorage.getItem('authToken');
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'An API error occurred');
  }

  const contentType = response.headers.get("content-type");
  if (contentType && contentType.indexOf("application/json") !== -1) {
    return response.json();
  }
  return true;
};

export const authApi = {
  login: (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    return request('/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
  },
};

export const adminApi = {
  getDashboardStats: () => request('/admin/stats'), // Assumes a new endpoint
  getPendingWastes: () => request('/admin/waste/pending'), // Assumes a new endpoint
};

export const wasteApi = {
  updateStatus: (wasteId, status) => request(`/waste/${wasteId}/status`, {
    method: 'PUT',
    body: JSON.stringify({ status })
  }),
};
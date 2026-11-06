import axios from "axios";

// Create axios instance with backend API base URL from environment variables
// Base URL configured in .env file as VITE_API_URL (e.g., http://localhost:8000/api)
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Request interceptor - automatically adds JWT token to Authorization header
// Token is retrieved from localStorage where it was stored during login
// This ensures all API requests include the authentication token without manual header setting
api.interceptors.request.use((config) => {
  // Try to get JWT token from localStorage
  const token = localStorage.getItem("token");

  // If token exists, add it to Authorization header in Bearer format (OAuth2 standard)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Export configured axios instance for use in all service files
export default api;

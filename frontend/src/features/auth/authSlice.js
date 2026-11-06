import { createSlice } from "@reduxjs/toolkit";

// Initial authentication state - user not logged in
const initialState = {
  user: null, // Authenticated user object { id, email, role }
  token: null, // JWT access token for API requests
  isAuthenticated: false, // Flag indicating current authentication status
};

// Redux slice for authentication state management
// Handles login success and logout actions
const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    // Login success action - called after successful authentication
    // Stores user data and JWT token in Redux state
    loginSuccess: (state, action) => {
      state.user = action.payload.user; // Store user profile data
      state.token = action.payload.token; // Store JWT token
      state.isAuthenticated = true; // Mark user as authenticated
    },
    // Logout action - clears authentication state and removes token from storage
    // Called from Navbar logout button
    logout: (state) => {
      state.user = null; // Clear user data
      state.token = null; // Clear JWT token
      state.isAuthenticated = false; // Mark user as not authenticated
      localStorage.removeItem("token"); // Remove persisted token from localStorage
    },
  },
});

// Export action creators for use in components
export const { loginSuccess, logout } = authSlice.actions;
// Export reducer for use in Redux store
export default authSlice.reducer;

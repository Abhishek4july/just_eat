import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../features/auth/authSlice";
import cartReducer from "../features/cart/CartSlice";

// Configure and create Redux store
// Combines all reducers (auth and cart) into a single store
export const store = configureStore({
  reducer: {
    // Authentication state: user, token, isAuthenticated
    auth: authReducer,
    // Shopping cart state: items (persisted to localStorage)
    cart: cartReducer,
  },
});

import { createSlice } from "@reduxjs/toolkit";

// Redux slice for managing shopping cart state
// Cart items include restaurant_id to enforce single-restaurant restriction
const storedCart = localStorage.getItem("cart");

const initialState = {
  items: storedCart ? JSON.parse(storedCart) : [], // Restore cart from localStorage on app load
};

const cartSlice = createSlice({
  name: "cart",
  initialState,

  reducers: {
    // Add item to cart or increase quantity if already exists
    // Payload includes restaurant_id which is used to enforce single-restaurant restriction
    addToCart: (state, action) => {
      const existingItem = state.items.find(
        (item) => item.id === action.payload.id,
      );

      if (existingItem) {
        // Increase quantity if item already in cart
        existingItem.quantity += 1;
      } else {
        // Add new item with quantity 1 and restaurant_id
        state.items.push({
          ...action.payload, // Includes item data + restaurant_id
          quantity: 1,
        });
      }

      // Persist to localStorage for cart persistence across browser sessions
      localStorage.setItem("cart", JSON.stringify(state.items));
    },

    // Remove item completely from cart
    removeFromCart: (state, action) => {
      state.items = state.items.filter((item) => item.id !== action.payload);

      localStorage.setItem("cart", JSON.stringify(state.items));
    },

    // Increase quantity of an item in cart
    increaseQuantity: (state, action) => {
      const item = state.items.find((item) => item.id === action.payload);

      if (item) {
        item.quantity++;
      }

      localStorage.setItem("cart", JSON.stringify(state.items));
    },

    // Decrease quantity or remove item if quantity reaches 0
    decreaseQuantity: (state, action) => {
      const item = state.items.find((item) => item.id === action.payload);

      if (!item) return;

      if (item.quantity > 1) {
        item.quantity--;
      } else {
        // Remove item if quantity is 1 and user decreases
        state.items = state.items.filter((i) => i.id !== action.payload);
      }

      localStorage.setItem("cart", JSON.stringify(state.items));
    },

    // Clear entire cart (used after order placement)
    clearCart: (state) => {
      state.items = [];

      localStorage.setItem("cart", JSON.stringify(state.items));
    },
  },
});

export const {
  addToCart,
  removeFromCart,
  increaseQuantity,
  decreaseQuantity,
  clearCart,
} = cartSlice.actions;

export default cartSlice.reducer;

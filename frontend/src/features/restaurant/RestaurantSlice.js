import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { getRestaurants } from "../../services/RestaurantService.js";

export const fetchRestaurants = createAsyncThunk(
  "restaurant/fetchRestaurants",
  async (filters) => {
    return await getRestaurants(filters);
  },
);

const restaurantSlice = createSlice({
  name: "restaurant",

  initialState: {
    restaurants: [],
    loading: false,
    error: null,
  },

  reducers: {},

  extraReducers: (builder) => {
    builder
      .addCase(fetchRestaurants.pending, (state) => {
        state.loading = true;
      })

      .addCase(fetchRestaurants.fulfilled, (state, action) => {
        state.loading = false;
        state.restaurants = action.payload;
      })

      .addCase(fetchRestaurants.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default restaurantSlice.reducer;

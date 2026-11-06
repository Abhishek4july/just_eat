import api from "../api/axios";

// Fetch all restaurants with optional filters (name, location, cuisine, price range)
// Filters are passed as query parameters to backend for filtering
export const getRestaurants = async (filters = {}) => {
  const response = await api.get("/restaurant/", {
    params: filters,
  });
  return response.data;
};

// Fetch a single restaurant's details by ID (name, location, cuisine, phone, description)
// Used on Home page for individual restaurant cards and RestaurantDetails page for hero section
export const getRestaurantById = async (id) => {
  const response = await api.get(`/restaurant/${id}`);
  return response.data;
};

// Fetch all menu items for a specific restaurant by restaurant ID
// Returns array of menu items with name, description, price, etc.
// Used on RestaurantDetails page to display menu items in the grid
export const getRestaurantMenu = async (restaurantId) => {
  const response = await api.get(`/restaurant/${restaurantId}/menu`);
  return response.data;
};

// Fetch all favorite restaurants of the logged-in customer
// Used on the Favorite Restaurants page
export const getFavoriteRestaurants = async () => {
  const response = await api.get("/favorite-restaurants");
  return response.data;
};

// Add a restaurant to the logged-in customer's favorites
// restaurantId is passed as a path parameter
export const addFavoriteRestaurant = async (restaurantId) => {
  const response = await api.post(`/favorite-restaurants/${restaurantId}`);
  return response.data;
};

// Remove a restaurant from the logged-in customer's favorites
// restaurantId is passed as a path parameter
export const removeFavoriteRestaurant = async (restaurantId) => {
  const response = await api.delete(`/favorite-restaurants/${restaurantId}`);
  return response.data;
};

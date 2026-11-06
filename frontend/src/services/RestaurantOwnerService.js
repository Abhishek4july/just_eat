import api from "../api/axios";

export const getMyRestaurants = async () => {
  const response = await api.get("/restaurant/my");
  return response.data;
};

export const getDashboard = async (restaurantId) => {
  const response = await api.get(`/restaurant/${restaurantId}/dashboard`);
  return response.data;
};

export const getTopItems = async (restaurantId) => {
  const response = await api.get(`/restaurant/${restaurantId}/top-items`);
  return response.data;
};

export const createRestaurant = async (restaurantData) => {
  const response = await api.post("/restaurant/", restaurantData);
  return response.data;
};

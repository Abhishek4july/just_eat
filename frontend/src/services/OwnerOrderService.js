import api from "../api/axios";

export const getRestaurantOrders = async (restaurantId) => {
  const response = await api.get(`/orders/restaurant/${restaurantId}`);
  return response.data;
};

export const updateOrderStatus = async (orderId, data) => {
  const response = await api.put(`/orders/${orderId}`, data);
  return response.data;
};

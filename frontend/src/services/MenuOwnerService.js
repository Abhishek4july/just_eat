// src/services/MenuOwnerService.js

import api from "../api/axios";

export const getRestaurantMenu = async (restaurantId) => {
  const response = await api.get(`/restaurant/${restaurantId}/menu`);
  return response.data;
};

export const createMenuItem = async (restaurantId, data) => {
  const response = await api.post(`/restaurant/${restaurantId}/menu`, data);
  return response.data;
};

export const updateMenuItem = async (menuItemId, data) => {
  const response = await api.put(`/menu/${menuItemId}`, data);
  return response.data;
};

export const deleteMenuItem = async (menuItemId) => {
  const response = await api.delete(`/menu/${menuItemId}`);
  return response.data;
};

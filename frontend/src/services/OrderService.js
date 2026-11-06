import api from "../api/axios";

// API service for order-related operations
// All order responses include restaurant_name from the backend

// Create a new order for the customer
export const placeOrder = async (order) => {
  const response = await api.post("/orders/", order);
  // Response includes: id, customer_id, restaurant_id, restaurant_name, total_price, status, created_at, order_items
  return response.data;
};

// Fetch customer's orders with optional search filter
// Search can be by restaurant name or status
export const getMyOrders = async (search = "") => {
  const response = await api.get("/orders/my-orders", {
    params: {
      search: search || undefined, // Backend filters by restaurant name or status
    },
  });

  // Response array includes restaurant_name for each order
  return response.data;
};

// Cancel a pending or confirmed order
export const cancelOrder = async (orderId) => {
  const response = await api.patch(`/orders/${orderId}/cancel`);
  // Response includes updated order with CANCELLED status and restaurant_name
  return response.data;
};

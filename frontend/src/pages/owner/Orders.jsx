import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getRestaurantOrders,
  updateOrderStatus,
} from "../../services/OwnerOrderService";
import LoadingSpinner from "../../components/LoadingSpinner.jsx";

function Orders() {
  // Get restaurant ID from URL
  const { restaurantId } = useParams();

  // Stores all restaurant orders
  const [orders, setOrders] = useState([]);

  // Controls loading spinner
  const [loading, setLoading] = useState(true);

  // Fetch orders whenever restaurantId changes
  useEffect(() => {
    loadOrders();
  }, [restaurantId]);

  // Fetch restaurant orders from backend
  const loadOrders = async () => {
    try {
      const data = await getRestaurantOrders(restaurantId);

      // Store fetched orders
      setOrders(data);
    } catch (err) {
      console.log(err);
    } finally {
      // Stop loading spinner
      setLoading(false);
    }
  };

  // Update order status
  const handleStatusChange = async (orderId, status) => {
    try {
      // Update status in backend
      await updateOrderStatus(orderId, { status });

      // Update status in local state
      setOrders((prev) =>
        prev.map((order) =>
          order.id === orderId ? { ...order, status } : order,
        ),
      );
    } catch (err) {
      console.log(err);

      alert("Failed to update order status.");
    }
  };

  // Show loading spinner while fetching orders
  if (loading) return <LoadingSpinner message="Loading Orders..." />;

  return (
    <div className="p-8">
      {/* Page Heading */}
      <h1 className="text-3xl font-bold mb-8">Restaurant Orders</h1>

      {/* Show message if no orders exist */}
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        // Display all restaurant orders
        orders.map((order) => (
          <div
            key={order.id}
            className="bg-white rounded-xl shadow-md p-6 mb-6 border"
          >
            {/* Order Header */}
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold">Order #{order.id}</h2>

              {/* Order Status Badge */}
              <span
                className={`px-3 py-1 rounded-full text-sm font-medium ${
                  order.status === "PENDING"
                    ? "bg-yellow-100 text-yellow-700"
                    : order.status === "CONFIRMED"
                      ? "bg-blue-100 text-blue-700"
                      : order.status === "PREPARING"
                        ? "bg-purple-100 text-purple-700"
                        : order.status === "READY"
                          ? "bg-green-100 text-green-700"
                          : order.status === "DELIVERED"
                            ? "bg-gray-200 text-gray-700"
                            : "bg-red-100 text-red-700"
                }`}
              >
                {order.status}
              </span>
            </div>

            {/* Order Details */}
            <div className="mt-4 space-y-2">
              <p>
                <strong>Customer ID:</strong> {order.customer_id}
              </p>

              <p>
                <strong>Total:</strong> ₹{order.total_price}
              </p>

              <p>
                <strong>Ordered At:</strong>{" "}
                {new Date(order.created_at).toLocaleString()}
              </p>
            </div>

            {/* Ordered Items */}
            {order.order_items?.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold mb-3">Items Ordered</h3>

                <div className="space-y-3">
                  {order.order_items.map((item) => (
                    <div
                      key={item.id}
                      className="flex justify-between items-center border rounded-lg p-3 bg-gray-50"
                    >
                      <div>
                        {/* Menu Item Name */}
                        <p className="font-medium">{item.menu_item_name}</p>

                        {/* Quantity Ordered */}
                        <p className="text-sm text-gray-500">
                          Quantity: {item.quantity}
                        </p>
                      </div>

                      {/* Item Price */}
                      <div className="font-semibold">₹{item.price}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Status Update Dropdown */}
            <div className="mt-6">
              <label className="font-semibold mr-2">Update Status:</label>

              <select
                value={order.status}
                onChange={(e) => handleStatusChange(order.id, e.target.value)}
                className="border rounded-md px-3 py-2"
              >
                <option value="PENDING">PENDING</option>
                <option value="CONFIRMED">CONFIRMED</option>
                <option value="PREPARING">PREPARING</option>
                <option value="READY">READY</option>
                <option value="DELIVERED">DELIVERED</option>
                <option value="CANCELLED">CANCELLED</option>
              </select>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default Orders;

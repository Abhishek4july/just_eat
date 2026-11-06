import { useEffect, useState } from "react";
import { FaReceipt, FaClock } from "react-icons/fa";
import { toast } from "react-toastify";
import { getMyOrders, cancelOrder } from "../../services/OrderService";

// My Orders page displays customer's order history
// Shows order details including items, total price, status, and restaurant name
// Allows users to search orders and cancel pending/confirmed orders
function MyOrders() {
  // Array of orders fetched from backend
  const [orders, setOrders] = useState([]);
  // Loading state while fetching orders from API
  const [loading, setLoading] = useState(true);
  // Tracks which order is currently being cancelled (for button loading state)
  const [cancelingOrderId, setCancelingOrderId] = useState(null);
  // Search term for filtering orders by restaurant name or status
  const [search, setSearch] = useState("");

  // Fetch orders whenever search term changes
  useEffect(() => {
    loadOrders();
  }, [search]);

  // Fetch orders from backend with optional search filter
  const loadOrders = async () => {
    setLoading(true);
    try {
      // Get orders with search query (searches restaurant name or status)
      const data = await getMyOrders(search);
      setOrders(data);
    } catch (error) {
      console.error(error);
      // Show error toast notification if fetch fails
      toast.error("Failed to load orders.");
    } finally {
      setLoading(false);
    }
  };

  // Cancel an order - only available for PENDING and CONFIRMED orders
  const handleCancelOrder = async (orderId) => {
    setCancelingOrderId(orderId);

    try {
      // Submit cancel request to backend
      await cancelOrder(orderId);

      // Show success message
      toast.success("Order cancelled successfully!");

      // Refresh order list to reflect the cancellation
      loadOrders();
    } catch (error) {
      console.error(error);
      // Show error message if cancellation failed
      toast.error("Unable to cancel order.");
    } finally {
      setCancelingOrderId(null);
    }
  };

  // Map order status to Tailwind color classes for visual status badge
  const getStatusColor = (status) => {
    switch (status) {
      case "PENDING":
        return "bg-yellow-100 text-yellow-700";
      case "CONFIRMED":
        return "bg-blue-100 text-blue-700";
      case "PREPARING":
        return "bg-purple-100 text-purple-700";
      case "OUT_FOR_DELIVERY":
        return "bg-indigo-100 text-indigo-700";
      case "DELIVERED":
        return "bg-green-100 text-green-700";
      case "CANCELLED":
        return "bg-red-100 text-red-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 py-10">
      <div className="max-w-6xl mx-auto px-6">
        {/* Page header with title and icon */}
        <div className="flex items-center gap-4 mb-10">
          <FaReceipt className="text-4xl text-orange-500" />

          <div>
            <h1 className="text-4xl font-bold text-gray-800">My Orders</h1>

            <p className="text-gray-500">
              Track all your previous food orders.
            </p>
          </div>
        </div>

        {/* Search and clear filters section */}
        <div className="flex gap-4 mb-8">
          {/* Search input - filters orders by restaurant name or status */}
          <input
            type="text"
            placeholder="Search by restaurant name or status..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500"
          />

          {/* Clear button - resets search and loads all orders */}
          <button
            onClick={() => setSearch("")}
            className="bg-gray-300 hover:bg-gray-400 px-5 rounded-lg btn"
          >
            Clear
          </button>
        </div>

        {/* Conditional rendering: loading spinner, empty state, or orders list */}
        {loading ? (
          // Loading spinner shown while fetching orders
          <div className="flex justify-center items-center py-20">
            <svg
              className="animate-spin h-12 w-12 text-orange-500"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
              ></path>
            </svg>
          </div>
        ) : orders.length === 0 ? (
          // Empty state when no orders found matching search
          <div className="bg-white rounded-2xl shadow-lg p-12 text-center">
            <h2 className="text-2xl font-semibold text-gray-700">
              No Orders Found
            </h2>

            <p className="text-gray-500 mt-3">
              Try changing your search or place a new order.
            </p>
          </div>
        ) : (
          // Orders list - displays each order as a card
          <div className="space-y-6">
            {orders.map((order) => (
              <div
                key={order.id}
                className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition duration-300 p-6"
              >
                <div className="flex justify-between items-start">
                  <div>
                    {/* Order ID */}
                    <h2 className="text-2xl font-bold text-gray-800">
                      Order #{order.id}
                    </h2>

                    {/* Order metadata: timestamp and restaurant name/ID */}
                    <div className="flex flex-col gap-2 mt-2 text-gray-500">
                      {/* Order creation timestamp */}
                      <div className="flex items-center gap-2">
                        <FaClock />
                        <span>
                          {new Date(order.created_at).toLocaleString()}
                        </span>
                      </div>
                      {/* Display restaurant name if available, otherwise use restaurant ID */}
                      <p>
                        <span className="font-semibold text-gray-700">
                          Restaurant:
                        </span>{" "}
                        {order.restaurant_name || `#${order.restaurant_id}`}
                      </p>
                    </div>

                    {/* Order items list - shows name and quantity of each item */}
                    {order.order_items?.length > 0 && (
                      <div className="mt-4 space-y-2">
                        <p className="text-sm font-semibold text-gray-600">
                          Items:
                        </p>
                        <ul className="list-disc list-inside text-gray-700 text-sm">
                          {order.order_items.map((item) => (
                            <li key={item.id}>
                              {item.menu_item_name} x{item.quantity}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Order status badge - colored based on status */}
                  <span
                    className={`px-4 py-2 rounded-full text-sm font-semibold ${getStatusColor(
                      order.status,
                    )}`}
                  >
                    {order.status.replaceAll("_", " ")}
                  </span>
                </div>

                <hr className="my-5" />

                {/* Order summary: total price and restaurant ID */}
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-gray-500">Total Amount</p>

                    <h2 className="text-3xl font-bold text-orange-500">
                      ₹ {order.total_price}
                    </h2>
                  </div>

                  <div className="text-right">
                    <p className="text-gray-500">Restaurant ID</p>

                    <p className="text-lg font-semibold">
                      #{order.restaurant_id}
                    </p>
                  </div>
                </div>

                {/* Cancel Order button - only shown for PENDING and CONFIRMED orders */}
                {["PENDING", "CONFIRMED"].includes(order.status) && (
                  <div className="mt-6">
                    <button
                      onClick={() => handleCancelOrder(order.id)}
                      disabled={cancelingOrderId === order.id}
                      className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg transition btn disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {cancelingOrderId === order.id
                        ? "Canceling..."
                        : "Cancel Order"}
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Export MyOrders component for customer routes
export default MyOrders;

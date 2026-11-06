import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  FaShoppingBag,
  FaClock,
  FaCheckCircle,
  FaUtensils,
} from "react-icons/fa";

import {
  getDashboard,
  getTopItems,
} from "../../services/RestaurantOwnerService";

function Dashboard() {
  const { restaurantId } = useParams();

  const [dashboard, setDashboard] = useState(null);
  const [topItems, setTopItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, [restaurantId]);

  const loadDashboard = async () => {
    try {
      const stats = await getDashboard(restaurantId);
      const items = await getTopItems(restaurantId);

      setDashboard(stats);
      setTopItems(items);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex justify-center items-center bg-orange-50">
        <div className="text-center">
          <div className="h-14 w-14 border-4 border-orange-400 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-5 text-xl font-semibold text-gray-700">
            Loading Dashboard...
          </p>
        </div>
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="min-h-screen flex justify-center items-center bg-orange-50">
        <h2 className="text-3xl font-bold text-gray-600">
          Restaurant not found.
        </h2>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-orange-100 to-orange-50 p-8">
      {/* Header */}
      <div className="bg-white rounded-3xl shadow-xl p-8 mb-10 border-l-8 border-orange-500">
        <h1 className="text-4xl font-extrabold text-gray-800">
          🍽 {dashboard.restaurant_name}
        </h1>
        <p className="text-gray-500 mt-2">
          Welcome back! Here's a quick overview of your restaurant.
        </p>
      </div>

      {/* Stats */}
      <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition duration-300 p-8 border-t-4 border-orange-500">
          <FaShoppingBag className="text-5xl text-orange-500 mb-4" />
          <p className="text-gray-500 text-lg">Total Orders</p>
          <h2 className="text-4xl font-bold text-gray-800 mt-2">
            {dashboard.total_orders}
          </h2>
        </div>

        <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition duration-300 p-8 border-t-4 border-yellow-500">
          <FaClock className="text-5xl text-yellow-500 mb-4" />
          <p className="text-gray-500 text-lg">Pending Orders</p>
          <h2 className="text-4xl font-bold text-gray-800 mt-2">
            {dashboard.pending_orders}
          </h2>
        </div>

        <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition duration-300 p-8 border-t-4 border-green-500">
          <FaCheckCircle className="text-5xl text-green-500 mb-4" />
          <p className="text-gray-500 text-lg">Delivered Orders</p>
          <h2 className="text-4xl font-bold text-gray-800 mt-2">
            {dashboard.delivered_orders}
          </h2>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="grid lg:grid-cols-2 gap-8 mt-10">
        {/* Order Status */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-8">
            📊 Order Status
          </h2>

          <div className="space-y-5">
            {[
              {
                label: "Pending",
                value: dashboard.pending_orders,
                color: "bg-yellow-500",
              },
              {
                label: "Confirmed",
                value: dashboard.confirmed_orders,
                color: "bg-blue-500",
              },
              {
                label: "Preparing",
                value: dashboard.preparing_orders,
                color: "bg-purple-500",
              },
              {
                label: "Ready",
                value: dashboard.ready_orders,
                color: "bg-orange-500",
              },
              {
                label: "Delivered",
                value: dashboard.delivered_orders,
                color: "bg-green-500",
              },
              {
                label: "Cancelled",
                value: dashboard.cancelled_orders,
                color: "bg-red-500",
              },
            ].map((status) => (
              <div
                key={status.label}
                className="flex justify-between items-center bg-orange-50 rounded-xl px-5 py-4 hover:bg-orange-100 transition"
              >
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${status.color}`}></div>
                  <span className="font-medium text-gray-700">
                    {status.label}
                  </span>
                </div>

                <span className="font-bold text-xl text-gray-800">
                  {status.value}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Selling Items */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-8">
            🔥 Top Selling Items
          </h2>

          {topItems.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-gray-500">
              <FaUtensils className="text-6xl text-orange-300 mb-4" />
              <p className="text-lg">No sales yet.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {topItems.map((item, index) => (
                <div
                  key={item.id}
                  className="flex justify-between items-center bg-orange-50 rounded-xl px-5 py-4 hover:bg-orange-100 transition shadow-sm"
                >
                  <div className="flex items-center gap-4">
                    <div className="bg-orange-500 text-white h-10 w-10 rounded-full flex items-center justify-center font-bold">
                      {index + 1}
                    </div>

                    <div>
                      <p className="font-semibold text-gray-800">{item.name}</p>
                      <p className="text-sm text-gray-500">Bestseller Item</p>
                    </div>
                  </div>

                  <span className="bg-orange-500 text-white px-4 py-2 rounded-full font-semibold">
                    {item.order_count} Orders
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

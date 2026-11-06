import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaPlus, FaStore } from "react-icons/fa";
import { toast } from "react-toastify";

import { getMyRestaurants } from "../../services/RestaurantOwnerService";
import LoadingSpinner from "../../components/LoadingSpinner.jsx";

function RestaurantManagement() {
  // Hook used for programmatic navigation
  const navigate = useNavigate();

  // Stores all restaurants owned by the logged-in user
  const [restaurants, setRestaurants] = useState([]);

  // Controls loading spinner visibility
  const [loading, setLoading] = useState(true);

  // Fetch restaurants when the component mounts
  useEffect(() => {
    loadRestaurants();
  }, []);

  // Fetch restaurants from the backend
  const loadRestaurants = async () => {
    try {
      const data = await getMyRestaurants();

      // Save fetched restaurants into state
      setRestaurants(data);
    } catch (err) {
      console.log(err);

      // Show error notification if API call fails
      toast.error("Failed to load restaurants.");
    } finally {
      // Hide loading spinner
      setLoading(false);
    }
  };

  // Show loading spinner while restaurants are being fetched
  if (loading) {
    return <LoadingSpinner message="Loading Restaurants..." />;
  }

  return (
    <div className="min-h-screen bg-orange-50 p-8">
      {/* Page Header */}
      <div className="flex justify-between items-center mb-10">
        <h1 className="text-4xl font-bold">My Restaurants</h1>

        {/* Button to create a new restaurant */}
        <button
          onClick={() => navigate("/owner/restaurants/new")}
          className="flex items-center gap-2 bg-orange-500 hover:bg-orange-600 text-white px-5 py-3 rounded-lg"
        >
          <FaPlus />
          Add Restaurant
        </button>
      </div>

      {/* Show message if no restaurants exist */}
      {restaurants.length === 0 ? (
        <div className="text-center mt-20">
          <h2 className="text-2xl font-semibold">No restaurants found</h2>

          <p className="text-gray-500 mt-2">Create your first restaurant.</p>
        </div>
      ) : (
        // Display all restaurants
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {restaurants.map((restaurant) => (
            <div
              key={restaurant.id}
              className="bg-white rounded-xl shadow-lg p-6 cursor-pointer hover:shadow-xl transition"
              onClick={() =>
                navigate(`/owner/restaurants/${restaurant.id}/dashboard`)
              }
            >
              {/* Restaurant Icon */}
              <FaStore className="text-5xl text-orange-500 mb-4" />

              {/* Restaurant Name */}
              <h2 className="text-2xl font-bold">{restaurant.name}</h2>

              {/* Cuisine */}
              <p className="text-gray-600 mt-2">{restaurant.cuisine}</p>

              {/* City and State */}
              <p className="text-gray-500">
                {restaurant.city}, {restaurant.state}
              </p>

              {/* Open Dashboard Button */}
              <button className="mt-6 w-full bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-lg">
                Open Dashboard
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default RestaurantManagement;

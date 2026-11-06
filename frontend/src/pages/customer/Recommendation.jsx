import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { getRecommendations } from "../../services/RecommendationService";
import LoadingSpinner from "../../components/LoadingSpinner.jsx";

function Recommendations() {
  // Stores the list of recommended restaurants
  const [restaurants, setRestaurants] = useState([]);

  // Controls loading spinner
  const [loading, setLoading] = useState(true);

  // Fetch recommendations when component mounts
  useEffect(() => {
    loadRecommendations();
  }, []);

  // Fetch recommended restaurants from backend
  const loadRecommendations = async () => {
    try {
      const data = await getRecommendations();

      // Store fetched recommendations
      setRestaurants(data);
    } catch (err) {
      console.log(err);

      // Show error message if API fails
      toast.error("Failed to load recommendations.");
    } finally {
      // Stop loading spinner
      setLoading(false);
    }
  };

  // Show loading spinner while data is being fetched
  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Page Heading */}
      <h1 className="text-3xl font-bold mb-6">Recommended Restaurants</h1>

      {/* Show message if no recommendations exist */}
      {restaurants.length === 0 ? (
        <p>No recommendations available.</p>
      ) : (
        // Display recommended restaurants
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {restaurants.map((restaurant) => (
            <div key={restaurant.id} className="bg-white shadow rounded-xl p-5">
              {/* Restaurant Name */}
              <h2 className="text-xl font-bold">{restaurant.name}</h2>

              {/* Restaurant Description */}
              <p className="text-gray-600 mt-2">{restaurant.description}</p>

              {/* Restaurant Details */}
              <div className="mt-4 space-y-1 text-sm text-gray-700">
                <p>
                  <strong>Cuisine:</strong> {restaurant.cuisine}
                </p>

                <p>
                  <strong>City:</strong> {restaurant.city}
                </p>

                <p>
                  <strong>State:</strong> {restaurant.state}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Recommendations;

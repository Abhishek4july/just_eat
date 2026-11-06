import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaHeart, FaRegHeart } from "react-icons/fa";
import {
  addFavoriteRestaurant,
  removeFavoriteRestaurant,
  getFavoriteRestaurants,
} from "../../services/RestaurantService";

// RestaurantCard displays a single restaurant card with
// favorite/unfavorite functionality and navigation to menu page.
function RestaurantCard({ restaurant }) {
  const navigate = useNavigate();

  // Stores whether this restaurant is currently marked as favorite
  const [isFavorite, setIsFavorite] = useState(false);

  // Prevents multiple API requests while favorite action is in progress
  const [loading, setLoading] = useState(false);

  // Check whether this restaurant is already in user's favorites
  // when the component is mounted.
  useEffect(() => {
    checkFavorite();
  }, []);

  // Fetch all favorite restaurants and determine if the current
  // restaurant exists in the favorites list.
  const checkFavorite = async () => {
    try {
      const favorites = await getFavoriteRestaurants();

      const exists = favorites.some(
        (fav) => fav.restaurant.id === restaurant.id,
      );

      setIsFavorite(exists);
    } catch (err) {
      console.log(err);
    }
  };

  // Toggle favorite status of the restaurant.
  // Adds the restaurant if not favorited.
  // Removes it if already favorited.
  const toggleFavorite = async (e) => {
    // Prevent button click from triggering parent click events
    e.stopPropagation();

    // Ignore multiple rapid clicks while request is running
    if (loading) return;

    setLoading(true);

    try {
      if (isFavorite) {
        // Remove restaurant from favorites
        await removeFavoriteRestaurant(restaurant.id);
        setIsFavorite(false);
      } else {
        // Add restaurant to favorites
        await addFavoriteRestaurant(restaurant.id);
        setIsFavorite(true);
      }
    } catch (err) {
      console.log(err);
      alert("Unable to update favorites.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-5 hover:shadow-xl transition duration-300">
      {/* Restaurant name and favorite button */}
      <div className="flex justify-between items-start">
        <div>
          {/* Restaurant name */}
          <h2 className="text-xl font-bold">{restaurant.name}</h2>

          {/* Restaurant location */}
          <p className="text-gray-500 mt-2">
            {restaurant.city}, {restaurant.state}
          </p>
        </div>

        {/* Favorite / Unfavorite button */}
        <button
          onClick={toggleFavorite}
          className="text-2xl cursor-pointer transition hover:scale-110"
          disabled={loading}
        >
          {isFavorite ? (
            <FaHeart className="text-red-500" />
          ) : (
            <FaRegHeart className="text-gray-400 hover:text-red-500" />
          )}
        </button>
      </div>

      {/* Navigate to restaurant menu */}
      <button
        onClick={() => navigate(`/customer/restaurants/${restaurant.id}`)}
        className="mt-5 w-full bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-lg transition cursor-pointer active:scale-95 active:opacity-90"
      >
        View Menu
      </button>
    </div>
  );
}

export default RestaurantCard;

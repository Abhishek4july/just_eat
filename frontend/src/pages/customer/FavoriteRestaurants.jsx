import { useEffect, useState } from "react";
import LoadingSpinner from "../../components/LoadingSpinner";
import RestaurantCard from "../../components/customer/RestaurantCard";
import { getFavoriteRestaurants } from "../../services/RestaurantService";

function FavoriteRestaurants() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = async () => {
    try {
      const data = await getFavoriteRestaurants();

      // Backend returns FavoriteRestaurant objects.
      // Extract restaurant from each object.
      setRestaurants(data.map((item) => item.restaurant));
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Favorite Restaurants</h1>

      {restaurants.length === 0 ? (
        <div className="bg-white rounded-xl shadow p-8 text-center">
          <h2 className="text-xl font-semibold">
            No favorite restaurants yet ❤️
          </h2>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {restaurants.map((restaurant) => (
            <RestaurantCard key={restaurant.id} restaurant={restaurant} />
          ))}
        </div>
      )}
    </div>
  );
}

export default FavoriteRestaurants;

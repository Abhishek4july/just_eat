import { useEffect, useState } from "react";
import { getRestaurants } from "../../services/RestaurantService.js";
import RestaurantCard from "../../components/customer/RestaurantCard.jsx";
import LoadingSpinner from "../../components/LoadingSpinner.jsx";

// Home page displays all restaurants with search and filter functionality
// Customers can search by restaurant name, location, cuisine type, and price range
// Each restaurant is displayed as a clickable card for menu browsing
function Home() {
  // List of restaurants fetched from backend, updated by search/filter
  const [restaurants, setRestaurants] = useState([]);
  // Loading state shown while fetching initial restaurant list
  const [loading, setLoading] = useState(true);

  // Search filter states - used to filter restaurants by various criteria
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  // Load all restaurants when component mounts (empty dependency array = runs once)
  useEffect(() => {
    loadRestaurants();
  }, []);

  // Fetch restaurants from backend with applied search filters
  // Omitted filter values are sent as undefined to backend (ignores empty filters)
  const loadRestaurants = async () => {
    try {
      // Call API with current filter values from state
      const data = await getRestaurants({
        name,
        location,
        cuisine,
        min_price: minPrice || undefined, // Convert empty string to undefined
        max_price: maxPrice || undefined, // Omitted filters are ignored by backend
      });
      setRestaurants(data);
    } catch (error) {
      // Log error to console for debugging (could display toast to user)
      console.log(error);
    } finally {
      // Always hide loading spinner after API call completes (success or failure)
      // Always hide loading spinner after API call completes (success or failure)
      setLoading(false);
    }
  };

  // Show loading spinner while fetching initial restaurant list
  if (loading) return <LoadingSpinner />;

  return (
    <div className="p-6">
      {/* Page title */}
      <h1 className="text-3xl font-bold mb-6">Restaurants</h1>

      {/* Search and filter input fields - responsive layout (1 column on mobile, 5 on desktop) */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        {/* Restaurant name search input */}
        <input
          type="text"
          placeholder="Search by name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border rounded-lg p-2"
        />

        {/* Location filter input */}
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="border rounded-lg p-2"
        />

        {/* Cuisine type filter input */}
        <input
          type="text"
          placeholder="Cuisine"
          value={cuisine}
          onChange={(e) => setCuisine(e.target.value)}
          className="border rounded-lg p-2"
        />

        {/* Minimum price filter input */}
        <input
          type="number"
          placeholder="Min Price"
          value={minPrice}
          onChange={(e) => setMinPrice(e.target.value)}
          className="border rounded-lg p-2"
        />

        {/* Maximum price filter input */}
        <input
          type="number"
          placeholder="Max Price"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          className="border rounded-lg p-2"
        />
      </div>

      {/* Search and Clear buttons - apply or reset filters */}
      <div className="flex gap-3 mb-6">
        {/* Search button - triggers loadRestaurants with current filter values */}
        <button
          onClick={loadRestaurants}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Search
        </button>

        {/* Clear button - resets all filters and loads all restaurants again */}
        <button
          onClick={() => {
            // Reset all filter state variables to empty strings
            setName("");
            setLocation("");
            setCuisine("");
            setMinPrice("");
            setMaxPrice("");

            // Fetch all restaurants without any filters applied
            getRestaurants().then((data) => {
              setRestaurants(data);
            });
          }}
          className="bg-gray-300 px-4 py-2 rounded-lg hover:bg-gray-400"
        >
          Clear
        </button>
      </div>

      {/* Restaurant grid - displays each restaurant as a clickable card */}
      {/* Responsive layout: 1 column on mobile, 2 on tablet, 3 on desktop */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {restaurants.map((restaurant) => (
          <RestaurantCard key={restaurant.id} restaurant={restaurant} />
        ))}
      </div>
    </div>
  );
}

// Export Home component for use in customer routes
export default Home;

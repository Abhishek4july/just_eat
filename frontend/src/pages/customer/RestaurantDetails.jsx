import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getRestaurantById,
  getRestaurantMenu,
} from "../../services/RestaurantService";
import MenuCard from "../../components/customer/MenuCard.jsx";
import LoadingSpinner from "../../components/LoadingSpinner.jsx";

// Restaurant details page displays restaurant information and its menu items
// Handles cart restriction errors when user tries to add items from different restaurants
// Shows inline error message that auto-dismisses after 4 seconds
function RestaurantDetails() {
  // Extract restaurant ID from URL parameters
  const { id } = useParams();

  // Restaurant details: name, location, cuisine, phone, description, etc.
  const [restaurant, setRestaurant] = useState(null);
  // Array of menu items belonging to this restaurant
  const [menu, setMenu] = useState([]);
  // Error message displayed when user violates single-restaurant cart rule
  // Auto-dismisses after 4 seconds via setTimeout in handleAddError
  const [cartError, setCartError] = useState("");

  // Fetch restaurant data and menu items when component mounts
  useEffect(() => {
    loadRestaurant();
  }, []);

  // Handle cart restriction errors from MenuCard component (when trying to add items from different restaurant)
  // Displays error on screen and auto-dismisses after 4 seconds for better UX
  const handleAddError = (message) => {
    setCartError(message);
    // Auto-dismiss error message after 4 seconds
    window.setTimeout(() => setCartError(""), 4000);
  };

  // Fetch restaurant details and menu items from backend using restaurant ID from URL
  const loadRestaurant = async () => {
    try {
      // Fetch restaurant information (name, location, cuisine, phone, description)
      const restaurantData = await getRestaurantById(id);
      console.log(restaurantData);
      setRestaurant(restaurantData);
      setRestaurant(restaurantData);

      // Fetch all menu items for this restaurant
      const menuData = await getRestaurantMenu(id);
      setMenu(menuData);
    } catch (error) {
      // Log errors to console (could display toast to user for better error handling)
      console.log(error);
    }
  };

  // Show loading message while fetching restaurant data
  if (!restaurant) {
    return (
      <div className="flex justify-center items-center h-[70vh]">
        <h2 className="text-2xl font-semibold text-orange-500">
          Loading Restaurant...
        </h2>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      {/* Hero section - displays restaurant banner, name, description, and key info */}
      <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
        {/* Restaurant banner image */}
        <img
          src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200"
          alt="Restaurant"
          className="w-full h-72 object-cover"
        />

        <div className="p-8">
          <div className="flex justify-between items-start">
            <div>
              {/* Restaurant name and description */}
              <h1 className="text-4xl font-bold text-gray-800">
                {restaurant.name}
              </h1>

              <p className="text-gray-500 mt-2">{restaurant.description}</p>
            </div>

            {/* Rating badge */}
            <div className="bg-green-100 text-green-700 px-4 py-2 rounded-xl font-semibold">
              ⭐ 4.5
            </div>
          </div>

          {/* Restaurant info grid - location, cuisine, phone, status */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
            {/* Location info box */}
            <div className="bg-orange-50 rounded-xl p-5 text-center">
              <p className="text-gray-500">Location</p>
              <h2 className="text-lg font-bold mt-2">
                {restaurant.city}, {restaurant.state}
              </h2>
            </div>

            {/* Cuisine type info box */}
            <div className="bg-orange-50 rounded-xl p-5 text-center">
              <p className="text-gray-500">Cuisine</p>
              <h2 className="text-lg font-bold mt-2">{restaurant.cuisine}</h2>
            </div>

            {/* Contact phone info box */}
            <div className="bg-orange-50 rounded-xl p-5 text-center">
              <p className="text-gray-500">Phone</p>
              <h2 className="text-lg font-bold mt-2">{restaurant.phone}</h2>
            </div>

            {/* Restaurant status info box */}
            <div className="bg-orange-50 rounded-xl p-5 text-center">
              <p className="text-gray-500">Status</p>
              <h2 className="text-lg font-bold text-green-600 mt-2">Open</h2>
            </div>
          </div>
        </div>
      </div>

      {/* View Menu button - currently decorative, full menu is displayed below */}
      <div className="mt-10 text-center">
        <button className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-xl text-lg font-semibold transition cursor-pointer active:scale-95 active:opacity-90">
          View Menu
        </button>
      </div>

      {/* Menu section with all restaurant items and error handling */}
      <div className="mt-10">
        <h2 className="text-3xl font-bold mb-6">Menu</h2>

        {/* Inline error banner - displays when user tries to add items from different restaurant */}
        {/* Auto-dismisses after 4 seconds */}
        {cartError && (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
            {cartError}
          </div>
        )}

        {/* Menu items grid - responsive layout (1 column on mobile, 2 on larger screens) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Map through menu items and create MenuCard for each */}
            {menu.map((item) => (
              <MenuCard
                key={item.id}
                item={item}
                restaurantId={restaurant.id}
                onAddError={handleAddError}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// Export RestaurantDetails component for customer menu viewing routes
export default RestaurantDetails;

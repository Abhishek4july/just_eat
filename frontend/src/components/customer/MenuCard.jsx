import { useDispatch, useSelector } from "react-redux";
import { toast } from "react-toastify";
import { addToCart } from "../../features/cart/CartSlice.js";

// Menu item card component with single-restaurant cart restriction
// Prevents users from adding items from different restaurants to the same cart
function MenuCard({ item, restaurantId, onAddError }) {
  const dispatch = useDispatch();
  const cartItems = useSelector((state) => state.cart.items);

  // Get the restaurant ID of items already in cart
  const cartRestaurantId =
    cartItems.length > 0 ? cartItems[0].restaurant_id : null;

  // Allow add only if cart is empty or item is from same restaurant
  const canAdd = !cartRestaurantId || cartRestaurantId === restaurantId;

  // Handle add to cart with restaurant restriction
  const handleAdd = () => {
    if (!canAdd) {
      // Show error message when trying to add from different restaurant
      const message =
        "You can only add items from one restaurant at a time. Clear your cart first to add from another restaurant.";
      toast.error(message);
      // Pass error to parent component for additional UI feedback
      if (onAddError) {
        onAddError(message);
      }
      return;
    }

    // Add item to cart with restaurant ID
    dispatch(
      addToCart({
        ...item,
        restaurant_id: restaurantId,
      }),
    );
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-5 flex justify-between items-center">
      <div>
        <h3 className="text-xl font-semibold">{item.name}</h3>

        <p className="text-gray-500">{item.description}</p>

        <p className="text-orange-500 font-bold mt-2">₹ {item.price}</p>
      </div>

      {/* Add to cart button with cart restriction styling */}
      <button
        onClick={handleAdd}
        disabled={!canAdd}
        style={
          !canAdd
            ? {
                // Custom red blocking circle cursor when button is disabled
                cursor:
                  'url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgc3Ryb2tlPSIjZWYyODMzIiBzdHJva2Utd2lkdGg9IjIiLz48bGluZSB4MT0iNiIgeTE9IjEyIiB4Mj0iMTgiIHkyPSIxMiIgc3Ryb2tlPSIjZWYyODMzIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvc3ZnPg==\") 12 12, not-allowed',
              }
            : {}
        }
        className={`px-4 py-2 rounded-md transition active:scale-95 active:opacity-90 ${
          canAdd
            ? "bg-orange-500 hover:bg-orange-600 text-white cursor-pointer"
            : "bg-red-500 text-white opacity-70" // Red button when restricted from different restaurant
        }`}
        title={!canAdd ? "Cannot add items from different restaurants" : ""}
      >
        Add
      </button>
    </div>
  );
}

export default MenuCard;

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";

import MenuCard from "../../components/owner/MenuCard.jsx";
import MenuForm from "../../components/owner/MenuForm.jsx";
import LoadingSpinner from "../../components/LoadingSpinner.jsx";
import {
  getRestaurantMenu,
  createMenuItem,
  updateMenuItem,
} from "../../services/MenuOwnerService";

function Menu() {
  // Get restaurant ID from URL
  const { restaurantId } = useParams();

  // Stores all menu items
  const [menu, setMenu] = useState([]);

  // Controls loading spinner
  const [loading, setLoading] = useState(true);

  // Controls visibility of MenuForm
  const [showForm, setShowForm] = useState(false);

  // Stores the item currently being edited
  const [editingItem, setEditingItem] = useState(null);

  // Fetch menu whenever restaurantId changes
  useEffect(() => {
    loadMenu();
  }, [restaurantId]);

  // Fetch menu items from backend
  const loadMenu = async () => {
    try {
      const items = await getRestaurantMenu(restaurantId);

      // Store fetched menu items
      setMenu(items);
    } catch (err) {
      console.log(err);

      // Display error message
      toast.error("Unable to load menu");
    } finally {
      // Stop loading spinner
      setLoading(false);
    }
  };

  // Handles both Create and Update operations
  const handleSave = async (data) => {
    try {
      if (editingItem) {
        // Update existing menu item
        await updateMenuItem(editingItem.id, data);
        toast.success("Menu item updated");
      } else {
        // Create new menu item
        await createMenuItem(restaurantId, data);
        toast.success("Menu item created");
      }

      // Close the form
      setShowForm(false);

      // Clear editing state
      setEditingItem(null);

      // Refresh menu list
      loadMenu();
    } catch (err) {
      console.log(err);

      // Display error message
      toast.error("Operation failed");
    }
  };

  // Show loading spinner while menu is loading
  if (loading) {
    return <LoadingSpinner message="Loading Menu..." />;
  }

  return (
    <div className="min-h-screen bg-orange-50 p-8">
      {/* Header Section */}
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-bold">🍽 Restaurant Menu</h1>

          <p className="text-gray-500">Manage your menu items</p>
        </div>

        {/* Add Menu Item Button */}
        <button
          onClick={() => {
            // Open form in create mode
            setEditingItem(null);
            setShowForm(true);
          }}
          className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-xl"
        >
          + Add Menu Item
        </button>
      </div>

      {/* Menu Form */}
      {showForm && (
        <div className="mb-8">
          <MenuForm
            initialData={editingItem}
            onSubmit={handleSave}
            onCancel={() => {
              // Close form
              setShowForm(false);

              // Clear edit state
              setEditingItem(null);
            }}
          />
        </div>
      )}

      {/* Empty Menu Message */}
      {menu.length === 0 ? (
        <div className="text-center text-gray-500 mt-20">
          No menu items found.
        </div>
      ) : (
        // Display Menu Items
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {menu.map((item) => (
            <MenuCard
              key={item.id}
              item={item}
              // Refresh menu after delete/update
              refresh={loadMenu}
              // Open form in edit mode
              onEdit={(item) => {
                setEditingItem(item);
                setShowForm(true);
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default Menu;

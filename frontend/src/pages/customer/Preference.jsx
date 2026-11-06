import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import {
  getPreferences,
  updatePreferences,
} from "../../services/PreferenceService";
import LoadingSpinner from "../../components/LoadingSpinner.jsx";

function Preferences() {
  // Stores user's food preferences
  const [preferences, setPreferences] = useState({
    favorite_cuisine: "",
    dietary_restriction: "",
  });

  // Controls loading spinner
  const [loading, setLoading] = useState(true);

  // Controls whether form is in edit mode or view mode
  const [isEditing, setIsEditing] = useState(false);

  // Fetch preferences when component mounts
  useEffect(() => {
    loadPreferences();
  }, []);

  // Fetch user preferences from backend
  const loadPreferences = async () => {
    try {
      const data = await getPreferences();

      if (data) {
        // Populate state with fetched data
        setPreferences({
          favorite_cuisine: data.favorite_cuisine || "",
          dietary_restriction: data.dietary_restriction || "",
        });

        // If preferences exist, show them in view mode
        if (data.favorite_cuisine || data.dietary_restriction) {
          setIsEditing(false);
        } else {
          // Otherwise open edit mode
          setIsEditing(true);
        }
      } else {
        // No data found
        setIsEditing(true);
      }
    } catch (err) {
      console.log(err);
      toast.error("Failed to load preferences.");

      // Allow user to enter preferences
      setIsEditing(true);
    } finally {
      setLoading(false);
    }
  };

  // Update state whenever user changes dropdown values
  const handleChange = (e) => {
    setPreferences({
      ...preferences,
      [e.target.name]: e.target.value,
    });
  };

  // Save updated preferences
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send updated preferences to backend
      const updated = await updatePreferences(preferences);

      // Update state with response
      setPreferences({
        favorite_cuisine: updated.favorite_cuisine || "",
        dietary_restriction: updated.dietary_restriction || "",
      });

      toast.success("Preferences updated successfully.");

      // Return to view mode
      setIsEditing(false);
    } catch (err) {
      console.log(err);
      toast.error("Failed to update preferences.");
    }
  };

  // Show loading spinner while fetching data
  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-xl mx-auto p-6">
      {/* Page Heading */}
      <h1 className="text-3xl font-bold mb-6">My Preferences</h1>

      {/* View Mode */}
      {!isEditing ? (
        <div className="bg-white shadow rounded-xl p-6 space-y-5">
          {/* Favorite Cuisine */}
          <div>
            <h3 className="font-semibold text-gray-600">Favorite Cuisine</h3>

            <p className="text-lg">
              {preferences.favorite_cuisine || "Not Set"}
            </p>
          </div>

          {/* Dietary Restriction */}
          <div>
            <h3 className="font-semibold text-gray-600">Dietary Restriction</h3>

            <p className="text-lg">
              {preferences.dietary_restriction || "None"}
            </p>
          </div>

          {/* Edit Button */}
          <button
            onClick={() => setIsEditing(true)}
            className="bg-orange-500 hover:bg-orange-600 text-white px-5 py-2 rounded-lg"
          >
            Edit Preferences
          </button>
        </div>
      ) : (
        /* Edit Mode */
        <form
          onSubmit={handleSubmit}
          className="bg-white shadow rounded-xl p-6 space-y-5"
        >
          {/* Favorite Cuisine Dropdown */}
          <div>
            <label className="block mb-2 font-medium">Favorite Cuisine</label>

            <select
              name="favorite_cuisine"
              value={preferences.favorite_cuisine}
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
            >
              <option value="">Select Cuisine</option>
              <option value="North Indian">North Indian</option>
              <option value="Chinese">Chinese</option>
              <option value="Italian">Italian</option>
              <option value="Mexican">Mexican</option>
              <option value="American">American</option>
            </select>
          </div>

          {/* Dietary Restriction Dropdown */}
          <div>
            <label className="block mb-2 font-medium">
              Dietary Restriction
            </label>

            <select
              name="dietary_restriction"
              value={preferences.dietary_restriction}
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
            >
              <option value="">None</option>
              <option value="Vegetarian">Vegetarian</option>
              <option value="Vegan">Vegan</option>
              <option value="Jain">Jain</option>
              <option value="Gluten-Free">Gluten-Free</option>
            </select>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            {/* Save Button */}
            <button
              type="submit"
              className="bg-orange-500 hover:bg-orange-600 text-white px-5 py-2 rounded-lg"
            >
              Save Preferences
            </button>

            {/* Cancel Button */}
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              className="bg-gray-500 hover:bg-gray-600 text-white px-5 py-2 rounded-lg"
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

export default Preferences;

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import { createRestaurant } from "../../services/RestaurantOwnerService";

function CreateRestaurant() {
  // Hook for programmatic navigation
  const navigate = useNavigate();

  // Form state to store restaurant details
  const [form, setForm] = useState({
    name: "",
    description: "",
    address: "",
    city: "",
    state: "",
    cuisine: "",
    phone: "",
  });

  // Loading state while API request is in progress
  const [loading, setLoading] = useState(false);

  // Updates form fields whenever user types
  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  // Handles form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Start loading
      setLoading(true);

      // Send restaurant details to backend
      await createRestaurant(form);

      // Show success message
      toast.success("Restaurant created successfully");

      // Redirect to owner dashboard
      navigate("/owner");
    } catch (err) {
      console.log(err);

      // Show error message if request fails
      toast.error("Failed to create restaurant");
    } finally {
      // Stop loading
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 flex justify-center items-center py-10">
      {/* Form Container */}
      <div className="bg-white shadow-xl rounded-xl w-full max-w-2xl p-8">
        {/* Page Heading */}
        <h1 className="text-3xl font-bold mb-8">Add Restaurant</h1>

        {/* Restaurant Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Restaurant Name */}
          <input
            name="name"
            placeholder="Restaurant Name"
            value={form.name}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-3"
            required
          />

          {/* Description */}
          <textarea
            name="description"
            placeholder="Description"
            value={form.description}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-3"
            rows={3}
            required
          />

          {/* Address */}
          <input
            name="address"
            placeholder="Address"
            value={form.address}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-3"
            required
          />

          {/* City and State */}
          <div className="grid grid-cols-2 gap-4">
            <input
              name="city"
              placeholder="City"
              value={form.city}
              onChange={handleChange}
              className="border rounded-lg px-4 py-3"
              required
            />

            <input
              name="state"
              placeholder="State"
              value={form.state}
              onChange={handleChange}
              className="border rounded-lg px-4 py-3"
              required
            />
          </div>

          {/* Cuisine */}
          <input
            name="cuisine"
            placeholder="Cuisine"
            value={form.cuisine}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-3"
            required
          />

          {/* Phone Number */}
          <input
            name="phone"
            placeholder="Phone Number"
            value={form.phone}
            onChange={handleChange}
            className="w-full border rounded-lg px-4 py-3"
            required
          />

          {/* Action Buttons */}
          <div className="flex gap-4">
            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create Restaurant"}
            </button>

            {/* Cancel Button */}
            <button
              type="button"
              onClick={() => navigate("/owner")}
              className="border px-6 py-3 rounded-lg hover:bg-gray-100"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateRestaurant;

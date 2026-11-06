// src/components/owner/MenuForm.jsx

import { useEffect, useState } from "react";

function MenuForm({ initialData, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    price: "",
    category: "",
    is_special: false,
    special_title: "",
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        description: initialData.description || "",
        price: initialData.price,
        category: initialData.category,
        is_special: initialData.is_special,
        special_title: initialData.special_title || "",
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    onSubmit({
      ...formData,
      price: Number(formData.price),
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow-lg p-6 space-y-4"
    >
      <input
        className="w-full border rounded-lg p-3"
        placeholder="Name"
        name="name"
        value={formData.name}
        onChange={handleChange}
        required
      />

      <textarea
        className="w-full border rounded-lg p-3"
        placeholder="Description"
        name="description"
        value={formData.description}
        onChange={handleChange}
      />

      <input
        type="number"
        className="w-full border rounded-lg p-3"
        placeholder="Price"
        name="price"
        value={formData.price}
        onChange={handleChange}
        required
      />

      <input
        className="w-full border rounded-lg p-3"
        placeholder="Category"
        name="category"
        value={formData.category}
        onChange={handleChange}
        required
      />

      <label className="flex items-center gap-3">
        <input
          type="checkbox"
          name="is_special"
          checked={formData.is_special}
          onChange={handleChange}
        />
        Special Item
      </label>

      {formData.is_special && (
        <input
          className="w-full border rounded-lg p-3"
          placeholder="Special Title"
          name="special_title"
          value={formData.special_title}
          onChange={handleChange}
        />
      )}

      <div className="flex gap-4">
        <button
          type="submit"
          className="flex-1 bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-lg"
        >
          Save
        </button>

        <button
          type="button"
          onClick={onCancel}
          className="flex-1 bg-gray-400 hover:bg-gray-500 text-white py-3 rounded-lg"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}

export default MenuForm;

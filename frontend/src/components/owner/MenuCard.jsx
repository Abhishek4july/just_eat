import { FaTrash } from "react-icons/fa";
import { toast } from "react-toastify";

import { deleteMenuItem } from "../../services/MenuOwnerService";

function MenuCard({ item, refresh, onEdit }) {
  const handleDelete = async () => {
    if (!window.confirm("Delete this menu item?")) return;

    try {
      await deleteMenuItem(item.id);

      toast.success("Deleted successfully");

      refresh();
    } catch (err) {
      console.log(err);

      toast.error(err.response?.data?.detail || "Unable to delete");
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition p-6">
      <div className="flex justify-between">
        <h2 className="text-2xl font-bold">{item.name}</h2>

        {item.is_special && (
          <span className="bg-orange-500 text-white text-xs px-3 py-1 rounded-full">
            ⭐ Special
          </span>
        )}
      </div>

      <p className="text-gray-500 mt-2">{item.description}</p>

      <div className="mt-4">
        <p>
          <strong>Category:</strong> {item.category}
        </p>

        <p>
          <strong>Price:</strong> ₹ {item.price}
        </p>

        <p>
          <strong>Orders Sold:</strong> {item.order_count}
        </p>
      </div>

      <div className="flex gap-3 mt-6">
        <button
          onClick={() => onEdit(item)}
          className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg"
        >
          Edit
        </button>

        <button
          onClick={handleDelete}
          className="flex-1 py-2 rounded-lg text-white transition bg-red-500 hover:bg-red-600"
          title="Delete menu item"
        >
          <FaTrash className="inline mr-2" />
          Delete
        </button>
      </div>
    </div>
  );
}

export default MenuCard;

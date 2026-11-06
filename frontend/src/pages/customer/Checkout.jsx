import { toast } from "react-toastify";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { placeOrder } from "../../services/OrderService";
import { clearCart } from "../../features/cart/CartSlice.js";

function Checkout() {
  // Redux dispatch function
  const dispatch = useDispatch();

  // Used for navigation after placing order
  const navigate = useNavigate();

  // Get cart items from Redux store
  const items = useSelector((state) => state.cart.items);

  // Calculate total cart amount
  const total = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );

  // Controls loading state while placing order
  const [placing, setPlacing] = useState(false);

  // Place order handler
  const handlePlaceOrder = async () => {
    // Prevent placing an empty order
    if (items.length === 0) {
      toast.error("Cart is empty");
      return;
    }

    setPlacing(true);

    try {
      // Create request payload
      const order = {
        restaurant_id: items[0].restaurant_id,

        // Convert cart items into API format
        items: items.map((item) => ({
          menu_item_id: item.id,
          quantity: item.quantity,
        })),
      };

      console.log(order);

      // Send order to backend
      await placeOrder(order);

      // Success message
      toast.success("Order placed successfully!");

      // Clear cart after successful order
      dispatch(clearCart());

      // Navigate to Orders page
      navigate("/customer/orders");
    } catch (error) {
      console.error(error);

      toast.error("Unable to place order.");
    } finally {
      // Stop loading spinner/button
      setPlacing(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      {/* Page Heading */}
      <h1 className="text-4xl font-bold mb-8">Checkout</h1>

      <div className="bg-white rounded-xl shadow-lg p-6">
        {/* Cart Items */}
        {items.map((item) => (
          <div key={item.id} className="flex justify-between border-b py-4">
            <div>
              {/* Item Name */}
              <h2 className="font-semibold">{item.name}</h2>

              {/* Item Quantity */}
              <p>Qty : {item.quantity}</p>
            </div>

            {/* Item Total Price */}
            <div>₹ {item.price * item.quantity}</div>
          </div>
        ))}

        {/* Grand Total */}
        <div className="flex justify-between mt-6 text-2xl font-bold">
          <span>Total</span>

          <span>₹ {total}</span>
        </div>

        {/* Place Order Button */}
        <button
          onClick={handlePlaceOrder}
          disabled={placing}
          className="w-full mt-8 bg-orange-500 hover:bg-orange-600 text-white py-4 rounded-xl text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {placing ? "Placing..." : "Place Order"}
        </button>
      </div>
    </div>
  );
}

export default Checkout;

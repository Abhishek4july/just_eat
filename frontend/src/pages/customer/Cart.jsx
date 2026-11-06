import { useDispatch, useSelector } from "react-redux";
import {
  increaseQuantity,
  decreaseQuantity,
  removeFromCart,
} from "../../features/cart/CartSlice.js";
import { useNavigate } from "react-router-dom";

// Cart page displays all items in the customer's cart
// Each item includes restaurant_id to enforce single-restaurant cart restriction
function Cart() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  // Cart items from Redux store - each item includes restaurant_id
  const items = useSelector((state) => state.cart.items);

  // Calculate total price for all items in cart
  const total = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );

  if (items.length === 0) {
    return (
      <div className="h-[70vh] flex justify-center items-center">
        <h1 className="text-3xl font-bold text-orange-500">
          🛒 Your Cart is Empty
        </h1>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8">My Cart</h1>

      <div className="space-y-5">
        {items.map((item) => (
          <div
            key={item.id}
            className="bg-white shadow-lg rounded-xl p-6 flex justify-between items-center"
          >
            <div>
              <h2 className="text-2xl font-semibold">{item.name}</h2>

              <p className="text-gray-500 mt-2">₹ {item.price}</p>
            </div>

            <div className="flex items-center gap-4">
              {/* Decrease quantity button */}
              <button
                onClick={() => dispatch(decreaseQuantity(item.id))}
                className="w-10 h-10 rounded-full bg-orange-500 text-white text-xl"
              >
                -
              </button>

              <span className="text-xl font-bold">{item.quantity}</span>

              {/* Increase quantity button */}
              <button
                onClick={() => dispatch(increaseQuantity(item.id))}
                className="w-10 h-10 rounded-full bg-orange-500 text-white text-xl"
              >
                +
              </button>

              {/* Remove item from cart button */}
              <button
                onClick={() => dispatch(removeFromCart(item.id))}
                className="ml-5 text-red-600 font-semibold"
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-10 bg-orange-50 rounded-xl p-6 flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold">Total</h2>

          <p className="text-2xl text-orange-600 mt-2">₹ {total}</p>
        </div>

        <button
          onClick={() => navigate("/customer/checkout")}
          className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-xl text-lg font-semibold"
        >
          Proceed to Checkout
        </button>
      </div>
    </div>
  );
}

export default Cart;

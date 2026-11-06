import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  FaShoppingCart,
  FaUserCircle,
  FaHeart,
  FaBars,
  FaTimes,
} from "react-icons/fa";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../features/auth/authSlice";

// Navbar component - main navigation bar for customer pages
// Displays app logo, navigation links, logout button, profile icon, favorites link,
// and cart icon with item count
function Navbar() {
  // Get all items from Redux cart state
  const items = useSelector((state) => state.cart.items);

  // Calculate total number of items in cart
  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  // Controls mobile menu visibility
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    dispatch(logout());
    navigate("/", { replace: true });
    setMenuOpen(false);
  };

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
        {/* App branding and home link */}
        <Link to="/customer" className="text-2xl font-bold text-orange-500">
          🍔 Foodie
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden lg:flex items-center gap-6">
          {/* Recommendations */}
          <Link
            to="/customer/recommendations"
            className="text-gray-700 hover:text-orange-500 font-medium transition"
          >
            Recommendations
          </Link>

          {/* Preferences */}
          <Link
            to="/customer/preferences"
            className="text-gray-700 hover:text-orange-500 font-medium transition"
          >
            Preferences
          </Link>

          {/* Orders */}
          <Link
            to="/customer/my-orders"
            className="text-gray-700 hover:text-orange-500 font-medium transition"
          >
            My Orders
          </Link>

          {/* Favorite Restaurants */}
          <Link
            to="/customer/favorite-restaurants"
            className="flex items-center gap-2 text-gray-700 hover:text-orange-500 font-medium transition"
          >
            <FaHeart className="text-lg" />
            Favorites
          </Link>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="text-gray-700 hover:text-orange-500 font-medium cursor-pointer active:scale-95 transition"
          >
            Logout
          </button>

          {/* Profile */}
          <Link
            to="/customer/profile"
            className="text-gray-700 hover:text-orange-500 transition"
            title="Profile"
          >
            <FaUserCircle className="text-2xl" />
          </Link>

          {/* Cart */}
          <Link to="/customer/cart" className="relative" title="Cart">
            <FaShoppingCart className="text-2xl text-gray-700 hover:text-orange-500 transition" />

            {totalItems > 0 && (
              <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {totalItems}
              </span>
            )}
          </Link>
        </div>

        {/* Mobile Right Section */}
        <div className="flex items-center gap-5 lg:hidden">
          {/* Cart */}
          <Link to="/customer/cart" className="relative">
            <FaShoppingCart className="text-2xl text-gray-700" />

            {totalItems > 0 && (
              <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {totalItems}
              </span>
            )}
          </Link>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="text-2xl text-gray-700"
          >
            {menuOpen ? <FaTimes /> : <FaBars />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      {menuOpen && (
        <div className="lg:hidden border-t bg-white shadow-md">
          <div className="flex flex-col px-6 py-4 space-y-4">
            {/* Recommendations */}
            <Link
              to="/customer/recommendations"
              onClick={() => setMenuOpen(false)}
              className="text-gray-700 hover:text-orange-500"
            >
              Recommendations
            </Link>

            {/* Preferences */}
            <Link
              to="/customer/preferences"
              onClick={() => setMenuOpen(false)}
              className="text-gray-700 hover:text-orange-500"
            >
              Preferences
            </Link>

            {/* Orders */}
            <Link
              to="/customer/my-orders"
              onClick={() => setMenuOpen(false)}
              className="text-gray-700 hover:text-orange-500"
            >
              My Orders
            </Link>

            {/* Favorite Restaurants */}
            <Link
              to="/customer/favorite-restaurants"
              onClick={() => setMenuOpen(false)}
              className="flex items-center gap-2 text-gray-700 hover:text-orange-500"
            >
              <FaHeart />
              Favorites
            </Link>

            {/* Profile */}
            <Link
              to="/customer/profile"
              onClick={() => setMenuOpen(false)}
              className="flex items-center gap-2 text-gray-700 hover:text-orange-500"
            >
              <FaUserCircle />
              Profile
            </Link>

            {/* Logout */}
            <button
              onClick={handleLogout}
              className="text-left text-gray-700 hover:text-orange-500"
            >
              Logout
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navbar;

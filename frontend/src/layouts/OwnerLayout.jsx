import { useState } from "react";
import {
  Link,
  Outlet,
  useLocation,
  useParams,
  useNavigate,
} from "react-router-dom";
import {
  FaStore,
  FaUtensils,
  FaClipboardList,
  FaSignOutAlt,
  FaBars,
  FaTimes,
} from "react-icons/fa";
import { useDispatch } from "react-redux";
import { logout } from "../features/auth/authSlice";

function OwnerLayout() {
  // Get the current URL location (used to highlight the active tab)
  const location = useLocation();

  // Get restaurantId from the URL
  const { restaurantId } = useParams();

  // Redux dispatch function
  const dispatch = useDispatch();

  // Used for programmatic navigation
  const navigate = useNavigate();

  // Controls mobile menu visibility
  const [menuOpen, setMenuOpen] = useState(false);

  // Navigation paths
  const dashboardPath = `/owner/restaurants/${restaurantId}/dashboard`;
  const menuPath = `/owner/restaurants/${restaurantId}/menu`;
  const ordersPath = `/owner/restaurants/${restaurantId}/orders`;

  // Returns different styles for active and inactive navigation links
  const linkStyle = (path) =>
    `flex items-center gap-2 px-4 py-2 rounded-lg transition ${
      location.pathname === path
        ? "bg-orange-500 text-white"
        : "text-gray-700 hover:bg-orange-100 hover:text-orange-500"
    }`;

  const handleLogout = () => {
    // Clear authentication data from Redux
    dispatch(logout());

    // Redirect user to login/home page
    navigate("/", { replace: true });

    setMenuOpen(false);
  };

  return (
    <div className="min-h-screen bg-orange-50">
      {/* Top Navigation Bar */}
      <nav className="bg-white shadow-md border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
          {/* Logo / Home */}
          <Link
            to="/owner"
            className="text-2xl md:text-3xl font-bold text-orange-500 flex items-center gap-2"
          >
            🍽 Owner Panel
          </Link>

          {/* Desktop Navigation Links */}
          <div className="hidden lg:flex items-center gap-4">
            {/* Dashboard */}
            <Link to={dashboardPath} className={linkStyle(dashboardPath)}>
              <FaStore />
              Dashboard
            </Link>

            {/* Menu */}
            <Link to={menuPath} className={linkStyle(menuPath)}>
              <FaUtensils />
              Menu
            </Link>

            {/* Orders */}
            <Link to={ordersPath} className={linkStyle(ordersPath)}>
              <FaClipboardList />
              Orders
            </Link>

            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition cursor-pointer active:scale-95 active:opacity-90"
            >
              <FaSignOutAlt />
              Logout
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden text-2xl text-gray-700"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <FaTimes /> : <FaBars />}
          </button>
        </div>

        {/* Mobile Navigation Menu */}
        {menuOpen && (
          <div className="lg:hidden border-t bg-white shadow-md">
            <div className="flex flex-col px-6 py-4 space-y-3">
              {/* Dashboard */}
              <Link
                to={dashboardPath}
                className={linkStyle(dashboardPath)}
                onClick={() => setMenuOpen(false)}
              >
                <FaStore />
                Dashboard
              </Link>

              {/* Menu */}
              <Link
                to={menuPath}
                className={linkStyle(menuPath)}
                onClick={() => setMenuOpen(false)}
              >
                <FaUtensils />
                Menu
              </Link>

              {/* Orders */}
              <Link
                to={ordersPath}
                className={linkStyle(ordersPath)}
                onClick={() => setMenuOpen(false)}
              >
                <FaClipboardList />
                Orders
              </Link>

              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
              >
                <FaSignOutAlt />
                Logout
              </button>
            </div>
          </div>
        )}
      </nav>

      {/* Child pages (Dashboard, Menu, Orders) are rendered here */}
      <main className="max-w-7xl mx-auto py-8 px-4 md:px-6">
        <Outlet />
      </main>
    </div>
  );
}

export default OwnerLayout;

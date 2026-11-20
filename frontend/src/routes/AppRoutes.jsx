import { Routes, Route } from "react-router-dom";
import Register from "../pages/auth/Register.jsx";
import Login from "../pages/auth/Login.jsx";

import CustomerLayout from "../layouts/CustomerLayout.jsx";
import OwnerLayout from "../layouts/OwnerLayout.jsx";

import ProtectedRoute from "./ProtectedRoutes.jsx";

// Customer Pages
import Home from "../pages/customer/Home.jsx";
import FavoriteRestaurants from "../pages/customer/FavoriteRestaurants.jsx";
import RestaurantDetails from "../pages/customer/RestaurantDetails.jsx";
import Cart from "../pages/customer/Cart.jsx";
import Checkout from "../pages/customer/Checkout.jsx";
import MyOrders from "../pages/customer/MyOrders.jsx";
import Profile from "../pages/customer/Profile";
import Preferences from "../pages/customer/Preference.jsx";
import Recommendations from "../pages/customer/Recommendation";

// Owner Pages
import RestaurantManagement from "../pages/owner/RestaurantManagement.jsx";
import CreateRestaurant from "../pages/owner/Createrestaurant.jsx";
import Dashboard from "../pages/owner/Dashboard.jsx";
import Menu from "../pages/owner/Menu.jsx";
import Orders from "../pages/owner/Orders.jsx";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      {/* CUSTOMER */}
      <Route
        path="/customer"
        element={
          <ProtectedRoute allowedRoles={["CUSTOMER"]}>
            <CustomerLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Home />} />
        <Route path="restaurants/:id" element={<RestaurantDetails />} />
        <Route path="cart" element={<Cart />} />
        <Route path="checkout" element={<Checkout />} />
        <Route path="orders" element={<MyOrders />} />
        <Route path="profile" element={<Profile />} />
        <Route path="preferences" element={<Preferences />} />
        <Route path="recommendations" element={<Recommendations />} />
        <Route path="/customer/my-orders" element={<MyOrders />} />
        <Route
          path="/customer/favorite-restaurants"
          element={<FavoriteRestaurants />}
        />
      </Route>

      {/* OWNER MANAGEMENT */}
      <Route
        path="/owner"
        element={
          <ProtectedRoute allowedRoles={["RESTAURANT_OWNER"]}>
            <RestaurantManagement />
          </ProtectedRoute>
        }
      />

      {/* CREATE RESTAURANT */}
      <Route
        path="/owner/restaurants/new"
        element={
          <ProtectedRoute allowedRoles={["RESTAURANT_OWNER"]}>
            <CreateRestaurant />
          </ProtectedRoute>
        }
      />

      {/* OWNER LAYOUT */}
      <Route
        path="/owner/restaurants/:restaurantId"
        element={
          <ProtectedRoute allowedRoles={["RESTAURANT_OWNER"]}>
            <OwnerLayout />
          </ProtectedRoute>
        }
      >
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="menu" element={<Menu />} />
        <Route path="orders" element={<Orders />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;

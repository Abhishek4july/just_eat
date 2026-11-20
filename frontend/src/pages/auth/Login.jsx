import { useState } from "react";
import { FaEye, FaEyeSlash, FaUtensils } from "react-icons/fa";
import { login, getCurrentUser } from "../../services/authService";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { loginSuccess } from "../../features/auth/authSlice";

// Login page component for customer and restaurant owner authentication
// Handles email/password validation, JWT token storage, and role-based navigation
function Login() {
  // Form state for email and password inputs
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  // UI state for password visibility toggle
  const [showPassword, setShowPassword] = useState(false);
  // Error message displayed on authentication failure
  const [error, setError] = useState("");
  // Loading state during login API call
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const dispatch = useDispatch();

  // Handle form input changes and clear any previous errors
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    // Clear error while typing to provide better UX
    setError("");
  };

  // Handle login form submission with authentication workflow
  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true); // Show loading spinner and disable button during API call

    try {
      // Step 1: Submit credentials to backend for authentication
      const tokenData = await login(formData);

      // Step 2: Save JWT token to localStorage for authenticated API requests
      localStorage.setItem("token", tokenData.access_token);

      // Step 3: Fetch current user data using the new token
      const user = await getCurrentUser();

      // Step 4: Save user and token to Redux store for app-wide access
      dispatch(
        loginSuccess({
          token: tokenData.access_token,
          user,
        }),
      );

      // Step 5: Redirect based on user role (CUSTOMER or OWNER)
      if (user.role?.toUpperCase() === "CUSTOMER") {
  navigate("/customer");
} else if (user.role?.toUpperCase() === "RESTAURANT_OWNER") {
  navigate("/owner");
} else {
  setError("Invalid user role.");
}
    } catch (error) {
      console.error(error.response?.data || error.message);

      // Display backend error message or generic fallback
      setError(error.response?.data?.detail || "Invalid email or password.");
    } finally {
      setLoading(false); // Hide loading spinner after API call completes
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-400 via-orange-500 to-red-500 flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8">
        {/* App branding section */}
        <div className="flex justify-center">
          <div className="w-20 h-20 rounded-full bg-orange-100 flex items-center justify-center">
            <FaUtensils className="text-4xl text-orange-500" />
          </div>
        </div>

        <h1 className="text-3xl font-bold text-center mt-5 text-gray-800">
          Food Ordering
        </h1>

        <p className="text-center text-gray-500 mt-2">
          Welcome back! Login to continue.
        </p>

        {/* Login form with email and password fields */}
        <form onSubmit={handleSubmit} className="mt-8 space-y-5">
          {/* Email input field */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Email
            </label>

            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email"
              className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            />
          </div>

          {/* Password input field with show/hide toggle */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Password
            </label>

            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                className="w-full border border-gray-300 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />

              {/* Password visibility toggle button */}
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500"
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
          </div>

          {/* Error message display */}
          {error && (
            <div className="bg-red-100 border border-red-300 text-red-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          {/* Login button with loading state */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-500 hover:bg-orange-600 transition-all duration-300 text-white py-3 rounded-xl font-semibold text-lg shadow-md disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {/* Show spinner and text during loading, otherwise show Login text */}
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Logging in...
              </span>
            ) : (
              "Login"
            )}
          </button>
        </form>

        <p className="text-center text-gray-600 mt-6">
  Don't have an account?{" "}
  <Link
    to="/register"
    className="text-orange-500 font-semibold hover:underline"
  >
    Register
  </Link>
</p>

      </div>
    </div>
  );
}

// Export Login component for use in app routes
export default Login;

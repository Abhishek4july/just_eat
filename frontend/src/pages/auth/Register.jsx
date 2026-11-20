
import { useState } from "react";
import { FaUtensils, FaEye, FaEyeSlash } from "react-icons/fa";
import { register } from "../../services/authService";
import { useNavigate, Link } from "react-router-dom";

function Register() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      await register(formData);

      alert("Registration successful! Please login.");
      navigate("/");
    } catch (error) {
      console.error(error.response?.data || error.message);

      setError(
        error.response?.data?.detail ||
        "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-400 via-orange-500 to-red-500 flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8">

        <div className="flex justify-center">
          <div className="w-20 h-20 rounded-full bg-orange-100 flex items-center justify-center">
            <FaUtensils className="text-4xl text-orange-500" />
          </div>
        </div>

        <h1 className="text-3xl font-bold text-center mt-5 text-gray-800">
          Create Account
        </h1>

        <p className="text-center text-gray-500 mt-2">
          Register as a customer to get started.
        </p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-5">

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Username
            </label>

            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your name"
              className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            />
          </div>

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
                placeholder="Create a password"
                className="w-full border border-gray-300 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />

              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500"
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-300 text-red-700 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-500 hover:bg-orange-600 transition-all text-white py-3 rounded-xl font-semibold text-lg shadow-md disabled:opacity-60"
          >
            {loading ? "Creating Account..." : "Register"}
          </button>
        </form>

        <p className="text-center text-gray-600 mt-6">
          Already have an account?{" "}
          <Link to="/" className="text-orange-500 font-semibold hover:underline">
            Login
          </Link>
        </p>

      </div>
    </div>
  );
}

export default Register;

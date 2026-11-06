import api from "../api/axios";

// Submit email and password credentials to backend for authentication
// Backend returns JWT access_token on success
// Note: FastAPI requires urlencoded format, not JSON, for /token endpoint (OAuth2 standard)
export const login = async (credentials) => {
  // Convert credentials to URLEncoded format (OAuth2 standard for FastAPI)
  const formData = new URLSearchParams();

  // OAuth2 uses 'username' field for email
  formData.append("username", credentials.email);
  formData.append("password", credentials.password);

  // Post login request with urlencoded content type
  const response = await api.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  // Returns { access_token: "jwt_token_string" }
  return response.data;
};

// Fetch authenticated user's profile data using stored JWT token from localStorage
// Token is automatically included in Authorization header by axios interceptor
// Returns user object with id, email, role (CUSTOMER or OWNER)
export const getCurrentUser = async () => {
  const response = await api.get("/auth/me");
  return response.data;
};

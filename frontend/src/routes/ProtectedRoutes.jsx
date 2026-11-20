
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

function ProtectedRoute({ children, allowedRoles }) {
  const { isAuthenticated, user } = useSelector((state) => state.auth);

  if (!isAuthenticated || !user) {
    return <Navigate to="/" replace />;
  }

  const userRole = user.role?.toUpperCase();

  const normalizedRoles = allowedRoles.map((role) =>
    role.toUpperCase()
  );

  if (!normalizedRoles.includes(userRole)) {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default ProtectedRoute;

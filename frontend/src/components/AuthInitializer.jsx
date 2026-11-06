import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { getCurrentUser } from "../services/authService";
import { loginSuccess } from "../features/auth/authSlice";

function AuthInitializer({ children }) {
  const dispatch = useDispatch();

  useEffect(() => {
    const initialize = async () => {
      const token = localStorage.getItem("token");

      if (!token) return;

      try {
        const user = await getCurrentUser();

        dispatch(
          loginSuccess({
            token,
            user,
          }),
        );
      } catch (err) {
        localStorage.removeItem("token");
      }
    };

    initialize();
  }, [dispatch]);

  return children;
}

export default AuthInitializer;

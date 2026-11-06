import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import {
  getProfile,
  updateProfile,
  changePassword,
} from "../../services/ProfileService";
import { useNavigate } from "react-router-dom";
import LoadingSpinner from "../../components/LoadingSpinner.jsx";

function Profile() {
  const [profile, setProfile] = useState({
    username: "",
    email: "",
    role: "",
  });

  const [passwordData, setPasswordData] = useState({
    current_password: "",
    new_password: "",
  });

  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await getProfile();
      setProfile(data);
    } catch (err) {
      console.log(err);
      toast.error("Failed to load profile.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value,
    });
  };

  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const updatedUser = await updateProfile({
        username: profile.username,
      });

      setProfile(updatedUser);

      toast.success("Profile updated successfully.");

      navigate("/customer");
    } catch (err) {
      console.log(err);
      toast.error("Failed to update profile.");
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();

    try {
      await changePassword(passwordData);

      toast.success("Password changed successfully.");

      setPasswordData({
        current_password: "",
        new_password: "",
      });

      navigate("/"); // Change this if your login route is different
    } catch (err) {
      console.log(err);

      toast.error(err?.response?.data?.detail || "Failed to change password.");
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">My Profile</h1>

      <form
        onSubmit={handleSubmit}
        className="space-y-5 bg-white shadow rounded-xl p-6"
      >
        <div>
          <label className="block mb-2 font-medium">Username</label>

          <input
            type="text"
            name="username"
            value={profile.username}
            onChange={handleChange}
            className="w-full border rounded-lg px-3 py-2"
          />
        </div>

        <div>
          <label className="block mb-2 font-medium">Email</label>

          <input
            type="email"
            value={profile.email}
            disabled
            className="w-full border rounded-lg px-3 py-2 bg-gray-100"
          />
        </div>

        <div>
          <label className="block mb-2 font-medium">Role</label>

          <input
            type="text"
            value={profile.role}
            disabled
            className="w-full border rounded-lg px-3 py-2 bg-gray-100"
          />
        </div>

        <button
          type="submit"
          className="bg-orange-500 hover:bg-orange-600 text-white px-5 py-2 rounded-lg"
        >
          Update Profile
        </button>
      </form>

      <hr className="my-8" />

      <h2 className="text-2xl font-bold mb-4">Change Password</h2>

      <form
        onSubmit={handlePasswordSubmit}
        className="space-y-4 bg-white shadow rounded-xl p-6"
      >
        <div>
          <label className="block mb-2 font-medium">Current Password</label>

          <input
            type="password"
            name="current_password"
            value={passwordData.current_password}
            onChange={handlePasswordChange}
            className="w-full border rounded-lg px-3 py-2"
            required
          />
        </div>

        <div>
          <label className="block mb-2 font-medium">New Password</label>

          <input
            type="password"
            name="new_password"
            value={passwordData.new_password}
            onChange={handlePasswordChange}
            className="w-full border rounded-lg px-3 py-2"
            required
          />
        </div>

        <button
          type="submit"
          className="bg-red-500 hover:bg-red-600 text-white px-5 py-2 rounded-lg"
        >
          Change Password
        </button>
      </form>
    </div>
  );
}

export default Profile;

// src/screens/LoginScreen.jsx
import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../auth/useAuth.jsx";
import { useLanguage } from "../context/LanguageContext.jsx";

import SidebarContainer from "../components/layout/SidebarContainer.jsx";
import LeftSidebar from "../components/layout/LeftSidebar.jsx";
import RightSidebar from "../components/layout/RightSidebar.jsx";

export default function LoginScreen() {
  const { login, loadingUser } = useAuth();
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || "/dashboard";

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!username || !password) {
      setError(
        isHi
          ? "कृपया उपयोगकर्ता नाम और पासवर्ड दर्ज करें।"
          : "Please enter username and password."
      );
      return;
    }

    try {
      setSubmitting(true);
      await login(username, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(
        isHi
          ? "लॉगिन असफल रहा, कृपया फिर से प्रयास करें।"
          : err.message || "Login failed"
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <SidebarContainer
      leftContent={<LeftSidebar />}
      rightContent={<RightSidebar />}
    >
      {/* Center Section */}
      <section className="flex justify-center px-4 w-full">
        <div className="w-full max-w-2xl bg-white dark:bg-[#2d2d2d] rounded-2xl shadow-soft border border-gray-200 dark:border-gray-700 p-8 md:p-12 text-center">
          {/* Title */}
          <h2 className="text-3xl font-extrabold text-textMain dark:text-white">
            {isHi ? "अपने खाते में लॉग इन करें" : "Log In to Your Account"}
          </h2>

          <p className="mt-2 text-textSubtle dark:text-gray-300 text-sm">
            {isHi ? "अपना पर्सनलाइज़्ड डैशबोर्ड देखें" : "Access your personalised dashboard"}
          </p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-6 text-left">
            {/* Username / Email */}
            <div className="space-y-2">
              <label className="font-medium text-sm text-textMain dark:text-gray-200">
                {isHi
                  ? "उपयोगकर्ता नाम"
                  : "Username"}{" "}
              </label>

              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full h-14 px-4 rounded-xl bg-[#FEF6EF] dark:bg-[#1a1a1a] border border-gray-300 dark:border-gray-700 focus:ring-2 focus:ring-primary/50 focus:outline-none placeholder:text-gray-400"
                placeholder={
                  isHi
                    ? "अपना उपयोगकर्ता नाम दर्ज करें"
                    : "Enter username"
                }
              />
            </div>

            {/* Password */}
            <div className="space-y-2">
              <label className="font-medium text-sm text-textMain dark:text-gray-200">
                {isHi ? "पासवर्ड" : "Password"}
              </label>

              <div className="flex items-center border border-gray-300 dark:border-gray-700 rounded-xl bg-[#FEF6EF] dark:bg-[#1a1a1a] focus-within:ring-2 focus-within:ring-primary/50">
                <input
                  type={showPass ? "text" : "password"}
                  className="w-full h-14 px-4 rounded-xl bg-transparent focus:outline-none placeholder:text-gray-400"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder={
                    isHi ? "अपना पासवर्ड दर्ज करें" : "Enter password"
                  }
                />
                <button
                  type="button"
                  onClick={() => setShowPass(!showPass)}
                  className="px-4 text-gray-500 dark:text-gray-300"
                >
                  <span className="material-symbols-outlined">
                    {showPass ? "visibility" : "visibility_off"}
                  </span>
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <p className="text-sm text-red-500 text-center">{error}</p>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={submitting || loadingUser}
              className="flex w-full items-center justify-center h-14 bg-primary text-white rounded-xl font-bold text-lg hover:bg-primary/90 disabled:opacity-60 transition"
            >
              {submitting || loadingUser
                ? isHi
                  ? "लॉगिन हो रहा है..."
                  : "Logging in..."
                : isHi
                ? "लॉगिन करें"
                : "Log In"}
            </button>
          </form>

          {/* Forgot Password */}
          <div className="mt-6">
            <button className="text-primary font-medium hover:underline text-sm">
              {isHi ? "पासवर्ड भूल गए?" : "Forgot Password?"}
            </button>
          </div>

          {/* Register Link */}
          <div className="mt-4 text-sm text-gray-600 dark:text-gray-300">
            {isHi ? "नए हैं?" : "New here?"}{" "}
            <button
              onClick={() => navigate("/register")}
              className="text-primary font-semibold hover:underline"
            >
              {isHi ? "खाता बनाएं" : "Create an account"}
            </button>
          </div>
        </div>
      </section>
    </SidebarContainer>
  );
}

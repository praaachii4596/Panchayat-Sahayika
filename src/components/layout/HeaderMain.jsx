import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../../auth/useAuth.jsx";
import { useLanguage } from "../../context/LanguageContext.jsx";
import { useTheme } from "../../hooks/useTheme.jsx";
import { useState, useRef, useEffect } from "react";

export default function HeaderMain() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const isHome = pathname === "/";

  const { user, logout } = useAuth();
  const { isHindi, isEnglish, setLang } = useLanguage();
  const { theme, toggleTheme } = useTheme();

  /* Dropdown State */
  const [open, setOpen] = useState(false);
  const menuRef = useRef();

  /* Close dropdown on outside click */
  useEffect(() => {
    function handler(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("click", handler);
    return () => document.removeEventListener("click", handler);
  }, []);

  return (
    <header
      className="
        sticky top-0 z-50 
        border-b border-border-light dark:border-border-dark
        bg-background-light/80 dark:bg-background-dark/80
        backdrop-blur-md shadow-sm transition-colors duration-300
      "
    >
      <div className="flex w-full max-w-6xl mx-auto items-center justify-between px-4 py-3">

        {/* BACK BUTTON (NOT ON HOME) */}
        {!isHome && (
          <button
            onClick={() => navigate(-1)}
            className="
              absolute left-4 top-1/2 -translate-y-1/2 mr-3 w-10 h-10 flex items-center justify-center rounded-full
              bg-card-light dark:bg-card-dark border border-border-light dark:border-border-dark
              shadow-soft hover:shadow-md active:scale-95 transition-all
            "
          >
            <span className="material-symbols-outlined text-xl">arrow_back</span>
          </button>
        )}

        {/* LEFT: LOGO */}
        <div
          onClick={() => navigate("/")}
          className="flex items-center gap-4 cursor-pointer group"
        >
          <div className="size-9 text-primary transition-transform duration-300 group-hover:scale-110">
            <svg
              fill="none"
              viewBox="0 0 48 48"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill="currentColor"
                fillRule="evenodd"
                clipRule="evenodd"
                d="M39.475 21.6262C40.358 21.4363 40.6863 21.5589 40.7581 21.5934C40.7876 
                  21.655 40.8547 21.857 40.8082 22.3336C40.7408 23.0255 40.4502 24.0046 
                  39.8572 25.2301C38.6799 27.6631 36.5085 30.6631 33.5858 33.5858C30.6631 
                  36.5085 27.6632 38.6799 25.2301 39.8572C24.0046 40.4502 23.0255 40.7407 
                  22.3336 40.8082C21.8571 40.8547 21.6551 40.7875 21.5934 40.7581C21.5589 
                  40.6863 21.4363 40.358 21.6262 39.475C21.8562 38.4054 22.4689 36.9657 
                  23.5038 35.2817C24.7575 33.2417 26.5497 30.9744 28.7621 28.762C30.9744 
                  26.5497 33.2417 24.7574 35.2817 23.5037C36.9657 22.4689 38.4054 21.8562 
                  39.475 21.6262ZM4.41189 29.2403L18.7597 43.5881C19.8813 44.7097 21.4027 
                  44.9179 22.7217 44.7893C24.0585 44.659 25.5148 44.1631 26.9723 43.4579C29.9052 
                  42.0387 33.2618 39.5667 36.4142 36.4142C39.5667 33.2618 42.0387 29.9052 
                  43.4579 26.9723C44.1631 25.5148 44.659 24.0585 44.7893 22.7217C44.9179 
                  21.4027 44.7097 19.8813 43.5881 18.7597L29.2403 4.41187C27.8527 3.02428 
                  25.8765 3.02573 24.2861 3.36776C22.6081 3.72863 20.7334 4.58419 18.8396 
                  5.74801C16.4978 7.18716 13.9881 9.18353 11.5858 11.5858C9.18354 13.988 
                  7.18717 16.4978 5.74802 18.8396C4.58421 20.7334 3.72865 22.6081 3.36778 
                  24.2861C3.02574 25.8765 3.02429 27.8527 4.41189 29.2403Z"
              />
           </svg>
          </div>

          <div>
            <h2 className="text-lg font-bold tracking-tight group-hover:text-primary transition-colors">
              {isHindi ? "पंचायत सहायिका" : "Panchayat Sahayika"}
            </h2>

            <p className="text-xs text-text-light/70 dark:text-text-dark/60">
              {isHindi
                ? "विश्वसनीय जानकारी • सरकारी प्रेरित डेमो"
                : "Trusted information • Government-inspired demo"}
            </p>
          </div>
        </div>

        {/* RIGHT: Language + Theme + Auth */}
        <div className="flex items-center gap-6">
          {/* Language Toggle - Pill Style */}
           <div className="flex items-center bg-card-light dark:bg-card-dark border border-border-light dark:border-border-dark rounded-full px-1 py-1 shadow-sm">
            <button
              onClick={() => setLang("hi")}
              className={`
                px-3 py-1 text-sm rounded-full transition-all
                ${isHindi
                  ? "bg-primary text-white shadow-md"
                  : "text-text-light dark:text-text-dark hover:bg-black/10 dark:hover:bg-white/10"}
              `}
            >
              हि
            </button>
            <button
              onClick={() => setLang("en")}
              className={`
                px-3 py-1 text-sm rounded-full transition-all
                ${isEnglish
                  ? "bg-primary text-white shadow-md"
                  : "text-text-light dark:text-text-dark hover:bg-black/10 dark:hover:bg-white/10"}
              `}
            >
              En
            </button>
          </div>

          {/* Theme Button */}
          <button
            onClick={toggleTheme}
            className="
              w-10 h-10 flex items-center justify-center 
              rounded-full bg-card-light dark:bg-card-dark 
              border border-border-light dark:border-border-dark
              shadow-soft hover:shadow-md active:scale-95 transition-all
            "
          >
            {theme === "light" ? "🌙" : "☀️"}
          </button>

          {/* LOGGED OUT → Show Login Button */}
          {!user && (
            <button
              onClick={() => navigate("/login")}
              className="
      flex h-10 min-w-[84px] px-4 items-center justify-center rounded-lg 
      bg-primary text-white text-sm font-bold shadow-soft
      hover:bg-primary/90 hover:shadow-md active:scale-95
      transition-all
    "
           >
              {isHindi ? "लॉगिन / रजिस्टर" : "Login / Register"}
            </button>
          )}

          {/* LOGGED IN → Avatar Dropdown */}
          {user && (
            <div className="relative" ref={menuRef}>
              <button
                onClick={() => setOpen(!open)}
                className="
                  w-10 h-10 rounded-full bg-card-light dark:bg-card-dark
                  border border-border-light dark:border-border-dark
                  flex items-center justify-center shadow-soft hover:shadow-md
                  active:scale-95 transition-all
                "
              >
                <span className="material-symbols-outlined text-primary text-2xl">
                  account_circle
                </span>
              </button>

              {/* DROPDOWN */}
              {open && (
                <div
                  className="
                    absolute right-0 mt-2 w-48 rounded-xl
                    bg-card-light dark:bg-card-dark
                    border border-border-light dark:border-border-dark
                    shadow-lg p-2 animate-fadeIn
                  "
                >
                  <button
                    onClick={() => {
                      navigate("/dashboard");
                      setOpen(false);
                    }}
                    className="w-full text-left px-3 py-2 rounded-lg hover:bg-primary/10 dark:hover:bg-white/10"
                  >
                    📊 {isHindi ? "डैशबोर्ड" : "Dashboard"}
                  </button>

                  <button
                    onClick={() => {
                      navigate("/profile/edit");
                      setOpen(false);
                    }}
                    className="w-full text-left px-3 py-2 rounded-lg hover:bg-primary/10 dark:hover:bg-white/10"
                  >
                    ✏️ {isHindi ? "प्रोफ़ाइल संपादित करें" : "Edit Profile"}
                  </button>

                  <button
                    onClick={() => {
                      logout();
                      navigate("/login");
                      setOpen(false);
                    }}
                    className="w-full text-left px-3 py-2 rounded-lg hover:bg-red-500/10 text-red-600 dark:text-red-400"
                  >
                    🚪 {isHindi ? "लॉगआउट" : "Logout"}
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

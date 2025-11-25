/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],

  theme: {
    extend: {
      colors: {
        primary: "#166534",

        // Light mode
        "background-light": "#FEF6EF",
        "text-light": "#333333",
        "card-light": "#FFFFFF",
        "border-light": "#E0E0E0",

        // Dark mode
        "background-dark": "#122018",
        "text-dark": "#E0E0E0",
        "card-dark": "#1A2C21",
        "border-dark": "#3A4D41",
      },

      fontFamily: {
        display: ["Public Sans", "Noto Sans Devanagari", "sans-serif"],
      },

      borderRadius: {
        DEFAULT: "0.5rem",
        lg: "1rem",
        xl: "1.5rem",
        "2xl": "2rem",
        full: "9999px",
      },

      boxShadow: {
        soft: "0 4px 12px 0 rgba(0, 0, 0, 0.05)",
      },
    },
  },

  plugins: [],
};

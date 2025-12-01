// /** @type {import('tailwindcss').Config} */
// export default {
//   darkMode: "class",
//   content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
//   theme: {
//     extend: {
//       colors: {
//         primary: {
//           light: "#166534",
//           dark: "#22C55E",
//         },
//         "background-light": "#FEF6EF",
//         "background-dark": "#0A1A11",
//         "card-light": "#FFFFFF",
//         "card-dark": "#13271B",
//         "text-light": "#333333",
//         "text-dark": "#EAF4ED",
//         "border-light": "#E0E0E0",
//         "border-dark": "#2A3C31",
//           },

//       fontFamily: {
//         display: ["Public Sans", "Noto Sans Devanagari", "sans-serif"],
//         sans: ["Public Sans", "Noto Sans Devanagari", "sans-serif"],
//       },

//       borderRadius: {
//         DEFAULT: "0.5rem",
//         lg: "1rem",
//         xl: "1.5rem",
//         "2xl": "2rem",
//         full: "9999px",
//       },

//       boxShadow: {
//         soft: "0 4px 12px 0 rgba(0, 0, 0, 0.05)",
//       },
//     },
//   },
//   plugins: [require("@tailwindcss/forms"), require("@tailwindcss/container-queries")],
// };

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: "#166534",
          dark: "#22C55E",
        },
        "background-light": "#FEF6EF",
        "background-dark": "#1a1511",
        "card-light": "#FFFFFF",
        "card-dark": "#2c2a27",
        "bot-bubble-light": "#F0FDF4",
        "bot-bubble-dark": "#1c2a20",
        "text-light": "#1F2937",
        "text-dark": "#E5E7EB",
        "text-subtle-light": "#6B7280",
        "text-subtle-dark": "#9CA3AF",
      },
      fontFamily: {
        display: ["Inter", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "0.5rem",
        lg: "1rem",
        xl: "1.5rem",
        "2xl": "1.5rem",
        full: "9999px",
      },
      boxShadow: {
        soft: "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05)",
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
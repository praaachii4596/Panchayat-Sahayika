// // import HeaderMain from "./HeaderMain.jsx";

// // export default function AppShell({ children }) {
// //   return (
// //     <div className="min-h-screen bg-softBeige text-gray-900 flex flex-col">
// //       <HeaderMain />
// //       <main className="flex-1 w-full max-w-6xl mx-auto px-6 py-8">
// //         {children}
// //       </main>
// //     </div>
// //   );
// // }


// // src/components/layout/AppShell.jsx
// export default function AppShell({ children }) {
//   return (
//     <div className="flex flex-col h-screen bg-softBeige">
//       {/* TOP NAVBAR (your existing code inside) */}
//       <header className="h-16 bg-[#0b5a2b] text-white flex items-center px-6">
//         {/* ...logo + title + language buttons etc... */}
//       </header>

//       {/* MAIN AREA: fills remaining height, no scroll here */}
//       <main className="flex-1 overflow-hidden">{children}</main>
//     </div>
//   );
// }


// src/components/layout/AppShell.jsx
// import HeaderMain from "./HeaderMain.jsx";

// export default function AppShell({ children }) {
//   return (
//     <div className="flex flex-col h-screen bg-softBeige text-gray-900">
//       {/* 🔹 Your existing navbar with all buttons */}
//       <HeaderMain />

//       {/* 🔹 Main area fills remaining height, inner screens handle their own scroll */}
//       <main className="flex-1 overflow-hidden">
//         {/* Optional max-width like before so content stays centered */}
//         <div className="w-full max-w-6xl mx-auto px-6 py-4 h-full">
//           {children}
//         </div>
//       </main>
//     </div>
//   );
// }


import HeaderMain from "./HeaderMain.jsx";
import ChatBubble from "../ui/ChatBubble.jsx";
import { Outlet } from "react-router-dom";

export default function AppShell({ children }) {
  return (
    <div className="min-h-screen flex flex-col">

      {/* HEADER */}
      <HeaderMain />

      {/* SCROLLABLE MAIN CONTENT */}
      <main
        className="
          flex-1 overflow-y-auto 
          bg-background-light dark:bg-background-dark 
          transition-colors
          pb-24      /* <-- Add this */
        "
      >
        {children || <Outlet />}
      </main>

      {/* FLOATING CHAT BUBBLE */}
      <ChatBubble />

      {/* FOOTER */}
      <footer
        className="
          fixed bottom-0 w-full
          flex justify-center 
          border-t border-border-light dark:border-border-dark
          bg-card-light dark:bg-card-dark
          text-text-light dark:text-text-dark
          z-50
        "
      >
        <div className="w-full max-w-6xl px-4 py-8">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">

            {/* COPYRIGHT */}
            <p className="text-sm text-text-light/70 dark:text-text-dark/70">
              © 2025 Panchayat Sahayika. All rights reserved.
            </p>

            {/* FOOTER LINKS */}
            <div className="flex gap-6">
              <a
                className="text-sm font-medium hover:text-primary dark:hover:text-primary"
                href="#"
              >
                गोपनीयता नीति / Privacy Policy
              </a>

              <a
                className="text-sm font-medium hover:text-primary dark:hover:text-primary"
                href="#"
              >
                संपर्क करें / Contact Us
              </a>
            </div>

          </div>
        </div>
      </footer>
    </div>
  );
}

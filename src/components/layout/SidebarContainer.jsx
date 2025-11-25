// src/components/layout/SidebarContainer.jsx
import LeftSidebar from "./LeftSidebar.jsx";
import RightSidebar from "./RightSidebar.jsx";

export default function SidebarContainer({ children }) {
  return (
    <div className="w-full max-w-screen-2xl mx-auto grid grid-cols-12 gap-6 px-6 py-8">
      
      {/* LEFT SIDEBAR */}
      <aside className="hidden lg:block col-span-3">
        <LeftSidebar />
      </aside>

      {/* MAIN CONTENT */}
      <main className="col-span-12 lg:col-span-6">
        {children}
      </main>

      {/* RIGHT SIDEBAR */}
      <aside className="hidden lg:block col-span-3">
        <RightSidebar />
      </aside>

    </div>
  );
}

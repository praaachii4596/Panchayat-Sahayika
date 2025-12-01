// // src/components/layout/LeftSidebar.jsx
// import { useLanguage } from "../../context/LanguageContext.jsx";

// export default function LeftSidebar({
//   chats,
//   activeChatId,
//   onNewChat,
//   onSelectChat,
//   onDeleteChat,
//   collapsed,
//   setCollapsed,
// }) {
//   const { lang } = useLanguage();
//   const isHi = lang === "hi";

//   return (
//     <aside
//       className={`transition-all duration-300 bg-white shadow-soft rounded-2xl border
//       ${collapsed ? "w-0 p-0 overflow-hidden" : "w-64 p-4"}`}
//     >
//       {!collapsed && (
//         <>
//           {/* === Header: Chat History & Collapse === */}
//           <div className="flex items-center justify-between mb-4">
//             <div>
//               <h2 className="text-sm font-bold">
//                 {isHi ? "चैट इतिहास" : "Chat History"}
//               </h2>
//               <p className="text-[11px] text-gray-500">
//                 {isHi ? "आपकी पिछली बातचीत" : "Your past conversations"}
//               </p>
//             </div>

//             {/* Collapse button */}
//             <button
//               onClick={() => setCollapsed(true)}
//               className="p-1 w-7 h-7 rounded-full hover:bg-gray-100 flex items-center justify-center"
//               title={isHi ? "छुपाएँ" : "Collapse"}
//             >
//               <span className="material-symbols-outlined text-gray-500 text-sm">
//                 chevron_left
//               </span>
//             </button>
//           </div>

//           {/* === Chat List === */}
//           <div className="flex-1 overflow-y-auto space-y-2 pr-1">
//             {chats.map((chat) => (
//               <div
//                 key={chat.id}
//                 className={`group flex items-center justify-between border rounded-xl px-3 py-2 cursor-pointer transition ${
//                   chat.id === activeChatId
//                     ? "bg-[#E6F4EA] border-[#166534]"
//                     : "bg-white border-gray-200 hover:bg-gray-50"
//                 }`}
//                 onClick={() => onSelectChat(chat.id)}
//               >
//                 <div className="flex items-center gap-2 min-w-0">
//                   {/* Icon */}
//                   <span
//                     className={`material-symbols-outlined text-lg ${
//                       chat.id === activeChatId
//                         ? "text-[#166534]"
//                         : "text-gray-500"
//                     }`}
//                   >
//                     chat
//                   </span>

//                   {/* Title */}
//                   <div className="flex flex-col min-w-0">
//                     <span className="text-sm font-medium truncate">
//                       {chat.title}
//                     </span>
//                     <span className="text-[10px] text-gray-400">
//                       {new Date(chat.createdAt).toLocaleDateString()}
//                     </span>
//                   </div>
//                 </div>

//                 {/* Delete button */}
//                 <button
//                   onClick={(e) => {
//                     e.stopPropagation();
//                     onDeleteChat(chat.id);
//                   }}
//                   className="opacity-0 group-hover:opacity-100 transition text-red-500 text-xs"
//                   title={isHi ? "हटाएँ" : "Delete"}
//                 >
//                   🗑
//                 </button>
//               </div>
//             ))}
//           </div>

//           {/* === New Chat Button === */}
//           <button
//             onClick={onNewChat}
//             className="mt-4 w-full rounded-full bg-[#166534] text-white py-2 text-sm font-bold hover:bg-[#14532d] transition"
//           >
//             {isHi ? "नई चैट" : "New Chat"}
//           </button>
//         </>
//       )}
//     </aside>
//   );
// }

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../../context/LanguageContext.jsx";
import { getStorageKey } from "../../utils/chatStorage";
import { useAuth } from "../../auth/useAuth";

export default function LeftSidebar() {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  const [collapsed, setCollapsed] = useState(false);
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const { user } = useAuth();
  const storageKey = getStorageKey(user?.username);

  // -----------------------------
  // Load chats from localStorage
  // -----------------------------
  const loadChats = () => {
    try {
      const raw = localStorage.getItem(storageKey);
      if (!raw) {
        setChats([]);
        setActiveChat(null);
        return;
      }

      const parsed = JSON.parse(raw);

      const savedChats = Array.isArray(parsed.chats) ? parsed.chats : [];
      const savedActive = parsed.activeChatId || (savedChats[0]?.id ?? null);

      setChats(savedChats);
      setActiveChat(savedActive);
    } catch (err) {
      console.error("Error loading chats:", err);
      setChats([]);
      setActiveChat(null);
    }
  };

  useEffect(() => {
    loadChats();
  }, []);

  // -----------------------------
  // Save chat history
  // -----------------------------
  const saveChats = (updatedChats, active) => {
    const payload = {
      chats: updatedChats,
      activeChatId: active ?? activeChat,
    };
    localStorage.setItem(storageKey, JSON.stringify(payload));
    setChats(updatedChats);
    setActiveChat(payload.activeChatId);
  };

  // -----------------------------
  // Create new chat
  // -----------------------------
  const createNewChat = () => {
    const newChat = {
      id: "chat_" + Date.now(),
      title: isHi ? "नई चैट" : "New Chat",
      createdAt: Date.now(),
      messages: [
        {
          from: "bot",
          type: "text",
          text: "नमस्ते! मैं आपकी पंचायत सहायिका हूं…",
        },
      ],
    };
    const updated = [...chats, newChat];
    saveChats(updated, newChat.id);
    navigate(`/chat?id=${newChat.id}`);

    setActiveChat(newChat.id);
  };

  // -----------------------------
  // Delete chat
  // -----------------------------
  const deleteChat = (id, e) => {
    e.stopPropagation();
    const updated = chats.filter((c) => c.id !== id);
    saveChats(updated);

    if (id === activeChat) {
      if (updated.length > 0) {
        navigate(`/chat/${updated[0].id}`);
        setActiveChat(updated[0].id);
      } else {
        setActiveChat(null);
        navigate("/chat");
      }
    }
  };

  // -----------------------------
  // Open chat
  // -----------------------------
  const openChat = (id) => {
  setActiveChat(id);
  saveChats(chats, id);
  navigate(`/chat?id=${id}`);
};

  return (
    <aside
      className={`hidden fixed top-24 left-6 z-40 lg:block transition-all ${
        collapsed ? "w-20" : "w-72"
      }`}
    >
      <div className="sticky top-28">
        <div className="p-4 bg-white dark:bg-neutral-900 rounded-2xl shadow-soft border border-gray-200 dark:border-neutral-700">
          {/* Header row */}
          <div className="flex items-center justify-between mb-3">
            {!collapsed && (
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-3xl text-primary">
                  forum
                </span>
                <div>
                  <h2 className="font-bold text-text-main dark:text-white">
                    {isHi ? "चैट इतिहास" : "Chat History"}
                  </h2>
                  <p className="text-sm text-text-subtle dark:text-neutral-400">
                    {isHi ? "आपकी हाल की बातचीत" : "Your recent conversations"}
                  </p>
                </div>
              </div>
            )}

            {/* Collapse toggle */}
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-neutral-700"
            >
              <span className="material-symbols-outlined text-neutral-500 dark:text-neutral-400">
                {collapsed ? "history" : "chevron_left"}
              </span>
            </button>
          </div>

          {/* New Chat Button */}
          {!collapsed && (
            <button
              onClick={createNewChat}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg bg-primary text-white hover:bg-primary/90 transition"
            >
              <span className="material-symbols-outlined">add_comment</span>
              {isHi ? "नई चैट" : "New Chat"}
            </button>
          )}

          {/* Chat list */}
          <div className="mt-4 space-y-1">
            {chats.length === 0 && !collapsed && (
              <p className="text-xs text-center text-neutral-500 dark:text-neutral-400 py-4">
                {isHi ? "कोई चैट नहीं मिली" : "No chats found"}
              </p>
            )}

            {chats.map((chat) => (
              <div
                key={chat.id}
                onClick={() => openChat(chat.id)}
                className={`group relative flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
                  activeChat === chat.id
                    ? "bg-primary/10 text-primary"
                    : "hover:bg-gray-100 dark:hover:bg-neutral-700"
                }`}
              >
                {/* Icon with fill variations */}
                {/* Hide chat icons when collapsed */}
                {!collapsed && (
                  <span
                    className="material-symbols-outlined"
                    style={{
                      fontVariationSettings: `'FILL' ${
                        activeChat === chat.id ? 1 : 0
                      }, 'wght' 400, 'GRAD' 0, 'opsz' 24`,
                    }}
                  >
                    chat_bubble
                  </span>
                )}
                {collapsed && <div className="w-6" />}

                {!collapsed && (
                  <div className="flex flex-col">
                    <p
                      className={`font-medium text-sm ${
                        activeChat === chat.id
                          ? "text-primary"
                          : "text-text-main dark:text-white"
                      }`}
                    >
                      {chat.title}
                    </p>

                    {chat.lastMessage && (
                      <p className="text-xs text-neutral-500 dark:text-neutral-400 truncate max-w-[150px]">
                        {chat.lastMessage}
                      </p>
                    )}
                  </div>
                )}

                {/* Delete icon visible ONLY on hover */}
                {!collapsed && (
                  <button
                    onClick={(e) => deleteChat(chat.id, e)}
                    className="absolute right-2 opacity-0 group-hover:opacity-100 transition p-1 rounded-full hover:bg-red-100 dark:hover:bg-red-900/30"
                  >
                    <span className="material-symbols-outlined text-red-500">
                      delete
                    </span>
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </aside>
  );
}

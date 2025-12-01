// // src/screens/ChatScreen.jsx
// import React, { useEffect, useState, useRef } from "react";
// import { useNavigate } from "react-router-dom";
// import AnswerCard from "../components/ui/AnswerCard.jsx";
// import { useAuth } from "../auth/useAuth.jsx";
// import { useLanguage } from "../context/LanguageContext.jsx";
// import SCHEMES from "../data/samaj_kalyan_vibhag_clean_typed.json";

// // ⬇️ NEW: use the same RightSidebar as SidebarContainer
// import RightSidebar from "../components/layout/RightSidebar.jsx";

// const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";
// const API_URL = `${API_BASE}/ask`;
// const STORAGE_KEY_BASE = "ps_chats_v1";

// const WELCOME_MESSAGE = {
//   from: "bot",
//   type: "text",
//   text: "नमस्ते! मैं आपकी पंचायत सहायिका हूं। Aap apna sawal bolkar ya likhkar pooch sakte hain – हिन्दी, गढ़वाली ya English mein.",
// };

// function createNewChat() {
//   return {
//     id: `chat_${Date.now()}`,
//     title: "New chat",
//     createdAt: Date.now(),
//     messages: [WELCOME_MESSAGE],
//   };
// }

// /* --------------------- Scheme Details Modal --------------------- */
// function SchemeDetailsModal({ scheme, onClose }) {
//   if (!scheme) return null;

//   return (
//     <div className="fixed inset-0 bg-black/40 z-40 flex items-center justify-center px-4">
//       <div className="relative bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-xl">
//         <button
//           onClick={onClose}
//           className="absolute right-4 top-4 text-2xl text-gray-400 hover:text-gray-600"
//         >
//           ✕
//         </button>

//         <h2 className="text-xl font-bold mb-1">
//           {scheme.name_hi || scheme.name_en}
//         </h2>
//         {scheme.name_en && (
//           <p className="text-sm text-gray-600 mb-2">{scheme.name_en}</p>
//         )}

//         <p className="text-xs text-gray-500 mb-4">
//           {scheme.category ? scheme.category + " • " : ""}
//           {scheme.department || ""}
//         </p>

//         {scheme.description_hi && (
//           <div className="mb-3">
//             <h3 className="font-semibold text-sm mb-1">विवरण (Hindi)</h3>
//             <p className="text-sm whitespace-pre-line">
//               {scheme.description_hi}
//             </p>
//           </div>
//         )}
//         {scheme.description_en && (
//           <div>
//             <h3 className="font-semibold text-sm mb-1">
//               Description (English)
//             </h3>
//             <p className="text-sm whitespace-pre-line">
//               {scheme.description_en}
//             </p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// /* ========================= MAIN SCREEN ========================= */
// export default function ChatScreen() {
//   const navigate = useNavigate();
//   const { user } = useAuth();
//   const { lang } = useLanguage();
//   const isHi = lang === "hi";

//   const storageKey = user?.username
//     ? `${STORAGE_KEY_BASE}_${user.username}`
//     : `${STORAGE_KEY_BASE}_guest`;

//   const [chats, setChats] = useState([]);
//   const [activeChatId, setActiveChatId] = useState(null);

//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);

//   // Chatbot answer language
//   const [uiLang, setUiLang] = useState("hi");

//   // Voice features
//   const [listening, setListening] = useState(false);
//   const [speakingKey, setSpeakingKey] = useState(null);
//   const [copiedKey, setCopiedKey] = useState(null);
//   const audioRef = useRef(null);
//   const [voices, setVoices] = useState([]);

//   // UI state
//   const [selectedScheme, setSelectedScheme] = useState(null);

//   const activeChat =
//     chats.find((c) => c.id === activeChatId) || chats[0] || null;
//   const messages = activeChat?.messages || [];

//   /* --------------------- Load browser voices --------------------- */
//   useEffect(() => {
//     if (typeof window === "undefined" || !window.speechSynthesis) return;

//     const synth = window.speechSynthesis;

//     function loadVoices() {
//       const vs = synth.getVoices();
//       if (vs && vs.length) setVoices(vs);
//     }

//     loadVoices();
//     synth.onvoiceschanged = loadVoices;
//     return () => {
//       synth.onvoiceschanged = null;
//     };
//   }, []);

//   /* --------------------- Helpers --------------------- */
//   function stripHtml(html) {
//     const tmp = document.createElement("div");
//     tmp.innerHTML = html;
//     return tmp.textContent || tmp.innerText || "";
//   }

//   function stripApplyReadMore(html) {
//     if (!html) return html;
//     return html.replace(/Apply\s*\/\s*Read More[^<]*/gi, "");
//   }

//   function getSchemeByLabel(label) {
//     if (!label) return null;
//     const norm = label.replace(/[()]/g, "").trim().toLowerCase();

//     return (
//       SCHEMES.find((s) => {
//         const hi = String(s.name_hi || "").toLowerCase();
//         const en = String(s.name_en || "").toLowerCase();
//         return (
//           hi === norm || en === norm || hi.includes(norm) || en.includes(norm)
//         );
//       }) || null
//     );
//   }

//   // For source pills (more lenient)
//   function findScheme(label) {
//     if (!label) return null;
//     const l = label.toLowerCase();
//     return (
//       SCHEMES.find(
//         (s) =>
//           (s.name_hi || "").toLowerCase().includes(l) ||
//           (s.name_en || "").toLowerCase().includes(l)
//       ) || null
//     );
//   }

//   /* --------------------- Load chats on mount --------------------- */
//   useEffect(() => {
//     try {
//       const raw = localStorage.getItem(storageKey);
//       if (raw) {
//         const parsed = JSON.parse(raw);
//         const loaded = Array.isArray(parsed.chats) ? parsed.chats : [];
//         if (loaded.length > 0) {
//           setChats(loaded);
//           setActiveChatId(parsed.activeChatId || loaded[0].id);
//           return;
//         }
//       }
//     } catch (err) {
//       console.error("Failed to load chats:", err);
//     }

//     const first = createNewChat();
//     setChats([first]);
//     setActiveChatId(first.id);
//   }, [storageKey]);

//   /* --------------------- Persist chats --------------------- */
//   useEffect(() => {
//     if (!chats.length) return;
//     try {
//       localStorage.setItem(storageKey, JSON.stringify({ chats, activeChatId }));
//     } catch (err) {
//       console.error("Failed to save chats:", err);
//     }
//   }, [chats, activeChatId, storageKey]);

//   /* --------------------- Voice: Speak answer --------------------- */
//   function handleSpeak(msgKey, msg) {
//     try {
//       // 1) If server audio_url present (Garhwali TTS)
//       if (msg.audio_url) {
//         if (speakingKey === msgKey && audioRef.current) {
//           audioRef.current.pause();
//           audioRef.current.currentTime = 0;
//           audioRef.current = null;
//           setSpeakingKey(null);
//           return;
//         }

//         if (audioRef.current) {
//           audioRef.current.pause();
//           audioRef.current.currentTime = 0;
//         }

//         const audio = new Audio(
//           msg.audio_url.startsWith("http")
//             ? msg.audio_url
//             : `${API_BASE}${msg.audio_url}`
//         );
//         audioRef.current = audio;
//         setSpeakingKey(msgKey);

//         audio.onended = () => {
//           setSpeakingKey((curr) => (curr === msgKey ? null : curr));
//           audioRef.current = null;
//         };

//         audio.play().catch((err) => {
//           console.error("Failed to play TTS audio:", err);
//           setSpeakingKey(null);
//         });
//         return;
//       }

//       // 2) Browser TTS fallback
//       if (typeof window === "undefined" || !window.speechSynthesis) {
//         alert(
//           isHi
//             ? "आपका ब्राउज़र वॉइस सपोर्ट नहीं करता।"
//             : "Your browser doesn't support TTS."
//         );
//         return;
//       }

//       if (speakingKey === msgKey) {
//         window.speechSynthesis.cancel();
//         setSpeakingKey(null);
//         return;
//       }

//       const plainText = stripHtml(msg.text || "");
//       if (!plainText.trim()) return;

//       const utterance = new SpeechSynthesisUtterance(plainText);
//       const hasDevanagari = /[\u0900-\u097F]/.test(plainText);
//       const synth = window.speechSynthesis;

//       let selectedVoice = null;

//       if (msg.lang === "en" && !hasDevanagari) {
//         utterance.lang = "en-IN";
//         selectedVoice =
//           voices.find((v) => v.lang?.toLowerCase().startsWith("en-in")) ||
//           voices.find((v) => v.lang?.toLowerCase().startsWith("en")) ||
//           null;
//       } else {
//         utterance.lang = "hi-IN";
//         selectedVoice =
//           voices.find((v) => v.lang?.toLowerCase().startsWith("hi")) ||
//           voices.find((v) => v.lang?.toLowerCase().includes("hi-in")) ||
//           null;
//       }

//       if (selectedVoice) utterance.voice = selectedVoice;

//       synth.cancel();
//       synth.speak(utterance);
//       setSpeakingKey(msgKey);
//       utterance.onend = () => setSpeakingKey(null);
//     } catch (err) {
//       console.error("TTS error:", err);
//       setSpeakingKey(null);
//     }
//   }

//   /* --------------------- Copy answer text --------------------- */
//   async function handleCopy(msgKey, msg) {
//     try {
//       const plainText = stripHtml(msg.text || "");
//       if (!plainText.trim()) return;

//       if (navigator.clipboard && navigator.clipboard.writeText) {
//         await navigator.clipboard.writeText(plainText);
//       } else {
//         const textarea = document.createElement("textarea");
//         textarea.value = plainText;
//         document.body.appendChild(textarea);
//         textarea.select();
//         document.execCommand("copy");
//         document.body.removeChild(textarea);
//       }

//       setCopiedKey(msgKey);
//       setTimeout(() => {
//         setCopiedKey((curr) => (curr === msgKey ? null : curr));
//       }, 1500);
//     } catch (err) {
//       console.error("Copy failed:", err);
//       alert(isHi ? "कॉपी विफल हुआ।" : "Copy failed.");
//     }
//   }

//   /* --------------------- Mic / Speech input --------------------- */
//   function startListening() {
//     try {
//       const SpeechRecognition =
//         window.SpeechRecognition || window.webkitSpeechRecognition;

//       if (!SpeechRecognition) {
//         alert(
//           isHi
//             ? "आपका ब्राउज़र वॉइस इनपुट सपोर्ट नहीं करता।"
//             : "Your browser does not support voice input."
//         );
//         return;
//       }

//       const recognition = new SpeechRecognition();
//       recognition.lang = "hi-IN";
//       recognition.interimResults = false;

//       recognition.onstart = () => setListening(true);
//       recognition.onend = () => setListening(false);

//       recognition.onresult = (event) => {
//         const speechText = event.results?.[0]?.[0]?.transcript ?? "";
//         if (!speechText) return;
//         setInput((prev) =>
//           prev ? `${prev.trimEnd()} ${speechText}` : speechText
//         );
//       };

//       recognition.onerror = (err) => {
//         console.error("Speech recognition error:", err);
//         setListening(false);
//         alert(
//           (isHi ? "माइक त्रुटि: " : "Mic error: ") + (err?.error ?? "unknown")
//         );
//       };

//       recognition.start();
//     } catch (err) {
//       console.error("Speech recognition exception:", err);
//       setListening(false);
//     }
//   }

//   /* --------------------- Chat management --------------------- */
//   function handleNewChat() {
//     const nc = createNewChat();
//     setChats((prev) => [...prev, nc]);
//     setActiveChatId(nc.id);
//     setInput("");
//     setSpeakingKey(null);
//     setCopiedKey(null);
//     if (typeof window !== "undefined" && window.speechSynthesis) {
//       window.speechSynthesis.cancel();
//     }
//   }

//   function handleDeleteChat(chatId, e) {
//     e.stopPropagation();
//     setChats((prev) => {
//       const filtered = prev.filter((c) => c.id !== chatId);
//       if (filtered.length === 0) {
//         const nc = createNewChat();
//         setActiveChatId(nc.id);
//         return [nc];
//       }
//       if (chatId === activeChatId) setActiveChatId(filtered[0].id);
//       return filtered;
//     });
//   }

//   function handleSelectChat(chatId) {
//     setActiveChatId(chatId);
//     setSpeakingKey(null);
//     setCopiedKey(null);
//     if (typeof window !== "undefined" && window.speechSynthesis) {
//       window.speechSynthesis.cancel();
//     }
//   }

//   /* --------------------- Send message --------------------- */
//   async function sendMessage() {
//     const question = input.trim();
//     if (!question || loading) return;
//     if (!activeChatId || !activeChat) return;

//     const prevMessages = messages || [];
//     const historyForBackend = prevMessages.slice(-6).map((m) => ({
//       role: m.from === "user" ? "user" : "assistant",
//       content: stripHtml(m.text || ""),
//     }));

//     const userMeta = user
//       ? {
//           district: user.district || null,
//           block: user.block || null,
//           village_code: user.village_code || null,
//           age: user.age || null,
//           gender: user.gender || null,
//           interest_tag: user.interest_tag || null,
//           disability: user.disability || null,
//           occupation: user.occupation || null,
//           income_bracket: user.income_bracket || null,
//           social_category: user.social_category || null,
//         }
//       : null;

//     const userMsg = { from: "user", type: "text", text: question };
//     setChats((prev) =>
//       prev.map((chat) =>
//         chat.id === activeChatId
//           ? {
//               ...chat,
//               title:
//                 chat.title === "New chat"
//                   ? question.length > 30
//                     ? question.slice(0, 30) + "..."
//                     : question
//                   : chat.title,
//               messages: [...chat.messages, userMsg],
//             }
//           : chat
//       )
//     );

//     setInput("");
//     setLoading(true);

//     try {
//       const res = await fetch(API_URL, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           question,
//           ui_lang: uiLang,
//           mode: "auto",
//           history: historyForBackend,
//           user_meta: userMeta,
//         }),
//       });

//       if (!res.ok)
//         throw new Error(`API error: ${res.status} ${res.statusText}`);

//       const data = await res.json();
//       const responseHtml = stripApplyReadMore(
//         data.message || data.response || ""
//       );
//       const sources = Array.isArray(data.sources) ? data.sources : [];
//       const cards = Array.isArray(data.cards) ? data.cards : [];
//       const audioUrl = data.audio_url || null;

//       let botMsg;
//       if (cards.length > 0) {
//         botMsg = {
//           from: "bot",
//           type: "answer+cards",
//           text: responseHtml,
//           cards,
//           lang: uiLang,
//           sources,
//           audio_url: audioUrl,
//         };
//       } else {
//         botMsg = {
//           from: "bot",
//           type: "answer",
//           text: responseHtml,
//           sources,
//           lang: uiLang,
//           audio_url: audioUrl,
//         };
//       }

//       setChats((prev) =>
//         prev.map((chat) =>
//           chat.id === activeChatId
//             ? { ...chat, messages: [...chat.messages, botMsg] }
//             : chat
//         )
//       );
//     } catch (err) {
//       console.error(err);
//       const errorMsg = {
//         from: "bot",
//         type: "text",
//         text: isHi
//           ? "माफ़ कीजिए, सर्वर से कनेक्शन नहीं हो पाया। कृपया थोड़ी देर बाद पुनः प्रयास करें।"
//           : "Sorry, couldn't connect to the server. Please try again later.",
//       };
//       setChats((prev) =>
//         prev.map((chat) =>
//           chat.id === activeChatId
//             ? { ...chat, messages: [...chat.messages, errorMsg] }
//             : chat
//         )
//       );
//     } finally {
//       setLoading(false);
//     }
//   }

//   if (!activeChat) return null;

//   // Simple grouping for "Today" / "Yesterday" in sidebar (visual only)
//   const today = new Date();
//   today.setHours(0, 0, 0, 0);
//   const yesterday = new Date(today);
//   yesterday.setDate(today.getDate() - 1);

//   const todayChats = chats.filter((c) => {
//     const d = new Date(c.createdAt);
//     d.setHours(0, 0, 0, 0);
//     return d.getTime() === today.getTime();
//   });

//   const yesterdayChats = chats.filter((c) => {
//     const d = new Date(c.createdAt);
//     d.setHours(0, 0, 0, 0);
//     return d.getTime() === yesterday.getTime();
//   });

//   const otherChats = chats.filter(
//     (c) => !todayChats.includes(c) && !yesterdayChats.includes(c)
//   );

//   // ⬇️ Static three-column grid now (left + center + right)
//   const gridCols = "grid-cols-[260px_1fr_320px]";

//   /* ======================= UI LAYOUT ======================= */
//   return (
//     <>
//       <div className="flex h-screen w-full flex-col bg-background-light dark:bg-background-dark font-display text-text-light dark:text-text-dark overflow-hidden">
//         {/* ========= FIXED HEADER ========= */}
//         {/* <header className="flex h-16 shrink-0 items-center justify-between border-b border-black/10 dark:border-white/10 px-4 bg-background-light dark:bg-background-dark">
//           <div className="flex items-center gap-3">
//             <button
//               onClick={() => navigate(-1)}
//               className="flex items-center justify-center size-8 rounded-full hover:bg-black/5 dark:hover:bg-white/5"
//             >
//               <span className="material-symbols-outlined text-2xl">
//                 arrow_back
//               </span>
//             </button>
//             <div className="flex size-9 items-center justify-center rounded-full bg-primary text-white font-bold text-lg">
//               S
//             </div>
//             <h1 className="text-lg font-bold">Panchayat Sahayika (Demo)</h1>
//           </div> */}

//         {/* <div className="flex items-center gap-4"> */}
//         {/* App language pill (from global context) */}
//         {/* <button className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-9 px-4 bg-primary/10 dark:bg-primary/20 text-primary dark:text-green-300 text-sm font-bold">
//               <span>{isHi ? "हिन्दी" : "English"}</span>
//             </button> */}
//         {/* Simple avatar from username initial */}
//         {/* <div className="size-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
//               {(user?.username || "U").charAt(0).toUpperCase()}
//             </div>
//           </div>
//         </header> */}

//         {/* ================= MAIN CONTENT GRID ================= */}
//         <main
//           className={`grid flex-1 overflow-hidden ${gridCols} gap-x-4 transition-[grid-template-columns] duration-200`}
//         >
//           {/* =============== LEFT COLUMN (Chat List) =============== */}
//           <aside className="flex flex-col border-r border-black/10 dark:border-white/10 p-2 bg-background-light dark:bg-background-dark overflow-hidden">
//             <div className="p-2 flex items-center gap-2 overflow-y-auto">
//               <button
//                 onClick={handleNewChat}
//                 className="flex flex-1 items-center justify-center gap-2 rounded-lg h-10 bg-primary px-4 text-sm font-bold text-white hover:bg-primary/90"
//               >
//                 <span className="material-symbols-outlined text-xl">add</span>
//                 <span>New chat</span>
//               </button>
//             </div>

//             <div className="flex flex-1 flex-col gap-4 overflow-y-auto px-2 py-3">
//               {todayChats.length > 0 && (
//                 <div>
//                   <h3 className="px-2 text-xs font-semibold uppercase text-text-subtle-light dark:text-text-subtle-dark">
//                     Today
//                   </h3>
//                   <ul className="mt-1 flex flex-col gap-1">
//                     {todayChats.map((chat) => (
//                       <li key={chat.id}>
//                         <button
//                           onClick={() => handleSelectChat(chat.id)}
//                           className={`group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm ${
//                             chat.id === activeChatId
//                               ? "bg-primary/10 dark:bg-primary/20 text-primary dark:text-green-300 font-medium"
//                               : "text-text-light dark:text-text-dark hover:bg-black/5 dark:hover:bg-white/5"
//                           }`}
//                         >
//                           <span className="material-symbols-outlined text-base text-text-subtle-light">
//                             chat_bubble
//                           </span>
//                           <span className="flex-1 truncate">{chat.title}</span>
//                           <span
//                             className="material-symbols-outlined text-[16px] text-red-400 opacity-0 group-hover:opacity-100"
//                             onClick={(e) => handleDeleteChat(chat.id, e)}
//                           >
//                             delete
//                           </span>
//                         </button>
//                       </li>
//                     ))}
//                   </ul>
//                 </div>
//               )}

//               {yesterdayChats.length > 0 && (
//                 <div>
//                   <h3 className="px-2 text-xs font-semibold uppercase text-text-subtle-light dark:text-text-subtle-dark">
//                     Yesterday
//                   </h3>
//                   <ul className="mt-1 flex flex-col gap-1">
//                     {yesterdayChats.map((chat) => (
//                       <li key={chat.id}>
//                         <button
//                           onClick={() => handleSelectChat(chat.id)}
//                           className={`group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm ${
//                             chat.id === activeChatId
//                               ? "bg-primary/10 dark:bg-primary/20 text-primary dark:text-green-300 font-medium"
//                               : "text-text-light dark:text-text-dark hover:bg-black/5 dark:hover:bg-white/5"
//                           }`}
//                         >
//                           <span className="material-symbols-outlined text-base text-text-subtle-light">
//                             chat_bubble
//                           </span>
//                           <span className="flex-1 truncate">{chat.title}</span>
//                           <span
//                             className="material-symbols-outlined text-[16px] text-red-400 opacity-0 group-hover:opacity-100"
//                             onClick={(e) => handleDeleteChat(chat.id, e)}
//                           >
//                             delete
//                           </span>
//                         </button>
//                       </li>
//                     ))}
//                   </ul>
//                 </div>
//               )}

//               {otherChats.length > 0 && (
//                 <div>
//                   <h3 className="px-2 text-xs font-semibold uppercase text-text-subtle-light dark:text-text-subtle-dark">
//                     Older
//                   </h3>
//                   <ul className="mt-1 flex flex-col gap-1">
//                     {otherChats.map((chat) => (
//                       <li key={chat.id}>
//                         <button
//                           onClick={() => handleSelectChat(chat.id)}
//                           className={`group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm ${
//                             chat.id === activeChatId
//                               ? "bg-primary/10 dark:bg-primary/20 text-primary dark:text-green-300 font-medium"
//                               : "text-text-light dark:text-text-dark hover:bg-black/5 dark:hover:bg-white/5"
//                           }`}
//                         >
//                           <span className="material-symbols-outlined text-base text-text-subtle-light">
//                             chat_bubble
//                           </span>
//                           <span className="flex-1 truncate">{chat.title}</span>
//                           <span
//                             className="material-symbols-outlined text-[16px] text-red-400 opacity-0 group-hover:opacity-100"
//                             onClick={(e) => handleDeleteChat(chat.id, e)}
//                           >
//                             delete
//                           </span>
//                         </button>
//                       </li>
//                     ))}
//                   </ul>
//                 </div>
//               )}
//             </div>
//           </aside>

//           {/* =============== CENTER COLUMN (Chat Interface) =============== */}
//           {/* ⬇️ MAIN FIX: make this a flex column with overflow on messages only,
//               so input box stays fixed at bottom of center column */}
//           <div className="flex flex-col bg-white/50 dark:bg-black/20 overflow-hidden">
//             {/* Chat Header (conversation title + bot language toggle) */}
//             <div className="flex h-14 shrink-0 items-center justify-between border-b border-black/10 dark:border-white/10 px-4">
//               <h2 className="font-semibold truncate">
//                 {activeChat?.title || "Panchayat Sahayika"}
//               </h2>
//               <div className="flex items-center gap-2 text-xs">
//                 <button
//                   onClick={() => setUiLang("hi")}
//                   className={`rounded-full h-8 px-3 font-bold border text-xs ${
//                     uiLang === "hi"
//                       ? "bg-primary text-white border-primary"
//                       : "bg-black/5 dark:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark border-transparent"
//                   }`}
//                 >
//                   हिन्दी
//                 </button>
//                 <button
//                   onClick={() => setUiLang("en")}
//                   className={`rounded-full h-8 px-3 font-bold border text-xs ${
//                     uiLang === "en"
//                       ? "bg-primary text-white border-primary"
//                       : "bg-black/5 dark:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark border-transparent"
//                   }`}
//                 >
//                   English
//                 </button>
//                 <button
//                   onClick={() => setUiLang("garhwali")}
//                   className={`rounded-full h-8 px-3 font-bold border text-xs ${
//                     uiLang === "garhwali"
//                       ? "bg-primary text-white border-primary"
//                       : "bg-black/5 dark:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark border-transparent"
//                   }`}
//                 >
//                   Garhwali
//                 </button>
//               </div>
//             </div>

//             {/* Message Area – only this scrolls now */}
//             <div className="flex-1 space-y-6 overflow-y-auto p-4 md:p-6">
//               {messages.map((msg, idx) => {
//                 const msgKey = `${activeChatId}-${idx}`;

//                 // USER MESSAGE
//                 if (msg.from === "user") {
//                   const initial = (user?.username || "U")
//                     .charAt(0)
//                     .toUpperCase();
//                   return (
//                     <div
//                       key={msgKey}
//                       className="flex items-end justify-end gap-3"
//                     >
//                       <div className="flex w-full max-w-3xl flex-col items-end gap-1">
//                         <p className="text-xs text-text-subtle-light dark:text-text-subtle-dark">
//                           {isHi ? "आप" : "You"}
//                         </p>
//                         <p className="rounded-2xl rounded-br-lg bg-primary px-4 py-2.5 text-base text-white">
//                           {msg.text}
//                         </p>
//                       </div>
//                       <div className="size-9 shrink-0 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
//                         {initial}
//                       </div>
//                     </div>
//                   );
//                 }

//                 // BOT: ANSWER + CARDS
//                 if (msg.type === "answer+cards") {
//                   return (
//                     <div key={msgKey} className="flex items-end gap-3">
//                       {/* Bot avatar */}
//                       <div className="size-9 shrink-0 rounded-full bg-primary/20 flex items-center justify-center">
//                         <div className="size-6 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold">
//                           S
//                         </div>
//                       </div>

//                       <div className="flex w-full max-w-3xl flex-col items-start gap-1">
//                         <p className="text-xs text-text-subtle-light dark:text-text-subtle-dark">
//                           Sahayika Bot
//                         </p>

//                         {/* Little text bubble if any intro text */}
//                         {msg.text && (
//                           <p className="rounded-2xl rounded-bl-lg bg-bot-bubble-light dark:bg-bot-bubble-dark px-4 py-2.5 text-base text-text-light dark:text-text-dark whitespace-pre-line">
//                             <span
//                               dangerouslySetInnerHTML={{ __html: msg.text }}
//                             />
//                           </p>
//                         )}

//                         {/* Main AnswerCard like in reference */}
//                         <div className="mt-2 w-full max-w-xl">
//                           <AnswerCard>
//                             <div className="flex items-center justify-end gap-1 border-b border-black/10 dark:border-white/10 px-3 py-1.5">
//                               <button
//                                 onClick={() => handleSpeak(msgKey, msg)}
//                                 className="flex size-7 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark"
//                               >
//                                 {speakingKey === msgKey ? (
//                                   <span className="material-symbols-outlined text-base">
//                                     stop
//                                   </span>
//                                 ) : (
//                                   <span className="material-symbols-outlined text-base">
//                                     volume_up
//                                   </span>
//                                 )}
//                               </button>
//                               <button
//                                 onClick={() => handleCopy(msgKey, msg)}
//                                 className="flex size-7 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark"
//                               >
//                                 <span className="material-symbols-outlined text-base">
//                                   content_copy
//                                 </span>
//                               </button>
//                               {copiedKey === msgKey && (
//                                 <span className="text-[10px] text-gray-500">
//                                   {isHi ? "कॉपी हुआ" : "Copied"}
//                                 </span>
//                               )}
//                             </div>

//                             {/* Cards from backend (scheme tiles) */}
//                             <div className="p-4 space-y-2">
//                               {msg.cards?.map((c, i) => {
//                                 const label = c.title_hi || c.title;
//                                 const hasData = getSchemeByLabel(label);
//                                 if (!hasData) return null;

//                                 return (
//                                   <button
//                                     key={i}
//                                     onClick={() => setSelectedScheme(hasData)}
//                                     className="w-full text-left rounded-2xl bg-card-light dark:bg-card-dark border border-black/10 dark:border-white/10 px-3 py-2 hover:bg-black/5 dark:hover:bg-white/5 transition cursor-pointer"
//                                   >
//                                     <div className="text-sm font-semibold text-text-light dark:text-text-dark">
//                                       {c.title}
//                                     </div>
//                                     {c.subtitle && (
//                                       <div className="text-[11px] text-text-subtle-light dark:text-text-subtle-dark mt-0.5">
//                                         {c.subtitle}
//                                       </div>
//                                     )}
//                                   </button>
//                                 );
//                               })}
//                             </div>
//                           </AnswerCard>
//                         </div>

//                         {/* Source pills */}
//                         {msg.sources?.length > 0 && (
//                           <div className="mt-2 flex flex-wrap gap-2">
//                             {msg.sources.map((s, i) => {
//                               const label = s.name_hi || s.name_en;
//                               const hasData = findScheme(label);
//                               if (!hasData) return null;
//                               return (
//                                 <button
//                                   key={i}
//                                   onClick={() => setSelectedScheme(hasData)}
//                                   className="px-3 py-1 bg-green-50 border border-green-200 text-green-700 text-[10px] rounded-full hover:bg-green-100"
//                                 >
//                                   {label}
//                                 </button>
//                               );
//                             })}
//                           </div>
//                         )}
//                       </div>
//                     </div>
//                   );
//                 }

//                 // BOT: NORMAL ANSWER / TEXT
//                 if (msg.type === "answer" || msg.type === "text") {
//                   return (
//                     <div key={msgKey} className="flex items-end gap-3">
//                       <div className="size-9 shrink-0 rounded-full bg-primary/20 flex items-center justify-center">
//                         <div className="size-6 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold">
//                           S
//                         </div>
//                       </div>

//                       <div className="flex max-w-xl flex-col items-start gap-1">
//                         <p className="text-xs text-text-subtle-light dark:text-text-subtle-dark">
//                           Sahayika Bot
//                         </p>

//                         <AnswerCard>
//                           <div className="flex items-center justify-end gap-1 border-b border-black/10 dark:border-white/10 px-3 py-1.5">
//                             <button
//                               onClick={() => handleSpeak(msgKey, msg)}
//                               className="flex size-7 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark"
//                             >
//                               {speakingKey === msgKey ? (
//                                 <span className="material-symbols-outlined text-base">
//                                   stop
//                                 </span>
//                               ) : (
//                                 <span className="material-symbols-outlined text-base">
//                                   volume_up
//                                 </span>
//                               )}
//                             </button>
//                             <button
//                               onClick={() => handleCopy(msgKey, msg)}
//                               className="flex size-7 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark"
//                             >
//                               <span className="material-symbols-outlined text-base">
//                                 content_copy
//                               </span>
//                             </button>
//                             {copiedKey === msgKey && (
//                               <span className="text-[10px] text-gray-500">
//                                 {isHi ? "कॉपी हुआ" : "Copied"}
//                               </span>
//                             )}
//                           </div>

//                           <div
//                             className="p-4 text-sm leading-relaxed whitespace-pre-line text-text-light dark:text-text-dark"
//                             dangerouslySetInnerHTML={{ __html: msg.text }}
//                           />

//                           {msg.sources?.length > 0 && (
//                             <div className="border-t border-black/10 dark:border-white/10 px-4 py-3 flex flex-wrap gap-2">
//                               {msg.sources.map((s, i) => {
//                                 const label = s.name_hi || s.name_en;
//                                 const hasData = findScheme(label);
//                                 if (!hasData) return null;
//                                 return (
//                                   <button
//                                     key={i}
//                                     onClick={() => setSelectedScheme(hasData)}
//                                     className="px-3 py-1 bg-green-50 border border-green-200 text-green-700 text-[10px] rounded-full hover:bg-green-100"
//                                   >
//                                     {label}
//                                   </button>
//                                 );
//                               })}
//                             </div>
//                           )}
//                         </AnswerCard>
//                       </div>
//                     </div>
//                   );
//                 }

//                 // Fallback
//                 return (
//                   <div key={msgKey} className="flex items-end gap-3">
//                     <div className="size-9 shrink-0 rounded-full bg-primary/20 flex items-center justify-center">
//                       <div className="size-6 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold">
//                         S
//                       </div>
//                     </div>
//                     <div className="flex max-w-xl flex-col items-start gap-1">
//                       <p className="text-xs text-text-subtle-light dark:text-text-subtle-dark">
//                         Sahayika Bot
//                       </p>
//                       <p className="rounded-2xl rounded-bl-lg bg-bot-bubble-light dark:bg-bot-bubble-dark px-4 py-2.5 text-base text-text-light dark:text-text-dark">
//                         {msg.text}
//                       </p>
//                     </div>
//                   </div>
//                 );
//               })}

//               {loading && (
//                 <div className="flex items-center gap-2 text-xs text-gray-600">
//                   <div className="size-6 rounded-full border-2 border-primary border-t-transparent animate-spin" />
//                   <span>{isHi ? "सोच रही हूँ..." : "Thinking…"}</span>
//                 </div>
//               )}
//             </div>

//             {/* ⬇️ FIXED Chat Input Footer (center column bottom) */}
//             <div className="shrink-0 border-t border-black/10 dark:border-white/10 px-4 py-3 bg-background-light dark:bg-background-dark">
//               <div className="relative flex items-center">
//                 <button
//                   onClick={startListening}
//                   className="absolute left-2 flex size-8 items-center justify-center rounded-full hover:bg-black/10 dark:hover:bg-white/10"
//                 >
//                   {listening ? (
//                     <span className="material-symbols-outlined text-text-subtle-light dark:text-text-subtle-dark">
//                       stop
//                     </span>
//                   ) : (
//                     <span className="material-symbols-outlined text-text-subtle-light dark:text-text-subtle-dark">
//                       mic
//                     </span>
//                   )}
//                 </button>

//                 <textarea
//                   rows={1}
//                   className="w-full resize-none rounded-xl border-0 bg-black/5 dark:bg-white/5 py-2.5 pl-12 pr-12 text-base focus:ring-2 focus:ring-primary"
//                   placeholder={
//                     isHi
//                       ? "अपना प्रश्न पूछें... / Ask your question..."
//                       : "Ask your question... / अपना प्रश्न पूछें..."
//                   }
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   onKeyDown={(e) => {
//                     if (e.key === "Enter" && !e.shiftKey) {
//                       e.preventDefault();
//                       sendMessage();
//                     }
//                   }}
//                 />

//                 <button
//                   onClick={sendMessage}
//                   disabled={loading || !input.trim()}
//                   className="absolute right-2 flex size-8 items-center justify-center rounded-full bg-primary text-white hover:bg-primary/90 disabled:opacity-50"
//                 >
//                   <span className="material-symbols-outlined">send</span>
//                 </button>
//               </div>
//               {listening && (
//                 <div className="mt-1 text-[11px] text-green-700">
//                   🎙️ {isHi ? "मैं आपकी बात सुन रही हूँ..." : "I'm listening..."}
//                 </div>
//               )}
//             </div>
//           </div>

//           {/* =============== RIGHT COLUMN (Global RightSidebar) =============== */}
//           {/* ⬇️ OLD related-schemes sidebar removed.
//               Now using the shared RightSidebar from your layout. */}
//           <aside className="flex flex-col border-l border-black/10 dark:border-white/10 pl-5 pr-4 py-4 overflow-y-auto bg-background-light dark:bg-background-dark">
//             <RightSidebar />
//           </aside>
//         </main>
//       </div>

//       {/* Scheme Modal */}
//       {selectedScheme && (
//         <SchemeDetailsModal
//           scheme={selectedScheme}
//           onClose={() => setSelectedScheme(null)}
//         />
//       )}
//     </>
//   );
// }



// src/screens/ChatScreen.jsx
import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import AnswerCard from "../components/ui/AnswerCard.jsx";
import { useAuth } from "../auth/useAuth.jsx";
import { useLanguage } from "../context/LanguageContext.jsx";
import SCHEMES from "../data/samaj_kalyan_vibhag_clean_typed.json";

// Right sidebar used in layout
import RightSidebar from "../components/layout/RightSidebar.jsx";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";
const API_URL = `${API_BASE}/ask`;
const STORAGE_KEY_BASE = "ps_chats_v1";

const WELCOME_MESSAGE = {
  from: "bot",
  type: "text",
  text: "नमस्ते! मैं आपकी पंचायत सहायिका हूं। Aap apna sawal bolkar ya likhkar pooch sakte hain – हिन्दी, गढ़वाली ya English mein.",
};

function createNewChat() {
  return {
    id: `chat_${Date.now()}`,
    title: "New chat",
    createdAt: Date.now(),
    messages: [WELCOME_MESSAGE],
  };
}

/* --------------------- Scheme Details Modal --------------------- */
function SchemeDetailsModal({ scheme, onClose }) {
  if (!scheme) return null;

  return (
    <div className="fixed inset-0 bg-black/40 z-40 flex items-center justify-center px-4">
      <div className="relative bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-xl">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 text-2xl text-gray-400 hover:text-gray-600"
        >
          ✕
        </button>

        <h2 className="text-xl font-bold mb-1">
          {scheme.name_hi || scheme.name_en}
        </h2>
        {scheme.name_en && (
          <p className="text-sm text-gray-600 mb-2">{scheme.name_en}</p>
        )}

        <p className="text-xs text-gray-500 mb-4">
          {scheme.category ? scheme.category + " • " : ""}
          {scheme.department || ""}
        </p>

        {scheme.description_hi && (
          <div className="mb-3">
            <h3 className="font-semibold text-sm mb-1">विवरण (Hindi)</h3>
            <p className="text-sm whitespace-pre-line">
              {scheme.description_hi}
            </p>
          </div>
        )}
        {scheme.description_en && (
          <div>
            <h3 className="font-semibold text-sm mb-1">
              Description (English)
            </h3>
            <p className="text-sm whitespace-pre-line">
              {scheme.description_en}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/* ========================= MAIN SCREEN ========================= */
export default function ChatScreen() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  const storageKey = user?.username
    ? `${STORAGE_KEY_BASE}_${user.username}`
    : `${STORAGE_KEY_BASE}_guest`;

  const [chats, setChats] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Chatbot answer language
  const [uiLang, setUiLang] = useState("hi");

  // Voice features
  const [listening, setListening] = useState(false);
  const [speakingKey, setSpeakingKey] = useState(null);
  const [copiedKey, setCopiedKey] = useState(null);
  const audioRef = useRef(null);
  const [voices, setVoices] = useState([]);

  // UI state
  const [selectedScheme, setSelectedScheme] = useState(null);

  const activeChat =
    chats.find((c) => c.id === activeChatId) || chats[0] || null;
  const messages = activeChat?.messages || [];

  /* --------------------- Load browser voices --------------------- */
  useEffect(() => {
    if (typeof window === "undefined" || !window.speechSynthesis) return;

    const synth = window.speechSynthesis;

    function loadVoices() {
      const vs = synth.getVoices();
      if (vs && vs.length) setVoices(vs);
    }

    loadVoices();
    synth.onvoiceschanged = loadVoices;
    return () => {
      synth.onvoiceschanged = null;
    };
  }, []);

  /* --------------------- Helpers --------------------- */
  function stripHtml(html) {
    const tmp = document.createElement("div");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
  }

  function stripApplyReadMore(html) {
    if (!html) return html;
    return html.replace(/Apply\s*\/\s*Read More[^<]*/gi, "");
  }

  function getSchemeByLabel(label) {
    if (!label) return null;
    const norm = label.replace(/[()]/g, "").trim().toLowerCase();

    return (
      SCHEMES.find((s) => {
        const hi = String(s.name_hi || "").toLowerCase();
        const en = String(s.name_en || "").toLowerCase();
        return (
          hi === norm || en === norm || hi.includes(norm) || en.includes(norm)
        );
      }) || null
    );
  }

  // For source pills (more lenient)
  function findScheme(label) {
    if (!label) return null;
    const l = label.toLowerCase();
    return (
      SCHEMES.find(
        (s) =>
          (s.name_hi || "").toLowerCase().includes(l) ||
          (s.name_en || "").toLowerCase().includes(l)
      ) || null
    );
  }

  /* --------------------- Load chats on mount --------------------- */
  useEffect(() => {
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) {
        const parsed = JSON.parse(raw);
        const loaded = Array.isArray(parsed.chats) ? parsed.chats : [];
        if (loaded.length > 0) {
          setChats(loaded);
          setActiveChatId(parsed.activeChatId || loaded[0].id);
          return;
        }
      }
    } catch (err) {
      console.error("Failed to load chats:", err);
    }

    const first = createNewChat();
    setChats([first]);
    setActiveChatId(first.id);
  }, [storageKey]);

  /* --------------------- Persist chats --------------------- */
  useEffect(() => {
    if (!chats.length) return;
    try {
      localStorage.setItem(storageKey, JSON.stringify({ chats, activeChatId }));
    } catch (err) {
      console.error("Failed to save chats:", err);
    }
  }, [chats, activeChatId, storageKey]);

  /* --------------------- Voice: Speak answer --------------------- */
  function handleSpeak(msgKey, msg) {
    try {
      // 1) If server audio_url present (Garhwali TTS)
      if (msg.audio_url) {
        if (speakingKey === msgKey && audioRef.current) {
          audioRef.current.pause();
          audioRef.current.currentTime = 0;
          audioRef.current = null;
          setSpeakingKey(null);
          return;
        }

        if (audioRef.current) {
          audioRef.current.pause();
          audioRef.current.currentTime = 0;
        }

        const audio = new Audio(
          msg.audio_url.startsWith("http")
            ? msg.audio_url
            : `${API_BASE}${msg.audio_url}`
        );
        audioRef.current = audio;
        setSpeakingKey(msgKey);

        audio.onended = () => {
          setSpeakingKey((curr) => (curr === msgKey ? null : curr));
          audioRef.current = null;
        };

        audio.play().catch((err) => {
          console.error("Failed to play TTS audio:", err);
          setSpeakingKey(null);
        });
        return;
      }

      // 2) Browser TTS fallback
      if (typeof window === "undefined" || !window.speechSynthesis) {
        alert(
          isHi
            ? "आपका ब्राउज़र वॉइस सपोर्ट नहीं करता।"
            : "Your browser doesn't support TTS."
        );
        return;
      }

      if (speakingKey === msgKey) {
        window.speechSynthesis.cancel();
        setSpeakingKey(null);
        return;
      }

      const plainText = stripHtml(msg.text || "");
      if (!plainText.trim()) return;

      const utterance = new SpeechSynthesisUtterance(plainText);
      const hasDevanagari = /[\u0900-\u097F]/.test(plainText);
      const synth = window.speechSynthesis;

      let selectedVoice = null;

      if (msg.lang === "en" && !hasDevanagari) {
        utterance.lang = "en-IN";
        selectedVoice =
          voices.find((v) => v.lang?.toLowerCase().startsWith("en-in")) ||
          voices.find((v) => v.lang?.toLowerCase().startsWith("en")) ||
          null;
      } else {
        utterance.lang = "hi-IN";
        selectedVoice =
          voices.find((v) => v.lang?.toLowerCase().startsWith("hi")) ||
          voices.find((v) => v.lang?.toLowerCase().includes("hi-in")) ||
          null;
      }

      if (selectedVoice) utterance.voice = selectedVoice;

      synth.cancel();
      synth.speak(utterance);
      setSpeakingKey(msgKey);
      utterance.onend = () => setSpeakingKey(null);
    } catch (err) {
      console.error("TTS error:", err);
      setSpeakingKey(null);
    }
  }

  /* --------------------- Copy answer text --------------------- */
  async function handleCopy(msgKey, msg) {
    try {
      const plainText = stripHtml(msg.text || "");
      if (!plainText.trim()) return;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(plainText);
      } else {
        const textarea = document.createElement("textarea");
        textarea.value = plainText;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
      }

      setCopiedKey(msgKey);
      setTimeout(() => {
        setCopiedKey((curr) => (curr === msgKey ? null : curr));
      }, 1500);
    } catch (err) {
      console.error("Copy failed:", err);
      alert(isHi ? "कॉपी विफल हुआ।" : "Copy failed.");
    }
  }

  /* --------------------- Mic / Speech input --------------------- */
  function startListening() {
    try {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

      if (!SpeechRecognition) {
        alert(
          isHi
            ? "आपका ब्राउज़र वॉइस इनपुट सपोर्ट नहीं करता।"
            : "Your browser does not support voice input."
        );
        return;
      }

      const recognition = new SpeechRecognition();
      recognition.lang = "hi-IN";
      recognition.interimResults = false;

      recognition.onstart = () => setListening(true);
      recognition.onend = () => setListening(false);

      recognition.onresult = (event) => {
        const speechText = event.results?.[0]?.[0]?.transcript ?? "";
        if (!speechText) return;
        setInput((prev) =>
          prev ? `${prev.trimEnd()} ${speechText}` : speechText
        );
      };

      recognition.onerror = (err) => {
        console.error("Speech recognition error:", err);
        setListening(false);
        alert(
          (isHi ? "माइक त्रुटि: " : "Mic error: ") + (err?.error ?? "unknown")
        );
      };

      recognition.start();
    } catch (err) {
      console.error("Speech recognition exception:", err);
      setListening(false);
    }
  }

  /* --------------------- Chat management --------------------- */
  function handleNewChat() {
    const nc = createNewChat();
    setChats((prev) => [...prev, nc]);
    setActiveChatId(nc.id);
    setInput("");
    setSpeakingKey(null);
    setCopiedKey(null);
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  }

  function handleDeleteChat(chatId, e) {
    e.stopPropagation();
    setChats((prev) => {
      const filtered = prev.filter((c) => c.id !== chatId);
      if (filtered.length === 0) {
        const nc = createNewChat();
        setActiveChatId(nc.id);
        return [nc];
      }
      if (chatId === activeChatId) setActiveChatId(filtered[0].id);
      return filtered;
    });
  }

  function handleSelectChat(chatId) {
    setActiveChatId(chatId);
    setSpeakingKey(null);
    setCopiedKey(null);
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  }

  /* --------------------- Send message --------------------- */
  async function sendMessage() {
    const question = input.trim();
    if (!question || loading) return;
    if (!activeChatId || !activeChat) return;

    const prevMessages = messages || [];
    const historyForBackend = prevMessages.slice(-6).map((m) => ({
      role: m.from === "user" ? "user" : "assistant",
      content: stripHtml(m.text || ""),
    }));

    const userMeta = user
      ? {
          district: user.district || null,
          block: user.block || null,
          village_code: user.village_code || null,
          age: user.age || null,
          gender: user.gender || null,
          interest_tag: user.interest_tag || null,
          disability: user.disability || null,
          occupation: user.occupation || null,
          income_bracket: user.income_bracket || null,
          social_category: user.social_category || null,
        }
      : null;

    const userMsg = { from: "user", type: "text", text: question };
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === activeChatId
          ? {
              ...chat,
              title:
                chat.title === "New chat"
                  ? question.length > 30
                    ? question.slice(0, 30) + "..."
                    : question
                  : chat.title,
              messages: [...chat.messages, userMsg],
            }
          : chat
      )
    );

    setInput("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          ui_lang: uiLang,
          mode: "auto",
          history: historyForBackend,
          user_meta: userMeta,
        }),
      });

      if (!res.ok)
        throw new Error(`API error: ${res.status} ${res.statusText}`);

      const data = await res.json();
      const responseHtml = stripApplyReadMore(
        data.message || data.response || ""
      );
      const sources = Array.isArray(data.sources) ? data.sources : [];
      const cards = Array.isArray(data.cards) ? data.cards : [];
      const audioUrl = data.audio_url || null;

      let botMsg;
      if (cards.length > 0) {
        botMsg = {
          from: "bot",
          type: "answer+cards",
          text: responseHtml,
          cards,
          lang: uiLang,
          sources,
          audio_url: audioUrl,
        };
      } else {
        botMsg = {
          from: "bot",
          type: "answer",
          text: responseHtml,
          sources,
          lang: uiLang,
          audio_url: audioUrl,
        };
      }

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? { ...chat, messages: [...chat.messages, botMsg] }
            : chat
        )
      );
    } catch (err) {
      console.error(err);
      const errorMsg = {
        from: "bot",
        type: "text",
        text: isHi
          ? "माफ़ कीजिए, सर्वर से कनेक्शन नहीं हो पाया। कृपया थोड़ी देर बाद पुनः प्रयास करें।"
          : "Sorry, couldn't connect to the server. Please try again later.",
      };
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? { ...chat, messages: [...chat.messages, errorMsg] }
            : chat
        )
      );
    } finally {
      setLoading(false);
    }
  }

  if (!activeChat) return null;

  // Simple grouping for "Today" / "Yesterday" in sidebar (visual only)
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  const todayChats = chats.filter((c) => {
    const d = new Date(c.createdAt);
    d.setHours(0, 0, 0, 0);
    return d.getTime() === today.getTime();
  });

  const yesterdayChats = chats.filter((c) => {
    const d = new Date(c.createdAt);
    d.setHours(0, 0, 0, 0);
    return d.getTime() === yesterday.getTime();
  });

  const otherChats = chats.filter(
    (c) => !todayChats.includes(c) && !yesterdayChats.includes(c)
  );

  // Static three-column grid (left + center + right)
  const gridCols = "grid-cols-[260px_1fr_320px]";

  /* ======================= UI LAYOUT ======================= */
  return (
    <>
      <div className="flex h-screen w-full flex-col bg-background-light dark:bg-background-dark font-display text-text-light dark:text-text-dark overflow-hidden">
        {/* (Header handled by outer layout / navbar, so omitted here) */}

        {/* ================= MAIN CONTENT GRID ================= */}
        <main
          className={`grid flex-1 overflow-hidden ${gridCols} gap-x-4 transition-[grid-template-columns] duration-200`}
        >
          {/* =============== LEFT COLUMN (Chat List) =============== */}
          <aside className="flex flex-col border-r border-black/10 dark:border-white/10 bg-background-light dark:bg-background-dark overflow-hidden">
            {/* Top: New chat */}
            <div className="p-3 flex items-center gap-2 border-b border-black/5 dark:border-white/5 shrink-0">
              <button
                onClick={handleNewChat}
                className="flex flex-1 items-center justify-center gap-2 rounded-lg h-10 bg-primary px-4 text-sm font-bold text-white hover:bg-primary/90"
              >
                <span className="material-symbols-outlined text-xl">add</span>
                <span>New chat</span>
              </button>
            </div>

            {/* Chat list scrollable */}
            <div className="flex flex-1 flex-col gap-4 overflow-y-auto px-2 py-3">
              {todayChats.length > 0 && (
                <div>
                  <h3 className="px-2 text-xs font-semibold uppercase text-text-subtle-light dark:text-text-subtle-dark">
                    Today
                  </h3>
                  <ul className="mt-1 flex flex-col gap-1">
                    {todayChats.map((chat) => (
                      <li key={chat.id}>
                        <button
                          onClick={() => handleSelectChat(chat.id)}
                          className={`group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm ${
                            chat.id === activeChatId
                              ? "bg-primary/10 dark:bg-primary/20 text-primary dark:text-green-300 font-medium"
                              : "text-text-light dark:text-text-dark hover:bg-black/5 dark:hover:bg-white/5"
                          }`}
                        >
                          <span className="material-symbols-outlined text-base text-text-subtle-light">
                            chat_bubble
                          </span>
                          <span className="flex-1 truncate">{chat.title}</span>
                          <span
                            className="material-symbols-outlined text-[16px] text-red-400 opacity-0 group-hover:opacity-100"
                            onClick={(e) => handleDeleteChat(chat.id, e)}
                          >
                            delete
                          </span>
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {yesterdayChats.length > 0 && (
                <div>
                  <h3 className="px-2 text-xs font-semibold uppercase text-text-subtle-light dark:text-text-subtle-dark">
                    Yesterday
                  </h3>
                  <ul className="mt-1 flex flex-col gap-1">
                    {yesterdayChats.map((chat) => (
                      <li key={chat.id}>
                        <button
                          onClick={() => handleSelectChat(chat.id)}
                          className={`group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm ${
                            chat.id === activeChatId
                              ? "bg-primary/10 dark:bg-primary/20 text-primary dark:text-green-300 font-medium"
                              : "text-text-light dark:text-text-dark hover:bg-black/5 dark:hover:bg-white/5"
                          }`}
                        >
                          <span className="material-symbols-outlined text-base text-text-subtle-light">
                            chat_bubble
                          </span>
                          <span className="flex-1 truncate">{chat.title}</span>
                          <span
                            className="material-symbols-outlined text-[16px] text-red-400 opacity-0 group-hover:opacity-100"
                            onClick={(e) => handleDeleteChat(chat.id, e)}
                          >
                            delete
                          </span>
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {otherChats.length > 0 && (
                <div>
                  <h3 className="px-2 text-xs font-semibold uppercase text-text-subtle-light dark:text-text-subtle-dark">
                    Older
                  </h3>
                  <ul className="mt-1 flex flex-col gap-1">
                    {otherChats.map((chat) => (
                      <li key={chat.id}>
                        <button
                          onClick={() => handleSelectChat(chat.id)}
                          className={`group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm ${
                            chat.id === activeChatId
                              ? "bg-primary/10 dark:bg-primary/20 text-primary dark:text-green-300 font-medium"
                              : "text-text-light dark:text-text-dark hover:bg-black/5 dark:hover:bg-white/5"
                          }`}
                        >
                          <span className="material-symbols-outlined text-base text-text-subtle-light">
                            chat_bubble
                          </span>
                          <span className="flex-1 truncate">{chat.title}</span>
                          <span
                            className="material-symbols-outlined text-[16px] text-red-400 opacity-0 group-hover:opacity-100"
                            onClick={(e) => handleDeleteChat(chat.id, e)}
                          >
                            delete
                          </span>
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </aside>

          {/* =============== CENTER COLUMN (Chat Interface) =============== */}
          <div className="flex flex-col bg-white/50 dark:bg-black/20 overflow-hidden">
            {/* Chat Header (conversation title + bot language toggle) */}
            <div className="flex h-14 shrink-0 items-center justify-between border-b border-black/10 dark:border-white/10 px-4">
              <h2 className="font-semibold truncate">
                {activeChat?.title || "Panchayat Sahayika"}
              </h2>
              <div className="flex items-center gap-2 text-xs">
                <button
                  onClick={() => setUiLang("hi")}
                  className={`rounded-full h-8 px-3 font-bold border text-xs ${
                    uiLang === "hi"
                      ? "bg-primary text-white border-primary"
                      : "bg-black/5 dark:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark border-transparent"
                  }`}
                >
                  हिन्दी
                </button>
                <button
                  onClick={() => setUiLang("en")}
                  className={`rounded-full h-8 px-3 font-bold border text-xs ${
                    uiLang === "en"
                      ? "bg-primary text-white border-primary"
                      : "bg-black/5 dark:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark border-transparent"
                  }`}
                >
                  English
                </button>
                <button
                  onClick={() => setUiLang("garhwali")}
                  className={`rounded-full h-8 px-3 font-bold border text-xs ${
                    uiLang === "garhwali"
                      ? "bg-primary text-white border-primary"
                      : "bg-black/5 dark:bg:white/5 text-text-subtle-light dark:text-text-subtle-dark border-transparent"
                  }`}
                >
                  Garhwali
                </button>
              </div>
            </div>

            {/* Message Area – centered column, scrollable */}
            <div className="flex-1 overflow-y-auto px-4 md:px-6 py-4 md:py-6">
              <div className="space-y-6 max-w-3xl mx-auto">
                {messages.map((msg, idx) => {
                  const msgKey = `${activeChatId}-${idx}`;

                  // USER MESSAGE
                  if (msg.from === "user") {
                    const initial = (user?.username || "U")
                      .charAt(0)
                      .toUpperCase();
                    return (
                      <div
                        key={msgKey}
                        className="flex items-end justify-end gap-3"
                      >
                        <div className="flex w-full flex-col items-end gap-1">
                          <p className="text-xs text-text-subtle-light dark:text-text-subtle-dark">
                            {isHi ? "आप" : "You"}
                          </p>
                          <p className="rounded-2xl rounded-br-lg bg-primary px-4 py-2.5 text-base text-white">
                            {msg.text}
                          </p>
                        </div>
                        <div className="size-9 shrink-0 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                          {initial}
                        </div>
                      </div>
                    );
                  }

                  // BOT: ANSWER + CARDS
                  if (msg.type === "answer+cards") {
                    return (
                      <div key={msgKey} className="flex items-end gap-3">
                        {/* Bot avatar */}
                        <div className="size-9 shrink-0 rounded-full bg-primary/20 flex items-center justify-center">
                          <div className="size-6 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold">
                            S
                          </div>
                        </div>

                        <div className="flex w-full flex-col items-start gap-1">
                          <p className="text-xs text-text-subtle-light dark:text-text-subtle-dark">
                            Sahayika Bot
                          </p>

                          {/* Little text bubble if any intro text */}
                          {msg.text && (
                            <p className="rounded-2xl rounded-bl-lg bg-bot-bubble-light dark:bg-bot-bubble-dark px-4 py-2.5 text-base text-text-light dark:text-text-dark whitespace-pre-line">
                              <span
                                dangerouslySetInnerHTML={{ __html: msg.text }}
                              />
                            </p>
                          )}

                          {/* Main AnswerCard like in reference */}
                          <div className="mt-2 w-full">
                            <AnswerCard>
                              <div className="flex items-center justify-end gap-1 border-b border-black/10 dark:border-white/10 px-3 py-1.5">
                                <button
                                  onClick={() => handleSpeak(msgKey, msg)}
                                  className="flex size-7 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark"
                                >
                                  {speakingKey === msgKey ? (
                                    <span className="material-symbols-outlined text-base">
                                      stop
                                    </span>
                                  ) : (
                                    <span className="material-symbols-outlined text-base">
                                      volume_up
                                    </span>
                                  )}
                                </button>
                                <button
                                  onClick={() => handleCopy(msgKey, msg)}
                                  className="flex size-7 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark"
                                >
                                  <span className="material-symbols-outlined text-base">
                                    content_copy
                                  </span>
                                </button>
                                {copiedKey === msgKey && (
                                  <span className="text-[10px] text-gray-500">
                                    {isHi ? "कॉपी हुआ" : "Copied"}
                                  </span>
                                )}
                              </div>

                              {/* Cards from backend (scheme tiles) */}
                              <div className="p-4 space-y-2">
                                {msg.cards?.map((c, i) => {
                                  const label = c.title_hi || c.title;
                                  const hasData = getSchemeByLabel(label);
                                  if (!hasData) return null;

                                  return (
                                    <button
                                      key={i}
                                      onClick={() =>
                                        setSelectedScheme(hasData)
                                      }
                                      className="w-full text-left rounded-2xl bg-card-light dark:bg-card-dark border border-black/10 dark:border-white/10 px-3 py-2 hover:bg-black/5 dark:hover:bg-white/5 transition cursor-pointer"
                                    >
                                      <div className="text-sm font-semibold text-text-light dark:text-text-dark">
                                        {c.title}
                                      </div>
                                      {c.subtitle && (
                                        <div className="text-[11px] text-text-subtle-light dark:text-text-subtle-dark mt-0.5">
                                          {c.subtitle}
                                        </div>
                                      )}
                                    </button>
                                  );
                                })}
                              </div>
                            </AnswerCard>
                          </div>

                          {/* Source pills */}
                          {msg.sources?.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-2">
                              {msg.sources.map((s, i) => {
                                const label = s.name_hi || s.name_en;
                                const hasData = findScheme(label);
                                if (!hasData) return null;
                                return (
                                  <button
                                    key={i}
                                    onClick={() => setSelectedScheme(hasData)}
                                    className="px-3 py-1 bg-green-50 border border-green-200 text-green-700 text-[10px] rounded-full hover:bg-green-100"
                                  >
                                    {label}
                                  </button>
                                );
                              })}
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  }

                  // BOT: NORMAL ANSWER / TEXT
                  if (msg.type === "answer" || msg.type === "text") {
                    return (
                      <div key={msgKey} className="flex items-end gap-3">
                        <div className="size-9 shrink-0 rounded-full bg-primary/20 flex items-center justify-center">
                          <div className="size-6 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold">
                            S
                          </div>
                        </div>

                        <div className="flex w-full flex-col items-start gap-1">
                          <p className="text-xs text-text-subtle-light dark:text-text-subtle-dark">
                            Sahayika Bot
                          </p>

                          <AnswerCard>
                            <div className="flex items-center justify-end gap-1 border-b border-black/10 dark:border-white/10 px-3 py-1.5">
                              <button
                                onClick={() => handleSpeak(msgKey, msg)}
                                className="flex size-7 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark"
                              >
                                {speakingKey === msgKey ? (
                                  <span className="material-symbols-outlined text-base">
                                    stop
                                  </span>
                                ) : (
                                  <span className="material-symbols-outlined text-base">
                                    volume_up
                                  </span>
                                )}
                              </button>
                              <button
                                onClick={() => handleCopy(msgKey, msg)}
                                className="flex size-7 items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-subtle-light dark:text-text-subtle-dark"
                              >
                                <span className="material-symbols-outlined text-base">
                                  content_copy
                                </span>
                              </button>
                              {copiedKey === msgKey && (
                                <span className="text-[10px] text-gray-500">
                                  {isHi ? "कॉपी हुआ" : "Copied"}
                                </span>
                              )}
                            </div>

                            <div
                              className="p-4 text-sm leading-relaxed whitespace-pre-line text-text-light dark:text-text-dark"
                              dangerouslySetInnerHTML={{ __html: msg.text }}
                            />

                            {msg.sources?.length > 0 && (
                              <div className="border-t border-black/10 dark:border-white/10 px-4 py-3 flex flex-wrap gap-2">
                                {msg.sources.map((s, i) => {
                                  const label = s.name_hi || s.name_en;
                                  const hasData = findScheme(label);
                                  if (!hasData) return null;
                                  return (
                                    <button
                                      key={i}
                                      onClick={() =>
                                        setSelectedScheme(hasData)
                                      }
                                      className="px-3 py-1 bg-green-50 border border-green-200 text-green-700 text-[10px] rounded-full hover:bg-green-100"
                                    >
                                      {label}
                                    </button>
                                  );
                                })}
                              </div>
                            )}
                          </AnswerCard>
                        </div>
                      </div>
                    );
                  }

                  // Fallback
                  return (
                    <div key={msgKey} className="flex items-end gap-3">
                      <div className="size-9 shrink-0 rounded-full bg-primary/20 flex items-center justify-center">
                        <div className="size-6 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold">
                          S
                        </div>
                      </div>
                      <div className="flex w-full flex-col items-start gap-1">
                        <p className="text-xs text-text-subtle-light dark:text-text-subtle-dark">
                          Sahayika Bot
                        </p>
                        <p className="rounded-2xl rounded-bl-lg bg-bot-bubble-light dark:bg-bot-bubble-dark px-4 py-2.5 text-base text-text-light dark:text-text-dark">
                          {msg.text}
                        </p>
                      </div>
                    </div>
                  );
                })}

                {loading && (
                  <div className="flex items-center gap-2 text-xs text-gray-600">
                    <div className="size-6 rounded-full border-2 border-primary border-t-transparent animate-spin" />
                    <span>{isHi ? "सोच रही हूँ..." : "Thinking…"}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Fixed Chat Input Footer (center column bottom, centered width) */}
            <div className="shrink-0 border-t border-black/10 dark:border-white/10 px-4 py-3 bg-background-light dark:bg-background-dark">
              <div className="relative flex items-center max-w-3xl mx-auto">
                <button
                  onClick={startListening}
                  className="absolute left-2 flex size-8 items-center justify-center rounded-full hover:bg-black/10 dark:hover:bg-white/10"
                >
                  {listening ? (
                    <span className="material-symbols-outlined text-text-subtle-light dark:text-text-subtle-dark">
                      stop
                    </span>
                  ) : (
                    <span className="material-symbols-outlined text-text-subtle-light dark:text-text-subtle-dark">
                      mic
                    </span>
                  )}
                </button>

                <textarea
                  rows={1}
                  className="w-full resize-none rounded-xl border-0 bg-black/5 dark:bg-white/5 py-2.5 pl-12 pr-12 text-base focus:ring-2 focus:ring-primary"
                  placeholder={
                    isHi
                      ? "अपना प्रश्न पूछें... / Ask your question..."
                      : "Ask your question... / अपना प्रश्न पूछें..."
                  }
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      sendMessage();
                    }
                  }}
                />

                <button
                  onClick={sendMessage}
                  disabled={loading || !input.trim()}
                  className="absolute right-2 flex size-8 items-center justify-center rounded-full bg-primary text-white hover:bg-primary/90 disabled:opacity-50"
                >
                  <span className="material-symbols-outlined">send</span>
                </button>
              </div>
              {listening && (
                <div className="mt-1 text-[11px] text-green-700 max-w-3xl mx-auto">
                  🎙️ {isHi ? "मैं आपकी बात सुन रही हूँ..." : "I'm listening..."}
                </div>
              )}
            </div>
          </div>

          {/* =============== RIGHT COLUMN (Global RightSidebar) =============== */}
          <aside className="flex flex-col border-l border-black/10 dark:border-white/10 bg-background-light dark:bg-background-dark overflow-y-auto px-3 py-4">
            <div className="max-w-xs mx-auto w-full">
              <RightSidebar />
            </div>
          </aside>
        </main>
      </div>

      {/* Scheme Modal */}
      {selectedScheme && (
        <SchemeDetailsModal
          scheme={selectedScheme}
          onClose={() => setSelectedScheme(null)}
        />
      )}
    </>
  );
}

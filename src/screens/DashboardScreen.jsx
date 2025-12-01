import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth.jsx";
import { useLanguage } from "../context/LanguageContext.jsx";
import SCHEMES from "../data/samaj_kalyan_vibhag_clean_typed.json";

/* ---------------------- API URLs ---------------------- */

const CHAT_API = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";
const TRAIN_API = "http://127.0.0.1:7000";
const GRAM_API = "http://127.0.0.1:5000";

/* ---------------------- HELPERS ---------------------- */

function clean(txt) {
  return String(txt || "")
    .toLowerCase()
    .replace(/[()]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function findScheme(card) {
  const raw =
    card.title ||
    card.name_hi ||
    card.name_en ||
    card.scheme_name_hi ||
    card.scheme_name_en ||
    card.subtitle ||
    "";
  if (!raw) return null;

  const parts = clean(raw)
    .split("/")
    .map((p) => p.trim())
    .filter(Boolean);

  if (parts.length === 0) parts.push(clean(raw));

  for (const s of SCHEMES) {
    const hi = clean(s.name_hi);
    const en = clean(s.name_en);

    for (const p of parts) {
      if (!p) continue;

      if (hi && (p === hi || hi.startsWith(p) || p.startsWith(hi))) return s;
      if (en && (p === en || en.startsWith(p) || p.startsWith(en))) return s;
    }
  }
  return null;
}

/* ---------------------- GOOGLE IMAGE FETCHER ---------------------- */

async function getGoogleImage(keyword) {
  try {
    if (!keyword) keyword = "India government scheme";

    const API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;
    const CX = import.meta.env.VITE_GOOGLE_CSE_ID;

    const url = `https://www.googleapis.com/customsearch/v1?key=${API_KEY}&cx=${CX}&searchType=image&q=${encodeURIComponent(
      keyword
    )}&num=1`;

    const res = await fetch(url);
    const data = await res.json();

    if (data.items && data.items.length > 0 && data.items[0].link) {
      return data.items[0].link;
    }
    return null;
  } catch (e) {
    console.error("Google Image fetch error:", e);
    return null;
  }
}

/* ---------------------- MODAL ---------------------- */

function FinderStyleModal({ scheme, lang, onClose }) {
  if (!scheme) return null;
  const isHi = lang === "hi";

  const t_hi = scheme.name_hi || scheme.scheme_name_hi || scheme.title_hi || "";
  const t_en = scheme.name_en || scheme.scheme_name_en || scheme.title_en || "";
  const title = isHi ? t_hi || t_en : t_en || t_hi;
  const sub = isHi ? t_en : t_hi;

  const desc_hi =
    scheme.long_description_hi ||
    scheme.description_hi ||
    scheme.short_desc_hi ||
    "";
  const desc_en =
    scheme.long_description_en ||
    scheme.description_en ||
    scheme.short_desc_en ||
    "";

  return (
    <div
      className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center px-4 mb-20"
      onClick={onClose}
    >
      <div
        className="w-full max-w-3xl bg-white dark:bg-[#2a2a2a] rounded-3xl shadow-xl p-6 space-y-4 max-h-[85vh] overflow-y-auto relative scrollbar-hide"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-xl text-gray-500 dark:text-gray-300 hover:text-gray-700"
        >
          ✕
        </button>

        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            {title}
          </h2>

          {sub && (
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {sub}
            </p>
          )}

          <p className="text-xs text-gray-400 mt-2">
            {[
              scheme.type?.includes("program")
                ? isHi
                  ? "प्रोग्राम"
                  : "Programme"
                : isHi
                ? "योजना"
                : "Scheme",
              scheme.category,
              scheme.department,
            ]
              .filter(Boolean)
              .join(" • ")}
          </p>
        </div>

        {desc_hi && (
          <div>
            <h3 className="text-xs text-gray-600 dark:text-gray-300 font-semibold">
              विवरण (Hindi)
            </h3>
            <p className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-line">
              {desc_hi}
            </p>
          </div>
        )}

        {desc_en && (
          <div>
            <h3 className="text-xs text-gray-600 dark:text-gray-300 font-semibold">
              Description (English)
            </h3>
            <p className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-line">
              {desc_en}
            </p>
          </div>
        )}

        <div className="border-t border-gray-300 dark:border-gray-700 pt-3">
          <h3 className="text-xs font-semibold text-gray-500 mb-2">
            {isHi ? "सभी JSON फ़ील्ड" : "All JSON Fields"}
          </h3>

          <dl className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {Object.entries(scheme)
              .filter(([_, v]) => v !== null && v !== "")
              .map(([k, v]) => (
                <div key={k}>
                  <dt className="uppercase text-[10px] text-gray-400">{k}</dt>
                  <dd className="text-[11px] text-gray-800 dark:text-gray-300 whitespace-pre-line">
                    {String(v)}
                  </dd>
                </div>
              ))}
          </dl>
        </div>
      </div>
    </div>
  );
}

/* ---------------------- DEFICIT LABEL ---------------------- */

function deficitLabel(k, isHi) {
  const m = k.toLowerCase();
  if (isHi) {
    if (m.includes("road")) return "सड़कें";
    if (m.includes("health")) return "स्वास्थ्य";
    if (m.includes("education")) return "शिक्षा";
    if (m.includes("water")) return "पेयजल";
    if (m.includes("sanitation")) return "स्वच्छता";
    if (m.includes("electric")) return "बिजली";
    if (m.includes("internet")) return "इंटरनेट";
    if (m.includes("housing")) return "आवास";
    if (k === "digital") return "डिजिटल";
    return k;
  }
  return k.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

/* ---------------------- MAIN DASHBOARD ---------------------- */

export default function DashboardScreen() {
  const { user, token } = useAuth();
  const { lang } = useLanguage();
  const navigate = useNavigate();
  const isHi = lang === "hi";

  const [schemes, setSchemes] = useState([]);
  const [schemeImages, setSchemeImages] = useState({});
  const [trainings, setTrainings] = useState([]);
  const [village, setVillage] = useState(null);
  const [selectedScheme, setSelectedScheme] = useState(null);

  /* ---------------------- Fetch Recommended Schemes + Images ---------------------- */
  useEffect(() => {
    if (!token) return;

    fetch(`${CHAT_API}/user/recommended-schemes`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then(async (d) => {
        const arr = Array.isArray(d) ? d : d.items || [];
        setSchemes(arr);

        const imgMap = {};

        for (const s of arr) {
          const keyword =
            s.name_en ||
            s.name_hi ||
            s.scheme_name_en ||
            s.scheme_name_hi ||
            "India government scheme";

          imgMap[s.id || keyword] = await getGoogleImage(keyword);
        }

        setSchemeImages(imgMap);
      })
      .catch(() => setSchemes([]));
  }, [token]);

  /* ---------------------- Fetch Trainings + Village Data ---------------------- */

  useEffect(() => {
    if (!user) return;

    const params = new URLSearchParams();
    if (user.district) params.append("district", user.district);
    if (user.block) params.append("block", user.block);

    fetch(`${TRAIN_API}/trainings?${params}`)
      .then((r) => r.json())
      .then((d) => setTrainings(d.items || []))
      .catch(() => setTrainings([]));

    if (user.village_code) {
      fetch(`${GRAM_API}/api/village_detail?village_code=${user.village_code}`)
        .then((r) => r.json())
        .then(setVillage)
        .catch(() => setVillage(null));
    }
  }, [user]);

  if (!user)
    return (
      <div className="p-6 text-center">
        {isHi ? "कृपया लॉगिन करें।" : "Please login."}
      </div>
    );

  return (
    <div className="p-8 ml-20 mr-20">
      <div className="flex flex-col gap-y-12">
        {/* GREETING */}
        <h1 className="text-4xl font-extrabold tracking-tight">
          {isHi ? "नमस्ते," : "Namaste,"} {user.full_name || user.username}
        </h1>

        {/* ---------------------- RECOMMENDED SCHEMES ---------------------- */}
        <section>
          <h2 className="text-2xl font-bold mb-4">
            {isHi ? "सुझाई गई योजनाएँ" : "Recommended Schemes"}
          </h2>

          <div className="flex overflow-x-auto gap-4 pb-3 scrollbar-hide">
            {schemes.length === 0 && (
              <p className="text-gray-500 text-sm">
                {isHi
                  ? "अभी कोई योजना उपलब्ध नहीं।"
                  : "No recommendations found."}
              </p>
            )}

            {/* {schemes.map((s, i) => {
              const full = findScheme(s) || s;

              const title = isHi
                ? full.name_hi || full.name_en
                : full.name_en || full.name_hi;

              const short =
                full.description_en ||
                full.description_hi ||
                full.short_desc_en ||
                full.short_desc_hi ||
                "";

              const keyword =
                full.name_en ||
                full.name_hi ||
                full.scheme_name_en ||
                full.scheme_name_hi ||
                "India government scheme";

              const imgKey = s.id || keyword;
              const img =
                schemeImages[imgKey] ||
                "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg";

              return (
                <button
                  key={i}
                  onClick={() => setSelectedScheme(full)}
                  className="min-w-64 bg-white dark:bg-[#2a2a2a]/60 rounded-2xl shadow-subtle border border-black/10 dark:border-white/10 p-4 text-left hover:shadow-lg transition"
                >
                   <img
                    src={img}
                    className="w-full h-36 object-cover rounded-xl mb-3"
                    alt={title}
                  /> 
                  <p className="font-bold text-gray-900 dark:text-white">{title}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                    {short.slice(0, 80)}...
                  </p>
                </button>
              );
            })} */}

            {schemes.map((s, i) => {
              const full = findScheme(s) || s;

              const title = isHi
                ? full.name_hi || full.name_en
                : full.name_en || full.name_hi;

              const short =
                full.description_en ||
                full.description_hi ||
                full.short_desc_en ||
                full.short_desc_hi ||
                "";

              return (
                <button
                  key={i}
                  onClick={() => setSelectedScheme(full)}
                  className="min-w-64 bg-white dark:bg-[#2a2a2a]/60 rounded-2xl shadow-subtle border border-black/10 dark:border-white/10 p-4 text-left hover:shadow-lg transition"
                >
                  {/* IMAGE REMOVED */}
                  {/* 
      <img
        src={img}
        className="w-full h-36 object-cover rounded-xl mb-3"
        alt={title}
      />
      */}

                  <p className="font-bold text-gray-900 dark:text-white">
                    {title}
                  </p>

                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                    {short.slice(0, 80)}...
                  </p>
                </button>
              );
            })}
          </div>
        </section>

        {/* ---------------------- TRAININGS ---------------------- */}
        <section>
          <h2 className="text-2xl font-bold mb-4">
            {isHi
              ? "आपके क्षेत्र में प्रशिक्षण"
              : "Upcoming Trainings in Your Area"}
          </h2>

          {trainings.length === 0 ? (
            <p className="text-gray-500">
              {isHi ? "कोई प्रशिक्षण नहीं।" : "No trainings found."}
            </p>
          ) : (
            <div className="grid gap-3">
              {trainings.slice(0, 4).map((t, i) => (
                <div
                  key={i}
                  className="p-4 bg-white dark:bg-[#2a2a2a]/60 rounded-2xl shadow-subtle border border-black/10 dark:border-white/10"
                >
                  <p className="font-semibold">{t.training_name}</p>
                  <p className="text-sm text-gray-500">{t.org_institute}</p>
                  <p className="text-sm">
                    🗓 {t.start_date} – {t.end_date}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* ---------------------- VILLAGE INFRA ---------------------- */}
        <section>
          <h2 className="text-2xl font-bold mb-4">
            {isHi
              ? "गाँव की आधारभूत सुविधाएँ"
              : "Village Infrastructure Status"}
          </h2>

          {!village ? (
            <p className="text-gray-500">
              {isHi
                ? "गाँव की जानकारी उपलब्ध नहीं।"
                : "Village data unavailable."}
            </p>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {Object.entries(village.deficits).map(([k, v]) => (
                <div
                  key={k}
                  className="p-4 bg-white dark:bg-[#2a2a2a]/60 rounded-2xl shadow-subtle border border-black/10 dark:border-white/10"
                >
                  <p className="font-semibold">{deficitLabel(k, isHi)}</p>
                  <p>
                    {isHi ? "स्कोर" : "Score"}: {v.score.toFixed(2)}
                  </p>
                  <p
                    className={
                      v.level === "High"
                        ? "text-red-600 font-bold"
                        : v.level === "Medium"
                        ? "text-orange-500 font-bold"
                        : "text-green-600 font-bold"
                    }
                  >
                    {isHi
                      ? v.level === "High"
                        ? "उच्च कमी"
                        : v.level === "Medium"
                        ? "मध्यम कमी"
                        : "कम कमी"
                      : `${v.level} deficit`}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* ---------------------- MODAL ---------------------- */}
        {selectedScheme && (
          <FinderStyleModal
            scheme={selectedScheme}
            lang={lang}
            onClose={() => setSelectedScheme(null)}
          />
        )}

        {/* ---------------------- QUICK TOOLS ---------------------- */}
        <section>
          <div className="grid grid-cols-3 gap-4">
            <button
              onClick={() => navigate("/chat")}
              className="flex flex-col items-center bg-white dark:bg-[#2a2a2a]/60 p-6 rounded-2xl shadow-subtle hover:shadow-md"
            >
              <span className="material-symbols-outlined text-4xl text-primary">
                forum
              </span>
              <p className="font-bold mt-2">{isHi ? "पूछें" : "Ask (Chat)"}</p>
            </button>

            <button
              onClick={() => navigate("/finder")}
              className="flex flex-col items-center bg-white dark:bg-[#2a2a2a]/60 p-6 rounded-2xl shadow-subtle hover:shadow-md"
            >
              <span className="material-symbols-outlined text-4xl text-primary">
                search
              </span>
              <p className="font-bold mt-2">
                {isHi ? "योजनाएँ खोजें" : "Find Schemes"}
              </p>
            </button>

            <button
              onClick={() => navigate("/my-panchayat")}
              className="flex flex-col items-center bg-white dark:bg-[#2a2a2a]/60 p-6 rounded-2xl shadow-subtle hover:shadow-md"
            >
              <span className="material-symbols-outlined text-4xl text-primary">
                holiday_village
              </span>
              <p className="font-bold mt-2">
                {isHi ? "मेरी पंचायत" : "My Panchayat"}
              </p>
            </button>
          </div>
        </section>
      </div>
      <style>
        {`
    .scrollbar-hide::-webkit-scrollbar {
      display: none;
    }
    .scrollbar-hide {
      -ms-overflow-style: none;  /* IE and Edge */
      scrollbar-width: none;      /* Firefox */
    }
  `}
      </style>
    </div>
  );
}

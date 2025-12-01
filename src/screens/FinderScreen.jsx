// src/screens/FinderScreen.jsx
import React, { useMemo, useState } from "react";
import { useLanguage } from "../context/LanguageContext.jsx";
import RightSidebar from "../components/layout/RightSidebar.jsx";

import SCHEMES from "../data/samaj_kalyan_vibhag_clean_typed.json";

/* ---------------------------------------------------
   TYPE NORMALIZATION
--------------------------------------------------- */
function normalizeType(item) {
  const raw = (item?.type || "").toLowerCase();

  if (raw.includes("scheme")) return "scheme";
  if (raw.includes("programme") || raw.includes("program")) return "programme";

  const blob = [
    item?.name_en,
    item?.name_hi,
    item?.description_en,
    item?.description_hi,
    item?.category,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

  const programmeHints = [
    "programme",
    "program",
    "training",
    "campaign",
    "awareness",
    "workshop",
    "skill",
    "कार्यक्रम",
    "प्रशिक्षण",
    "अभियान",
    "जागरूकता",
    "कौशल",
  ];

  const schemeHints = [
    "scheme",
    "yojana",
    "mission",
    "plan",
    "assistance",
    "subsidy",
    "pension",
    "insurance",
    "housing",
    "loan",
    "employment",
    "योजना",
    "अनुदान",
    "कल्याण",
  ];

  if (programmeHints.some((k) => blob.includes(k))) return "programme";
  if (schemeHints.some((k) => blob.includes(k))) return "scheme";

  return "scheme";
}

function countByType(list) {
  let scheme = 0,
    programme = 0;
  for (const s of list) {
    const t = normalizeType(s);
    if (t === "programme") programme++;
    else scheme++;
  }
  return { scheme, programme };
}

/* ---------------------------------------------------
   MAIN SCREEN
--------------------------------------------------- */
export default function FinderScreen() {
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [department, setDepartment] = useState("");
  const [serviceType, setServiceType] = useState("");
  const [selectedScheme, setSelectedScheme] = useState(null);

  /* ---------- Categories & Departments ---------- */
  const { categories, departments } = useMemo(() => {
    const cats = new Set();
    const deps = new Set();

    SCHEMES.forEach((s) => {
      if (s.category) cats.add(String(s.category).trim());
      if (s.department) deps.add(String(s.department).trim());
    });

    return {
      categories: [...cats].sort(),
      departments: [...deps].sort(),
    };
  }, []);

  const typeCounts = useMemo(() => countByType(SCHEMES), []);

  /* ---------- FILTERED RESULTS ---------- */
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();

    return SCHEMES.filter((s) => {
      const matchQuery = !q
        ? true
        : [s.name_hi, s.name_en, s.description_hi, s.description_en]
            .filter(Boolean)
            .some((t) => t.toLowerCase().includes(q));

      const cat = s.category || "";
      const dept = s.department || "";
      const t = normalizeType(s);

      return (
        matchQuery &&
        (!category || category === cat) &&
        (!department || department === dept) &&
        (!serviceType || t === serviceType)
      );
    });
  }, [query, category, department, serviceType]);

  const hasActive =
    query || category || department || serviceType ? true : false;

  const clearAll = () => {
    setQuery("");
    setCategory("");
    setDepartment("");
    setServiceType("");
  };

  /* ---------------------------------------------------
     MODAL CONTENT — ALL JSON FIELDS INCLUDED
  --------------------------------------------------- */
  const renderDetailsModal = (scheme) => {
    if (!scheme) return null;

    const t_hi =
      scheme.name_hi || scheme.scheme_name_hi || scheme.title_hi || "";
    const t_en =
      scheme.name_en || scheme.scheme_name_en || scheme.title_en || "";

    const title = isHi
      ? t_hi || t_en || "अनाम योजना"
      : t_en || t_hi || "Unnamed Scheme";
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
        className="
          w-full max-w-3xl
          bg-white dark:bg-[#2a2a2a] 
          rounded-3xl shadow-xl 
          p-6 space-y-4 
          max-h-[85vh]
          overflow-y-auto
        "
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              {title}
            </h2>
            {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}

            <p className="text-xs text-gray-500 mt-2">
              {[
                normalizeType(scheme) === "programme"
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

          <button
            className="text-gray-500 hover:text-gray-700 text-xl"
            onClick={() => setSelectedScheme(null)}
          >
            ✕
          </button>
        </div>

        {/* HI Description */}
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

        {/* EN Description */}
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

        {scheme.eligibility && (
          <div>
            <h3 className="text-xs font-semibold text-gray-700 dark:text-gray-300">
              {isHi ? "पात्रता" : "Eligibility"}
            </h3>
            <p className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-line">
              {scheme.eligibility}
            </p>
          </div>
        )}

        {scheme.benefit && (
          <div>
            <h3 className="text-xs font-semibold text-gray-700 dark:text-gray-300">
              {isHi ? "लाभ" : "Benefit"}
            </h3>
            <p className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-line">
              {scheme.benefit}
            </p>
          </div>
        )}

        {scheme.apply_process && (
          <div>
            <h3 className="text-xs font-semibold text-gray-700 dark:text-gray-300">
              {isHi ? "आवेदन प्रक्रिया" : "Apply Process"}
            </h3>
            <p className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-line">
              {scheme.apply_process}
            </p>
          </div>
        )}

        {/* All JSON fields */}
        <div className="border-t border-gray-300 dark:border-gray-700 pt-3">
          <h3 className="text-xs font-semibold text-gray-600 mb-2">
            {isHi ? "सभी JSON फ़ील्ड" : "All JSON Fields"}
          </h3>

          <dl className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {Object.entries(scheme)
              .filter(([_, v]) => v !== null && v !== "")
              .map(([k, v]) => (
                <div key={k}>
                  <dt className="uppercase text-[10px] text-gray-400">{k}</dt>
                  <dd className="text-[11px] text-gray-700 dark:text-gray-300 whitespace-pre-line">
                    {String(v)}
                  </dd>
                </div>
              ))}
          </dl>
        </div>
      </div>
    );
  };

  /* -----------------
     MAIN UI 
--------------------*/
  return (
    <div className="flex w-full py-10">
      {/* MAIN CONTENT — NOW FULL WIDTH */}
      <main className="w-full mx-14 md:px-8 max-w-5xl">
        {/* PAGE TITLE */}
        <div className="mb-8">
          <h1 className="text-4xl font-black text-gray-900 dark:text-white">
            {isHi ? "योजना एवं कार्यक्रम खोजक" : "Schemes & Programmes Finder"}
          </h1>
          <p className="text-primary dark:text-primary/90 text-base mt-4">
            {isHi
              ? "सरकारी योजनाएँ और कार्यक्रम खोजें।"
              : "Search for government schemes and programmes."}
          </p>
        </div>

        {/* FILTER BAR (STICKY) */}
        <div
          className="
            sticky top-16 z-30
            bg-white dark:bg-[#2a2a2a]/60 backdrop-blur
            border border-black/5 dark:border-white/10
            rounded-2xl shadow-sm p-4 mb-8
          "
        >
          <div className="flex flex-wrap items-end gap-3">
            {/* SEARCH */}
            <div className="relative flex-1 min-w-[220px]">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={isHi ? "योजनाएँ खोजें…" : "Search schemes…"}
                className="
                  w-full h-10 px-3 pr-10
                  rounded-2xl border
                  bg-background-light dark:bg-background-dark
                  border-gray-300 dark:border-gray-700
                  text-sm text-gray-900 dark:text-gray-100
                  focus:ring-2 focus:ring-primary/50
               "
              />
              <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                search
              </span>
            </div>

            <SelectPill
              label={isHi ? "प्रकार" : "Type"}
              value={serviceType}
              onChange={setServiceType}
              options={[
                { label: isHi ? "योजनाएँ" : "Schemes", value: "scheme" },
                {
                  label: isHi ? "प्रोग्राम" : "Programmes",
                  value: "programme",
                },
              ]}
            />

            <SelectPill
              label={isHi ? "श्रेणी" : "Category"}
              value={category}
              onChange={setCategory}
              options={categories}
            />

            <SelectPill
              label={isHi ? "विभाग" : "Department"}
              value={department}
              onChange={setDepartment}
              options={departments}
            />

            {hasActive && (
              <button
                className="
                  ml-auto text-xs px-4 h-10 rounded-2xl 
                  border border-gray-300 dark:border-gray-600
                "
                onClick={clearAll}
              >
                {isHi ? "साफ़ करें" : "Clear"}
              </button>
            )}
          </div>
        </div>

        {/* SUMMARY */}
        <div className="text-xs text-gray-600 dark:text-gray-400 mb-4">
          {isHi ? "कुल" : "Total"}: {SCHEMES.length} •{" "}
          {isHi ? "योजनाएँ" : "Schemes"}: {typeCounts.scheme} •{" "}
          {isHi ? "प्रोग्राम" : "Programmes"}: {typeCounts.programme}
        </div>

        {/* ACTIVE FILTER CHIPS */}
        {hasActive && (
          <div className="flex flex-wrap gap-2 mb-4">
            {query && (
              <Chip>
                {isHi ? "खोज" : "Search"}: “{query}”
              </Chip>
            )}
            {serviceType && (
              <Chip>
                {isHi ? "प्रकार" : "Type"}:{" "}
                {serviceType === "scheme"
                  ? isHi
                    ? "योजना"
                    : "Scheme"
                  : isHi
                  ? "प्रोग्राम"
                  : "Programme"}
              </Chip>
            )}
            {category && (
              <Chip>
                {isHi ? "श्रेणी" : "Category"}: {category}
              </Chip>
            )}
            {department && (
              <Chip>
                {isHi ? "विभाग" : "Department"}: {department}
              </Chip>
            )}
          </div>
        )}

        {/* RESULTS GRID */}
        {filtered.length === 0 ? (
          <div
            className="
              bg-white dark:bg-[#2a2a2a]/60
              border border-black/5 dark:border-white/10
              rounded-2xl shadow-sm
             py-16 px-4 text-center
            "
          >
            <span className="material-symbols-outlined text-6xl text-gray-400 dark:text-gray-500 mb-4">
              search
            </span>
            <p className="text-gray-600 dark:text-gray-400 text-sm max-w-md mx-auto">
              {isHi
                ? "कोई परिणाम नहीं मिला। फ़िल्टर बदलकर देखें।"
                : "No matching results. Try different filters."}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filtered.map((s, i) => {
              const t_hi = s.name_hi || s.scheme_name_hi || s.title_hi || "";
              const t_en = s.name_en || s.scheme_name_en || s.title_en || "";

              const title = isHi ? t_hi || t_en : t_en || t_hi;
              const desc = isHi
                ? s.description_hi || "—"
                : s.description_en || "—";

              return (
                <button
                  key={i}
                  onClick={() => setSelectedScheme(s)}
                  className="
                    text-left bg-white dark:bg-[#2a2a2a]/60
                    border border-black/5 dark:border-white/10
                    rounded-2xl shadow-sm
                    px-4 py-3 hover:shadow-md
                    transition
                 "
                >
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">📄</span>
                    <div className="flex-1">
                      <p className="font-semibold text-sm text-gray-900 dark:text-white">
                        {title}
                        {t_hi && t_en && (
                          <span className="text-xs text-gray-500">
                            {" "}
                            / {isHi ? t_en : t_hi}
                          </span>
                        )}
                      </p>

                      <p className="mt-1 text-[11px] text-gray-600 dark:text-gray-400 line-clamp-2">
                        {desc}
                      </p>

                      <p className="mt-1 text-[10px] text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                        <span className="w-2 h-2 rounded-full bg-emerald-500" />
                        {isHi
                          ? "Verified by Panchayat Portal"
                          : "Verified by Panchayat Portal"}
                      </p>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        )}

        {/* MODAL */}
        {selectedScheme && (
          <div
            className="
              fixed inset-0 z-50 bg-black/30 
              flex items-center justify-center
              px-4 backdrop-blur-sm mb-20 scrollbar-hide
            "
            onClick={() => setSelectedScheme(null)}
          >
            <div onClick={(e) => e.stopPropagation()}>
              {renderDetailsModal(selectedScheme)}
            </div>
          </div>
        )}
      </main>

      {/* KEEP RIGHT SIDEBAR */}
      <RightSidebar />
    </div>
  );
}

/* ---------------------------------------------------
     SELECT PILL
--------------------------------------------------- */
function SelectPill({ label, value, onChange, options }) {
  const arr = options.map((o) =>
    typeof o === "string" ? { label: o, value: o } : o
  );

  const selectedObj = arr.find((o) => o.value === value);
  const display = selectedObj ? selectedObj.label : label;

  return (
    <div className="relative">
      <div
        className="
          h-10 px-4 pr-8 rounded-2xl border
          bg-white dark:bg-[#222]
          border-gray-300 dark:border-gray-700
          text-sm flex items-center
        "
      >
        <span
          className={
            value ? "text-gray-900 dark:text-gray-100" : "text-gray-500"
          }
        >
          {display}
        </span>
        <span className="material-symbols-outlined absolute right-2 text-[18px] text-gray-400">
          expand_more
        </span>
      </div>

      <select
        className="absolute inset-0 opacity-0 cursor-pointer"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">{label}</option>
        {arr.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
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

/* ---------------------------------------------------
   CHIP
--------------------------------------------------- */
function Chip({ children }) {
  return (
    <span
      className="
        px-3 py-1 rounded-full 
        bg-emerald-50 dark:bg-emerald-900/30
        text-emerald-800 dark:text-emerald-300
        border border-emerald-200 dark:border-emerald-700
        text-xs
      "
    >
      {children}
    </span>
  );
}

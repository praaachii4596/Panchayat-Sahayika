// src/screens/TrainingFinderScreen.jsx
import React, { useEffect, useMemo, useState } from "react";
import { useLanguage } from "../context/LanguageContext.jsx";
import RightSidebar from "../components/layout/RightSidebar.jsx";

const API_BASE = "http://127.0.0.1:7000";

export default function TrainingFinderScreen() {
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  const [districts, setDistricts] = useState([]);
  const [blocksByDistrict, setBlocksByDistrict] = useState({});
  const [selectedDistrict, setSelectedDistrict] = useState("");
  const [selectedBlock, setSelectedBlock] = useState("");

  const [trainings, setTrainings] = useState([]);
  const [loadingFilters, setLoadingFilters] = useState(false);
  const [loadingTrainings, setLoadingTrainings] = useState(false);
  const [error, setError] = useState("");

  // Load filters
  useEffect(() => {
    const loadFilters = async () => {
      try {
        setLoadingFilters(true);
        const res = await fetch(`${API_BASE}/filters`);
        const data = await res.json();

        setDistricts(data.districts || []);
        setBlocksByDistrict(data.blocksByDistrict || {});

        if ((data.districts || []).length > 0) {
          setSelectedDistrict(data.districts[0]);
        }
      } catch (err) {
        setError(isHi ? "फ़िल्टर लोड नहीं हो पाए।" : "Unable to load filters.");
      } finally {
        setLoadingFilters(false);
      }
    };

    loadFilters();
  }, [isHi]);

  const currentBlocks = useMemo(() => {
    return blocksByDistrict[selectedDistrict] || [];
  }, [selectedDistrict, blocksByDistrict]);

  useEffect(() => {
    setSelectedBlock("");
  }, [selectedDistrict]);

  // Search trainings
  const handleSearch = async () => {
    try {
      setLoadingTrainings(true);
      setError("");

      const params = new URLSearchParams();
      if (selectedDistrict) params.append("district", selectedDistrict);
      if (selectedBlock) params.append("block", selectedBlock);

      const res = await fetch(`${API_BASE}/trainings?${params.toString()}`);
      const data = await res.json();
      setTrainings(data.items || []);
    } catch (err) {
      setError(
        isHi ? "ट्रेनिंग लोड नहीं हो पाई।" : "Unable to load trainings."
      );
    } finally {
      setLoadingTrainings(false);
    }
  };

  return (
    <div className="flex w-full mt-10">
      {/* MAIN CONTENT (Now Full Width) */}
      <main className="w-full ml-14 md:px-8 max-w-5xl">
        {/* PAGE TITLE */}
        <div className="mb-8">
          <h1
            className="
            text-4xl font-black tracking-tight 
            text-gray-900 dark:text-white
          "
          >
            {isHi
              ? "उत्तराखंड पंचायत प्रशिक्षण खोजक"
              : "Uttarakhand Panchayat Trainings Finder"}
          </h1>
          <p
            className="
            text-primary dark:text-primary 
            text-base mt-4 mb-10
          "
          >
            {isHi
              ? "अपने क्षेत्र में प्रासंगिक सरकारी प्रशिक्षण कार्यक्रम खोजें।"
              : "Search for relevant government training programs in your area."}
          </p>
        </div>

        {/* FILTERS CARD */}
        <div
          className="
          bg-white dark:bg-[#2a2a2a]/60
          p-4 rounded-2xl shadow-sm 
          border border-black/5 dark:border-white/10
          mb-8
        "
        >
          <div className="flex flex-wrap items-end gap-4">
            {/* STATE */}
            <div className="flex h-14 items-center">
              <div
                className="
                flex items-center gap-2 
                h-10 px-4 rounded-2xl 
                bg-primary/10 dark:bg-primary/20
              "
              >
                <span className="material-symbols-outlined text-primary text-base">
                  push_pin
                </span>
                <p className="bg-green-50 text-primary font-medium text-sm px-5 py-4 rounded-2xl">
                  {isHi ? "राज्य: उत्तराखंड" : "State: Uttarakhand"}
                </p>
              </div>
            </div>

            {/* DISTRICT */}
            <label className="flex flex-col flex-1 min-w-40">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 pb-1">
                {isHi ? "जिला" : "District"}
              </p>
              <select
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                className="
                  h-10 px-3 rounded-2xl border 
                  bg-background-light dark:bg-background-dark
                  border-gray-300 dark:border-gray-700
                  text-gray-800 dark:text-gray-200
                  focus:ring-2 focus:ring-primary/50
                "
              >
                <option>{isHi ? "जिला चुनें" : "Select District"}</option>
                {districts.map((d) => (
                  <option key={d}>{d}</option>
                ))}
              </select>
            </label>

            {/* BLOCK */}
            <label className="flex flex-col flex-1 min-w-40">
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300 pb-1">
                {isHi ? "ब्लॉक" : "Block"}
              </p>
              <select
                disabled={!selectedDistrict}
                value={selectedBlock}
                onChange={(e) => setSelectedBlock(e.target.value)}
                className="
                  h-10 px-3 rounded-2xl border
                  bg-background-light dark:bg-background-dark
                  border-gray-300 dark:border-gray-700
                  text-gray-800 dark:text-gray-200
                  focus:ring-2 focus:ring-primary/50
                "
              >
                <option>
                  {!selectedDistrict
                    ? isHi
                      ? "पहले जिला चुनें"
                      : "Select district first"
                    : isHi
                    ? "ब्लॉक चुनें"
                    : "Select Block"}
                </option>
                {currentBlocks.map((b) => (
                  <option key={b}>{b}</option>
                ))}
              </select>
            </label>

            {/* SEARCH BUTTON */}
            <button
              onClick={handleSearch}
              disabled={loadingTrainings || !selectedDistrict}
              className="
                min-w-[120px] h-10 px-6 rounded-2xl 
                bg-primary text-white font-bold shadow 
                hover:bg-primary/90 transition 
                disabled:opacity-50
              "
            >
              {loadingTrainings
                ? isHi
                  ? "लोड हो रहा है..."
                  : "Loading..."
                : isHi
                ? "ट्रेनिंग दिखाएं"
                : "Show Trainings"}
            </button>
          </div>

          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </div>

        {/* TRAINING LIST */}
        <div className="space-y-6">
          {trainings.length === 0 && !loadingTrainings && (
            <div
              className="
      flex flex-col items-center justify-center
      bg-white dark:bg-[#2a2a2a]/60
      border border-black/5 dark:border-white/10
      rounded-2xl shadow-sm
      py-16 px-4 text-center
    "
            >
              <span className="material-symbols-outlined text-6xl text-gray-400 dark:text-gray-500 mb-4">
                search
              </span>

              <p className="text-gray-600 dark:text-gray-400 text-sm max-w-md leading-relaxed">
                {isHi
                  ? "चयनित मानदंडों के लिए कोई प्रशिक्षण नहीं मिला। कृपया अलग फ़िल्टर आज़माएँ।"
                  : "No trainings found for the selected criteria. Please try different filters."}
              </p>
            </div>
          )}

          {trainings.map((t, idx) => (
            <div
              key={idx}
              className="
                bg-white dark:bg-[#2a2a2a]/60 
                rounded-2xl p-5 shadow-sm
                border border-black/5 dark:border-white/10
                hover:shadow-md transition duration-300
              "
            >
              <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-3">
                <div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                    {t.training_name || (isHi ? "प्रशिक्षण" : "Training")}
                  </h3>
                  {t.batch_no && (
                    <p className="text-sm text-gray-700 dark:text-gray-300 font-semibold mt-1">
                      {isHi ? "बैच: " : "Batch: "} {t.batch_no}
                    </p>
                  )}
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-3">
                    <strong>{isHi ? "आयोजक:" : "Organized by:"}</strong>{" "}
                    {t.org_institute}
                  </p>
                </div>

                {t.training_category && (
                  <div
                    className="
                    text-xs md:text-sm max-w-sm bg-primary/10 dark:bg-primary/20 text-primary dark:text-primary/90
                    rounded-full px-3 py-2 leading-relaxed
                  "
                  >
                    <span className="font-semibold">
                      {isHi ? "श्रेणी: " : "Category: "}{" "}
                    </span>

                    {t.training_category}

                    {t.training_sub_category && (
                      <div className="mt-1 space-y-1">
                        {t.training_sub_category
                          .split(",")
                          .map((theme, idx) => (
                            <p
                              key={idx}
                              className="text-[11px] leading-snug opacity-80"
                            >
                              • {theme.trim()}
                            </p>
                          ))}
                      </div>
                    )}

                    {t.themes && t.themes.length > 0 && (
                      <ul className="mt-1 space-y-[2px] text-[11px] text-primary dark:text-primary/90">
                        {t.themes.map((theme, i) => (
                          <li key={i} className="flex gap-1">
                            • <span>{theme}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>

              <div className="border-t border-gray-200 dark:border-gray-700 my-4" />

              {/* Details Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="font-semibold text-gray-700 dark:text-gray-300">
                    {isHi ? "🗓️ तारीखें:" : "🗓️ Dates:"}
                  </p>
                  <p className="text-gray-600 dark:text-gray-400">
                    {t.start_date} – {t.end_date}
                  </p>
                </div>

                {t.targeted_participants && (
                  <div>
                    <p className="font-semibold text-gray-700 dark:text-gray-300">
                      {isHi ? "👥 लक्ष्य: " : "👥 Target: "}
                    </p>
                    <p className="text-gray-600 dark:text-gray-400">
                      {t.targeted_participants}
                    </p>
                  </div>
                )}

                {t.agenda && (
                  <div>
                    <p className="font-semibold text-gray-700 dark:text-gray-300">
                      {isHi ? "एजेंडा:" : "Agenda Highlight:"}
                    </p>
                    <p className="text-gray-600 dark:text-gray-400">
                      {t.agenda}
                    </p>
                  </div>
                )}
              </div>

              <p className="text-right text-xs text-gray-400 dark:text-gray-500 mt-3">
                {isHi ? "स्रोत: " : "Source: "} {t.source}
              </p>
            </div>
          ))}
        </div>
      </main>

      {/* RIGHT SIDEBAR (KEPT) */}
      <RightSidebar />
    </div>
  );
}

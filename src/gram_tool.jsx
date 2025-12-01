// src/gram_tool.jsx
import React, { useEffect, useState } from "react";
import { useLanguage } from "./context/LanguageContext";

const API_BASE = "http://127.0.0.1:5000";

export default function GramPlanningTool() {
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState("CHAMPAWAT");
  const [villages, setVillages] = useState([]);
  const [selectedVillageCode, setSelectedVillageCode] = useState("");
  const [villageDetail, setVillageDetail] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  /* Load districts */
  useEffect(() => {
    fetch(`${API_BASE}/api/districts`)
      .then((r) => r.json())
      .then((d) => setDistricts(d.districts || []));
  }, []);

  /* Load villages when district changes */
  useEffect(() => {
    if (!selectedDistrict) return;
    fetch(
      `${API_BASE}/api/villages?district=${encodeURIComponent(
        selectedDistrict
      )}`
    )
      .then((r) => r.json())
      .then((d) => setVillages(d.villages || []));
  }, [selectedDistrict]);

  function loadVillageDetail(code) {
    setSelectedVillageCode(code);
    setLoadingDetail(true);

    fetch(`${API_BASE}/api/village_detail?village_code=${code}`)
      .then((r) => r.json())
      .then((data) => {
        setVillageDetail(data);
        setLoadingDetail(false);
      })
      .catch(() => setLoadingDetail(false));
  }

  /* Bilingual deficit labels */
  const deficitLabels = {
    health: isHi ? "स्वास्थ्य" : "Health",
    education: isHi ? "शिक्षा" : "Education",
    sanitation: isHi ? "स्वच्छता" : "Sanitation",
    roads: isHi ? "सड़कें" : "Roads",
    digital: isHi ? "डिजिटल" : "Digital",
    electricity: isHi ? "बिजली" : "Electricity",
  };

  const pdiLabel = isHi ? "PDI स्कोर" : "PDI Score";
  const deficitIndexLabel = isHi ? "कुल कमी सूचकांक" : "Overall Deficit Index";

  const pdiExplain = isHi
    ? "उच्च PDI = बेहतर विकास स्तर। कम PDI वाले गाँवों को प्राथमिकता दें।"
    : "Higher PDI = better overall development. Lower PDI villages need priority.";

  const levelLabel = (lvl) => {
    if (!isHi) return `${lvl} deficit`;
    if (lvl === "High") return "उच्च कमी";
    if (lvl === "Medium") return "मध्यम कमी";
    return "कम कमी";
  };

  return (
    <div className="space-y-6 py-4 m-20 mt-5 mb-5">
      {/* HEADER CARD */}
      <div
        className="
        sticky top-0 z-20 
        bg-white dark:bg-[#1f1f1f]/80 backdrop-blur-md 
        border border-border-light dark:border-border-dark 
        rounded-2xl shadow-soft p-4
      "
      >
        <h2 className="text-3xl font-bold mb-3 text-primary">
          🧠 {isHi ? "स्मार्ट ग्राम प्लानिंग टूल" : "Smart Gram Planning Tool"}
        </h2>

        <div className="flex gap-3 items-center">
          <div>
            <label className="block text-xs font-medium mb-1">
              {isHi ? "ज़िला" : "DISTRICT"}

              <select
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                className="
                border border-border-light dark:border-border-dark
                rounded-xl px-8 py-2 bg-card-light dark:bg-card-dark
                text-sm focus:ring-2 focus:ring-primary outline-none
              "
              >
                {districts.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* LEFT: VILLAGE LIST */}
        <div
          className="
          bg-white dark:bg-card-dark rounded-2xl shadow-soft p-4 
          border border-border-light dark:border-border-dark
          max-h-[140vh] overflow-y-auto scrollbar-hide
        "
        >
          <h3 className="text-sm font-semibold mb-3">
            {isHi ? "गाँव (कम PDI वाले पहले)" : "Villages (lowest PDI first)"}
          </h3>

          <ul className="space-y-3">
            {villages.map((v) => {
              const active = selectedVillageCode === v.village_code;

              return (
                <li
                  key={v.village_code}
                  onClick={() => loadVillageDetail(v.village_code)}
                  className={`
                    p-3 rounded-xl border cursor-pointer transition-all
                    shadow-sm hover:shadow-md 
                    ${
                      active
                        ? "border-primary bg-primary/10"
                        : "border-border-light dark:border-border-dark bg-card-light dark:bg-card-dark"
                    }
                  `}
                >
                  <div className="font-bold">
                    {v.village_name} ({v.gp_name})
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-300">
                    {v.block_name}, {v.district_name}
                  </div>

                  {/* PDI */}
                  <div className="text-xs mt-1">
                    {pdiLabel}:{" "}
                    <span className="font-semibold">
                      {v.pdi_village != null ? v.pdi_village.toFixed(2) : "NA"}
                    </span>
                    {v.pdi_grade && (
                      <span className="ml-1 text-[11px] px-1.5 py-0.5 rounded-full bg-blue-100 text-blue-700">
                        {v.pdi_grade}
                      </span>
                    )}
                  </div>

                  {/* Deficit Index */}
                  <div className="text-[11px] text-gray-500">
                    {deficitIndexLabel}:{" "}
                    <div className="text-xs mt-1">
                      {isHi ? "कुल कमी सूचकांक" : "Overall Deficit Index"}:{" "}
                      <span className="font-semibold">
                        {v.service_deficit_index?.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>

        {/* RIGHT: DETAILS */}
        <div
          className="
          bg-white dark:bg-card-dark rounded-2xl shadow-soft p-5
          border border-border-light dark:border-border-dark
          max-h-[140vh]
        "
        >
          {loadingDetail && (
            <p className="text-sm">{isHi ? "लोड हो रहा है…" : "Loading…"}</p>
          )}

          {/* No selection */}
          {!loadingDetail && !villageDetail && (
            <p className="text-sm text-gray-500">
              {isHi
                ? "विवरण देखने के लिए बाईं ओर से कोई गाँव चुनें।"
                : "Select a village from the left to view details."}
            </p>
          )}

          {/* DETAILS */}
          {!loadingDetail && villageDetail && (
            <div className="space-y-4 text-sm">
              {/* BASIC INFO */}
              <div>
                <h3 className="text-lg font-bold">
                  {villageDetail.village_name} ({villageDetail.gp_name})
                </h3>
                <p className="text-xs text-gray-500">
                  {villageDetail.block_name}, {villageDetail.district_name} •{" "}
                  {isHi ? "कोड" : "Code"}: {villageDetail.village_code}
                </p>
              </div>

              {/* PDI SUMMARY */}
              <div className="border rounded-xl p-3 bg-blue-50/30">
                <p className="font-semibold">
                  {isHi ? "कुल PDI" : "Overall PDI"}
                </p>
                <p>
                  {isHi ? "स्कोर" : "Score"}:{" "}
                  <span className="font-semibold">
                    {villageDetail.pdi_village?.toFixed(2)}
                  </span>
                  {villageDetail.pdi_grade && (
                    <span className="ml-2 bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full text-[11px]">
                      {isHi ? "ग्रेड" : "Grade"}: {villageDetail.pdi_grade}
                    </span>
                  )}
                </p>
                <p className="text-xs text-gray-700 mt-1">{pdiExplain}</p>
              </div>

              {/* THEMES */}
              {villageDetail.themes && (
                <div>
                  <h4 className="text-xs font-semibold mb-1">
                    {isHi
                      ? "थीम-वार स्कोर (0–100)"
                      : "Theme-wise Scores (0–100)"}
                  </h4>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(villageDetail.themes).map(
                      ([key, value]) => (
                        <div
                          key={key}
                          className="rounded-xl p-3 border bg-card-light dark:bg-card-dark"
                        >
                          <p className="font-semibold capitalize">
                            {key.replace(/_/g, " ")}
                          </p>
                          <p>
                            {isHi ? "स्कोर" : "Score"}:{" "}
                            {value.score?.toFixed(2)}
                          </p>
                          {value.status && (
                            <p className="text-[11px] text-gray-600">
                              {isHi ? "स्थिति" : "Status"}:{" "}
                              <span className="font-semibold">
                                {value.status}
                              </span>
                            </p>
                          )}
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}

              {/* DEFICITS */}
              <div>
                <h4 className="text-xs font-semibold mb-1">
                  {isHi ? "सेक्टर-वार कमी (0–1)" : "Sector-wise Deficits (0–1)"}
                </h4>

                <div className="grid grid-cols-2 gap-3">
                  {Object.entries(villageDetail.deficits).map(([key, val]) => (
                    <div
                      key={key}
                      className="
                          rounded-xl p-3 border
                          bg-card-light dark:bg-card-dark
                          shadow-sm
                        "
                    >
                      <p className="font-semibold capitalize">
                        {deficitLabels[key] || key}
                      </p>
                      <p>
                        {isHi ? "स्कोर" : "Score"}: {val.score?.toFixed(2)}
                      </p>

                      <p
                        className={
                          val.level === "High"
                            ? "text-red-600 font-bold"
                            : val.level === "Medium"
                            ? "text-orange-500 font-bold"
                            : "text-green-600 font-bold"
                        }
                      >
                        {levelLabel(val.level)}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* SUGGESTION SECTION */}
              <div className="border-t pt-3 text-xs">
                <h4 className="font-semibold mb-1">
                  {isHi ? "प्राथमिक सुझाव" : "Basic Planning Suggestion"}
                </h4>

                <p className="leading-relaxed">
                  {isHi
                    ? "कम PDI और उच्च कमी वाले क्षेत्रों वाले गाँवों को प्राथमिकता दें। उदाहरण: यदि सड़क और स्वास्थ्य में कमी है, तो PHC/CHC तक सड़क कनेक्टिविटी और स्वास्थ्य सुविधाओं को मजबूत करने की योजना बनाएं।"
                    : "Prioritize villages with low PDI and sectors showing High deficit. For example, if roads and health sectors are weak, plan for better road connectivity to PHC/CHC and upgrade local health services."}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Hide Scrollbar */}
      <style>{`
        .scrollbar-hide::-webkit-scrollbar { display: none; }
        .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
      `}</style>
    </div>
  );
}

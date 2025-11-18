import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth.jsx";
import ServiceCard from "../components/ui/ServiceCard.jsx";
import SCHEMES from "../data/samaj_kalyan_vibhag_clean_typed.json";

const CHAT_API = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";
const TRAIN_API = "http://127.0.0.1:7000";
const GRAM_API = "http://127.0.0.1:5000";

// type detection just to label “Scheme / Programme”
function normalizeType(item) {
  const raw = (item?.type || "").toString().toLowerCase();
  if (raw === "scheme" || raw === "schemes") return "scheme";
  if (raw === "programme" || raw.startsWith("program")) return "programme";
  return "scheme";
}

// simple text normaliser
function clean(txt) {
  return String(txt || "")
    .toLowerCase()
    .replace(/[()]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

// map dashboard recommendation card → full JSON scheme
function findSchemeFromCard(card) {
  const rawLabel =
    card.title || card.name_hi || card.name_en || card.subtitle || "";
  if (!rawLabel) return null;

  // dashboard titles often look like "हिन्दी नाम / English Name"
  const labelParts = clean(rawLabel)
    .split("/")
    .map((p) => p.trim())
    .filter(Boolean);

  if (labelParts.length === 0) labelParts.push(clean(rawLabel));

  for (const s of SCHEMES) {
    const hi = clean(s.name_hi);
    const en = clean(s.name_en);

    for (const part of labelParts) {
      if (!part) continue;

      // strong exact/startsWith both ways
      if (
        (hi && (part === hi || hi.startsWith(part) || part.startsWith(hi))) ||
        (en && (part === en || en.startsWith(part) || part.startsWith(en)))
      ) {
        return s;
      }

      // softer includes both directions
      if (
        (hi && (hi.includes(part) || part.includes(hi))) ||
        (en && (en.includes(part) || part.includes(en)))
      ) {
        return s;
      }
    }
  }

  console.warn("No scheme match for dashboard card:", rawLabel);
  return null;
}

// detail card (very similar to FinderScreen’s modal content)
function SchemeDetailCard({ scheme, onClose }) {
  if (!scheme) return null;

  const titleHi =
    scheme.name_hi || scheme.scheme_name_hi || scheme.title_hi || "";
  const titleEn =
    scheme.name_en || scheme.scheme_name_en || scheme.title_en || "";
  const descHi =
    scheme.long_description_hi ||
    scheme.description_hi ||
    scheme.short_desc_hi ||
    "";
  const descEn =
    scheme.long_description_en ||
    scheme.description_en ||
    scheme.short_desc_en ||
    "";

  return (
    <div className="w-full max-w-4xl bg-white rounded-3xl shadow-xl p-6 md:p-8 text-sm space-y-4 max-h-[85vh] overflow-y-auto">
      {/* header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg md:text-xl font-semibold text-gray-900">
            {titleHi || titleEn || "Unnamed Scheme"}
          </h2>
          {titleHi && titleEn && (
            <p className="text-xs text-gray-500 mt-0.5">{titleEn}</p>
          )}
          <p className="mt-2 text-[11px] text-gray-500">
            {[
              normalizeType(scheme) === "programme"
                ? "Programme"
                : "Scheme / Yojana",
              scheme.category,
              scheme.department,
            ]
              .filter(Boolean)
              .join(" • ")}
          </p>
        </div>

        <button
          type="button"
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 text-lg leading-none"
          aria-label="Close"
        >
          ✕
        </button>
      </div>

      {/* main descriptions */}
      <div className="space-y-3 leading-relaxed">
        {descHi && (
          <div>
            <h3 className="text-xs font-semibold text-gray-700 mb-1">
              विवरण (Hindi)
            </h3>
            <p className="text-[13px] text-gray-800 whitespace-pre-line">
              {descHi}
            </p>
          </div>
        )}

        {descEn && (
          <div>
            <h3 className="text-xs font-semibold text-gray-700 mb-1">
              Description (English)
            </h3>
            <p className="text-[13px] text-gray-800 whitespace-pre-line">
              {descEn}
            </p>
          </div>
        )}

        {scheme.eligibility_hi && (
          <div>
            <h3 className="text-xs font-semibold text-gray-700 mb-1">
              पात्रता
            </h3>
            <p className="text-[13px] text-gray-800 whitespace-pre-line">
              {scheme.eligibility_hi}
            </p>
          </div>
        )}

        {scheme.benefit_hi && (
          <div>
            <h3 className="text-xs font-semibold text-gray-700 mb-1">
              लाभ / Benefit
            </h3>
            <p className="text-[13px] text-gray-800 whitespace-pre-line">
              {scheme.benefit_hi}
            </p>
          </div>
        )}
      </div>

      {/* raw JSON-ish fields */}
      <div className="mt-3 border-top border-gray-100 pt-3">
        <h3 className="text-[11px] font-semibold text-gray-500 mb-2">
          Detailed fields (JSON se)
        </h3>
        <dl className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2 text-[11px]">
          {Object.entries(scheme)
            .filter(([key, value]) => {
              if (value == null || value === "") return false;
              return ![
                "id",
                "scheme_id",
                "slug",
                "apply_url",
                "read_more_url",
                "created_at",
                "updated_at",
                "name_hi",
                "name_en",
                "scheme_name_hi",
                "scheme_name_en",
                "title_hi",
                "title_en",
                "description_hi",
                "description_en",
                "short_desc_hi",
                "short_desc_en",
                "long_description_hi",
                "long_description_en",
                "eligibility_hi",
                "benefit_hi",
              ].includes(key);
            })
            .map(([key, value]) => (
              <div key={key}>
                <dt className="uppercase tracking-wide text-[10px] text-gray-400">
                  {key.replace(/_/g, " ")}
                </dt>
                <dd className="text-[11px] text-gray-800 whitespace-pre-line">
                  {String(value)}
                </dd>
              </div>
            ))}
        </dl>
      </div>
    </div>
  );
}

/* -------------------- main dashboard screen -------------------- */

export default function DashboardScreen() {
  const { user, token } = useAuth();
  const navigate = useNavigate();

  const [schemes, setSchemes] = useState([]);
  const [trainings, setTrainings] = useState([]);
  const [village, setVillage] = useState(null);

  // 🔴 NEW: currently opened scheme for modal
  const [selectedScheme, setSelectedScheme] = useState(null);

  // 1) Recommended schemes
  useEffect(() => {
    if (!token) return;

    fetch(`${CHAT_API}/user/recommended-schemes`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        // backend may return {items: [...]} or plain array; handle both
        if (Array.isArray(data)) setSchemes(data);
        else if (Array.isArray(data.items)) setSchemes(data.items);
        else setSchemes([]);
      })
      .catch((err) => {
        console.error(err);
        setSchemes([]);
      });
  }, [token]);

  // 2) Trainings + village detail (based on user profile)
  useEffect(() => {
    if (!user) return;

    // Trainings
    const params = new URLSearchParams();
    if (user.district) params.append("district", user.district);
    if (user.block) params.append("block", user.block);

    fetch(`${TRAIN_API}/trainings?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => setTrainings(data.items || []))
      .catch((err) => {
        console.error(err);
        setTrainings([]);
      });

    // Village infra detail
    if (user.village_code) {
      fetch(`${GRAM_API}/api/village_detail?village_code=${user.village_code}`)
        .then((res) => res.json())
        .then(setVillage)
        .catch((err) => {
          console.error(err);
          setVillage(null);
        });
    } else {
      setVillage(null);
    }
  }, [user]);

  if (!user) {
    return (
      <section className="mt-8 text-sm text-center space-y-3">
        <p>Please login to see your personalised dashboard.</p>
        <button
          onClick={() => navigate("/login")}
          className="inline-flex items-center px-4 py-2 rounded-full bg-[#166534] text-white text-xs font-semibold hover:bg-green-800"
        >
          Go to Login
        </button>
      </section>
    );
  }

  return (
    <>
      <section className="space-y-4">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-sm p-4 text-sm flex items-start justify-between gap-3">
          <div>
            <h2 className="text-base font-semibold">
              Namaste, {user.full_name || user.username} 👋
            </h2>
            <p className="text-[11px] text-gray-500">
              Yeh aapka personalised dashboard hai – schemes, trainings aur
              village status aapke profile ke basis par.
            </p>
            <p className="text-[11px] text-gray-500 mt-1">
              {user.district && (
                <>
                  District:{" "}
                  <span className="font-semibold">{user.district}</span>{" "}
                </>
              )}
              {user.block && (
                <>
                  • Block:{" "}
                  <span className="font-semibold">{user.block}</span>{" "}
                </>
              )}
              {user.village_code && (
                <>
                  • Village code:{" "}
                  <span className="font-semibold">{user.village_code}</span>
                </>
              )}
            </p>
          </div>

          <div className="flex flex-col gap-1">
            <button
              onClick={() => navigate("/profile/edit")}
              className="self-start sm:self-auto px-3 py-1.5 rounded-full border border-gray-300 text-[11px] hover:bg-gray-50"
            >
              ✏️ Edit profile
            </button>
          </div>
        </div>

        {/* Recommended schemes */}
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-[#166534]">
              Recommended Schemes for you
            </h3>
            <button
              onClick={() => navigate("/finder")}
              className="text-[11px] text-[#166534] underline"
            >
              Open Schemes Finder ↗
            </button>
          </div>

          {schemes.length === 0 ? (
            <p className="text-[11px] text-gray-500">
              Abhi koi recommendation nahi mila. Registration me apni details
              check karo ya chat me schemes pucho.
            </p>
          ) : (
            <div className="grid sm:grid-cols-2 gap-3">
              {schemes.map((s, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => {
                    const full = findSchemeFromCard(s);
                    if (full) {
                      setSelectedScheme(full); // 🟢 open modal
                    } else {
                      // fallback: open finder with prefilled query
                      navigate("/finder", {
                        state: {
                          initialQuery:
                            s.title || s.name_en || s.name_hi || "",
                        },
                      });
                    }
                  }}
                  className="text-left"
                >
                  <ServiceCard
                    icon="📄"
                    title={s.title || s.name_hi || s.name_en || "Scheme"}
                    description={
                      s.subtitle ||
                      s.description_hi ||
                      s.description_en ||
                      "—"
                    }
                    badges={s.badges}
                    applyUrl={s.apply_url}
                    readMoreUrl={s.read_more_url}
                  />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Trainings */}
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-[#166534]">
              Upcoming trainings in your area
            </h3>
            <button
              onClick={() => navigate("/my-panchayat/trainings")}
              className="text-[11px] text-[#166534] underline"
            >
              See all trainings ↗
            </button>
          </div>

          {trainings.length === 0 ? (
            <p className="text-[11px] text-gray-500">
              Abhi trainings list nahi mili. District/block sahi bharo
              registration me.
            </p>
          ) : (
            <div className="space-y-2 text-[11px]">
              {trainings.slice(0, 5).map((t, idx) => (
                <div
                  key={idx}
                  className="border rounded-xl p-2 flex flex-col gap-0.5"
                >
                  <div className="font-semibold text-gray-800">
                    {t.training_name || "Training"}
                  </div>
                  <div className="text-gray-500 text-[10px]">
                    {t.org_institute}
                  </div>
                  <div className="text-gray-600">
                    🗓 {t.start_date} – {t.end_date}
                  </div>
                  <div className="text-[10px] text-gray-500">
                    {t.district}
                    {t.block ? ` • ${t.block}` : ""}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Village infra status */}
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-[#166534]">
              Village infra status
            </h3>
            <button
              onClick={() => navigate("/my-panchayat/planning")}
              className="text-[11px] text-blue-600 underline"
            >
              Open full planning tool ↗
            </button>
          </div>

          {!village ? (
            <p className="text-[11px] text-gray-500">
              Registration me village code bharoge to yahan status dikhega.
            </p>
          ) : (
            <div className="text-[11px] space-y-2">
              <div className="font-semibold">
                {village.village_name} ({village.gp_name})
              </div>
              <div className="text-gray-500">
                {village.block_name}, {village.district_name} | Code:{" "}
                {village.village_code}
              </div>

              <div className="grid grid-cols-2 gap-2 mt-2">
                {Object.entries(village.deficits).map(([k, v]) => (
                  <div key={k} className="border rounded-xl p-2">
                    <div className="font-semibold capitalize">{k}</div>
                    <div>Score: {v.score?.toFixed(2)}</div>
                    <div
                      className={
                        v.level === "High"
                          ? "text-red-600 font-semibold"
                          : v.level === "Medium"
                          ? "text-orange-500 font-semibold"
                          : "text-green-600 font-semibold"
                      }
                    >
                      {v.level} deficit
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>

      {/* 🔴 Modal overlay for scheme details*/}
      {selectedScheme && (
        <div
          className="fixed inset-0 z-50 bg-black/30 flex items-center justify-center px-4"
          onClick={() => setSelectedScheme(null)}
        >
          <div onClick={(e) => e.stopPropagation()}>
            <SchemeDetailCard
              scheme={selectedScheme}
              onClose={() => setSelectedScheme(null)}
            />
          </div>
        </div>
      )}
    </>
  );
}

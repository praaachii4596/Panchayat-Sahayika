import { useNavigate } from "react-router-dom";
import {
  EyeIcon,
  GlobeAltIcon,
  UserGroupIcon,
} from "@heroicons/react/24/outline";
import { useLanguage } from "../context/LanguageContext.jsx";
import img from '../assets/panchayati-raj.png';

export default function HomeScreen() {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  return (
    <div className="font-display text-text-light dark:text-text-dark flex flex-col items-center transition-colors duration-300">
      <div className="w-full max-w-6xl px-4 py-10 md:py-20 flex flex-col gap-20">

        {/* ---------------------------------------------------
           HERO SECTION
        --------------------------------------------------- */}
        <div className="flex flex-col gap-10 md:flex-row md:items-center">

          {/* LEFT SIDE TEXT */}
          <div className="flex w-full flex-col gap-6 md:w-1/2 animate-fadeIn">
            <div className="flex flex-col gap-2 text-left">

              <h1 className="text-4xl md:text-5xl font-black leading-tight tracking-tight">
                {isHi ? (
                  <>
                    नमस्ते! मैं आपकी पंचायत सहायिका हूं। <br />
                    {/* <span className="text-primary dark:text-primary/80">
                      Namaste! I am your Panchayat Sahayika.
                    </span> */}
                  </>
                ) : (
                  <>
                    Namaste! I am your Panchayat Sahayika. <br />
                    {/* <span className="text-primary dark:text-primary/80">
                      Your trusted village information guide.
                    </span> */}
                  </>
                )}
              </h1>

              <h2 className="mt-5 text-base font-normal leading-normal text-gray-700 dark:text-gray-300">
                {isHi
                  ? "अपने गाँव, योजनाओं, सेवाओं और सुविधाओं से जुड़ी जानकारी समझने के लिए सरल और भरोसेमंद डिजिटल साथी — बिना जटिल भाषा, सीधे आधिकारिक सरकारी स्रोतों से।"
                  : "Your simple and trustworthy digital companion to understand village schemes, services, and facilities—direct from official government sources."}
              </h2>

            </div>

            {/* CTA BUTTONS */}
            <div className="flex flex-wrap gap-3 mt-6">
              <button
                onClick={() => navigate("/chat")}
                className="
                  flex h-12 px-5 items-center justify-center rounded-lg 
                  bg-primary text-white text-base font-bold 
                  shadow-[0_4px_12px_rgba(0,0,0,0.1)]
                  hover:shadow-[0_6px_16px_var(--primary)]
                  hover:-translate-y-[2px] active:translate-y-[1px]
                  active:brightness-90
                  transition-all duration-300
                "
              >
                {isHi ? "शुरू करें" : "Get Started"}
              </button>

              <button
                onClick={() => navigate("/register")}
                className="
                  flex h-12 px-5 items-center justify-center rounded-lg
                  bg-transparent text-primary ring-1 ring-primary-light font-bold
                  hover:bg-primary hover:text-white
                  hover:shadow-[0_6px_16px_var(--primary)]
                  hover:-translate-y-[2px] active:translate-y-[1px]
                  transition-all duration-300
                "
              >
                {isHi ? "रेजिस्टर करें" : "Register Now"}
              </button>
            </div>
          </div>

          {/* RIGHT SIDE IMAGE */}
    <div className="w-full md:w-1/2">
      <div
        className="
          aspect-square ml-20 w-2/3 rounded-2xl bg-cover bg-center bg-no-repeat shadow-soft
          transform transition-all duration-300
        "
        style={{
          backgroundImage: `url(${img})`,
        }}
      />
    </div>
        </div>

        {/* ---------------------------------------------------
           OUR SERVICES
        --------------------------------------------------- */}
        <div>
          <h2 className="text-2xl font-bold tracking-tight pb-3 pt-10">
            {isHi ? "मुख्य सेवाएँ" : "Our Services"}
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {services(isHi).map((s, i) => (
              <div
                key={i}
                onClick={() => navigate(s.route)}
                className="
                  cursor-pointer flex flex-col gap-4 rounded-2xl border 
                  border-border-light dark:border-border-dark 
                  bg-card-light dark:bg-card-dark p-6 shadow-soft
                  hover:shadow-[0_6px_16px_var(--primary)] hover:-translate-y-1 hover:border-primary/40
                  active:scale-[0.99] transition-all duration-300 backdrop-blur-sm
                "
              >
                <div className="text-primary text-4xl">{s.icon}</div>

                <div className="flex flex-col gap-1">
                  <h3 className="text-lg font-bold text-primary dark:text-primary/80">
                    {s.label}
                  </h3>
                  <p className="text-sm font-bold">{s.title}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ---------------------------------------------------
           OUR MISSION
        --------------------------------------------------- */}
        <div className="pt-16 pb-10">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">
            {isHi ? "हमारी प्रतिबद्धता" : "Our Mission"}
          </h1>

          <p className="max-w-3xl text-base leading-relaxed text-gray-700 dark:text-gray-300">
            {isHi
              ? "हमारा लक्ष्य है कि गाँव के हर नागरिक तक तकनीक के माध्यम से सही और सरल जानकारी पहुँचे।"
              : "Our mission is to bridge the information gap between citizens and their panchayat using technology."}
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
            {mission(isHi).map((m, index) => (
              <div
                key={index}
                className="
                  flex flex-col gap-4 rounded-2xl border border-border-light dark:border-border-dark
                  bg-card-light dark:bg-card-dark p-6 shadow-soft
                  hover:shadow-[0_6px_16px_var(--primary)] hover:-translate-y-1 transition-all duration-300
                "
              >
                <span className="material-symbols-outlined text-primary dark:text-green-300 text-3xl">
                  {m.icon}
                </span>
                <div className="flex flex-col gap-1">
                  <h3 className="text-lg font-bold">{m.title}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {m.body}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}

/* ---------------- DATA (Dynamic based on language) ---------------- */

const services = (isHi) => [
  {
    icon: "💬",
    label: isHi ? "सवाल पूछें (Chat)" : "Ask a Question",
    title: isHi ? "अपनी समस्या लिखें" : "Type your query",
    desc: isHi
      ? "हम आपको सही योजना या सेवा तक पहुँचाएँगे।"
      : "We help you reach the right scheme or service.",
    route: "/chat",
  },
  {
    icon: "🔍",
    label: isHi ? "योजनाएँ / सेवाएँ / प्रोग्राम" : "Schemes & Services",
    title: isHi ? "सरकारी योजनाएँ देखें" : "Browse government schemes",
    desc: isHi
      ? "श्रेणी, स्थान और पात्रता के आधार पर खोजें।"
      : "Filter by category, location, and eligibility.",
    route: "/finder",
  },
  {
    icon: "🏠",
    label: isHi ? "मेरी पंचायत" : "My Panchayat",
    title: isHi ? "ग्राम पंचायत प्रोफ़ाइल" : "Village Panchayat Profile",
    desc: isHi
      ? "आपके गाँव के लिंक और विवरण।"
      : "Quick access to your village details.",
    route: "/my-panchayat",
  },
];

const mission = (isHi) => [
  {
    icon: "visibility",
    title: isHi ? "पारदर्शिता" : "Transparency",
    body: isHi
      ? "सारी जानकारी स्पष्ट और सरल रूप में।"
      : "Making information clear and simple.",
  },
  {
    icon: "language",
    title: isHi ? "सुलभता" : "Accessibility",
    body: isHi
      ? "हर नागरिक के लिए आसान उपकरण।"
      : "Tools that everyone can use.",
  },
  {
    icon: "groups",
    title: isHi ? "सशक्तिकरण" : "Empowerment",
    body: isHi
      ? "नागरिकों को शासन में भागीदारी के लिए प्रेरित करना।"
      : "Helping citizens participate in governance.",
  },
];

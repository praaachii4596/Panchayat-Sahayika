// import { useNavigate } from "react-router-dom";
// import { useLanguage } from "../../context/LanguageContext.jsx";

// export default function RightSidebar() {
//   const navigate = useNavigate();
//   const { lang } = useLanguage();
//   const isHi = lang === "hi";

//   return (
//     <aside className="w-80 hidden lg:flex flex-col gap-4 pr-4 pt-10">

//       {/* Card 1 – Schemes & Services */}
//       <button
//         type="button"
//         onClick={() => navigate("/finder")}
//         className="bg-white dark:bg-gray-900 rounded-3xl shadow-md border border-[#F4E3C3] 
//                    dark:border-gray-700 px-4 py-4 text-left hover:shadow-lg transition cursor-pointer"
//       >
//         <div className="text-xs font-semibold text-[#166534] dark:text-green-300 mb-1">
//           {isHi ? "योजनाएँ / सेवाएँ / प्रोग्राम" : "Schemes / Services / Programs"}
//         </div>

//         <div className="text-sm font-semibold mb-1 text-gray-900 dark:text-gray-100">
//           {isHi ? "सरकारी योजनाएं खोजें" : "Find Schemes & Services"}
//         </div>

//         <p className="text-[11px] text-gray-600 dark:text-gray-300 leading-relaxed">
//           {isHi
//             ? "अपने गाँव, जाति, सेवा या अन्य विवरण के आधार पर आपके लिए उपलब्ध सरकारी योजनाएँ देखें।"
//             : "Check government schemes available for your village, caste, service or other details."}
//         </p>
//       </button>

//       {/* Card 2 – Trainings Finder */}
//       <button
//         type="button"
//         onClick={() => navigate("/my-panchayat/trainings")}
//         className="bg-white dark:bg-gray-900 rounded-3xl shadow-md border border-[#F4E3C3] 
//                    dark:border-gray-700 px-4 py-4 text-left hover:shadow-lg transition cursor-pointer"
//       >
//         <div className="text-xs font-semibold text-[#166534] dark:text-green-300 mb-1">
//           {isHi ? "प्रशिक्षण / क्षमता विकास" : "Trainings / Capacity Building"}
//         </div>

//         <div className="text-sm font-semibold mb-1 text-gray-900 dark:text-gray-100">
//           {isHi ? "पंचायत प्रशिक्षण खोजक" : "Panchayat Trainings Finder"}
//         </div>

//         <p className="text-[11px] text-gray-600 dark:text-gray-300 leading-relaxed">
//           {isHi
//             ? "जिला और ब्लॉक के हिसाब से सभी पंचायत प्रशिक्षण एक ही जगह पर देखें।"
//             : "View all Panchayat trainings by district and block."}
//         </p>
//       </button>

//       {/* Card 3 – Smart Gram Planning */}
//       <button
//         type="button"
//         onClick={() => navigate("/my-panchayat/planning")}
//         className="bg-white dark:bg-gray-900 rounded-3xl shadow-md border border-[#F4E3C3] 
//                    dark:border-gray-700 px-4 py-4 text-left hover:shadow-lg transition cursor-pointer"
//       >
//         <div className="text-xs font-semibold text-[#166534] dark:text-green-300 mb-1">
//           {isHi ? "स्मार्ट ग्राम प्लानिंग" : "Smart Gram Planning"}
//         </div>

//         <div className="text-sm font-semibold mb-1 text-gray-900 dark:text-gray-100">
//           {isHi ? "स्मार्ट ग्राम योजना उपकरण" : "Smart Gram Planning Tool"}
//         </div>

//         <p className="text-[11px] text-gray-600 dark:text-gray-300 leading-relaxed">
//           {isHi
//             ? "ग्राम इन्फ्रा डेफिसिट इंडेक्स के आधार पर विकास प्राथमिकताएँ और सुझाए गए परियोजनाएं देखें।"
//             : "See development priorities and suggested projects based on infra deficit index."}
//         </p>
//       </button>

//     </aside>
//   );
// }

// src/components/layout/RightSidebar.jsx
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../../context/LanguageContext.jsx";

export default function RightSidebar() {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  return (
    <div className="fixed top-25 right-10 space-y-5 w-80 z-40">
      
      {/* FINDER CARD */}
      <div
        onClick={() => navigate("/finder")}
        className="cursor-pointer p-5 bg-white dark:bg-card-dark rounded-2xl shadow-soft border border-stone-200 dark:border-gray-700 hover:shadow-lg transition"
        title={isHi ? "सरकारी योजनाएं / सेवाएँ खोजें" : "Find Schemes & Services"}
      >
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-7 flex items-center justify-center rounded-full bg-primary/10 text-primary">
            <span className="material-symbols-outlined">search</span>
          </div>
          <h3 className="font-bold text-text-main dark:text-text-dark">
            {isHi ? "सरकारी योजनाएं / सेवाएँ खोजें" : "Find Schemes & Services"}
          </h3>
        </div>

        <p className="text-sm font-semibold text-text-main dark:text-white mb-2">
          {isHi ? "योजनाएँ / सेवाएँ / प्रोग्राम" : "Schemes / Services / Programs"}
        </p>
        <p className="text-sm text-text-subtle dark:text-gray-300 leading-relaxed">
          {isHi
            ? "अपने गाँव, जाति, सेवा या अन्य विवरण के आधार पर आपके लिए उपलब्ध सरकारी योजनाएँ देखें।"
            : "Check government schemes available for your village, caste, service or other details."}
        </p>
      </div>


      {/* TRAININGS CARD */}
      <div
        onClick={() => navigate("/my-panchayat/trainings")}
        className="cursor-pointer p-5 bg-white dark:bg-card-dark rounded-2xl shadow-soft border border-stone-200 dark:border-gray-700 hover:shadow-lg transition"
        title={isHi ? "पंचायत प्रशिक्षण खोजक" : "Panchayat Trainings Finder"}
      >
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-7 flex items-center justify-center rounded-full bg-primary/10 text-primary">
            <span className="material-symbols-outlined">school</span>
          </div>
          <h3 className="font-bold text-text-main dark:text-text-dark">
            {isHi ? "पंचायत प्रशिक्षण खोजक" : "Panchayat Trainings Finder"}
          </h3>
        </div>

        <p className="text-sm font-semibold text-text-main dark:text-white mb-2">
          {isHi ? "प्रशिक्षण / क्षमता विकास" : "Training / Capacity Building"}
        </p>
        <p className="text-sm text-text-subtle dark:text-gray-300 leading-relaxed">
          {isHi
            ? "जिला और ब्लॉक के हिसाब से सभी पंचायत प्रशिक्षण एक ही जगह पर देखें।"
            : "View all Panchayat trainings by District and Block in one place."}
        </p>
      </div>


      {/* PLANNING CARD */}
      <div
        onClick={() => navigate("/my-panchayat/planning")}
        className="cursor-pointer p-5 bg-white dark:bg-card-dark rounded-2xl shadow-soft border border-stone-200 dark:border-gray-700 hover:shadow-lg transition"
        title={isHi ? "स्मार्ट ग्राम प्लानिंग" : "Smart Gram Planning"}
      >
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-7 flex items-center justify-center rounded-full bg-primary/10 text-primary">
            <span className="material-symbols-outlined">map</span>
          </div>
          <h3 className="font-bold text-text-main dark:text-text-dark">
            {isHi ? "स्मार्ट ग्राम योजना उपकरण" : "Smart Gram Planning Tool"}
          </h3>
        </div>

        <p className="text-sm font-semibold text-text-main dark:text-white mb-2">
          {isHi ? "स्मार्ट ग्राम प्लानिंग" : "Smart Gram Planning"}
        </p>
        <p className="text-sm text-text-subtle dark:text-gray-300 leading-relaxed">
          {isHi
            ? "ग्राम इन्फ्रा डेफिसिट इंडेक्स के आधार पर विकास प्राथमिकताएँ और सुझाए गए परियोजनाएं देखें।"
            : "See development priorities and suggested projects based on village infra deficit index."}
        </p>
      </div>

    </div>
  );
}

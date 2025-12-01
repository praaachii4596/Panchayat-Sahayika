// src/screens/MyPanchayatScreen.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext.jsx";
import SidebarContainer from "../components/layout/SidebarContainer.jsx";
import LeftSidebar from "../components/layout/LeftSidebar.jsx";
import RightSidebar from "../components/layout/RightSidebar.jsx";

export default function MyPanchayatScreen() {
  const navigate = useNavigate();
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  return (
    <SidebarContainer
      leftContent={<LeftSidebar />}
      rightContent={<RightSidebar />}
    >
      <main className="w-full px-4 md:px-8">

        {/* ===========================
            PAGE TITLE
        ============================ */}
        <div className="mb-10">
          <h1 className="
            text-primary dark:text-white
            text-4xl font-black leading-tight tracking-[-0.03em]
          ">
            {isHi ? "मेरे पंचायत उपकरण" : "My Panchayat Tools"}
          </h1>

          {/* <p className="
            text-text-subtle-light dark:text-text-subtle-dark
            text-base mt-1
          ">
            {isHi ? "मेरे पंचायत उपकरण" : "My village tools & resources"}
          </p> */}
        </div>

        {/* ===========================
            2-CARD GRID
        ============================ */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          {/* ---------------------------------
              CARD 1 — TRAININGS FINDER
          ---------------------------------- */}
          <div
            onClick={() => navigate("/my-panchayat/trainings")}
            className="
              p-4 rounded-2xl 
              bg-white dark:bg-[#2a2a2a]
              border border-stone-200 dark:border-neutral-700
              
              cursor-pointer flex flex-col
              shadow-sm
              hover:shadow-xl dark:hover:shadow-[0_8px_24px_var(--primary)]
              hover:-translate-y-1
              hover:scale-[1.01]
              
              transition-all duration-300 ease-out
            "
          >
            {/* Card Image */}
            <div
              className="w-full aspect-video bg-cover bg-center rounded-xl mb-4 transition-all duration-300"
              style={{
                backgroundImage:
                  "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAKEKtrETw_gAsD3IChapLyZ7dVyuRTjAKPaoR_-ECMKTU5-m0AWTu-PoE-uLsdvS6j321kUkvRQmxnQ8nNMBxIOfBgsjI-bGNQxiAunbcWvTOMU4jE_zsQ-KrElKgovQlnunBvDlPzGZAAqq7xJ0K7yjaXzArVDIf--xIyvDtgoi3L6_2ChK-a9LUVnfZxBv6wgOcTZoaZJPfer1nwFXv0ssYGblgPnx5cFVyDEehbthfxhEm6J-6Qb_pPPiYtXVKOkYbhwo-fFoGs')",
              }}
            />

            {/* Titles */}
            <p className="text-primary dark:text-white text-xl font-bold">
              {isHi ? "पंचायत प्रशिक्षण खोजक" : "Panchayat Trainings Finder"}
            </p>

            {/* Description + Button */}
            <div className="flex items-center justify-between mt-2 mb-2">
              <p className="
                text-sm max-w-xs
                text-text-subtle-light dark:text-gray-300
              ">
                {isHi
            ? "जिला और ब्लॉक के हिसाब से सभी पंचायत प्रशिक्षण एक ही जगह पर देखें।"
            : "View all Panchayat trainings by District and Block in one place."}
              </p>

              {/* <button
                className="
                  h-10 px-5 rounded-xl bg-primary text-white
                  text-sm font-medium hover:bg-primary/90 transition
                "
              >
                {isHi ? "खोलें" : "Open"}
              </button> */}
            </div>
          </div>

          {/* ---------------------------------
              CARD 2 — SMART GRAM PLANNING
          ---------------------------------- */}
          <div
            onClick={() => navigate("/my-panchayat/planning")}
            className="
              p-4 rounded-2xl 
              bg-white dark:bg-[#2a2a2a]
              border border-stone-200 dark:border-neutral-700
              
              cursor-pointer flex flex-col
              
              shadow-sm
              hover:shadow-xl dark:hover:shadow-[0_8px_24px_var(--primary)]
              hover:-translate-y-1
              hover:scale-[1.01]
              
              transition-all duration-300 ease-out
            "
          >
            {/* Card Image */}
            <div
              className="w-full aspect-video bg-cover bg-center rounded-xl mb-4"
              style={{
                backgroundImage:
                  "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBAOLhG4-8HzuJHSEoGMN6835PwQDgp588bE7rcIXCVPxXIysF9g1KGd5h--CGVK4L6nwm9MjQYfZWW7jaZkQ6D5CiSx0hDELqw9bp2y2o0ZRHhTRsn2rRWEH2moFc90uDZkKi_ygpfrJy4fWU9joxqB_Mm9YuLfkXQ48-gG_xknTkxcPR39RThIRP8AItkOdesuGtGa0XA5zJQ6SyA0jFpO_JKPzSphZv4PK9bg0ULaDaEpvfxj7rR_ZNzpfzH_ILmR0eBhrXI1dqf')",
              }}
            />

            {/* Titles */}
            <p className="text-primary dark:text-white text-xl font-bold">
              {isHi ? "स्मार्ट ग्राम योजना उपकरण" : "Smart Gram Planning Tool"}
            </p>

            {/* Description + Button */}
            <div className="flex items-center justify-between mt-2 mb-2">
              <p className="
                text-sm max-w-xs
                text-text-subtle-light dark:text-gray-300
              ">
                {isHi
            ? "ग्राम इन्फ्रा डेफिसिट इंडेक्स के आधार पर विकास प्राथमिकताएँ और सुझाए गए परियोजनाएं देखें।"
            : "See development priorities and suggested projects based on village infra deficit index."}
              </p>

              {/* <button
                className="
                  h-10 px-5 rounded-xl bg-primary text-white
                  text-sm font-medium hover:bg-primary/90 transition
                "
              >
                {isHi ? "खोलें" : "Open"}
              </button> */}
            </div>
          </div>
        </div>

      </main>
    </SidebarContainer>
  );
}

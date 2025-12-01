// // src/screens/RegisterScreen.jsx
// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { useAuth } from "../auth/useAuth.jsx";
// import { useLanguage } from "../context/LanguageContext.jsx";

// import SidebarContainer from "../layout/SidebarContainer.jsx";

// export default function RegisterScreen() {
//   const { register } = useAuth();
//   const { lang } = useLanguage();
//   const isHi = lang === "hi";

//   const navigate = useNavigate();

//   const [form, setForm] = useState({
//     username: "",
//     password: "",
//     full_name: "",
//     district: "",
//     block: "",
//     village_code: "",
//     age: "",
//     gender: "",
//     interest_tag: "",
//     disability: "",
//     occupation: "",
//     income_bracket: "",
//     social_category: "",
//   });

//   const [submitting, setSubmitting] = useState(false);
//   const [error, setError] = useState("");
//   const [successMsg, setSuccessMsg] = useState("");

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setForm((f) => ({ ...f, [name]: value }));
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setError("");
//     setSuccessMsg("");

//     if (!form.username || !form.password) {
//       setError(
//         isHi
//           ? "उपयोगकर्ता नाम और पासवर्ड आवश्यक हैं।"
//           : "Username and password are required."
//       );
//       return;
//     }

//     try {
//       setSubmitting(true);
//       const payload = {
//         ...form,
//         age: form.age ? Number(form.age) : null,
//       };
//       await register(payload);
//       setSuccessMsg(
//         isHi
//           ? "पंजीकरण सफल रहा। अब आप लॉगिन कर सकते हैं।"
//           : "Registration successful. You can now login."
//       );
//       setTimeout(() => navigate("/login"), 800);
//     } catch (err) {
//       console.error(err);
//       setError(
//         isHi
//           ? "पंजीकरण असफल रहा, कृपया फिर से प्रयास करें।"
//           : err.message || "Registration failed, please try again."
//       );
//     } finally {
//       setSubmitting(false);
//     }
//   };

//   return (
//     <SidebarContainer>
//       <section className="w-full flex justify-center px-4 py-8">

//         {/* Main card */}
//         <div className="w-full max-w-3xl bg-white dark:bg-gray-900 
//                         rounded-3xl shadow-md border border-gray-200 
//                         dark:border-gray-700 px-8 py-10 space-y-6">

//           {/* Title */}
//           <h1 className="text-2xl font-semibold text-[#166534] dark:text-green-300">
//             {isHi ? "अपना खाता बनाएँ" : "Create Your Account"}
//           </h1>

//           <p className="text-[13px] text-gray-600 dark:text-gray-400">
//             {isHi
//               ? "कुछ मूल जानकारी भरें ताकि हम आपके लिए सही योजनाएँ और प्रशिक्षण सुझा सकें।"
//               : "Fill in basic details so we can recommend schemes & trainings for you."}
//           </p>

//           {/* FORM */}
//           <form
//             onSubmit={handleSubmit}
//             className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm"
//           >

//             {/* Username */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "उपयोगकर्ता नाम *" : "Username *"}
//               </label>
//               <input
//                 name="username"
//                 value={form.username}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               />
//             </div>

//             {/* District */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "ज़िला" : "District"}
//               </label>
//               <input
//                 name="district"
//                 value={form.district}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               />
//             </div>

//             {/* Password */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "पासवर्ड *" : "Password *"}
//               </label>
//               <input
//                 type="password"
//                 name="password"
//                 value={form.password}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300
//                            dark:border-gray-700 dark:bg-gray-800 text-sm
//                            outline-none focus:border-[#166534]"
//               />
//             </div>

//             {/* Block */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "ब्लॉक" : "Block"}
//               </label>
//               <input
//                 name="block"
//                 value={form.block}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               />
//             </div>

//             {/* Full Name */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "पूरा नाम" : "Full Name"}
//               </label>
//               <input
//                 name="full_name"
//                 value={form.full_name}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               />
//             </div>

//             {/* Village Code */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "गाँव कोड" : "Village Code"}
//               </label>
//               <input
//                 name="village_code"
//                 value={form.village_code}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               />
//             </div>

//             {/* Age */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "आयु" : "Age"}
//               </label>
//               <input
//                 type="number"
//                 name="age"
//                 value={form.age}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               />
//             </div>

//             {/* Gender */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "लिंग" : "Gender"}
//               </label>
//               <select
//                 name="gender"
//                 value={form.gender}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               >
//                 <option value="">{isHi ? "चुनें" : "Select"}</option>
//                 <option value="Female">{isHi ? "महिला" : "Female"}</option>
//                 <option value="Male">{isHi ? "पुरुष" : "Male"}</option>
//                 <option value="Other">{isHi ? "अन्य" : "Other"}</option>
//               </select>
//             </div>

//             {/* Disability */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "विकलांगता" : "Disability"}
//               </label>
//               <select
//                 name="disability"
//                 value={form.disability}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               >
//                 <option value="">{isHi ? "नहीं / नहीं बताना चाहते" : "None"}</option>
//                 <option value="locomotor">{isHi ? "चलने-फिरने में समस्या" : "Locomotor"}</option>
//                 <option value="visual">{isHi ? "दृष्टि बाधित" : "Visual"}</option>
//                 <option value="hearing">{isHi ? "श्रवण बाधित" : "Hearing"}</option>
//                 <option value="intellectual">{isHi ? "बौद्धिक विकलांगता" : "Intellectual"}</option>
//                 <option value="multiple">{isHi ? "एक से अधिक" : "Multiple"}</option>
//               </select>
//             </div>

//             {/* Occupation */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "पेशा" : "Occupation"}
//               </label>
//               <select
//                 name="occupation"
//                 value={form.occupation}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               >
//                 <option value="">{isHi ? "चुनें" : "Select"}</option>
//                 <option value="farmer">{isHi ? "किसान" : "Farmer"}</option>
//                 <option value="student">{isHi ? "छात्र" : "Student"}</option>
//                 <option value="anganwadi">{isHi ? "आंगनवाड़ी कार्यकर्ता" : "Anganwadi"}</option>
//                 <option value="asha">{isHi ? "आशा / स्वास्थ्य कार्यकर्ता" : "ASHA worker"}</option>
//                 <option value="shg_member">{isHi ? "एसएचजी सदस्य" : "SHG Member"}</option>
//                 <option value="labour">{isHi ? "मज़दूर" : "Labour"}</option>
//                 <option value="homemaker">{isHi ? "गृहणी" : "Homemaker"}</option>
//                 <option value="other">{isHi ? "अन्य" : "Other"}</option>
//               </select>
//             </div>

//             {/* Income Bracket */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "आय वर्ग" : "Income Bracket"}
//               </label>
//               <select
//                 name="income_bracket"
//                 value={form.income_bracket}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               >
//                 <option value="">{isHi ? "चुनें" : "Select"}</option>
//                 <option value="BPL">{isHi ? "बीपीएल / अंत्योदय" : "BPL"}</option>
//                 <option value="APL">{isHi ? "एपीएल" : "APL"}</option>
//                 <option value="lower_middle">{isHi ? "निम्न मध्यम" : "Lower Middle"}</option>
//                 <option value="middle">{isHi ? "मध्यम वर्ग" : "Middle"}</option>
//               </select>
//             </div>

//             {/* Social Category */}
//             <div className="space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "सामाजिक वर्ग" : "Social Category"}
//               </label>
//               <select
//                 name="social_category"
//                 value={form.social_category}
//                 onChange={handleChange}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               >
//                 <option value="">{isHi ? "चुनें" : "Select"}</option>
//                 <option value="SC">{isHi ? "अनुसूचित जाति (SC)" : "SC"}</option>
//                 <option value="ST">{isHi ? "अनुसूचित जनजाति (ST)" : "ST"}</option>
//                 <option value="OBC">{isHi ? "ओबीसी" : "OBC"}</option>
//                 <option value="General">{isHi ? "सामान्य" : "General"}</option>
//               </select>
//             </div>

//             {/* Interest */}
//             <div className="sm:col-span-2 space-y-1">
//               <label className="text-[12px] font-medium text-gray-700 dark:text-gray-300">
//                 {isHi ? "रुचि टैग" : "Interest Tag"}
//               </label>
//               <input
//                 name="interest_tag"
//                 value={form.interest_tag}
//                 onChange={handleChange}
//                 placeholder={isHi ? "किसान, छात्र..." : "farmer, student..."}
//                 className="w-full px-4 py-2 rounded-xl border border-gray-300 
//                            dark:border-gray-700 dark:bg-gray-800 text-sm 
//                            outline-none focus:border-[#166534]"
//               />
//             </div>

//             {/* Messages */}
//             <div className="sm:col-span-2">
//               {error && (
//                 <p className="text-[12px] text-red-500">{error}</p>
//               )}
//               {successMsg && (
//                 <p className="text-[12px] text-green-600">{successMsg}</p>
//               )}
//             </div>

//             {/* Submit */}
//             <div className="sm:col-span-2">
//               <button
//                 type="submit"
//                 disabled={submitting}
//                 className="w-full bg-[#166534] dark:bg-green-700 text-white 
//                            py-2 rounded-xl font-semibold text-sm 
//                            disabled:opacity-60"
//               >
//                 {submitting
//                   ? isHi
//                     ? "खाता बनाया जा रहा है..."
//                     : "Creating account..."
//                   : isHi
//                     ? "रजिस्टर करें"
//                     : "Register"}
//               </button>

//               <p className="text-[12px] text-gray-600 dark:text-gray-300 mt-2">
//                 {isHi ? "पहले से खाता है?" : "Already have an account?"}{" "}
//                 <button
//                   type="button"
//                   onClick={() => navigate("/login")}
//                   className="text-[#166534] dark:text-green-300 underline"
//                 >
//                   {isHi ? "लॉगिन करें" : "Login"}
//                 </button>
//               </p>
//             </div>
//           </form>
//         </div>
//       </section>
//     </SidebarContainer>
//   );
// }

// src/screens/RegisterScreen.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth.jsx";
import { useLanguage } from "../context/LanguageContext.jsx";

import SidebarContainer from "../components/layout/SidebarContainer.jsx";
import LeftSidebar from "../components/layout/LeftSidebar.jsx";
import RightSidebar from "../components/layout/RightSidebar.jsx";

export default function RegisterScreen() {
  const { register } = useAuth();
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
    full_name: "",
    district: "",
    block: "",
    village_code: "",
    age: "",
    gender: "",
    interest_tag: "",
    disability: "",
    occupation: "",
    income_bracket: "",
    social_category: "",
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccessMsg("");

    if (!form.username || !form.password) {
      setError(
        isHi
          ? "उपयोगकर्ता नाम और पासवर्ड आवश्यक हैं।"
          : "Username and password are required."
      );
      return;
    }

    try {
      setSubmitting(true);
      const payload = { ...form, age: form.age ? Number(form.age) : null };
      await register(payload);

      setSuccessMsg(
        isHi
          ? "पंजीकरण सफल रहा! अब आप लॉगिन कर सकते हैं।"
          : "Registration successful! You can now login."
      );

      setTimeout(() => navigate("/login"), 900);
    } catch (err) {
      setError(
        isHi
          ? "पंजीकरण असफल रहा, कृपया फिर से प्रयास करें।"
          : err.message || "Registration failed. Try again."
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <SidebarContainer
      leftContent={<LeftSidebar />}
      rightContent={<RightSidebar />}
    >
      <section className="flex justify-center px-4 w-full">
        <div className="w-full max-w-2xl bg-white dark:bg-[#2d2d2d] rounded-2xl shadow-soft border border-gray-200 dark:border-gray-700 p-8 md:p-10">
          {/* Title */}
          <div className="text-center mb-8">
            <h2 className="text-3xl font-extrabold text-textMain dark:text-white">
              {isHi ? "अपना खाता बनाएँ" : "Create Your Account"}
            </h2>

            <p className="mt-2 text-textSubtle dark:text-gray-300 text-sm">
              {isHi
                ? "शुरू करने के लिए नीचे दिए गए विवरण भरें।"
                : "Fill in the details below to get started."}
            </p>
          </div>

          {/* FORM */}
          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 gap-6 sm:grid-cols-2"
          >
            {/* USERNAME */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "उपयोगकर्ता नाम *" : "Username *"}
              </p>
              <input
                name="username"
                value={form.username}
                onChange={handleChange}
                placeholder={
                  isHi ? "अपना उपयोगकर्ता नाम दर्ज करें" : "Enter username"
                }
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a] placeholder:text-gray-400 dark:placeholder:text-gray-300 focus:ring-2 focus:ring-primary/50"
              />
            </label>

            {/* DISTRICT */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "ज़िला" : "District"}
              </p>
              <input
                name="district"
                value={form.district}
                onChange={handleChange}
                placeholder={isHi ? "ज़िला दर्ज करें" : "Enter district"}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              />
            </label>

            {/* PASSWORD */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "पासवर्ड *" : "Password *"}
              </p>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                placeholder={
                  isHi ? "सुरक्षित पासवर्ड दर्ज करें" : "Enter password"
                }
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              />
            </label>

            {/* BLOCK */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "ब्लॉक" : "Block"}
              </p>
              <input
                name="block"
                value={form.block}
                onChange={handleChange}
                placeholder={isHi ? "ब्लॉक दर्ज करें" : "Enter block"}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              />
            </label>

            {/* FULL NAME */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "पूरा नाम" : "Full Name"}
              </p>
              <input
                name="full_name"
                value={form.full_name}
                onChange={handleChange}
                placeholder={isHi ? "अपना पूरा नाम दर्ज करें" : "Enter full name"}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              />
            </label>

            {/* VILLAGE CODE */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "गाँव कोड" : "Village Code"}
              </p>
              <input
                name="village_code"
                value={form.village_code}
                onChange={handleChange}
                placeholder={isHi ? "गाँव कोड दर्ज करें" : "Enter code"}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              />
            </label>

            {/* AGE */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "आयु" : "Age"}
              </p>
              <input
                type="number"
                name="age"
                value={form.age}
                onChange={handleChange}
                placeholder={isHi ? "आयु दर्ज करें" : "Enter age"}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              />
            </label>

            {/* GENDER */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "लिंग" : "Gender"}
              </p>
              <select
                name="gender"
                value={form.gender}
                onChange={handleChange}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              >
                <option value="">{isHi ? "चुनें" : "Select"}</option>
                <option value="Male">{isHi ? "पुरुष" : "Male"}</option>
                <option value="Female">{isHi ? "महिला" : "Female"}</option>
                <option value="Other">{isHi ? "अन्य" : "Other"}</option>
              </select>
            </label>

            {/* DISABILITY */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "विकलांगता" : "Disability"}
              </p>
              <select
                name="disability"
                value={form.disability}
                onChange={handleChange}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              >
                <option value="">
                  {isHi ? "नहीं / बताना नहीं चाहते"
                    : "None / Prefer not to say"}
                </option>
                <option value="locomotor">
                  {isHi ? "चलने-फिरने में समस्या (Locomotor)" : "Locomotor disability"}
                </option>
                <option value="visual">
                  {isHi ? "दृष्टि बाधित (Visual)" : "Visual impairment"}
                </option>
                <option value="hearing">
                  {isHi ? "श्रवण बाधित (Hearing)" : "Hearing impairment"}
                </option>
                <option value="intellectual">
                  {isHi ? "बौद्धिक विकलांगता" : "Intellectual disability"}
                </option>
                <option value="multiple">
                  {isHi ? "एक से अधिक (Multiple)" : "Multiple disabilities"}
                </option>
              </select>
            </label>

            {/* OCCUPATION */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "पेशा" : "Occupation"}
              </p>
              <select
                name="occupation"
                value={form.occupation}
                onChange={handleChange}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              >
                <option value="">
                  {isHi ? "चुनें" : "Select"}
                </option>
                <option value="farmer">
                  {isHi ? "किसान (Farmer)" : "Farmer"}
                </option>
                <option value="student">
                  {isHi ? "छात्र / छात्रा (Student)" : "Student"}
                </option>
                <option value="anganwadi">
                  {isHi ? "आंगनवाड़ी कार्यकर्ता" : "Anganwadi worker"}
                </option>
                <option value="asha">
                  {isHi ? "आशा / स्वास्थ्य कार्यकर्ता" : "ASHA worker"}
                </option>
                <option value="shg_member">
                  {isHi ? "एसएचजी सदस्य" : "SHG member"}
                </option>
                <option value="labour">
                  {isHi ? "दैनिक मज़दूर (Daily wage labour)" : "Daily wage labour"}
                </option>
                <option value="homemaker">
                  {isHi ? "गृहणी (Homemaker)" : "Homemaker"}
                </option>
                <option value="other">
                  {isHi ? "अन्य (Other)" : "Other"}
                </option>
              </select>
            </label>

            {/* INCOME BRACKET */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "आय वर्ग" : "Income Bracket"}
              </p>
              <select
                name="income_bracket"
                value={form.income_bracket}
                onChange={handleChange}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              >
                <option value="">
                  {isHi ? "चुनें" : "Select"}
                </option>
                <option value="BPL">
                  {isHi ? "बीपीएल / अंत्योदय (BPL)" : "BPL / Antyodaya"}
                </option>
                <option value="APL">
                  {isHi ? "एपीएल (APL)" : "APL"}
                </option>
                <option value="lower_middle">
                  {isHi ? "निम्न मध्यम वर्ग" : "Lower middle"}
                </option>
                <option value="middle">
                  {isHi ? "मध्यम वर्ग" : "Middle"}
                </option>
              </select>
            </label>

            {/* SOCIAL CATEGORY */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "सामाजिक वर्ग" : "Social Category"}
              </p>
              <select
                name="social_category"
                value={form.social_category}
                onChange={handleChange}
                className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
              >
                <option value="">{isHi ? "चुनें" : "Select"}</option>
                <option value="SC">
                  {isHi ? "अनुसूचित जाति (SC)" : "SC"}
                </option>
                <option value="ST">
                  {isHi ? "अनुसूचित जनजाति (ST)" : "ST"}
                </option>
                <option value="OBC">
                  {isHi ? "ओबीसी (OBC)" : "OBC"}
                </option>
                <option value="General">
                  {isHi ? "सामान्य (General)" : "General"}
                </option>
              </select>
            </label>

            {/* INTEREST TAG */}
            <div className="sm:col-span-2">
              <label className="flex flex-col">
                <p className="pb-2 text-sm font-medium dark:text-gray-200">
                  {isHi ? "रुचि टैग" : "Interest Tag"}
                </p>
                <input
                  name="interest_tag"
                  value={form.interest_tag}
                  onChange={handleChange}
                  placeholder={
                    isHi ? "किसान, छात्र..." : "farmer, student..."
                  }
                  className="h-12 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]"
                />
              </label>
            </div>

            {/* Messages */}
            {error && (
              <p className="sm:col-span-2 text-sm text-red-500">{error}</p>
            )}

            {successMsg && (
              <p className="sm:col-span-2 text-sm text-green-600">
                {successMsg}
              </p>
            )}

            {/* SUBMIT BUTTON */}
            <div className="sm:col-span-2 mt-2">
              <button
                type="submit"
                disabled={submitting}
                className="w-full h-12 bg-primary text-white rounded-xl font-bold hover:bg-primary/90 disabled:opacity-60 transition"
              >
                {submitting
                  ? isHi
                    ? "बना रहा है..."
                    : "Creating..."
                  : isHi
                  ? "रजिस्टर करें"
                  : "Register"}
              </button>

              {/* LOGIN LINK */}
              <p className="text-center mt-6 text-sm text-gray-700 dark:text-gray-300">
                {isHi ? "पहले से खाता है?" : "Already have an account?"}{" "}
                <button
                  type="button"
                  onClick={() => navigate("/login")}
                  className="text-primary font-semibold hover:underline"
                >
                  {isHi ? "लॉगिन करें" : "Login"}
                </button>
              </p>
            </div>
          </form>
        </div>
      </section>
    </SidebarContainer>
  );
}

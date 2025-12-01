// src/screens/EditProfileScreen.jsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth.jsx";
import { useLanguage } from "../context/LanguageContext.jsx";

import SidebarContainer from "../components/layout/SidebarContainer.jsx";
import LeftSidebar from "../components/layout/LeftSidebar.jsx";
import RightSidebar from "../components/layout/RightSidebar.jsx";

export default function EditProfileScreen() {
  const { user, updateProfile } = useAuth();
  const { lang } = useLanguage();
  const isHi = lang === "hi";

  const navigate = useNavigate();

  const [form, setForm] = useState({
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

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  // Load user data
  useEffect(() => {
    if (!user) return;
    setForm({
      full_name: user.full_name || "",
      district: user.district || "",
      block: user.block || "",
      village_code: user.village_code || "",
      age: user.age ?? "",
      gender: user.gender || "",
      interest_tag: user.interest_tag || "",
      disability: user.disability || "",
      occupation: user.occupation || "",
      income_bracket: user.income_bracket || "",
      social_category: user.social_category || "",
    });
  }, [user]);

  if (!user) {
    return (
      <section className="mt-8 text-sm text-center">
        {isHi
          ? "कृपया अपनी प्रोफ़ाइल संपादित करने के लिए लॉगिन करें।"
          : "Please login to edit your profile."}
      </section>
    );
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccessMsg("");

    try {
      setSaving(true);

      const payload = {
        ...form,
        age: form.age ? Number(form.age) : null,
      };

      await updateProfile(payload);

      setSuccessMsg(
        isHi
          ? "प्रोफ़ाइल सफलतापूर्वक अपडेट हो गई।"
          : "Profile updated successfully."
      );

      setTimeout(() => navigate("/dashboard"), 750);
    } catch (err) {
      setError(
        isHi
          ? "अपडेट करते समय त्रुटि हुई।"
          : err.message || "Update failed"
      );
    } finally {
      setSaving(false);
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
              {isHi ? "अपनी प्रोफ़ाइल संपादित करें" : "Edit Your Profile"}
            </h2>
            <p className="mt-2 text-textSubtle dark:text-gray-300 text-sm">
              {isHi
                ? "अपनी जानकारी अपडेट करें ताकि सिफ़ारिशें सटीक रहें।"
                : "Update your information to improve recommendations."}
            </p>
          </div>

          {/* FORM */}
          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 sm:grid-cols-2 gap-6"
          >
            {/* Full Name */}
            <label className="flex flex-col">
              <p className="pb-2 text-sm font-medium dark:text-gray-200">
                {isHi ? "पूरा नाम" : "Full Name"}
              </p>
              <input
                name="full_name"
                value={form.full_name}
                onChange={handleChange}
                placeholder={isHi ? "पूरा नाम दर्ज करें" : "Enter full name"}
                className="h-12 px-4 rounded-xl border border-gray-300 
                dark:border-gray-700 bg-[#FEF6EF] dark:bg-[#1a1a1a]
                placeholder:text-gray-400 dark:placeholder:text-gray-300
                focus:ring-2 focus:ring-primary/50"
              />
            </label>

            {/* District */}
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

            {/* Block */}
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

            {/* Village Code */}
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

            {/* Age */}
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

            {/* Gender */}
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

            {/* Disability */}
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

            {/* Occupation */}
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

            {/* Income */}
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

            {/* Social Category */}
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

            {/* Interest Tag */}
            <div className="sm:col-span-2">
              <label className="flex flex-col">
                <p className="pb-2 text-sm font-medium dark:text-gray-200">
                  {isHi ? "रुचि टैग" : "Interest Tag"}
                </p>
                <input
                  name="interest_tag"
                  value={form.interest_tag}
                  onChange={handleChange}
                  placeholder={isHi ? "किसान, छात्र..." : "farmer, student..."}
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

            {/* BUTTONS */}
            <div className="sm:col-span-2 flex items-center justify-between mt-4">
              <button
                type="button"
                onClick={() => navigate(-1)}
                className="h-12 px-6 rounded-xl border border-gray-400 dark:border-gray-500 text-sm dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                {isHi ? "रद्द करें" : "Cancel"}
              </button>

              <button
                type="submit"
                disabled={saving}
                className="h-12 px-6 rounded-xl bg-primary text-white text-sm font-semibold hover:bg-primary/90 disabled:opacity-60"
              >
                {saving
                  ? isHi
                    ? "सेव हो रहा है..."
                    : "Saving..."
                  : isHi
                  ? "बदलाव सेव करें"
                  : "Save Changes"}
              </button>
            </div>
          </form>
        </div>
      </section>
    </SidebarContainer>
  );
}

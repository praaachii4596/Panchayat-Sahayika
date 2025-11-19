# # # import os
# # # import json
# # # import uuid
# # # import re
# # # import unicodedata
# # # from pathlib import Path
# # # from typing import List, Dict, Any, Optional, Tuple

# # # from dotenv import load_dotenv
# # # from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from fastapi.responses import HTMLResponse
# # # from fastapi.templating import Jinja2Templates

# # # from pydantic import BaseModel

# # # from qdrant_client import QdrantClient
# # # from qdrant_client.models import (
# # #     VectorParams,
# # #     Distance,
# # #     PointStruct,
# # #     Filter,
# # #     FieldCondition,
# # #     MatchText,
# # # )
# # # from qdrant_client.http import models as qm  # noqa: F401  (kept if later needed)

# # # from sentence_transformers import SentenceTransformer
# # # from fastembed import TextEmbedding
# # # from groq import Groq
# # # from googletrans import Translator  # Google Translate

# # # from sqlmodel import Field, SQLModel, Session, create_engine, select
# # # from passlib.context import CryptContext
# # # from jose import JWTError, jwt
# # # from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# # # # ================== CONFIG ==================

# # # BASE_DIR = Path(__file__).resolve().parent.parent  # repo root (panchayat-sahayika)

# # # # Schemes JSON path
# # # SCHEMES_PATH = BASE_DIR / "samaj_kalyan_vibhag_clean_typed.json"
# # # # or, if in public:
# # # # SCHEMES_PATH = BASE_DIR / "public" / "samaj_kalyan_vibhag_clean_typed.json"

# # # load_dotenv()

# # # # ---- Groq / LLM ----
# # # GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# # # if not GROQ_API_KEY:
# # #     raise RuntimeError("GROQ_API_KEY missing in .env")

# # # LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
# # # GROQ_MODEL_DOCS = os.getenv("GROQ_MODEL", LLM_MODEL)

# # # groq_client = Groq(api_key=GROQ_API_KEY)

# # # # ---- DOCS RAG Qdrant (remote or local) ----
# # # DOC_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# # # DOC_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
# # # DOC_COLLECTION = os.getenv("COLLECTION_NAME", "panchayat_uk_docs")

# # # doc_qclient = QdrantClient(url=DOC_QDRANT_URL, api_key=DOC_QDRANT_API_KEY)
# # # doc_embedder = TextEmbedding()

# # # # ---- Schemes Qdrant (local embedded) ----
# # # EMBED_MODEL_NAME_SCHEMES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# # # SCHEMES_COLLECTION = "samaj_kalyan_vibhag_schemes"

# # # scheme_embed_model = SentenceTransformer(EMBED_MODEL_NAME_SCHEMES)
# # # scheme_qdrant = QdrantClient(path=str(BASE_DIR / "qdrant_data"))

# # # origins = [
# # #     "http://localhost:5173",
# # #     "http://127.0.0.1:5173",
# # # ]

# # # # ---- FastAPI + Templates ----
# # # app = FastAPI(title="Panchayat Sahayika Unified Backend")

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
# # #     allow_headers=["*"],
# # # )

# # # templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# # # translator = Translator()  # Google translator instance

# # # # ================== AUTH / USERS ==================

# # # DATABASE_URL = "sqlite:///./panchayat_users.db"  # SQLite file in backend folder
# # # engine = create_engine(DATABASE_URL, echo=False)

# # # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# # # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # # SECRET_KEY = os.getenv("SECRET_KEY", "baea29ce56f4b02733883b6ae1a76265988d123d5ad3e9d2214dae4646a81ee6")
# # # ALGORITHM = "HS256"
# # # ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# # # class User(SQLModel, table=True):
# # #     id: Optional[int] = Field(default=None, primary_key=True)
# # #     username: str = Field(index=True, unique=True)
# # #     full_name: Optional[str] = None
# # #     hashed_password: str

# # #     # profile info (for recommendations / chatbot)
# # #     district: Optional[str] = None
# # #     block: Optional[str] = None
# # #     village_code: Optional[str] = None
# # #     age: Optional[int] = None
# # #     gender: Optional[str] = None          # "M"/"F"/"O" or free text
# # #     interest_tag: Optional[str] = None    # "farmer", "student", etc.

# # #     disability: Optional[str] = None      # e.g. "none", "locomotor", "visual", etc.
# # #     occupation: Optional[str] = None      # "farmer", "student", "ASHA", "SHG member"...
# # #     income_bracket: Optional[str] = None  # "BPL", "APL", etc.
# # #     social_category: Optional[str] = None # "SC", "ST", "OBC", "General", etc.


# # # class UserCreate(SQLModel):
# # #     username: str
# # #     password: str
# # #     full_name: Optional[str] = None
# # #     district: Optional[str] = None
# # #     block: Optional[str] = None
# # #     village_code: Optional[str] = None
# # #     age: Optional[int] = None
# # #     gender: Optional[str] = None
# # #     interest_tag: Optional[str] = None

# # #     disability: Optional[str] = None
# # #     occupation: Optional[str] = None
# # #     income_bracket: Optional[str] = None
# # #     social_category: Optional[str] = None


# # # class UserRead(SQLModel):
# # #     id: int
# # #     username: str
# # #     full_name: Optional[str] = None
# # #     district: Optional[str] = None
# # #     block: Optional[str] = None
# # #     village_code: Optional[str] = None
# # #     age: Optional[int] = None
# # #     gender: Optional[str] = None
# # #     interest_tag: Optional[str] = None

# # #     disability: Optional[str] = None
# # #     occupation: Optional[str] = None
# # #     income_bracket: Optional[str] = None
# # #     social_category: Optional[str] = None

# # # class UserUpdate(SQLModel):
# # #     full_name: Optional[str] = None
# # #     district: Optional[str] = None
# # #     block: Optional[str] = None
# # #     village_code: Optional[str] = None
# # #     age: Optional[int] = None
# # #     gender: Optional[str] = None
# # #     interest_tag: Optional[str] = None

# # #     disability: Optional[str] = None
# # #     occupation: Optional[str] = None
# # #     income_bracket: Optional[str] = None
# # #     social_category: Optional[str] = None

# # # class Token(SQLModel):
# # #     access_token: str
# # #     token_type: str = "bearer"


# # # def create_db_and_tables():
# # #     SQLModel.metadata.create_all(engine)


# # # def get_session():
# # #     with Session(engine) as session:
# # #         yield session


# # # def _bcrypt_safe(password: str) -> str:
# # #     """
# # #     Bcrypt only uses first 72 bytes of the password.
# # #     To avoid errors, we explicitly cut to 72 bytes.
# # #     """
# # #     if password is None:
# # #         return ""
# # #     pw_bytes = password.encode("utf-8")
# # #     return pw_bytes[:72].decode("utf-8", errors="ignore")


# # # def get_password_hash(password: str) -> str:
# # #     safe_pw = _bcrypt_safe(password)
# # #     return pwd_context.hash(safe_pw)


# # # def verify_password(plain: str, hashed: str) -> bool:
# # #     safe_pw = _bcrypt_safe(plain)
# # #     return pwd_context.verify(safe_pw, hashed)


# # # def create_access_token(data: dict) -> str:
# # #     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# # # def get_user_by_username(session: Session, username: str) -> Optional[User]:
# # #     stmt = select(User).where(User.username == username)
# # #     return session.exec(stmt).first()


# # # async def get_current_user(
# # #     token: str = Depends(oauth2_scheme),
# # #     session: Session = Depends(get_session),
# # # ) -> User:
# # #     credentials_exception = HTTPException(
# # #         status_code=status.HTTP_401_UNAUTHORIZED,
# # #         detail="Could not validate credentials",
# # #         headers={"WWW-Authenticate": "Bearer"},
# # #     )
# # #     try:
# # #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# # #         username: Optional[str] = payload.get("sub")
# # #         if username is None:
# # #             raise credentials_exception
# # #     except JWTError:
# # #         raise credentials_exception

# # #     user = get_user_by_username(session, username=username)
# # #     if not user:
# # #         raise credentials_exception
# # #     return user


# # # @app.on_event("startup")
# # # def on_startup():
# # #     create_db_and_tables()

# # # # ================== COMMON LANGUAGE HELPERS ==================


# # # def contains_devanagari(text: str) -> bool:
# # #     """Check if text has any Devanagari characters."""
# # #     for ch in text:
# # #         if "\u0900" <= ch <= "\u097F":
# # #             return True
# # #     return False


# # # def _llm_translate(text: str, target_desc: str) -> str:
# # #     """
# # #     Generic translator using Groq LLM.
# # #     `target_desc` = description of target language/style.
# # #     """
# # #     system_msg = (
# # #         "You are a translator for Gram Panchayat content.\n"
# # #         "You ONLY translate the text; you do not add explanations.\n"
# # #         "Preserve markdown bold markers **like this** exactly as they are.\n"
# # #         "Do not change the meaning; only change the language.\n"
# # #     )

# # #     user_msg = (
# # #         f"Translate the following text into {target_desc}\n\n"
# # #         f"Text:\n{text}"
# # #     )

# # #     completion = groq_client.chat.completions.create(
# # #         model=LLM_MODEL,
# # #         messages=[
# # #             {"role": "system", "content": system_msg},
# # #             {"role": "user", "content": user_msg},
# # #         ],
# # #         temperature=0.2,
# # #         max_tokens=1200,
# # #     )
# # #     out = completion.choices[0].message.content or text
# # #     return out


# # # def translate_answer(text: str, target_lang: str) -> str:
# # #     """
# # #     Final step translation:

# # #     target_lang:
# # #       - 'en'       -> FIRST try Google Translate to English,
# # #                      if fail or Hindi aa jaye to Groq se English.
# # #       - 'hi'       -> Groq se simple Hindi (Devanagari)
# # #       - 'hinglish' -> Groq se simple Hinglish (Roman Hindi)
# # #     """

# # #     # ---------- 1) English UI ----------
# # #     if target_lang == "en":
# # #         try:
# # #             res = translator.translate(text, dest="en")
# # #             out = res.text
# # #             if out and not contains_devanagari(out) and out.strip() != "":
# # #                 return out
# # #         except Exception:
# # #             pass

# # #         return _llm_translate(
# # #             text,
# # #             "clear, simple English suitable for village-level users. "
# # #             "Avoid Hindi script and use plain English sentences."
# # #         )

# # #     # ---------- 2) Hindi (Devanagari) ----------
# # #     if target_lang == "hi":
# # #         return _llm_translate(
# # #             text,
# # #             "very simple Hindi in Devanagari script, using everyday words "
# # #             "that village-level users understand."
# # #         )

# # #     # ---------- 3) Hinglish (Roman Hindi) ----------
# # #     return _llm_translate(
# # #         text,
# # #         "very simple Hinglish (Roman Hindi using English letters). "
# # #         "Do NOT use Devanagari characters."
# # #     )


# # # def _convert_markdown_bold_to_html(text: str) -> str:
# # #     """**bold** -> <strong>bold</strong> for UI."""
# # #     return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


# # # # ================== DOCS RAG PIPELINE ==================


# # # def build_docs_system_prompt() -> str:
# # #     """
# # #     System prompt for docs:
# # #     - Sirf Qdrant se aaye context ka use karo
# # #     - Gram Panchayat users ke liye simple Hindi
# # #     """
# # #     return (
# # #         "आप 'Panchayat Sahayika' हैं, उत्तराखंड की ग्राम पंचायतों के लिए सहायक।\n"
# # #         "आपको केवल नीचे दिए गए संदर्भ (official Panchayati Raj documents: acts, rules, guidelines, roles, schemes, training material)\n"
# # #         "का इस्तेमाल करके ही जवाब देना है।\n\n"
# # #         "भाषा बहुत ही सरल और आसान हिन्दी होनी चाहिए ताकि सरपंच, वार्ड मेंबर और ग्राम पंचायत कर्मचारी आसानी से समझ सकें।\n"
# # #         "कानूनी भारी शब्दों से बचें।\n"
# # #         "अगर ज़रूरी जानकारी संदर्भ में नहीं है, तो साफ-साफ लिखें कि यह जानकारी उपलब्ध नहीं है और आप अंदाज़ा नहीं लगा रहे हैं।\n"
# # #         "कभी भी दस्तावेज़ का नाम, फाइल का नाम, पेज नंबर या 'source' list का ज़िक्र न करें।\n"
# # #     )


# # # def retrieve_docs_context(query: str, top_k: int = 8) -> List[Dict[str, Any]]:
# # #     query_vec = list(doc_embedder.embed([query]))[0]
# # #     results = doc_qclient.search(
# # #         collection_name=DOC_COLLECTION,
# # #         query_vector=query_vec,
# # #         limit=top_k,
# # #         with_payload=True,
# # #     )

# # #     contexts = []
# # #     for r in results:
# # #         pl = r.payload or {}
# # #         contexts.append(
# # #             {
# # #                 "text": pl.get("text", ""),
# # #                 "source_file": pl.get("source_file", ""),
# # #                 "page": pl.get("page", ""),
# # #                 "url": pl.get("url", ""),
# # #                 "score": r.score,
# # #             }
# # #         )
# # #     return contexts


# # # def generate_docs_answer_raw(
# # #     query: str,
# # #     history: List[Dict[str, str]],
# # #     user_meta: Dict[str, Any] | None = None,
# # # ) -> Tuple[str, List[Dict[str, Any]]]:
# # #     """
# # #     Returns raw answer in Hindi-ish language (LLM decides, but system prompt nudges to Hindi).
# # #     We will later translate to final UI language using translate_answer().
# # #     """
# # #     contexts = retrieve_docs_context(query)

# # #     context_block = "\n\n---\n\n".join(
# # #         c["text"] for c in contexts if c["text"]
# # #     )

# # #     # 👤 personalise a bit
# # #     user_ctx = build_user_context(user_meta)

# # #     system_prompt = build_docs_system_prompt()
# # #     if user_ctx:
# # #         system_prompt += (
# # #             "\n\nउपयोगकर्ता प्रोफाइल (उदाहरणों को practical banane ke liye):\n"
# # #             f"{user_ctx}\n"
# # #             "जवाब में आप user ki स्थिति ke हिसाब से छोटा सा context de sakte hain "
# # #             "(jaise किसान, छात्र, दिव्यांग इत्यादि)."
# # #         )

# # #     messages = [
# # #         {"role": "system", "content": system_prompt},
# # #     ]

# # #     # include a few last turns from history (server-side only)
# # #     for h in history[-4:]:
# # #         messages.append({"role": h["role"], "content": h["content"]})

# # #     messages.append(
# # #         {
# # #             "role": "user",
# # #             "content": (
# # #                 f"प्रश्न: {query}\n\n"
# # #                 f"नीचे दिए गए दस्तावेज़ों के संदर्भ का उपयोग करके उत्तर दीजिए। "
# # #                 f"अपने उत्तर में इन दस्तावेज़ों के नाम या पेज नंबर का ज़िक्र मत कीजिए:\n\n"
# # #                 f"{context_block}"
# # #             ),
# # #         }
# # #     )

# # #     completion = groq_client.chat.completions.create(
# # #         model=GROQ_MODEL_DOCS,
# # #         messages=messages,
# # #         temperature=0.3,
# # #         max_tokens=900,
# # #     )
# # #     raw_answer = completion.choices[0].message.content or ""

# # #     # dedupe sources
# # #     unique_sources = []
# # #     seen = set()
# # #     for c in contexts:
# # #         key = (c["source_file"], c["page"])
# # #         if key not in seen and c["source_file"]:
# # #             seen.add(key)
# # #             unique_sources.append(
# # #                 {
# # #                     "source_file": c["source_file"],
# # #                     "page": c["page"],
# # #                     "url": c["url"],
# # #                 }
# # #             )

# # #     return raw_answer, unique_sources


# # # # ================== SCHEMES PIPELINE ==================

# # # def load_schemes() -> List[Dict[str, Any]]:
# # #     with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
# # #         data = json.load(f)
# # #     # ensure strings and minimal keys exist
# # #     for s in data:
# # #         s.setdefault("name_hi", "")
# # #         s.setdefault("name_en", "")
# # #         s.setdefault("category", "")
# # #         s.setdefault("department", "")
# # #         s.setdefault("description_hi", "")
# # #         s.setdefault("description_en", "")
# # #         s.setdefault("eligibility", "")
# # #         s.setdefault("benefit", "")
# # #         s.setdefault("apply_process", "")
# # #         s.setdefault("apply_link", "")
# # #         s.setdefault("source_url", "")
# # #         s.setdefault("type", s.get("type", "scheme"))
# # #     return data


# # # def _concat_item_text(s: Dict[str, Any]) -> str:
# # #     """
# # #     Text used for vector embedding.
# # #     We heavily weight the scheme name so that exact-name queries hit correctly.
# # #     """
# # #     name = (s.get("name_hi", "") + " " + s.get("name_en", "")).strip()
# # #     other_parts = [
# # #         s.get("category", ""),
# # #         s.get("department", ""),
# # #         s.get("description_hi", ""),
# # #         s.get("description_en", ""),
# # #         s.get("eligibility", ""),
# # #         s.get("benefit", ""),
# # #         s.get("apply_process", ""),
# # #     ]

# # #     # Repeat name 5x → boosts similarity when user types scheme name
# # #     weighted_name = " ".join([name] * 5) if name else ""
# # #     rest = " | ".join([str(p) for p in other_parts if p])

# # #     return " | ".join([p for p in [weighted_name, rest] if p])


# # # def init_schemes_collection():
# # #     schemes = load_schemes()

# # #     scheme_qdrant.recreate_collection(
# # #         collection_name=SCHEMES_COLLECTION,
# # #         vectors_config=VectorParams(
# # #             size=scheme_embed_model.get_sentence_embedding_dimension(),
# # #             distance=Distance.COSINE,
# # #         ),
# # #     )

# # #     points: List[PointStruct] = []
# # #     for s in schemes:
# # #         vec = scheme_embed_model.encode(_concat_item_text(s)).tolist()
# # #         payload = dict(s)
# # #         payload["__search_blob"] = _concat_item_text(s)
# # #         points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload))

# # #     scheme_qdrant.upsert(SCHEMES_COLLECTION, points)
# # #     print(f"✅ Indexed {len(points)} schemes into Qdrant (schemes collection)")


# # # # Build index at import time
# # # init_schemes_collection()


# # # def _norm(s: str) -> str:
# # #     if not s:
# # #         return ""
# # #     s = unicodedata.normalize("NFKC", s)
# # #     s = re.sub(r"\s+", " ", s).strip().lower()
# # #     return s


# # # def _qdrant_filter(
# # #     category: Optional[str],
# # #     department: Optional[str],
# # #     typ: Optional[str],
# # # ) -> Optional[Filter]:
# # #     conds = []
# # #     if category:
# # #         conds.append(FieldCondition(key="category", match=MatchText(text=category)))
# # #     if department:
# # #         conds.append(FieldCondition(key="department", match=MatchText(text=department)))
# # #     if typ:
# # #         conds.append(FieldCondition(key="type", match=MatchText(text=typ)))
# # #     if not conds:
# # #         return None
# # #     return Filter(must=conds)


# # # def _keyword_boost(question: str, item: Dict[str, Any]) -> float:
# # #     """
# # #     Simple textual boost based on name/category/department match.
# # #     Helps exact-name queries like 'atal awas yojna' hit the right scheme.
# # #     """
# # #     q = _norm(question)
# # #     name = _norm((item.get("name_hi", "") + " " + item.get("name_en", "")))
# # #     cat = _norm(item.get("category", ""))
# # #     dept = _norm(item.get("department", ""))

# # #     boost = 0.0

# # #     if q and q in name:
# # #         boost += 0.6

# # #     q_words = [w for w in q.split() if len(w) > 2]
# # #     for w in q_words:
# # #         if w in name or w in cat or w in dept:
# # #             boost += 0.15

# # #     return boost


# # # def search_schemes(
# # #     question: str,
# # #     limit: int = 3,
# # #     page: int = 1,
# # #     min_score: float = 0.20,
# # #     category: Optional[str] = None,
# # #     department: Optional[str] = None,
# # #     typ: Optional[str] = None,
# # # ):
# # #     """
# # #     Hybrid search for schemes.
# # #     Returns: (results:list[payload+_score], total:int)
# # #     """
# # #     qvec = scheme_embed_model.encode(question).tolist()
# # #     page = max(page, 1)
# # #     limit = max(1, min(20, limit))

# # #     MAX_HITS = 50

# # #     hits = scheme_qdrant.search(
# # #         collection_name=SCHEMES_COLLECTION,
# # #         query_vector=qvec,
# # #         limit=MAX_HITS,
# # #         with_payload=True,
# # #         with_vectors=False,
# # #         query_filter=_qdrant_filter(category, department, typ),
# # #     )

# # #     scored: List[Dict[str, Any]] = []
# # #     for h in hits:
# # #         base_score = float(h.score) if hasattr(h, "score") else 0.0
# # #         if base_score < min_score:
# # #             continue
# # #         p = dict(h.payload)
# # #         kw_boost = _keyword_boost(question, p)
# # #         final_score = base_score + kw_boost
# # #         p["_score"] = base_score
# # #         p["_final_score"] = final_score
# # #         scored.append(p)

# # #     # De-duplicate by scheme name
# # #     deduped: List[Dict[str, Any]] = []
# # #     seen = set()
# # #     for p in scored:
# # #         key = (p.get("name_hi") or p.get("name_en") or "").strip()
# # #         if not key:
# # #             key = p.get("id", "")
# # #         if key in seen:
# # #             continue
# # #         seen.add(key)
# # #         deduped.append(p)

# # #     deduped.sort(key=lambda x: x.get("_final_score", 0.0), reverse=True)

# # #     total = len(deduped)
# # #     start = (page - 1) * limit
# # #     end = start + limit
# # #     page_items = deduped[start:end]

# # #     return page_items, total


# # # def _fmt_scheme_card(s: Dict[str, Any]) -> str:
# # #     name = s.get("name_hi") or s.get("name_en") or "—"
# # #     bits = [
# # #         f"• **{name}**",
# # #         f"  - 🎓 पात्रता: {s.get('eligibility','उपलब्ध नहीं')}",
# # #         f"  - 💰 लाभ: {s.get('benefit','उपलब्ध नहीं')}",
# # #         f"  - 📝 आवेदन: {s.get('apply_process','उपलब्ध नहीं')}",
# # #     ]
# # #     if s.get("apply_link"):
# # #         bits.append(f"  - 🔗 लिंक: {s['apply_link']}")
# # #     return "\n".join(bits)


# # # def build_user_context(user_meta: dict | None) -> str:
# # #     """Convert user profile info into natural-language context for LLM."""
# # #     if not user_meta:
# # #         return ""

# # #     district = user_meta.get("district")
# # #     block = user_meta.get("block")
# # #     village = user_meta.get("village_code")
# # #     age = user_meta.get("age")
# # #     gender = user_meta.get("gender")
# # #     interest = user_meta.get("interest_tag")

# # #     disability = user_meta.get("disability")
# # #     occupation = user_meta.get("occupation")
# # #     income_bracket = user_meta.get("income_bracket")
# # #     social_category = user_meta.get("social_category")

# # #     parts = []

# # #     if district:
# # #         parts.append(f"जिला {district}")
# # #     if block:
# # #         parts.append(f"ब्लॉक {block}")
# # #     if village:
# # #         parts.append(f"गाँव कोड {village}")
# # #     if age:
# # #         parts.append(f"आयु {age} वर्ष")
# # #     if gender:
# # #         parts.append(f"लिंग {gender}")
# # #     if occupation:
# # #         parts.append(f"पेशा: {occupation}")
# # #     if income_bracket:
# # #         parts.append(f"आय वर्ग: {income_bracket}")
# # #     if social_category:
# # #         parts.append(f"सोशल कैटेगरी: {social_category}")
# # #     if disability and disability.lower() not in ("none", "nahin", "no"):
# # #         parts.append(f"विशेष आवश्यकताएँ / दिव्यांगता: {disability}")
# # #     if interest:
# # #         parts.append(f"रुचि: {interest}")

# # #     if not parts:
# # #         return ""

# # #     return "उपयोगकर्ता की जानकारी: " + ", ".join(parts) + ". "



# # # def build_schemes_answer(
# # #     question: str,
# # #     schemes: List[Dict[str, Any]],
# # #     user_meta: Dict[str, Any] | None = None,
# # # ) -> str:
# # #     """
# # #     Build Hindi-centric, LLM-generated answer for schemes.
# # #     Personalised slightly using user_meta (occupation, disability, etc.).
# # #     """
# # #     if not schemes:
# # #         return (
# # #             "माफ़ कीजिए, इस सवाल से मिलती-जुलती कोई योजना नहीं मिली। "
# # #             "कृपया अलग शब्दों में पूछें, या ज़िला/विभाग/श्रेणी लिखें।\n\n"
# # #             "**English:** No strong matches. Try different words or add location/department."
# # #         )

# # #     user_ctx = build_user_context(user_meta)

# # #     q_low = question.lower()
# # #     want_apply = any(w in q_low for w in [
# # #         "apply", " आवेदन", "आवेदन", "फॉर्म", "form", "कैसे", "kaise", "कहाँ", "kaha", "कहां"
# # #     ])
# # #     want_benefit = any(w in q_low for w in [
# # #         "लाभ", "benefit", "paisa", "₹", "kitna", "कितना", "राशि"
# # #     ])
# # #     want_elig = any(w in q_low for w in [
# # #         "पात्रता", "eligibility", "kaun", "कौन", "किसको", "kis ko", "kisko"
# # #     ])

# # #     if not GROQ_API_KEY:
# # #         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
# # #         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
# # #         eng = "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
# # #         return hdr + body + eng

# # #     context_lines = []
# # #     for s in schemes:
# # #         context_lines.append(
# # #             "योजना: {name}\nविवरण: {desc}\nपात्रता: {elig}\nलाभ: {ben}\nआवेदन प्रक्रिया: {proc}\nविभाग: {dept}\nश्रेणी: {cat}\nलिंक: {link}\n".format(
# # #                 name=(s.get("name_hi") or s.get("name_en") or ""),
# # #                 desc=s.get("description_hi", ""),
# # #                 elig=s.get("eligibility", ""),
# # #                 ben=s.get("benefit", ""),
# # #                 proc=s.get("apply_process", ""),
# # #                 dept=s.get("department", ""),
# # #                 cat=s.get("category", ""),
# # #                 link=s.get("apply_link", ""),
# # #             )
# # #         )
# # #     context = "\n---\n".join(context_lines)

# # #     focus_lines = []
# # #     if want_apply:
# # #         focus_lines.append(
# # #             "- User is mainly asking **how to apply**. "
# # #             "You MUST explain the पूरा 'आवेदन प्रक्रिया' field step-by-step in simple Hindi. "
# # #             "हर ज़रूरी स्टेप और हर ज़रूरी दस्तावेज़ का नाम जरूर बताएं।"
# # #         )
# # #     if want_benefit:
# # #         focus_lines.append(
# # #             "- User is asking about **benefits / amount**. "
# # #             "Explain the 'लाभ' field completely. अलग-अलग राशि हो तो सब बताएं।"
# # #         )
# # #     if want_elig:
# # #         focus_lines.append(
# # #             "- User is asking about **eligibility / who can get it**. "
# # #             "Explain the 'पात्रता' field पूरी तरह, सभी शर्तें (1, 2, 3...) अलग-अलग लिखें।"
# # #         )

# # #     focus_text = "\n".join(focus_lines) if focus_lines else "- Follow the general rules below."

# # #     # 👤 personalisation text
# # #     profile_text = user_ctx or "कोई अतिरिक्त उपयोगकर्ता जानकारी उपलब्ध नहीं है। अगर जानकारी ना हो तो generic जवाब दें।"

# # #     prompt = f"""
# # # You are **Panchayat Sahayika**, a friendly, polite and knowledgeable AI assistant created to help rural citizens of India. 
# # # Your main goal is to explain information in very **simple, clear, human-like Hindi**, so that even villagers, elderly people, 
# # # and first-time smartphone users can easily understand.

# # # User profile (for context, don't repeat fully, just use it smartly in examples):
# # # {profile_text}

# # # You must use **only** the information given in the schemes context below. 
# # # Do NOT invent or guess any benefits, eligibility rules, amounts or links that are not present.

# # # --------------------------------------------
# # # 📌 USER QUESTION:
# # # {question}

# # # 📌 RELEVANT SCHEMES (if matched):
# # # {context}
# # # --------------------------------------------

# # # ### 🔍 SPECIAL FOCUS (based on the user's question)
# # # {focus_text}

# # # ### 🟢 MAIN RULES FOR ANSWERING:
# # # - Explain in **simple conversational Hindi**, short sentences, and natural flow.  
# # # - Do NOT sound robotic. Do NOT dump raw data.  
# # # - Be clear, warm, and practical.
# # # - **Whenever you write the name of any scheme / yojana, always wrap it like this: `**PM Awas Yojana**`.  
# # #   यानी हर योजना का नाम hamesha `**` ke andar hona chahiye.**

# # # Include these only if available in provided context:
# # # - योज़ना / स्कीम का नाम  
# # # - यह किसके लिए है (पात्रता)  
# # # - कितना लाभ मिलता है (लाभ)  
# # # - कैसे और कहाँ आवेदन करना है (आवेदन प्रक्रिया)  
# # # - लिंक हो तो बताएं  

# # # If multiple schemes match, explain **2–3** clearly but naturally.
# # # Missing data → write “उपलब्ध नहीं” naturally.

# # # ### 🟡 ALWAYS END WITH:
# # # "अगर ज़रूरत हो तो अपने ग्राम पंचायत या CSC केंद्र से मदद लें।"

# # # ### 🌍 AFTER THE HINDI ANSWER:
# # # Give **one short English summary sentence** (not detailed).

# # # --------------------------------------------
# # # Now write the final answer in a natural, fluent, friendly tone.
# # # --------------------------------------------
# # # """

# # #     try:
# # #         completion = groq_client.chat.completions.create(
# # #             model=LLM_MODEL,
# # #             messages=[{"role": "user", "content": prompt}],
# # #             temperature=0.2,
# # #         )
# # #         ai_answer = completion.choices[0].message.content.strip()
# # #     except Exception:
# # #         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
# # #         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
# # #         eng = "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
# # #         return hdr + body + eng

# # #     return ai_answer


# # # def _should_use_schemes(question: str, schemes: List[Dict[str, Any]]) -> bool:
# # #     """
# # #     Decide kare ki is query ke liye schemes pipeline use karni hai ya nahi.
# # #     """
# # #     if not schemes:
# # #         return False

# # #     top = schemes[0]
# # #     top_final = float(top.get("_final_score", top.get("_score", 0.0)) or 0.0)

# # #     q = question.lower()
# # #     has_scheme_word = any(
# # #         w in q
# # #         for w in [
# # #             "योजना",
# # #             "yojana",
# # #             "scheme",
# # #             "स्कीम",
# # #             "pension",
# # #             "पेंशन",
# # #             "subsidy",
# # #             "सब्सिडी",
# # #             "बीमा",
# # #             "insurance",
# # #             "scholarship",
# # #             " छात्रवृत्ति",
# # #         ]
# # #     )

# # #     if top_final >= 0.60:
# # #         return True

# # #     if has_scheme_word and top_final >= 0.25:
# # #         return True

# # #     return False


# # # # ================== MODELS FOR JSON /ask ==================


# # # class AskRequest(BaseModel):
# # #     question: str
# # #     ui_lang: str = "hi"        # "hi" or "en"
# # #     mode: str = "auto"         # "auto" | "docs" | "schemes"
# # #     history: List[Dict[str, str]] = []
# # #     user_meta: Dict[str, Any] | None = None


# # # class AskResponse(BaseModel):
# # #     response: str
# # #     sources: List[Dict[str, Any]] = []


# # # class SchemeCard(SQLModel):
# # #     title: str
# # #     subtitle: Optional[str] = None
# # #     verified: bool = True
# # #     badges: List[str] = []
# # #     apply_url: Optional[str] = None
# # #     read_more_url: Optional[str] = None


# # # # ================== PERSONALISED RECOMMENDATIONS API ==================


# # # @app.get("/user/recommended-schemes", response_model=List[SchemeCard])
# # # def recommended_schemes(current_user: User = Depends(get_current_user)):
# # #     # Build simple query text from profile
# # #     parts = []

# # #     if current_user.district:
# # #         parts.append(current_user.district)
# # #     if current_user.block:
# # #         parts.append(current_user.block)
# # #     if current_user.gender:
# # #         parts.append(current_user.gender)
# # #     if current_user.age:
# # #         parts.append(f"age {current_user.age}")
# # #     if current_user.interest_tag:
# # #         parts.append(current_user.interest_tag)

# # #     # 🔴 NEW – these strongly influence scheme matching
# # #     if current_user.occupation:
# # #         parts.append(current_user.occupation)
# # #     if current_user.disability and current_user.disability.lower() not in ("none", "nahin", "no"):
# # #         parts.append("divyang")
# # #         parts.append(current_user.disability)
# # #     if current_user.income_bracket:
# # #         parts.append(current_user.income_bracket)
# # #     if current_user.social_category:
# # #         parts.append(current_user.social_category)

# # #     question = " ".join(parts) or "gramin yojana"

# # #     schemes, _total = search_schemes(
# # #         question=question,
# # #         limit=5,
# # #         page=1,
# # #         min_score=0.20,
# # #         category=None,
# # #         department=None,
# # #         typ=None,
# # #     )

# # #     cards: List[SchemeCard] = []
# # #     for s in schemes:
# # #         title = (
# # #             (s.get("name_hi") or "") +
# # #             (" / " + s.get("name_en", "") if s.get("name_en") else "")
# # #         ).strip(" /")
# # #         subtitle = s.get("description_hi") or s.get("description_en") or ""
# # #         badges = [s.get("department", ""), s.get("category", "")]
# # #         cards.append(
# # #             SchemeCard(
# # #                 title=title or "Yojana",
# # #                 subtitle=subtitle,
# # #                 verified=True,
# # #                 badges=[b for b in badges if b],
# # #                 apply_url=s.get("apply_link") or None,
# # #                 read_more_url=s.get("source_url") or None,
# # #             )
# # #         )
# # #     return cards

# # # # ================== ROUTES (HTML DEMO) ==================


# # # @app.get("/", response_class=HTMLResponse)
# # # async def get_home(
# # #     request: Request,
# # #     lang: str = "hi",      # ui_lang
# # #     mode: str = "docs",    # "docs" or "schemes"
# # # ):
# # #     if lang not in ("hi", "en"):
# # #         lang = "hi"
# # #     if mode not in ("docs", "schemes"):
# # #         mode = "docs"

# # #     return templates.TemplateResponse(
# # #         "index.html",
# # #         {
# # #             "request": request,
# # #             "messages": [],
# # #             "history_json": "[]",
# # #             "lang": lang,
# # #             "mode": mode,
# # #         },
# # #     )


# # # @app.post("/", response_class=HTMLResponse)
# # # async def post_query(
# # #     request: Request,
# # #     query: str = Form(...),
# # #     history_json: str = Form("[]"),
# # #     ui_lang: str = Form("hi"),   # "hi" or "en"
# # #     mode: str = Form("docs"),    # "docs" or "schemes"
# # # ):
# # #     try:
# # #         history = json.loads(history_json)
# # #     except Exception:
# # #         history = []

# # #     if ui_lang == "en":
# # #         target_lang = "en"
# # #     else:
# # #         target_lang = "hi" if contains_devanagari(query) else "hinglish"

# # #     if mode == "schemes":
# # #         schemes, _total = search_schemes(
# # #             question=query,
# # #             limit=3,
# # #             page=1,
# # #             min_score=0.20,
# # #             category=None,
# # #             department=None,
# # #             typ=None,
# # #         )
# # #         base_answer = build_schemes_answer(query, schemes)
# # #     else:
# # #         base_answer, _sources = generate_docs_answer_raw(query, history)

# # #     final_text = translate_answer(base_answer, target_lang)
# # #     answer_html = _convert_markdown_bold_to_html(final_text)

# # #     history.append({"role": "user", "content": query})
# # #     history.append({"role": "assistant", "content": answer_html})

# # #     messages = [{"role": h["role"], "content": h["content"]} for h in history]

# # #     return templates.TemplateResponse(
# # #         "index.html",
# # #         {
# # #             "request": request,
# # #             "messages": messages,
# # #             "history_json": json.dumps(history, ensure_ascii=False),
# # #             "lang": ui_lang,
# # #             "mode": mode,
# # #         },
# # #     )


# # # # ================== JSON API FOR REACT CHAT ==================


# # # @app.post("/ask", response_model=AskResponse)
# # # def ask(req: AskRequest):
# # #     """
# # #     Used by React ChatScreen.
# # #     - Decides schemes vs docs (or forced by req.mode)
# # #     - Applies translation for UI lang
# # #     - Uses user_meta for slight personalisation
# # #     - Returns { response, sources } that your ChatScreen understands
# # #     """

# # #     # Decide final language
# # #     if req.ui_lang == "en":
# # #         target_lang = "en"
# # #     else:
# # #         target_lang = "hi" if contains_devanagari(req.question) else "hinglish"

# # #     # 👤 user profile from frontend
# # #     user_meta = req.user_meta or None

# # #     schemes: List[Dict[str, Any]] = []
# # #     doc_sources: List[Dict[str, Any]] = []
# # #     use_schemes = False

# # #     if req.mode in ("schemes", "auto"):
# # #         schemes, total = search_schemes(
# # #             question=req.question,
# # #             limit=5,
# # #             page=1,
# # #             min_score=0.20,
# # #             category=None,
# # #             department=None,
# # #             typ=None,
# # #         )
# # #         if req.mode == "schemes":
# # #             use_schemes = True
# # #         else:
# # #             use_schemes = _should_use_schemes(req.question, schemes)

# # #     if use_schemes:
# # #         base_answer = build_schemes_answer(req.question, schemes, user_meta=user_meta)
# # #         sources = [
# # #             {
# # #                 "name_hi": s.get("name_hi"),
# # #                 "name_en": s.get("name_en"),
# # #                 "score": s.get("_score"),
# # #                 "department": s.get("department"),
# # #                 "category": s.get("category"),
# # #                 "apply_link": s.get("apply_link"),
# # #             }
# # #             for s in schemes
# # #         ]
# # #     else:
# # #         base_answer, doc_sources = generate_docs_answer_raw(
# # #             req.question,
# # #             req.history,
# # #             user_meta=user_meta,
# # #         )
# # #         sources = doc_sources

# # #     final_text = translate_answer(base_answer, target_lang)
# # #     final_html = _convert_markdown_bold_to_html(final_text)

# # #     return AskResponse(response=final_html, sources=sources)


# # # # ================== AUTH ROUTES ==================


# # # @app.post("/auth/register", response_model=UserRead)
# # # def register(user_in: UserCreate, session: Session = Depends(get_session)):
# # #     existing = get_user_by_username(session, user_in.username)
# # #     if existing:
# # #         raise HTTPException(status_code=400, detail="Username already registered")

# # #     user = User(
# # #         username=user_in.username,
# # #         full_name=user_in.full_name,
# # #         hashed_password=get_password_hash(user_in.password),
# # #         district=user_in.district,
# # #         block=user_in.block,
# # #         village_code=user_in.village_code,
# # #         age=user_in.age,
# # #         gender=user_in.gender,
# # #         interest_tag=user_in.interest_tag,

# # #         disability=user_in.disability,
# # #         occupation=user_in.occupation,
# # #         income_bracket=user_in.income_bracket,
# # #         social_category=user_in.social_category,
# # #     )
# # #     session.add(user)
# # #     session.commit()
# # #     session.refresh(user)
# # #     return user


# # # @app.post("/auth/login", response_model=Token)
# # # def login(
# # #     form_data: OAuth2PasswordRequestForm = Depends(),
# # #     session: Session = Depends(get_session),
# # # ):
# # #     user = get_user_by_username(session, form_data.username)
# # #     if not user or not verify_password(form_data.password, user.hashed_password):
# # #         raise HTTPException(status_code=400, detail="Incorrect username or password")

# # #     token = create_access_token({"sub": user.username})
# # #     return Token(access_token=token)


# # # @app.get("/me", response_model=UserRead)
# # # def read_me(current_user: User = Depends(get_current_user)):
# # #     return current_user


# # # @app.get("/health")
# # # def health():
# # #     return {
# # #         "status": "ok",
# # #         "docs_collection": DOC_COLLECTION,
# # #         "schemes_collection": SCHEMES_COLLECTION,
# # #         "embed_model_schemes": EMBED_MODEL_NAME_SCHEMES,
# # #     }
    
    
# # # @app.put("/me", response_model=UserRead)
# # # def update_me(
# # #     user_update: UserUpdate,
# # #     current_user: User = Depends(get_current_user),
# # #     session: Session = Depends(get_session),
# # # ):
# # #     data = user_update.dict(exclude_unset=True)

# # #     for field, value in data.items():
# # #         setattr(current_user, field, value)

# # #     session.add(current_user)
# # #     session.commit()
# # #     session.refresh(current_user)
# # #     return current_user

# # import os
# # import json
# # import uuid
# # import re
# # import unicodedata
# # from pathlib import Path
# # from typing import List, Dict, Any, Optional, Tuple

# # from dotenv import load_dotenv
# # from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse
# # from fastapi.templating import Jinja2Templates

# # from pydantic import BaseModel

# # from qdrant_client import QdrantClient
# # from qdrant_client.models import (
# #     VectorParams,
# #     Distance,
# #     PointStruct,
# #     Filter,
# #     FieldCondition,
# #     MatchText,
# # )
# # from qdrant_client.http import models as qm  # noqa: F401  (kept if later needed)

# # from sentence_transformers import SentenceTransformer
# # from fastembed import TextEmbedding
# # from groq import Groq
# # from googletrans import Translator  # Google Translate

# # from sqlmodel import Field, SQLModel, Session, create_engine, select
# # from passlib.context import CryptContext
# # from jose import JWTError, jwt
# # from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# # # ================== CONFIG ==================

# # BASE_DIR = Path(__file__).resolve().parent.parent  # repo root (panchayat-sahayika)

# # # Schemes JSON path
# # SCHEMES_PATH = BASE_DIR / "samaj_kalyan_vibhag_clean_typed.json"
# # # or, if in public:
# # # SCHEMES_PATH = BASE_DIR / "public" / "samaj_kalyan_vibhag_clean_typed.json"

# # load_dotenv()

# # # ---- Groq / LLM ----
# # GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# # if not GROQ_API_KEY:
# #     raise RuntimeError("GROQ_API_KEY missing in .env")

# # LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
# # GROQ_MODEL_DOCS = os.getenv("GROQ_MODEL", LLM_MODEL)

# # groq_client = Groq(api_key=GROQ_API_KEY)

# # # ---- DOCS RAG Qdrant (remote or local) ----
# # DOC_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# # DOC_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
# # DOC_COLLECTION = os.getenv("COLLECTION_NAME", "panchayat_uk_docs")

# # doc_qclient = QdrantClient(url=DOC_QDRANT_URL, api_key=DOC_QDRANT_API_KEY)
# # doc_embedder = TextEmbedding()

# # # ---- Schemes Qdrant (local embedded) ----
# # EMBED_MODEL_NAME_SCHEMES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# # SCHEMES_COLLECTION = "samaj_kalyan_vibhag_schemes"

# # scheme_embed_model = SentenceTransformer(EMBED_MODEL_NAME_SCHEMES)
# # scheme_qdrant = QdrantClient(path=str(BASE_DIR / "qdrant_data"))

# # origins = [
# #     "http://localhost:5173",
# #     "http://127.0.0.1:5173",
# # ]

# # # ---- FastAPI + Templates ----
# # app = FastAPI(title="Panchayat Sahayika Unified Backend")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
# #     allow_headers=["*"],
# # )

# # templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# # translator = Translator()  # Google translator instance

# # # ================== AUTH / USERS ==================

# # DATABASE_URL = "sqlite:///./panchayat_users.db"  # SQLite file in backend folder
# # engine = create_engine(DATABASE_URL, echo=False)

# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # SECRET_KEY = os.getenv(
# #     "SECRET_KEY",
# #     "baea29ce56f4b02733883b6ae1a76265988d123d5ad3e9d2214dae4646a81ee6",
# # )
# # ALGORITHM = "HS256"
# # ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# # class User(SQLModel, table=True):
# #     id: Optional[int] = Field(default=None, primary_key=True)
# #     username: str = Field(index=True, unique=True)
# #     full_name: Optional[str] = None
# #     hashed_password: str

# #     # profile info (for recommendations / chatbot)
# #     district: Optional[str] = None
# #     block: Optional[str] = None
# #     village_code: Optional[str] = None
# #     age: Optional[int] = None
# #     gender: Optional[str] = None          # "M"/"F"/"O" or free text
# #     interest_tag: Optional[str] = None    # "farmer", "student", etc.

# #     disability: Optional[str] = None      # e.g. "none", "locomotor", "visual", etc.
# #     occupation: Optional[str] = None      # "farmer", "student", "ASHA", "SHG member"...
# #     income_bracket: Optional[str] = None  # "BPL", "APL", etc.
# #     social_category: Optional[str] = None # "SC", "ST", "OBC", "General", etc.


# # class UserCreate(SQLModel):
# #     username: str
# #     password: str
# #     full_name: Optional[str] = None
# #     district: Optional[str] = None
# #     block: Optional[str] = None
# #     village_code: Optional[str] = None
# #     age: Optional[int] = None
# #     gender: Optional[str] = None
# #     interest_tag: Optional[str] = None

# #     disability: Optional[str] = None
# #     occupation: Optional[str] = None
# #     income_bracket: Optional[str] = None
# #     social_category: Optional[str] = None


# # class UserRead(SQLModel):
# #     id: int
# #     username: str
# #     full_name: Optional[str] = None
# #     district: Optional[str] = None
# #     block: Optional[str] = None
# #     village_code: Optional[str] = None
# #     age: Optional[int] = None
# #     gender: Optional[str] = None
# #     interest_tag: Optional[str] = None

# #     disability: Optional[str] = None
# #     occupation: Optional[str] = None
# #     income_bracket: Optional[str] = None
# #     social_category: Optional[str] = None


# # class UserUpdate(SQLModel):
# #     full_name: Optional[str] = None
# #     district: Optional[str] = None
# #     block: Optional[str] = None
# #     village_code: Optional[str] = None
# #     age: Optional[int] = None
# #     gender: Optional[str] = None
# #     interest_tag: Optional[str] = None

# #     disability: Optional[str] = None
# #     occupation: Optional[str] = None
# #     income_bracket: Optional[str] = None
# #     social_category: Optional[str] = None


# # class Token(SQLModel):
# #     access_token: str
# #     token_type: str = "bearer"


# # def create_db_and_tables():
# #     SQLModel.metadata.create_all(engine)


# # def get_session():
# #     with Session(engine) as session:
# #         yield session


# # def _bcrypt_safe(password: str) -> str:
# #     """
# #     Bcrypt only uses first 72 bytes of the password.
# #     To avoid errors, we explicitly cut to 72 bytes.
# #     """
# #     if password is None:
# #         return ""
# #     pw_bytes = password.encode("utf-8")
# #     return pw_bytes[:72].decode("utf-8", errors="ignore")


# # def get_password_hash(password: str) -> str:
# #     safe_pw = _bcrypt_safe(password)
# #     return pwd_context.hash(safe_pw)


# # def verify_password(plain: str, hashed: str) -> bool:
# #     safe_pw = _bcrypt_safe(plain)
# #     return pwd_context.verify(safe_pw, hashed)


# # def create_access_token(data: dict) -> str:
# #     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# # def get_user_by_username(session: Session, username: str) -> Optional[User]:
# #     stmt = select(User).where(User.username == username)
# #     return session.exec(stmt).first()


# # async def get_current_user(
# #     token: str = Depends(oauth2_scheme),
# #     session: Session = Depends(get_session),
# # ) -> User:
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         username: Optional[str] = payload.get("sub")
# #         if username is None:
# #             raise credentials_exception
# #     except JWTError:
# #         raise credentials_exception

# #     user = get_user_by_username(session, username=username)
# #     if not user:
# #         raise credentials_exception
# #     return user


# # @app.on_event("startup")
# # def on_startup():
# #     create_db_and_tables()

# # # ================== COMMON LANGUAGE HELPERS ==================


# # def contains_devanagari(text: str) -> bool:
# #     """Check if text has any Devanagari characters."""
# #     for ch in text:
# #         if "\u0900" <= ch <= "\u097F":
# #             return True
# #     return False


# # def _llm_translate(text: str, target_desc: str) -> str:
# #     """
# #     Generic translator using Groq LLM.
# #     `target_desc` = description of target language/style.
# #     """
# #     system_msg = (
# #         "You are a translator for Gram Panchayat content.\n"
# #         "You ONLY translate the text; you do not add explanations.\n"
# #         "Preserve markdown bold markers **like this** exactly as they are.\n"
# #         "Do not change the meaning; only change the language.\n"
# #     )

# #     user_msg = (
# #         f"Translate the following text into {target_desc}\n\n"
# #         f"Text:\n{text}"
# #     )

# #     completion = groq_client.chat.completions.create(
# #         model=LLM_MODEL,
# #         messages=[
# #             {"role": "system", "content": system_msg},
# #             {"role": "user", "content": user_msg},
# #         ],
# #         temperature=0.2,
# #         max_tokens=1200,
# #     )
# #     out = completion.choices[0].message.content or text
# #     return out


# # def translate_answer(text: str, target_lang: str) -> str:
# #     """
# #     Final step translation:

# #     target_lang:
# #       - 'en'        -> English
# #       - 'hi'        -> simple Hindi (Devanagari)
# #       - 'garhwali'  -> simple Garhwali (Devanagari)
# #       - 'hinglish'  -> simple Hinglish (Roman Hindi)
# #     """

# #     # ---------- 1) English UI ----------
# #     if target_lang == "en":
# #         try:
# #             res = translator.translate(text, dest="en")
# #             out = res.text
# #             if out and not contains_devanagari(out) and out.strip() != "":
# #                 return out
# #         except Exception:
# #             pass

# #         return _llm_translate(
# #             text,
# #             "clear, simple English suitable for village-level users. "
# #             "Avoid Hindi script and use plain English sentences."
# #         )

# #     # ---------- 2) Hindi (Devanagari) ----------
# #     if target_lang == "hi":
# #         return _llm_translate(
# #             text,
# #             "very simple Hindi in Devanagari script, using everyday words "
# #             "that village-level users understand."
# #         )

# #     # ---------- 3) Garhwali (Devanagari) ----------
# #         # ---------- 3) Garhwali (Devanagari) ----------
# #     # ---------- 3) Garhwali (Devanagari) ----------
# #     if target_lang == "garhwali":
# #         return _llm_translate(
# #             text,
# #             (
# #                 "Translate into PURE Garhwali language (Central Garhwal dialect), "
# #                 "written in Devanagari script.\n\n"
# #                 "STRICT RULES:\n"
# #                 "- Every sentence MUST be in natural Garhwali, NOT Hindi.\n"
# #                 "- Avoid Hindi forms: 'मैं', 'आप', 'कैसे', 'करना', 'है', 'हैं', 'होगा', etc.\n"
# #                 "- Use Garhwali forms: 'मैं', 'त्यूँ', 'कसि', 'च', 'क्या', 'लागदा', 'भैजी', "
# #                 "'जा', 'रै', 'ल्यो', 'णै', 'चुव', 'छूँ', 'छ', 'च' etc.\n"
# #                 "- Make sentences exactly like villagers speak at home.\n"
# #                 "- EXAMPLES:\n"
# #                 "  Hindi: 'आप कैसे हैं?' → Garhwali: 'त्यूँ कसि च?' \n"
# #                 "  Hindi: 'मैं तुम्हारी मदद करूँगा।' → 'मैं तैरी मदद करैल।'\n"
# #                 "  Hindi: 'यह प्रक्रिया ऐसे होती है।' → 'ई प्रक्रिया ऐसि ह्वै।'\n"
# #                 "- DO NOT use Hindi connectors like: 'क्योंकि', 'लेकिन', 'इसके अलावा'.\n"
# #                 "- Use Garhwali connectors: 'कां', 'न', 'भल', 'ति', 'तिल', 'कि', 'जा'.\n"
# #                 "- Keep government scheme names exactly in Hindi.\n"
# #                 "- If any Hindi-style word is unavoidable, convert it into Garhwali tone.\n"
# #             )
# #         )



# #     # ---------- 4) Hinglish (Roman Hindi) ----------
# #     return _llm_translate(
# #         text,
# #         "very simple Hinglish (Roman Hindi using English letters). "
# #         "Do NOT use Devanagari characters."
# #     )


# # def _convert_markdown_bold_to_html(text: str) -> str:
# #     """**bold** -> <strong>bold</strong> for UI."""
# #     return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


# # # ================== DOCS RAG PIPELINE ==================


# # def build_docs_system_prompt() -> str:
# #     """
# #     System prompt for docs:
# #     - Sirf Qdrant se aaye context ka use karo
# #     - Gram Panchayat users ke liye simple Hindi
# #     - Users can ask in Hindi, Hinglish, or Garhwali; you can first think in Hindi.
# #     """
# #     return (
# #         "आप 'Panchayat Sahayika' हैं, उत्तराखंड की ग्राम पंचायतों के लिए सहायक。\n"
# #         "यूज़र कभी-कभी गढ़वाली या हिंग्लिश में भी सवाल पूछ सकते हैं; "
# #         "आप अर्थ समझकर पहले सरल हिन्दी में जवाब तैयार करें。\n"
# #         "आपको केवल नीचे दिए गए संदर्भ (official Panchayati Raj documents: acts, rules, guidelines, roles, schemes, training material)\n"
# #         "का इस्तेमाल करके ही जवाब देना है。\n\n"
# #         "भाषा बहुत ही सरल और आसान हिन्दी होनी चाहिए ताकि सरपंच, वार्ड मेंबर और ग्राम पंचायत कर्मचारी आसानी से समझ सकें。\n"
# #         "कानूनी भारी शब्दों से बचें。\n"
# #         "अगर ज़रूरी जानकारी संदर्भ में नहीं है, तो साफ-साफ लिखें कि यह जानकारी उपलब्ध नहीं है और आप अंदाज़ा नहीं लगा रहे हैं。\n"
# #         "कभी भी दस्तावेज़ का नाम, फाइल का नाम, पेज नंबर या 'source' list का ज़िक्र न करें。\n"
# #     )


# # def retrieve_docs_context(query: str, top_k: int = 8) -> List[Dict[str, Any]]:
# #     query_vec = list(doc_embedder.embed([query]))[0]
# #     results = doc_qclient.search(
# #         collection_name=DOC_COLLECTION,
# #         query_vector=query_vec,
# #         limit=top_k,
# #         with_payload=True,
# #     )

# #     contexts = []
# #     for r in results:
# #         pl = r.payload or {}
# #         contexts.append(
# #             {
# #                 "text": pl.get("text", ""),
# #                 "source_file": pl.get("source_file", ""),
# #                 "page": pl.get("page", ""),
# #                 "url": pl.get("url", ""),
# #                 "score": r.score,
# #             }
# #         )
# #     return contexts


# # def generate_docs_answer_raw(
# #     query: str,
# #     history: List[Dict[str, str]],
# #     user_meta: Dict[str, Any] | None = None,
# # ) -> Tuple[str, List[Dict[str, Any]]]:
# #     """
# #     Returns raw answer in Hindi-ish language (LLM decides, but system prompt nudges to Hindi).
# #     We will later translate to final UI language using translate_answer().
# #     """
# #     contexts = retrieve_docs_context(query)

# #     context_block = "\n\n---\n\n".join(
# #         c["text"] for c in contexts if c["text"]
# #     )

# #     # 👤 personalise a bit
# #     user_ctx = build_user_context(user_meta)

# #     system_prompt = build_docs_system_prompt()
# #     if user_ctx:
# #         system_prompt += (
# #             "\n\nउपयोगकर्ता प्रोफाइल (उदाहरणों को practical banane ke liye):\n"
# #             f"{user_ctx}\n"
# #             "जवाब में आप user ki स्थिति ke हिसाब से छोटा सा context de sakte hain "
# #             "(jaise किसान, छात्र, दिव्यांग इत्यादि)."
# #         )

# #     messages = [
# #         {"role": "system", "content": system_prompt},
# #     ]

# #     # include a few last turns from history (server-side only)
# #     for h in history[-4:] if history else []:
# #         messages.append({"role": h["role"], "content": h["content"]})

# #     messages.append(
# #         {
# #             "role": "user",
# #             "content": (
# #                 f"प्रश्न: {query}\n\n"
# #                 f"नीचे दिए गए दस्तावेज़ों के संदर्भ का उपयोग करके उत्तर दीजिए। "
# #                 f"अपने उत्तर में इन दस्तावेज़ों के नाम या पेज नंबर का ज़िक्र मत कीजिए:\n\n"
# #                 f"{context_block}"
# #             ),
# #         }
# #     )

# #     completion = groq_client.chat.completions.create(
# #         model=GROQ_MODEL_DOCS,
# #         messages=messages,
# #         temperature=0.3,
# #         max_tokens=900,
# #     )
# #     raw_answer = completion.choices[0].message.content or ""

# #     # dedupe sources
# #     unique_sources = []
# #     seen = set()
# #     for c in contexts:
# #         key = (c["source_file"], c["page"])
# #         if key not in seen and c["source_file"]:
# #             seen.add(key)
# #             unique_sources.append(
# #                 {
# #                     "source_file": c["source_file"],
# #                     "page": c["page"],
# #                     "url": c["url"],
# #                 }
# #             )

# #     return raw_answer, unique_sources


# # # ================== SCHEMES PIPELINE ==================


# # def load_schemes() -> List[Dict[str, Any]]:
# #     with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
# #         data = json.load(f)
# #     # ensure strings and minimal keys exist
# #     for s in data:
# #         s.setdefault("name_hi", "")
# #         s.setdefault("name_en", "")
# #         s.setdefault("category", "")
# #         s.setdefault("department", "")
# #         s.setdefault("description_hi", "")
# #         s.setdefault("description_en", "")
# #         s.setdefault("eligibility", "")
# #         s.setdefault("benefit", "")
# #         s.setdefault("apply_process", "")
# #         s.setdefault("apply_link", "")
# #         s.setdefault("source_url", "")
# #         s.setdefault("type", s.get("type", "scheme"))
# #     return data


# # def _concat_item_text(s: Dict[str, Any]) -> str:
# #     """
# #     Text used for vector embedding.
# #     We heavily weight the scheme name so that exact-name queries hit correctly.
# #     """
# #     name = (s.get("name_hi", "") + " " + s.get("name_en", "")).strip()
# #     other_parts = [
# #         s.get("category", ""),
# #         s.get("department", ""),
# #         s.get("description_hi", ""),
# #         s.get("description_en", ""),
# #         s.get("eligibility", ""),
# #         s.get("benefit", ""),
# #         s.get("apply_process", ""),
# #     ]

# #     # Repeat name 5x → boosts similarity when user types scheme name
# #     weighted_name = " ".join([name] * 5) if name else ""
# #     rest = " | ".join([str(p) for p in other_parts if p])

# #     return " | ".join([p for p in [weighted_name, rest] if p])


# # def init_schemes_collection():
# #     schemes = load_schemes()

# #     scheme_qdrant.recreate_collection(
# #         collection_name=SCHEMES_COLLECTION,
# #         vectors_config=VectorParams(
# #             size=scheme_embed_model.get_sentence_embedding_dimension(),
# #             distance=Distance.COSINE,
# #         ),
# #     )

# #     points: List[PointStruct] = []
# #     for s in schemes:
# #         vec = scheme_embed_model.encode(_concat_item_text(s)).tolist()
# #         payload = dict(s)
# #         payload["__search_blob"] = _concat_item_text(s)
# #         points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload))

# #     scheme_qdrant.upsert(SCHEMES_COLLECTION, points)
# #     print(f"✅ Indexed {len(points)} schemes into Qdrant (schemes collection)")


# # # Build index at import time
# # init_schemes_collection()


# # def _norm(s: str) -> str:
# #     if not s:
# #         return ""
# #     s = unicodedata.normalize("NFKC", s)
# #     s = re.sub(r"\s+", " ", s).strip().lower()
# #     return s


# # def _qdrant_filter(
# #     category: Optional[str],
# #     department: Optional[str],
# #     typ: Optional[str],
# # ) -> Optional[Filter]:
# #     conds = []
# #     if category:
# #         conds.append(FieldCondition(key="category", match=MatchText(text=category)))
# #     if department:
# #         conds.append(FieldCondition(key="department", match=MatchText(text=department)))
# #     if typ:
# #         conds.append(FieldCondition(key="type", match=MatchText(text=typ)))
# #     if not conds:
# #         return None
# #     return Filter(must=conds)


# # def _keyword_boost(question: str, item: Dict[str, Any]) -> float:
# #     """
# #     Simple textual boost based on name/category/department match.
# #     Helps exact-name queries like 'atal awas yojna' hit the right scheme.
# #     """
# #     q = _norm(question)
# #     name = _norm((item.get("name_hi", "") + " " + item.get("name_en", "")))
# #     cat = _norm(item.get("category", ""))
# #     dept = _norm(item.get("department", ""))

# #     boost = 0.0

# #     if q and q in name:
# #         boost += 0.6

# #     q_words = [w for w in q.split() if len(w) > 2]
# #     for w in q_words:
# #         if w in name or w in cat or w in dept:
# #             boost += 0.15

# #     return boost


# # def search_schemes(
# #     question: str,
# #     limit: int = 3,
# #     page: int = 1,
# #     min_score: float = 0.20,
# #     category: Optional[str] = None,
# #     department: Optional[str] = None,
# #     typ: Optional[str] = None,
# # ):
# #     """
# #     Hybrid search for schemes.
# #     Returns: (results:list[payload+_score], total:int)
# #     """
# #     qvec = scheme_embed_model.encode(question).tolist()
# #     page = max(page, 1)
# #     limit = max(1, min(20, limit))

# #     MAX_HITS = 50

# #     hits = scheme_qdrant.search(
# #         collection_name=SCHEMES_COLLECTION,
# #         query_vector=qvec,
# #         limit=MAX_HITS,
# #         with_payload=True,
# #         with_vectors=False,
# #         query_filter=_qdrant_filter(category, department, typ),
# #     )

# #     scored: List[Dict[str, Any]] = []
# #     for h in hits:
# #         base_score = float(h.score) if hasattr(h, "score") else 0.0
# #         if base_score < min_score:
# #             continue
# #         p = dict(h.payload)
# #         kw_boost = _keyword_boost(question, p)
# #         final_score = base_score + kw_boost
# #         p["_score"] = base_score
# #         p["_final_score"] = final_score
# #         scored.append(p)

# #     # De-duplicate by scheme name
# #     deduped: List[Dict[str, Any]] = []
# #     seen = set()
# #     for p in scored:
# #         key = (p.get("name_hi") or p.get("name_en") or "").strip()
# #         if not key:
# #             key = p.get("id", "")
# #         if key in seen:
# #             continue
# #         seen.add(key)
# #         deduped.append(p)

# #     deduped.sort(key=lambda x: x.get("_final_score", 0.0), reverse=True)

# #     total = len(deduped)
# #     start = (page - 1) * limit
# #     end = start + limit
# #     page_items = deduped[start:end]

# #     return page_items, total


# # def _fmt_scheme_card(s: Dict[str, Any]) -> str:
# #     name = s.get("name_hi") or s.get("name_en") or "—"
# #     bits = [
# #         f"• **{name}**",
# #         f"  - 🎓 पात्रता: {s.get('eligibility','उपलब्ध नहीं')}",
# #         f"  - 💰 लाभ: {s.get('benefit','उपलब्ध नहीं')}",
# #         f"  - 📝 आवेदन: {s.get('apply_process','उपलब्ध नहीं')}",
# #     ]
# #     if s.get("apply_link"):
# #         bits.append(f"  - 🔗 लिंक: {s['apply_link']}")
# #     return "\n".join(bits)


# # def build_user_context(user_meta: dict | None) -> str:
# #     """Convert user profile info into natural-language context for LLM."""
# #     if not user_meta:
# #         return ""

# #     district = user_meta.get("district")
# #     block = user_meta.get("block")
# #     village = user_meta.get("village_code")
# #     age = user_meta.get("age")
# #     gender = user_meta.get("gender")
# #     interest = user_meta.get("interest_tag")

# #     disability = user_meta.get("disability")
# #     occupation = user_meta.get("occupation")
# #     income_bracket = user_meta.get("income_bracket")
# #     social_category = user_meta.get("social_category")

# #     parts = []

# #     if district:
# #         parts.append(f"जिला {district}")
# #     if block:
# #         parts.append(f"ब्लॉक {block}")
# #     if village:
# #         parts.append(f"गाँव कोड {village}")
# #     if age:
# #         parts.append(f"आयु {age} वर्ष")
# #     if gender:
# #         parts.append(f"लिंग {gender}")
# #     if occupation:
# #         parts.append(f"पेशा: {occupation}")
# #     if income_bracket:
# #         parts.append(f"आय वर्ग: {income_bracket}")
# #     if social_category:
# #         parts.append(f"सोशल कैटेगरी: {social_category}")
# #     if disability and disability.lower() not in ("none", "nahin", "no"):
# #         parts.append(f"विशेष आवश्यकताएँ / दिव्यांगता: {disability}")
# #     if interest:
# #         parts.append(f"रुचि: {interest}")

# #     if not parts:
# #         return ""

# #     return "उपयोगकर्ता की जानकारी: " + ", ".join(parts) + ". "


# # def build_schemes_answer(
# #     question: str,
# #     schemes: List[Dict[str, Any]],
# #     user_meta: Dict[str, Any] | None = None,
# # ) -> str:
# #     """
# #     Build Hindi-centric, LLM-generated answer for schemes.
# #     Personalised slightly using user_meta (occupation, disability, etc.).
# #     """
# #     if not schemes:
# #         return (
# #             "माफ़ कीजिए, इस सवाल से मिलती-जुलती कोई योजना नहीं मिली। "
# #             "कृपया अलग शब्दों में पूछें, या ज़िला/विभाग/श्रेणी लिखें。\n\n"
# #             "**English:** No strong matches. Try different words or add location/department."
# #         )

# #     user_ctx = build_user_context(user_meta)

# #     q_low = question.lower()
# #     want_apply = any(
# #         w in q_low
# #         for w in [
# #             "apply",
# #             " आवेदन",
# #             "आवेदन",
# #             "फॉर्म",
# #             "form",
# #             "कैसे",
# #             "kaise",
# #             "कहाँ",
# #             "kaha",
# #             "कहां",
# #         ]
# #     )
# #     want_benefit = any(
# #         w in q_low
# #         for w in [
# #             "लाभ",
# #             "benefit",
# #             "paisa",
# #             "₹",
# #             "kitna",
# #             "कितना",
# #             "राशि",
# #         ]
# #     )
# #     want_elig = any(
# #         w in q_low
# #         for w in [
# #             "पात्रता",
# #             "eligibility",
# #             "kaun",
# #             "कौन",
# #             "किसको",
# #             "kis ko",
# #             "kisko",
# #         ]
# #     )

# #     if not GROQ_API_KEY:
# #         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
# #         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
# #         eng = (
# #             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
# #         )
# #         return hdr + body + eng

# #     context_lines = []
# #     for s in schemes:
# #         context_lines.append(
# #             "योजना: {name}\nविवरण: {desc}\nपात्रता: {elig}\nलाभ: {ben}\nआवेदन प्रक्रिया: {proc}\nविभाग: {dept}\nश्रेणी: {cat}\nलिंक: {link}\n".format(
# #                 name=(s.get("name_hi") or s.get("name_en") or ""),
# #                 desc=s.get("description_hi", ""),
# #                 elig=s.get("eligibility", ""),
# #                 ben=s.get("benefit", ""),
# #                 proc=s.get("apply_process", ""),
# #                 dept=s.get("department", ""),
# #                 cat=s.get("category", ""),
# #                 link=s.get("apply_link", ""),
# #             )
# #         )
# #     context = "\n---\n".join(context_lines)

# #     focus_lines = []
# #     if want_apply:
# #         focus_lines.append(
# #             "- User is mainly asking **how to apply**. "
# #             "You MUST explain the पूरा 'आवेदन प्रक्रिया' field step-by-step in simple Hindi. "
# #             "हर ज़रूरी स्टेप और हर ज़रूरी दस्तावेज़ का नाम जरूर बताएं।"
# #         )
# #     if want_benefit:
# #         focus_lines.append(
# #             "- User is asking about **benefits / amount**. "
# #             "Explain the 'लाभ' field completely. अलग-अलग राशि हो तो सब बताएं।"
# #         )
# #     if want_elig:
# #         focus_lines.append(
# #             "- User is asking about **eligibility / who can get it**. "
# #             "Explain the 'पात्रता' field पूरी तरह, सभी शर्तें (1, 2, 3...) अलग-अलग लिखें।"
# #         )

# #     focus_text = "\n".join(focus_lines) if focus_lines else "- Follow the general rules below."

# #     # 👤 personalisation text
# #     profile_text = user_ctx or "कोई अतिरिक्त उपयोगकर्ता जानकारी उपलब्ध नहीं है। अगर जानकारी ना हो तो generic जवाब दें।"

# #     prompt = f"""
# # You are **Panchayat Sahayika**, a friendly, polite and knowledgeable AI assistant created to help rural citizens of India. 
# # Your main goal is to explain information in very **simple, clear, human-like Hindi**, so that even villagers, elderly people, 
# # and first-time smartphone users can easily understand.

# # User profile (for context, don't repeat fully, just use it smartly in examples):
# # {profile_text}

# # You must use **only** the information given in the schemes context below. 
# # Do NOT invent or guess any benefits, eligibility rules, amounts or links that are not present.

# # --------------------------------------------
# # 📌 USER QUESTION:
# # {question}

# # 📌 RELEVANT SCHEMES (if matched):
# # {context}
# # --------------------------------------------

# # ### 🔍 SPECIAL FOCUS (based on the user's question)
# # {focus_text}

# # ### 🟢 MAIN RULES FOR ANSWERING:
# # - Explain in **simple conversational Hindi**, short sentences, and natural flow.  
# # - Do NOT sound robotic. Do NOT dump raw data.  
# # - Be clear, warm, and practical.
# # - **Whenever you write the name of any scheme / yojana, always wrap it like this: `**PM Awas Yojana**`.  
# #   यानी हर योजना का नाम hamesha `**` ke andar hona chahiye.**

# # Include these only if available in provided context:
# # - योज़ना / स्कीम का नाम  
# # - यह किसके लिए है (पात्रता)  
# # - कितना लाभ मिलता है (लाभ)  
# # - कैसे और कहाँ आवेदन करना है (आवेदन प्रक्रिया)  
# # - लिंक हो तो बताएं  

# # If multiple schemes match, explain **2–3** clearly but naturally.
# # Missing data → write “उपलब्ध नहीं” naturally.

# # ### 🟡 ALWAYS END WITH:
# # "अगर ज़रूरत हो तो अपने ग्राम पंचायत या CSC केंद्र से मदद लें।"

# # ### 🌍 AFTER THE HINDI ANSWER:
# # Give **one short English summary sentence** (not detailed).

# # --------------------------------------------
# # Now write the final answer in a natural, fluent, friendly tone.
# # --------------------------------------------
# # """

# #     try:
# #         completion = groq_client.chat.completions.create(
# #             model=LLM_MODEL,
# #             messages=[{"role": "user", "content": prompt}],
# #             temperature=0.2,
# #         )
# #         ai_answer = completion.choices[0].message.content.strip()
# #     except Exception:
# #         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
# #         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
# #         eng = (
# #             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
# #         )
# #         return hdr + body + eng

# #     return ai_answer


# # def _should_use_schemes(question: str, schemes: List[Dict[str, Any]]) -> bool:
# #     """
# #     Decide kare ki is query ke liye schemes pipeline use karni hai ya nahi।
# #     """
# #     if not schemes:
# #         return False

# #     top = schemes[0]
# #     top_final = float(top.get("_final_score", top.get("_score", 0.0)) or 0.0)

# #     q = question.lower()
# #     has_scheme_word = any(
# #         w in q
# #         for w in [
# #             "योजना",
# #             "yojana",
# #             "scheme",
# #             "स्कीम",
# #             "pension",
# #             "पेंशन",
# #             "subsidy",
# #             "सब्सिडी",
# #             "बीमा",
# #             "insurance",
# #             "scholarship",
# #             " छात्रवृत्ति",
# #         ]
# #     )

# #     if top_final >= 0.60:
# #         return True

# #     if has_scheme_word and top_final >= 0.25:
# #         return True

# #     return False


# # # ================== MODELS FOR JSON /ask ==================


# # class AskRequest(BaseModel):
# #     question: str
# #     ui_lang: str = "hi"        # "hi" | "garhwali" | "en"
# #     mode: str = "auto"         # "auto" | "docs" | "schemes"
# #     history: List[Dict[str, str]] = []
# #     user_meta: Dict[str, Any] | None = None


# # class AskResponse(BaseModel):
# #     response: str
# #     sources: List[Dict[str, Any]] = []


# # class SchemeCard(SQLModel):
# #     title: str
# #     subtitle: Optional[str] = None
# #     verified: bool = True
# #     badges: List[str] = []
# #     apply_url: Optional[str] = None
# #     read_more_url: Optional[str] = None


# # # ================== PERSONALISED RECOMMENDATIONS API ==================


# # @app.get("/user/recommended-schemes", response_model=List[SchemeCard])
# # def recommended_schemes(current_user: User = Depends(get_current_user)):
# #     # Build simple query text from profile
# #     parts = []

# #     if current_user.district:
# #         parts.append(current_user.district)
# #     if current_user.block:
# #         parts.append(current_user.block)
# #     if current_user.gender:
# #         parts.append(current_user.gender)
# #     if current_user.age:
# #         parts.append(f"age {current_user.age}")
# #     if current_user.interest_tag:
# #         parts.append(current_user.interest_tag)

# #     # 🔴 NEW – these strongly influence scheme matching
# #     if current_user.occupation:
# #         parts.append(current_user.occupation)
# #     if current_user.disability and current_user.disability.lower() not in (
# #         "none",
# #         "nahin",
# #         "no",
# #     ):
# #         parts.append("divyang")
# #         parts.append(current_user.disability)
# #     if current_user.income_bracket:
# #         parts.append(current_user.income_bracket)
# #     if current_user.social_category:
# #         parts.append(current_user.social_category)

# #     question = " ".join(parts) or "gramin yojana"

# #     schemes, _total = search_schemes(
# #         question=question,
# #         limit=5,
# #         page=1,
# #         min_score=0.20,
# #         category=None,
# #         department=None,
# #         typ=None,
# #     )

# #     cards: List[SchemeCard] = []
# #     for s in schemes:
# #         title = (
# #             (s.get("name_hi") or "")
# #             + (" / " + s.get("name_en", "") if s.get("name_en") else "")
# #         ).strip(" /")
# #         subtitle = s.get("description_hi") or s.get("description_en") or ""
# #         badges = [s.get("department", ""), s.get("category", "")]
# #         cards.append(
# #             SchemeCard(
# #                 title=title or "Yojana",
# #                 subtitle=subtitle,
# #                 verified=True,
# #                 badges=[b for b in badges if b],
# #                 apply_url=s.get("apply_link") or None,
# #                 read_more_url=s.get("source_url") or None,
# #             )
# #         )
# #     return cards


# # # ================== ROUTES (HTML DEMO) ==================


# # @app.get("/", response_class=HTMLResponse)
# # async def get_home(
# #     request: Request,
# #     lang: str = "hi",      # ui_lang
# #     mode: str = "docs",    # "docs" or "schemes"
# # ):
# #     # allow hi / en / garhwali in demo
# #     if lang not in ("hi", "en", "garhwali"):
# #         lang = "hi"
# #     if mode not in ("docs", "schemes"):
# #         mode = "docs"

# #     return templates.TemplateResponse(
# #         "index.html",
# #         {
# #             "request": request,
# #             "messages": [],
# #             "history_json": "[]",
# #             "lang": lang,
# #             "mode": mode,
# #         },
# #     )


# # @app.post("/", response_class=HTMLResponse)
# # async def post_query(
# #     request: Request,
# #     query: str = Form(...),
# #     history_json: str = Form("[]"),
# #     ui_lang: str = Form("hi"),   # "hi" | "garhwali" | "en"
# #     mode: str = Form("docs"),    # "docs" or "schemes"
# # ):
# #     try:
# #         history = json.loads(history_json)
# #     except Exception:
# #         history = []

# #     # Decide target language for demo HTML
# #     if ui_lang == "en":
# #         target_lang = "en"
# #     elif ui_lang == "garhwali":
# #         target_lang = "garhwali"
# #     else:
# #         # "hi" / default → Hindi or Hinglish based on script
# #         target_lang = "hi" if contains_devanagari(query) else "hinglish"

# #     if mode == "schemes":
# #         schemes, _total = search_schemes(
# #             question=query,
# #             limit=3,
# #             page=1,
# #             min_score=0.20,
# #             category=None,
# #             department=None,
# #             typ=None,
# #         )
# #         base_answer = build_schemes_answer(query, schemes)
# #     else:
# #         base_answer, _sources = generate_docs_answer_raw(query, history)

# #     final_text = translate_answer(base_answer, target_lang)
# #     answer_html = _convert_markdown_bold_to_html(final_text)

# #     history.append({"role": "user", "content": query})
# #     history.append({"role": "assistant", "content": answer_html})

# #     messages = [{"role": h["role"], "content": h["content"]} for h in history]

# #     return templates.TemplateResponse(
# #         "index.html",
# #         {
# #             "request": request,
# #             "messages": messages,
# #             "history_json": json.dumps(history, ensure_ascii=False),
# #             "lang": ui_lang,
# #             "mode": mode,
# #         },
# #     )


# # # ================== JSON API FOR REACT CHAT ==================


# # @app.post("/ask", response_model=AskResponse)
# # def ask(req: AskRequest):
# #     """
# #     Used by React ChatScreen.
# #     - Decides schemes vs docs (or forced by req.mode)
# #     - Applies translation for UI lang
# #     - Uses user_meta for slight personalisation
# #     - Returns { response, sources } that your ChatScreen understands
# #     """

# #     # Decide final language for UI
# #     if req.ui_lang == "en":
# #         target_lang = "en"
# #     elif req.ui_lang == "garhwali":
# #         target_lang = "garhwali"
# #     else:
# #         # "hi" / default → Hindi or Hinglish based on script
# #         target_lang = "hi" if contains_devanagari(req.question) else "hinglish"

# #     # 👤 user profile from frontend
# #     user_meta = req.user_meta or None

# #     schemes: List[Dict[str, Any]] = []
# #     doc_sources: List[Dict[str, Any]] = []
# #     use_schemes = False

# #     if req.mode in ("schemes", "auto"):
# #         schemes, total = search_schemes(
# #             question=req.question,
# #             limit=5,
# #             page=1,
# #             min_score=0.20,
# #             category=None,
# #             department=None,
# #             typ=None,
# #         )
# #         if req.mode == "schemes":
# #             use_schemes = True
# #         else:
# #             use_schemes = _should_use_schemes(req.question, schemes)

# #     if use_schemes:
# #         base_answer = build_schemes_answer(req.question, schemes, user_meta=user_meta)
# #         sources = [
# #             {
# #                 "name_hi": s.get("name_hi"),
# #                 "name_en": s.get("name_en"),
# #                 "score": s.get("_score"),
# #                 "department": s.get("department"),
# #                 "category": s.get("category"),
# #                 "apply_link": s.get("apply_link"),
# #             }
# #             for s in schemes
# #         ]
# #     else:
# #         base_answer, doc_sources = generate_docs_answer_raw(
# #             req.question,
# #             req.history,
# #             user_meta=user_meta,
# #         )
# #         sources = doc_sources

# #     final_text = translate_answer(base_answer, target_lang)
# #     final_html = _convert_markdown_bold_to_html(final_text)

# #     return AskResponse(response=final_html, sources=sources)


# # # ================== AUTH ROUTES ==================


# # @app.post("/auth/register", response_model=UserRead)
# # def register(user_in: UserCreate, session: Session = Depends(get_session)):
# #     existing = get_user_by_username(session, user_in.username)
# #     if existing:
# #         raise HTTPException(status_code=400, detail="Username already registered")

# #     user = User(
# #         username=user_in.username,
# #         full_name=user_in.full_name,
# #         hashed_password=get_password_hash(user_in.password),
# #         district=user_in.district,
# #         block=user_in.block,
# #         village_code=user_in.village_code,
# #         age=user_in.age,
# #         gender=user_in.gender,
# #         interest_tag=user_in.interest_tag,
# #         disability=user_in.disability,
# #         occupation=user_in.occupation,
# #         income_bracket=user_in.income_bracket,
# #         social_category=user_in.social_category,
# #     )
# #     session.add(user)
# #     session.commit()
# #     session.refresh(user)
# #     return user


# # @app.post("/auth/login", response_model=Token)
# # def login(
# #     form_data: OAuth2PasswordRequestForm = Depends(),
# #     session: Session = Depends(get_session),
# # ):
# #     user = get_user_by_username(session, form_data.username)
# #     if not user or not verify_password(form_data.password, user.hashed_password):
# #         raise HTTPException(status_code=400, detail="Incorrect username or password")

# #     token = create_access_token({"sub": user.username})
# #     return Token(access_token=token)


# # @app.get("/me", response_model=UserRead)
# # def read_me(current_user: User = Depends(get_current_user)):
# #     return current_user


# # @app.get("/health")
# # def health():
# #     return {
# #         "status": "ok",
# #         "docs_collection": DOC_COLLECTION,
# #         "schemes_collection": SCHEMES_COLLECTION,
# #         "embed_model_schemes": EMBED_MODEL_NAME_SCHEMES,
# #     }


# # @app.put("/me", response_model=UserRead)
# # def update_me(
# #     user_update: UserUpdate,
# #     current_user: User = Depends(get_current_user),
# #     session: Session = Depends(get_session),
# # ):
# #     data = user_update.dict(exclude_unset=True)

# #     for field, value in data.items():
# #         setattr(current_user, field, value)

# #     session.add(current_user)
# #     session.commit()
# #     session.refresh(current_user)
# #     return current_user



# import os
# import json
# import uuid
# import re
# import unicodedata
# from pathlib import Path
# from typing import List, Dict, Any, Optional, Tuple

# from dotenv import load_dotenv
# from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# from pydantic import BaseModel

# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchText,
# )
# from qdrant_client.http import models as qm  # noqa: F401

# from sentence_transformers import SentenceTransformer
# from fastembed import TextEmbedding
# from groq import Groq
# from googletrans import Translator  # Google Translate

# from sqlmodel import Field, SQLModel, Session, create_engine, select
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# # ================== CONFIG ==================

# BASE_DIR = Path(__file__).resolve().parent.parent  # repo root (panchayat-sahayika)

# # Schemes JSON path
# SCHEMES_PATH = BASE_DIR / "samaj_kalyan_vibhag_clean_typed.json"
# # or, if in public:
# # SCHEMES_PATH = BASE_DIR / "public" / "samaj_kalyan_vibhag_clean_typed.json"

# load_dotenv()

# # ---- Groq / LLM ----
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise RuntimeError("GROQ_API_KEY missing in .env")

# LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
# GROQ_MODEL_DOCS = os.getenv("GROQ_MODEL", LLM_MODEL)

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---- DOCS RAG Qdrant (remote or local) ----
# DOC_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# DOC_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
# DOC_COLLECTION = os.getenv("COLLECTION_NAME", "panchayat_uk_docs")

# doc_qclient = QdrantClient(url=DOC_QDRANT_URL, api_key=DOC_QDRANT_API_KEY)
# doc_embedder = TextEmbedding()

# # ---- Schemes Qdrant (local embedded) ----
# EMBED_MODEL_NAME_SCHEMES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# SCHEMES_COLLECTION = "samaj_kalyan_vibhag_schemes"

# scheme_embed_model = SentenceTransformer(EMBED_MODEL_NAME_SCHEMES)
# scheme_qdrant = QdrantClient(path=str(BASE_DIR / "qdrant_data"))

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

# # ---- FastAPI + Templates ----
# app = FastAPI(title="Panchayat Sahayika Unified Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )

# templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# translator = Translator()  # Google translator instance


# # ================== AUTH / USERS ==================

# DATABASE_URL = "sqlite:///./panchayat_users.db"  # SQLite file in backend folder
# engine = create_engine(DATABASE_URL, echo=False)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# SECRET_KEY = os.getenv(
#     "SECRET_KEY",
#     "baea29ce56f4b02733883b6ae1a76265988d123d5ad3e9d2214dae4646a81ee6",
# )
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str = Field(index=True, unique=True)
#     full_name: Optional[str] = None
#     hashed_password: str

#     # profile info (for recommendations / chatbot)
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None          # "M"/"F"/"O" or free text
#     interest_tag: Optional[str] = None    # "farmer", "student", etc.

#     disability: Optional[str] = None      # e.g. "none", "locomotor", "visual", etc.
#     occupation: Optional[str] = None      # "farmer", "student", "ASHA", "SHG member"...
#     income_bracket: Optional[str] = None  # "BPL", "APL", etc.
#     social_category: Optional[str] = None # "SC", "ST", "OBC", "General", etc.


# class UserCreate(SQLModel):
#     username: str
#     password: str
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserRead(SQLModel):
#     id: int
#     username: str
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserUpdate(SQLModel):
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class Token(SQLModel):
#     access_token: str
#     token_type: str = "bearer"


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# def _bcrypt_safe(password: str) -> str:
#     """
#     Bcrypt only uses first 72 bytes of the password.
#     To avoid errors, we explicitly cut to 72 bytes.
#     """
#     if password is None:
#         return ""
#     pw_bytes = password.encode("utf-8")
#     return pw_bytes[:72].decode("utf-8", errors="ignore")


# def get_password_hash(password: str) -> str:
#     safe_pw = _bcrypt_safe(password)
#     return pwd_context.hash(safe_pw)


# def verify_password(plain: str, hashed: str) -> bool:
#     safe_pw = _bcrypt_safe(plain)
#     return pwd_context.verify(safe_pw, hashed)


# def create_access_token(data: dict) -> str:
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# def get_user_by_username(session: Session, username: str) -> Optional[User]:
#     stmt = select(User).where(User.username == username)
#     return session.exec(stmt).first()


# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     session: Session = Depends(get_session),
# ) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: Optional[str] = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = get_user_by_username(session, username=username)
#     if not user:
#         raise credentials_exception
#     return user


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# # ================== COMMON LANGUAGE HELPERS ==================


# def contains_devanagari(text: str) -> bool:
#     """Check if text has any Devanagari characters."""
#     for ch in text:
#         if "\u0900" <= ch <= "\u097F":
#             return True
#     return False


# def _llm_translate(text: str, target_desc: str) -> str:
#     """
#     Generic translator using Groq LLM.
#     `target_desc` = description of target language/style.
#     """
#     system_msg = (
#         "You are a translator for Gram Panchayat content.\n"
#         "You ONLY translate the text; you do not add explanations.\n"
#         "Preserve markdown bold markers **like this** exactly as they are.\n"
#         "Do not change the meaning; only change the language.\n"
#     )

#     user_msg = (
#         f"Translate the following text into {target_desc}\n\n"
#         f"Text:\n{text}"
#     )

#     completion = groq_client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "system", "content": system_msg},
#             {"role": "user", "content": user_msg},
#         ],
#         temperature=0.2,
#         max_tokens=1200,
#     )
#     out = completion.choices[0].message.content or text
#     return out


# def translate_answer(text: str, target_lang: str) -> str:
#     """
#     Final step translation:

#     target_lang:
#       - 'en'        -> English
#       - 'hi'        -> simple Hindi (Devanagari)
#       - 'garhwali'  -> simple Garhwali (Devanagari)
#       - 'hinglish'  -> simple Hinglish (Roman Hindi)
#     """

#     # ---------- 1) English UI ----------
#     if target_lang == "en":
#         try:
#             res = translator.translate(text, dest="en")
#             out = res.text
#             if out and not contains_devanagari(out) and out.strip() != "":
#                 return out
#         except Exception:
#             pass

#         return _llm_translate(
#             text,
#             "clear, simple English suitable for village-level users. "
#             "Avoid Hindi script and use plain English sentences.",
#         )

#     # ---------- 2) Hindi (Devanagari) ----------
#     if target_lang == "hi":
#         return _llm_translate(
#             text,
#             "very simple Hindi in Devanagari script, using everyday words "
#             "that village-level users understand.",
#         )

#     # ---------- 3) Garhwali (Devanagari) ----------
#     if target_lang == "garhwali":
#         return _llm_translate(
#             text,
#             (
#                 "Translate into PURE Garhwali language (Central Garhwal dialect), "
#                 "written in Devanagari script.\n\n"
#                 "STRICT RULES:\n"
#                 "- Every sentence MUST be in natural Garhwali, not standard Hindi.\n"
#                 "- Avoid typical Hindi forms like: 'आप', 'कैसे', 'करना', 'है', 'हैगा', etc.\n"
#                 "- Prefer Garhwali forms: 'त्यूँ', 'कसि', 'च', 'भै', 'ल्यो', 'जा', 'रै', 'णै', etc.\n"
#                 "- Make sentences exactly like villagers speak at home.\n"
#                 "- EXAMPLES:\n"
#                 "  Hindi: 'आप कैसे हैं?' → Garhwali: 'त्यूँ कसि च?'\n"
#                 "  Hindi: 'मैं तुम्हारी मदद करूँगा।' → 'मैं तैरी मदद करैल।'\n"
#                 "  Hindi: 'यह प्रक्रिया ऐसे होती है।' → 'ई प्रक्रिया ऐसि ह्वै।'\n"
#                 "- Do NOT use Hindi connectors like: 'क्योंकि', 'लेकिन', 'इसके अलावा'.\n"
#                 "- Use Garhwali-style connectors where possible.\n"
#                 "- Keep government scheme names exactly in Hindi.\n"
#                 "- If a Hindi-style word is unavoidable, bend it into a Garhwali tone.",
#             ),
#         )

#     # ---------- 4) Hinglish (Roman Hindi) ----------
#     return _llm_translate(
#         text,
#         "very simple Hinglish (Roman Hindi using English letters). "
#         "Do NOT use Devanagari characters.",
#     )


# def _convert_markdown_bold_to_html(text: str) -> str:
#     """**bold** -> <strong>bold</strong> for UI."""
#     return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


# # ================== DOCS RAG PIPELINE ==================


# def build_docs_system_prompt() -> str:
#     """
#     System prompt for docs:
#     - Sirf Qdrant se aaye context ka use karo
#     - Gram Panchayat users ke liye simple Hindi
#     - Users can ask in Hindi, Hinglish, or Garhwali; you can first think in Hindi.
#     """
#     return (
#         "आप 'Panchayat Sahayika' हैं, उत्तराखंड की ग्राम पंचायतों के लिए सहायक.\n"
#         "यूज़र कभी-कभी गढ़वाली या हिंग्लिश में भी सवाल पूछ सकते हैं; "
#         "आप अर्थ समझकर पहले सरल हिन्दी में जवाब तैयार करें.\n"
#         "आपको केवल नीचे दिए गए संदर्भ (official Panchayati Raj documents: acts, rules, "
#         "guidelines, roles, schemes, training material)\n"
#         "का इस्तेमाल करके ही जवाब देना है.\n\n"
#         "भाषा बहुत ही सरल और आसान हिन्दी होनी चाहिए ताकि सरपंच, वार्ड मेंबर और ग्राम पंचायत कर्मचारी आसानी से समझ सकें.\n"
#         "कानूनी भारी शब्दों से बचें.\n"
#         "अगर ज़रूरी जानकारी संदर्भ में नहीं है, तो साफ-साफ लिखें कि यह जानकारी उपलब्ध नहीं है "
#         "और आप अंदाज़ा नहीं लगा रहे हैं.\n"
#         "कभी भी दस्तावेज़ का नाम, फाइल का नाम, पेज नंबर या 'source' list का ज़िक्र न करें.\n"
#     )


# def retrieve_docs_context(query: str, top_k: int = 8) -> List[Dict[str, Any]]:
#     query_vec = list(doc_embedder.embed([query]))[0]
#     results = doc_qclient.search(
#         collection_name=DOC_COLLECTION,
#         query_vector=query_vec,
#         limit=top_k,
#         with_payload=True,
#     )

#     contexts = []
#     for r in results:
#         pl = r.payload or {}
#         contexts.append(
#             {
#                 "text": pl.get("text", ""),
#                 "source_file": pl.get("source_file", ""),
#                 "page": pl.get("page", ""),
#                 "url": pl.get("url", ""),
#                 "score": r.score,
#             }
#         )
#     return contexts


# def generate_docs_answer_raw(
#     query: str,
#     history: List[Dict[str, str]],
#     user_meta: Dict[str, Any] | None = None,
# ) -> Tuple[str, List[Dict[str, Any]]]:
#     """
#     Returns raw answer in Hindi-ish language (LLM decides, but system prompt nudges to Hindi).
#     We will later translate to final UI language using translate_answer().
#     """
#     contexts = retrieve_docs_context(query)

#     context_block = "\n\n---\n\n".join(
#         c["text"] for c in contexts if c["text"]
#     )

#     # 👤 personalise a bit
#     user_ctx = build_user_context(user_meta)

#     system_prompt = build_docs_system_prompt()
#     if user_ctx:
#         system_prompt += (
#             "\n\nउपयोगकर्ता प्रोफाइल (उदाहरणों को practical banane ke liye):\n"
#             f"{user_ctx}\n"
#             "जवाब में आप user ki स्थिति ke हिसाब से छोटा सा context de sakte hain "
#             "(jaise किसान, छात्र, दिव्यांग इत्यादि)."
#         )

#     messages = [
#         {"role": "system", "content": system_prompt},
#     ]

#     # include a few last turns from history (server-side only)
#     for h in history[-4:] if history else []:
#         messages.append({"role": h["role"], "content": h["content"]})

#     messages.append(
#         {
#             "role": "user",
#             "content": (
#                 f"प्रश्न: {query}\n\n"
#                 f"नीचे दिए गए दस्तावेज़ों के संदर्भ का उपयोग करके उत्तर दीजिए. "
#                 f"अपने उत्तर में इन दस्तावेज़ों के नाम या पेज नंबर का ज़िक्र मत कीजिए:\n\n"
#                 f"{context_block}"
#             ),
#         }
#     )

#     completion = groq_client.chat.completions.create(
#         model=GROQ_MODEL_DOCS,
#         messages=messages,
#         temperature=0.3,
#         max_tokens=900,
#     )
#     raw_answer = completion.choices[0].message.content or ""

#     # dedupe sources
#     unique_sources = []
#     seen = set()
#     for c in contexts:
#         key = (c["source_file"], c["page"])
#         if key not in seen and c["source_file"]:
#             seen.add(key)
#             unique_sources.append(
#                 {
#                     "source_file": c["source_file"],
#                     "page": c["page"],
#                     "url": c["url"],
#                 }
#             )

#     return raw_answer, unique_sources


# # ================== SCHEMES PIPELINE ==================


# def load_schemes() -> List[Dict[str, Any]]:
#     with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     # ensure strings and minimal keys exist
#     for s in data:
#         s.setdefault("name_hi", "")
#         s.setdefault("name_en", "")
#         s.setdefault("category", "")
#         s.setdefault("department", "")
#         s.setdefault("description_hi", "")
#         s.setdefault("description_en", "")
#         s.setdefault("eligibility", "")
#         s.setdefault("benefit", "")
#         s.setdefault("apply_process", "")
#         s.setdefault("apply_link", "")
#         s.setdefault("source_url", "")
#         s.setdefault("type", s.get("type", "scheme"))
#     return data


# def _concat_item_text(s: Dict[str, Any]) -> str:
#     """
#     Text used for vector embedding.
#     We heavily weight the scheme name so that exact-name queries hit correctly.
#     """
#     name = (s.get("name_hi", "") + " " + s.get("name_en", "")).strip()
#     other_parts = [
#         s.get("category", ""),
#         s.get("department", ""),
#         s.get("description_hi", ""),
#         s.get("description_en", ""),
#         s.get("eligibility", ""),
#         s.get("benefit", ""),
#         s.get("apply_process", ""),
#     ]

#     # Repeat name 5x → boosts similarity when user types scheme name
#     weighted_name = " ".join([name] * 5) if name else ""
#     rest = " | ".join([str(p) for p in other_parts if p])

#     return " | ".join([p for p in [weighted_name, rest] if p])


# def init_schemes_collection():
#     schemes = load_schemes()

#     scheme_qdrant.recreate_collection(
#         collection_name=SCHEMES_COLLECTION,
#         vectors_config=VectorParams(
#             size=scheme_embed_model.get_sentence_embedding_dimension(),
#             distance=Distance.COSINE,
#         ),
#     )

#     points: List[PointStruct] = []
#     for s in schemes:
#         vec = scheme_embed_model.encode(_concat_item_text(s)).tolist()
#         payload = dict(s)
#         payload["__search_blob"] = _concat_item_text(s)
#         points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload))

#     scheme_qdrant.upsert(SCHEMES_COLLECTION, points)
#     print(f"✅ Indexed {len(points)} schemes into Qdrant (schemes collection)")


# # Build index at import time
# init_schemes_collection()


# def _norm(s: str) -> str:
#     if not s:
#         return ""
#     s = unicodedata.normalize("NFKC", s)
#     s = re.sub(r"\s+", " ", s).strip().lower()
#     return s


# def _qdrant_filter(
#     category: Optional[str],
#     department: Optional[str],
#     typ: Optional[str],
# ) -> Optional[Filter]:
#     conds = []
#     if category:
#         conds.append(FieldCondition(key="category", match=MatchText(text=category)))
#     if department:
#         conds.append(FieldCondition(key="department", match=MatchText(text=department)))
#     if typ:
#         conds.append(FieldCondition(key="type", match=MatchText(text=typ)))
#     if not conds:
#         return None
#     return Filter(must=conds)


# def _keyword_boost(question: str, item: Dict[str, Any]) -> float:
#     """
#     Simple textual boost based on name/category/department match.
#     Helps exact-name queries like 'atal awas yojna' hit the right scheme.
#     """
#     q = _norm(question)
#     name = _norm((item.get("name_hi", "") + " " + item.get("name_en", "")))
#     cat = _norm(item.get("category", ""))
#     dept = _norm(item.get("department", ""))

#     boost = 0.0

#     if q and q in name:
#         boost += 0.6

#     q_words = [w for w in q.split() if len(w) > 2]
#     for w in q_words:
#         if w in name or w in cat or w in dept:
#             boost += 0.15

#     return boost


# def search_schemes(
#     question: str,
#     limit: int = 3,
#     page: int = 1,
#     min_score: float = 0.20,
#     category: Optional[str] = None,
#     department: Optional[str] = None,
#     typ: Optional[str] = None,
# ):
#     """
#     Hybrid search for schemes.
#     Returns: (results:list[payload+_score], total:int)
#     """
#     qvec = scheme_embed_model.encode(question).tolist()
#     page = max(page, 1)
#     limit = max(1, min(20, limit))

#     MAX_HITS = 50

#     hits = scheme_qdrant.search(
#         collection_name=SCHEMES_COLLECTION,
#         query_vector=qvec,
#         limit=MAX_HITS,
#         with_payload=True,
#         with_vectors=False,
#         query_filter=_qdrant_filter(category, department, typ),
#     )

#     scored: List[Dict[str, Any]] = []
#     for h in hits:
#         base_score = float(h.score) if hasattr(h, "score") else 0.0
#         if base_score < min_score:
#             continue
#         p = dict(h.payload)
#         kw_boost = _keyword_boost(question, p)
#         final_score = base_score + kw_boost
#         p["_score"] = base_score
#         p["_final_score"] = final_score
#         scored.append(p)

#     # De-duplicate by scheme name
#     deduped: List[Dict[str, Any]] = []
#     seen = set()
#     for p in scored:
#         key = (p.get("name_hi") or p.get("name_en") or "").strip()
#         if not key:
#             key = p.get("id", "")
#         if key in seen:
#             continue
#         seen.add(key)
#         deduped.append(p)

#     deduped.sort(key=lambda x: x.get("_final_score", 0.0), reverse=True)

#     total = len(deduped)
#     start = (page - 1) * limit
#     end = start + limit
#     page_items = deduped[start:end]

#     return page_items, total


# def _fmt_scheme_card(s: Dict[str, Any]) -> str:
#     name = s.get("name_hi") or s.get("name_en") or "—"
#     bits = [
#         f"• **{name}**",
#         f"  - 🎓 पात्रता: {s.get('eligibility','उपलब्ध नहीं')}",
#         f"  - 💰 लाभ: {s.get('benefit','उपलब्ध नहीं')}",
#         f"  - 📝 आवेदन: {s.get('apply_process','उपलब्ध नहीं')}",
#     ]
#     if s.get("apply_link"):
#         bits.append(f"  - 🔗 लिंक: {s['apply_link']}")
#     return "\n".join(bits)


# def build_user_context(user_meta: dict | None) -> str:
#     """Convert user profile info into natural-language context for LLM."""
#     if not user_meta:
#         return ""

#     district = user_meta.get("district")
#     block = user_meta.get("block")
#     village = user_meta.get("village_code")
#     age = user_meta.get("age")
#     gender = user_meta.get("gender")
#     interest = user_meta.get("interest_tag")

#     disability = user_meta.get("disability")
#     occupation = user_meta.get("occupation")
#     income_bracket = user_meta.get("income_bracket")
#     social_category = user_meta.get("social_category")

#     parts = []

#     if district:
#         parts.append(f"जिला {district}")
#     if block:
#         parts.append(f"ब्लॉक {block}")
#     if village:
#         parts.append(f"गाँव कोड {village}")
#     if age:
#         parts.append(f"आयु {age} वर्ष")
#     if gender:
#         parts.append(f"लिंग {gender}")
#     if occupation:
#         parts.append(f"पेशा: {occupation}")
#     if income_bracket:
#         parts.append(f"आय वर्ग: {income_bracket}")
#     if social_category:
#         parts.append(f"सोशल कैटेगरी: {social_category}")
#     if disability and disability.lower() not in ("none", "nahin", "no"):
#         parts.append(f"विशेष आवश्यकताएँ / दिव्यांगता: {disability}")
#     if interest:
#         parts.append(f"रुचि: {interest}")

#     if not parts:
#         return ""

#     return "उपयोगकर्ता की जानकारी: " + ", ".join(parts) + ". "


# def build_schemes_answer(
#     question: str,
#     schemes: List[Dict[str, Any]],
#     user_meta: Dict[str, Any] | None = None,
# ) -> str:
#     """
#     Build Hindi-centric, LLM-generated answer for schemes.
#     Personalised slightly using user_meta (occupation, disability, etc.).
#     """
#     if not schemes:
#         return (
#             "माफ़ कीजिए, इस सवाल से मिलती-जुलती कोई योजना नहीं मिली. "
#             "कृपया अलग शब्दों में पूछें, या ज़िला/विभाग/श्रेणी लिखें.\n\n"
#             "**English:** No strong matches. Try different words or add location/department."
#         )

#     user_ctx = build_user_context(user_meta)

#     q_low = question.lower()
#     want_apply = any(
#         w in q_low
#         for w in [
#             "apply",
#             " आवेदन",
#             "आवेदन",
#             "फॉर्म",
#             "form",
#             "कैसे",
#             "kaise",
#             "कहाँ",
#             "kaha",
#             "कहां",
#         ]
#     )
#     want_benefit = any(
#         w in q_low
#         for w in [
#             "लाभ",
#             "benefit",
#             "paisa",
#             "₹",
#             "kitna",
#             "कितना",
#             "राशि",
#         ]
#     )
#     want_elig = any(
#         w in q_low
#         for w in [
#             "पात्रता",
#             "eligibility",
#             "kaun",
#             "कौन",
#             "किसको",
#             "kis ko",
#             "kisko",
#         ]
#     )

#     if not GROQ_API_KEY:
#         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
#         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
#         eng = (
#             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
#         )
#         return hdr + body + eng

#     context_lines = []
#     for s in schemes:
#         context_lines.append(
#             "योजना: {name}\nविवरण: {desc}\nपात्रता: {elig}\nलाभ: {ben}\nआवेदन प्रक्रिया: {proc}\nविभाग: {dept}\nश्रेणी: {cat}\nलिंक: {link}\n".format(
#                 name=(s.get("name_hi") or s.get("name_en") or ""),
#                 desc=s.get("description_hi", ""),
#                 elig=s.get("eligibility", ""),
#                 ben=s.get("benefit", ""),
#                 proc=s.get("apply_process", ""),
#                 dept=s.get("department", ""),
#                 cat=s.get("category", ""),
#                 link=s.get("apply_link", ""),
#             )
#         )
#     context = "\n---\n".join(context_lines)

#     focus_lines = []
#     if want_apply:
#         focus_lines.append(
#             "- User is mainly asking **how to apply**. "
#             "You MUST explain the पूरा 'आवेदन प्रक्रिया' field step-by-step in simple Hindi. "
#             "हर ज़रूरी स्टेप और हर ज़रूरी दस्तावेज़ का नाम जरूर बताएं."
#         )
#     if want_benefit:
#         focus_lines.append(
#             "- User is asking about **benefits / amount**. "
#             "Explain the 'लाभ' field completely. अलग-अलग राशि हो तो सब बताएं."
#         )
#     if want_elig:
#         focus_lines.append(
#             "- User is asking about **eligibility / who can get it**. "
#             "Explain the 'पात्रता' field पूरी तरह, सभी शर्तें (1, 2, 3...) अलग-अलग लिखें."
#         )

#     focus_text = "\n".join(focus_lines) if focus_lines else "- Follow the general rules below."

#     # 👤 personalisation text
#     profile_text = (
#         user_ctx
#         or "कोई अतिरिक्त उपयोगकर्ता जानकारी उपलब्ध नहीं है. अगर जानकारी ना हो तो generic जवाब दें."
#     )

#     prompt = f"""
# You are **Panchayat Sahayika**, a friendly, polite and knowledgeable AI assistant created to help rural citizens of India. 
# Your main goal is to explain information in very **simple, clear, human-like Hindi**, so that even villagers, elderly people, 
# and first-time smartphone users can easily understand.

# User profile (for context, don't repeat fully, just use it smartly in examples):
# {profile_text}

# You must use **only** the information given in the schemes context below. 
# Do NOT invent or guess any benefits, eligibility rules, amounts or links that are not present.

# --------------------------------------------
# 📌 USER QUESTION:
# {question}

# 📌 RELEVANT SCHEMES (if matched):
# {context}
# --------------------------------------------

# ### 🔍 SPECIAL FOCUS (based on the user's question)
# {focus_text}

# ### 🟢 MAIN RULES FOR ANSWERING:
# - Explain in **simple conversational Hindi**, short sentences, and natural flow.  
# - Do NOT sound robotic. Do NOT dump raw data.  
# - Be clear, warm, and practical.
# - **Whenever you write the name of any scheme / yojana, always wrap it like this: `**PM Awas Yojana**`.  
#   यानी हर योजना का नाम hamesha `**` ke andar hona chahiye.**

# Include these only if available in provided context:
# - योज़ना / स्कीम का नाम  
# - यह किसके लिए है (पात्रता)  
# - कितना लाभ मिलता है (लाभ)  
# - कैसे और कहाँ आवेदन करना है (आवेदन प्रक्रिया)  
# - लिंक हो तो बताएं  

# If multiple schemes match, explain **2–3** clearly but naturally.
# Missing data → write “उपलब्ध नहीं” naturally.

# ### 🟡 ALWAYS END WITH:
# "अगर ज़रूरत हो तो अपने ग्राम पंचायत या CSC केंद्र से मदद लें।"

# ### 🌍 AFTER THE HINDI ANSWER:
# Give **one short English summary sentence** (not detailed).

# --------------------------------------------
# Now write the final answer in a natural, fluent, friendly tone.
# --------------------------------------------
# """

#     try:
#         completion = groq_client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2,
#         )
#         ai_answer = completion.choices[0].message.content.strip()
#     except Exception:
#         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
#         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
#         eng = (
#             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
#         )
#         return hdr + body + eng

#     return ai_answer


# def _should_use_schemes(question: str, schemes: List[Dict[str, Any]]) -> bool:
#     """
#     Decide kare ki is query ke liye schemes pipeline use karni hai ya nahi.
#     """
#     if not schemes:
#         return False

#     top = schemes[0]
#     top_final = float(top.get("_final_score", top.get("_score", 0.0)) or 0.0)

#     q = question.lower()
#     has_scheme_word = any(
#         w in q
#         for w in [
#             "योजना",
#             "yojana",
#             "scheme",
#             "स्कीम",
#             "pension",
#             "पेंशन",
#             "subsidy",
#             "सब्सिडी",
#             "बीमा",
#             "insurance",
#             "scholarship",
#             " छात्रवृत्ति",
#         ]
#     )

#     if top_final >= 0.60:
#         return True

#     if has_scheme_word and top_final >= 0.25:
#         return True

#     return False


# # ================== MODELS FOR JSON /ask ==================


# class AskRequest(BaseModel):
#     question: str
#     ui_lang: str = "hi"        # "hi" | "garhwali" | "en"
#     mode: str = "auto"         # "auto" | "docs" | "schemes"
#     history: List[Dict[str, str]] = []
#     user_meta: Dict[str, Any] | None = None


# class AskResponse(BaseModel):
#     response: str
#     sources: List[Dict[str, Any]] = []


# class SchemeCard(SQLModel):
#     title: str
#     subtitle: Optional[str] = None
#     verified: bool = True
#     badges: List[str] = []
#     apply_url: Optional[str] = None
#     read_more_url: Optional[str] = None


# # ================== PERSONALISED RECOMMENDATIONS API ==================


# @app.get("/user/recommended-schemes", response_model=List[SchemeCard])
# def recommended_schemes(current_user: User = Depends(get_current_user)):
#     # Build simple query text from profile
#     parts = []

#     if current_user.district:
#         parts.append(current_user.district)
#     if current_user.block:
#         parts.append(current_user.block)
#     if current_user.gender:
#         parts.append(current_user.gender)
#     if current_user.age:
#         parts.append(f"age {current_user.age}")
#     if current_user.interest_tag:
#         parts.append(current_user.interest_tag)

#     # strongly influence scheme matching
#     if current_user.occupation:
#         parts.append(current_user.occupation)
#     if current_user.disability and current_user.disability.lower() not in (
#         "none",
#         "nahin",
#         "no",
#     ):
#         parts.append("divyang")
#         parts.append(current_user.disability)
#     if current_user.income_bracket:
#         parts.append(current_user.income_bracket)
#     if current_user.social_category:
#         parts.append(current_user.social_category)

#     question = " ".join(parts) or "gramin yojana"

#     schemes, _total = search_schemes(
#         question=question,
#         limit=5,
#         page=1,
#         min_score=0.20,
#         category=None,
#         department=None,
#         typ=None,
#     )

#     cards: List[SchemeCard] = []
#     for s in schemes:
#         title = (
#             (s.get("name_hi") or "")
#             + (" / " + s.get("name_en", "") if s.get("name_en") else "")
#         ).strip(" /")
#         subtitle = s.get("description_hi") or s.get("description_en") or ""
#         badges = [s.get("department", ""), s.get("category", "")]
#         cards.append(
#             SchemeCard(
#                 title=title or "Yojana",
#                 subtitle=subtitle,
#                 verified=True,
#                 badges=[b for b in badges if b],
#                 apply_url=s.get("apply_link") or None,
#                 read_more_url=s.get("source_url") or None,
#             )
#         )
#     return cards


# # ================== ROUTES (HTML DEMO) ==================


# @app.get("/", response_class=HTMLResponse)
# async def get_home(
#     request: Request,
#     lang: str = "hi",      # ui_lang
#     mode: str = "docs",    # "docs" or "schemes"
# ):
#     # allow hi / en / garhwali in demo
#     if lang not in ("hi", "en", "garhwali"):
#         lang = "hi"
#     if mode not in ("docs", "schemes"):
#         mode = "docs"

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "messages": [],
#             "history_json": "[]",
#             "lang": lang,
#             "mode": mode,
#         },
#     )


# @app.post("/", response_class=HTMLResponse)
# async def post_query(
#     request: Request,
#     query: str = Form(...),
#     history_json: str = Form("[]"),
#     ui_lang: str = Form("hi"),   # "hi" | "garhwali" | "en"
#     mode: str = Form("docs"),    # "docs" or "schemes"
# ):
#     try:
#         history = json.loads(history_json)
#     except Exception:
#         history = []

#     # Decide target language for demo HTML
#     if ui_lang == "en":
#         target_lang = "en"
#     elif ui_lang == "garhwali":
#         target_lang = "garhwali"
#     else:
#         # "hi" / default → Hindi or Hinglish based on script
#         target_lang = "hi" if contains_devanagari(query) else "hinglish"

#     if mode == "schemes":
#         schemes, _total = search_schemes(
#             question=query,
#             limit=3,
#             page=1,
#             min_score=0.20,
#             category=None,
#             department=None,
#             typ=None,
#         )
#         base_answer = build_schemes_answer(query, schemes)
#     else:
#         base_answer, _sources = generate_docs_answer_raw(query, history)

#     final_text = translate_answer(base_answer, target_lang)
#     answer_html = _convert_markdown_bold_to_html(final_text)

#     history.append({"role": "user", "content": query})
#     history.append({"role": "assistant", "content": answer_html})

#     messages = [{"role": h["role"], "content": h["content"]} for h in history]

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "messages": messages,
#             "history_json": json.dumps(history, ensure_ascii=False),
#             "lang": ui_lang,
#             "mode": mode,
#         },
#     )


# # ================== JSON API FOR REACT CHAT ==================


# @app.post("/ask", response_model=AskResponse)
# def ask(req: AskRequest):
#     """
#     Used by React ChatScreen.
#     - Decides schemes vs docs (or forced by req.mode)
#     - Applies translation for UI lang
#     - Uses user_meta for slight personalisation
#     - Returns { response, sources } that your ChatScreen understands
#     """

#     # Decide final language for UI
#     if req.ui_lang == "en":
#         target_lang = "en"
#     elif req.ui_lang == "garhwali":
#         target_lang = "garhwali"
#     else:
#         # "hi" / default → Hindi or Hinglish based on script
#         target_lang = "hi" if contains_devanagari(req.question) else "hinglish"

#     # 👤 user profile from frontend
#     user_meta = req.user_meta or None

#     schemes: List[Dict[str, Any]] = []
#     doc_sources: List[Dict[str, Any]] = []
#     use_schemes = False

#     if req.mode in ("schemes", "auto"):
#         schemes, total = search_schemes(
#             question=req.question,
#             limit=5,
#             page=1,
#             min_score=0.20,
#             category=None,
#             department=None,
#             typ=None,
#         )
#         if req.mode == "schemes":
#             use_schemes = True
#         else:
#             use_schemes = _should_use_schemes(req.question, schemes)

#     if use_schemes:
#         base_answer = build_schemes_answer(req.question, schemes, user_meta=user_meta)
#         sources = [
#             {
#                 "name_hi": s.get("name_hi"),
#                 "name_en": s.get("name_en"),
#                 "score": s.get("_score"),
#                 "department": s.get("department"),
#                 "category": s.get("category"),
#                 "apply_link": s.get("apply_link"),
#             }
#             for s in schemes
#         ]
#     else:
#         base_answer, doc_sources = generate_docs_answer_raw(
#             req.question,
#             req.history,
#             user_meta=user_meta,
#         )
#         sources = doc_sources

#     final_text = translate_answer(base_answer, target_lang)
#     final_html = _convert_markdown_bold_to_html(final_text)

#     return AskResponse(response=final_html, sources=sources)


# # ================== AUTH ROUTES ==================


# @app.post("/auth/register", response_model=UserRead)
# def register(user_in: UserCreate, session: Session = Depends(get_session)):
#     existing = get_user_by_username(session, user_in.username)
#     if existing:
#         raise HTTPException(status_code=400, detail="Username already registered")

#     user = User(
#         username=user_in.username,
#         full_name=user_in.full_name,
#         hashed_password=get_password_hash(user_in.password),
#         district=user_in.district,
#         block=user_in.block,
#         village_code=user_in.village_code,
#         age=user_in.age,
#         gender=user_in.gender,
#         interest_tag=user_in.interest_tag,
#         disability=user_in.disability,
#         occupation=user_in.occupation,
#         income_bracket=user_in.income_bracket,
#         social_category=user_in.social_category,
#     )
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user


# @app.post("/auth/login", response_model=Token)
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     session: Session = Depends(get_session),
# ):
#     user = get_user_by_username(session, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     token = create_access_token({"sub": user.username})
#     return Token(access_token=token)


# @app.get("/me", response_model=UserRead)
# def read_me(current_user: User = Depends(get_current_user)):
#     return current_user


# @app.put("/me", response_model=UserRead)
# def update_me(
#     user_update: UserUpdate,
#     current_user: User = Depends(get_current_user),
#     session: Session = Depends(get_session),
# ):
#     data = user_update.dict(exclude_unset=True)

#     for field, value in data.items():
#         setattr(current_user, field, value)

#     session.add(current_user)
#     session.commit()
#     session.refresh(current_user)
#     return current_user


# @app.get("/health")
# def health():
#     return {
#         "status": "ok",
#         "docs_collection": DOC_COLLECTION,
#         "schemes_collection": SCHEMES_COLLECTION,
#         "embed_model_schemes": EMBED_MODEL_NAME_SCHEMES,
#     }





# import os
# import json
# import uuid
# import re
# import unicodedata
# import tempfile
# import shutil
# from pathlib import Path
# from typing import List, Dict, Any, Optional, Tuple

# from dotenv import load_dotenv
# from fastapi import (
#     FastAPI,
#     Request,
#     Form,
#     Depends,
#     HTTPException,
#     status,
#     UploadFile,
#     File,
# )
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# from pydantic import BaseModel

# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchText,
# )
# from qdrant_client.http import models as qm  # noqa: F401  (kept if later needed)

# from sentence_transformers import SentenceTransformer
# from fastembed import TextEmbedding
# from groq import Groq
# from googletrans import Translator  # Google Translate

# from faster_whisper import WhisperModel
# from gtts import gTTS

# from sqlmodel import Field, SQLModel, Session, create_engine, select
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# # ================== CONFIG ==================

# BASE_DIR = Path(__file__).resolve().parent.parent  # repo root (panchayat-sahayika)

# # Schemes JSON path
# SCHEMES_PATH = BASE_DIR / "samaj_kalyan_vibhag_clean_typed.json"
# # or, if in public:
# # SCHEMES_PATH = BASE_DIR / "public" / "samaj_kalyan_vibhag_clean_typed.json"

# # TTS output directory
# TTS_OUTPUT_DIR = BASE_DIR / "tts_output"
# TTS_OUTPUT_DIR.mkdir(exist_ok=True)

# load_dotenv()

# # ---- Groq / LLM ----
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise RuntimeError("GROQ_API_KEY missing in .env")

# LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
# GROQ_MODEL_DOCS = os.getenv("GROQ_MODEL", LLM_MODEL)

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---- DOCS RAG Qdrant (remote or local) ----
# DOC_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# DOC_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
# DOC_COLLECTION = os.getenv("COLLECTION_NAME", "panchayat_uk_docs")

# doc_qclient = QdrantClient(url=DOC_QDRANT_URL, api_key=DOC_QDRANT_API_KEY)
# doc_embedder = TextEmbedding()

# # ---- Schemes Qdrant (local embedded) ----
# EMBED_MODEL_NAME_SCHEMES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# SCHEMES_COLLECTION = "samaj_kalyan_vibhag_schemes"

# scheme_embed_model = SentenceTransformer(EMBED_MODEL_NAME_SCHEMES)
# scheme_qdrant = QdrantClient(path=str(BASE_DIR / "qdrant_data"))

# # ---- Voice models (Whisper STT) ----
# WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "medium")
# USE_CUDA = os.getenv("USE_CUDA", "0") == "1"

# whisper_model = WhisperModel(
#     WHISPER_MODEL_NAME,
#     device="cuda" if USE_CUDA else "cpu",
#     compute_type="float16" if USE_CUDA else "int8",
# )

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

# # ---- FastAPI + Templates ----
# app = FastAPI(title="Panchayat Sahayika Unified Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )

# # static mount for TTS files
# app.mount("/tts", StaticFiles(directory=str(TTS_OUTPUT_DIR)), name="tts")

# templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# translator = Translator()  # Google translator instance

# # ================== AUTH / USERS ==================

# DATABASE_URL = "sqlite:///./panchayat_users.db"  # SQLite file in backend folder
# engine = create_engine(DATABASE_URL, echo=False)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# SECRET_KEY = os.getenv(
#     "SECRET_KEY",
#     "baea29ce56f4b02733883b6ae1a76265988d123d5ad3e9d2214dae4646a81ee6",
# )
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str = Field(index=True, unique=True)
#     full_name: Optional[str] = None
#     hashed_password: str

#     # profile info (for recommendations / chatbot)
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None          # "M"/"F"/"O" or free text
#     interest_tag: Optional[str] = None    # "farmer", "student", etc.

#     disability: Optional[str] = None      # e.g. "none", "locomotor", "visual", etc.
#     occupation: Optional[str] = None      # "farmer", "student", "ASHA", "SHG member"...
#     income_bracket: Optional[str] = None  # "BPL", "APL", etc.
#     social_category: Optional[str] = None # "SC", "ST", "OBC", "General", etc.


# class UserCreate(SQLModel):
#     username: str
#     password: str
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserRead(SQLModel):
#     id: int
#     username: str
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserUpdate(SQLModel):
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class Token(SQLModel):
#     access_token: str
#     token_type: str = "bearer"


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# def _bcrypt_safe(password: str) -> str:
#     """
#     Bcrypt only uses first 72 bytes of the password.
#     To avoid errors, we explicitly cut to 72 bytes.
#     """
#     if password is None:
#         return ""
#     pw_bytes = password.encode("utf-8")
#     return pw_bytes[:72].decode("utf-8", errors="ignore")


# def get_password_hash(password: str) -> str:
#     safe_pw = _bcrypt_safe(password)
#     return pwd_context.hash(safe_pw)


# def verify_password(plain: str, hashed: str) -> bool:
#     safe_pw = _bcrypt_safe(plain)
#     return pwd_context.verify(safe_pw, hashed)


# def create_access_token(data: dict) -> str:
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# def get_user_by_username(session: Session, username: str) -> Optional[User]:
#     stmt = select(User).where(User.username == username)
#     return session.exec(stmt).first()


# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     session: Session = Depends(get_session),
# ) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: Optional[str] = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = get_user_by_username(session, username=username)
#     if not user:
#         raise credentials_exception
#     return user


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

# # ================== COMMON LANGUAGE + VOICE HELPERS ==================


# def contains_devanagari(text: str) -> bool:
#     """Check if text has any Devanagari characters."""
#     for ch in text:
#         if "\u0900" <= ch <= "\u097F":
#             return True
#     return False


# def _llm_translate(text: str, target_desc: str) -> str:
#     """
#     Generic translator using Groq LLM.
#     `target_desc` = description of target language/style.
#     """
#     system_msg = (
#         "You are a translator for Gram Panchayat content.\n"
#         "You ONLY translate the text; you do not add explanations.\n"
#         "Preserve markdown bold markers **like this** exactly as they are.\n"
#         "Do not change the meaning; only change the language.\n"
#     )

#     user_msg = (
#         f"Translate the following text into {target_desc}\n\n"
#         f"Text:\n{text}"
#     )

#     completion = groq_client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "system", "content": system_msg},
#             {"role": "user", "content": user_msg},
#         ],
#         temperature=0.2,
#         max_tokens=1200,
#     )
#     out = completion.choices[0].message.content or text
#     return out


# def translate_answer(text: str, target_lang: str) -> str:
#     """
#     Final step translation:

#     target_lang:
#       - 'en'        -> English
#       - 'hi'        -> simple Hindi (Devanagari)
#       - 'garhwali'  -> simple Garhwali (Devanagari)
#       - 'hinglish'  -> simple Hinglish (Roman Hindi)
#     """

#     # ---------- 1) English UI ----------
#     if target_lang == "en":
#         try:
#             res = translator.translate(text, dest="en")
#             out = res.text
#             if out and not contains_devanagari(out) and out.strip() != "":
#                 return out
#         except Exception:
#             pass

#         return _llm_translate(
#             text,
#             "clear, simple English suitable for village-level users. "
#             "Avoid Hindi script and use plain English sentences.",
#         )

#     # ---------- 2) Hindi (Devanagari) ----------
#     if target_lang == "hi":
#         return _llm_translate(
#             text,
#             "very simple Hindi in Devanagari script, using everyday words "
#             "that village-level users understand.",
#         )

#     # ---------- 3) Garhwali (Devanagari) ----------
#     if target_lang == "garhwali":
#         return _llm_translate(
#             text,
#             (
#                 "Translate into PURE Garhwali language (Central Garhwal dialect), "
#                 "written in Devanagari script.\n\n"
#                 "STRICT RULES:\n"
#                 "- Every sentence MUST be in natural Garhwali, NOT standard Hindi.\n"
#                 "- Avoid Hindi forms: 'आप', 'कैसे', 'करना', 'है', 'होगा' etc.\n"
#                 "- Use Garhwali forms: 'त्यूँ', 'कसि', 'च', 'जा', 'रै', 'ल्यो', 'णै' etc.\n"
#                 "- Make sentences exactly like villagers speak at home.\n"
#                 "- Government scheme names must stay exactly as in Hindi.\n"
#             ),
#         )

#     # ---------- 4) Hinglish (Roman Hindi) ----------
#     return _llm_translate(
#         text,
#         "very simple Hinglish (Roman Hindi using English letters). "
#         "Do NOT use Devanagari characters.",
#     )


# def _convert_markdown_bold_to_html(text: str) -> str:
#     """**bold** -> <strong>bold</strong> for UI."""
#     return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


# def transcribe_garhwali_audio(path: str) -> str:
#     """
#     Whisper se Garhwali/Hindi transcription.
#     Hum language="hi" hint dete hain, taaki model Hindi script me likhe.
#     Speaker Garhwali bolega, text mostly Hindi/near-Garhwali me aa jayega.
#     """
#     segments, info = whisper_model.transcribe(
#         path,
#         language="hi",
#         task="transcribe",
#         vad_filter=True,
#     )
#     pieces = [seg.text.strip() for seg in segments if seg.text.strip()]
#     text = " ".join(pieces).strip()
#     return text


# def tts_garhwali(text: str) -> str:
#     """
#     Garhwali text (Devanagari) ko Hindi TTS se bolwate hain.
#     Returns: relative filename inside TTS_OUTPUT_DIR.
#     """
#     safe_text = text.strip()
#     if len(safe_text) > 1500:
#         safe_text = safe_text[:1500]

#     filename = f"garhwali_{uuid.uuid4().hex}.mp3"
#     out_path = TTS_OUTPUT_DIR / filename

#     tts = gTTS(text=safe_text, lang="hi")
#     tts.save(str(out_path))

#     return filename

# # ================== DOCS RAG PIPELINE ==================


# def build_docs_system_prompt() -> str:
#     """
#     System prompt for docs:
#     - Sirf Qdrant se aaye context ka use karo
#     - Gram Panchayat users ke liye simple Hindi
#     - Users can ask in Hindi, Hinglish, or Garhwali.
#     """
#     return (
#         "आप 'Panchayat Sahayika' हैं, उत्तराखंड की ग्राम पंचायतों के लिए सहायक।\n"
#         "यूज़र कभी-कभी गढ़वाली या हिंग्लिश में भी सवाल पूछ सकते हैं; "
#         "आप अर्थ समझकर पहले सरल हिन्दी में जवाब तैयार करें।\n"
#         "आपको केवल नीचे दिए गए संदर्भ (official Panchayati Raj documents: acts, rules, "
#         "guidelines, roles, schemes, training material) का इस्तेमाल करके ही जवाब देना है।\n\n"
#         "भाषा बहुत ही सरल और आसान हिन्दी होनी चाहिए ताकि सरपंच, वार्ड मेंबर और ग्राम पंचायत "
#         "कर्मचारी आसानी से समझ सकें।\n"
#         "कानूनी भारी शब्दों से बचें।\n"
#         "अगर ज़रूरी जानकारी संदर्भ में नहीं है, तो साफ-साफ लिखें कि यह जानकारी उपलब्ध नहीं है "
#         "और आप अंदाज़ा नहीं लगा रहे हैं।\n"
#         "कभी भी दस्तावेज़ का नाम, फाइल का नाम, पेज नंबर या 'source' list का ज़िक्र न करें।\n"
#     )


# def retrieve_docs_context(query: str, top_k: int = 8) -> List[Dict[str, Any]]:
#     query_vec = list(doc_embedder.embed([query]))[0]
#     results = doc_qclient.search(
#         collection_name=DOC_COLLECTION,
#         query_vector=query_vec,
#         limit=top_k,
#         with_payload=True,
#     )

#     contexts = []
#     for r in results:
#         pl = r.payload or {}
#         contexts.append(
#             {
#                 "text": pl.get("text", ""),
#                 "source_file": pl.get("source_file", ""),
#                 "page": pl.get("page", ""),
#                 "url": pl.get("url", ""),
#                 "score": r.score,
#             }
#         )
#     return contexts


# def generate_docs_answer_raw(
#     query: str,
#     history: List[Dict[str, str]],
#     user_meta: Dict[str, Any] | None = None,
# ) -> Tuple[str, List[Dict[str, Any]]]:
#     """
#     Returns raw answer in Hindi-ish language (LLM decides, but system prompt nudges to Hindi).
#     We will later translate to final UI language using translate_answer().
#     """
#     contexts = retrieve_docs_context(query)

#     context_block = "\n\n---\n\n".join(c["text"] for c in contexts if c["text"])

#     # 👤 personalise a bit
#     user_ctx = build_user_context(user_meta)

#     system_prompt = build_docs_system_prompt()
#     if user_ctx:
#         system_prompt += (
#             "\n\nउपयोगकर्ता प्रोफाइल (उदाहरणों को practical banane ke liye):\n"
#             f"{user_ctx}\n"
#             "जवाब में आप user ki स्थिति ke हिसाब से छोटा सा context de sakte hain "
#             "(jaise किसान, छात्र, दिव्यांग इत्यादि)."
#         )

#     messages = [
#         {"role": "system", "content": system_prompt},
#     ]

#     # include a few last turns from history (server-side only)
#     for h in history[-4:] if history else []:
#         messages.append({"role": h["role"], "content": h["content"]})

#     messages.append(
#         {
#             "role": "user",
#             "content": (
#                 f"प्रश्न: {query}\n\n"
#                 f"नीचे दिए गए दस्तावेज़ों के संदर्भ का उपयोग करके उत्तर दीजिए। "
#                 f"अपने उत्तर में इन दस्तावेज़ों के नाम या पेज नंबर का ज़िक्र मत कीजिए:\n\n"
#                 f"{context_block}"
#             ),
#         }
#     )

#     completion = groq_client.chat.completions.create(
#         model=GROQ_MODEL_DOCS,
#         messages=messages,
#         temperature=0.3,
#         max_tokens=900,
#     )
#     raw_answer = completion.choices[0].message.content or ""

#     # dedupe sources
#     unique_sources = []
#     seen = set()
#     for c in contexts:
#         key = (c["source_file"], c["page"])
#         if key not in seen and c["source_file"]:
#             seen.add(key)
#             unique_sources.append(
#                 {
#                     "source_file": c["source_file"],
#                     "page": c["page"],
#                     "url": c["url"],
#                 }
#             )

#     return raw_answer, unique_sources

# # ================== SCHEMES PIPELINE ==================


# def load_schemes() -> List[Dict[str, Any]]:
#     with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     # ensure strings and minimal keys exist
#     for s in data:
#         s.setdefault("name_hi", "")
#         s.setdefault("name_en", "")
#         s.setdefault("category", "")
#         s.setdefault("department", "")
#         s.setdefault("description_hi", "")
#         s.setdefault("description_en", "")
#         s.setdefault("eligibility", "")
#         s.setdefault("benefit", "")
#         s.setdefault("apply_process", "")
#         s.setdefault("apply_link", "")
#         s.setdefault("source_url", "")
#         s.setdefault("type", s.get("type", "scheme"))
#     return data


# def _concat_item_text(s: Dict[str, Any]) -> str:
#     """
#     Text used for vector embedding.
#     We heavily weight the scheme name so that exact-name queries hit correctly.
#     """
#     name = (s.get("name_hi", "") + " " + s.get("name_en", "")).strip()
#     other_parts = [
#         s.get("category", ""),
#         s.get("department", ""),
#         s.get("description_hi", ""),
#         s.get("description_en", ""),
#         s.get("eligibility", ""),
#         s.get("benefit", ""),
#         s.get("apply_process", ""),
#     ]

#     # Repeat name 5x → boosts similarity when user types scheme name
#     weighted_name = " ".join([name] * 5) if name else ""
#     rest = " | ".join([str(p) for p in other_parts if p])

#     return " | ".join([p for p in [weighted_name, rest] if p])


# def init_schemes_collection():
#     schemes = load_schemes()

#     scheme_qdrant.recreate_collection(
#         collection_name=SCHEMES_COLLECTION,
#         vectors_config=VectorParams(
#             size=scheme_embed_model.get_sentence_embedding_dimension(),
#             distance=Distance.COSINE,
#         ),
#     )

#     points: List[PointStruct] = []
#     for s in schemes:
#         vec = scheme_embed_model.encode(_concat_item_text(s)).tolist()
#         payload = dict(s)
#         payload["__search_blob"] = _concat_item_text(s)
#         points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload))

#     scheme_qdrant.upsert(SCHEMES_COLLECTION, points)
#     print(f"✅ Indexed {len(points)} schemes into Qdrant (schemes collection)")


# # Build index at import time
# init_schemes_collection()


# def _norm(s: str) -> str:
#     if not s:
#         return ""
#     s = unicodedata.normalize("NFKC", s)
#     s = re.sub(r"\s+", " ", s).strip().lower()
#     return s


# def _qdrant_filter(
#     category: Optional[str],
#     department: Optional[str],
#     typ: Optional[str],
# ) -> Optional[Filter]:
#     conds = []
#     if category:
#         conds.append(FieldCondition(key="category", match=MatchText(text=category)))
#     if department:
#         conds.append(FieldCondition(key="department", match=MatchText(text=department)))
#     if typ:
#         conds.append(FieldCondition(key="type", match=MatchText(text=typ)))
#     if not conds:
#         return None
#     return Filter(must=conds)


# def _keyword_boost(question: str, item: Dict[str, Any]) -> float:
#     """
#     Simple textual boost based on name/category/department match.
#     Helps exact-name queries like 'atal awas yojna' hit the right scheme.
#     """
#     q = _norm(question)
#     name = _norm((item.get("name_hi", "") + " " + item.get("name_en", "")))
#     cat = _norm(item.get("category", ""))
#     dept = _norm(item.get("department", ""))

#     boost = 0.0

#     if q and q in name:
#         boost += 0.6

#     q_words = [w for w in q.split() if len(w) > 2]
#     for w in q_words:
#         if w in name or w in cat or w in dept:
#             boost += 0.15

#     return boost


# def search_schemes(
#     question: str,
#     limit: int = 3,
#     page: int = 1,
#     min_score: float = 0.20,
#     category: Optional[str] = None,
#     department: Optional[str] = None,
#     typ: Optional[str] = None,
# ):
#     """
#     Hybrid search for schemes.
#     Returns: (results:list[payload+_score], total:int)
#     """
#     qvec = scheme_embed_model.encode(question).tolist()
#     page = max(page, 1)
#     limit = max(1, min(20, limit))

#     MAX_HITS = 50

#     hits = scheme_qdrant.search(
#         collection_name=SCHEMES_COLLECTION,
#         query_vector=qvec,
#         limit=MAX_HITS,
#         with_payload=True,
#         with_vectors=False,
#         query_filter=_qdrant_filter(category, department, typ),
#     )

#     scored: List[Dict[str, Any]] = []
#     for h in hits:
#         base_score = float(h.score) if hasattr(h, "score") else 0.0
#         if base_score < min_score:
#             continue
#         p = dict(h.payload)
#         kw_boost = _keyword_boost(question, p)
#         final_score = base_score + kw_boost
#         p["_score"] = base_score
#         p["_final_score"] = final_score
#         scored.append(p)

#     # De-duplicate by scheme name
#     deduped: List[Dict[str, Any]] = []
#     seen = set()
#     for p in scored:
#         key = (p.get("name_hi") or p.get("name_en") or "").strip()
#         if not key:
#             key = p.get("id", "")
#         if key in seen:
#             continue
#         seen.add(key)
#         deduped.append(p)

#     deduped.sort(key=lambda x: x.get("_final_score", 0.0), reverse=True)

#     total = len(deduped)
#     start = (page - 1) * limit
#     end = start + limit
#     page_items = deduped[start:end]

#     return page_items, total


# def _fmt_scheme_card(s: Dict[str, Any]) -> str:
#     name = s.get("name_hi") or s.get("name_en") or "—"
#     bits = [
#         f"• **{name}**",
#         f"  - 🎓 पात्रता: {s.get('eligibility','उपलब्ध नहीं')}",
#         f"  - 💰 लाभ: {s.get('benefit','उपलब्ध नहीं')}",
#         f"  - 📝 आवेदन: {s.get('apply_process','उपलब्ध नहीं')}",
#     ]
#     if s.get("apply_link"):
#         bits.append(f"  - 🔗 लिंक: {s['apply_link']}")
#     return "\n".join(bits)


# def build_user_context(user_meta: dict | None) -> str:
#     """Convert user profile info into natural-language context for LLM."""
#     if not user_meta:
#         return ""

#     district = user_meta.get("district")
#     block = user_meta.get("block")
#     village = user_meta.get("village_code")
#     age = user_meta.get("age")
#     gender = user_meta.get("gender")
#     interest = user_meta.get("interest_tag")

#     disability = user_meta.get("disability")
#     occupation = user_meta.get("occupation")
#     income_bracket = user_meta.get("income_bracket")
#     social_category = user_meta.get("social_category")

#     parts = []

#     if district:
#         parts.append(f"जिला {district}")
#     if block:
#         parts.append(f"ब्लॉक {block}")
#     if village:
#         parts.append(f"गाँव कोड {village}")
#     if age:
#         parts.append(f"आयु {age} वर्ष")
#     if gender:
#         parts.append(f"लिंग {gender}")
#     if occupation:
#         parts.append(f"पेशा: {occupation}")
#     if income_bracket:
#         parts.append(f"आय वर्ग: {income_bracket}")
#     if social_category:
#         parts.append(f"सोशल कैटेगरी: {social_category}")
#     if disability and disability.lower() not in ("none", "nahin", "no"):
#         parts.append(f"विशेष आवश्यकताएँ / दिव्यांगता: {disability}")
#     if interest:
#         parts.append(f"रुचि: {interest}")

#     if not parts:
#         return ""

#     return "उपयोगकर्ता की जानकारी: " + ", ".join(parts) + ". "


# def build_schemes_answer(
#     question: str,
#     schemes: List[Dict[str, Any]],
#     user_meta: Dict[str, Any] | None = None,
# ) -> str:
#     """
#     Build Hindi-centric, LLM-generated answer for schemes.
#     Personalised slightly using user_meta (occupation, disability, etc.).
#     """
#     if not schemes:
#         return (
#             "माफ़ कीजिए, इस सवाल से मिलती-जुलती कोई योजना नहीं मिली। "
#             "कृपया अलग शब्दों में पूछें, या ज़िला/विभाग/श्रेणी लिखें।\n\n"
#             "**English:** No strong matches. Try different words or add location/department."
#         )

#     user_ctx = build_user_context(user_meta)

#     q_low = question.lower()
#     want_apply = any(
#         w in q_low
#         for w in [
#             "apply",
#             " आवेदन",
#             "आवेदन",
#             "फॉर्म",
#             "form",
#             "कैसे",
#             "kaise",
#             "कहाँ",
#             "kaha",
#             "कहां",
#         ]
#     )
#     want_benefit = any(
#         w in q_low
#         for w in [
#             "लाभ",
#             "benefit",
#             "paisa",
#             "₹",
#             "kitna",
#             "कितना",
#             "राशि",
#         ]
#     )
#     want_elig = any(
#         w in q_low
#         for w in [
#             "पात्रता",
#             "eligibility",
#             "kaun",
#             "कौन",
#             "किसको",
#             "kis ko",
#             "kisko",
#         ]
#     )

#     if not GROQ_API_KEY:
#         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
#         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
#         eng = (
#             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
#         )
#         return hdr + body + eng

#     context_lines = []
#     for s in schemes:
#         context_lines.append(
#             "योजना: {name}\nविवरण: {desc}\nपात्रता: {elig}\nलाभ: {ben}\nआवेदन प्रक्रिया: {proc}\nविभाग: {dept}\nश्रेणी: {cat}\nलिंक: {link}\n".format(
#                 name=(s.get("name_hi") or s.get("name_en") or ""),
#                 desc=s.get("description_hi", ""),
#                 elig=s.get("eligibility", ""),
#                 ben=s.get("benefit", ""),
#                 proc=s.get("apply_process", ""),
#                 dept=s.get("department", ""),
#                 cat=s.get("category", ""),
#                 link=s.get("apply_link", ""),
#             )
#         )
#     context = "\n---\n".join(context_lines)

#     focus_lines = []
#     if want_apply:
#         focus_lines.append(
#             "- User is mainly asking **how to apply**. "
#             "You MUST explain the पूरा 'आवेदन प्रक्रिया' field step-by-step in simple Hindi. "
#             "हर ज़रूरी स्टेप और हर ज़रूरी दस्तावेज़ का नाम जरूर बताएं।"
#         )
#     if want_benefit:
#         focus_lines.append(
#             "- User is asking about **benefits / amount**. "
#             "Explain the 'लाभ' field completely. अलग-अलग राशि हो तो सब बताएं।"
#         )
#     if want_elig:
#         focus_lines.append(
#             "- User is asking about **eligibility / who can get it**. "
#             "Explain the 'पात्रता' field पूरी तरह, सभी शर्तें (1, 2, 3...) अलग-अलग लिखें।"
#         )

#     focus_text = "\n".join(focus_lines) if focus_lines else "- Follow the general rules below."

#     # 👤 personalisation text
#     profile_text = user_ctx or "कोई अतिरिक्त उपयोगकर्ता जानकारी उपलब्ध नहीं है। अगर जानकारी ना हो तो generic जवाब दें।"

#     prompt = f"""
# You are **Panchayat Sahayika**, a friendly, polite and knowledgeable AI assistant created to help rural citizens of India. 
# Your main goal is to explain information in very **simple, clear, human-like Hindi**, so that even villagers, elderly people, 
# and first-time smartphone users can easily understand.

# User profile (for context, don't repeat fully, just use it smartly in examples):
# {profile_text}

# You must use **only** the information given in the schemes context below. 
# Do NOT invent or guess any benefits, eligibility rules, amounts or links that are not present.

# --------------------------------------------
# 📌 USER QUESTION:
# {question}

# 📌 RELEVANT SCHEMES (if matched):
# {context}
# --------------------------------------------

# ### 🔍 SPECIAL FOCUS (based on the user's question)
# {focus_text}

# ### 🟢 MAIN RULES FOR ANSWERING:
# - Explain in **simple conversational Hindi**, short sentences, and natural flow.  
# - Do NOT sound robotic. Do NOT dump raw data.  
# - Be clear, warm, and practical.
# - **Whenever you write the name of any scheme / yojana, always wrap it like this: `**PM Awas Yojana**`.  
#   यानी हर योजना का नाम hamesha `**` ke andar hona chahiye.**

# Include these only if available in provided context:
# - योज़ना / स्कीम का नाम  
# - यह किसके लिए है (पात्रता)  
# - कितना लाभ मिलता है (लाभ)  
# - कैसे और कहाँ आवेदन करना है (आवेदन प्रक्रिया)  
# - लिंक हो तो बताएं  

# If multiple schemes match, explain **2–3** clearly but naturally.
# Missing data → write “उपलब्ध नहीं” naturally.

# ### 🟡 ALWAYS END WITH:
# "अगर ज़रूरत हो तो अपने ग्राम पंचायत या CSC केंद्र से मदद लें।"

# ### 🌍 AFTER THE HINDI ANSWER:
# Give **one short English summary sentence** (not detailed).

# --------------------------------------------
# Now write the final answer in a natural, fluent, friendly tone.
# --------------------------------------------
# """

#     try:
#         completion = groq_client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2,
#         )
#         ai_answer = completion.choices[0].message.content.strip()
#     except Exception:
#         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
#         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
#         eng = (
#             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
#         )
#         return hdr + body + eng

#     return ai_answer


# def _should_use_schemes(question: str, schemes: List[Dict[str, Any]]) -> bool:
#     """
#     Decide kare ki is query ke liye schemes pipeline use karni hai ya nahi।
#     """
#     if not schemes:
#         return False

#     top = schemes[0]
#     top_final = float(top.get("_final_score", top.get("_score", 0.0)) or 0.0)

#     q = question.lower()
#     has_scheme_word = any(
#         w in q
#         for w in [
#             "योजना",
#             "yojana",
#             "scheme",
#             "स्कीम",
#             "pension",
#             "पेंशन",
#             "subsidy",
#             "सब्सिडी",
#             "बीमा",
#             "insurance",
#             "scholarship",
#             " छात्रवृत्ति",
#         ]
#     )

#     if top_final >= 0.60:
#         return True

#     if has_scheme_word and top_final >= 0.25:
#         return True

#     return False

# # ================== MODELS FOR JSON /ask ==================


# class AskRequest(BaseModel):
#     question: str
#     ui_lang: str = "hi"        # "hi" | "garhwali" | "en"
#     mode: str = "auto"         # "auto" | "docs" | "schemes"
#     history: List[Dict[str, str]] = []
#     user_meta: Dict[str, Any] | None = None


# class AskResponse(BaseModel):
#     response: str
#     sources: List[Dict[str, Any]] = []


# class SchemeCard(SQLModel):
#     title: str
#     subtitle: Optional[str] = None
#     verified: bool = True
#     badges: List[str] = []
#     apply_url: Optional[str] = None
#     read_more_url: Optional[str] = None

# # ================== PERSONALISED RECOMMENDATIONS API ==================


# @app.get("/user/recommended-schemes", response_model=List[SchemeCard])
# def recommended_schemes(current_user: User = Depends(get_current_user)):
#     # Build simple query text from profile
#     parts = []

#     if current_user.district:
#         parts.append(current_user.district)
#     if current_user.block:
#         parts.append(current_user.block)
#     if current_user.gender:
#         parts.append(current_user.gender)
#     if current_user.age:
#         parts.append(f"age {current_user.age}")
#     if current_user.interest_tag:
#         parts.append(current_user.interest_tag)

#     # Strong signals
#     if current_user.occupation:
#         parts.append(current_user.occupation)
#     if current_user.disability and current_user.disability.lower() not in (
#         "none",
#         "nahin",
#         "no",
#     ):
#         parts.append("divyang")
#         parts.append(current_user.disability)
#     if current_user.income_bracket:
#         parts.append(current_user.income_bracket)
#     if current_user.social_category:
#         parts.append(current_user.social_category)

#     question = " ".join(parts) or "gramin yojana"

#     schemes, _total = search_schemes(
#         question=question,
#         limit=5,
#         page=1,
#         min_score=0.20,
#         category=None,
#         department=None,
#         typ=None,
#     )

#     cards: List[SchemeCard] = []
#     for s in schemes:
#         title = (
#             (s.get("name_hi") or "")
#             + (" / " + s.get("name_en", "") if s.get("name_en") else "")
#         ).strip(" /")
#         subtitle = s.get("description_hi") or s.get("description_en") or ""
#         badges = [s.get("department", ""), s.get("category", "")]
#         cards.append(
#             SchemeCard(
#                 title=title or "Yojana",
#                 subtitle=subtitle,
#                 verified=True,
#                 badges=[b for b in badges if b],
#                 apply_url=s.get("apply_link") or None,
#                 read_more_url=s.get("source_url") or None,
#             )
#         )
#     return cards

# # ================== ROUTES (HTML DEMO) ==================


# @app.get("/", response_class=HTMLResponse)
# async def get_home(
#     request: Request,
#     lang: str = "hi",      # ui_lang
#     mode: str = "docs",    # "docs" or "schemes"
# ):
#     # allow hi / en / garhwali in demo
#     if lang not in ("hi", "en", "garhwali"):
#         lang = "hi"
#     if mode not in ("docs", "schemes"):
#         mode = "docs"

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "messages": [],
#             "history_json": "[]",
#             "lang": lang,
#             "mode": mode,
#         },
#     )


# @app.post("/", response_class=HTMLResponse)
# async def post_query(
#     request: Request,
#     query: str = Form(...),
#     history_json: str = Form("[]"),
#     ui_lang: str = Form("hi"),   # "hi" | "garhwali" | "en"
#     mode: str = Form("docs"),    # "docs" or "schemes"
# ):
#     try:
#         history = json.loads(history_json)
#     except Exception:
#         history = []

#     # Decide target language for demo HTML
#     if ui_lang == "en":
#         target_lang = "en"
#     elif ui_lang == "garhwali":
#         target_lang = "garhwali"
#     else:
#         # "hi" / default → Hindi or Hinglish based on script
#         target_lang = "hi" if contains_devanagari(query) else "hinglish"

#     if mode == "schemes":
#         schemes, _total = search_schemes(
#             question=query,
#             limit=3,
#             page=1,
#             min_score=0.20,
#             category=None,
#             department=None,
#             typ=None,
#         )
#         base_answer = build_schemes_answer(query, schemes)
#     else:
#         base_answer, _sources = generate_docs_answer_raw(query, history)

#     final_text = translate_answer(base_answer, target_lang)
#     answer_html = _convert_markdown_bold_to_html(final_text)

#     history.append({"role": "user", "content": query})
#     history.append({"role": "assistant", "content": answer_html})

#     messages = [{"role": h["role"], "content": h["content"]} for h in history]

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "messages": messages,
#             "history_json": json.dumps(history, ensure_ascii=False),
#             "lang": ui_lang,
#             "mode": mode,
#         },
#     )

# # ================== CORE ASK LOGIC (shared) ==================


# def process_ask_request(req: AskRequest) -> AskResponse:
#     # Decide final language for UI
#     if req.ui_lang == "en":
#         target_lang = "en"
#     elif req.ui_lang == "garhwali":
#         target_lang = "garhwali"
#     else:
#         # "hi" / default → Hindi or Hinglish based on script
#         target_lang = "hi" if contains_devanagari(req.question) else "hinglish"

#     user_meta = req.user_meta or None

#     schemes: List[Dict[str, Any]] = []
#     doc_sources: List[Dict[str, Any]] = []
#     use_schemes = False

#     if req.mode in ("schemes", "auto"):
#         schemes, total = search_schemes(
#             question=req.question,
#             limit=5,
#             page=1,
#             min_score=0.20,
#             category=None,
#             department=None,
#             typ=None,
#         )
#         if req.mode == "schemes":
#             use_schemes = True
#         else:
#             use_schemes = _should_use_schemes(req.question, schemes)

#     if use_schemes:
#         base_answer = build_schemes_answer(req.question, schemes, user_meta=user_meta)
#         sources = [
#             {
#                 "name_hi": s.get("name_hi"),
#                 "name_en": s.get("name_en"),
#                 "score": s.get("_score"),
#                 "department": s.get("department"),
#                 "category": s.get("category"),
#                 "apply_link": s.get("apply_link"),
#             }
#             for s in schemes
#         ]
#     else:
#         base_answer, doc_sources = generate_docs_answer_raw(
#             req.question,
#             req.history,
#             user_meta=user_meta,
#         )
#         sources = doc_sources

#     final_text = translate_answer(base_answer, target_lang)
#     final_html = _convert_markdown_bold_to_html(final_text)

#     return AskResponse(response=final_html, sources=sources)

# # ================== JSON API FOR REACT CHAT ==================


# @app.post("/ask", response_model=AskResponse)
# def ask(req: AskRequest):
#     """
#     Text chat endpoint (used by React ChatScreen).
#     """
#     return process_ask_request(req)


# @app.post("/voice/ask")
# async def voice_ask(
#     audio: UploadFile = File(...),
#     mode: str = "auto",
#     ui_lang: str = "garhwali",
# ):
#     """
#     Voice chat endpoint:
#     1. Take uploaded audio (Garhwali / Hindi speech)
#     2. Transcribe with Whisper
#     3. Run normal ask pipeline with ui_lang=garhwali (by default)
#     4. Convert answer text to TTS mp3
#     5. Return: transcribed_question, text_answer_html, audio_url, sources
#     """
#     # ---- Save temp audio ----
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
#         shutil.copyfileobj(audio.file, tmp)
#         tmp_path = tmp.name

#     try:
#         # ---- STT: audio -> text ----
#         question_text = transcribe_garhwali_audio(tmp_path)

#         # ---- Build AskRequest ----
#         req = AskRequest(
#             question=question_text,
#             ui_lang=ui_lang,
#             mode=mode,
#             history=[],
#             user_meta=None,
#         )

#         ask_resp = process_ask_request(req)
#         answer_html = ask_resp.response

#         # HTML se plain text nikal lo for TTS
#         answer_plain = re.sub("<[^<]+?>", "", answer_html)

#         audio_filename = tts_garhwali(answer_plain)
#         audio_url = f"/tts/{audio_filename}"

#         return {
#             "question_text": question_text,
#             "answer_html": answer_html,
#             "audio_url": audio_url,
#             "sources": ask_resp.sources,
#         }

#     finally:
#         try:
#             os.remove(tmp_path)
#         except Exception:
#             pass

# # ================== AUTH ROUTES ==================


# @app.post("/auth/register", response_model=UserRead)
# def register(user_in: UserCreate, session: Session = Depends(get_session)):
#     existing = get_user_by_username(session, user_in.username)
#     if existing:
#         raise HTTPException(status_code=400, detail="Username already registered")

#     user = User(
#         username=user_in.username,
#         full_name=user_in.full_name,
#         hashed_password=get_password_hash(user_in.password),
#         district=user_in.district,
#         block=user_in.block,
#         village_code=user_in.village_code,
#         age=user_in.age,
#         gender=user_in.gender,
#         interest_tag=user_in.interest_tag,
#         disability=user_in.disability,
#         occupation=user_in.occupation,
#         income_bracket=user_in.income_bracket,
#         social_category=user_in.social_category,
#     )
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user


# @app.post("/auth/login", response_model=Token)
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     session: Session = Depends(get_session),
# ):
#     user = get_user_by_username(session, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     token = create_access_token({"sub": user.username})
#     return Token(access_token=token)


# @app.get("/me", response_model=UserRead)
# def read_me(current_user: User = Depends(get_current_user)):
#     return current_user


# @app.put("/me", response_model=UserRead)
# def update_me(
#     user_update: UserUpdate,
#     current_user: User = Depends(get_current_user),
#     session: Session = Depends(get_session),
# ):
#     data = user_update.dict(exclude_unset=True)

#     for field, value in data.items():
#         setattr(current_user, field, value)

#     session.add(current_user)
#     session.commit()
#     session.refresh(current_user)
#     return current_user


# @app.get("/health")
# def health():
#     return {
#         "status": "ok",
#         "docs_collection": DOC_COLLECTION,
#         "schemes_collection": SCHEMES_COLLECTION,
#         "embed_model_schemes": EMBED_MODEL_NAME_SCHEMES,
#     }











# import os
# import json
# import uuid
# import re
# import unicodedata
# import tempfile
# import shutil
# from pathlib import Path
# from typing import List, Dict, Any, Optional, Tuple

# from dotenv import load_dotenv
# from fastapi import (
#     FastAPI,
#     Request,
#     Form,
#     Depends,
#     HTTPException,
#     status,
#     UploadFile,
#     File,
# )
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# from pydantic import BaseModel

# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchText,
# )
# from qdrant_client.http import models as qm  # noqa: F401  (kept if later needed)

# from sentence_transformers import SentenceTransformer
# from fastembed import TextEmbedding
# from groq import Groq
# from googletrans import Translator  # Google Translate

# from faster_whisper import WhisperModel
# from gtts import gTTS

# from sqlmodel import Field, SQLModel, Session, create_engine, select
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# # ================== CONFIG ==================

# BASE_DIR = Path(__file__).resolve().parent.parent  # repo root (panchayat-sahayika)

# # Schemes JSON path
# SCHEMES_PATH = BASE_DIR / "samaj_kalyan_vibhag_clean_typed.json"
# # or, if in public:
# # SCHEMES_PATH = BASE_DIR / "public" / "samaj_kalyan_vibhag_clean_typed.json"

# # TTS output directory
# TTS_OUTPUT_DIR = BASE_DIR / "tts_output"
# TTS_OUTPUT_DIR.mkdir(exist_ok=True)

# load_dotenv()

# # ---- Groq / LLM ----
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise RuntimeError("GROQ_API_KEY missing in .env")

# LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
# GROQ_MODEL_DOCS = os.getenv("GROQ_MODEL", LLM_MODEL)

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---- DOCS RAG Qdrant (remote or local) ----
# DOC_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# DOC_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
# DOC_COLLECTION = os.getenv("COLLECTION_NAME", "panchayat_uk_docs")

# doc_qclient = QdrantClient(url=DOC_QDRANT_URL, api_key=DOC_QDRANT_API_KEY)
# doc_embedder = TextEmbedding()

# # ---- Schemes Qdrant (local embedded) ----
# EMBED_MODEL_NAME_SCHEMES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# SCHEMES_COLLECTION = "samaj_kalyan_vibhag_schemes"

# scheme_embed_model = SentenceTransformer(EMBED_MODEL_NAME_SCHEMES)
# scheme_qdrant = QdrantClient(path=str(BASE_DIR / "qdrant_data"))

# # ---- Voice models (Whisper STT) ----
# WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "medium")
# USE_CUDA = os.getenv("USE_CUDA", "0") == "1"

# whisper_model = WhisperModel(
#     WHISPER_MODEL_NAME,
#     device="cuda" if USE_CUDA else "cpu",
#     compute_type="float16" if USE_CUDA else "int8",
# )

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

# # ---- FastAPI + Templates ----
# app = FastAPI(title="Panchayat Sahayika Unified Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )

# # static mount for TTS files
# app.mount("/tts", StaticFiles(directory=str(TTS_OUTPUT_DIR)), name="tts")

# templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# translator = Translator()  # Google translator instance

# # ================== AUTH / USERS ==================

# DATABASE_URL = "sqlite:///./panchayat_users.db"  # SQLite file in backend folder
# engine = create_engine(DATABASE_URL, echo=False)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# SECRET_KEY = os.getenv(
#     "SECRET_KEY",
#     "baea29ce56f4b02733883b6ae1a76265988d123d5ad3e9d2214dae4646a81ee6",
# )
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str = Field(index=True, unique=True)
#     full_name: Optional[str] = None
#     hashed_password: str

#     # profile info (for recommendations / chatbot)
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None          # "M"/"F"/"O" or free text
#     interest_tag: Optional[str] = None    # "farmer", "student", etc.

#     disability: Optional[str] = None      # e.g. "none", "locomotor", "visual", etc.
#     occupation: Optional[str] = None      # "farmer", "student", "ASHA", "SHG member"...
#     income_bracket: Optional[str] = None  # "BPL", "APL", etc.
#     social_category: Optional[str] = None # "SC", "ST", "OBC", "General", etc.


# class UserCreate(SQLModel):
#     username: str
#     password: str
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserRead(SQLModel):
#     id: int
#     username: str
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserUpdate(SQLModel):
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class Token(SQLModel):
#     access_token: str
#     token_type: str = "bearer"


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# def _bcrypt_safe(password: str) -> str:
#     """
#     Bcrypt only uses first 72 bytes of the password.
#     To avoid errors, we explicitly cut to 72 bytes.
#     """
#     if password is None:
#         return ""
#     pw_bytes = password.encode("utf-8")
#     return pw_bytes[:72].decode("utf-8", errors="ignore")


# def get_password_hash(password: str) -> str:
#     safe_pw = _bcrypt_safe(password)
#     return pwd_context.hash(safe_pw)


# def verify_password(plain: str, hashed: str) -> bool:
#     safe_pw = _bcrypt_safe(plain)
#     return pwd_context.verify(safe_pw, hashed)


# def create_access_token(data: dict) -> str:
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# def get_user_by_username(session: Session, username: str) -> Optional[User]:
#     stmt = select(User).where(User.username == username)
#     return session.exec(stmt).first()


# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     session: Session = Depends(get_session),
# ) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: Optional[str] = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = get_user_by_username(session, username=username)
#     if not user:
#         raise credentials_exception
#     return user


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

# # ================== COMMON LANGUAGE + VOICE HELPERS ==================


# def contains_devanagari(text: str) -> bool:
#     """Check if text has any Devanagari characters."""
#     for ch in text:
#         if "\u0900" <= ch <= "\u097F":
#             return True
#     return False


# def _llm_translate(text: str, target_desc: str) -> str:
#     """
#     Generic translator using Groq LLM.
#     `target_desc` = description of target language/style.
#     """
#     system_msg = (
#         "You are a translator for Gram Panchayat content.\n"
#         "You ONLY translate the text; you do not add explanations.\n"
#         "Preserve markdown bold markers **like this** exactly as they are.\n"
#         "Do not change the meaning; only change the language.\n"
#     )

#     user_msg = (
#         f"Translate the following text into {target_desc}\n\n"
#         f"Text:\n{text}"
#     )

#     completion = groq_client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "system", "content": system_msg},
#             {"role": "user", "content": user_msg},
#         ],
#         temperature=0.2,
#         max_tokens=1200,
#     )
#     out = completion.choices[0].message.content or text
#     return out


# def translate_answer(text: str, target_lang: str) -> str:
#     """
#     Final step translation:

#     target_lang:
#       - 'en'        -> English
#       - 'hi'        -> simple Hindi (Devanagari)
#       - 'garhwali'  -> simple Garhwali (Devanagari)
#       - 'hinglish'  -> simple Hinglish (Roman Hindi)
#     """

#     # ---------- 1) English UI ----------
#     if target_lang == "en":
#         try:
#             res = translator.translate(text, dest="en")
#             out = res.text
#             if out and not contains_devanagari(out) and out.strip() != "":
#                 return out
#         except Exception:
#             pass

#         return _llm_translate(
#             text,
#             "clear, simple English suitable for village-level users. "
#             "Avoid Hindi script and use plain English sentences.",
#         )

#     # ---------- 2) Hindi (Devanagari) ----------
#     if target_lang == "hi":
#         return _llm_translate(
#             text,
#             "very simple Hindi in Devanagari script, using everyday words "
#             "that village-level users understand.",
#         )

#     # ---------- 3) Garhwali (Devanagari) ----------
#     if target_lang == "garhwali":
#         return _llm_translate(
#             text,
#             (
#                 "Translate into PURE Garhwali language (Central Garhwal dialect), "
#                 "written in Devanagari script.\n\n"
#                 "STRICT RULES:\n"
#                 "- Every sentence MUST be in natural Garhwali, NOT standard Hindi.\n"
#                 "- Avoid Hindi forms: 'आप', 'कैसे', 'करना', 'है', 'होगा' etc.\n"
#                 "- Use Garhwali forms: 'त्यूँ', 'कसि', 'च', 'जा', 'रै', 'ल्यो', 'णै' etc.\n"
#                 "- Make sentences exactly like villagers speak at home.\n"
#                 "- Government scheme names must stay exactly as in Hindi.\n"
#             ),
#         )

#     # ---------- 4) Hinglish (Roman Hindi) ----------
#     return _llm_translate(
#         text,
#         "very simple Hinglish (Roman Hindi using English letters). "
#         "Do NOT use Devanagari characters.",
#     )


# def _convert_markdown_bold_to_html(text: str) -> str:
#     """**bold** -> <strong>bold</strong> for UI."""
#     return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


# def transcribe_garhwali_audio(path: str) -> str:
#     """
#     Whisper se Garhwali/Hindi transcription.
#     Hum language="hi" hint dete hain, taaki model Hindi script me likhe.
#     Speaker Garhwali bolega, text mostly Hindi/near-Garhwali me aa jayega.
#     """
#     segments, info = whisper_model.transcribe(
#         path,
#         language="hi",
#         task="transcribe",
#         vad_filter=True,
#     )
#     pieces = [seg.text.strip() for seg in segments if seg.text.strip()]
#     text = " ".join(pieces).strip()
#     return text


# def tts_garhwali(text: str) -> str:
#     """
#     Garhwali text (Devanagari) ko Hindi TTS se bolwate hain.
#     Returns: relative filename inside TTS_OUTPUT_DIR.
#     """
#     safe_text = text.strip()
#     if len(safe_text) > 1500:
#         safe_text = safe_text[:1500]

#     filename = f"garhwali_{uuid.uuid4().hex}.mp3"
#     out_path = TTS_OUTPUT_DIR / filename

#     tts = gTTS(text=safe_text, lang="hi")
#     tts.save(str(out_path))

#     return filename

# # ================== DOCS RAG PIPELINE ==================


# def build_docs_system_prompt() -> str:
#     """
#     System prompt for docs:
#     - Sirf Qdrant se aaye context ka use karo
#     - Gram Panchayat users ke liye simple Hindi
#     - Users can ask in Hindi, Hinglish, or Garhwali.
#     """
#     return (
#         "आप 'Panchayat Sahayika' हैं, उत्तराखंड की ग्राम पंचायतों के लिए सहायक।\n"
#         "यूज़र कभी-कभी गढ़वाली या हिंग्लिश में भी सवाल पूछ सकते हैं; "
#         "आप अर्थ समझकर पहले सरल हिन्दी में जवाब तैयार करें।\n"
#         "आपको केवल नीचे दिए गए संदर्भ (official Panchayati Raj documents: acts, rules, "
#         "guidelines, roles, schemes, training material) का इस्तेमाल करके ही जवाब देना है।\n\n"
#         "भाषा बहुत ही सरल और आसान हिन्दी होनी चाहिए ताकि सरपंच, वार्ड मेंबर और ग्राम पंचायत "
#         "कर्मचारी आसानी से समझ सकें।\n"
#         "कानूनी भारी शब्दों से बचें।\n"
#         "अगर ज़रूरी जानकारी संदर्भ में नहीं है, तो साफ-साफ लिखें कि यह जानकारी उपलब्ध नहीं है "
#         "और आप अंदाज़ा नहीं लगा रहे हैं।\n"
#         "कभी भी दस्तावेज़ का नाम, फाइल का नाम, पेज नंबर या 'source' list का ज़िक्र न करें।\n"
#     )


# def retrieve_docs_context(query: str, top_k: int = 8) -> List[Dict[str, Any]]:
#     query_vec = list(doc_embedder.embed([query]))[0]
#     results = doc_qclient.search(
#         collection_name=DOC_COLLECTION,
#         query_vector=query_vec,
#         limit=top_k,
#         with_payload=True,
#     )

#     contexts = []
#     for r in results:
#         pl = r.payload or {}
#         contexts.append(
#             {
#                 "text": pl.get("text", ""),
#                 "source_file": pl.get("source_file", ""),
#                 "page": pl.get("page", ""),
#                 "url": pl.get("url", ""),
#                 "score": r.score,
#             }
#         )
#     return contexts


# def generate_docs_answer_raw(
#     query: str,
#     history: List[Dict[str, str]],
#     user_meta: Dict[str, Any] | None = None,
# ) -> Tuple[str, List[Dict[str, Any]]]:
#     """
#     Returns raw answer in Hindi-ish language (LLM decides, but system prompt nudges to Hindi).
#     We will later translate to final UI language using translate_answer().
#     """
#     contexts = retrieve_docs_context(query)

#     context_block = "\n\n---\n\n".join(c["text"] for c in contexts if c["text"])

#     # 👤 personalise a bit
#     user_ctx = build_user_context(user_meta)

#     system_prompt = build_docs_system_prompt()
#     if user_ctx:
#         system_prompt += (
#             "\n\nउपयोगकर्ता प्रोफाइल (उदाहरणों को practical banane ke liye):\n"
#             f"{user_ctx}\n"
#             "जवाब में आप user ki स्थिति ke हिसाब से छोटा सा context de sakte hain "
#             "(jaise किसान, छात्र, दिव्यांग इत्यादि)."
#         )

#     messages = [
#         {"role": "system", "content": system_prompt},
#     ]

#     # include a few last turns from history (server-side only)
#     for h in history[-4:] if history else []:
#         messages.append({"role": h["role"], "content": h["content"]})

#     messages.append(
#         {
#             "role": "user",
#             "content": (
#                 f"प्रश्न: {query}\n\n"
#                 f"नीचे दिए गए दस्तावेज़ों के संदर्भ का उपयोग करके उत्तर दीजिए। "
#                 f"अपने उत्तर में इन दस्तावेज़ों के नाम या पेज नंबर का ज़िक्र मत कीजिए:\n\n"
#                 f"{context_block}"
#             ),
#         }
#     )

#     completion = groq_client.chat.completions.create(
#         model=GROQ_MODEL_DOCS,
#         messages=messages,
#         temperature=0.3,
#         max_tokens=900,
#     )
#     raw_answer = completion.choices[0].message.content or ""

#     # dedupe sources
#     unique_sources = []
#     seen = set()
#     for c in contexts:
#         key = (c["source_file"], c["page"])
#         if key not in seen and c["source_file"]:
#             seen.add(key)
#             unique_sources.append(
#                 {
#                     "source_file": c["source_file"],
#                     "page": c["page"],
#                     "url": c["url"],
#                 }
#             )

#     return raw_answer, unique_sources

# # ================== SCHEMES PIPELINE ==================


# def load_schemes() -> List[Dict[str, Any]]:
#     with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     # ensure strings and minimal keys exist
#     for s in data:
#         s.setdefault("name_hi", "")
#         s.setdefault("name_en", "")
#         s.setdefault("category", "")
#         s.setdefault("department", "")
#         s.setdefault("description_hi", "")
#         s.setdefault("description_en", "")
#         s.setdefault("eligibility", "")
#         s.setdefault("benefit", "")
#         s.setdefault("apply_process", "")
#         s.setdefault("apply_link", "")
#         s.setdefault("source_url", "")
#         s.setdefault("type", s.get("type", "scheme"))
#     return data


# def _concat_item_text(s: Dict[str, Any]) -> str:
#     """
#     Text used for vector embedding.
#     We heavily weight the scheme name so that exact-name queries hit correctly.
#     """
#     name = (s.get("name_hi", "") + " " + s.get("name_en", "")).strip()
#     other_parts = [
#         s.get("category", ""),
#         s.get("department", ""),
#         s.get("description_hi", ""),
#         s.get("description_en", ""),
#         s.get("eligibility", ""),
#         s.get("benefit", ""),
#         s.get("apply_process", ""),
#     ]

#     # Repeat name 5x → boosts similarity when user types scheme name
#     weighted_name = " ".join([name] * 5) if name else ""
#     rest = " | ".join([str(p) for p in other_parts if p])

#     return " | ".join([p for p in [weighted_name, rest] if p])


# def init_schemes_collection():
#     schemes = load_schemes()

#     scheme_qdrant.recreate_collection(
#         collection_name=SCHEMES_COLLECTION,
#         vectors_config=VectorParams(
#             size=scheme_embed_model.get_sentence_embedding_dimension(),
#             distance=Distance.COSINE,
#         ),
#     )

#     points: List[PointStruct] = []
#     for s in schemes:
#         vec = scheme_embed_model.encode(_concat_item_text(s)).tolist()
#         payload = dict(s)
#         payload["__search_blob"] = _concat_item_text(s)
#         points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload))

#     scheme_qdrant.upsert(SCHEMES_COLLECTION, points)
#     print(f"✅ Indexed {len(points)} schemes into Qdrant (schemes collection)")


# # Build index at import time
# init_schemes_collection()


# def _norm(s: str) -> str:
#     if not s:
#         return ""
#     s = unicodedata.normalize("NFKC", s)
#     s = re.sub(r"\s+", " ", s).strip().lower()
#     return s


# def _qdrant_filter(
#     category: Optional[str],
#     department: Optional[str],
#     typ: Optional[str],
# ) -> Optional[Filter]:
#     conds = []
#     if category:
#         conds.append(FieldCondition(key="category", match=MatchText(text=category)))
#     if department:
#         conds.append(FieldCondition(key="department", match=MatchText(text=department)))
#     if typ:
#         conds.append(FieldCondition(key="type", match=MatchText(text=typ)))
#     if not conds:
#         return None
#     return Filter(must=conds)


# def _keyword_boost(question: str, item: Dict[str, Any]) -> float:
#     """
#     Simple textual boost based on name/category/department match.
#     Helps exact-name queries like 'atal awas yojna' hit the right scheme.
#     """
#     q = _norm(question)
#     name = _norm((item.get("name_hi", "") + " " + item.get("name_en", "")))
#     cat = _norm(item.get("category", ""))
#     dept = _norm(item.get("department", ""))

#     boost = 0.0

#     if q and q in name:
#         boost += 0.6

#     q_words = [w for w in q.split() if len(w) > 2]
#     for w in q_words:
#         if w in name or w in cat or w in dept:
#             boost += 0.15

#     return boost


# def search_schemes(
#     question: str,
#     limit: int = 3,
#     page: int = 1,
#     min_score: float = 0.20,
#     category: Optional[str] = None,
#     department: Optional[str] = None,
#     typ: Optional[str] = None,
# ):
#     """
#     Hybrid search for schemes.
#     Returns: (results:list[payload+_score], total:int)
#     """
#     qvec = scheme_embed_model.encode(question).tolist()
#     page = max(page, 1)
#     limit = max(1, min(20, limit))

#     MAX_HITS = 50

#     hits = scheme_qdrant.search(
#         collection_name=SCHEMES_COLLECTION,
#         query_vector=qvec,
#         limit=MAX_HITS,
#         with_payload=True,
#         with_vectors=False,
#         query_filter=_qdrant_filter(category, department, typ),
#     )

#     scored: List[Dict[str, Any]] = []
#     for h in hits:
#         base_score = float(h.score) if hasattr(h, "score") else 0.0
#         if base_score < min_score:
#             continue
#         p = dict(h.payload)
#         kw_boost = _keyword_boost(question, p)
#         final_score = base_score + kw_boost
#         p["_score"] = base_score
#         p["_final_score"] = final_score
#         scored.append(p)

#     # De-duplicate by scheme name
#     deduped: List[Dict[str, Any]] = []
#     seen = set()
#     for p in scored:
#         key = (p.get("name_hi") or p.get("name_en") or "").strip()
#         if not key:
#             key = p.get("id", "")
#         if key in seen:
#             continue
#         seen.add(key)
#         deduped.append(p)

#     deduped.sort(key=lambda x: x.get("_final_score", 0.0), reverse=True)

#     total = len(deduped)
#     start = (page - 1) * limit
#     end = start + limit
#     page_items = deduped[start:end]

#     return page_items, total


# def _fmt_scheme_card(s: Dict[str, Any]) -> str:
#     name = s.get("name_hi") or s.get("name_en") or "—"
#     bits = [
#         f"• **{name}**",
#         f"  - 🎓 पात्रता: {s.get('eligibility','उपलब्ध नहीं')}",
#         f"  - 💰 लाभ: {s.get('benefit','उपलब्ध नहीं')}",
#         f"  - 📝 आवेदन: {s.get('apply_process','उपलब्ध नहीं')}",
#     ]
#     if s.get("apply_link"):
#         bits.append(f"  - 🔗 लिंक: {s['apply_link']}")
#     return "\n".join(bits)


# def build_user_context(user_meta: dict | None) -> str:
#     """Convert user profile info into natural-language context for LLM."""
#     if not user_meta:
#         return ""

#     district = user_meta.get("district")
#     block = user_meta.get("block")
#     village = user_meta.get("village_code")
#     age = user_meta.get("age")
#     gender = user_meta.get("gender")
#     interest = user_meta.get("interest_tag")

#     disability = user_meta.get("disability")
#     occupation = user_meta.get("occupation")
#     income_bracket = user_meta.get("income_bracket")
#     social_category = user_meta.get("social_category")

#     parts = []

#     if district:
#         parts.append(f"जिला {district}")
#     if block:
#         parts.append(f"ब्लॉक {block}")
#     if village:
#         parts.append(f"गाँव कोड {village}")
#     if age:
#         parts.append(f"आयु {age} वर्ष")
#     if gender:
#         parts.append(f"लिंग {gender}")
#     if occupation:
#         parts.append(f"पेशा: {occupation}")
#     if income_bracket:
#         parts.append(f"आय वर्ग: {income_bracket}")
#     if social_category:
#         parts.append(f"सोशल कैटेगरी: {social_category}")
#     if disability and disability.lower() not in ("none", "nahin", "no"):
#         parts.append(f"विशेष आवश्यकताएँ / दिव्यांगता: {disability}")
#     if interest:
#         parts.append(f"रुचि: {interest}")

#     if not parts:
#         return ""

#     return "उपयोगकर्ता की जानकारी: " + ", ".join(parts) + ". "


# def build_schemes_answer(
#     question: str,
#     schemes: List[Dict[str, Any]],
#     user_meta: Dict[str, Any] | None = None,
# ) -> str:
#     """
#     Build Hindi-centric, LLM-generated answer for schemes.
#     Personalised slightly using user_meta (occupation, disability, etc.).
#     """
#     if not schemes:
#         return (
#             "माफ़ कीजिए, इस सवाल से मिलती-जुलती कोई योजना नहीं मिली। "
#             "कृपया अलग शब्दों में पूछें, या ज़िला/विभाग/श्रेणी लिखें।\n\n"
#             "**English:** No strong matches. Try different words or add location/department."
#         )

#     user_ctx = build_user_context(user_meta)

#     q_low = question.lower()
#     want_apply = any(
#         w in q_low
#         for w in [
#             "apply",
#             " आवेदन",
#             "आवेदन",
#             "फॉर्म",
#             "form",
#             "कैसे",
#             "kaise",
#             "कहाँ",
#             "kaha",
#             "कहां",
#         ]
#     )
#     want_benefit = any(
#         w in q_low
#         for w in [
#             "लाभ",
#             "benefit",
#             "paisa",
#             "₹",
#             "kitna",
#             "कितना",
#             "राशि",
#         ]
#     )
#     want_elig = any(
#         w in q_low
#         for w in [
#             "पात्रता",
#             "eligibility",
#             "kaun",
#             "कौन",
#             "किसको",
#             "kis ko",
#             "kisko",
#         ]
#     )

#     if not GROQ_API_KEY:
#         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
#         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
#         eng = (
#             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
#         )
#         return hdr + body + eng

#     context_lines = []
#     for s in schemes:
#         context_lines.append(
#             "योजना: {name}\nविवरण: {desc}\nपात्रता: {elig}\nलाभ: {ben}\nआवेदन प्रक्रिया: {proc}\nविभाग: {dept}\nश्रेणी: {cat}\nलिंक: {link}\n".format(
#                 name=(s.get("name_hi") or s.get("name_en") or ""),
#                 desc=s.get("description_hi", ""),
#                 elig=s.get("eligibility", ""),
#                 ben=s.get("benefit", ""),
#                 proc=s.get("apply_process", ""),
#                 dept=s.get("department", ""),
#                 cat=s.get("category", ""),
#                 link=s.get("apply_link", ""),
#             )
#         )
#     context = "\n---\n".join(context_lines)

#     focus_lines = []
#     if want_apply:
#         focus_lines.append(
#             "- User is mainly asking **how to apply**. "
#             "You MUST explain the पूरा 'आवेदन प्रक्रिया' field step-by-step in simple Hindi. "
#             "हर ज़रूरी स्टेप और हर ज़रूरी दस्तावेज़ का नाम जरूर बताएं।"
#         )
#     if want_benefit:
#         focus_lines.append(
#             "- User is asking about **benefits / amount**. "
#             "Explain the 'लाभ' field completely. अलग-अलग राशि हो तो सब बताएं।"
#         )
#     if want_elig:
#         focus_lines.append(
#             "- User is asking about **eligibility / who can get it**. "
#             "Explain the 'पात्रता' field पूरी तरह, सभी शर्तें (1, 2, 3...) अलग-अलग लिखें।"
#         )

#     focus_text = "\n".join(focus_lines) if focus_lines else "- Follow the general rules below."

#     # 👤 personalisation text
#     profile_text = user_ctx or "कोई अतिरिक्त उपयोगकर्ता जानकारी उपलब्ध नहीं है। अगर जानकारी ना हो तो generic जवाब दें।"

#     prompt = f"""
# You are **Panchayat Sahayika**, a friendly, polite and knowledgeable AI assistant created to help rural citizens of India. 
# Your main goal is to explain information in very **simple, clear, human-like Hindi**, so that even villagers, elderly people, 
# and first-time smartphone users can easily understand.

# User profile (for context, don't repeat fully, just use it smartly in examples):
# {profile_text}

# You must use **only** the information given in the schemes context below. 
# Do NOT invent or guess any benefits, eligibility rules, amounts or links that are not present.

# --------------------------------------------
# 📌 USER QUESTION:
# {question}

# 📌 RELEVANT SCHEMES (if matched):
# {context}
# --------------------------------------------

# ### 🔍 SPECIAL FOCUS (based on the user's question)
# {focus_text}

# ### 🟢 MAIN RULES FOR ANSWERING:
# - Explain in **simple conversational Hindi**, short sentences, and natural flow.  
# - Do NOT sound robotic. Do NOT dump raw data.  
# - Be clear, warm, and practical.
# - **Whenever you write the name of any scheme / yojana, always wrap it like this: `**PM Awas Yojana**`.  
#   यानी हर योजना का नाम hamesha `**` ke andar hona chahiye.**

# Include these only if available in provided context:
# - योज़ना / स्कीम का नाम  
# - यह किसके लिए है (पात्रता)  
# - कितना लाभ मिलता है (लाभ)  
# - कैसे और कहाँ आवेदन करना है (आवेदन प्रक्रिया)  
# - लिंक हो तो बताएं  

# If multiple schemes match, explain **2–3** clearly but naturally.
# Missing data → write “उपलब्ध नहीं” naturally.

# ### 🟡 ALWAYS END WITH:
# "अगर ज़रूरत हो तो अपने ग्राम पंचायत या CSC केंद्र से मदद लें।"

# ### 🌍 AFTER THE HINDI ANSWER:
# Give **one short English summary sentence** (not detailed).

# --------------------------------------------
# Now write the final answer in a natural, fluent, friendly tone.
# --------------------------------------------
# """

#     try:
#         completion = groq_client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2,
#         )
#         ai_answer = completion.choices[0].message.content.strip()
#     except Exception:
#         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
#         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
#         eng = (
#             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
#         )
#         return hdr + body + eng

#     return ai_answer


# def _should_use_schemes(question: str, schemes: List[Dict[str, Any]]) -> bool:
#     """
#     Decide kare ki is query ke liye schemes pipeline use karni hai ya nahi।
#     """
#     if not schemes:
#         return False

#     top = schemes[0]
#     top_final = float(top.get("_final_score", top.get("_score", 0.0)) or 0.0)

#     q = question.lower()
#     has_scheme_word = any(
#         w in q
#         for w in [
#             "योजना",
#             "yojana",
#             "scheme",
#             "स्कीम",
#             "pension",
#             "पेंशन",
#             "subsidy",
#             "सब्सिडी",
#             "बीमा",
#             "insurance",
#             "scholarship",
#             " छात्रवृत्ति",
#         ]
#     )

#     if top_final >= 0.60:
#         return True

#     if has_scheme_word and top_final >= 0.25:
#         return True

#     return False

# # ================== MODELS FOR JSON /ask ==================


# class AskRequest(BaseModel):
#     question: str
#     ui_lang: str = "hi"        # "hi" | "garhwali" | "en"
#     mode: str = "auto"         # "auto" | "docs" | "schemes"
#     history: List[Dict[str, str]] = []
#     user_meta: Dict[str, Any] | None = None


# class AskResponse(BaseModel):
#     response: str
#     sources: List[Dict[str, Any]] = []
#     audio_url: Optional[str] = None  # Garhwali TTS MP3 if generated


# class SchemeCard(SQLModel):
#     title: str
#     subtitle: Optional[str] = None
#     verified: bool = True
#     badges: List[str] = []
#     apply_url: Optional[str] = None
#     read_more_url: Optional[str] = None

# # ================== PERSONALISED RECOMMENDATIONS API ==================


# @app.get("/user/recommended-schemes", response_model=List[SchemeCard])
# def recommended_schemes(current_user: User = Depends(get_current_user)):
#     # Build simple query text from profile
#     parts = []

#     if current_user.district:
#         parts.append(current_user.district)
#     if current_user.block:
#         parts.append(current_user.block)
#     if current_user.gender:
#         parts.append(current_user.gender)
#     if current_user.age:
#         parts.append(f"age {current_user.age}")
#     if current_user.interest_tag:
#         parts.append(current_user.interest_tag)

#     # Strong signals
#     if current_user.occupation:
#         parts.append(current_user.occupation)
#     if current_user.disability and current_user.disability.lower() not in (
#         "none",
#         "nahin",
#         "no",
#     ):
#         parts.append("divyang")
#         parts.append(current_user.disability)
#     if current_user.income_bracket:
#         parts.append(current_user.income_bracket)
#     if current_user.social_category:
#         parts.append(current_user.social_category)

#     question = " ".join(parts) or "gramin yojana"

#     schemes, _total = search_schemes(
#         question=question,
#         limit=5,
#         page=1,
#         min_score=0.20,
#         category=None,
#         department=None,
#         typ=None,
#     )

#     cards: List[SchemeCard] = []
#     for s in schemes:
#         title = (
#             (s.get("name_hi") or "")
#             + (" / " + s.get("name_en", "") if s.get("name_en") else "")
#         ).strip(" /")
#         subtitle = s.get("description_hi") or s.get("description_en") or ""
#         badges = [s.get("department", ""), s.get("category", "")]
#         cards.append(
#             SchemeCard(
#                 title=title or "Yojana",
#                 subtitle=subtitle,
#                 verified=True,
#                 badges=[b for b in badges if b],
#                 apply_url=s.get("apply_link") or None,
#                 read_more_url=s.get("source_url") or None,
#             )
#         )
#     return cards

# # ================== ROUTES (HTML DEMO) ==================


# @app.get("/", response_class=HTMLResponse)
# async def get_home(
#     request: Request,
#     lang: str = "hi",      # ui_lang
#     mode: str = "docs",    # "docs" or "schemes"
# ):
#     # allow hi / en / garhwali in demo
#     if lang not in ("hi", "en", "garhwali"):
#         lang = "hi"
#     if mode not in ("docs", "schemes"):
#         mode = "docs"

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "messages": [],
#             "history_json": "[]",
#             "lang": lang,
#             "mode": mode,
#         },
#     )


# @app.post("/", response_class=HTMLResponse)
# async def post_query(
#     request: Request,
#     query: str = Form(...),
#     history_json: str = Form("[]"),
#     ui_lang: str = Form("hi"),   # "hi" | "garhwali" | "en"
#     mode: str = Form("docs"),    # "docs" or "schemes"
# ):
#     try:
#         history = json.loads(history_json)
#     except Exception:
#         history = []

#     # Decide target language for demo HTML
#     if ui_lang == "en":
#         target_lang = "en"
#     elif ui_lang == "garhwali":
#         target_lang = "garhwali"
#     else:
#         # "hi" / default → Hindi or Hinglish based on script
#         target_lang = "hi" if contains_devanagari(query) else "hinglish"

#     if mode == "schemes":
#         schemes, _total = search_schemes(
#             question=query,
#             limit=3,
#             page=1,
#             min_score=0.20,
#             category=None,
#             department=None,
#             typ=None,
#         )
#         base_answer = build_schemes_answer(query, schemes)
#     else:
#         base_answer, _sources = generate_docs_answer_raw(query, history)

#     final_text = translate_answer(base_answer, target_lang)
#     answer_html = _convert_markdown_bold_to_html(final_text)

#     history.append({"role": "user", "content": query})
#     history.append({"role": "assistant", "content": answer_html})

#     messages = [{"role": h["role"], "content": h["content"]} for h in history]

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "messages": messages,
#             "history_json": json.dumps(history, ensure_ascii=False),
#             "lang": ui_lang,
#             "mode": mode,
#         },
#     )

# # ================== CORE ASK LOGIC (shared) ==================


# def process_ask_request(req: AskRequest) -> AskResponse:
#     # Decide final language for UI
#     if req.ui_lang == "en":
#         target_lang = "en"
#     elif req.ui_lang == "garhwali":
#         target_lang = "garhwali"
#     else:
#         # "hi" / default → Hindi or Hinglish based on script
#         target_lang = "hi" if contains_devanagari(req.question) else "hinglish"

#     user_meta = req.user_meta or None

#     schemes: List[Dict[str, Any]] = []
#     doc_sources: List[Dict[str, Any]] = []
#     use_schemes = False

#     if req.mode in ("schemes", "auto"):
#         schemes, total = search_schemes(
#             question=req.question,
#             limit=5,
#             page=1,
#             min_score=0.20,
#             category=None,
#             department=None,
#             typ=None,
#         )
#         if req.mode == "schemes":
#             use_schemes = True
#         else:
#             use_schemes = _should_use_schemes(req.question, schemes)

#     if use_schemes:
#         base_answer = build_schemes_answer(req.question, schemes, user_meta=user_meta)
#         sources = [
#             {
#                 "name_hi": s.get("name_hi"),
#                 "name_en": s.get("name_en"),
#                 "score": s.get("_score"),
#                 "department": s.get("department"),
#                 "category": s.get("category"),
#                 "apply_link": s.get("apply_link"),
#             }
#             for s in schemes
#         ]
#     else:
#         base_answer, doc_sources = generate_docs_answer_raw(
#             req.question,
#             req.history,
#             user_meta=user_meta,
#         )
#         sources = doc_sources

#     final_text = translate_answer(base_answer, target_lang)
#     final_html = _convert_markdown_bold_to_html(final_text)

#     # If UI language is Garhwali → also generate TTS MP3 and return URL
#     audio_url: Optional[str] = None
#     if target_lang == "garhwali":
#         plain_answer = re.sub(r"<[^>]+>", "", final_html)
#         filename = tts_garhwali(plain_answer)
#         audio_url = f"/tts/{filename}"

#     return AskResponse(response=final_html, sources=sources, audio_url=audio_url)

# # ================== JSON API FOR REACT CHAT ==================


# @app.post("/ask", response_model=AskResponse)
# def ask(req: AskRequest):
#     """
#     Text chat endpoint (used by React ChatScreen).
#     """
#     return process_ask_request(req)


# @app.post("/voice/ask")
# async def voice_ask(
#     audio: UploadFile = File(...),
#     mode: str = "auto",
#     ui_lang: str = "garhwali",
# ):
#     """
#     Voice chat endpoint:
#     1. Take uploaded audio (Garhwali / Hindi speech)
#     2. Transcribe with Whisper
#     3. Run normal ask pipeline with ui_lang=garhwali (by default)
#     4. Convert answer text to TTS mp3
#     5. Return: transcribed_question, text_answer_html, audio_url, sources
#     """
#     # ---- Save temp audio ----
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
#         shutil.copyfileobj(audio.file, tmp)
#         tmp_path = tmp.name

#     try:
#         # ---- STT: audio -> text ----
#         question_text = transcribe_garhwali_audio(tmp_path)

#         # ---- Build AskRequest ----
#         req = AskRequest(
#             question=question_text,
#             ui_lang=ui_lang,
#             mode=mode,
#             history=[],
#             user_meta=None,
#         )

#         ask_resp = process_ask_request(req)
#         answer_html = ask_resp.response

#         # For voice endpoint we already got audio_url from process_ask_request if garhwali
#         audio_url = ask_resp.audio_url

#         return {
#             "question_text": question_text,
#             "answer_html": answer_html,
#             "audio_url": audio_url,
#             "sources": ask_resp.sources,
#         }

#     finally:
#         try:
#             os.remove(tmp_path)
#         except Exception:
#             pass

# # ================== AUTH ROUTES ==================


# @app.post("/auth/register", response_model=UserRead)
# def register(user_in: UserCreate, session: Session = Depends(get_session)):
#     existing = get_user_by_username(session, user_in.username)
#     if existing:
#         raise HTTPException(status_code=400, detail="Username already registered")

#     user = User(
#         username=user_in.username,
#         full_name=user_in.full_name,
#         hashed_password=get_password_hash(user_in.password),
#         district=user_in.district,
#         block=user_in.block,
#         village_code=user_in.village_code,
#         age=user_in.age,
#         gender=user_in.gender,
#         interest_tag=user_in.interest_tag,
#         disability=user_in.disability,
#         occupation=user_in.occupation,
#         income_bracket=user_in.income_bracket,
#         social_category=user_in.social_category,
#     )
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user


# @app.post("/auth/login", response_model=Token)
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     session: Session = Depends(get_session),
# ):
#     user = get_user_by_username(session, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     token = create_access_token({"sub": user.username})
#     return Token(access_token=token)


# @app.get("/me", response_model=UserRead)
# def read_me(current_user: User = Depends(get_current_user)):
#     return current_user


# @app.put("/me", response_model=UserRead)
# def update_me(
#     user_update: UserUpdate,
#     current_user: User = Depends(get_current_user),
#     session: Session = Depends(get_session),
# ):
#     data = user_update.dict(exclude_unset=True)

#     for field, value in data.items():
#         setattr(current_user, field, value)

#     session.add(current_user)
#     session.commit()
#     session.refresh(current_user)
#     return current_user


# @app.get("/health")
# def health():
#     return {
#         "status": "ok",
#         "docs_collection": DOC_COLLECTION,
#         "schemes_collection": SCHEMES_COLLECTION,
#         "embed_model_schemes": EMBED_MODEL_NAME_SCHEMES,
#     }































# import os
# import json
# import uuid
# import re
# import unicodedata
# import tempfile
# import shutil
# from pathlib import Path
# from typing import List, Dict, Any, Optional, Tuple

# from dotenv import load_dotenv
# from fastapi import (
#     FastAPI,
#     Request,
#     Form,
#     Depends,
#     HTTPException,
#     status,
#     UploadFile,
#     File,
# )
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# from pydantic import BaseModel

# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     VectorParams,
#     Distance,
#     PointStruct,
#     Filter,
#     FieldCondition,
#     MatchText,
# )
# from qdrant_client.http import models as qm  # noqa: F401

# from sentence_transformers import SentenceTransformer
# from fastembed import TextEmbedding
# from groq import Groq
# from googletrans import Translator

# from faster_whisper import WhisperModel
# from gtts import gTTS

# from sqlmodel import Field, SQLModel, Session, create_engine, select
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# # ================== CONFIG ==================

# BASE_DIR = Path(__file__).resolve().parent.parent  # repo root (panchayat-sahayika)

# # Schemes JSON path
# SCHEMES_PATH = BASE_DIR / "samaj_kalyan_vibhag_clean_typed.json"

# # TTS output directory
# TTS_OUTPUT_DIR = BASE_DIR / "tts_output"
# TTS_OUTPUT_DIR.mkdir(exist_ok=True)

# load_dotenv()

# # ---- Groq / LLM ----
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise RuntimeError("GROQ_API_KEY missing in .env")

# LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
# GROQ_MODEL_DOCS = os.getenv("GROQ_MODEL", LLM_MODEL)

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---- DOCS RAG Qdrant (remote or local) ----
# DOC_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# DOC_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
# DOC_COLLECTION = os.getenv("COLLECTION_NAME", "panchayat_uk_docs")

# doc_qclient = QdrantClient(url=DOC_QDRANT_URL, api_key=DOC_QDRANT_API_KEY)
# doc_embedder = TextEmbedding()

# # ---- Schemes Qdrant (local embedded) ----
# EMBED_MODEL_NAME_SCHEMES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# SCHEMES_COLLECTION = "samaj_kalyan_vibhag_schemes"

# scheme_embed_model = SentenceTransformer(EMBED_MODEL_NAME_SCHEMES)
# scheme_qdrant = QdrantClient(path=str(BASE_DIR / "qdrant_data"))

# # ---- Voice models (Whisper STT) ----
# WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "medium")
# USE_CUDA = os.getenv("USE_CUDA", "0") == "1"

# whisper_model = WhisperModel(
#     WHISPER_MODEL_NAME,
#     device="cuda" if USE_CUDA else "cpu",
#     compute_type="float16" if USE_CUDA else "int8",
# )

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

# # ---- FastAPI + Templates ----
# app = FastAPI(title="Panchayat Sahayika Unified Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )

# # static mount for TTS files
# app.mount("/tts", StaticFiles(directory=str(TTS_OUTPUT_DIR)), name="tts")

# templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# translator = Translator()  # Google translator instance

# # ================== AUTH / USERS ==================

# DATABASE_URL = "sqlite:///./panchayat_users.db"
# engine = create_engine(DATABASE_URL, echo=False)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# SECRET_KEY = os.getenv(
#     "SECRET_KEY",
#     "baea29ce56f4b02733883b6ae1a76265988d123d5ad3e9d2214dae4646a81ee6",
# )
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str = Field(index=True, unique=True)
#     full_name: Optional[str] = None
#     hashed_password: str

#     # profile info
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserCreate(SQLModel):
#     username: str
#     password: str
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserRead(SQLModel):
#     id: int
#     username: str
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class UserUpdate(SQLModel):
#     full_name: Optional[str] = None
#     district: Optional[str] = None
#     block: Optional[str] = None
#     village_code: Optional[str] = None
#     age: Optional[int] = None
#     gender: Optional[str] = None
#     interest_tag: Optional[str] = None

#     disability: Optional[str] = None
#     occupation: Optional[str] = None
#     income_bracket: Optional[str] = None
#     social_category: Optional[str] = None


# class Token(SQLModel):
#     access_token: str
#     token_type: str = "bearer"


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# def _bcrypt_safe(password: str) -> str:
#     if password is None:
#         return ""
#     pw_bytes = password.encode("utf-8")
#     return pw_bytes[:72].decode("utf-8", errors="ignore")


# def get_password_hash(password: str) -> str:
#     safe_pw = _bcrypt_safe(password)
#     return pwd_context.hash(safe_pw)


# def verify_password(plain: str, hashed: str) -> bool:
#     safe_pw = _bcrypt_safe(plain)
#     return pwd_context.verify(safe_pw, hashed)


# def create_access_token(data: dict) -> str:
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# def get_user_by_username(session: Session, username: str) -> Optional[User]:
#     stmt = select(User).where(User.username == username)
#     return session.exec(stmt).first()


# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     session: Session = Depends(get_session),
# ) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: Optional[str] = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = get_user_by_username(session, username=username)
#     if not user:
#         raise credentials_exception
#     return user


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

# # ================== COMMON LANGUAGE + VOICE HELPERS ==================


# def contains_devanagari(text: str) -> bool:
#     for ch in text:
#         if "\u0900" <= ch <= "\u097F":
#             return True
#     return False


# def _llm_translate(text: str, target_desc: str) -> str:
#     system_msg = (
#         "You are a translator for Gram Panchayat content.\n"
#         "You ONLY translate or rewrite the text; you do not add explanations.\n"
#         "Preserve markdown bold markers **like this** exactly as they are.\n"
#         "Do not change the meaning; only change the language/style.\n"
#     )

#     user_msg = (
#         f"Translate / rewrite the following text into {target_desc}\n\n"
#         f"Text:\n{text}"
#     )

#     completion = groq_client.chat.completions.create(
#         model=LLM_MODEL,
#         messages=[
#             {"role": "system", "content": system_msg},
#             {"role": "user", "content": user_msg},
#         ],
#         temperature=0.2,
#         max_tokens=1200,
#     )
#     out = completion.choices[0].message.content or text
#     return out


# def translate_answer(text: str, target_lang: str) -> str:
#     """
#     Final step translation:

#     target_lang:
#       - 'en'        -> English
#       - 'hi'        -> simple Hindi (Devanagari)
#       - 'garhwali'  -> Garhwali (Devanagari)
#       - 'hinglish'  -> Hinglish (Roman Hindi)
#     """

#     # ---------- English ----------
#     if target_lang == "en":
#         try:
#             res = translator.translate(text, dest="en")
#             out = res.text
#             if out and not contains_devanagari(out) and out.strip() != "":
#                 return out
#         except Exception:
#             pass

#         return _llm_translate(
#             text,
#             "clear, simple English suitable for village-level users. "
#             "Avoid Hindi script and use plain English sentences.",
#         )

#     # ---------- Hindi ----------
#     if target_lang == "hi":
#         return _llm_translate(
#             text,
#             "very simple Hindi in Devanagari script, using everyday words "
#             "that village-level users understand.",
#         )

#     # ---------- Garhwali ----------
#     if target_lang == "garhwali":
#         return _llm_translate(
#             text,
#             (
#                 "Rewrite the text into PURE Garhwali (Central Garhwal dialect) "
#                 "written in Devanagari script.\n\n"
#                 "STRICT RULES:\n"
#                 "1. हर वाक्य गढ़वाली बोलचाल जैसा हो, न कि मानक हिन्दी जैसा।\n"
#                 "2. जहाँ भी ‘है / होगा / होंगे / करना / करना है’ जैसे हिन्दी रूप हों, "
#                 "उन्हें गढ़वाली रूपों से बदलो – जैसे ‘च’, ‘रै’, ‘जा’, ‘करणो’, ‘करणु’ आदि।\n"
#                 "3. ‘आप’ की जगह हमेशा ‘त्यूँ / तुम्हर / तुमीं’ जैसे रूप इस्तेमाल करो।\n"
#                 "4. उदाहरण:\n"
#                 "   हिन्दी: 'आपको क्या करना है?'\n"
#                 "   गढ़वाली: 'त्यूँ कै करणु च?'\n"
#                 "   हिन्दी: 'योजना का लाभ मिलेगा।'\n"
#                 "   गढ़वाली: 'योजना को लाभ मिललि जा।'\n"
#                 "5. सरकारी योजना / scheme के नाम (जैसे **प्रधानमंत्री आवास योजना**, "
#                 "**राष्ट्रीय पशुधन मिशन** आदि) बिल्कुल ज्यों के त्यों रहने दो; "
#                 "उनको गढ़वाली में मत बदलो।\n"
#                 "6. कोई भी लाइन शुद्ध हिन्दी में न छोड़ो; हर लाइन गढ़वाली में ही दो।\n"
#             ),
#         )

#     # ---------- Hinglish ----------
#     return _llm_translate(
#         text,
#         "very simple Hinglish (Roman Hindi using English letters). "
#         "Do NOT use Devanagari characters.",
#     )


# def _convert_markdown_bold_to_html(text: str) -> str:
#     return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


# def transcribe_garhwali_audio(path: str) -> str:
#     segments, info = whisper_model.transcribe(
#         path,
#         language="hi",
#         task="transcribe",
#         vad_filter=True,
#     )
#     pieces = [seg.text.strip() for seg in segments if seg.text.strip()]
#     text = " ".join(pieces).strip()
#     return text


# def tts_garhwali(text: str) -> str:
#     safe_text = text.strip()
#     if len(safe_text) > 1500:
#         safe_text = safe_text[:1500]

#     filename = f"garhwali_{uuid.uuid4().hex}.mp3"
#     out_path = TTS_OUTPUT_DIR / filename

#     # Garhwali ke liye bhi abhi Hindi TTS (hi-IN) use kar rahe hain
#     tts = gTTS(text=safe_text, lang="hi")
#     tts.save(str(out_path))

#     return filename

# # ================== DOCS RAG PIPELINE ==================


# def build_docs_system_prompt() -> str:
#     return (
#         "आप 'Panchayat Sahayika' हैं, उत्तराखंड की ग्राम पंचायतों के लिए सहायक।\n"
#         "यूज़र कभी-कभी गढ़वाली या हिंग्लिश में भी सवाल पूछ सकते हैं; "
#         "आप अर्थ समझकर पहले सरल हिन्दी में जवाब तैयार करें।\n"
#         "आपको केवल नीचे दिए गए संदर्भ (official Panchayati Raj documents: acts, rules, "
#         "guidelines, roles, schemes, training material) का इस्तेमाल करके ही जवाब देना है।\n\n"
#         "भाषा बहुत ही सरल और आसान हिन्दी होनी चाहिए ताकि सरपंच, वार्ड मेंबर और ग्राम पंचायत "
#         "कर्मचारी आसानी से समझ सकें।\n"
#         "कानूनी भारी शब्दों से बचें।\n"
#         "अगर ज़रूरी जानकारी संदर्भ में नहीं है, तो साफ-साफ लिखें कि यह जानकारी उपलब्ध नहीं है "
#         "और आप अंदाज़ा नहीं लगा रहे हैं।\n"
#         "कभी भी दस्तावेज़ का नाम, फाइल का नाम, पेज नंबर या 'source' list का ज़िक्र न करें।\n"
#     )


# def retrieve_docs_context(query: str, top_k: int = 8) -> List[Dict[str, Any]]:
#     query_vec = list(doc_embedder.embed([query]))[0]
#     results = doc_qclient.search(
#         collection_name=DOC_COLLECTION,
#         query_vector=query_vec,
#         limit=top_k,
#         with_payload=True,
#     )

#     contexts = []
#     for r in results:
#         pl = r.payload or {}
#         contexts.append(
#             {
#                 "text": pl.get("text", ""),
#                 "source_file": pl.get("source_file", ""),
#                 "page": pl.get("page", ""),
#                 "url": pl.get("url", ""),
#                 "score": r.score,
#             }
#         )
#     return contexts


# def generate_docs_answer_raw(
#     query: str,
#     history: List[Dict[str, str]],
#     user_meta: Dict[str, Any] | None = None,
# ) -> Tuple[str, List[Dict[str, Any]]]:
#     contexts = retrieve_docs_context(query)

#     context_block = "\n\n---\n\n".join(c["text"] for c in contexts if c["text"])

#     user_ctx = build_user_context(user_meta)

#     system_prompt = build_docs_system_prompt()
#     if user_ctx:
#         system_prompt += (
#             "\n\nउपयोगकर्ता प्रोफाइल (उदाहरणों को practical banane ke liye):\n"
#             f"{user_ctx}\n"
#             "जवाब में आप user ki स्थिति ke हिसाब से छोटा सा context de sakte hain "
#             "(jaise किसान, छात्र, दिव्यांग इत्यादि)."
#         )

#     messages = [{"role": "system", "content": system_prompt}]

#     for h in history[-4:] if history else []:
#         messages.append({"role": h["role"], "content": h["content"]})

#     messages.append(
#         {
#             "role": "user",
#             "content": (
#                 f"प्रश्न: {query}\n\n"
#                 f"नीचे दिए गए दस्तावेज़ों के संदर्भ का उपयोग करके उत्तर दीजिए। "
#                 f"अपने उत्तर में इन दस्तावेज़ों के नाम या पेज नंबर का ज़िक्र मत कीजिए:\n\n"
#                 f"{context_block}"
#             ),
#         }
#     )

#     completion = groq_client.chat.completions.create(
#         model=GROQ_MODEL_DOCS,
#         messages=messages,
#         temperature=0.3,
#         max_tokens=900,
#     )
#     raw_answer = completion.choices[0].message.content or ""

#     unique_sources = []
#     seen = set()
#     for c in contexts:
#         key = (c["source_file"], c["page"])
#         if key not in seen and c["source_file"]:
#             seen.add(key)
#             unique_sources.append(
#                 {
#                     "source_file": c["source_file"],
#                     "page": c["page"],
#                     "url": c["url"],
#                 }
#             )

#     return raw_answer, unique_sources

# # ================== SCHEMES PIPELINE ==================


# def load_schemes() -> List[Dict[str, Any]]:
#     with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     for s in data:
#         s.setdefault("name_hi", "")
#         s.setdefault("name_en", "")
#         s.setdefault("category", "")
#         s.setdefault("department", "")
#         s.setdefault("description_hi", "")
#         s.setdefault("description_en", "")
#         s.setdefault("eligibility", "")
#         s.setdefault("benefit", "")
#         s.setdefault("apply_process", "")
#         s.setdefault("apply_link", "")
#         s.setdefault("source_url", "")
#         s.setdefault("type", s.get("type", "scheme"))
#     return data


# def _concat_item_text(s: Dict[str, Any]) -> str:
#     name = (s.get("name_hi", "") + " " + s.get("name_en", "")).strip()
#     other_parts = [
#         s.get("category", ""),
#         s.get("department", ""),
#         s.get("description_hi", ""),
#         s.get("description_en", ""),
#         s.get("eligibility", ""),
#         s.get("benefit", ""),
#         s.get("apply_process", ""),
#     ]
#     weighted_name = " ".join([name] * 5) if name else ""
#     rest = " | ".join([str(p) for p in other_parts if p])

#     return " | ".join([p for p in [weighted_name, rest] if p])


# def init_schemes_collection():
#     schemes = load_schemes()

#     scheme_qdrant.recreate_collection(
#         collection_name=SCHEMES_COLLECTION,
#         vectors_config=VectorParams(
#             size=scheme_embed_model.get_sentence_embedding_dimension(),
#             distance=Distance.COSINE,
#         ),
#     )

#     points: List[PointStruct] = []
#     for s in schemes:
#         vec = scheme_embed_model.encode(_concat_item_text(s)).tolist()
#         payload = dict(s)
#         payload["__search_blob"] = _concat_item_text(s)
#         points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload))

#     scheme_qdrant.upsert(SCHEMES_COLLECTION, points)
#     print(f"✅ Indexed {len(points)} schemes into Qdrant (schemes collection)")


# init_schemes_collection()


# def _norm(s: str) -> str:
#     if not s:
#         return ""
#     s = unicodedata.normalize("NFKC", s)
#     s = re.sub(r"\s+", " ", s).strip().lower()
#     return s


# def _qdrant_filter(
#     category: Optional[str],
#     department: Optional[str],
#     typ: Optional[str],
# ) -> Optional[Filter]:
#     conds = []
#     if category:
#         conds.append(FieldCondition(key="category", match=MatchText(text=category)))
#     if department:
#         conds.append(FieldCondition(key="department", match=MatchText(text=department)))
#     if typ:
#         conds.append(FieldCondition(key="type", match=MatchText(text=typ)))
#     if not conds:
#         return None
#     return Filter(must=conds)


# def _keyword_boost(question: str, item: Dict[str, Any]) -> float:
#     q = _norm(question)
#     name = _norm((item.get("name_hi", "") + " " + item.get("name_en", "")))
#     cat = _norm(item.get("category", ""))
#     dept = _norm(item.get("department", ""))

#     boost = 0.0

#     if q and q in name:
#         boost += 0.6

#     q_words = [w for w in q.split() if len(w) > 2]
#     for w in q_words:
#         if w in name or w in cat or w in dept:
#             boost += 0.15

#     return boost


# def search_schemes(
#     question: str,
#     limit: int = 3,
#     page: int = 1,
#     min_score: float = 0.20,
#     category: Optional[str] = None,
#     department: Optional[str] = None,
#     typ: Optional[str] = None,
# ):
#     qvec = scheme_embed_model.encode(question).tolist()
#     page = max(page, 1)
#     limit = max(1, min(20, limit))

#     MAX_HITS = 50

#     hits = scheme_qdrant.search(
#         collection_name=SCHEMES_COLLECTION,
#         query_vector=qvec,
#         limit=MAX_HITS,
#         with_payload=True,
#         with_vectors=False,
#         query_filter=_qdrant_filter(category, department, typ),
#     )

#     scored: List[Dict[str, Any]] = []
#     for h in hits:
#         base_score = float(h.score) if hasattr(h, "score") else 0.0
#         if base_score < min_score:
#             continue
#         p = dict(h.payload)
#         kw_boost = _keyword_boost(question, p)
#         final_score = base_score + kw_boost
#         p["_score"] = base_score
#         p["_final_score"] = final_score
#         scored.append(p)

#     deduped: List[Dict[str, Any]] = []
#     seen = set()
#     for p in scored:
#         key = (p.get("name_hi") or p.get("name_en") or "").strip()
#         if not key:
#             key = p.get("id", "")
#         if key in seen:
#             continue
#         seen.add(key)
#         deduped.append(p)

#     deduped.sort(key=lambda x: x.get("_final_score", 0.0), reverse=True)

#     total = len(deduped)
#     start = (page - 1) * limit
#     end = start + limit
#     page_items = deduped[start:end]

#     return page_items, total


# def _fmt_scheme_card(s: Dict[str, Any]) -> str:
#     name = s.get("name_hi") or s.get("name_en") or "—"
#     bits = [
#         f"• **{name}**",
#         f"  - 🎓 पात्रता: {s.get('eligibility','उपलब्ध नहीं')}",
#         f"  - 💰 लाभ: {s.get('benefit','उपलब्ध नहीं')}",
#         f"  - 📝 आवेदन: {s.get('apply_process','उपलब्ध नहीं')}",
#     ]
#     if s.get("apply_link"):
#         bits.append(f"  - 🔗 लिंक: {s['apply_link']}")
#     return "\n".join(bits)


# def build_user_context(user_meta: dict | None) -> str:
#     if not user_meta:
#         return ""

#     district = user_meta.get("district")
#     block = user_meta.get("block")
#     village = user_meta.get("village_code")
#     age = user_meta.get("age")
#     gender = user_meta.get("gender")
#     interest = user_meta.get("interest_tag")

#     disability = user_meta.get("disability")
#     occupation = user_meta.get("occupation")
#     income_bracket = user_meta.get("income_bracket")
#     social_category = user_meta.get("social_category")

#     parts = []

#     if district:
#         parts.append(f"जिला {district}")
#     if block:
#         parts.append(f"ब्लॉक {block}")
#     if village:
#         parts.append(f"गाँव कोड {village}")
#     if age:
#         parts.append(f"आयु {age} वर्ष")
#     if gender:
#         parts.append(f"लिंग {gender}")
#     if occupation:
#         parts.append(f"पेशा: {occupation}")
#     if income_bracket:
#         parts.append(f"आय वर्ग: {income_bracket}")
#     if social_category:
#         parts.append(f"सोशल कैटेगरी: {social_category}")
#     if disability and disability.lower() not in ("none", "nahin", "no"):
#         parts.append(f"विशेष आवश्यकताएँ / दिव्यांगता: {disability}")
#     if interest:
#         parts.append(f"रुचि: {interest}")

#     if not parts:
#         return ""

#     return "उपयोगकर्ता की जानकारी: " + ", ".join(parts) + ". "


# def build_schemes_answer(
#     question: str,
#     schemes: List[Dict[str, Any]],
#     user_meta: Dict[str, Any] | None = None,
# ) -> str:
#     if not schemes:
#         return (
#             "माफ़ कीजिए, इस सवाल से मिलती-जुलती कोई योजना नहीं मिली। "
#             "कृपया अलग शब्दों में पूछें, या ज़िला/विभाग/श्रेणी लिखें।\n\n"
#             "**English:** No strong matches. Try different words or add location/department."
#         )

#     user_ctx = build_user_context(user_meta)

#     q_low = question.lower()
#     want_apply = any(
#         w in q_low
#         for w in [
#             "apply",
#             " आवेदन",
#             "आवेदन",
#             "फॉर्म",
#             "form",
#             "कैसे",
#             "kaise",
#             "कहाँ",
#             "kaha",
#             "कहां",
#         ]
#     )
#     want_benefit = any(
#         w in q_low
#         for w in [
#             "लाभ",
#             "benefit",
#             "paisa",
#             "₹",
#             "kitna",
#             "कितना",
#             "राशि",
#         ]
#     )
#     want_elig = any(
#         w in q_low
#         for w in [
#             "पात्रता",
#             "eligibility",
#             "kaun",
#             "कौन",
#             "किसको",
#             "kis ko",
#             "kisko",
#         ]
#     )

#     if not GROQ_API_KEY:
#         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
#         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
#         eng = (
#             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
#         )
#         return hdr + body + eng

#     context_lines = []
#     for s in schemes:
#         context_lines.append(
#             "योजना: {name}\nविवरण: {desc}\nपात्रता: {elig}\nलाभ: {ben}\nआवेदन प्रक्रिया: {proc}\nविभाग: {dept}\nश्रेणी: {cat}\nलिंक: {link}\n".format(
#                 name=(s.get("name_hi") or s.get("name_en") or ""),
#                 desc=s.get("description_hi", ""),
#                 elig=s.get("eligibility", ""),
#                 ben=s.get("benefit", ""),
#                 proc=s.get("apply_process", ""),
#                 dept=s.get("department", ""),
#                 cat=s.get("category", ""),
#                 link=s.get("apply_link", ""),
#             )
#         )
#     context = "\n---\n".join(context_lines)

#     focus_lines = []
#     if want_apply:
#         focus_lines.append(
#             "- User is mainly asking **how to apply**. "
#             "You MUST explain the पूरा 'आवेदन प्रक्रिया' field step-by-step in simple Hindi. "
#             "हर ज़रूरी स्टेप और हर ज़रूरी दस्तावेज़ का नाम जरूर बताएं।"
#         )
#     if want_benefit:
#         focus_lines.append(
#             "- User is asking about **benefits / amount**. "
#             "Explain the 'लाभ' field completely. अलग-अलग राशि हो तो सब बताएं।"
#         )
#     if want_elig:
#         focus_lines.append(
#             "- User is asking about **eligibility / who can get it**. "
#             "Explain the 'पात्रता' field पूरी तरह, सभी शर्तें (1, 2, 3...) अलग-अलग लिखें।"
#         )

#     focus_text = "\n".join(focus_lines) if focus_lines else "- Follow the general rules below."

#     profile_text = user_ctx or "कोई अतिरिक्त उपयोगकर्ता जानकारी उपलब्ध नहीं है। अगर जानकारी ना हो तो generic जवाब दें।"

#     prompt = f"""
# You are **Panchayat Sahayika**, a friendly, polite and knowledgeable AI assistant created to help rural citizens of India. 
# Your main goal is to explain information in very **simple, clear, human-like Hindi**, so that even villagers, elderly people, 
# and first-time smartphone users can easily understand.

# User profile (for context, don't repeat fully, just use it smartly in examples):
# {profile_text}

# You must use **only** the information given in the schemes context below. 
# Do NOT invent or guess any benefits, eligibility rules, amounts or links that are not present.

# --------------------------------------------
# 📌 USER QUESTION:
# {question}

# 📌 RELEVANT SCHEMES (if matched):
# {context}
# --------------------------------------------

# ### 🔍 SPECIAL FOCUS (based on the user's question)
# {focus_text}

# ### 🟢 MAIN RULES FOR ANSWERING:
# - Explain in **simple conversational Hindi**, short sentences, and natural flow.  
# - Do NOT sound robotic. Do NOT dump raw data.  
# - Be clear, warm, and practical.
# - **Whenever you write the name of any scheme / yojana, always wrap it like this: `**PM Awas Yojana**`.**

# Include these only if available in provided context:
# - योज़ना / स्कीम का नाम  
# - यह किसके लिए है (पात्रता)  
# - कितना लाभ मिलता है (लाभ)  
# - कैसे और कहाँ आवेदन करना है (आवेदन प्रक्रिया)  
# - लिंक हो तो बताएं  

# If multiple schemes match, explain **2–3** clearly but naturally.
# Missing data → write “उपलब्ध नहीं” naturally.

# ### 🟡 ALWAYS END WITH:
# "अगर ज़रूरत हो तो अपने ग्राम पंचायत या CSC केंद्र से मदद लें।"

# ### 🌍 AFTER THE HINDI ANSWER:
# Give **one short English summary sentence** (not detailed).

# --------------------------------------------
# Now write the final answer in a natural, fluent, friendly tone.
# --------------------------------------------
# """

#     try:
#         completion = groq_client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2,
#         )
#         ai_answer = completion.choices[0].message.content.strip()
#     except Exception:
#         hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
#         body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
#         eng = (
#             "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
#         )
#         return hdr + body + eng

#     return ai_answer


# def _should_use_schemes(question: str, schemes: List[Dict[str, Any]]) -> bool:
#     if not schemes:
#         return False

#     top = schemes[0]
#     top_final = float(top.get("_final_score", top.get("_score", 0.0)) or 0.0)

#     q = question.lower()
#     has_scheme_word = any(
#         w in q
#         for w in [
#             "योजना",
#             "yojana",
#             "scheme",
#             "स्कीम",
#             "pension",
#             "पेंशन",
#             "subsidy",
#             "सब्सिडी",
#             "बीमा",
#             "insurance",
#             "scholarship",
#             " छात्रवृत्ति",
#         ]
#     )

#     if top_final >= 0.60:
#         return True

#     if has_scheme_word and top_final >= 0.25:
#         return True

#     return False

# # ================== MODELS FOR JSON /ask ==================


# class AskRequest(BaseModel):
#     question: str
#     ui_lang: str = "hi"        # "hi" | "garhwali" | "en"
#     mode: str = "auto"         # "auto" | "docs" | "schemes"
#     history: List[Dict[str, str]] = []
#     user_meta: Dict[str, Any] | None = None


# class AskResponse(BaseModel):
#     response: str
#     sources: List[Dict[str, Any]] = []


# class SchemeCard(SQLModel):
#     title: str
#     subtitle: Optional[str] = None
#     verified: bool = True
#     badges: List[str] = []
#     apply_url: Optional[str] = None
#     read_more_url: Optional[str] = None

# # ================== PERSONALISED RECOMMENDATIONS API ==================


# @app.get("/user/recommended-schemes", response_model=List[SchemeCard])
# def recommended_schemes(current_user: User = Depends(get_current_user)):
#     parts = []

#     if current_user.district:
#         parts.append(current_user.district)
#     if current_user.block:
#         parts.append(current_user.block)
#     if current_user.gender:
#         parts.append(current_user.gender)
#     if current_user.age:
#         parts.append(f"age {current_user.age}")
#     if current_user.interest_tag:
#         parts.append(current_user.interest_tag)

#     if current_user.occupation:
#         parts.append(current_user.occupation)
#     if current_user.disability and current_user.disability.lower() not in (
#         "none",
#         "nahin",
#         "no",
#     ):
#         parts.append("divyang")
#         parts.append(current_user.disability)
#     if current_user.income_bracket:
#         parts.append(current_user.income_bracket)
#     if current_user.social_category:
#         parts.append(current_user.social_category)

#     question = " ".join(parts) or "gramin yojana"

#     schemes, _total = search_schemes(
#         question=question,
#         limit=5,
#         page=1,
#         min_score=0.20,
#         category=None,
#         department=None,
#         typ=None,
#     )

#     cards: List[SchemeCard] = []
#     for s in schemes:
#         title = (
#             (s.get("name_hi") or "")
#             + (" / " + s.get("name_en", "") if s.get("name_en") else "")
#         ).strip(" /")
#         subtitle = s.get("description_hi") or s.get("description_en") or ""
#         badges = [s.get("department", ""), s.get("category", "")]
#         cards.append(
#             SchemeCard(
#                 title=title or "Yojana",
#                 subtitle=subtitle,
#                 verified=True,
#                 badges=[b for b in badges if b],
#                 apply_url=s.get("apply_link") or None,
#                 read_more_url=s.get("source_url") or None,
#             )
#         )
#     return cards

# # ================== ROUTES (HTML DEMO) ==================


# @app.get("/", response_class=HTMLResponse)
# async def get_home(
#     request: Request,
#     lang: str = "hi",
#     mode: str = "docs",
# ):
#     if lang not in ("hi", "en", "garhwali"):
#         lang = "hi"
#     if mode not in ("docs", "schemes"):
#         mode = "docs"

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "messages": [],
#             "history_json": "[]",
#             "lang": lang,
#             "mode": mode,
#         },
#     )


# @app.post("/", response_class=HTMLResponse)
# async def post_query(
#     request: Request,
#     query: str = Form(...),
#     history_json: str = Form("[]"),
#     ui_lang: str = Form("hi"),
#     mode: str = Form("docs"),
# ):
#     try:
#         history = json.loads(history_json)
#     except Exception:
#         history = []

#     if ui_lang == "en":
#         target_lang = "en"
#     elif ui_lang == "garhwali":
#         target_lang = "garhwali"
#     else:
#         target_lang = "hi" if contains_devanagari(query) else "hinglish"

#     if mode == "schemes":
#         schemes, _total = search_schemes(
#             question=query,
#             limit=3,
#             page=1,
#             min_score=0.20,
#             category=None,
#             department=None,
#             typ=None,
#         )
#         base_answer = build_schemes_answer(query, schemes)
#     else:
#         base_answer, _sources = generate_docs_answer_raw(query, history)

#     final_text = translate_answer(base_answer, target_lang)
#     answer_html = _convert_markdown_bold_to_html(final_text)

#     history.append({"role": "user", "content": query})
#     history.append({"role": "assistant", "content": answer_html})

#     messages = [{"role": h["role"], "content": h["content"]} for h in history]

#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "messages": messages,
#             "history_json": json.dumps(history, ensure_ascii=False),
#             "lang": ui_lang,
#             "mode": mode,
#         },
#     )

# # ================== CORE ASK LOGIC (shared) ==================


# def process_ask_request(req: AskRequest) -> AskResponse:
#     # Decide final language for UI text
#     if req.ui_lang == "en":
#         target_lang = "en"
#     elif req.ui_lang == "garhwali":
#         target_lang = "garhwali"
#     else:
#         target_lang = "hi" if contains_devanagari(req.question) else "hinglish"

#     user_meta = req.user_meta or None

#     schemes: List[Dict[str, Any]] = []
#     doc_sources: List[Dict[str, Any]] = []
#     use_schemes = False

#     if req.mode in ("schemes", "auto"):
#         schemes, total = search_schemes(
#             question=req.question,
#             limit=5,
#             page=1,
#             min_score=0.20,
#             category=None,
#             department=None,
#             typ=None,
#         )
#         if req.mode == "schemes":
#             use_schemes = True
#         else:
#             use_schemes = _should_use_schemes(req.question, schemes)

#     if use_schemes:
#         base_answer = build_schemes_answer(req.question, schemes, user_meta=user_meta)
#         sources = [
#             {
#                 "name_hi": s.get("name_hi"),
#                 "name_en": s.get("name_en"),
#                 "score": s.get("_score"),
#                 "department": s.get("department"),
#                 "category": s.get("category"),
#                 "apply_link": s.get("apply_link"),
#             }
#             for s in schemes
#         ]
#     else:
#         base_answer, doc_sources = generate_docs_answer_raw(
#             req.question,
#             req.history,
#             user_meta=user_meta,
#         )
#         sources = doc_sources

#     final_text = translate_answer(base_answer, target_lang)
#     final_html = _convert_markdown_bold_to_html(final_text)

#     return AskResponse(response=final_html, sources=sources)

# # ================== JSON API FOR REACT CHAT ==================


# @app.post("/ask", response_model=AskResponse)
# def ask(req: AskRequest):
#     return process_ask_request(req)


# @app.post("/voice/ask")
# async def voice_ask(
#     audio: UploadFile = File(...),
#     mode: str = "auto",
#     ui_lang: str = "garhwali",
# ):
#     """
#     Voice chat endpoint:
#     1. Audio (Garhwali/Hindi) -> Whisper transcription
#     2. /ask pipeline with ui_lang (default garhwali)
#     3. Answer text + Garhwali TTS mp3
#     """
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
#         shutil.copyfileobj(audio.file, tmp)
#         tmp_path = tmp.name

#     try:
#         question_text = transcribe_garhwali_audio(tmp_path)

#         req = AskRequest(
#             question=question_text,
#             ui_lang=ui_lang,
#             mode=mode,
#             history=[],
#             user_meta=None,
#         )

#         ask_resp = process_ask_request(req)
#         answer_html = ask_resp.response

#         answer_plain = re.sub("<[^<]+?>", "", answer_html)

#         audio_filename = tts_garhwali(answer_plain)
#         audio_url = f"/tts/{audio_filename}"

#         return {
#             "question_text": question_text,
#             "answer_html": answer_html,
#             "audio_url": audio_url,
#             "sources": ask_resp.sources,
#         }

#     finally:
#         try:
#             os.remove(tmp_path)
#         except Exception:
#             pass

# # ================== AUTH ROUTES ==================


# @app.post("/auth/register", response_model=UserRead)
# def register(user_in: UserCreate, session: Session = Depends(get_session)):
#     existing = get_user_by_username(session, user_in.username)
#     if existing:
#         raise HTTPException(status_code=400, detail="Username already registered")

#     user = User(
#         username=user_in.username,
#         full_name=user_in.full_name,
#         hashed_password=get_password_hash(user_in.password),
#         district=user_in.district,
#         block=user_in.block,
#         village_code=user_in.village_code,
#         age=user_in.age,
#         gender=user_in.gender,
#         interest_tag=user_in.interest_tag,
#         disability=user_in.disability,
#         occupation=user_in.occupation,
#         income_bracket=user_in.income_bracket,
#         social_category=user_in.social_category,
#     )
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user


# @app.post("/auth/login", response_model=Token)
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     session: Session = Depends(get_session),
# ):
#     user = get_user_by_username(session, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     token = create_access_token({"sub": user.username})
#     return Token(access_token=token)


# @app.get("/me", response_model=UserRead)
# def read_me(current_user: User = Depends(get_current_user)):
#     return current_user


# @app.put("/me", response_model=UserRead)
# def update_me(
#     user_update: UserUpdate,
#     current_user: User = Depends(get_current_user),
#     session: Session = Depends(get_session),
# ):
#     data = user_update.dict(exclude_unset=True)

#     for field, value in data.items():
#         setattr(current_user, field, value)

#     session.add(current_user)
#     session.commit()
#     session.refresh(current_user)
#     return current_user


# @app.get("/health")
# def health():
#     return {
#         "status": "ok",
#         "docs_collection": DOC_COLLECTION,
#         "schemes_collection": SCHEMES_COLLECTION,
#         "embed_model_schemes": EMBED_MODEL_NAME_SCHEMES,
#     }

















import os
import json
import uuid
import re
import unicodedata
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from dotenv import load_dotenv
from fastapi import (
    FastAPI,
    Request,
    Form,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchText,
)
from qdrant_client.http import models as qm  # noqa: F401

from sentence_transformers import SentenceTransformer
from fastembed import TextEmbedding
from groq import Groq
from googletrans import Translator

from faster_whisper import WhisperModel
from gtts import gTTS

from sqlmodel import Field, SQLModel, Session, create_engine, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# ================== CONFIG ==================

BASE_DIR = Path(__file__).resolve().parent.parent  # repo root

SCHEMES_PATH = BASE_DIR / "samaj_kalyan_vibhag_clean_typed.json"

TTS_OUTPUT_DIR = BASE_DIR / "tts_output"
TTS_OUTPUT_DIR.mkdir(exist_ok=True)

load_dotenv()

# ---- Groq / LLM ----
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY missing in .env")

LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
GROQ_MODEL_DOCS = os.getenv("GROQ_MODEL", LLM_MODEL)

groq_client = Groq(api_key=GROQ_API_KEY)

# ---- DOCS RAG Qdrant ----
DOC_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
DOC_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
DOC_COLLECTION = os.getenv("COLLECTION_NAME", "panchayat_uk_docs")

doc_qclient = QdrantClient(url=DOC_QDRANT_URL, api_key=DOC_QDRANT_API_KEY)
doc_embedder = TextEmbedding()

# ---- Schemes Qdrant (local) ----
EMBED_MODEL_NAME_SCHEMES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SCHEMES_COLLECTION = "samaj_kalyan_vibhag_schemes"

scheme_embed_model = SentenceTransformer(EMBED_MODEL_NAME_SCHEMES)
scheme_qdrant = QdrantClient(path=str(BASE_DIR / "qdrant_data"))

# ---- Whisper ----
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "medium")
USE_CUDA = os.getenv("USE_CUDA", "0") == "1"

whisper_model = WhisperModel(
    WHISPER_MODEL_NAME,
    device="cuda" if USE_CUDA else "cpu",
    compute_type="float16" if USE_CUDA else "int8",
)

# ---- FastAPI ----
app = FastAPI(title="Panchayat Sahayika Unified Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.mount("/tts", StaticFiles(directory=str(TTS_OUTPUT_DIR)), name="tts")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
translator = Translator()

# ================== AUTH / USERS ==================

DATABASE_URL = "sqlite:///./panchayat_users.db"
engine = create_engine(DATABASE_URL, echo=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "baea29ce56f4b02733883b6ae1a76265988d123d5ad3e9d2214dae4646a81ee6",
)
ALGORITHM = "HS256"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    hashed_password: str

    district: Optional[str] = None
    block: Optional[str] = None
    village_code: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    interest_tag: Optional[str] = None

    disability: Optional[str] = None
    occupation: Optional[str] = None
    income_bracket: Optional[str] = None
    social_category: Optional[str] = None


class UserCreate(SQLModel):
    username: str
    password: str
    full_name: Optional[str] = None
    district: Optional[str] = None
    block: Optional[str] = None
    village_code: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    interest_tag: Optional[str] = None

    disability: Optional[str] = None
    occupation: Optional[str] = None
    income_bracket: Optional[str] = None
    social_category: Optional[str] = None


class UserRead(SQLModel):
    id: int
    username: str
    full_name: Optional[str] = None
    district: Optional[str] = None
    block: Optional[str] = None
    village_code: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    interest_tag: Optional[str] = None

    disability: Optional[str] = None
    occupation: Optional[str] = None
    income_bracket: Optional[str] = None
    social_category: Optional[str] = None


class UserUpdate(SQLModel):
    full_name: Optional[str] = None
    district: Optional[str] = None
    block: Optional[str] = None
    village_code: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    interest_tag: Optional[str] = None

    disability: Optional[str] = None
    occupation: Optional[str] = None
    income_bracket: Optional[str] = None
    social_category: Optional[str] = None


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def _bcrypt_safe(password: str) -> str:
    if password is None:
        return ""
    pw_bytes = password.encode("utf-8")
    return pw_bytes[:72].decode("utf-8", errors="ignore")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(_bcrypt_safe(password))


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(_bcrypt_safe(plain), hashed)


def create_access_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    return session.exec(stmt).first()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(session, username=username)
    if not user:
        raise credentials_exception
    return user


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ================== COMMON LANGUAGE + VOICE HELPERS ==================


def contains_devanagari(text: str) -> bool:
    for ch in text:
        if "\u0900" <= ch <= "\u097F":
            return True
    return False


def _llm_translate(text: str, target_desc: str) -> str:
    system_msg = (
        "You are a translator for Gram Panchayat content.\n"
        "You ONLY translate / rewrite the text; you do not add explanations.\n"
        "Preserve markdown bold markers **like this** exactly as they are.\n"
        "Do not change the meaning; only change the language/style.\n"
    )

    user_msg = (
        f"Translate / rewrite the following text into {target_desc}.\n\n"
        f"Text:\n{text}"
    )

    completion = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.25,
        max_tokens=1200,
    )
    out = completion.choices[0].message.content or text
    return out


def translate_answer(text: str, target_lang: str) -> str:
    """
    target_lang:
      - 'en'        -> English
      - 'hi'        -> simple Hindi
      - 'garhwali'  -> Garhwali (Devnagari, village style)
      - 'hinglish'  -> Roman Hindi
    """

    # ---------- English ----------
    if target_lang == "en":
        try:
            res = translator.translate(text, dest="en")
            out = res.text
            if out and not contains_devanagari(out) and out.strip():
                return out
        except Exception:
            pass

        return _llm_translate(
            text,
            "clear, simple English suitable for village-level users. "
            "Avoid Hindi script and use plain English sentences.",
        )

    # ---------- Hindi ----------
    if target_lang == "hi":
        return _llm_translate(
            text,
            "very simple Hindi in Devanagari script, using everyday words "
            "that village-level users understand.",
        )

    # ---------- Garhwali ----------
        # ---------- Garhwali ----------
    if target_lang == "garhwali":
        return _llm_translate(
            text,
            (
                "PURE Central Garhwali (Pauri / Chamoli region) in Devanagari script only. "
                "Rewrite every sentence from simple Hindi into natural village-style Garhwali speech.\n"
                "\n"
                "STRICT RULES:\n"
                "1) Replace Hindi helper verbs like 'hai, hain, tha, thi, the, hoga, karna, karna hai' "
                "with Garhwali forms like 'ch, chan, rai, hondu ch, karanu, karno padul'.\n"
                "2) Use Garhwali pronouns: aap/tum -> 'tyun/tumi', aapka -> 'tyunr', aapko -> 'tyunku/tyunla', "
                "mera -> 'mer', meri -> 'meri', yahan -> 'yan', wahan -> 'tyan'.\n"
                "3) Style must sound like real village speech, not formal Hindi or legal language.\n"
                "4) Do NOT translate names of schemes or departments such as "
                "'प्रधानमंत्री आवास योजना', 'राष्ट्रीय पशुधन मिशन', 'Panchayati Raj Vibhag', "
                "'CSC Center', 'Uttarakhand Jal Sansthan' – keep them as they are inside the sentence.\n"
                "5) Never leave any line in plain Hindi; rewrite every line in Garhwali.\n"
                "6) Never use English letters (Roman script); use Devanagari only.\n"
                "7) Tone should be warm, simple, and like a normal Gaon ki boli.\n"
                "\n"
                "PROJECT EXAMPLES:\n"
                "Hindi: 'यह योजना महिलाओं के लिए है।'\n"
                "Garhwali: 'य योजना महिलां मनुक लागि च.'\n"
                "Hindi: 'विधवा पेंशन के लिए आपको CSC में आवेदन करना होगा।'\n"
                "Garhwali: 'विधवा पेंशन लागि त्यूँकु CSC म आवेदन करणो पडुल.'\n"
                "Hindi: 'आय प्रमाणपत्र के लिए पटवारी से मिलें।'\n"
                "Garhwali: 'आय प्रमाणपत्र लागि पटवारी स्यूँ मिलौ.'\n"
                "Hindi: 'पीने के पानी की समस्या के लिए जल संस्थान से संपर्क करें।'\n"
                "Garhwali: 'पीणखाल पाणी कु झमेलो लागि Uttarakhand Jal Sansthan स्यूँ संपर्क करदी.'\n"
                "Hindi: 'तलाक के लिए आवेदन करने से पहले पति से बात करनी चाहिए।'\n"
                "Garhwali: 'तलाक लागि आवेदन करणै स्यूँ पहलु त्यूँर पतिक संग बोलबात करणु चाहिणु.'\n"
                "\n"
                "Return ONLY the final Garhwali version of the text, with no Hindi or English explanation."
            ),
        )


    # ---------- Hinglish ----------
    return _llm_translate(
        text,
        "very simple Hinglish (Roman Hindi using English letters). "
        "Do NOT use Devanagari characters.",
    )


def _convert_markdown_bold_to_html(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def transcribe_garhwali_audio(path: str) -> str:
    segments, info = whisper_model.transcribe(
        path,
        language="hi",
        task="transcribe",
        vad_filter=True,
    )
    pieces = [seg.text.strip() for seg in segments if seg.text.strip()]
    return " ".join(pieces).strip()


def tts_garhwali(text: str) -> str:
    safe_text = text.strip()
    if len(safe_text) > 1500:
        safe_text = safe_text[:1500]

    filename = f"garhwali_{uuid.uuid4().hex}.mp3"
    out_path = TTS_OUTPUT_DIR / filename

    # अभी Garhwali भी Hindi TTS से ही बोलेगा (hi-IN voice)
    tts = gTTS(text=safe_text, lang="hi")
    tts.save(str(out_path))
    return filename

# ================== DOCS RAG PIPELINE ==================


def build_docs_system_prompt() -> str:
    return (
        "आप 'Panchayat Sahayika' हैं, उत्तराखंड की ग्राम पंचायतों के लिए सहायक।\n"
        "यूज़र कभी-कभी गढ़वाली या हिंग्लिश में भी सवाल पूछ सकते हैं; "
        "आप अर्थ समझकर पहले सरल हिन्दी में जवाब तैयार करें (बाद में ज़रूरत हो तो दूसरी भाषा में अनुवाद होगा)।\n"
        "आपको केवल नीचे दिए गए संदर्भ (official Panchayati Raj documents: acts, rules, "
        "guidelines, roles, schemes, training material) का इस्तेमाल करके ही जवाब देना है।\n\n"
        "भाषा बहुत ही सरल और आसान हिन्दी होनी चाहिए ताकि सरपंच, वार्ड मेंबर और ग्राम पंचायत "
        "कर्मचारी आसानी से समझ सकें।\n"
        "कानूनी भारी शब्दों से बचें।\n"
        "अगर ज़रूरी जानकारी संदर्भ में नहीं है, तो साफ-साफ लिखें कि यह जानकारी उपलब्ध नहीं है "
        "और आप अंदाज़ा नहीं लगा रहे हैं।\n"
        "कभी भी दस्तावेज़ का नाम, फाइल का नाम, पेज नंबर या 'source' list का ज़िक्र न करें।\n"
    )


def retrieve_docs_context(query: str, top_k: int = 8) -> List[Dict[str, Any]]:
    query_vec = list(doc_embedder.embed([query]))[0]
    results = doc_qclient.search(
        collection_name=DOC_COLLECTION,
        query_vector=query_vec,
        limit=top_k,
        with_payload=True,
    )

    contexts = []
    for r in results:
        pl = r.payload or {}
        contexts.append(
            {
                "text": pl.get("text", ""),
                "source_file": pl.get("source_file", ""),
                "page": pl.get("page", ""),
                "url": pl.get("url", ""),
                "score": r.score,
            }
        )
    return contexts


def generate_docs_answer_raw(
    query: str,
    history: List[Dict[str, str]],
    user_meta: Dict[str, Any] | None = None,
) -> Tuple[str, List[Dict[str, Any]]]:
    contexts = retrieve_docs_context(query)
    context_block = "\n\n---\n\n".join(c["text"] for c in contexts if c["text"])

    user_ctx = build_user_context(user_meta)

    system_prompt = build_docs_system_prompt()
    if user_ctx:
        system_prompt += (
            "\n\nउपयोगकर्ता प्रोफाइल (उदाहरणों को practical banane ke liye):\n"
            f"{user_ctx}\n"
            "जवाब में आप user ki स्थिति ke हिसाब से छोटा सा context de sakte hain "
            "(jaise किसान, छात्र, दिव्यांग इत्यादि)."
        )

    messages = [{"role": "system", "content": system_prompt}]

    for h in history[-4:] if history else []:
        messages.append({"role": h["role"], "content": h["content"]})

    messages.append(
        {
            "role": "user",
            "content": (
                f"प्रश्न: {query}\n\n"
                f"नीचे दिए गए दस्तावेज़ों के संदर्भ का उपयोग करके उत्तर दीजिए। "
                f"अपने उत्तर में इन दस्तावेज़ों के नाम या पेज नंबर का ज़िक्र मत कीजिए:\n\n"
                f"{context_block}"
            ),
        }
    )

    completion = groq_client.chat.completions.create(
        model=GROQ_MODEL_DOCS,
        messages=messages,
        temperature=0.3,
        max_tokens=900,
    )
    raw_answer = completion.choices[0].message.content or ""

    unique_sources = []
    seen = set()
    for c in contexts:
        key = (c["source_file"], c["page"])
        if key not in seen and c["source_file"]:
            seen.add(key)
            unique_sources.append(
                {
                    "source_file": c["source_file"],
                    "page": c["page"],
                    "url": c["url"],
                }
            )

    return raw_answer, unique_sources

# ================== SCHEMES PIPELINE ==================


def load_schemes() -> List[Dict[str, Any]]:
    with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for s in data:
        s.setdefault("name_hi", "")
        s.setdefault("name_en", "")
        s.setdefault("category", "")
        s.setdefault("department", "")
        s.setdefault("description_hi", "")
        s.setdefault("description_en", "")
        s.setdefault("eligibility", "")
        s.setdefault("benefit", "")
        s.setdefault("apply_process", "")
        s.setdefault("apply_link", "")
        s.setdefault("source_url", "")
        s.setdefault("type", s.get("type", "scheme"))
    return data


def _concat_item_text(s: Dict[str, Any]) -> str:
    name = (s.get("name_hi", "") + " " + s.get("name_en", "")).strip()
    other_parts = [
        s.get("category", ""),
        s.get("department", ""),
        s.get("description_hi", ""),
        s.get("description_en", ""),
        s.get("eligibility", ""),
        s.get("benefit", ""),
        s.get("apply_process", ""),
    ]
    weighted_name = " ".join([name] * 5) if name else ""
    rest = " | ".join([str(p) for p in other_parts if p])
    return " | ".join([p for p in [weighted_name, rest] if p])


def init_schemes_collection():
    schemes = load_schemes()

    scheme_qdrant.recreate_collection(
        collection_name=SCHEMES_COLLECTION,
        vectors_config=VectorParams(
            size=scheme_embed_model.get_sentence_embedding_dimension(),
            distance=Distance.COSINE,
        ),
    )

    points: List[PointStruct] = []
    for s in schemes:
        vec = scheme_embed_model.encode(_concat_item_text(s)).tolist()
        payload = dict(s)
        payload["__search_blob"] = _concat_item_text(s)
        points.append(PointStruct(id=str(uuid.uuid4()), vector=vec, payload=payload))

    scheme_qdrant.upsert(SCHEMES_COLLECTION, points)
    print(f"✅ Indexed {len(points)} schemes into Qdrant (schemes collection)")


init_schemes_collection()


def _norm(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def _qdrant_filter(
    category: Optional[str],
    department: Optional[str],
    typ: Optional[str],
) -> Optional[Filter]:
    conds = []
    if category:
        conds.append(FieldCondition(key="category", match=MatchText(text=category)))
    if department:
        conds.append(FieldCondition(key="department", match=MatchText(text=department)))
    if typ:
        conds.append(FieldCondition(key="type", match=MatchText(text=typ)))
    if not conds:
        return None
    return Filter(must=conds)


def _keyword_boost(question: str, item: Dict[str, Any]) -> float:
    q = _norm(question)
    name = _norm((item.get("name_hi", "") + " " + item.get("name_en", "")))
    cat = _norm(item.get("category", ""))
    dept = _norm(item.get("department", ""))

    boost = 0.0
    if q and q in name:
        boost += 0.6

    q_words = [w for w in q.split() if len(w) > 2]
    for w in q_words:
        if w in name or w in cat or w in dept:
            boost += 0.15

    return boost


def search_schemes(
    question: str,
    limit: int = 3,
    page: int = 1,
    min_score: float = 0.20,
    category: Optional[str] = None,
    department: Optional[str] = None,
    typ: Optional[str] = None,
):
    qvec = scheme_embed_model.encode(question).tolist()
    page = max(page, 1)
    limit = max(1, min(20, limit))

    MAX_HITS = 50

    hits = scheme_qdrant.search(
        collection_name=SCHEMES_COLLECTION,
        query_vector=qvec,
        limit=MAX_HITS,
        with_payload=True,
        with_vectors=False,
        query_filter=_qdrant_filter(category, department, typ),
    )

    scored: List[Dict[str, Any]] = []
    for h in hits:
        base_score = float(h.score) if hasattr(h, "score") else 0.0
        if base_score < min_score:
            continue
        p = dict(h.payload)
        kw_boost = _keyword_boost(question, p)
        final_score = base_score + kw_boost
        p["_score"] = base_score
        p["_final_score"] = final_score
        scored.append(p)

    deduped: List[Dict[str, Any]] = []
    seen = set()
    for p in scored:
        key = (p.get("name_hi") or p.get("name_en") or "").strip()
        if not key:
            key = p.get("id", "")
        if key in seen:
            continue
        seen.add(key)
        deduped.append(p)

    deduped.sort(key=lambda x: x.get("_final_score", 0.0), reverse=True)

    total = len(deduped)
    start = (page - 1) * limit
    end = start + limit
    page_items = deduped[start:end]

    return page_items, total


def _fmt_scheme_card(s: Dict[str, Any]) -> str:
    name = s.get("name_hi") or s.get("name_en") or "—"
    bits = [
        f"• **{name}**",
        f"  - 🎓 पात्रता: {s.get('eligibility','उपलब्ध नहीं')}",
        f"  - 💰 लाभ: {s.get('benefit','उपलब्ध नहीं')}",
        f"  - 📝 आवेदन: {s.get('apply_process','उपलब्ध नहीं')}",
    ]
    if s.get("apply_link"):
        bits.append(f"  - 🔗 लिंक: {s['apply_link']}")
    return "\n".join(bits)


def build_user_context(user_meta: dict | None) -> str:
    if not user_meta:
        return ""

    district = user_meta.get("district")
    block = user_meta.get("block")
    village = user_meta.get("village_code")
    age = user_meta.get("age")
    gender = user_meta.get("gender")
    interest = user_meta.get("interest_tag")

    disability = user_meta.get("disability")
    occupation = user_meta.get("occupation")
    income_bracket = user_meta.get("income_bracket")
    social_category = user_meta.get("social_category")

    parts = []

    if district:
        parts.append(f"जिला {district}")
    if block:
        parts.append(f"ब्लॉक {block}")
    if village:
        parts.append(f"गाँव कोड {village}")
    if age:
        parts.append(f"आयु {age} वर्ष")
    if gender:
        parts.append(f"लिंग {gender}")
    if occupation:
        parts.append(f"पेशा: {occupation}")
    if income_bracket:
        parts.append(f"आय वर्ग: {income_bracket}")
    if social_category:
        parts.append(f"सोशल कैटेगरी: {social_category}")
    if disability and disability.lower() not in ("none", "nahin", "no"):
        parts.append(f"विशेष आवश्यकताएँ / दिव्यांगता: {disability}")
    if interest:
        parts.append(f"रुचि: {interest}")

    if not parts:
        return ""

    return "उपयोगकर्ता की जानकारी: " + ", ".join(parts) + ". "


def build_schemes_answer(
    question: str,
    schemes: List[Dict[str, Any]],
    user_meta: Dict[str, Any] | None = None,
) -> str:
    if not schemes:
        return (
            "माफ़ कीजिए, इस सवाल से मिलती-जुलती कोई योजना नहीं मिली। "
            "कृपया अलग शब्दों में पूछें, या ज़िला/विभाग/श्रेणी लिखें।\n\n"
            "**English:** No strong matches. Try different words or add location/department."
        )

    user_ctx = build_user_context(user_meta)

    q_low = question.lower()
    want_apply = any(
        w in q_low
        for w in [
            "apply",
            " आवेदन",
            "आवेदन",
            "फॉर्म",
            "form",
            "कैसे",
            "kaise",
            "कहाँ",
            "kaha",
            "कहां",
        ]
    )
    want_benefit = any(
        w in q_low
        for w in [
            "लाभ",
            "benefit",
            "paisa",
            "₹",
            "kitna",
            "कितना",
            "राशि",
        ]
    )
    want_elig = any(
        w in q_low
        for w in [
            "पात्रता",
            "eligibility",
            "kaun",
            "कौन",
            "किसको",
            "kis ko",
            "kisko",
        ]
    )

    if not GROQ_API_KEY:
        hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
        body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
        eng = (
            "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
        )
        return hdr + body + eng

    context_lines = []
    for s in schemes:
        context_lines.append(
            "योजना: {name}\nविवरण: {desc}\nपात्रता: {elig}\nलाभ: {ben}\nआवेदन प्रक्रिया: {proc}\nविभाग: {dept}\nश्रेणी: {cat}\nलिंक: {link}\n".format(
                name=(s.get("name_hi") or s.get("name_en") or ""),
                desc=s.get("description_hi", ""),
                elig=s.get("eligibility", ""),
                ben=s.get("benefit", ""),
                proc=s.get("apply_process", ""),
                dept=s.get("department", ""),
                cat=s.get("category", ""),
                link=s.get("apply_link", ""),
            )
        )
    context = "\n---\n".join(context_lines)

    focus_lines = []
    if want_apply:
        focus_lines.append(
            "- User is mainly asking **how to apply**. "
            "You MUST explain the पूरा 'आवेदन प्रक्रिया' field step-by-step in simple Hindi. "
            "हर ज़रूरी स्टेप और हर ज़रूरी दस्तावेज़ का नाम जरूर बताएं।"
        )
    if want_benefit:
        focus_lines.append(
            "- User is asking about **benefits / amount**. "
            "Explain the 'लाभ' field completely. अलग-अलग राशि हो तो सब बताएं।"
        )
    if want_elig:
        focus_lines.append(
            "- User is asking about **eligibility / who can get it**. "
            "Explain the 'पात्रता' field पूरी तरह, सभी शर्तें (1, 2, 3...) अलग-अलग लिखें।"
        )

    focus_text = "\n".join(focus_lines) if focus_lines else "- Follow the general rules below."

    profile_text = user_ctx or "कोई अतिरिक्त उपयोगकर्ता जानकारी उपलब्ध नहीं है। अगर जानकारी ना हो तो generic जवाब दें।"

    prompt = f"""
You are **Panchayat Sahayika**, a friendly, polite and knowledgeable AI assistant created to help rural citizens of India. 
Your main goal is to explain information in very **simple, clear, human-like Hindi**, so that even villagers, elderly people, 
and first-time smartphone users can easily understand.

User profile (for context, don't repeat fully, just use it smartly in examples):
{profile_text}

You must use **only** the information given in the schemes context below. 
Do NOT invent or guess any benefits, eligibility rules, amounts or links that are not present.

--------------------------------------------
📌 USER QUESTION:
{question}

📌 RELEVANT SCHEMES (if matched):
{context}
--------------------------------------------

### 🔍 SPECIAL FOCUS (based on the user's question)
{focus_text}

### 🟢 MAIN RULES FOR ANSWERING:
- Explain in **simple conversational Hindi**, short sentences, and natural flow.  
- Do NOT sound robotic. Do NOT dump raw data.  
- Be clear, warm, and practical.
- Whenever you write the name of any scheme / yojana, always wrap it like this: `**PM Awas Yojana**`.

Include these only if available in provided context:
- योज़ना / स्कीम का नाम  
- यह किसके लिए है (पात्रता)  
- कितना लाभ मिलता है (लाभ)  
- कैसे और कहाँ आवेदन करना है (आवेदन प्रक्रिया)  
- लिंक हो तो बताएं  

If multiple schemes match, explain **2–3** clearly but naturally.
Missing data → write “उपलब्ध नहीं” naturally.

### 🟡 ALWAYS END WITH:
"अगर ज़रूरत हो तो अपने ग्राम पंचायत या CSC केंद्र से मदद लें।"

### 🌍 AFTER THE HINDI ANSWER:
Give one short English summary sentence (not detailed).

--------------------------------------------
Now write the final answer in a natural, fluent, friendly tone.
--------------------------------------------
"""

    try:
        completion = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        ai_answer = completion.choices[0].message.content.strip()
    except Exception:
        hdr = f"आपके सवाल के आधार पर {len(schemes)} योजनाएँ मिलीं:\n\n"
        body = "\n\n".join(_fmt_scheme_card(s) for s in schemes)
        eng = (
            "\n\n**English:** Listed top matches with eligibility, benefits and how to apply."
        )
        return hdr + body + eng

    return ai_answer


def _should_use_schemes(question: str, schemes: List[Dict[str, Any]]) -> bool:
    if not schemes:
        return False

    top = schemes[0]
    top_final = float(top.get("_final_score", top.get("_score", 0.0)) or 0.0)

    q = question.lower()
    has_scheme_word = any(
        w in q
        for w in [
            "योजना",
            "yojana",
            "scheme",
            "स्कीम",
            "pension",
            "पेंशन",
            "subsidy",
            "सब्सिडी",
            "बीमा",
            "insurance",
            "scholarship",
            " छात्रवृत्ति",
        ]
    )

    if top_final >= 0.60:
        return True

    if has_scheme_word and top_final >= 0.25:
        return True

    return False

# ================== ASK MODELS ==================


class AskRequest(BaseModel):
    question: str
    ui_lang: str = "hi"
    mode: str = "auto"         # "auto" | "docs" | "schemes"
    history: List[Dict[str, str]] = []
    user_meta: Dict[str, Any] | None = None


class AskResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []
    audio_url: Optional[str] = None


class SchemeCard(SQLModel):
    title: str
    subtitle: Optional[str] = None
    verified: bool = True
    badges: List[str] = []
    apply_url: Optional[str] = None
    read_more_url: Optional[str] = None

# ================== RECOMMENDATIONS ==================


@app.get("/user/recommended-schemes", response_model=List[SchemeCard])
def recommended_schemes(current_user: User = Depends(get_current_user)):
    parts = []

    if current_user.district:
        parts.append(current_user.district)
    if current_user.block:
        parts.append(current_user.block)
    if current_user.gender:
        parts.append(current_user.gender)
    if current_user.age:
        parts.append(f"age {current_user.age}")
    if current_user.interest_tag:
        parts.append(current_user.interest_tag)

    if current_user.occupation:
        parts.append(current_user.occupation)
    if current_user.disability and current_user.disability.lower() not in (
        "none",
        "nahin",
        "no",
    ):
        parts.append("divyang")
        parts.append(current_user.disability)
    if current_user.income_bracket:
        parts.append(current_user.income_bracket)
    if current_user.social_category:
        parts.append(current_user.social_category)

    question = " ".join(parts) or "gramin yojana"

    schemes, _total = search_schemes(
        question=question,
        limit=5,
        page=1,
        min_score=0.20,
        category=None,
        department=None,
        typ=None,
    )

    cards: List[SchemeCard] = []
    for s in schemes:
        title = (
            (s.get("name_hi") or "")
            + (" / " + s.get("name_en", "") if s.get("name_en") else "")
        ).strip(" /")
        subtitle = s.get("description_hi") or s.get("description_en") or ""
        badges = [s.get("department", ""), s.get("category", "")]
        cards.append(
            SchemeCard(
                title=title or "Yojana",
                subtitle=subtitle,
                verified=True,
                badges=[b for b in badges if b],
                apply_url=s.get("apply_link") or None,
                read_more_url=s.get("source_url") or None,
            )
        )
    return cards

# ================== HTML DEMO ROUTES ==================


@app.get("/", response_class=HTMLResponse)
async def get_home(
    request: Request,
    lang: str = "hi",
    mode: str = "docs",
):
    if lang not in ("hi", "en", "garhwali"):
        lang = "hi"
    if mode not in ("docs", "schemes"):
        mode = "docs"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "messages": [],
            "history_json": "[]",
            "lang": lang,
            "mode": mode,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def post_query(
    request: Request,
    query: str = Form(...),
    history_json: str = Form("[]"),
    ui_lang: str = Form("hi"),
    mode: str = Form("docs"),
):
    try:
        history = json.loads(history_json)
    except Exception:
        history = []

    if ui_lang == "en":
        target_lang = "en"
    elif ui_lang == "garhwali":
        target_lang = "garhwali"
    else:
        target_lang = "hi" if contains_devanagari(query) else "hinglish"

    if mode == "schemes":
        schemes, _ = search_schemes(
            question=query,
            limit=3,
            page=1,
            min_score=0.20,
            category=None,
            department=None,
            typ=None,
        )
        base_answer = build_schemes_answer(query, schemes)
    else:
        base_answer, _sources = generate_docs_answer_raw(query, history)

    final_text = translate_answer(base_answer, target_lang)
    answer_html = _convert_markdown_bold_to_html(final_text)

    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": answer_html})

    messages = [{"role": h["role"], "content": h["content"]} for h in history]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "messages": messages,
            "history_json": json.dumps(history, ensure_ascii=False),
            "lang": ui_lang,
            "mode": mode,
        },
    )

# ================== CORE ASK LOGIC ==================


def process_ask_request(req: AskRequest) -> AskResponse:
    # UI language se target lang decide
    if req.ui_lang == "en":
        target_lang = "en"
    elif req.ui_lang == "garhwali":
        target_lang = "garhwali"
    else:
        target_lang = "hi" if contains_devanagari(req.question) else "hinglish"

    user_meta = req.user_meta or None

    schemes: List[Dict[str, Any]] = []
    doc_sources: List[Dict[str, Any]] = []
    use_schemes = False

    # ---------- routing: schemes vs docs ----------
    if req.mode in ("schemes", "auto"):
        schemes, _ = search_schemes(
            question=req.question,
            limit=5,
            page=1,
            min_score=0.20,
            category=None,
            department=None,
            typ=None,
        )
        if req.mode == "schemes":
            use_schemes = True
        else:
            use_schemes = _should_use_schemes(req.question, schemes)

    if use_schemes:
        base_answer = build_schemes_answer(req.question, schemes, user_meta=user_meta)
        sources = [
            {
                "name_hi": s.get("name_hi"),
                "name_en": s.get("name_en"),
                "score": s.get("_score"),
                "department": s.get("department"),
                "category": s.get("category"),
                "apply_link": s.get("apply_link"),
            }
            for s in schemes
        ]
    else:
        base_answer, doc_sources = generate_docs_answer_raw(
            req.question,
            req.history,
            user_meta=user_meta,
        )
        sources = doc_sources

    # ---------- translate to requested UI language ----------
    final_text = translate_answer(base_answer, target_lang)
    final_html = _convert_markdown_bold_to_html(final_text)

    # ---------- TTS for Garhwali (audio_url) ----------
    audio_url: Optional[str] = None
    if req.ui_lang == "garhwali":
        # strip HTML to get plain text
        plain = re.sub("<[^<]+?>", "", final_html)
        if plain.strip():
            filename = tts_garhwali(plain)
            audio_url = f"/tts/{filename}"

    return AskResponse(response=final_html, sources=sources, audio_url=audio_url)

# ================== JSON API FOR REACT CHAT ==================


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    return process_ask_request(req)


@app.post("/voice/ask")
async def voice_ask(
    audio: UploadFile = File(...),
    mode: str = "auto",
    ui_lang: str = "garhwali",
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        shutil.copyfileobj(audio.file, tmp)
        tmp_path = tmp.name

    try:
        question_text = transcribe_garhwali_audio(tmp_path)

        req = AskRequest(
            question=question_text,
            ui_lang=ui_lang,
            mode=mode,
            history=[],
            user_meta=None,
        )

        ask_resp = process_ask_request(req)
        answer_html = ask_resp.response
        answer_plain = re.sub("<[^<]+?>", "", answer_html)

        audio_filename = tts_garhwali(answer_plain)
        audio_url = f"/tts/{audio_filename}"

        return {
            "question_text": question_text,
            "answer_html": answer_html,
            "audio_url": audio_url,
            "sources": ask_resp.sources,
        }

    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

# ================== AUTH ROUTES ==================


@app.post("/auth/register", response_model=UserRead)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    existing = get_user_by_username(session, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        district=user_in.district,
        block=user_in.block,
        village_code=user_in.village_code,
        age=user_in.age,
        gender=user_in.gender,
        interest_tag=user_in.interest_tag,
        disability=user_in.disability,
        occupation=user_in.occupation,
        income_bracket=user_in.income_bracket,
        social_category=user_in.social_category,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.post("/auth/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token({"sub": user.username})
    return Token(access_token=token)


@app.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.put("/me", response_model=UserRead)
def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    data = user_update.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(current_user, field, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@app.get("/health")
def health():
    return {
        "status": "ok",
        "docs_collection": DOC_COLLECTION,
        "schemes_collection": SCHEMES_COLLECTION,
        "embed_model_schemes": EMBED_MODEL_NAME_SCHEMES,
    }

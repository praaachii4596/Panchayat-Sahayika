# import os
# import json
# import uuid
# import re
# import unicodedata
# import tempfile
# import shutil
# from pathlib import Path
# from typing import List, Dict, Any, Optional, Tuple
# from difflib import SequenceMatcher
# import torch
# from transformers import MT5ForConditionalGeneration, MT5Tokenizer
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

# BASE_DIR = Path(__file__).resolve().parent.parent  # repo root

# SCHEMES_PATH = BASE_DIR / "samaj_kalyan_vibhag_clean_typed.json"

# TTS_OUTPUT_DIR = BASE_DIR / "tts_output"
# TTS_OUTPUT_DIR.mkdir(exist_ok=True)

# # ---- Hindi -> Garhwali custom dataset ----
# # Expected file: list of objects like
# # [
# #   {"input": "आवेदक के पास बैंक खाता होना आवश्यक है।",
# #    "output": "आवेदक कु पास बैंकु खाता होणो जरूरी छ।"},
# #   ...
# # ]
# GARHWALI_DATA_PATH = BASE_DIR / "dataset_final.json"

# # ---- Hindi -> Garhwali rule-based replacements ----

# GARHWALI_RULES = [
#     # 1. negatives + modals
#     (r"नहीं होना चाहिए", "नीं होयु चयेने"),
#     (r"नहीं होना चाहिए।", "नीं होयु चयेने।"),

#     # 2. ke liye -> khatar
#     (r"के लिए", "खातर"),
#     (r"के लिये", "खातर"),

#     # 3. ke tahat -> ku tahat
#     (r"के तहत", "कु तहत"),

#     # 4. genitive ka/ke/ki -> ku
#     (r"([^\s]+) का ", r"\1 कु "),
#     (r"([^\s]+) के ", r"\1 कु "),
#     (r"([^\s]+) की ", r"\1 कु "),

#     # 5. में -> म
#     (r" में ", " म "),

#     # 6. hona chahiye
#     (r"होना चाहिए।", "होयु चयेने।"),
#     (r"होना चाहिए", "होयु चयेने"),
#     (r"होनी चाहिए।", "होई चयेने।"),
#     (r"होनी चाहिए", "होई चयेने"),

#     # 7. se kam honi chahiye
#     (r"से कम होनी चाहिए", "से कम होई चयेने"),

#     # 8. hai -> ch
#     (r" है।", " छ।"),
#     (r" है?", " छ?"),
#     (r" है ", " छ "),

#     # 9. upalabdh / aavashyak / anivarya / aarakshit
#     (r"उपलब्ध छ है", "उपलब्ध छ"),  # safety
#     (r"उपलब्ध है", "उपलब्ध छ"),
#     (r"आरक्षित है", "आरक्षित छ"),
#     (r"अनिवार्य है", "अनिवार्य छ"),
#     (r"जरूरी है", "जरूरी छ"),
#     (r"आवश्यक है", "आवश्यक छ"),

#     # 10. dia jayega / di jayegi
#     (r"दिया जाएगा।", "दिउँ जालु।"),
#     (r"दिया जाएगा", "दिउँ जालु"),
#     (r"दी जाएगी।", "दिज़ली जाली।"),
#     (r"दी जाएगी", "दिज़ली जाली"),

#     (r"प्रदान की जाएगी", "प्रदान कु जाएगी"),
#     (r"प्रदान की जाती है", "प्रदान कु जाती छ"),

#     # 11. jama / bharna
#     (r"जमा करनी होगी", "जमा करनु होलु"),
#     (r"जमा करना होगा", "जमा करनु होलु"),
#     (r"भरना होगा", "भरनु होलु"),
#     (r"भरने के बाद", "भरने कु बाद"),

#     # 12. le sakte hain
#     (r"ले सकते हैं।", "ले सकद्या छौं।"),
#     (r"ले सकते हैं", "ले सकद्या छौं"),
# ]


# def apply_garhwali_rules(text: str) -> str:
#     """
#     Hindi → Garhwali output par rule-based post-processing.
#     LLM/MT5 se aane wale sentences ko thoda aur natural Garhwali banata hai.
#     """
#     if not text:
#         return text

#     out = text
#     for pattern, repl in GARHWALI_RULES:
#         out = re.sub(pattern, repl, out)
#     return out.strip()


# def _load_garhwali_examples() -> List[Tuple[str, str]]:
#     """
#     Load parallel Hindi->Garhwali examples from JSON or JSONL.
#     Tries multiple common key names so that your existing 60-line
#     file will work even if keys are slightly different.
#     """
#     if not GARHWALI_DATA_PATH.exists():
#         return []

#     pairs: List[Tuple[str, str]] = []
#     try:
#         # Try normal JSON first
#         with open(GARHWALI_DATA_PATH, "r", encoding="utf-8") as f:
#             data = json.load(f)
#         if isinstance(data, dict):
#             data = data.get("data") or data.get("examples") or []
#     except Exception:
#         # Fallback: maybe JSONL
#         data = []
#         with open(GARHWALI_DATA_PATH, "r", encoding="utf-8") as f:
#             for line in f:
#                 line = line.strip()
#                 if not line:
#                     continue
#                 try:
#                     data.append(json.loads(line))
#                 except Exception:
#                     continue

#     for row in data:
#         if not isinstance(row, dict):
#             continue
#         hi = (
#             row.get("input")
#             or row.get("hindi")
#             or row.get("source")
#             or row.get("text_hi")
#             or row.get("text")
#         )
#         gw = (
#             row.get("output")
#             or row.get("garhwali")
#             or row.get("target")
#             or row.get("text_gw")
#         )
#         if hi and gw:
#             hi = hi.strip()
#             gw = gw.strip()
#             if hi and gw:
#                 pairs.append((hi, gw))

#     return pairs


# GARHWALI_EXAMPLES: List[Tuple[str, str]] = _load_garhwali_examples()

# load_dotenv()

# # ---- Garhwali MT5 fine-tuned model ----
# GARHWALI_MODEL_PATH = os.getenv(
#     "GARHWALI_MODEL_PATH",
#     str(BASE_DIR / "garhwali_mt5_finetuned"),  # put your folder here
# )

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# try:
#     gw_tokenizer = MT5Tokenizer.from_pretrained(GARHWALI_MODEL_PATH)
#     gw_model = MT5ForConditionalGeneration.from_pretrained(
#         GARHWALI_MODEL_PATH
#     ).to(DEVICE)
#     print(f"✅ Loaded Garhwali MT5 model from: {GARHWALI_MODEL_PATH}")
# except Exception as e:
#     print("⚠️ Could not load Garhwali MT5 model, will use Groq fallback:", e)
#     gw_tokenizer = None
#     gw_model = None

# # ---- Groq / LLM ----
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise RuntimeError("GROQ_API_KEY missing in .env")

# LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
# GROQ_MODEL_DOCS = os.getenv("GROQ_MODEL", LLM_MODEL)

# groq_client = Groq(api_key=GROQ_API_KEY)

# # ---- DOCS RAG Qdrant ----
# DOC_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# DOC_QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
# DOC_COLLECTION = os.getenv("COLLECTION_NAME", "panchayat_uk_docs")

# doc_qclient = QdrantClient(url=DOC_QDRANT_URL, api_key=DOC_QDRANT_API_KEY)
# doc_embedder = TextEmbedding()

# # ---- Schemes Qdrant (local) ----
# EMBED_MODEL_NAME_SCHEMES = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# SCHEMES_COLLECTION = "samaj_kalyan_vibhag_schemes"

# scheme_embed_model = SentenceTransformer(EMBED_MODEL_NAME_SCHEMES)
# scheme_qdrant = QdrantClient(path=str(BASE_DIR / "qdrant_data"))

# # ---- Whisper ----
# WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "medium")
# USE_CUDA = os.getenv("USE_CUDA", "0") == "1"

# whisper_model = WhisperModel(
#     WHISPER_MODEL_NAME,
#     device="cuda" if USE_CUDA else "cpu",
#     compute_type="float16" if USE_CUDA else "int8",
# )

# # ---- FastAPI ----
# app = FastAPI(title="Panchayat Sahayika Unified Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )

# app.mount("/tts", StaticFiles(directory=str(TTS_OUTPUT_DIR)), name="tts")

# templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
# translator = Translator()

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


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str = Field(index=True, unique=True)
#     full_name: Optional[str] = None
#     hashed_password: str

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
#     return pwd_context.hash(_bcrypt_safe(password))


# def verify_password(plain: str, hashed: str) -> bool:
#     return pwd_context.verify(_bcrypt_safe(plain), hashed)


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

# def _llm_translate(text: str | None, instruction: str) -> str:
#     """
#     Generic helper: use Groq LLM to rewrite `text` according to `instruction`.
#     Always returns a string (never None).
#     """
#     if text is None:
#         text = ""

#     prompt = f"""
# Instruction:
# {instruction}

# Input text:
# {text}

# Now rewrite the text according to the instruction.
# """

#     try:
#         completion = groq_client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=[
#                 {"role": "system", "content": "You rewrite text as requested."},
#                 {"role": "user", "content": prompt},
#             ],
#             temperature=0.3,
#             max_tokens=800,
#         )
#         out = completion.choices[0].message.content
#         if not out:
#             return text
#         return out.strip()
#     except Exception as e:
#         print("⚠️ _llm_translate error:", e)
#         return text



# def _most_similar_garhwali_example(
#     text: str, threshold: float = 0.92
# ) -> Optional[str]:
#     """
#     For short Hindi lines (like eligibility bullets), see if we have
#     almost-exact match in the dataset. If yes, directly return
#     the Garhwali from dataset (no LLM needed).
#     """
#     if not GARHWALI_EXAMPLES:
#         return None

#     best_score = 0.0
#     best_out: Optional[str] = None
#     for hi, gw in GARHWALI_EXAMPLES:
#         score = SequenceMatcher(None, text, hi).ratio()
#         if score > best_score:
#             best_score = score
#             best_out = gw

#     if best_score >= threshold:
#         return best_out
#     return None

# # --- Small helpers for Garhwali translation ---

# SENTENCE_SPLIT_RE = re.compile(r"(?<=[।!?])\s+|\n+")


# def _split_hindi_sentences(text: str) -> List[str]:
#     """
#     Split long Hindi paragraph into smaller sentence-like chunks,
#     so that MT5 + rules can translate line-by-line.
#     """
#     if not text:
#         return []
#     parts = [p.strip() for p in SENTENCE_SPLIT_RE.split(text) if p.strip()]
#     return parts


# ENGLISH_LINE_RE = re.compile(r"^\s*(\*\*English\*\*|English:)", re.IGNORECASE)


# def _strip_english_for_garhwali(text: str) -> str:
#     """
#     remove the final English summary etc. before sending to Garhwali model,
#     because MT5 was trained only on Hindi → Garhwali.
#     """
#     lines = text.splitlines()
#     kept: List[str] = []
#     for ln in lines:
#         if ENGLISH_LINE_RE.match(ln):
#             # skip English summary lines
#             continue
#         kept.append(ln)
#     return "\n".join(kept).strip()

# def _llm_translate_garhwali_with_examples(text: str) -> str:
#     """
#     Main Hindi -> Garhwali translator:

#     0) For long paragraphs, first split into Hindi sentences and translate
#        each sentence separately, then join back.
#     1) If a short line is very similar to a known dataset line, use dataset output (+ rules).
#     2) Otherwise, if fine-tuned MT5 model is available, use that (+ rules).
#     3) If model is not available, fallback to Groq LLM few-shot prompt (+ rules).
#     """
#     clean = text.strip()
#     if not clean:
#         return clean

#     # 0) If text is long or multi-line, do sentence-wise translation
#     if len(clean) > 220 or "\n" in clean:
#         sentences = _split_hindi_sentences(clean)
#         out_sentences: List[str] = []
#         for s in sentences:
#             gw = _llm_translate_garhwali_with_examples(s)
#             if gw:
#                 out_sentences.append(gw)
#         # join with space – sentences already include their own "।" / "?" etc.
#         return " ".join(out_sentences).strip()

#     # 1) Direct lookup for short, formulaic lines (eligibility, bullets, etc.)
#     if len(clean) <= 140:
#         direct = _most_similar_garhwali_example(clean)
#         if direct:
#             return apply_garhwali_rules(direct)

#     # 2) Use fine-tuned MT5 model if available
#     if gw_model is not None and gw_tokenizer is not None:
#         try:
#             input_text = f"translate Hindi to Garhwali: {clean}"

#             inputs = gw_tokenizer(
#                 input_text,
#                 return_tensors="pt",
#                 truncation=True,
#                 padding=True,
#                 max_length=256,
#             ).to(DEVICE)

#             outputs = gw_model.generate(
#                 **inputs,
#                 max_length=256,
#                 num_beams=4,
#             )

#             decoded = gw_tokenizer.decode(outputs[0], skip_special_tokens=True)
#             decoded = decoded.strip()
#             # Post-process with handcrafted rules
#             return apply_garhwali_rules(decoded)
#         except Exception as e:
#             print("⚠️ Error in Garhwali MT5 translation, falling back to Groq:", e)

#     # 3) Fallback: Groq LLM with few-shot examples (old behaviour)
#     examples = GARHWALI_EXAMPLES[:10]
#     ex_lines = []
#     for hi, gw in examples:
#         ex_lines.append(f"Hindi: {hi}\nGarhwali: {gw}")
#     examples_block = "\n\n".join(ex_lines)

#     system_msg = (
#         "You are a native Garhwali speaker from rural Uttarakhand. "
#         "Your job is to rewrite Hindi text into pure, natural village-style Garhwali "
#         "in Devanagari script only. Do NOT explain, only translate / rewrite.\n"
#     )

#     user_msg = f"""
# नीचे कुछ उदाहरण दिए गए हैं कि हमें Hindi से Garhwali में कैसे भाषा बदलनी है:

# {examples_block}

# अब नीचे दिए गए पूरे टेक्स्ट को उसी स्टाइल में Garhwali में बदलो:

# Hindi text:
# {clean}

# सिर्फ final Garhwali version दो, बिना किसी extra explanation के.
# ध्यान रहे:
# - 'है, हैं, था, थे, होगा' जैसे शब्दों को Garhwali रूपों से बदलना है (जैसे 'छ, छन, ह्वे, पडुल' आदि).
# - Tone हमेशा गाँव की normal बोली जैसा हो, ज़्यादा legal / किताब वाली Hindi मत रखो.
# - Scheme / department के नाम (जैसे 'प्रधानमंत्री आवास योजना', 'Uttarakhand Jal Sansthan') Hindi में जैसे हैं वैसे ही रहने दो.
# """

#     try:
#         completion = groq_client.chat.completions.create(
#             model=LLM_MODEL,
#             messages=[
#                 {"role": "system", "content": system_msg},
#                 {"role": "user", "content": user_msg},
#             ],
#             temperature=0.25,
#             max_tokens=1200,
#         )
#         raw_out = completion.choices[0].message.content or clean
#         raw_out = raw_out.strip()
#         final_out = apply_garhwali_rules(raw_out)
#         return final_out
#     except Exception:
#         # last-resort: return original Hindi (better than wrong Garhwali)
#         return clean



# def translate_answer(text: str, target_lang: str) -> str:
#     """
#     target_lang:
#       - 'en'        -> English
#       - 'hi'        -> simple Hindi
#       - 'garhwali'  -> Garhwali (Devnagari, village style)
#       - 'hinglish'  -> Roman Hindi
#     """

#     # ---------- English ----------
#     if target_lang == "en":
#         try:
#             res = translator.translate(text, dest="en")
#             out = res.text
#             if out and not contains_devanagari(out) and out.strip():
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
#         # remove English summary etc. before sending to MT5
#         hindi_only = _strip_english_for_garhwali(text)
#         return _llm_translate_garhwali_with_examples(hindi_only)

#     # ---------- Hinglish ----------
#     return _llm_translate(
#         text,
#         "very simple Hinglish (Roman Hindi using English letters). "
#         "Do NOT use Devanagari characters.",
#     )



# def translate_answer(text: str | None, target_lang: str) -> str:
#     """
#     target_lang:
#       - 'en'        -> English
#       - 'hi'        -> simple Hindi
#       - 'garhwali'  -> Garhwali (Devnagari, village style)
#       - 'hinglish'  -> Roman Hindi
#     """
#     if text is None:
#         text = ""


#     # ---------- English ----------
#     if target_lang == "en":
#         try:
#             res = translator.translate(text, dest="en")
#             out = res.text
#             if out and not contains_devanagari(out) and out.strip():
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
#         # Flow jo tu chah raha hai:
#         # 1) Pehle ensure text simple Hindi ho
#         # 2) Fir us Hindi paragraph ko line-by-line Garhwali me MT5 se translate karo
#         if not contains_devanagari(text):
#             # Agar kisi wajah se answer English ya Hinglish aa gaya ho
#             text_hi = _llm_translate(
#                 text,
#                 "very simple Hindi in Devanagari script, using everyday words "
#                 "that village-level users understand.",
#             )
#         else:
#             text_hi = text
#         return _llm_translate_garhwali_with_examples(text_hi)

#     # ---------- Hinglish ----------
#     return _llm_translate(
#         text,
#         "very simple Hinglish (Roman Hindi using English letters). "
#         "Do NOT use Devanagari characters.",
#     )


# def _convert_markdown_bold_to_html(text: str | None) -> str:
#     """
#     Convert **bold** markdown to <strong>bold</strong>.
#     If text is None, return empty string to avoid TypeError.
#     """
#     if not isinstance(text, str):
#         return ""
#     return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)



# def transcribe_garhwali_audio(path: str) -> str:
#     segments, info = whisper_model.transcribe(
#         path,
#         language="hi",
#         task="transcribe",
#         vad_filter=True,
#     )
#     pieces = [seg.text.strip() for seg in segments if seg.text.strip()]
#     return " ".join(pieces).strip()


# def tts_garhwali(text: str) -> str:
#     safe_text = text.strip()
#     if len(safe_text) > 1500:
#         safe_text = safe_text[:1500]

#     filename = f"garhwali_{uuid.uuid4().hex}.mp3"
#     out_path = TTS_OUTPUT_DIR / filename

#     # अभी Garhwali भी Hindi TTS से ही बोलेगा (hi-IN voice)
#     tts = gTTS(text=safe_text, lang="hi")
#     tts.save(str(out_path))
#     return filename

# # ================== DOCS RAG PIPELINE ==================


# def build_docs_system_prompt() -> str:
#     return (
#         "आप 'Panchayat Sahayika' हैं, उत्तराखंड की ग्राम पंचायतों के लिए सहायक।\n"
#         "यूज़र कभी-कभी गढ़वाली या हिंग्लिश में भी सवाल पूछ सकते हैं; "
#         "आप अर्थ समझकर पहले सरल हिन्दी में जवाब तैयार करें (बाद में ज़रूरत हो तो दूसरी भाषा में अनुवाद होगा)।\n"
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
# - Whenever you write the name of any scheme / yojana, always wrap it like this: `**PM Awas Yojana**`.

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
# Give one short English summary sentence (not detailed).

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

# # ================== ASK MODELS ==================


# class AskRequest(BaseModel):
#     question: str
#     ui_lang: str = "hi"
#     mode: str = "auto"         # "auto" | "docs" | "schemes"
#     history: List[Dict[str, str]] = []
#     user_meta: Dict[str, Any] | None = None


# class AskResponse(BaseModel):
#     response: str
#     sources: List[Dict[str, Any]] = []
#     audio_url: Optional[str] = None


# class SchemeCard(SQLModel):
#     title: str
#     subtitle: Optional[str] = None
#     verified: bool = True
#     badges: List[str] = []
#     apply_url: Optional[str] = None
#     read_more_url: Optional[str] = None

# # ================== RECOMMENDATIONS ==================


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

# # ================== HTML DEMO ROUTES ==================


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
#         schemes, _ = search_schemes(
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

# # ================== CORE ASK LOGIC ==================


# def process_ask_request(req: AskRequest) -> AskResponse:
#     # UI language se target lang decide
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

#     # ---------- routing: schemes vs docs ----------
#     if req.mode in ("schemes", "auto"):
#         schemes, _ = search_schemes(
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

#     # ---------- translate to requested UI language ----------
#     final_text = translate_answer(base_answer, target_lang)
#     final_html = _convert_markdown_bold_to_html(final_text)

#     # ---------- TTS for Garhwali (audio_url) ----------
    
#     audio_url: Optional[str] = None
#     if req.ui_lang in ["garhwali", "hi", "hinglish"]:
#      plain = re.sub("<[^<]+?>", "", final_html)
#     if plain.strip():
#         filename = tts_garhwali(plain)
#         audio_url = f"/tts/{filename}"


#     return AskResponse(response=final_html, sources=sources, audio_url=audio_url)

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
#         "garhwali_examples_count": len(GARHWALI_EXAMPLES),
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
from difflib import SequenceMatcher

import torch
from transformers import MT5ForConditionalGeneration, MT5Tokenizer
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

# ---- Hindi -> Garhwali custom dataset ----
# Expected file: list of objects like
# [
#   {"input": "आवेदक के पास बैंक खाता होना आवश्यक है।",
#    "output": "आवेदक कु पास बैंकु खाता होणो जरूरी छ।"},
#   ...
# ]
GARHWALI_DATA_PATH = BASE_DIR / "dataset_final.json"

# ---- Hindi -> Garhwali rule-based replacements ----

GARHWALI_RULES = [
    # 1. negatives + modals
    (r"नहीं होना चाहिए", "नीं होयु चयेने"),
    (r"नहीं होना चाहिए।", "नीं होयु चयेने।"),

    # 2. ke liye -> khatar
    (r"के लिए", "खातर"),
    (r"के लिये", "खातर"),

    # 3. ke tahat -> ku tahat
    (r"के तहत", "कु तहत"),

    # 4. genitive ka/ke/ki -> ku
    (r"([^\s]+) का ", r"\1 कु "),
    (r"([^\s]+) के ", r"\1 कु "),
    (r"([^\s]+) की ", r"\1 कु "),

    # 5. में -> म
    (r" में ", " म "),

    # 6. hona chahiye
    (r"होना चाहिए।", "होयु चयेने।"),
    (r"होना चाहिए", "होयु चयेने"),
    (r"होनी चाहिए।", "होई चयेने।"),
    (r"होनी चाहिए", "होई चयेने"),

    # 7. se kam honi chahiye
    (r"से कम होनी चाहिए", "से कम होई चयेने"),

    # 8. hai -> ch
    (r" है।", " छ।"),
    (r" है?", " छ?"),
    (r" है ", " छ "),

    # 9. upalabdh / aavashyak / anivarya / aarakshit
    (r"उपलब्ध छ है", "उपलब्ध छ"),  # safety
    (r"उपलब्ध है", "उपलब्ध छ"),
    (r"आरक्षित है", "आरक्षित छ"),
    (r"अनिवार्य है", "अनिवार्य छ"),
    (r"जरूरी है", "जरूरी छ"),
    (r"आवश्यक है", "आवश्यक छ"),

    # 10. dia jayega / di jayegi
    (r"दिया जाएगा।", "दिउँ जालु।"),
    (r"दिया जाएगा", "दिउँ जालु"),
    (r"दी जाएगी।", "दिज़ली जाली।"),
    (r"दी जाएगी", "दिज़ली जाली"),

    (r"प्रदान की जाएगी", "प्रदान कु जाएगी"),
    (r"प्रदान की जाती है", "प्रदान कु जाती छ"),

    # 11. jama / bharna
    (r"जमा करनी होगी", "जमा करनु होलु"),
    (r"जमा करना होगा", "जमा करनु होलु"),
    (r"भरना होगा", "भरनु होलु"),
    (r"भरने के बाद", "भरने कु बाद"),

    # 12. le sakte hain
    (r"ले सकते हैं।", "ले सकद्या छौं।"),
    (r"ले सकते हैं", "ले सकद्या छौं"),
]


def apply_garhwali_rules(text: str) -> str:
    """
    Hindi → Garhwali output par rule-based post-processing.
    LLM/MT5 se aane wale sentences ko thoda aur natural Garhwali banata hai.
    """
    if not text:
        return text

    out = text
    for pattern, repl in GARHWALI_RULES:
        out = re.sub(pattern, repl, out)
    return out.strip()


def _load_garhwali_examples() -> List[Tuple[str, str]]:
    """
    Load parallel Hindi->Garhwali examples from JSON or JSONL.
    Tries multiple common key names so that your existing 60-line
    file will work even if keys are slightly different.
    """
    if not GARHWALI_DATA_PATH.exists():
        return []

    pairs: List[Tuple[str, str]] = []
    try:
        # Try normal JSON first
        with open(GARHWALI_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = data.get("data") or data.get("examples") or []
    except Exception:
        # Fallback: maybe JSONL
        data = []
        with open(GARHWALI_DATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data.append(json.loads(line))
                except Exception:
                    continue

    for row in data:
        if not isinstance(row, dict):
            continue
        hi = (
            row.get("input")
            or row.get("hindi")
            or row.get("source")
            or row.get("text_hi")
            or row.get("text")
        )
        gw = (
            row.get("output")
            or row.get("garhwali")
            or row.get("target")
            or row.get("text_gw")
        )
        if hi and gw:
            hi = hi.strip()
            gw = gw.strip()
            if hi and gw:
                pairs.append((hi, gw))

    return pairs


GARHWALI_EXAMPLES: List[Tuple[str, str]] = _load_garhwali_examples()

load_dotenv()

# ---- Garhwali MT5 fine-tuned model ----
GARHWALI_MODEL_PATH = os.getenv(
    "GARHWALI_MODEL_PATH",
    str(BASE_DIR / "garhwali_mt5_finetuned"),  # put your folder here
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

try:
    gw_tokenizer = MT5Tokenizer.from_pretrained(GARHWALI_MODEL_PATH)
    gw_model = MT5ForConditionalGeneration.from_pretrained(
        GARHWALI_MODEL_PATH
    ).to(DEVICE)
    print(f"✅ Loaded Garhwali MT5 model from: {GARHWALI_MODEL_PATH}")
except Exception as e:
    print("⚠️ Could not load Garhwali MT5 model, will use Groq fallback:", e)
    gw_tokenizer = None
    gw_model = None

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


def _llm_translate(text: str | None, instruction: str) -> str:
    """
    Generic helper: use Groq LLM to rewrite `text` according to `instruction`.
    Always returns a string (never None).
    """
    if text is None:
        text = ""

    prompt = f"""
Instruction:
{instruction}

Input text:
{text}

Now rewrite the text according to the instruction.
"""

    try:
        completion = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You rewrite text as requested."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=800,
        )
        out = completion.choices[0].message.content
        if not out:
            return text
        return out.strip()
    except Exception as e:
        print("⚠️ _llm_translate error:", e)
        return text


def _most_similar_garhwali_example(
    text: str, threshold: float = 0.92
) -> Optional[str]:
    """
    For short Hindi lines (like eligibility bullets), see if we have
    almost-exact match in the dataset. If yes, directly return
    the Garhwali from dataset (no LLM needed).
    """
    if not GARHWALI_EXAMPLES:
        return None

    best_score = 0.0
    best_out: Optional[str] = None
    for hi, gw in GARHWALI_EXAMPLES:
        score = SequenceMatcher(None, text, hi).ratio()
        if score > best_score:
            best_score = score
            best_out = gw

    if best_score >= threshold:
        return best_out
    return None


# --- Small helpers for Garhwali translation ---

SENTENCE_SPLIT_RE = re.compile(r"(?<=[।!?])\s+|\n+")


def _split_hindi_sentences(text: str) -> List[str]:
    """
    Split long Hindi paragraph into smaller sentence-like chunks,
    so that MT5 + rules can translate line-by-line.
    """
    if not text:
        return []
    parts = [p.strip() for p in SENTENCE_SPLIT_RE.split(text) if p.strip()]
    return parts


ENGLISH_LINE_RE = re.compile(r"^\s*(\*\*English\*\*|English:)", re.IGNORECASE)


def _strip_english_for_garhwali(text: str) -> str:
    """
    remove the final English summary etc. before sending to Garhwali model,
    because MT5 was trained only on Hindi → Garhwali.
    """
    lines = text.splitlines()
    kept: List[str] = []
    for ln in lines:
        if ENGLISH_LINE_RE.match(ln):
            # skip English summary lines
            continue
        kept.append(ln)
    return "\n".join(kept).strip()


def _llm_translate_garhwali_with_examples(text: str) -> str:
    """
    Main Hindi -> Garhwali translator:

    0) For long paragraphs, first split into Hindi sentences and translate
       each sentence separately, then join back.
    1) If a short line is very similar to a known dataset line, use dataset output (+ rules).
    2) Otherwise, if fine-tuned MT5 model is available, use that (+ rules).
    3) If model is not available, fallback to Groq LLM few-shot prompt (+ rules).
    """
    clean = text.strip()
    if not clean:
        return clean

    # 0) If text is long or multi-line, do sentence-wise translation
    if len(clean) > 220 or "\n" in clean:
        sentences = _split_hindi_sentences(clean)
        out_sentences: List[str] = []
        for s in sentences:
            gw = _llm_translate_garhwali_with_examples(s)
            if gw:
                out_sentences.append(gw)
        # join with space – sentences already include their own "।" / "?" etc.
        return " ".join(out_sentences).strip()

    # 1) Direct lookup for short, formulaic lines (eligibility, bullets, etc.)
    if len(clean) <= 140:
        direct = _most_similar_garhwali_example(clean)
        if direct:
            return apply_garhwali_rules(direct)

    # 2) Use fine-tuned MT5 model if available
    if gw_model is not None and gw_tokenizer is not None:
        try:
            input_text = f"translate Hindi to Garhwali: {clean}"

            inputs = gw_tokenizer(
                input_text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=256,
            ).to(DEVICE)

            outputs = gw_model.generate(
                **inputs,
                max_length=256,
                num_beams=4,
            )

            decoded = gw_tokenizer.decode(outputs[0], skip_special_tokens=True)
            decoded = decoded.strip()
            # Post-process with handcrafted rules
            return apply_garhwali_rules(decoded)
        except Exception as e:
            print("⚠️ Error in Garhwali MT5 translation, falling back to Groq:", e)

    # 3) Fallback: Groq LLM with few-shot examples (old behaviour)
    examples = GARHWALI_EXAMPLES[:10]
    ex_lines = []
    for hi, gw in examples:
        ex_lines.append(f"Hindi: {hi}\nGarhwali: {gw}")
    examples_block = "\n\n".join(ex_lines)

    system_msg = (
        "You are a native Garhwali speaker from rural Uttarakhand. "
        "Your job is to rewrite Hindi text into pure, natural village-style Garhwali "
        "in Devanagari script only. Do NOT explain, only translate / rewrite.\n"
    )

    user_msg = f"""
नीचे कुछ उदाहरण दिए गए हैं कि हमें Hindi से Garhwali में कैसे भाषा बदलनी है:

{examples_block}

अब नीचे दिए गए पूरे टेक्स्ट को उसी स्टाइल में Garhwali में बदलो:

Hindi text:
{clean}

सिर्फ final Garhwali version दो, बिना किसी extra explanation के.
ध्यान रहे:
- 'है, हैं, था, थे, होगा' जैसे शब्दों को Garhwali रूपों से बदलना है (जैसे 'छ, छन, ह्वे, पडुल' आदि).
- Tone हमेशा गाँव की normal बोली जैसा हो, ज़्यादा legal / किताब वाली Hindi मत रखो.
- Scheme / department के नाम (जैसे 'प्रधानमंत्री आवास योजना', 'Uttarakhand Jal Sansthan') Hindi में जैसे हैं वैसे ही रहने दो.
"""

    try:
        completion = groq_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.25,
            max_tokens=1200,
        )
        raw_out = completion.choices[0].message.content or clean
        raw_out = raw_out.strip()
        final_out = apply_garhwali_rules(raw_out)
        return final_out
    except Exception:
        # last-resort: return original Hindi (better than wrong Garhwali)
        return clean


def translate_answer(text: str | None, target_lang: str) -> str:
    """
    target_lang:
      - 'en'        -> English
      - 'hi'        -> simple Hindi
      - 'garhwali'  -> Garhwali (Devnagari, village style)
      - 'hinglish'  -> Roman Hindi
    """
    if text is None:
        text = ""

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
    if target_lang == "garhwali":
        # Flow:
        # 1) Ensure text is simple Hindi
        # 2) Then translate Hindi paragraph line-by-line to Garhwali
        if not contains_devanagari(text):
            text_hi = _llm_translate(
                text,
                "very simple Hindi in Devanagari script, using everyday words "
                "that village-level users understand.",
            )
        else:
            text_hi = text
        hindi_only = _strip_english_for_garhwali(text_hi)
        return _llm_translate_garhwali_with_examples(hindi_only)

    # ---------- Hinglish ----------
    return _llm_translate(
        text,
        "very simple Hinglish (Roman Hindi using English letters). "
        "Do NOT use Devanagari characters.",
    )


def _convert_markdown_bold_to_html(text: str | None) -> str:
    """
    Convert **bold** markdown to <strong>bold</strong>.
    If text is None, return empty string to avoid TypeError.
    """
    if not isinstance(text, str):
        return ""
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
            "రाशि",
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

    # UI language -> target language (no auto-detect here)
    if ui_lang == "en":
        target_lang = "en"
    elif ui_lang == "hi":
        target_lang = "hi"
    elif ui_lang == "garhwali":
        target_lang = "garhwali"
    elif ui_lang == "hinglish":
        target_lang = "hinglish"
    else:
        # fallback: auto
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
    # UI language se target lang direct decide karo
    if req.ui_lang == "en":
        target_lang = "en"
    elif req.ui_lang == "hi":
        target_lang = "hi"
    elif req.ui_lang == "garhwali":
        target_lang = "garhwali"
    elif req.ui_lang == "hinglish":
        target_lang = "hinglish"
    else:
        # fallback auto
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

    # ---------- TTS for Garhwali / Hindi / Hinglish ----------
    audio_url: Optional[str] = None
    if req.ui_lang in ["garhwali", "hi", "hinglish"]:
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
        "garhwali_examples_count": len(GARHWALI_EXAMPLES),
    }

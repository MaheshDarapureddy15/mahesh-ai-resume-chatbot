"""
Mahesh AI Resume Assistant
==========================
A modern, text-based interactive AI chatbot built with Streamlit and Google Gemini API
(Google GenAI Python SDK). Grounded strictly on Mahesh Darapureddy's verified resume.

Author: Mahesh Darapureddy
Portfolio: https://maheshdarapureddy.in
"""

import os
import sys
from typing import Generator
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Attempt to import Google GenAI SDK
try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    APIError = Exception


# ==============================================================================
# STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Mahesh AI Resume Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==============================================================================
# CUSTOM CSS STYLING (MODERN, RESPONSIVE & PROFESSIONAL)
# ==============================================================================
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Modern Chat Banner Header */
    .hero-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        color: #ffffff;
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #ffffff 0%, #c7d2fe 50%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-top: 6px;
        margin-bottom: 12px;
        font-weight: 400;
    }
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.18);
        border: 1px solid rgba(129, 140, 248, 0.35);
        color: #c7d2fe;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        backdrop-filter: blur(8px);
    }
    .hero-badge-csa {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(52, 211, 153, 0.4);
        color: #6ee7b7;
    }
    .hero-badge-cad {
        background: rgba(245, 158, 11, 0.15);
        border-color: rgba(251, 191, 36, 0.4);
        color: #fde68a;
    }

    /* Sidebar Profile Card */
    .profile-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .profile-name {
        font-size: 18px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 2px;
    }
    .profile-role {
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 12px;
    }
    .profile-links a {
        display: block;
        padding: 6px 10px;
        margin: 4px 0;
        background: rgba(255, 255, 255, 0.04);
        border-radius: 8px;
        color: #38bdf8 !important;
        text-decoration: none;
        font-size: 12.5px;
        font-weight: 500;
        border: 1px solid rgba(56, 189, 248, 0.15);
        transition: all 0.2s ease;
    }
    .profile-links a:hover {
        background: rgba(56, 189, 248, 0.12);
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateX(2px);
    }

    /* Section Headers in Sidebar */
    .sidebar-section-title {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94a3b8;
        margin-top: 18px;
        margin-bottom: 10px;
    }

    /* Suggested Questions Section */
    .suggested-title {
        font-size: 13px;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Chat bubble enhancements */
    .stChatMessage {
        border-radius: 14px;
        margin-bottom: 12px;
        animation: fadeIn 0.3s ease;
    }

    /* Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    .status-online {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .status-offline {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Clean Streamlit button styling */
    .stButton>button {
        border-radius: 10px;
        font-weight: 500;
        font-size: 13px;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# RESUME KNOWLEDGE BASE LOADER
# ==============================================================================
@st.cache_data
def load_resume() -> str:
    """Load the candidate resume text from resume.txt."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resume_path = os.path.join(base_dir, "resume.txt")
    if not os.path.exists(resume_path):
        return ""
    try:
        with open(resume_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as exc:
        return f"Error reading resume file: {exc}"


# ==============================================================================
# SYSTEM INSTRUCTION BUILDER
# ==============================================================================
def build_system_instruction(resume_text: str) -> str:
    """Construct a rigorous system instruction grounding the model in the resume."""
    return f"""You are "Mahesh AI Resume Assistant", a dedicated, professional, highly articulate, and courteous AI assistant representing Mahesh Darapureddy.

Your primary purpose is to help recruiters, hiring managers, engineers, and visitors learn about Mahesh's education, skills, projects, internships, certifications, and portfolio.

CRITICAL INSTRUCTIONS & STRICT ACCURACY RULES:
1. STRICT KNOWLEDGE BASE GROUNDING:
   - Your sole source of truth is the verified resume information provided below.
   - NEVER invent, extrapolate, or hallucinate facts, work experience, previous employers, contact details, grades, or personal details that are not in the resume.
2. HANDLING UNAVAILABLE INFORMATION:
   - If a user asks a question about something NOT present in the resume (e.g. personal phone number, home address, unrelated companies, hobbies, or tools not listed), respond politely and honestly:
     "I do not have that specific information in Mahesh's official resume. You can connect with Mahesh directly via his portfolio website at https://maheshdarapureddy.in for more details."
3. INTERVIEW-STYLE QUESTIONS:
   - When asked interview questions like "Tell me about yourself", "What are your greatest strengths?", "Why should we hire you?", or "Walk me through your multi-modal project", answer with confidence, professionalism, and structured clarity (e.g. using bullet points or STAR method where appropriate).
   - Emphasize his dual ServiceNow certifications (CSA & CAD), his full-stack AI/ML projects with live deployed links, his B.Tech in ECE from BVCITS, and his internships with AICTE and Eduskills.
4. TONE & FORMAT:
   - Maintain a friendly, polished, professional, and respectful tone.
   - Use Markdown formatting: bullet points, bold key terms, and hyperlinks for websites/projects.
   - Text chat only. No voice or audio references.

================================================================================
OFFICIAL RESUME KNOWLEDGE BASE:
================================================================================
{resume_text}
================================================================================
"""


# ==============================================================================
# GEMINI CLIENT & GENERATION HANDLER
# ==============================================================================
def is_placeholder_key(key: str) -> bool:
    """Check if an API key string is empty or an obvious placeholder."""
    if not key:
        return True
    cleaned = key.strip().strip("\"'").strip()
    lower = cleaned.lower()
    known_placeholders = {
        "your_api_key",
        "your_new_api_key",
        "your_gemini_api_key_here",
        "enter_your_api_key_here",
        "your-api-key",
        "my_api_key",
        "placeholder",
        "aizasy...",
        "xxx",
        "none",
    }
    if lower in known_placeholders or "your_" in lower or "placeholder" in lower:
        return True
    # Real Google Gemini API keys are typically ~39 characters starting with 'AIzaSy'
    if len(cleaned) < 15:
        return True
    return False


def mask_api_key(key: str) -> str:
    """Safely mask API key for UI display (e.g. AIzaSy...9aBc) without exposing secrets."""
    if not key or is_placeholder_key(key):
        return "None"
    cleaned = key.strip().strip("\"'").strip()
    if len(cleaned) <= 8:
        return "••••••••"
    return f"{cleaned[:6]}...{cleaned[-4:]}"


def get_resolved_api_key() -> tuple[str, str, str]:
    """
    Retrieve and validate the Gemini API key in priority order:
    1. User sidebar input (session state)
    2. .env file (reloaded on every run with override=True)
    3. Streamlit secrets

    Returns:
        tuple[clean_key, source_name, status]
        status is one of: 'valid', 'placeholder', 'missing'
    """
    # 1. User entered via sidebar
    sidebar_raw = st.session_state.get("user_gemini_api_key", "")
    if sidebar_raw:
        cleaned_sidebar = sidebar_raw.strip().strip("\"'").strip()
        if cleaned_sidebar:
            if is_placeholder_key(cleaned_sidebar):
                return "", "sidebar", "placeholder"
            return cleaned_sidebar, "sidebar", "valid"

    # 2. Dynamically reload .env so edits take effect immediately
    try:
        load_dotenv(override=True)
    except Exception:
        pass
    env_raw = os.getenv("GEMINI_API_KEY", "")
    if env_raw:
        cleaned_env = env_raw.strip().strip("\"'").strip()
        if cleaned_env:
            if is_placeholder_key(cleaned_env):
                return "", ".env", "placeholder"
            return cleaned_env, ".env", "valid"

    # 3. Streamlit secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            sec_raw = str(st.secrets["GEMINI_API_KEY"])
            cleaned_sec = sec_raw.strip().strip("\"'").strip()
            if cleaned_sec:
                if is_placeholder_key(cleaned_sec):
                    return "", "secrets", "placeholder"
                return cleaned_sec, "secrets", "valid"
    except Exception:
        pass

    return "", "none", "missing"


def get_api_key() -> str:
    """Convenience helper returning the resolved key string (or empty if missing/placeholder)."""
    key, _, _ = get_resolved_api_key()
    return key


def test_gemini_connection(api_key: str, model_name: str) -> tuple[bool, str]:
    """
    Test Gemini API connectivity without logging or exposing the key.
    Returns:
        (success_bool, message_string)
    """
    if not GENAI_AVAILABLE:
        return False, "The `google-genai` SDK is not installed. Please run `pip install google-genai`."

    if not api_key or is_placeholder_key(api_key):
        return False, "No valid API key provided. Please configure a valid key from Google AI Studio."

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents="Respond with the single word: OK",
            config=types.GenerateContentConfig(
                max_output_tokens=5,
                temperature=0.0
            )
        )
        if response and response.text:
            return True, f"Connection successful! Model '{model_name}' responded."
        return True, f"Connected to Google Gemini ({model_name})."
    except APIError as api_err:
        code = getattr(api_err, "code", 0)
        msg = getattr(api_err, "message", str(api_err))
        if code == 400 or "API_KEY_INVALID" in str(msg) or "API key not valid" in str(msg):
            return False, (
                "400 API_KEY_INVALID: Google rejected this API key. "
                "Please verify you copied the full key from https://aistudio.google.com/app/apikey."
            )
        elif code == 429 or "RESOURCE_EXHAUSTED" in str(msg):
            return False, "429 RESOURCE_EXHAUSTED: Rate limit or quota exceeded for this API key."
        elif code == 404 or "NOT_FOUND" in str(msg):
            return False, f"404 NOT_FOUND: Model '{model_name}' is not accessible. Try 'gemini-3.1-flash-lite' or 'gemini-3.5-flash-lite'."
        return False, f"Gemini API Error (HTTP {code}): {msg}"
    except Exception as exc:
        exc_str = str(exc)
        if "getaddrinfo failed" in exc_str or "ConnectError" in exc_str:
            return False, "Network Connection Failed: Unable to reach Google servers. Check your internet connection."
        return False, f"Connection test failed: {exc_str}"


def stream_gemini_response(
    messages: list[dict],
    system_instruction: str,
    api_key: str,
    selected_model: str
) -> Generator[str, None, None]:
    """Stream response from Gemini using Google GenAI SDK with graceful fallbacks."""
    if not GENAI_AVAILABLE:
        yield "❌ **Error**: The `google-genai` SDK is not installed. Please run `pip install google-genai`."
        return

    active_key, key_source, key_status = get_resolved_api_key()

    if key_status == "placeholder":
        yield (
            "⚠️ **Placeholder API Key Detected**\n\n"
            f"Your `{key_source}` configuration currently contains a placeholder value (e.g. `YOUR_NEW_API_KEY`).\n\n"
            "**How to fix:**\n"
            "1. Obtain your free Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey).\n"
            "2. Paste it in the sidebar under **Gemini API Configuration**, or edit `.env`:\n"
            "   ```env\n"
            "   GEMINI_API_KEY=AIzaSyYourActualKeyHere\n"
            "   ```\n"
            "3. The chatbot will connect immediately!"
        )
        return

    if not active_key or key_status == "missing":
        yield (
            "⚠️ **Gemini API Key Required**\n\n"
            "Please provide a Google Gemini API Key to enable chat responses.\n\n"
            "- Add `GEMINI_API_KEY=AIzaSy...` in your `.env` file, OR\n"
            "- Enter your key in the sidebar under **Gemini API Configuration**.\n\n"
            "You can get a free Gemini API key at: [Google AI Studio](https://aistudio.google.com/app/apikey)"
        )
        return

    # List of models to try (selected first, then standard modern fallbacks)
    models_to_try = [selected_model]
    for fallback in [
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.8-flash",
        "gemini-2.5-flash"
    ]:
        if fallback not in models_to_try:
            models_to_try.append(fallback)

    last_error = None
    client = None

    try:
        client = genai.Client(api_key=active_key)
    except Exception as exc:
        yield f"❌ **Initialization Error**: Failed to initialize Gemini client: {exc}"
        return

    # Format conversation history for GenAI SDK
    # Gemini requires multi-turn chat to begin with a user turn
    formatted_contents = []
    for msg in messages:
        # Skip initial assistant greeting if no user query has occurred yet
        if not formatted_contents and msg["role"] != "user":
            continue
        role = "user" if msg["role"] == "user" else "model"
        formatted_contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )

    # Attempt generation with fallback model support
    for model_name in models_to_try:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                max_output_tokens=2048,
            )

            response_stream = client.models.generate_content_stream(
                model=model_name,
                contents=formatted_contents,
                config=config,
            )

            streamed_any = False
            for chunk in response_stream:
                if chunk.text:
                    streamed_any = True
                    yield chunk.text

            if streamed_any:
                return

        except APIError as api_err:
            last_error = str(api_err)
            continue
        except Exception as exc:
            last_error = str(exc)
            continue

    # If all models failed, provide helpful diagnosis
    error_detail = str(last_error)
    if "API_KEY_INVALID" in error_detail or "API key not valid" in error_detail:
        yield (
            "❌ **API Key Error (400 API_KEY_INVALID)**: Google Gemini rejected this API key.\n\n"
            "**Troubleshooting steps:**\n"
            "1. Verify that you copied the complete key from [Google AI Studio](https://aistudio.google.com/app/apikey).\n"
            "2. Make sure there are no missing or extra characters.\n"
            "3. Paste the key directly into the sidebar **API Key** field and click **🧪 Test API Connection**."
        )
    else:
        yield (
            f"❌ **API Error**: Unable to complete response from Gemini.\n\n"
            f"**Details**: `{error_detail}`\n\n"
            f"Please verify your Gemini API key, check your rate limits, or try another model in the sidebar."
        )


# ==============================================================================
# INITIALIZE SESSION STATE
# ==============================================================================
INITIAL_WELCOME = (
    "Hello and welcome! 👋 I am the **Mahesh AI Resume Assistant**, an intelligent chatbot "
    "trained on the verified background and portfolio of **Mahesh Darapureddy**.\n\n"
    "Feel free to ask me anything about Mahesh's:\n"
    "- 🎓 **Education** (B.Tech in ECE, Intermediate, SSC)\n"
    "- 🛠️ **Technical Skills** (Python, Java, SQL, ServiceNow ITSM, Next.js, ML)\n"
    "- 🚀 **Live Projects** (Multi-Modal AI Chatbot, AI Analyzer, Diabetes Predictor, Kidney Stone Detection)\n"
    "- 📜 **Certifications** (ServiceNow CSA & CAD)\n"
    "- 💼 **Internships** (AICTE, Eduskills)\n"
    "- 🎤 **Interview Inquiries** (\"Why should we hire Mahesh?\", \"Tell me about yourself\")\n\n"
    "How can I assist you today?"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": INITIAL_WELCOME}
    ]

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ==============================================================================
# SIDEBAR SETUP (PROFILE, PROJECTS, CONFIGURATION)
# ==============================================================================
with st.sidebar:
    # Candidate Profile Header Card
    st.markdown("""
    <div class="profile-card">
        <div style="font-size: 32px; margin-bottom: 6px;">👨‍💻</div>
        <div class="profile-name">Mahesh Darapureddy</div>
        <div class="profile-role">AI Developer | Full-Stack Engineer<br>ServiceNow CSA & CAD Certified</div>
        <div class="profile-links">
            <a href="https://maheshdarapureddy.in" target="_blank">🌐 Official Portfolio Website ↗</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Live Projects Section
    st.markdown('<div class="sidebar-section-title">🚀 Featured Projects</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="profile-links" style="margin-bottom: 16px;">
        <a href="https://chat.maheshdarapureddy.in" target="_blank">🤖 Multi-Modal AI Chatbot ↗</a>
        <a href="https://chatai.maheshdarapureddy.in" target="_blank">📄 AI Analyzer (RAG) ↗</a>
        <a href="https://diabetes.maheshdarapureddy.in" target="_blank">🩺 Diabetes Predictor ↗</a>
        <a href="https://detect.maheshdarapureddy.in" target="_blank">🩻 Kidney Stone Detection ↗</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # API Configuration
    st.markdown('<div class="sidebar-section-title">⚙️ Gemini API Configuration</div>', unsafe_allow_html=True)

    # Check key status using robust resolver
    active_key, key_source, key_status = get_resolved_api_key()

    if key_status == "valid":
        masked_preview = mask_api_key(active_key)
        st.markdown(
            f'<div class="status-pill status-online">● Key Active ({key_source}: {masked_preview})</div>',
            unsafe_allow_html=True
        )
    elif key_status == "placeholder":
        st.markdown(
            f'<div class="status-pill status-offline">⚠️ Placeholder in {key_source}</div>',
            unsafe_allow_html=True
        )
        st.caption(f"⚠️ Placeholder key detected in `{key_source}`. Please replace with your actual key.")
    else:
        st.markdown(
            '<div class="status-pill status-offline">● API Key Missing</div>',
            unsafe_allow_html=True
        )

    # Password input bound to Streamlit session state
    st.text_input(
        "API Key (or configure .env)",
        type="password",
        key="user_gemini_api_key",
        placeholder="AIzaSy... paste Gemini key here",
        help="Get your free API key from https://aistudio.google.com/app/apikey"
    )

    # Model Selection
    model_choice = st.selectbox(
        "Gemini Model",
        options=[
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.8-flash"
        ],
        index=0,
        help="Select the Gemini model variant. gemini-3.1-flash-lite is ultra-fast, modern, and reliable."
    )

    # Test API Connection Button
    if st.button("🧪 Test API Connection", use_container_width=True):
        if key_status == "missing":
            st.warning("⚠️ No API key provided. Please enter your key above or update `.env`.")
        elif key_status == "placeholder":
            st.error(f"❌ Placeholder key detected in `{key_source}`. Please enter your real key from Google AI Studio.")
        else:
            with st.spinner("Testing connection to Google Gemini..."):
                is_ok, msg = test_gemini_connection(active_key, model_choice)
                if is_ok:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")

    st.markdown("---")

    # Clear Chat Button
    st.markdown('<div class="sidebar-section-title">🗑️ Chat Controls</div>', unsafe_allow_html=True)
    if st.button("Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = [
            {"role": "assistant", "content": INITIAL_WELCOME}
        ]
        st.session_state.pending_prompt = None
        st.rerun()

    # Footer note
    st.markdown("""
    <div style="font-size: 11px; color: #64748b; margin-top: 24px; text-align: center;">
        Mahesh AI Resume Assistant v1.0<br>
        Built with Streamlit & Google GenAI SDK
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# MAIN PAGE HEADER
# ==============================================================================
st.markdown("""
<div class="hero-header">
    <div class="hero-title">Mahesh AI Resume Assistant</div>
    <div class="hero-subtitle">
        Interactive conversational agent grounded on Mahesh Darapureddy's verified resume and portfolio.
    </div>
    <div class="badge-container">
        <span class="hero-badge">🎓 B.Tech ECE (BVCITS '26)</span>
        <span class="hero-badge hero-badge-csa">🏆 ServiceNow CSA</span>
        <span class="hero-badge hero-badge-cad">🏆 ServiceNow CAD</span>
        <span class="hero-badge">⚡ Next.js & FastAPI</span>
        <span class="hero-badge">🧠 Generative AI & RAG</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# SUGGESTED QUESTIONS (CLICK TO ASK)
# ==============================================================================
st.markdown('<div class="suggested-title">💡 Suggested Questions (Click any topic below to ask):</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💼 Tell me about Mahesh", use_container_width=True):
        st.session_state.pending_prompt = "Tell me about Mahesh Darapureddy, his background, and what he specializes in."
        st.rerun()
    if st.button("🛠️ Technical Skills Overview", use_container_width=True):
        st.session_state.pending_prompt = "What are Mahesh's core technical skills in programming, AI/ML, and ServiceNow?"
        st.rerun()

with col2:
    if st.button("🚀 Projects & Live Links", use_container_width=True):
        st.session_state.pending_prompt = "Describe the projects Mahesh has built, their tech stacks, and their live website links."
        st.rerun()
    if st.button("📜 ServiceNow Certifications", use_container_width=True):
        st.session_state.pending_prompt = "What ServiceNow certifications and ITSM experience does Mahesh have?"
        st.rerun()

with col3:
    if st.button("🎯 Why Should We Hire Mahesh?", use_container_width=True):
        st.session_state.pending_prompt = "Why should our company hire Mahesh? Give an interview-style answer."
        st.rerun()
    if st.button("🎓 Education & Internships", use_container_width=True):
        st.session_state.pending_prompt = "What is Mahesh's educational background, grades, and internship experience?"
        st.rerun()

st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# RENDER CHAT HISTORY
# ==============================================================================
for msg in st.session_state.messages:
    avatar = "💼" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# ==============================================================================
# PROCESS CHAT INPUT & GENERATE RESPONSE
# ==============================================================================
# Determine if there is input from chat_input or a clicked suggestion button
chat_input_val = st.chat_input("Ask any question about Mahesh's experience, skills, projects, or certifications...")

active_prompt = None
if chat_input_val:
    active_prompt = chat_input_val.strip()
elif st.session_state.pending_prompt:
    active_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if active_prompt:
    # 1. Append user message to history
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(active_prompt)

    # 2. Load resume context and system instruction
    resume_content = load_resume()
    if not resume_content:
        st.error("⚠️ Warning: `resume.txt` could not be found or loaded. Responses will lack grounding.")
    system_inst = build_system_instruction(resume_content)

    # 3. Stream assistant response
    with st.chat_message("assistant", avatar="💼"):
        api_key_to_use = get_api_key()
        response_generator = stream_gemini_response(
            messages=st.session_state.messages,
            system_instruction=system_inst,
            api_key=api_key_to_use,
            selected_model=model_choice
        )
        full_response = st.write_stream(response_generator)

    # 4. Save assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

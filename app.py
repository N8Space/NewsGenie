import streamlit as st
import os
from dotenv import load_dotenv

# Try loading from .env
load_dotenv()

from newsgenie.workflow import get_app

# Page configuration
st.set_page_config(
    page_title="NewsGenie - AI News & Deep Search",
    page_icon="assets/genie_logo.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom sleek modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Background and containers */
    .stApp {
        background: radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 85% 90%, rgba(139, 92, 246, 0.06) 0%, transparent 40%),
                    #0A0E1A;
        color: #F1F5F9;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0A0E1A;
    }
    ::-webkit-scrollbar-thumb {
        background: #2D3748;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #4A5568;
    }

    /* Hero Banner Header */
    .hero-container {
        padding: 1.75rem 2rem;
        background: linear-gradient(135deg, rgba(26, 35, 60, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        margin-bottom: 1.75rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #6366F1, #A855F7, #EC4899, #06B6D4);
    }

    .hero-title {
        font-size: 2.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 20%, #A5B4FC 60%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 1rem;
        margin-top: 0.4rem;
        margin-bottom: 1rem;
        font-weight: 400;
    }

    /* Badges & Pills */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #CBD5E1;
        transition: all 0.2s ease;
    }

    .badge-pill:hover {
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(99, 102, 241, 0.15);
        color: #FFFFFF;
    }

    .badge-pill-status {
        background: rgba(16, 185, 129, 0.12);
        border-color: rgba(16, 185, 129, 0.3);
        color: #34D399;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }

    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #E2E8F0;
        font-weight: 700;
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .sidebar-brand-card {
        padding: 0.85rem 1rem;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.18), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.25);
        margin-bottom: 1rem;
    }

    .sidebar-status-card {
        padding: 0.85rem 1rem;
        border-radius: 12px;
        background: rgba(19, 27, 46, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 0.75rem;
    }

    .key-status-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.35rem 0.5rem;
        margin-bottom: 0.3rem;
        border-radius: 6px;
        font-size: 0.78rem;
        background: rgba(30, 41, 59, 0.6);
    }

    .key-status-dot {
        height: 8px;
        width: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    .dot-connected {
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
    }

    .dot-missing {
        background-color: #EF4444;
    }

    /* Equal Sized Uniform Buttons */
    .stButton > button, .stDownloadButton > button {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: #1E293B !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        min-height: 40px !important;
        height: 40px !important;
        max-height: 40px !important;
        padding: 0 0.4rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
        overflow: hidden !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    .stButton > button p, .stButton > button span,
    .stDownloadButton > button p, .stDownloadButton > button span {
        font-size: 0.8rem !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: #6366F1 !important;
        background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transform: translateY(-1px);
    }

    .stButton > button:active, .stDownloadButton > button:active {
        transform: translateY(0);
    }

    /* Welcome / Starter Cards */
    .starter-card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }

    .starter-card {
        padding: 1.25rem;
        border-radius: 12px;
        background: rgba(19, 27, 46, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        transition: all 0.25s ease;
    }

    .starter-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(30, 41, 59, 0.8);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    }

    .starter-card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .starter-card-desc {
        font-size: 0.8rem;
        color: #94A3B8;
        line-height: 1.4;
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 14px;
        margin-bottom: 1rem;
        padding: 1rem 1.25rem;
        border: 1px solid rgba(255, 255, 255, 0.06);
        background: rgba(19, 27, 46, 0.6);
        backdrop-filter: blur(8px);
    }

    div[data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(30, 41, 59, 0.5);
        border-left: 3px solid #6366F1;
    }

    div[data-testid="stChatMessage"]:nth-child(odd) {
        background: rgba(15, 23, 42, 0.6);
        border-left: 3px solid #06B6D4;
    }

    /* Chat Input */
    .stChatInputContainer {
        border-radius: 14px !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
    }

    .stChatInputContainer:focus-within {
        border-color: #818CF8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.25), 0 8px 24px rgba(0, 0, 0, 0.4) !important;
    }

    /* Author Footer */
    .footer-container {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #64748B;
        font-size: 0.8rem;
    }

    .footer-container a {
        color: #818CF8;
        text-decoration: none;
        font-weight: 500;
    }

    .footer-container a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- MODERN GENIE LOGO SVG -----------------
GENIE_SVG_ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="38" height="38" style="vertical-align:middle; flex-shrink:0;">
  <defs>
    <radialGradient id="hBg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1E1B4B" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.98"/>
    </radialGradient>
    <linearGradient id="hNeon" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06B6D4"/>
      <stop offset="40%" stop-color="#6366F1"/>
      <stop offset="80%" stop-color="#A855F7"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </linearGradient>
    <linearGradient id="hLamp" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#818CF8"/>
      <stop offset="50%" stop-color="#4F46E5"/>
      <stop offset="100%" stop-color="#312E81"/>
    </linearGradient>
    <filter id="hGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feComposite in="SourceGraphic" in2="b" operator="over"/>
    </filter>
  </defs>
  <circle cx="60" cy="60" r="54" fill="url(#hBg)" stroke="url(#hNeon)" stroke-width="2.5" filter="url(#hGlow)"/>
  <path d="M 60 22 C 70 20, 80 28, 76 38 C 73 47, 60 48, 66 58 C 71 66, 80 68, 70 77 C 62 83, 48 80, 52 68 C 56 57, 44 51, 46 39 C 48 27, 54 22, 60 22 Z" fill="url(#hNeon)" filter="url(#hGlow)" opacity="0.95"/>
  <circle cx="60" cy="36" r="3.5" fill="#FFFFFF"/>
  <path d="M 46 94 L 74 94 L 70 89 L 50 89 Z" fill="#312E81" stroke="#818CF8" stroke-width="1.2"/>
  <path d="M 32 75 C 32 68, 42 63, 60 63 C 78 63, 88 68, 88 75 C 88 83, 76 89, 60 89 C 44 89, 32 83, 32 75 Z" fill="url(#hLamp)" stroke="#A5B4FC" stroke-width="1.8"/>
  <path d="M 38 70 C 22 64, 18 80, 30 84 C 25 79, 28 69, 38 72 Z" fill="url(#hNeon)" stroke="#6366F1" stroke-width="0.8"/>
  <path d="M 80 72 C 92 68, 102 58, 104 50 C 101 54, 94 60, 84 64 Z" fill="url(#hNeon)" stroke="#38BDF8" stroke-width="0.8"/>
  <path d="M 88 28 L 90.5 34.5 L 97 37 L 90.5 39.5 L 88 46 L 85.5 39.5 L 79 37 L 85.5 34.5 Z" fill="#F472B6"/>
  <path d="M 28 42 L 30 46.5 L 35 48.5 L 30 50.5 L 28 55 L 26 50.5 L 21 48.5 L 26 46.5 Z" fill="#38BDF8"/>
</svg>"""

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand-card">
        <div style="display:flex; align-items:center; gap:0.75rem;">
            {GENIE_SVG_ICON}
            <div>
                <div style="font-weight:800; font-size:1.15rem; color:#F8FAFC; line-height:1.2;">NewsGenie</div>
                <div style="font-size:0.7rem; color:#818CF8; font-weight:700; letter-spacing:0.04em;">INTELLIGENT AGENT v2.0</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Connectivity Status Display (Keys hidden securely)
    has_gemini = bool(os.environ.get("GEMINI_API_KEY"))
    has_tavily = bool(os.environ.get("TAVILY_API_KEY"))
    has_news = bool(os.environ.get("NEWSAPI_KEY"))

    st.markdown("""
    <div class="sidebar-status-card">
        <div style="font-size:0.75rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.6rem;">System & API Services</div>
        <div class="key-status-row">
            <span>Gemini Reasoning</span>
            <span><span class="key-status-dot {}"></span> <span style="font-size:0.75rem; color:{};">{}</span></span>
        </div>
        <div class="key-status-row">
            <span>Tavily Web Search</span>
            <span><span class="key-status-dot {}"></span> <span style="font-size:0.75rem; color:{};">{}</span></span>
        </div>
        <div class="key-status-row">
            <span>NewsAPI Headlines</span>
            <span><span class="key-status-dot {}"></span> <span style="font-size:0.75rem; color:{};">{}</span></span>
        </div>
        <div style="font-size:0.7rem; color:#64748B; margin-top:0.5rem; text-align:center;">
            🔒 Keys loaded securely from environment (.env)
        </div>
    </div>
    """.format(
        "dot-connected" if has_gemini else "dot-missing", "#34D399" if has_gemini else "#94A3B8", "Connected" if has_gemini else "Not Configured",
        "dot-connected" if has_tavily else "dot-missing", "#34D399" if has_tavily else "#94A3B8", "Connected" if has_tavily else "Not Configured",
        "dot-connected" if has_news else "dot-missing", "#34D399" if has_news else "#94A3B8", "Connected" if has_news else "Not Configured",
    ), unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Topic Launchers")
    st.markdown("<div style='font-size:0.78rem; color:#94A3B8; margin-bottom:0.5rem;'>Fetch curated category headlines:</div>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("🤖 Technology", use_container_width=True):
            st.session_state.shortcut = "What are the latest breaking technology news and AI advancements today?"
        if st.button("📈 Business", use_container_width=True):
            st.session_state.shortcut = "What is the latest global business, finance, and market news?"
        if st.button("🔬 Science", use_container_width=True):
            st.session_state.shortcut = "What are the latest scientific discoveries and space updates?"
    with col_t2:
        if st.button("🩺 Health", use_container_width=True):
            st.session_state.shortcut = "Show me the latest health and medical research news."
        if st.button("🏆 Sports", use_container_width=True):
            st.session_state.shortcut = "What are the top sports headlines and match results today?"
        if st.button("🎭 Entertainment", use_container_width=True):
            st.session_state.shortcut = "What are the latest entertainment, movie, and culture stories?"

    st.markdown("### 🛠️ Session Controls")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_s2:
        # Export transcript button
        chat_text = ""
        if "messages" in st.session_state and st.session_state.messages:
            for m in st.session_state.messages:
                role = "NewsGenie" if m["role"] == "assistant" else "User"
                chat_text += f"### {role}\n{m['content']}\n\n---\n\n"
        st.download_button(
            label="📥 Export Chat",
            data=chat_text or "No conversation yet.",
            file_name="newsgenie-conversation.md",
            mime="text/markdown",
            use_container_width=True,
            disabled=not bool(chat_text)
        )

    st.markdown("""
    <div class="footer-container">
        <div><strong>NewsGenie</strong> • Built by <a href="https://winelogbooks.com" target="_blank">Nathan Lester</a></div>
        <div style="font-size:0.75rem; margin-top:0.25rem;">LangGraph • Gemini 2.5 Flash • Tavily • NewsAPI</div>
    </div>
    """, unsafe_allow_html=True)


# ----------------- MAIN UI -----------------

# Header Hero Section
st.markdown(f"""
<div class="hero-container">
    <h1 class="hero-title">
        {GENIE_SVG_ICON}
        <span>NewsGenie</span>
    </h1>
    <div class="hero-subtitle">
        Your intelligent AI companion for real-time news aggregation, live web search, and contextual reasoning.
    </div>
    <div class="badge-container">
        <span class="badge-pill">✨ Google Gemini 2.5 Flash</span>
        <span class="badge-pill">⚡ LangGraph State Graph</span>
        <span class="badge-pill">📰 NewsAPI Engine</span>
        <span class="badge-pill">🔍 Tavily Real-Time Search</span>
        <span class="badge-pill badge-pill-status">🟢 System Ready</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize LangGraph app
if "graph_app" not in st.session_state:
    if os.environ.get("GEMINI_API_KEY"):
        st.session_state.graph_app = get_app()
    else:
        st.session_state.graph_app = None

# Re-init if key was supplied and app is none
if os.environ.get("GEMINI_API_KEY") and st.session_state.graph_app is None:
    st.session_state.graph_app = get_app()
    st.rerun()

# Empty State Welcome Dashboard
if not st.session_state.messages:
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h3 style="font-weight:700; color:#F8FAFC; margin-bottom:0.25rem;">👋 Welcome to NewsGenie</h3>
        <p style="color:#94A3B8; font-size:0.9rem; margin:0;">
            Ask any question, explore breaking headlines across categories, or perform live factual searches. Select a prompt below or start typing.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="starter-card">
            <div class="starter-card-title">🚀 Tech & Artificial Intelligence</div>
            <div class="starter-card-desc">Explore the most significant AI updates, breakthroughs, and gadget launches.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ask: AI & Tech Breakthroughs", key="sc_tech", use_container_width=True):
            st.session_state.shortcut = "What are the biggest breakthroughs in AI and tech today?"
            st.rerun()

        st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="starter-card">
            <div class="starter-card-title">📊 Global Economy & Markets</div>
            <div class="starter-card-desc">Get timely summaries of financial markets, central bank moves, and economy trends.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ask: Global Markets Update", key="sc_biz", use_container_width=True):
            st.session_state.shortcut = "Provide a summary of the latest global market moves and business headlines."
            st.rerun()

    with col2:
        st.markdown("""
        <div class="starter-card">
            <div class="starter-card-title">🔍 Real-Time Web Deep Dive</div>
            <div class="starter-card-desc">Search the live web for verified facts, recent events, and technical topics.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ask: Space Exploration News", key="sc_space", use_container_width=True):
            st.session_state.shortcut = "What are the latest developments and missions in space exploration this week?"
            st.rerun()

        st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="starter-card">
            <div class="starter-card-title">🌍 Global Top Headlines</div>
            <div class="starter-card-desc">Curated headlines from top global publishers across major international stories.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ask: Top World Headlines", key="sc_world", use_container_width=True):
            st.session_state.shortcut = "What are the top general news headlines in the world right now?"
            st.rerun()

# Display chat history on app rerun
for message in st.session_state.messages:
    if message.get("role") != "system":
        avatar = "assets/genie_logo.svg" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Process input / shortcut trigger
prompt_input = st.chat_input("Ask a question, request breaking news, or search the web...")

# If shortcut button was clicked
prompt = None
if "shortcut" in st.session_state and st.session_state.shortcut:
    prompt = st.session_state.shortcut
    st.session_state.shortcut = None
elif prompt_input:
    prompt = prompt_input

if prompt:
    # Display user message in chat container
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if not os.environ.get("GEMINI_API_KEY"):
        st.warning("⚠️ **Gemini API Key Required**: Please configure your `GEMINI_API_KEY` in the `.env` file to enable reasoning.", icon="🔒")
        st.stop()
        
    try:
        # Prepare inputs for LangGraph
        langchain_messages = []
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                langchain_messages.append(("user", msg["content"]))
            else:
                langchain_messages.append(("assistant", msg["content"]))
                
        with st.spinner("NewsGenie is analyzing, gathering sources, and generating insights..."):
            if st.session_state.graph_app is None:
                st.session_state.graph_app = get_app()
                
            app = st.session_state.graph_app
            final_state = app.invoke({"messages": langchain_messages})
            
            # The last message in the state is the AI's final response
            response = final_state["messages"][-1]
            content_val = response.content
            
            # Google Gemini models may return a list of dictionaries instead of a simple string
            if isinstance(content_val, list):
                parts = []
                for p in content_val:
                    if isinstance(p, dict) and "text" in p:
                        parts.append(p["text"])
                    elif isinstance(p, str):
                        parts.append(p)
                response_content = " ".join(parts).strip()
            else:
                response_content = str(content_val)
            
        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar="assets/genie_logo.svg"):
            st.markdown(response_content)
            
        # Add assistant message to session state cache
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ An error occurred while processing your request: {str(e)}")



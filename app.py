import streamlit as st
import os
from dotenv import load_dotenv

# Try loading from .env
load_dotenv()

from newsgenie.workflow import get_app

st.set_page_config(page_title="NewsGenie", page_icon="🧞", layout="wide")

st.title("🧞 NewsGenie")
st.markdown("Your unified platform for conversational queries and real-time news.")

with st.sidebar:
    st.header("Settings")
    
    gemini_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    tavily_key = st.text_input("Tavily API Key", type="password", value=os.getenv("TAVILY_API_KEY", ""))
    news_key = st.text_input("NewsAPI Key", type="password", value=os.getenv("NEWSAPI_KEY", ""))
    
    st.markdown("---")
    st.markdown("### Shortcuts")
    if st.button("Get Technology News"):
        st.session_state.shortcut = "Show me the top technology news"
    if st.button("Get Business News"):
        st.session_state.shortcut = "What is the latest business news?"

    # Update env vars dynamically
    if gemini_key: 
        os.environ["GEMINI_API_KEY"] = gemini_key
        os.environ["GOOGLE_API_KEY"] = gemini_key
    if tavily_key: os.environ["TAVILY_API_KEY"] = tavily_key
    if news_key: os.environ["NEWSAPI_KEY"] = news_key

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize LangGraph app
if "graph_app" not in st.session_state:
    if "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"]:
        st.session_state.graph_app = get_app()
    else:
        st.session_state.graph_app = None
        
# Re-init if key changes
if gemini_key and st.session_state.graph_app is None:
    st.session_state.graph_app = get_app()
    st.rerun()

# Display chat history on app rerun
for message in st.session_state.messages:
    if message.get("role") != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Ask me a general question or request the latest news!")

if "shortcut" in st.session_state and st.session_state.shortcut:
    prompt = st.session_state.shortcut
    st.session_state.shortcut = None

if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to session state cache (for UI)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Please provide a Gemini API Key in the sidebar.")
        st.stop()
        
    try:
        # Prepare inputs for LangGraph
        langchain_messages = []
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                langchain_messages.append(("user", msg["content"]))
            else:
                langchain_messages.append(("assistant", msg["content"]))
                
        with st.spinner("Processing your request..."):
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
        with st.chat_message("assistant"):
            st.markdown(response_content)
            
        # Add assistant message to session state cache
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

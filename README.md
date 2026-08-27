# 🧞 NewsGenie

An intelligent AI-powered assistant that combines conversational reasoning with real-time news retrieval and live web search using **LangGraph**, **Google Gemini**, **NewsAPI**, and **Tavily**.

---

## 🌟 Overview

**NewsGenie** solves the problem of static LLM knowledge cutoffs by integrating dynamic multi-tool routing inside a cyclical state graph. The agent dynamically decides whether to:
1. **Answer directly** from model knowledge for general inquiries.
2. **Fetch categorized headlines** via **NewsAPI** for current news topics.
3. **Perform live web search** via **Tavily** for recent factual verification.

Built with a sleek, modern **Streamlit** dark glassmorphism interface featuring dynamic API status telemetry, one-click category launchers, starter prompt cards, markdown transcript export, interactive chat history, and runtime key configuration.

---

## 🏗️ Architecture

```
                 +-------------------+
                 |   User Prompt     |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | LangGraph Agent   |<-----------+
                 | (Gemini 2.5 Flash)|            |
                 +---------+---------+            |
                           |                      |
            +--------------+--------------+       |
            |                             |       |
            v                             v       |
   [ Fetch News Tool ]          [ Web Search Tool ]
   (NewsAPI Headlines)          (Tavily API Search)
            |                             |       |
            +--------------+--------------+       |
                           |                      |
                           +----------------------+
                           | (Tool Outputs)
                           v
                 +-------------------+
                 | Final Response to |
                 |     User UI       |
                 +-------------------+
```

---

## 🛠️ Tech Stack

- **Orchestration / Graph:** [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain)
- **Foundation Model:** Google Gemini (`gemini-2.5-flash`) via `langchain-google-genai`
- **External Tools & APIs:** [NewsAPI](https://newsapi.org/), [Tavily AI Search](https://tavily.com/)
- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Language:** Python 3.10+

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/N8Space/NewsGenie.git
cd NewsGenie
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file from the example template:
```bash
cp .env.example .env
```
Fill in your API keys in `.env` (loaded securely by the application):
```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
NEWSAPI_KEY=your_news_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
NewsGenie/
├── .streamlit/
│   └── config.toml     # Modern theme configuration
├── newsgenie/
│   ├── __init__.py
│   ├── tools.py        # NewsAPI and Tavily search tool definitions
│   └── workflow.py     # LangGraph state graph & Gemini agent compilation
├── app.py              # Modern Streamlit chat interface & session handling
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules for Python, venv & keys
└── README.md           # Documentation & Architecture overview
```

---

## 👤 Author

**Nathan Lester**
- AI Enablement Lead & Cloud AI Practitioner
- Portfolio: [winelogbooks.com](https://winelogbooks.com)

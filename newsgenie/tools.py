import os
import requests
from langchain_core.tools import tool
from tavily import TavilyClient

@tool
def fetch_news(category: str, query: str = "") -> str:
    """Fetch the latest news based on a news category and an optional specific query."""
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        return "Error: NEWSAPI_KEY environment variable is missing. Cannot fetch news."

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": "us"
    }
    
    # NewsAPI accepts categories: business, entertainment, general, health, science, sports, technology
    valid_categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    if category.lower() in valid_categories:
        params["category"] = category.lower()
    
    if query:
        params["q"] = query

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            return f"Error fetching news from API: {data.get('message', 'Unknown error')}"

        articles = data.get("articles", [])
        if not articles:
            return f"No news found for category '{category}' and query '{query}'."

        results = []
        for a in articles[:5]:  # Top 5 articles
            title = a.get("title", "No Title")
            source = a.get("source", {}).get("name", "Unknown Source")
            url = a.get("url", "")
            desc = a.get("description", "No description available.")
            results.append(f"### {title}\n- **Source:** {source}\n- **Summary:** {desc}\n- **Link:** {url}")
            
        return "\n\n".join(results)
    except Exception as e:
        return f"Warning: Failed to fetch news due to an error: {str(e)}. Fallback to general knowledge if needed."

@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information utilizing the Tavily API."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY environment variable is missing. Cannot search the web."
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, search_depth="basic", max_results=3)
        results = response.get("results", [])
        
        if not results:
            return f"No web search results found for query '{query}'."

        formatted_results = []
        for r in results:
            title = r.get("title", "No Title")
            url = r.get("url", "")
            content = r.get("content", "")
            formatted_results.append(f"**{title}**\n{content}\nSource: {url}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Warning: Web search failed due to an error: {str(e)}."

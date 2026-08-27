import os
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from newsgenie.tools import fetch_news, web_search

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def get_app():
    # Initialize the tools
    tools = [fetch_news, web_search]
    tool_node = ToolNode(tools)

    # Initialize the model using Google Gemini
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    model_with_tools = model.bind_tools(tools)

    # Define the core agent function
    def call_model(state: AgentState):
        messages = state['messages']
        
        if not messages or not isinstance(messages[0], SystemMessage):
            system_prompt = SystemMessage(
                content="You are NewsGenie, a sleek, intelligent AI news aggregator and conversational assistant designed to be a unified platform for answering general queries, conducting deep research, and fetching real-time news.\n\n"
                        "Guidelines:\n"
                        "1. If the user asks for news, use the `fetch_news` tool. Always deduce the closest valid category (business, entertainment, general, health, science, sports, technology).\n"
                        "2. If the user asks for current up-to-date facts outside of standard news contexts, use `web_search`.\n"
                        "3. If the user asks general conceptual, coding, or reasoning questions that can be answered with your training data alone, respond directly.\n"
                        "4. Formatting: Deliver answers in a clean, modern, well-structured format with clear headings, concise bullet points, key takeaways, and markdown links for sources when applicable.\n"
                        "5. If a tool fails to return valid results, politely inform the user and use another tool as a fallback if appropriate."
            )
            messages = [system_prompt] + messages
            
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    # Define the graph
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    app = workflow.compile()
    return app

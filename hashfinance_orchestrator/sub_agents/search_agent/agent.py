from google.adk.agents import Agent
from google.adk.tools import google_search
from hashfinance_orchestrator.utils.model import GEMINI_MODEL

search_agent = Agent(
    name="search_agent",
    model=GEMINI_MODEL,
    tools = [google_search],
    description=(
        "A specialized agent that accesses the public internet using Google Search to find "
        "real-time or historical information on financial instruments like stocks, mutual funds, "
        "or economic data (e.g., inflation rates)."
    ),
    instruction="""
    You have one function: to receive a specific query, search for it online, and return only the factual data you find.

    - **DO:** Execute the search and provide the information found (e.g., stock price, fund performance data, news articles).
    - **DO:** Cite the source URL if possible.
    - **DO NOT:** Analyze the data, answer the user's broader question, or offer opinions. Simply return the facts. For example, if asked "Should I invest in GOOG?", search for Google's stock performance and news, and return that data, not an investment recommendation.
    """,
)

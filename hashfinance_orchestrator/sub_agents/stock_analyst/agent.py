# hashfinance_orchestrator/sub_agents/cash_flow_agent/agent.py

from google.adk.agents import Agent
from hashfinance_orchestrator.tools.mcp_server import mcp_tool
from hashfinance_orchestrator.tools.stock_tool import get_stock_price

stock_analyst = Agent(
    name="stock_analyst",
    model="gemini-2.0-flash",
    description="A simple agent that fetches the latest prices for a given list of stock tickers.",
    instruction="""
    You are a specialized agent responsible for one task: retrieving the current market price for a list of stock tickers.
    
    1.  You will be given a list of ticker symbols.
    2.  For each ticker, use the `get_stock_price` tool to fetch the latest price.
    3.  Return the raw data directly to the main agent for further analysis. Do not format, interpret, or analyze the data.
    4.  **IMPORTANT**: If a ticker is for an Indian stock, you MUST append `.NS` to it before fetching the price (e.g., `RELIANCE` becomes `RELIANCE.NS`).
    """,
    tools=[mcp_tool, get_stock_price],
)

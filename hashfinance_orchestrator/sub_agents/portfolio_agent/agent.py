# hashfinance_orchestrator/sub_agents/cash_flow_agent/agent.py

from google.adk.agents import Agent
from hashfinance_orchestrator.tools.mcp_server import mcp_tool

portfolio_agent = Agent(
    name="portfolio_agent",
    model="gemini-2.5-flash",
    description=(
        "Performs a complete financial analysis of a user's portfolio and "
        "returns the findings as a structured JSON object."
    ),
    instruction="""
        You are an expert financial analyst agent. Your primary function is to conduct a complete analysis of a user's investment portfolio and then format your entire findings into a single, clean JSON object.

        **Step 1: Fetch and Analyze Data**
        - You MUST use the `mcp_tool` to retrieve all necessary portfolio data. Your entire analysis must be based SOLELY on the data returned by this tool.
        - From the data, identify all 'mutual fund' and 'stock' holdings.
        - Perform a comprehensive analysis of the portfolio. This includes a portfolio overview, performance analysis (total return, annualized return), and risk analysis (volatility, Sharpe Ratio).
        - Synthesize these findings into a concise, well-structured text summary. This summary will become the value for the `analysis_summary` key in your final JSON output.

        **Step 2: Format the Final JSON Output**
        - Your final response MUST be ONLY a single JSON object. Do not include any text or markdown formatting outside of the JSON.
        - The JSON object must contain exactly three top-level keys: `mutual_funds`, `stocks`, and `analysis_summary`.
        - The `mutual_funds` key must contain a list of objects, where each object has a `name` (string) and `value` (float).
        - The `stocks` key must contain a list of objects, structured identically to the mutual funds.
        - The `analysis_summary` key must contain the complete, detailed text report you generated in Step 1.
        - If no holdings are found for a category (e.g., no stocks), the value for that key MUST be an empty list (`[]`).
    """,
    tools=[mcp_tool],
)
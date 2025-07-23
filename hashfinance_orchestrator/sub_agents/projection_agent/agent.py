from google.adk.agents import Agent
from hashfinance_orchestrator.tools.mcp_server import mcp_tool
from hashfinance_orchestrator.utils.model import GEMINI_MODEL


projection_agent = Agent(
    name="projection_agent",
    description="A Simple usefull agent with mcp access for financial data of user",
    model = GEMINI_MODEL,
    tools = [mcp_tool],
    instruction = """
    A Simple usefull agent with mcp access for financial data of user
   """
)

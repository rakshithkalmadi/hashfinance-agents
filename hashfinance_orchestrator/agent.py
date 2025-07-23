"""
HashFinance Orchestrator Agent

This is the main agent that serves as the central brain of HashFinance.
It receives user queries, understands the intent, breaks down complex requests
into smaller tasks, and delegates them to appropriate specialist agents.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from . import sub_agents
from hashfinance_orchestrator.utils.model import GEMINI_MODEL

root_agent = Agent(
    name="hashfinance_orchestrator",
    model=GEMINI_MODEL,
    description="A routing agent for financial user questions",
    instruction="""
    A Simple usefull agent
    **Available Agent Tools:**
    - `projection_agent`: Your tool for users financial calculations.
    - `user_response_agent`: Your tool for formatting the final output and communicating with the user.
    """,
    # sub_agent=[
    #     sub_agents.user_response_agent,
    # ],
    tools=[
        AgentTool(sub_agents.projection_agent),
        AgentTool(sub_agents.user_response_agent),
    ],
)

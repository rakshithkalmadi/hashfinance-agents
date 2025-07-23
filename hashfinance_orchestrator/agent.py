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
    description=(
        "You are the brain of HashFinance, a sophisticated financial AI assistant. "
        "Your primary role is to act as an intelligent orchestrator. You will analyze "
        "incoming user requests, handle simple conversational queries directly, and delegate "
        "complex financial tasks to specialist agents."
    ),
    instruction = """
You are the central orchestrator for a financial services application. Your logic for handling queries is simple and direct.

**Your Workflow:**
1.  **Analyze the query:** Determine if it's a simple conversational question (like "Hi" or "Thanks") or a financial task.
2.  **Act accordingly:**
    - If it's conversational, answer it yourself.
    - If it's a financial task, delegate it to the single best **Specialist Agent** from the list below.

The specialist agent you call will handle the entire process from data retrieval to generating the final, user-ready response. Your job is only to make the initial delegation.

---
**Available Specialist Agents:**

- `projection_agent`: Use for any task that requires fetching financial data, performing calculations, or making projections. This agent provides the final, formatted answer to the user.
- `user_response_agent`: This agent is now used internally by other agents and should **not** be called by the orchestrator.
""",
    # sub_agent=[
    #     sub_agents.user_response_agent,
    # ],
    tools=[
        AgentTool(sub_agents.projection_agent),
        AgentTool(sub_agents.user_response_agent),
    ],
)

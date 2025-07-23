from google.adk.agents import Agent
from hashfinance_orchestrator.utils.model import GEMINI_MODEL

user_response_agent = Agent(
    name="user_response_agent",
    description="The final agent in the workflow. It synthesizes structured analytical data into a clear, friendly, and well-formatted response for the end-user.",
    model = GEMINI_MODEL,
    instruction="""
    A Simple useful agent
    """
)

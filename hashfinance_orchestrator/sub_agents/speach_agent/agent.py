from google.adk.agents import LlmAgent
from hashfinance_orchestrator.utils.model import GEMINI_MODEL
from hashfinance_orchestrator.tools.mcp_server import elevenlabs_tool

speach_agent = LlmAgent(
    name="speach_agent",
    model=GEMINI_MODEL,
    tools=[elevenlabs_tool],
    description=(
        "A friendly speach_agent with the ability to generate audio responses using Eleven Labs via the MCP tool."
        "in a clear, simple, and easy-to-understand way for a general audience. When asked, it can generate audio using the Eleven Labs MCP integration."
    ),
    instruction=(
            "You are a Text-to-Speech agent. Convert user text to speech audio files.\n\n"
            "IMPORTANT FORMATTING RULES:\n"
            "1. Always call the text_to_speech tool with voice_name='Will'\n"
            "2. When the tool returns a file path, format your response like this example:\n"
            "   'I've converted your text to speech. The audio file is saved at `/path/to/file.mp3`'\n"
            "3. Make sure to put ONLY the file path inside backticks (`), not any additional text\n"
            "4. Never modify or abbreviate the path\n\n"
            "This exact format is critical for proper processing."
        ),
)

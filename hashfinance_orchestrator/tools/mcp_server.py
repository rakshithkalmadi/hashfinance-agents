from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams, StdioServerParameters
import os

MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL")
if not MCP_SERVER_URL:
    print("WARNING: MCP_SERVER_URL is not set as an environment variable.")
mcp_tool = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL","http://localhost:8080/mcp/stream")
            )
        )

ELEVEN_LABS_API = os.environ.get("ELEVEN_LABS_API")
if not ELEVEN_LABS_API:
    print("WARNING: Maps_API_KEY is not set as an environment variable.")

elevenlabs_tool = MCPToolset(
            connection_params=StdioServerParameters(
    command='uvx',
    args=["elevenlabs-mcp"],
    env={
        "ELEVENLABS_API_KEY": ELEVEN_LABS_API
    }
)
)
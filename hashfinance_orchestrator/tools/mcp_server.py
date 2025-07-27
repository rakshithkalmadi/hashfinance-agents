from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
import os

MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL")
if not MCP_SERVER_URL:
    print("WARNING: MCP_SERVER_URL is not set as an environment variable.")
mcp_tool = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL","http://localhost:8080/mcp/stream")
            )
        )
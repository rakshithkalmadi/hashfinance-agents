The HashFinance Agents application is a sophisticated, modular financial AI assistant built using Google's Agent Development Kit (ADK) and powered by the Google Gemini large language model. It employs a multi-agent architecture to handle various financial queries, from data analysis and projections to education and personalized advice.

Here's a breakdown of the application's components and their functionalities:

### 1. Core Orchestration

*   **`hashfinance_orchestrator/agent.py` (HashFinance Orchestrator):** This is the central "brain" of the application.
    *   It receives user queries and acts as an intelligent router.
    *   It first checks if the query is a simple conversational opening/closing (e.g., "Hi", "Thanks") and responds directly if so.
    *   Next, it analyzes if the query is a follow-up to the immediately preceding answer and can be answered from that context. If yes, it answers directly without delegating.
    *   For new financial queries or follow-ups requiring new data/calculations, it delegates the task to the most appropriate specialist agent, rephrasing the request to be self-contained.
    *   It uses `GEMINI_MODEL` for its own processing and registers various sub-agents as tools.

### 2. Specialist Agents (Sub-Agents)

These agents reside in `hashfinance_orchestrator/sub_agents/` and are specialized to handle specific financial tasks. They are imported and made available to the Orchestrator via `hashfinance_orchestrator/sub_agents/__init__.py`.

*   **`cash_flow_agent/agent.py` (Cash Flow Agent):**
    *   Analyzes bank transactions to summarize financial inflows, outflows, and net cash flow over specific periods.
    *   **Workflow:** Fetches raw bank transaction data using `mcp_tool.fetch_bank_transactions()`, calculates total inflow/outflow/net cash flow, identifies major inflows/outflows, and packages the analysis into a structured JSON.
    *   Delegates final response formatting to `user_response_agent`.
    *   Handles conversion of string-based numerical values to floats for calculations.

*   **`edu_finance/agent.py` (Education Agent - "Timmy"):**
    *   A friendly financial educator that explains financial concepts, terms, and strategies.
    *   **Workflow:** Uses `google_search` to gather information, formulates concise explanations using simple analogies, avoids jargon, and always includes a mandatory educational disclaimer.

*   **`financial_advisor_agent/agent.py` (Financial Advisor Agent):**
    *   Provides personalized advice on purchases, budgeting, and financial planning.
    *   **Workflow:** Gathers comprehensive financial data using multiple `mcp_tool` functions (`fetch_net_worth`, `fetch_bank_transactions`, `fetch_credit_report`, `fetch_epf_details`, `fetch_mf_transactions`, `fetch_stock_transactions`). If needed, it uses `search_agent` to get external item prices.
    *   Performs detailed financial analysis (disposable income, liquid savings, existing EMIs, debt-to-income ratio, affordability assessment).
    *   Suggests payment plans (direct or EMI) and provides concise, actionable financial advice.
    *   Packages analysis into structured JSON and delegates formatting to `user_response_agent`.

*   **`projection_agent/agent.py` (Projection Agent):**
    *   Specializes in financial data analysis and future projections.
    *   **Workflow:** Identifies the required data-gathering tool (e.g., `fetch_mf_transactions`, `fetch_net_worth`), executes it via `mcp_tool`, performs analysis/prediction, and creates structured JSON.
    *   Delegates final response formatting to `user_response_agent`.

*   **`search_agent/agent.py` (Search Agent):**
    *   A specialized web search agent that accesses the public internet using `google_search`.
    *   **Function:** Finds real-time or historical factual information (e.g., stock prices, economic data) and cites sources. It explicitly *does not* analyze data or offer opinions.

*   **`speach_agent/agent.py` (Speech Agent):**
    *   Generates audio responses from text.
    *   **Workflow:** Uses the `elevenlabs_tool` (from `mcp_server.py`) to convert text to speech, specifically with the voice `Will`. It formats the output to provide the file path of the generated audio.

*   **`user_response_agent/agent.py` (User Response Agent):**
    *   The final agent responsible for formatting responses.
    *   **Function:** Receives structured JSON data from other agents, parses it, and converts it into a clear, friendly, and human-readable string for the end-user. It also incorporates any `assumptions` and `notes` from the JSON naturally into the response.

### 3. Tools and Utilities

*   **`tools/mcp_server.py`:**
    *   Initializes `MCPToolset` instances for interacting with external services.
    *   `mcp_tool`: Connects to the Model Context Protocol (MCP) server (URL from `MCP_SERVER_URL` environment variable) for secure access to user financial data.
    *   `elevenlabs_tool`: Connects to the Eleven Labs API (key from `ELEVEN_LABS_API` environment variable) for text-to-speech functionality.

*   **`utils/model.py`:**
    *   Loads the `GEMINI_MODEL` name from environment variables using `dotenv`. Defaults to 'gemini-1.5-flash-latest' if not set.

### 4. Overall Architecture and Data Flow

The application follows a clear delegation pattern:
1.  The **Orchestrator** receives a user query.
2.  It determines the intent and either responds directly or delegates to a **Specialist Agent**.
3.  **Specialist Agents** use `mcp_tool` to fetch internal user financial data and/or `google_search` (via `search_agent`) for external public data.
4.  Specialist Agents perform their specific analysis and generate structured JSON output.
5.  This JSON output is then passed to the **User Response Agent** for conversion into a user-friendly, natural language response.
6.  The formatted response is returned up the chain to the Orchestrator, and finally to the user.

The system is designed for modularity, allowing easy addition of new specialist agents. It relies heavily on environment variables for configuration, particularly for API keys and server URLs, promoting secure handling of sensitive information.
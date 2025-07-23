"# HashFinance Agents

HashFinance is an intelligent financial AI assistant system built using Google's Agent Development Kit (ADK). It provides users with comprehensive financial analysis, projections, and educational content through a sophisticated multi-agent architecture.

## 🚀 What is HashFinance?

HashFinance is a conversational AI platform that helps users:
- **Analyze Financial Data**: Retrieve and analyze personal financial information from connected accounts
- **Make Financial Projections**: Predict future net worth, investment growth, and financial scenarios
- **Learn Financial Concepts**: Get clear, simple explanations of complex financial terms and strategies
- **Access Real-time Market Data**: Search for current market information, stock prices, and financial news

## 🏗️ Architecture Overview

The system follows a hierarchical multi-agent architecture with intelligent task delegation:

```
┌─────────────────────────────────────┐
│        HashFinance Orchestrator     │
│         (Main Brain Agent)          │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│Projection│ │Education│ │Response │
│ Agent   │ │ Agent   │ │ Agent   │
└─────────┘ └─────────┘ └─────────┘
    │
    └─── Search Agent
```

## 🧠 Core Components

### 1. **HashFinance Orchestrator** (`hashfinance_orchestrator/agent.py`)
The central brain that:
- Analyzes user queries and conversation context
- Handles simple conversational interactions directly
- Routes complex financial tasks to specialist agents
- Maintains conversation flow and context awareness

**Key Features:**
- 3-step decision workflow for efficient query handling
- Context-aware follow-up question processing
- Intelligent task delegation to specialist agents

### 2. **Projection Agent** (`sub_agents/projection_agent/agent.py`)
Specializes in financial data analysis and future projections:
- Fetches user financial data via MCP (Model Context Protocol) server
- Performs financial calculations and projections
- Handles queries like "What will my net worth be in 5 years?"
- Makes reasonable assumptions when data is incomplete

**Workflow:**
1. Understands the financial goal
2. Executes appropriate data-gathering tools
3. Creates structured JSON with analysis results
4. Formats response through the User Response Agent

### 3. **Education Agent** (`sub_agents/edu_finance/agent.py`)
A friendly financial educator named "Timmy":
- Explains financial concepts in simple, accessible language
- Uses real-world analogies to clarify complex topics
- Searches the web for current financial information
- Always includes disclaimers for educational content

### 4. **Search Agent** (`sub_agents/search_agent/agent.py`)
Specialized web search agent:
- Finds real-time financial data (stock prices, market news)
- Retrieves historical financial information
- Provides factual data without analysis or opinions
- Cites sources when possible

### 5. **User Response Agent** (`sub_agents/user_response_agent/agent.py`)
The final formatter that:
- Converts complex JSON data into user-friendly responses
- Ensures consistent, friendly communication tone
- Incorporates assumptions and notes naturally
- Provides well-structured, readable output

## 🔧 Technical Stack

### Core Technologies
- **Google Agent Development Kit (ADK)**: Framework for building AI agents
- **Google Gemini**: Large language model powering the agents
- **Model Context Protocol (MCP)**: For accessing user financial data
- **FastAPI**: Web framework for API endpoints
- **Python 3.11+**: Primary development language

### Key Dependencies
- `google-adk==1.7.0` - Agent framework
- `google-genai==1.26.0` - Gemini model integration
- `mcp==1.12.0` - Model Context Protocol
- `fastapi==0.116.1` - Web framework
- `uvicorn==0.35.0` - ASGI server

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Google Cloud Platform account with API access
- Environment variables configured (see Configuration section)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd hashfinance-agents
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory with:

```env
# Gemini Model Configuration
GEMINI_MODEL=your-gemini-model-name

# MCP Server URL (for financial data access)
MCP_SERVER_URL=http://localhost:8080/mcp/stream

# Google Cloud credentials (if needed)
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

### Running the Application

```bash
# Start the application
python -m hashfinance_orchestrator
```

## 📊 Usage Examples

### Financial Projections
```
User: "How much will my net worth be in 5 years?"
HashFinance: [Fetches current data, applies growth assumptions, provides detailed projection]
```

### Transaction Analysis
```
User: "Show me my recent mutual fund transactions"
HashFinance: [Retrieves and formats transaction history with clear details]
```

### Financial Education
```
User: "What is NAV in mutual funds?"
HashFinance: [Provides simple explanation with analogies and educational context]
```

### Follow-up Conversations
```
User: "Show me my portfolio"
HashFinance: [Shows detailed portfolio breakdown]
User: "Which investment performed best?"
HashFinance: [Analyzes previous response to answer without new data calls]
```

## 🔄 Agent Workflow

### Orchestrator Decision Process
1. **Simple Conversation**: Direct response for greetings, thanks, etc.
2. **Follow-up Analysis**: Checks if question can be answered from recent context
3. **Task Delegation**: Routes complex queries to appropriate specialist agents

### Projection Agent Process
1. **Goal Understanding**: Analyzes the financial request
2. **Data Execution**: Calls MCP tools for user financial data
3. **JSON Structure**: Creates standardized data format with assumptions
4. **Response Formatting**: Uses User Response Agent for final output
5. **Final Return**: Delivers polished, user-friendly response

## 🛡️ Data Security & Privacy

- **MCP Integration**: Secure access to user financial data through standardized protocol
- **No Data Storage**: Processes data in memory without persistent storage
- **Environment Variables**: Sensitive configurations kept in environment files
- **Educational Disclaimers**: All financial advice includes appropriate disclaimers

## 🔧 Development

### Project Structure
```
hashfinance-agents/
├── hashfinance_orchestrator/          # Main orchestrator package
│   ├── agent.py                       # Main orchestrator agent
│   ├── sub_agents/                    # Specialist agents
│   │   ├── projection_agent/          # Financial analysis & projections
│   │   ├── edu_finance/              # Financial education
│   │   ├── search_agent/             # Web search functionality
│   │   └── user_response_agent/      # Response formatting
│   ├── tools/                        # External tools & integrations
│   │   └── mcp_server.py             # MCP server connection
│   └── utils/                        # Utilities & configuration
│       └── model.py                  # Model configuration
├── test/                             # Test files
├── requirements.txt                  # Python dependencies
└── questions.md                      # Sample queries for testing
```

### Adding New Agents
1. Create new agent directory in `sub_agents/`
2. Implement agent with proper Google ADK structure
3. Add to `sub_agents/__init__.py` for imports
4. Register with orchestrator in main `agent.py`

### Testing
Use the sample queries in `questions.md` for testing different agent functionalities:
- Projection Agent: "How much will I have in 2 years with 10% returns?"
- Education Agent: "What is NAV in mutual funds?"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing agent patterns
4. Test with sample queries
5. Submit a pull request

## 📄 License

This project is part of the HashFinance ecosystem. Please refer to the license terms for usage and distribution.

## 🆘 Support

For issues, questions, or contributions, please refer to the project's issue tracking system or contact the development team.

---

*HashFinance - Making Financial Intelligence Accessible Through AI*" 

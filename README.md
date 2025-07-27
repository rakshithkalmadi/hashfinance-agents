Please check the rk_prod branch for full codde

# HashFinance Agents

HashFinance Agents is a modular, multi-agent financial AI assistant system built using Google's Agent Development Kit (ADK). It provides users with comprehensive financial analysis, projections, education, and actionable advice through a sophisticated, extensible architecture.

## 🚀 What is HashFinance?

HashFinance is a conversational AI platform that helps users:
- **Analyze Financial Data**: Retrieve and analyze personal financial information from connected accounts
- **Make Financial Projections**: Predict future net worth, investment growth, and financial scenarios
- **Learn Financial Concepts**: Get clear, simple explanations of complex financial terms and strategies
- **Access Real-time Market Data**: Search for current market information, stock prices, and financial news
- **Get Personalized Financial Advice**: Receive actionable recommendations on purchases, budgeting, and planning
- **Understand Cash Flow**: Summarize income, expenses, and net cash flow

## 🏗️ Architecture Overview

The system follows a hierarchical, multi-agent architecture with intelligent task delegation:

```
┌─────────────────────────────────────┐
│        HashFinance Orchestrator     │
│         (Main Brain Agent)          │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    │         │         │         │         │
    ▼         ▼         ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Projection│ │Education│ │Response │ │Cash Flow│ │Financial│
│ Agent   │ │ Agent   │ │ Agent   │ │ Agent   │ │Advisor  │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
    │
    └─── Search Agent
```

## 🧠 Core Components & Agent Responsibilities

### 1. **HashFinance Orchestrator** (`hashfinance_orchestrator/agent.py`)
- Central brain that analyzes user queries and conversation context
- Handles simple conversational interactions directly
- Delegates complex financial tasks to specialist agents
- Maintains conversation flow and context awareness
- **Workflow:**
  1. Checks if the query is a simple greeting/closing (answers directly)
  2. Checks if it's a follow-up that can be answered from previous context (answers directly)
  3. Otherwise, delegates to the best specialist agent, rephrasing the request as needed

### 2. **Projection Agent** (`sub_agents/projection_agent/agent.py`)
- Specializes in financial data analysis and future projections
- Fetches user financial data via MCP (Model Context Protocol) server
- Performs calculations and projections (e.g., "What will my net worth be in 5 years?")
- Makes reasonable assumptions when data is incomplete
- **Workflow:**
  1. Understands the financial goal
  2. Executes the appropriate data-gathering tool
  3. Creates structured JSON with analysis results
  4. Formats response through the User Response Agent

### 3. **Education Agent** (`sub_agents/edu_finance/agent.py`)
- Friendly financial educator named "Timmy"
- Explains financial concepts in simple, accessible language using analogies
- Uses web search for current financial information
- Always includes disclaimers for educational content

### 4. **Search Agent** (`sub_agents/search_agent/agent.py`)
- Specialized web search agent
- Finds real-time and historical financial data (stock prices, market news)
- Provides factual data without analysis or opinions
- Cites sources when possible

### 5. **User Response Agent** (`sub_agents/user_response_agent/agent.py`)
- Final formatter that converts complex JSON data into user-friendly responses
- Ensures consistent, friendly communication tone
- Incorporates assumptions and notes naturally

### 6. **Cash Flow Agent** (`sub_agents/cash_flow_agent/agent.py`)
- Analyzes bank transactions to summarize inflows, outflows, and net cash flow for a given period
- Identifies major income and expense items
- Provides clear, actionable summaries of liquidity and spending habits

### 7. **Financial Advisor Agent** (`sub_agents/financial_advisor_agent/agent.py`)
- Provides personalized advice on purchases, budgeting, and planning
- Fetches all relevant user data (net worth, transactions, credit, investments)
- Searches for external prices if needed
- Calculates affordability, payment plans, and gives concise, actionable advice

## 🔧 Technical Stack

- **Google Agent Development Kit (ADK)**: Framework for building AI agents
- **Google Gemini**: Large language model powering the agents
- **Model Context Protocol (MCP)**: For accessing user financial data
- **FastAPI**: Web framework for API endpoints
- **Python 3.11+**: Primary development language
- **Docker**: For containerized deployment

## 📦 Tools & Utilities

- **MCP Tool** (`tools/mcp_server.py`): Connects to the MCP server for secure, real-time access to user financial data
- **Model Config** (`utils/model.py`): Loads the Gemini model name from environment variables

## 📝 Sample Questions & Testing

- **questions.md**: Sample queries for projection and education agents
- **questions_s.md**: Sample queries for cash flow, debt management, and portfolio agents
- **questions.py**: Programmatic sample questions for testing

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
python -m main
```
Or use Docker:
```bash
docker build -t hashfinance-agents .
docker run -p 8080:8080 hashfinance-agents
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

### Cash Flow Summary
```
User: "Summarise my income and expenses."
HashFinance: [Provides a summary of inflows, outflows, and net cash flow]
```

### Personalized Advice
```
User: "Can I afford to buy an iPhone?"
HashFinance: [Analyzes your finances, estimates affordability, and suggests payment plans]
```

## 🔄 Agent Workflow

### Orchestrator Decision Process
1. **Simple Conversation**: Direct response for greetings, thanks, etc.
2. **Follow-up Analysis**: Checks if question can be answered from recent context
3. **Task Delegation**: Routes complex queries to appropriate specialist agents

### Specialist Agent Workflows
- Each agent follows a strict, step-by-step workflow as documented in their respective files
- All agents return structured JSON, which is formatted by the User Response Agent for the end user

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
│   │   ├── edu_finance/               # Financial education
│   │   ├── search_agent/              # Web search functionality
│   │   ├── user_response_agent/       # Response formatting
│   │   ├── cash_flow_agent/           # Cash flow summaries
│   │   └── financial_advisor_agent/   # Personalized financial advice
│   ├── tools/                         # External tools & integrations
│   │   └── mcp_server.py              # MCP server connection
│   └── utils/                         # Utilities & configuration
│       └── model.py                   # Model configuration
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Containerization
├── main.py                            # Application entry point
├── questions.md / questions_s.md      # Sample queries for testing
├── questions.py                       # Programmatic sample questions
└── README.md                          # Project documentation
```

### Adding New Agents
1. Create new agent directory in `sub_agents/`
2. Implement agent with proper Google ADK structure
3. Add to `sub_agents/__init__.py` for imports
4. Register with orchestrator in main `agent.py`

### Testing
Use the sample queries in `questions.md`, `questions_s.md`, or `questions.py` for testing different agent functionalities.

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

*HashFinance - Making Financial Intelligence Accessible Through AI*

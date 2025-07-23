import os
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# This reliably gets the directory where the main.py script is located
# which is also the directory containing your agent folders.
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Example session service URI (e.g., SQLite)
SESSION_SERVICE_URI = "sqlite:///./sessions.db"
# Example allowed origins for CORS
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]
# Set web=True if you intend to serve a web interface, False otherwise
SERVE_WEB_INTERFACE = True

# The get_fast_api_app function will scan the AGENT_DIR
# for all valid agent sub-directories.
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_SERVICE_URI,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

# You can add more FastAPI routes or configurations below if needed
@app.get("/hello")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    # From your project root, run: python main.py
    uvicorn.run(app, host="localhost", port=int(os.environ.get("PORT", 8080)))
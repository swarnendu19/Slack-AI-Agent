from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
import os
from dotenv import load_dotenv
from pathlib import Path
from .services import slack_service, notion_service, calendar_service, openai_service
from .routers import slack, api
from fastapi.responses import JSONResponse
from .services.slack_service import SlackService
from .services.openai_service import OpenAIService
from pydantic import BaseModel
from typing import List, Dict

# Get the absolute path to the .env file
env_path = Path('.') / '.env'
print(f"Looking for .env file at: {env_path.absolute()}")

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Debug: Print environment variables (remove in production)
print("Current working directory:", os.getcwd())
print("SLACK_BOT_TOKEN:", os.getenv("SLACK_BOT_TOKEN"))
print("SLACK_SIGNING_SECRET:", os.getenv("SLACK_SIGNING_SECRET"))

# Verify required environment variables
if not os.getenv("SLACK_BOT_TOKEN"):
    raise ValueError("SLACK_BOT_TOKEN environment variable is not set")
if not os.getenv("SLACK_SIGNING_SECRET"):
    raise ValueError("SLACK_SIGNING_SECRET environment variable is not set")

# Initialize FastAPI app
app = FastAPI(title="AI Slack Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Slack app with explicit token
slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    raise ValueError("SLACK_BOT_TOKEN is not set in environment variables")

slack_app = App(
    token=slack_token,
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

# Include routers
app.include_router(slack.router)
app.include_router(api.router)

slack_service = SlackService()
openai_service = OpenAIService()

class Conversation(BaseModel):
    conversation: List[Dict[str, str]]

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"message": "AI Slack Agent is running"}

@app.post("/slack/events")
async def slack_events(request: Request):
    """Handle Slack events"""
    try:
        # Get the request body
        body = await request.json()
        
        # Handle URL verification
        if body.get("type") == "url_verification":
            return {"challenge": body.get("challenge")}
        
        # Handle other events
        return await slack_service.handler.handle(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/summarize")
async def summarize_conversation(conversation: Conversation):
    """Summarize a conversation"""
    try:
        summary = await openai_service.summarize_conversation(conversation.conversation)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/action-items")
async def extract_action_items(conversation: Conversation):
    """Extract action items from a conversation"""
    try:
        action_items = await openai_service.extract_action_items(conversation.conversation)
        return {"action_items": action_items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/digest")
async def get_daily_digest():
    """Generate daily digest"""
    try:
        # Mock content for testing
        content = {
            "emails": "Important email about project timeline",
            "notion_docs": "Updated project documentation",
            "meetings": "Team sync at 2 PM"
        }
        digest = await openai_service.generate_daily_digest(content)
        return {"digest": digest}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
from fastapi import APIRouter, Request, HTTPException
from ..services.slack_service import SlackService
from ..services.notion_service import NotionService
from ..services.calendar_service import CalendarService
from ..services.openai_service import OpenAIService

router = APIRouter(prefix="/slack", tags=["slack"])
slack_service = SlackService()
notion_service = NotionService()
calendar_service = CalendarService()
openai_service = OpenAIService()

@router.post("/events")
async def handle_slack_events(request: Request):
    """Handle Slack events."""
    try:
        body = await request.json()
        
        # Handle URL verification
        if body.get("type") == "url_verification":
            return {"challenge": body.get("challenge")}
        
        # Handle events
        event = body.get("event", {})
        event_type = event.get("type")
        
        if event_type == "message":
            # Handle message events
            await slack_service.handle_message(event, slack_service.app.client.chat_postMessage)
        elif event_type == "app_mention":
            # Handle mentions
            await slack_service.handle_mention(event, slack_service.app.client.chat_postMessage)
        
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interactions")
async def handle_slack_interactions(request: Request):
    """Handle Slack interactions (buttons, menus, etc.)."""
    try:
        form_data = await request.form()
        payload = form_data.get("payload")
        
        if not payload:
            raise HTTPException(status_code=400, detail="No payload provided")
        
        # Handle different types of interactions
        # Add your interaction handling logic here
        
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
from fastapi import APIRouter, HTTPException
from ..services.slack_service import SlackService
from ..services.notion_service import NotionService
from ..services.calendar_service import CalendarService
from ..services.openai_service import OpenAIService
from typing import Dict, List

router = APIRouter(prefix="/api", tags=["api"])
slack_service = SlackService()
notion_service = NotionService()
calendar_service = CalendarService()
openai_service = OpenAIService()

@router.post("/summarize")
async def summarize_conversation(conversation: List[Dict]):
    """Summarize a conversation."""
    try:
        summary = await openai_service.summarize_conversation(conversation)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/action-items")
async def extract_action_items(conversation: List[Dict]):
    """Extract and sync action items."""
    try:
        # Extract action items
        action_items = await openai_service.extract_action_items(conversation)
        
        # Create tasks in Notion
        for item in action_items.split('\n'):
            if item.strip():
                await notion_service.create_task(
                    title=item.strip(),
                    description=f"Action item from conversation: {item.strip()}"
                )
        
        return {"action_items": action_items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/digest")
async def generate_daily_digest():
    """Generate daily digest."""
    try:
        # Get content from different services
        notion_content = await notion_service.get_daily_digest_content()
        calendar_content = await calendar_service.get_daily_digest_content()
        
        # Combine content
        content = {
            "notion_docs": notion_content,
            "meetings": calendar_content,
            "emails": "Email integration to be implemented"  # Placeholder for email integration
        }
        
        # Generate digest
        digest = await openai_service.generate_daily_digest(content)
        
        # Send to Slack
        await slack_service.send_daily_digest("general", digest)
        
        return {"digest": digest}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
import os
from typing import Dict, List
from .openai_service import OpenAIService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SlackService:
    def __init__(self):
        # Debug: Print environment variables
        print("SLACK_BOT_TOKEN:", os.getenv("SLACK_BOT_TOKEN"))
        print("SLACK_SIGNING_SECRET:", os.getenv("SLACK_SIGNING_SECRET"))

        # Verify required environment variables
        if not os.getenv("SLACK_BOT_TOKEN"):
            raise ValueError("SLACK_BOT_TOKEN environment variable is not set")
        if not os.getenv("SLACK_SIGNING_SECRET"):
            raise ValueError("SLACK_SIGNING_SECRET environment variable is not set")

        # Initialize Slack app with explicit token
        self.app = App(
            token=os.getenv("SLACK_BOT_TOKEN"),
            signing_secret=os.getenv("SLACK_SIGNING_SECRET")
        )
        self.handler = SlackRequestHandler(self.app)
        self.openai_service = OpenAIService()
        
        # Register event handlers
        self.app.message(self.handle_message)
        self.app.event("app_mention")(self.handle_mention)

    async def handle_message(self, event: Dict, say):
        """Handle incoming messages and process them for summarization and action items."""
        try:
            # Get conversation history
            conversation = await self.get_conversation_history(event["channel"], event["ts"])
            
            # Generate summary using OpenAI
            summary = await self.openai_service.summarize_conversation(conversation)
            
            # Extract action items
            action_items = await self.openai_service.extract_action_items(conversation)
            
            # Post summary and action items in thread
            await say(
                text=f"*Conversation Summary:*\n{summary}\n\n*Action Items:*\n{action_items}",
                thread_ts=event["ts"]
            )
            
        except Exception as e:
            print(f"Error handling message: {str(e)}")
            await say(text="Sorry, I encountered an error processing your message.")

    async def handle_mention(self, event: Dict, say):
        """Handle when the bot is mentioned in a channel."""
        try:
            # Get the message text
            message = event.get("text", "")
            
            # Generate suggestions using OpenAI
            suggestions = await self.openai_service.generate_suggestions(message)
            
            # Post suggestions in thread
            await say(
                text=f"*Here are some suggestions:*\n{suggestions}",
                thread_ts=event["ts"]
            )
            
        except Exception as e:
            print(f"Error handling mention: {str(e)}")
            await say(text="Sorry, I encountered an error processing your mention.")

    async def get_conversation_history(self, channel: str, ts: str) -> List[Dict]:
        """Retrieve conversation history for a given channel and timestamp."""
        try:
            result = await self.app.client.conversations_replies(
                channel=channel,
                ts=ts
            )
            return result["messages"]
        except Exception as e:
            print(f"Error getting conversation history: {str(e)}")
            return []

    async def send_daily_digest(self, channel: str, digest_content: str):
        """Send daily digest to a specified channel."""
        try:
            await self.app.client.chat_postMessage(
                channel=channel,
                text=f"*Daily Digest*\n{digest_content}",
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Daily Digest*\n{digest_content}"
                        }
                    }
                ]
            )
        except Exception as e:
            print(f"Error sending daily digest: {str(e)}") 
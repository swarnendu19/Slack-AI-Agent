import os
from openai import AsyncOpenAI
from typing import List, Dict, Optional
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Create a custom httpx.AsyncClient
        http_client = httpx.AsyncClient(
            timeout=30.0,  # Set a reasonable timeout
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        # Initialize OpenAI client with custom http_client
        self.client = AsyncOpenAI(
            api_key=api_key,
            http_client=http_client
        )

    async def summarize_conversation(self, conversation: List[Dict]) -> str:
        """Summarize a conversation using OpenAI."""
        try:
            # Format conversation for the API
            formatted_conversation = "\n".join([
                f"{msg.get('user', 'Unknown')}: {msg.get('text', '')}"
                for msg in conversation
            ])

            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes conversations concisely."},
                    {"role": "user", "content": f"Please summarize this conversation:\n{formatted_conversation}"}
                ]
            )
            content = response.choices[0].message.content
            return content if content is not None else "Unable to summarize conversation."
        except Exception as e:
            print(f"Error summarizing conversation: {str(e)}")
            return "Unable to summarize conversation."

    async def extract_action_items(self, conversation: List[Dict]) -> str:
        """Extract action items from a conversation using OpenAI."""
        try:
            formatted_conversation = "\n".join([
                f"{msg.get('user', 'Unknown')}: {msg.get('text', '')}"
                for msg in conversation
            ])

            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts action items from conversations. Format them as a bulleted list."},
                    {"role": "user", "content": f"Please extract action items from this conversation:\n{formatted_conversation}"}
                ]
            )
            content = response.choices[0].message.content
            return content if content is not None else "Unable to extract action items."
        except Exception as e:
            print(f"Error extracting action items: {str(e)}")
            return "Unable to extract action items."

    async def generate_suggestions(self, message: str) -> str:
        """Generate suggestions based on a message using OpenAI."""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides relevant suggestions based on the context."},
                    {"role": "user", "content": f"Please provide suggestions for this message: {message}"}
                ]
            )
            content = response.choices[0].message.content
            return content if content is not None else "Unable to generate suggestions."
        except Exception as e:
            print(f"Error generating suggestions: {str(e)}")
            return "Unable to generate suggestions."

    async def generate_daily_digest(self, content: Dict[str, str]) -> str:
        """Generate a daily digest from various content sources."""
        try:
            formatted_content = f"""
            Emails: {content.get('emails', '')}
            Notion Docs: {content.get('notion_docs', '')}
            Meetings: {content.get('meetings', '')}
            """

            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise daily digests."},
                    {"role": "user", "content": f"Please create a daily digest from this content:\n{formatted_content}"}
                ]
            )
            content = response.choices[0].message.content
            return content if content is not None else "Unable to generate daily digest."
        except Exception as e:
            print(f"Error generating daily digest: {str(e)}")
            return "Unable to generate daily digest." 
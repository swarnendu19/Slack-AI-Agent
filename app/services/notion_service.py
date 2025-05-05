from notion_client import AsyncClient
import os
from typing import Dict, List

class NotionService:
    def __init__(self):
        self.client = AsyncClient(auth=os.getenv("NOTION_API_KEY"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")

    async def create_task(self, title: str, description: str, assignee: str = None) -> Dict:
        """Create a new task in Notion."""
        try:
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "To Do"
                    }
                }
            }

            if assignee:
                properties["Assignee"] = {
                    "people": [
                        {
                            "id": assignee
                        }
                    ]
                }

            response = await self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": description
                                    }
                                }
                            ]
                        }
                    }
                ]
            )
            return response
        except Exception as e:
            print(f"Error creating task in Notion: {str(e)}")
            return None

    async def get_recent_docs(self, days: int = 1) -> List[Dict]:
        """Get recently updated Notion documents."""
        try:
            response = await self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Last edited time",
                    "last_edited_time": {
                        "past_days": days
                    }
                }
            )
            return response.get("results", [])
        except Exception as e:
            print(f"Error getting recent docs from Notion: {str(e)}")
            return []

    async def update_task_status(self, page_id: str, status: str) -> Dict:
        """Update the status of a task in Notion."""
        try:
            response = await self.client.pages.update(
                page_id=page_id,
                properties={
                    "Status": {
                        "select": {
                            "name": status
                        }
                    }
                }
            )
            return response
        except Exception as e:
            print(f"Error updating task status in Notion: {str(e)}")
            return None

    async def get_daily_digest_content(self) -> str:
        """Get content from Notion for daily digest."""
        try:
            recent_docs = await self.get_recent_docs(days=1)
            digest_content = "Recent Notion Updates:\n"
            
            for doc in recent_docs:
                title = doc.get("properties", {}).get("Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Untitled")
                digest_content += f"- {title}\n"
            
            return digest_content
        except Exception as e:
            print(f"Error getting Notion digest content: {str(e)}")
            return "Unable to fetch Notion updates." 
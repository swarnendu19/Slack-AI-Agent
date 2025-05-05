from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, List

SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.initialize_service()

    def initialize_service(self):
        """Initialize the Google Calendar service."""
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)

            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)

                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)

            self.service = build('calendar', 'v3', credentials=self.creds)
        except Exception as e:
            print(f"Error initializing calendar service: {str(e)}")

    async def create_event(self, summary: str, description: str, start_time: datetime, end_time: datetime, attendees: List[str] = None) -> Dict:
        """Create a new calendar event."""
        try:
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                }
            }

            if attendees:
                event['attendees'] = [{'email': email} for email in attendees]

            event = self.service.events().insert(calendarId='primary', body=event).execute()
            return event
        except Exception as e:
            print(f"Error creating calendar event: {str(e)}")
            return None

    async def get_todays_events(self) -> List[Dict]:
        """Get today's calendar events."""
        try:
            now = datetime.utcnow()
            end_of_day = now.replace(hour=23, minute=59, second=59)

            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now.isoformat() + 'Z',
                timeMax=end_of_day.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            return events_result.get('items', [])
        except Exception as e:
            print(f"Error getting today's events: {str(e)}")
            return []

    async def get_daily_digest_content(self) -> str:
        """Get content from calendar for daily digest."""
        try:
            events = await self.get_todays_events()
            digest_content = "Today's Calendar Events:\n"
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'Untitled Event')
                digest_content += f"- {summary} ({start})\n"
            
            return digest_content
        except Exception as e:
            print(f"Error getting calendar digest content: {str(e)}")
            return "Unable to fetch calendar events." 
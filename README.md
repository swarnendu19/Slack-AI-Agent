# AI Slack Agent

An intelligent Slack bot that helps manage conversations, tasks, and schedules by integrating with Notion and Calendar.

## Features

- Conversation Summarization
- Action Item Extraction and Sync with Notion/Calendar
- In-thread Suggestions
- Daily Digests for Emails, Notion Docs, and Meetings

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:

   ```
   SLACK_BOT_TOKEN=your_slack_bot_token
   SLACK_SIGNING_SECRET=your_slack_signing_secret
   NOTION_API_KEY=your_notion_api_key
   NOTION_DATABASE_ID=your_notion_database_id
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `/slack/events` - Slack event webhook
- `/slack/interactions` - Slack interaction webhook
- `/api/summarize` - Summarize conversations
- `/api/action-items` - Extract and sync action items
- `/api/digest` - Generate daily digests

## Architecture

The application is built using:

- FastAPI for the backend
- Slack SDK for Slack integration
- Notion API for task management
- Google Calendar API for scheduling
- OpenAI API for natural language processing

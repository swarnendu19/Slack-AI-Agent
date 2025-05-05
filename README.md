# AI Slack Agent 🤖

An intelligent Slack bot that enhances team productivity by managing conversations, tasks, and schedules through seamless integration with Notion and Google Calendar.

## 🌟 Features

### 1. Smart Conversation Management

- **Conversation Summarization**: Automatically generates concise summaries of lengthy Slack threads
- **Action Item Extraction**: Identifies and extracts actionable items from conversations
- **In-thread Suggestions**: Provides contextual suggestions and recommendations within threads
- **Smart Notifications**: Intelligent notification management based on conversation context

### 2. Task Management

- **Notion Integration**:
  - Automatic task creation from Slack conversations
  - Two-way sync between Slack and Notion
  - Custom task templates and workflows
- **Task Prioritization**: AI-powered task prioritization based on context and deadlines

### 3. Calendar & Scheduling

- **Meeting Management**:
  - Automatic meeting scheduling from Slack
  - Smart meeting summaries
  - Calendar availability suggestions
- **Daily Digest**:
  - Personalized daily summaries of emails
  - Notion document updates
  - Upcoming meetings and deadlines

## 🏗️ Architecture

### Backend Stack

- **FastAPI**: High-performance async web framework
- **Slack SDK**: Official Slack API integration
- **Notion API**: Task and document management
- **Google Calendar API**: Scheduling and calendar management
- **OpenAI API**: Natural language processing and AI capabilities

### System Components

1. **Event Handler**

   - Processes incoming Slack events
   - Manages webhook endpoints
   - Handles real-time interactions

2. **AI Processing Engine**

   - Conversation analysis
   - Action item extraction
   - Summary generation
   - Context understanding

3. **Integration Layer**

   - Notion sync service
   - Calendar management
   - External API connections

4. **Data Management**
   - Conversation history
   - User preferences
   - Task tracking
   - Analytics

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Slack Workspace with admin access
- Notion account with API access
- Google Cloud project with Calendar API enabled
- OpenAI API key

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/slack-agent.git
   cd slack-agent
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file with the following:

   ```
   SLACK_BOT_TOKEN=your_slack_bot_token
   SLACK_SIGNING_SECRET=your_slack_signing_secret
   NOTION_API_KEY=your_notion_api_key
   NOTION_DATABASE_ID=your_notion_database_id
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📡 API Endpoints

### Slack Integration

- `POST /slack/events` - Handles Slack event webhooks
- `POST /slack/interactions` - Processes Slack interactions

### Core Features

- `POST /api/summarize` - Generates conversation summaries
- `POST /api/action-items` - Extracts and syncs action items
- `POST /api/digest` - Creates daily digests

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the AI capabilities
- Slack for the excellent API
- Notion for the powerful integration features
- Google Calendar API for scheduling capabilities

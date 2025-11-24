# Claude Code Analyzer - Architecture & Data Flow

## System Overview
The incident message analyzer is a defensive security tool that helps teams respond to technical incidents by analyzing Slack communications and providing AI-powered insights.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Slack API     │◄──►│  Python App     │◄──►│ Claude SDK      │
│                 │    │  (Local)        │    │ (via Vertex AI) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Channel Messages│    │ Local JSON Files│    │ GCP Vertex AI   │
│ User Data       │    │ Analysis Results│    │ API Endpoint    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Data Flow Summary

### 1. **Input Sources**
- **Slack Messages**: Real-time incident communications from monitored channels
- **GitHub Repository**: Source code hosted at `github.com/vkumar51/incident-message-analyzer`

### 2. **Processing Components**
- **Slack Bot** (`slack_bot.py`): Monitors channels, collects messages
- **Message Analyzer** (`message_analyzer.py`): Categorizes individual messages
- **Batch Analyzer** (`batch_analyzer.py`): Processes conversation threads
- **Summary Generator** (`summary_generator.py`): Creates executive summaries

### 3. **AI Integration**
- **Claude SDK**: Uses `anthropic[vertex]` Python library
- **Model**: Claude 3.5 Haiku via Google Vertex AI
- **Purpose**: Categorizes messages, generates insights

### 4. **Data Storage**
- **Local Files**: JSON analysis results stored locally
- **No Cloud Storage**: All data remains on local machine
- **No Databases**: Simple file-based persistence

## Data Types Processed

### **Input Data**
- Slack message text
- Message timestamps
- User identifiers
- Channel information

### **Output Data**
- Message categorization (diagnostics/actions/impact/resolution)
- Incident summaries
- Action item lists
- Impact assessments

## Security & Privacy

### **Data Handling**
- ✅ All processing occurs locally
- ✅ No data sent to external services except Claude API
- ✅ Slack tokens stored as environment variables
- ✅ No persistent storage of sensitive data

### **API Interactions**
1. **Slack API**: Read messages, post summaries (OAuth token required)
2. **Vertex AI**: Send message text to Claude for analysis
3. **GitHub**: Standard git operations for source code

### **Authentication**
- `SLACK_BOT_TOKEN`: Slack Bot User OAuth Token (xoxb-*)
- `ANTHROPIC_VERTEX_PROJECT_ID`: Google Cloud Project ID
- Environment variables only, no hardcoded credentials

## Deployment Model
- **Local Execution**: Runs on developer's machine
- **No Server Infrastructure**: Not deployed to cloud
- **Manual Operation**: Started/stopped by user

## Data Retention
- **Slack Messages**: Not permanently stored, only processed
- **Analysis Results**: Saved as timestamped JSON files locally
- **No Automatic Cleanup**: User manages local files

## Compliance Considerations
- **Data Minimization**: Only processes text content of messages
- **Purpose Limitation**: Used solely for incident response analysis
- **Access Control**: Limited by Slack channel permissions
- **Audit Trail**: All analysis results timestamped and saved

---

*This architecture supports defensive security operations by helping teams analyze and respond to technical incidents more effectively.*
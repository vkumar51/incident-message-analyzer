# Incident Message Analyzer

An AI-powered Slack bot that automatically analyzes incident communications, provides real-time insights, and generates comprehensive summaries to help teams respond faster and more effectively to outages and technical issues.

## Features

- **Real-time Message Analysis**: Monitors Slack channels and analyzes incident-related communications
- **Intelligent Categorization**: Automatically categorizes messages (errors, investigations, resolutions, etc.)
- **Comprehensive Summaries**: Generates executive summaries and action items
- **Slack Integration**: Posts analysis directly to monitored channels
- **Batch Processing**: Can analyze conversation histories for post-incident reviews

## Components

- `slack_bot.py` - Main Slack bot with real-time monitoring
- `batch_analyzer.py` - Batch message analysis engine
- `summary_generator.py` - Comprehensive incident summary generation
- `message_analyzer.py` - Core message analysis and categorization

## Prerequisites

- Python 3.8+
- Slack Bot Token with appropriate permissions
- Google Cloud Project with Vertex AI API enabled (for Claude integration)
- Anthropic API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/incident-message-analyzer.git
cd incident-message-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export SLACK_BOT_TOKEN="xoxb-your-slack-bot-token"
export ANTHROPIC_VERTEX_PROJECT_ID="your-gcp-project-id"
export ANTHROPIC_VERTEX_REGION="us-central1"  # optional
```

## Slack App Setup

1. Create a new Slack App at https://api.slack.com/apps
2. Add the following Bot Token Scopes:
   - `channels:read` - View basic information about channels
   - `channels:join` - Join public channels
   - `chat:write` - Send messages
   - `users:read` - View people in the workspace
   - `conversations:history` - View messages in channels

3. Install the app to your workspace
4. Copy the Bot User OAuth Token (starts with `xoxb-`)

## Usage

### Real-time Monitoring

```bash
python3 slack_bot.py
```

Enter the channel name you want to monitor when prompted. The bot will:
- Join the specified channel
- Monitor messages in real-time
- Trigger analysis after 20 messages or 30 minutes
- Post summaries directly to the channel

### Batch Analysis

```python
from batch_analyzer import BatchMessageAnalyzer

analyzer = BatchMessageAnalyzer()
messages = [
    {"text": "🚨 Database is down!", "timestamp": "2024-01-01T10:00:00", "user": "alice"},
    {"text": "Investigating the issue", "timestamp": "2024-01-01T10:05:00", "user": "bob"}
]

results = analyzer.analyze_conversation(messages)
print(results)
```

## Configuration

The bot can be configured through environment variables:

- `SLACK_BOT_TOKEN` - Your Slack bot token (required)
- `ANTHROPIC_VERTEX_PROJECT_ID` - Google Cloud project ID (required)
- `ANTHROPIC_VERTEX_REGION` - GCP region (default: us-central1)

## Analysis Categories

The system categorizes messages into:

- **Error Reports** - Error messages and system failures
- **Investigation** - Debugging and troubleshooting activities
- **Status Updates** - Progress and status communications
- **Resolution** - Problem fixes and solutions
- **Customer Impact** - User-facing impact reports
- **Technical Details** - Technical information and metrics

## Output Format

Analysis results include:

- Message categorization and confidence scores
- Significant event detection
- Incident timeline reconstruction
- Executive summary
- Action items with priority levels
- Key metrics and impact assessment

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- Never commit API keys or tokens to the repository
- Use environment variables for sensitive configuration
- Review the code before running in production environments
- Ensure proper Slack permissions and access controls

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section in `SLACK_SETUP.md`
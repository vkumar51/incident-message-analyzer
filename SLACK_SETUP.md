# Slack Bot Setup Guide

## 🚀 Quick Start

### 1. Create Slack App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name: `Claude Incident Analyzer`
4. Choose your workspace

### 2. Configure Bot Permissions

1. Go to **"OAuth & Permissions"** in sidebar
2. Scroll to **"Scopes"** → **"Bot Token Scopes"**
3. Add these scopes:
   - `channels:read` - View basic info about public channels
   - `channels:join` - Join public channels
   - `chat:write` - Send messages
   - `users:read` - View people in workspace
   - `groups:read` - View basic info about private channels (if needed)

### 3. Install App to Workspace

1. Scroll up to **"OAuth Tokens for Your Workspace"**
2. Click **"Install to Workspace"**
3. Authorize the app
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)

### 4. Set Environment Variables

```bash
export SLACK_BOT_TOKEN='xoxb-your-bot-token-here'
export ANTHROPIC_VERTEX_PROJECT_ID='your-gcp-project'
```

### 5. Install Dependencies & Run

```bash
# Install Slack SDK
source venv/bin/activate
pip install -r requirements.txt

# Run the bot
python3 slack_bot.py
```

## 📋 Testing Instructions

### Create Test Channel

1. Create a new Slack channel: `#claude-test-incident`
2. Invite the bot: `/invite @Claude Incident Analyzer`
3. Run the bot and enter channel name: `claude-test-incident`

### Test Messages

Try posting these test messages to see the analysis:

**Diagnostics:**
```
API latency spiking to 3+ seconds across all regions
Database connection pool maxed out at 100 connections
Found root cause: memory leak in payment service
```

**Actions:**
```
Scaling database connection pool to 200 connections
Restarting api-service-deployment now
Rolling back authentication service to v4.12.1
```

**Impact:**
```
Impact expanded: now affecting 75% of customers in EU
Severity upgraded from degraded to complete outage
```

**Resolution:**
```
Incident officially resolved - all systems normal
Post-mortem scheduled for tomorrow at 2 PM
```

### Expected Behavior

- Bot will analyze messages every **30 minutes** OR after **20 messages**
- Bot posts structured summaries with:
  - Executive summary
  - Action items
  - Category breakdown
  - Status assessment

## 🔧 Advanced Configuration

### Socket Mode (Real-time)

For real-time message processing:

1. Go to **"Socket Mode"** in Slack app settings
2. Enable Socket Mode
3. Generate App Token (starts with `xapp-`)
4. Set `SLACK_APP_TOKEN` environment variable

### Custom Analysis Intervals

Edit `slack_bot.py`:
```python
self.analysis_interval = 900  # 15 minutes
```

### Channel Auto-detection

For automatic incident channel detection, modify the channel pattern:
```python
# Monitor channels matching pattern
if channel_name.startswith('ITN-') or 'incident' in channel_name.lower():
    bot.add_channel_to_monitor(channel_name)
```

## 🚨 Troubleshooting

### Common Issues

**"channel_not_found"**
- Ensure channel exists and bot has access
- Try inviting bot manually: `/invite @Claude Incident Analyzer`

**"missing_scope"**
- Check bot token scopes in Slack app settings
- Reinstall app if scopes were changed

**"not_in_channel"**
- Bot needs to be invited to private channels
- For public channels, bot can auto-join

**Analysis not triggering**
- Check message count (need 20+ messages OR 30+ minutes)
- Verify `ANTHROPIC_VERTEX_PROJECT_ID` is set
- Check bot logs for errors

### Debug Mode

Add debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Notes

- Keep bot tokens secure (use environment variables)
- Bot can read all messages in channels it's invited to
- Consider using separate bot for production vs testing
- Review audit logs in Slack admin panel

## 📈 Production Deployment

For production use:

1. **Use Socket Mode** for real-time processing
2. **Add database** for message persistence
3. **Implement proper logging** and monitoring
4. **Add error handling** and retries
5. **Scale with multiple workers** if needed
6. **Set up alerting** for bot failures
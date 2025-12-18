# Invite-Only Mode - Claude Incident Analyzer

## Overview

The Claude Incident Message Analyzer now runs in **invite-only mode**. This means:

✅ **No channel configuration required**
✅ **Available to all teams in your Slack workspace**
✅ **Users control which channels to monitor**
✅ **Zero configuration - just invite and use**

---

## How It Works

### 1. **Deploy Once, Use Everywhere**

Deploy the bot to Docker/OpenShift **once**:
```bash
# Only 2 environment variables needed:
SLACK_BOT_TOKEN=xoxb-your-token
ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id

# That's it! No channel configuration!
```

### 2. **Invite to Channels as Needed**

When you need incident analysis in a channel:
```
/invite @claude_incident_analy
```

The bot will **immediately start monitoring** that channel.

### 3. **Remove When Done**

After the incident is resolved:
```
/remove @claude_incident_analy
```

The bot will **stop monitoring** that channel.

---

## User Workflow

### **During an Incident:**

1. Go to your incident channel (e.g., `#incident-db-outage`)
2. Type: `/invite @claude_incident_analy`
3. Continue your incident response normally
4. After 20 messages OR 30 minutes, bot posts AI-powered analysis
5. Review the analysis and use it for documentation

### **After the Incident:**

1. Type: `/remove @claude_incident_analy` (optional)
2. Bot stops monitoring that channel
3. Bot remains available for future incidents

---

## Benefits

### **For Users:**
- ✅ No waiting for admin to configure channels
- ✅ Use it when you need it
- ✅ Works in any channel (public or private)
- ✅ Self-service - invite it yourself

### **For Administrators:**
- ✅ Deploy once, forget about it
- ✅ No per-channel configuration
- ✅ No environment variable updates
- ✅ No container restarts needed
- ✅ Scales to unlimited channels

### **For Organizations:**
- ✅ Every team can use the same bot
- ✅ No dedicated instances per team
- ✅ Lower infrastructure costs
- ✅ Easier to maintain

---

## Technical Details

### **Auto-Discovery**

When the bot starts, it:
1. Connects to Slack
2. Discovers all channels it's a member of
3. Starts monitoring those channels automatically
4. Checks for new invitations every 5 minutes

### **Real-Time Monitoring**

When invited to a channel:
- ✅ Starts monitoring within 5 minutes (or immediately if just started)
- ✅ Collects messages in real-time
- ✅ Triggers analysis after 20 messages OR 30 minutes
- ✅ Posts AI-generated summary back to the channel

### **Multi-Channel Support**

The bot can monitor **multiple channels simultaneously**:
- Each channel tracked independently
- Separate message buffers per channel
- Individual analysis timers per channel
- No cross-contamination of incidents

---

## Example: Typical Day

**9:00 AM** - Bot deployed to OpenShift
```
✅ Bot is running and waiting for invitations...
```

**11:30 AM** - Database incident starts
```
User in #incident-db: /invite @claude_incident_analy
✅ Bot starts monitoring #incident-db
```

**12:00 PM** - 20 messages reached
```
🤖 Bot posts AI analysis of the database incident
```

**2:00 PM** - API incident starts
```
User in #incident-api: /invite @claude_incident_analy
✅ Bot starts monitoring #incident-api (still monitoring #incident-db)
```

**3:00 PM** - Both incidents resolved
```
Users can optionally /remove the bot or leave it for future use
```

---

## Comparison: Before vs After

### **Before (Channel Config Required)**

❌ Administrator must configure channel name
❌ Requires environment variable update
❌ Requires container restart
❌ One channel per deployment
❌ Teams must request access
❌ Deployment per team/channel

**Configuration:**
```yaml
env:
  - SLACK_CHANNEL_NAME: "incident-alerts"  # Hard-coded!
```

---

### **After (Invite-Only Mode)**

✅ No channel configuration
✅ No environment variable updates
✅ No container restarts
✅ Unlimited channels
✅ Self-service for teams
✅ Single shared deployment

**Configuration:**
```yaml
env:
  # No SLACK_CHANNEL_NAME needed!
```

**Usage:**
```
/invite @claude_incident_analy in any channel
```

---

## FAQs

### **Q: Can the bot monitor private channels?**
A: Yes! Just invite it to any private channel.

### **Q: What if I invite it by mistake?**
A: Simply `/remove @claude_incident_analy` to stop monitoring.

### **Q: How many channels can it monitor?**
A: Unlimited! The bot handles multiple channels simultaneously.

### **Q: Does it monitor ALL channels in Slack?**
A: No! It ONLY monitors channels it's been explicitly invited to.

### **Q: Do I need to restart the container when adding channels?**
A: No! Just invite the bot - it discovers new invitations automatically.

### **Q: What if the bot is already in a channel?**
A: It will automatically start monitoring it when the container starts.

### **Q: Can I see which channels are being monitored?**
A: Check the bot's startup logs - it lists all monitored channels.

---

## Deployment

### **Docker:**
```bash
docker run -d \
  -e SLACK_BOT_TOKEN='xoxb-your-token' \
  -e ANTHROPIC_VERTEX_PROJECT_ID='your-project-id' \
  incident-message-analyzer:latest
```

### **OpenShift:**
```bash
oc create secret generic incident-analyzer-secrets \
  --from-literal=SLACK_BOT_TOKEN='xoxb-your-token' \
  --from-literal=ANTHROPIC_VERTEX_PROJECT_ID='your-project-id'

oc apply -f openshift/configmap.yaml
oc apply -f openshift/buildconfig.yaml
oc start-build incident-analyzer
oc apply -f openshift/deployment-with-imagestream.yaml
```

**That's it!** No channel configuration needed.

---

## Support

**Bot not responding?**
1. Check if bot is running: `docker ps` or `oc get pods`
2. Check bot is in the channel: Look for "claude_incident_analy" in member list
3. Check logs: `docker logs <container>` or `oc logs deployment/incident-analyzer`

**Need to add a channel?**
```
/invite @claude_incident_analy
```

**Need to remove from a channel?**
```
/remove @claude_incident_analy
```

---

**Version**: 2.0 - Invite-Only Mode
**Last Updated**: December 2024
**Author**: Vikas Kumar (vkumar@redhat.com)

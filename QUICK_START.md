# Quick Start Guide - Claude Incident Message Analyzer

## For Teams Deploying to Their Own OpenShift Cluster

This is a 5-minute quick start guide for teams who want to deploy the Claude Incident Message Analyzer to their own OpenShift cluster.

---

## Prerequisites

✅ Access to an OpenShift cluster (v4.10+)
✅ OpenShift CLI (`oc`) installed
✅ Slack Bot Token (`xoxb-...`)
✅ Google Cloud Project ID (with Vertex AI enabled)
✅ Slack channel name to monitor

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/openshift-online/incident-message-analyzer.git
cd incident-message-analyzer
```

---

## Step 2: Login to Your OpenShift Cluster

```bash
oc login <your-openshift-cluster-url>
```

---

## Step 3: Create Namespace

```bash
oc apply -f openshift/namespace.yaml
oc project incident-analyzer
```

---

## Step 4: Create Secrets

**Replace with your actual credentials:**

```bash
oc create secret generic incident-analyzer-secrets \
  --from-literal=SLACK_BOT_TOKEN='xoxb-YOUR-ACTUAL-SLACK-TOKEN' \
  --from-literal=ANTHROPIC_VERTEX_PROJECT_ID='your-gcp-project-id' \
  -n incident-analyzer
```

---

## Step 5: Configure the Channel

Edit the ConfigMap to set your Slack channel:

```bash
oc apply -f openshift/configmap.yaml

# Edit to set your channel name
oc edit configmap incident-analyzer-config
```

Change `SLACK_CHANNEL_NAME` to your channel (e.g., `incident-prod`).

---

## Step 6: Build the Image

```bash
# Create BuildConfig and ImageStream
oc apply -f openshift/buildconfig.yaml

# Start the build
oc start-build incident-analyzer

# Watch build progress (takes 3-5 minutes)
oc logs -f bc/incident-analyzer
```

Wait for the build to show "Push successful" before continuing.

---

## Step 7: Deploy the Application

```bash
oc apply -f openshift/deployment-with-imagestream.yaml
```

---

## Step 8: Verify Deployment

```bash
# Check pod status
oc get pods

# Should show: incident-analyzer-xxxxx   1/1   Running

# View logs
oc logs -f deployment/incident-analyzer
```

You should see:
```
🤖 Claude Incident Message Analyzer - Container Mode
✅ Bot initialized successfully
✅ Successfully joined and monitoring #your-channel
```

---

## Done!

The bot is now monitoring your Slack channel and will provide AI-powered analysis of incident communications.

---

## Common Commands

```bash
# View logs
oc logs -f deployment/incident-analyzer

# Restart the bot
oc rollout restart deployment/incident-analyzer

# Stop the bot
oc scale deployment incident-analyzer --replicas=0

# Start the bot
oc scale deployment incident-analyzer --replicas=1

# Check status
oc get pods
oc get deployment
```

---

## Troubleshooting

**Bot not joining channel?**
- Ensure bot is invited to the Slack channel
- Verify channel name matches exactly (no `#` prefix)
- Check bot has proper Slack permissions

**Build failing?**
- Check build logs: `oc logs -f bc/incident-analyzer`
- Verify internet access from cluster
- Try rebuilding: `oc start-build incident-analyzer`

**Pod crashing?**
- Check logs: `oc logs deployment/incident-analyzer`
- Verify secrets are correct: `oc get secret incident-analyzer-secrets`
- Ensure GCP project has Vertex AI enabled

---

## Need More Help?

📖 **Full Documentation**: See [DOCKER_OPENSHIFT_DEPLOYMENT.md](DOCKER_OPENSHIFT_DEPLOYMENT.md)
🐛 **Issues**: https://github.com/openshift-online/incident-message-analyzer/issues
📧 **Contact**: vkumar@redhat.com

---

## Architecture Overview

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Slack     │────▶│  OpenShift Pod   │────▶│  Vertex AI      │
│   Channel   │◀────│  (Python Bot)    │◀────│  (Claude AI)    │
└─────────────┘     └──────────────────┘     └─────────────────┘
                            │
                            ▼
                    ┌──────────────────┐
                    │  Analysis Results│
                    │  Posted to Slack │
                    └──────────────────┘
```

---

## What This Tool Does

✅ Monitors Slack incident channels in real-time
✅ Categorizes messages (errors, investigations, resolutions)
✅ Generates AI-powered incident summaries
✅ Extracts action items automatically
✅ Posts analysis back to Slack channel
✅ Includes AI disclaimer on all outputs

---

## Important Notes

⚠️ **AI Disclaimer**: All AI-generated content requires human review before use
🔒 **Security**: Never commit secrets to Git - use `oc create secret` instead
📊 **Single Instance**: Only run 1 replica (bot maintains stateful buffers)
🔑 **Permissions**: Ensure Slack bot has proper channel access

---

**Version**: 2.0
**Last Updated**: December 2024

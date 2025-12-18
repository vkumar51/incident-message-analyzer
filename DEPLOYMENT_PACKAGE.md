# Deployment Package for Other Teams

This document describes what you need to provide to other teams to deploy the Claude Incident Analyzer on their OpenShift clusters.

## What to Provide

### 1. Container Image Access

**Recommended: Push to Container Registry**

```bash
# Push to Quay.io (Red Hat's registry)
docker tag incident-message-analyzer:latest quay.io/YOUR_ORG/incident-message-analyzer:v1.0
docker push quay.io/YOUR_ORG/incident-message-analyzer:v1.0
```

Then share the image URL: `quay.io/YOUR_ORG/incident-message-analyzer:v1.0`

**Alternative: Private Registry**
If using Red Hat's internal registry, provide the full image path.

### 2. Deployment Files

Provide these files from the repository:

```
incident-message-analyzer/
├── k8s-deployment.yaml           # Main deployment manifest
├── openshift/
│   └── configmap.yaml            # Configuration (region, thresholds)
├── KUBERNETES_DEPLOYMENT.md      # Complete deployment guide
├── QUICK_DEPLOY.md               # Quick reference
└── DEPLOYMENT_PACKAGE.md         # This file
```

**Note:** Update the image reference in `k8s-deployment.yaml` to point to your registry:

```yaml
spec:
  containers:
  - name: slack-bot
    image: quay.io/YOUR_ORG/incident-message-analyzer:v1.0  # Update this!
    imagePullPolicy: Always  # Change from "Never" to "Always"
```

### 3. Prerequisites Document

Share this checklist with the deploying team:

---

## Prerequisites for Deployment Team

### Required Before Deployment:

1. **Google Cloud Authentication** ✅
   ```bash
   # Run on your local machine:
   gcloud auth application-default login
   gcloud auth application-default set-quota-project cloudability-it-gemini
   ```

   This creates: `~/.config/gcloud/application_default_credentials.json`

2. **GCP Project Access** ✅
   - Ensure you have access to: `itpc-gcp-hcm-pe-eng-claude`
   - Or use your own GCP project (update ANTHROPIC_VERTEX_PROJECT_ID)
   - Vertex AI must be enabled in the project
   - Claude models must be available in the region

3. **Slack Bot Setup** ✅
   - Create a Slack App at: https://api.slack.com/apps
   - Required Bot Token Scopes:
     - `channels:read`
     - `channels:join`
     - `chat:write`
     - `users:read`
     - `channels:history`
     - `groups:read`
     - `groups:history`
   - Install app to workspace
   - Get Bot User OAuth Token (starts with `xoxb-`)

4. **OpenShift/Kubernetes Access** ✅
   - CLI access (`oc` or `kubectl`)
   - Permissions to create:
     - Namespaces
     - Secrets
     - ConfigMaps
     - Deployments

---

## Deployment Steps for Receiving Team

### Step 1: Create Namespace

```bash
oc new-project incident-analyzer
# or
kubectl create namespace incident-analyzer
```

### Step 2: Create GCP Credentials Secret

**CRITICAL:** This secret provides authentication to Google Cloud Vertex AI.

```bash
kubectl create secret generic gcp-credentials \
  --from-file=key.json=/Users/YOUR_USERNAME/.config/gcloud/application_default_credentials.json \
  -n incident-analyzer
```

**Important Notes:**
- Use the FULL path to your credentials file
- On Mac: `/Users/YOUR_USERNAME/.config/gcloud/application_default_credentials.json`
- On Linux: `/home/YOUR_USERNAME/.config/gcloud/application_default_credentials.json`
- This file is created by running `gcloud auth application-default login`

### Step 3: Create Slack & Vertex AI Secrets

```bash
kubectl create secret generic incident-analyzer-secrets \
  --from-literal=SLACK_BOT_TOKEN='YOUR_SLACK_BOT_TOKEN_HERE' \
  --from-literal=ANTHROPIC_VERTEX_PROJECT_ID='itpc-gcp-hcm-pe-eng-claude' \
  -n incident-analyzer
```

Replace:
- `YOUR_SLACK_BOT_TOKEN_HERE` with your actual Slack bot OAuth token (starts with `xoxb-`)

### Step 4: Apply Configuration

```bash
# Apply ConfigMap
kubectl apply -f openshift/configmap.yaml

# Apply Deployment
kubectl apply -f k8s-deployment.yaml
```

### Step 5: Verify Deployment

```bash
# Check pod status
kubectl get pods -n incident-analyzer

# Check logs
kubectl logs -n incident-analyzer deployment/incident-analyzer --tail=50
```

**Expected output:**
```
✅ Bot connected as: claude_incident_analy (ID: ...)
✅ Bot initialized successfully
✅ Bot is monitoring X channel(s)
🚀 Bot is now active and listening...
```

### Step 6: Invite Bot to Slack Channels

In any Slack channel where you want incident analysis:

```
/invite @claude_incident_analy
```

The bot will automatically start monitoring that channel.

---

## Configuration Parameters

### Environment Variables

| Variable | Value | Description | Required |
|----------|-------|-------------|----------|
| `ANTHROPIC_VERTEX_PROJECT_ID` | `itpc-gcp-hcm-pe-eng-claude` | GCP project for Vertex AI | Yes |
| `ANTHROPIC_VERTEX_REGION` | `us-east5` | **MUST be us-east5** | Yes |
| `SLACK_BOT_TOKEN` | `xoxb-...` | Your Slack bot OAuth token | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | `/var/secrets/google/key.json` | Path to mounted credentials | Yes |
| `ANALYSIS_INTERVAL` | `1800` (30 minutes) | Time between analyses | No |
| `MESSAGE_THRESHOLD` | `10` | Messages to trigger analysis | No |

### Critical Configuration Notes

⚠️ **Region MUST be us-east5**
- Claude models via Vertex AI are only available in `us-east5`
- Using any other region (like `us-central1`) will cause API failures

⚠️ **GCP Credentials are Required**
- The bot cannot function without valid Google Cloud credentials
- Credentials must have access to the Vertex AI project

⚠️ **Message Threshold**
- Default is 10 messages
- Lower values = more frequent analysis
- Adjust based on your channel activity

---

## Troubleshooting Guide

### Issue: "DefaultCredentialsError: Your default credentials were not found"

**Solution:**
1. Verify you ran `gcloud auth application-default login`
2. Check the secret exists:
   ```bash
   kubectl get secret gcp-credentials -n incident-analyzer
   ```
3. Verify the file path in the secret creation command

### Issue: "model is not servable in region us-central1"

**Solution:**
Update `openshift/configmap.yaml`:
```yaml
ANTHROPIC_VERTEX_REGION: "us-east5"  # MUST be us-east5
```

Then restart:
```bash
kubectl rollout restart deployment/incident-analyzer -n incident-analyzer
```

### Issue: Empty AI Summaries ("No significant incident activity detected")

**Possible Causes:**
1. Wrong region (not us-east5)
2. GCP credentials not mounted correctly
3. No access to Vertex AI project

**Debug:**
```bash
# Check environment variables
kubectl exec -n incident-analyzer deployment/incident-analyzer -- env | grep ANTHROPIC

# Test Claude API access
kubectl exec -n incident-analyzer deployment/incident-analyzer -- python3 -c "
from anthropic import AnthropicVertex
import os
client = AnthropicVertex(
    project_id=os.getenv('ANTHROPIC_VERTEX_PROJECT_ID'),
    region=os.getenv('ANTHROPIC_VERTEX_REGION')
)
response = client.messages.create(
    model='claude-3-5-haiku@20241022',
    max_tokens=20,
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print('SUCCESS:', response.content[0].text)
"
```

### Issue: Bot Not Detecting Messages

**Solution:**
1. Ensure bot is invited to the channel: `/invite @claude_incident_analy`
2. Check bot has proper Slack permissions
3. Verify bot is running:
   ```bash
   kubectl logs -n incident-analyzer deployment/incident-analyzer -f
   ```

---

## Security Considerations

### Secrets Management

⚠️ **Never commit these to version control:**
- Slack bot tokens
- GCP credentials files
- Any `*secrets*.yaml` files with actual values

✅ **Best Practices:**
1. Use Kubernetes secrets (not plain environment variables)
2. Rotate credentials periodically
3. Use RBAC to restrict secret access
4. Consider using external secret management (Vault, GCP Secret Manager)

### Network Security

For production deployments:
- Configure network policies
- Use private container registries
- Enable pod security policies
- Implement egress filtering

---

## Support & Contacts

- **Developer**: Vikas Kumar (vkumar@redhat.com)
- **Feedback Form**: https://docs.google.com/forms/d/e/1FAIpQLScs50MAteC0TZ2YefvXJHtKw1PZUeqSRy3PDpuiGXk6FIMnqw/viewform
- **Documentation**: See KUBERNETES_DEPLOYMENT.md for detailed guide

---

## Checklist for Deployment Handoff

Before handing off to another team, ensure:

- [ ] Container image pushed to accessible registry
- [ ] Image URL updated in k8s-deployment.yaml
- [ ] All deployment files included
- [ ] Documentation provided (this file + KUBERNETES_DEPLOYMENT.md)
- [ ] Prerequisites clearly communicated
- [ ] Example secrets templates provided (without actual values)
- [ ] Troubleshooting guide shared
- [ ] Support contact information included

---

## Version Information

- **Current Version**: 2.0
- **Last Updated**: 2025-12-18
- **Claude Model**: claude-3-5-haiku@20241022
- **Required Region**: us-east5
- **Deployment Type**: Invite-Only Mode

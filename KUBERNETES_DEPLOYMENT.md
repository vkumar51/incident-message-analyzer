# Kubernetes/OpenShift Deployment Guide

Complete guide for deploying the Claude Incident Analyzer to Kubernetes or OpenShift clusters.

## Prerequisites

1. **Google Cloud Credentials**: You need Application Default Credentials for Vertex AI
2. **Slack Bot Token**: OAuth token starting with `xoxb-`
3. **GCP Project Access**: Access to `itpc-gcp-hcm-pe-eng-claude` project
4. **kubectl/oc CLI**: Command-line access to your Kubernetes/OpenShift cluster

## Step 1: Authenticate with Google Cloud

Run these commands on your local machine (one-time setup):

```bash
# Authenticate with Google Cloud
gcloud auth application-default login

# Set the quota project
gcloud auth application-default set-quota-project cloudability-it-gemini
```

This creates the credentials file at: `~/.config/gcloud/application_default_credentials.json`

## Step 2: Create Kubernetes Namespace

```bash
kubectl create namespace incident-analyzer
```

Or for OpenShift:
```bash
oc new-project incident-analyzer
```

## Step 3: Create GCP Credentials Secret

**CRITICAL:** This secret contains your Google Cloud credentials for Vertex AI authentication.

```bash
# Create secret from your local credentials file
kubectl create secret generic gcp-credentials \
  --from-file=key.json=~/.config/gcloud/application_default_credentials.json \
  -n incident-analyzer
```

Verify the secret was created:
```bash
kubectl get secret gcp-credentials -n incident-analyzer
```

## Step 4: Create Slack & Vertex AI Secrets

```bash
kubectl create secret generic incident-analyzer-secrets \
  --from-literal=SLACK_BOT_TOKEN='your-slack-bot-token' \
  --from-literal=ANTHROPIC_VERTEX_PROJECT_ID='itpc-gcp-hcm-pe-eng-claude' \
  -n incident-analyzer
```

Replace `your-slack-bot-token` with your actual Slack bot OAuth token (starts with `xoxb-`).

## Step 5: Apply Configuration

```bash
# Apply the configuration
kubectl apply -f openshift/configmap.yaml

# Apply the deployment
kubectl apply -f k8s-deployment.yaml
```

## Step 6: Verify Deployment

Check that the pod is running:

```bash
kubectl get pods -n incident-analyzer
```

Check the logs to verify successful startup:

```bash
kubectl logs -n incident-analyzer deployment/incident-analyzer --tail=50
```

You should see:
```
✅ Bot connected as: claude_incident_analy (ID: U09D8HWM7BQ)
✅ Bot initialized successfully
✅ Bot is monitoring X channel(s)
🚀 Bot is now active and listening...
```

## Step 7: Invite Bot to Slack Channels

In any Slack channel where you want incident analysis:

```
/invite @claude_incident_analy
```

The bot will automatically start monitoring that channel.

## Configuration Details

### Environment Variables

The deployment uses these environment variables:

| Variable | Source | Value | Description |
|----------|--------|-------|-------------|
| `SLACK_BOT_TOKEN` | Secret | Your bot token | Slack API authentication |
| `ANTHROPIC_VERTEX_PROJECT_ID` | Secret | `itpc-gcp-hcm-pe-eng-claude` | GCP project for Vertex AI |
| `ANTHROPIC_VERTEX_REGION` | ConfigMap | `us-east5` | **MUST be us-east5** for Claude |
| `GOOGLE_APPLICATION_CREDENTIALS` | Pod env | `/var/secrets/google/key.json` | Path to mounted credentials |
| `ANALYSIS_INTERVAL` | ConfigMap | `1800` (30 min) | Time between analyses |
| `MESSAGE_THRESHOLD` | ConfigMap | `10` | Messages to trigger analysis |

### Important Notes

⚠️ **Region MUST be us-east5**: Claude models are only available in the `us-east5` region via Vertex AI.

⚠️ **Credentials Secret Required**: The `gcp-credentials` secret must exist and contain valid Google Cloud Application Default Credentials.

⚠️ **Invite-Only Mode**: The bot only monitors channels it's explicitly invited to. No pre-configuration needed.

## Troubleshooting

### Authentication Errors

If you see:
```
DefaultCredentialsError: Your default credentials were not found
```

**Solution**: Verify the `gcp-credentials` secret exists:
```bash
kubectl get secret gcp-credentials -n incident-analyzer -o yaml
```

### Region Errors

If you see:
```
model is not servable in region us-central1
```

**Solution**: Update the region to `us-east5` in `openshift/configmap.yaml`:
```yaml
ANTHROPIC_VERTEX_REGION: "us-east5"
```

Then restart the deployment:
```bash
kubectl rollout restart deployment/incident-analyzer -n incident-analyzer
```

### Empty AI Summaries

If summaries show "No significant incident activity detected" for clearly significant messages:

**Check:**
1. Region is set to `us-east5`
2. GCP credentials secret is mounted correctly
3. Logs for any API errors

**Verify API access:**
```bash
kubectl exec -n incident-analyzer deployment/incident-analyzer -- \
  gcloud auth application-default print-access-token
```

## Updating the Deployment

### Update Code

1. Build new Docker image
2. Push to container registry
3. Update image in deployment
4. Apply changes:

```bash
kubectl set image deployment/incident-analyzer \
  slack-bot=your-registry/incident-message-analyzer:new-tag \
  -n incident-analyzer
```

### Update Configuration

```bash
# Edit configmap
kubectl edit configmap incident-analyzer-config -n incident-analyzer

# Restart deployment to pick up changes
kubectl rollout restart deployment/incident-analyzer -n incident-analyzer
```

### Rotate Credentials

If you need to update GCP credentials:

```bash
# Delete old secret
kubectl delete secret gcp-credentials -n incident-analyzer

# Create new secret
kubectl create secret generic gcp-credentials \
  --from-file=key.json=~/.config/gcloud/application_default_credentials.json \
  -n incident-analyzer

# Restart deployment
kubectl rollout restart deployment/incident-analyzer -n incident-analyzer
```

## Monitoring

### View Logs

```bash
# Follow logs in real-time
kubectl logs -n incident-analyzer deployment/incident-analyzer -f

# View last 100 lines
kubectl logs -n incident-analyzer deployment/incident-analyzer --tail=100
```

### Check Resource Usage

```bash
kubectl top pod -n incident-analyzer
```

### View Analysis Results

Analysis results are saved inside the pod at `/app/analysis_*.json`:

```bash
kubectl exec -n incident-analyzer deployment/incident-analyzer -- \
  ls -la /app/analysis_*.json
```

## Production Considerations

For production deployments, consult with the GCP team for:

1. **Service Account Authentication**: Use Workload Identity instead of mounted credentials
2. **Secret Management**: Use external secret management (e.g., Vault, GCP Secret Manager)
3. **High Availability**: Configure replica count > 1 with proper anti-affinity
4. **Resource Limits**: Adjust based on actual usage patterns
5. **Monitoring**: Set up Prometheus metrics and alerting
6. **Backup**: Regular backups of analysis results

## Security Notes

⚠️ **Credentials Protection**:
- The `gcp-credentials` secret contains sensitive authentication information
- Ensure proper RBAC policies restrict secret access
- Rotate credentials periodically
- Never commit credentials to version control

⚠️ **Slack Token Protection**:
- Slack bot tokens provide full bot access
- Treat them as highly sensitive credentials
- Use Kubernetes secrets, not environment variables in deployment YAML
- Monitor for unauthorized token usage

## Support

For issues or questions:
- **Developer**: Vikas Kumar (vkumar@redhat.com)
- **Feedback Form**: https://docs.google.com/forms/d/e/1FAIpQLScs50MAteC0TZ2YefvXJHtKw1PZUeqSRy3PDpuiGXk6FIMnqw/viewform
- **GitHub**: Report issues in the repository

## Additional Resources

- [Claude SDK Documentation](https://docs.anthropic.com/en/api/claude-on-vertex-ai)
- [Google Cloud ADC Setup](https://cloud.google.com/docs/authentication/external/set-up-adc)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [OpenShift Documentation](https://docs.openshift.com/)

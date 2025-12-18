# Quick Deployment Reference

Fast reference for deploying to Kubernetes/OpenShift clusters.

## TL;DR - Deploy in 5 Commands

```bash
# 1. Create namespace
kubectl create namespace incident-analyzer

# 2. Create GCP credentials secret
kubectl create secret generic gcp-credentials \
  --from-file=key.json=~/.config/gcloud/application_default_credentials.json \
  -n incident-analyzer

# 3. Create Slack & Vertex AI secrets
kubectl create secret generic incident-analyzer-secrets \
  --from-literal=SLACK_BOT_TOKEN='xoxb-your-token-here' \
  --from-literal=ANTHROPIC_VERTEX_PROJECT_ID='itpc-gcp-hcm-pe-eng-claude' \
  -n incident-analyzer

# 4. Apply configuration and deployment
kubectl apply -f openshift/configmap.yaml
kubectl apply -f k8s-deployment.yaml

# 5. Verify deployment
kubectl get pods -n incident-analyzer
kubectl logs -n incident-analyzer deployment/incident-analyzer --tail=30
```

## Critical Configuration

✅ **Region MUST be us-east5** - Claude models only available in this region
✅ **GCP credentials required** - Mount from `~/.config/gcloud/application_default_credentials.json`
✅ **Message threshold: 10** - Triggers AI analysis after 10 messages
✅ **Invite-only mode** - Bot only monitors channels it's invited to

## Invite Bot to Channels

In any Slack channel:
```
/invite @claude_incident_analy
```

## View Logs

```bash
# Follow logs
kubectl logs -n incident-analyzer deployment/incident-analyzer -f

# Check last 50 lines
kubectl logs -n incident-analyzer deployment/incident-analyzer --tail=50
```

## Troubleshooting

**Empty AI summaries?**
→ Check region is `us-east5` in configmap.yaml

**Authentication errors?**
→ Verify `gcp-credentials` secret exists

**Bot not responding?**
→ Check logs for errors and verify bot is invited to channel

## Full Documentation

See [KUBERNETES_DEPLOYMENT.md](./KUBERNETES_DEPLOYMENT.md) for complete deployment guide.

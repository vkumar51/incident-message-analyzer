# Docker and OpenShift Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Building the Docker Image](#building-the-docker-image)
4. [Testing Locally with Docker](#testing-locally-with-docker)
5. [Setting up Local OpenShift Cluster](#setting-up-local-openshift-cluster)
6. [Deploying to OpenShift](#deploying-to-openshift)
7. [Deploying to Remote OpenShift Clusters](#deploying-to-remote-openshift-clusters)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This guide explains how to:
- Build a Docker image for the Claude Incident Message Analyzer
- Test the containerized application locally
- Deploy to a local OpenShift cluster (CodeReady Containers)
- Deploy to remote/managed OpenShift clusters

---

## Prerequisites

### Required Tools
- **Docker** (v20.10+) or **Podman** (v3.0+)
- **OpenShift CLI (oc)** (v4.10+)
- **Git**

### Required Credentials
- Slack Bot Token (`xoxb-...`)
- Google Cloud Project ID (with Vertex AI enabled)
- Slack channel name to monitor

### For Local Testing
- **CodeReady Containers (CRC)** - for local OpenShift cluster
  - Download: https://developers.redhat.com/products/codeready-containers/overview
  - Minimum requirements: 9GB RAM, 4 CPU cores, 35GB disk space

---

## Building the Docker Image

### 1. Clone the Repository

```bash
git clone https://github.com/openshift-online/incident-message-analyzer.git
cd incident-message-analyzer
```

### 2. Build the Docker Image

Using Docker:
```bash
docker build -t incident-message-analyzer:latest .
```

Using Podman:
```bash
podman build -t incident-message-analyzer:latest .
```

### 3. Verify the Image

```bash
# Using Docker
docker images | grep incident-message-analyzer

# Using Podman
podman images | grep incident-message-analyzer
```

You should see output like:
```
incident-message-analyzer   latest   abc123def456   2 minutes ago   450MB
```

---

## Testing Locally with Docker

### 1. Create Environment Variables File

Create a file named `.env.local`:

```bash
cat > .env.local <<EOF
SLACK_BOT_TOKEN=xoxb-your-actual-slack-bot-token
ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
ANTHROPIC_VERTEX_REGION=us-central1
SLACK_CHANNEL_NAME=incident-alerts
EOF
```

**IMPORTANT**: Add `.env.local` to `.gitignore` to avoid committing secrets!

### 2. Run the Container Locally

Using Docker:
```bash
docker run --rm -it \
  --env-file .env.local \
  --name incident-analyzer \
  incident-message-analyzer:latest
```

Using Podman:
```bash
podman run --rm -it \
  --env-file .env.local \
  --name incident-analyzer \
  incident-message-analyzer:latest
```

### 3. Verify It's Working

You should see output like:
```
============================================================
🤖 Claude Incident Message Analyzer - Container Mode
============================================================
📊 GCP Project: your-gcp-project-id
🌍 GCP Region: us-central1
📢 Monitoring Channel: #incident-alerts
============================================================

🔄 Initializing Slack bot...
✅ Bot initialized successfully (User ID: U12345678)

🔍 Adding channel '#incident-alerts' to monitoring list...
✅ Successfully joined and monitoring #incident-alerts
```

### 4. Stop the Container

Press `Ctrl+C` to stop the container gracefully.

---

## Setting up Local OpenShift Cluster

### 1. Install CodeReady Containers (CRC)

```bash
# Download from https://developers.redhat.com/products/codeready-containers/download
# Extract and move to PATH
tar xvf crc-linux-amd64.tar.xz
sudo mv crc-linux-*/crc /usr/local/bin/

# Setup CRC
crc setup

# Start CRC (this takes 5-10 minutes)
crc start
```

### 2. Login to OpenShift

```bash
# Get login credentials
crc console --credentials

# Login via CLI (use credentials from above)
oc login -u developer https://api.crc.testing:6443
```

### 3. Verify Cluster Access

```bash
oc whoami
oc cluster-info
```

---

## Deploying to OpenShift

### Option A: Build Image in OpenShift (Recommended)

This builds the image directly in OpenShift from your GitHub repository.

#### 1. Create the Namespace

```bash
oc apply -f openshift/namespace.yaml
```

#### 2. Switch to the Namespace

```bash
oc project incident-analyzer
```

#### 3. Create Secrets (with your actual credentials)

```bash
oc create secret generic incident-analyzer-secrets \
  --from-literal=SLACK_BOT_TOKEN='xoxb-your-actual-token' \
  --from-literal=ANTHROPIC_VERTEX_PROJECT_ID='your-gcp-project-id' \
  -n incident-analyzer
```

**IMPORTANT**: Replace the placeholder values with your actual credentials!

#### 4. Create ConfigMap

```bash
oc apply -f openshift/configmap.yaml
```

Edit the channel name if needed:
```bash
oc edit configmap incident-analyzer-config
```

#### 5. Create BuildConfig and ImageStream

```bash
oc apply -f openshift/buildconfig.yaml
```

#### 6. Start the Build

```bash
# Trigger the build
oc start-build incident-analyzer -n incident-analyzer

# Watch the build progress
oc logs -f bc/incident-analyzer
```

Wait for the build to complete (this takes 3-5 minutes).

#### 7. Deploy the Application

```bash
oc apply -f openshift/deployment-with-imagestream.yaml
```

#### 8. Verify Deployment

```bash
# Check deployment status
oc get deployment incident-analyzer

# Check pod status
oc get pods

# View logs
oc logs -f deployment/incident-analyzer
```

---

### Option B: Push Pre-built Image to Registry

If you've already built the image locally and want to push it to a registry.

#### 1. Tag the Image for Your Registry

```bash
# For Quay.io
docker tag incident-message-analyzer:latest quay.io/your-username/incident-message-analyzer:latest

# For Docker Hub
docker tag incident-message-analyzer:latest docker.io/your-username/incident-message-analyzer:latest
```

#### 2. Push the Image

```bash
# Login to registry
docker login quay.io
# or
docker login docker.io

# Push the image
docker push quay.io/your-username/incident-message-analyzer:latest
```

#### 3. Update deployment.yaml

Edit `openshift/deployment.yaml` and change the image line:
```yaml
image: quay.io/your-username/incident-message-analyzer:latest
```

#### 4. Deploy to OpenShift

```bash
# Create namespace
oc apply -f openshift/namespace.yaml

# Switch to namespace
oc project incident-analyzer

# Create secrets
oc create secret generic incident-analyzer-secrets \
  --from-literal=SLACK_BOT_TOKEN='xoxb-your-token' \
  --from-literal=ANTHROPIC_VERTEX_PROJECT_ID='your-project-id'

# Create configmap
oc apply -f openshift/configmap.yaml

# Deploy application
oc apply -f openshift/deployment.yaml

# Check status
oc get pods
oc logs -f deployment/incident-analyzer
```

---

## Deploying to Remote OpenShift Clusters

### Sharing with Other Teams

To enable other teams to deploy to their OpenShift clusters:

#### 1. Share the Repository

Provide access to: `https://github.com/openshift-online/incident-message-analyzer`

#### 2. Share the Docker Image (Optional)

If you've pushed to a public registry:
```
quay.io/openshift-online/incident-message-analyzer:latest
```

#### 3. Provide Deployment Instructions

Share this documentation file (`DOCKER_OPENSHIFT_DEPLOYMENT.md`) with:
- The OpenShift manifests directory (`openshift/`)
- Instructions for setting their own secrets
- Channel configuration requirements

### Deployment Steps for Remote Teams

```bash
# 1. Login to their OpenShift cluster
oc login <their-cluster-url>

# 2. Clone the repository
git clone https://github.com/openshift-online/incident-message-analyzer.git
cd incident-message-analyzer

# 3. Create namespace
oc apply -f openshift/namespace.yaml
oc project incident-analyzer

# 4. Create their secrets
oc create secret generic incident-analyzer-secrets \
  --from-literal=SLACK_BOT_TOKEN='their-slack-token' \
  --from-literal=ANTHROPIC_VERTEX_PROJECT_ID='their-gcp-project'

# 5. Update ConfigMap with their channel
oc apply -f openshift/configmap.yaml
oc edit configmap incident-analyzer-config  # Change SLACK_CHANNEL_NAME

# 6. Build and deploy
oc apply -f openshift/buildconfig.yaml
oc start-build incident-analyzer
oc logs -f bc/incident-analyzer

# Wait for build to complete, then deploy
oc apply -f openshift/deployment-with-imagestream.yaml

# 7. Verify
oc get pods
oc logs -f deployment/incident-analyzer
```

---

## Troubleshooting

### Build Failures

**Problem**: Build fails with "error building image"

**Solution**:
```bash
# Check build logs
oc logs -f bc/incident-analyzer

# Delete and recreate BuildConfig
oc delete buildconfig incident-analyzer
oc apply -f openshift/buildconfig.yaml
oc start-build incident-analyzer
```

### Pod CrashLoopBackOff

**Problem**: Pod keeps restarting

**Solution**:
```bash
# Check pod logs
oc logs deployment/incident-analyzer

# Common issues:
# 1. Missing environment variables - verify secret exists
oc get secret incident-analyzer-secrets

# 2. Invalid Slack token
oc describe secret incident-analyzer-secrets

# 3. Channel not accessible - check bot permissions in Slack
```

### Image Pull Errors

**Problem**: "ImagePullBackOff" or "ErrImagePull"

**Solution**:
```bash
# Check if ImageStream exists
oc get imagestream

# Check if build completed successfully
oc get builds

# Verify image in registry
oc describe imagestream incident-analyzer
```

### Application Not Monitoring Channel

**Problem**: Bot runs but doesn't process messages

**Solution**:
1. Verify bot has been invited to the Slack channel
2. Check the channel name in ConfigMap matches exactly
3. Verify bot has correct Slack permissions (see `SLACK_SETUP.md`)
4. Check application logs for errors

```bash
oc logs -f deployment/incident-analyzer
```

### Resource Issues

**Problem**: Pod pending or evicted due to resources

**Solution**:
```bash
# Check node resources
oc describe nodes

# Reduce resource requests in deployment
oc edit deployment incident-analyzer

# Modify:
resources:
  requests:
    memory: "128Mi"
    cpu: "50m"
```

### Viewing Application Logs

```bash
# Follow logs in real-time
oc logs -f deployment/incident-analyzer

# View last 100 lines
oc logs --tail=100 deployment/incident-analyzer

# View logs from previous crashed container
oc logs deployment/incident-analyzer --previous
```

### Redeploying After Code Changes

```bash
# Rebuild the image
oc start-build incident-analyzer

# Wait for build, then rollout restart
oc rollout restart deployment/incident-analyzer

# Watch rollout status
oc rollout status deployment/incident-analyzer
```

### Scaling the Deployment

**Note**: Only run ONE replica since the bot maintains stateful message buffers.

```bash
# Scale to 1 (default)
oc scale deployment incident-analyzer --replicas=1

# To stop temporarily (scale to 0)
oc scale deployment incident-analyzer --replicas=0
```

---

## Advanced Configuration

### Monitoring Multiple Channels

To monitor multiple channels, deploy multiple instances:

```bash
# Create second deployment with different channel
oc create deployment incident-analyzer-prod \
  --image=image-registry.openshift-image-registry.svc:5000/incident-analyzer/incident-analyzer:latest

# Set different channel name
oc set env deployment/incident-analyzer-prod SLACK_CHANNEL_NAME=incident-prod
```

### Using Persistent Storage

To save analysis results persistently:

```yaml
# Add to deployment.yaml volumes section
volumes:
- name: data-volume
  persistentVolumeClaim:
    claimName: incident-analyzer-pvc
```

Create PVC:
```bash
cat <<EOF | oc apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: incident-analyzer-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF
```

---

## Security Best Practices

1. **Never commit secrets to Git**
   - Use `oc create secret` instead of YAML files
   - Add `.env.local` to `.gitignore`

2. **Use separate secrets per environment**
   - Development, staging, production should have different tokens

3. **Regularly rotate credentials**
   - Update secrets periodically
   - Use `oc delete secret` and recreate

4. **Limit permissions**
   - Use dedicated Slack bot tokens with minimal permissions
   - Use separate GCP service accounts per environment

5. **Monitor access**
   - Review OpenShift RBAC regularly
   - Check who has access to the namespace

---

## Next Steps

After successful deployment:

1. **Monitor the application**: `oc logs -f deployment/incident-analyzer`
2. **Test with sample incident**: Post messages to your Slack channel
3. **Review AI output**: Verify disclaimers appear in summaries
4. **Provide feedback**: Use the Google Forms feedback mechanism
5. **Document any issues**: Open issues at https://github.com/openshift-online/incident-message-analyzer

---

## Support

- **Technical Issues**: Create GitHub issue
- **Slack Bot Questions**: vkumar@redhat.com
- **OpenShift Deployment**: Contact your cluster administrator

---

**Document Version**: 1.0
**Last Updated**: December 2024
**Maintained By**: Vikas Kumar (vkumar@redhat.com)

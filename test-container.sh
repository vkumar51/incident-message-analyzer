#!/bin/bash
# Test script for running the incident analyzer container locally

set -e

echo "=========================================="
echo "Claude Incident Analyzer - Local Test"
echo "=========================================="
echo ""

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "⚠️  .env.local file not found!"
    echo ""
    echo "Creating template .env.local file..."
    cat > .env.local <<EOF
# Replace these with your actual credentials
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token-here
ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id-here
ANTHROPIC_VERTEX_REGION=us-central1
SLACK_CHANNEL_NAME=your-channel-name-here
EOF
    echo "✅ Created .env.local template"
    echo ""
    echo "Please edit .env.local and add your actual credentials, then run this script again."
    exit 1
fi

# Check if image exists
IMAGE_NAME="incident-message-analyzer:latest"

# Detect container CLI
if command -v docker &> /dev/null; then
    CONTAINER_CLI="docker"
elif command -v podman &> /dev/null; then
    CONTAINER_CLI="podman"
else
    echo "❌ ERROR: Neither Docker nor Podman found!"
    exit 1
fi

echo "Using: ${CONTAINER_CLI}"
echo ""

# Check if image exists
if ! ${CONTAINER_CLI} image inspect ${IMAGE_NAME} &> /dev/null; then
    echo "⚠️  Image not found: ${IMAGE_NAME}"
    echo ""
    echo "Building image first..."
    ./build.sh
    echo ""
fi

echo "🚀 Starting container..."
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the container
${CONTAINER_CLI} run --rm -it \
    --name incident-analyzer-test \
    --env-file .env.local \
    ${IMAGE_NAME}

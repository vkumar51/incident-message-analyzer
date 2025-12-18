#!/bin/bash
# Build script for Claude Incident Message Analyzer Docker image

set -e

IMAGE_NAME="incident-message-analyzer"
IMAGE_TAG="${1:-latest}"
FULL_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"

echo "=========================================="
echo "Building Docker Image"
echo "=========================================="
echo "Image: ${FULL_IMAGE}"
echo ""

# Detect if Docker or Podman is available
if command -v docker &> /dev/null; then
    CONTAINER_CLI="docker"
elif command -v podman &> /dev/null; then
    CONTAINER_CLI="podman"
else
    echo "❌ ERROR: Neither Docker nor Podman found!"
    echo "Please install Docker or Podman to build images."
    exit 1
fi

echo "Using: ${CONTAINER_CLI}"
echo ""

# Build the image
echo "🔨 Building image..."
${CONTAINER_CLI} build -t "${FULL_IMAGE}" .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "Image: ${FULL_IMAGE}"
    echo ""
    echo "To test locally:"
    echo "  ${CONTAINER_CLI} run --rm -it \\"
    echo "    -e SLACK_BOT_TOKEN='xoxb-your-token' \\"
    echo "    -e ANTHROPIC_VERTEX_PROJECT_ID='your-project-id' \\"
    echo "    -e SLACK_CHANNEL_NAME='your-channel' \\"
    echo "    ${FULL_IMAGE}"
    echo ""
else
    echo "❌ Build failed!"
    exit 1
fi

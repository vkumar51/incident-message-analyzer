# Use official Python runtime as base image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="vkumar@redhat.com"
LABEL description="Claude Incident Message Analyzer - AI-powered Slack bot for incident analysis"
LABEL version="2.0"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./
COPY *.md ./

# Create directory for analysis output
RUN mkdir -p /app/data

# OpenShift compatibility: Set permissions for arbitrary user IDs
# OpenShift runs containers with random UIDs, but always in group 0 (root group)
RUN chgrp -R 0 /app && \
    chmod -R g=u /app && \
    chmod -R g+w /app/data

# Switch to non-root user (OpenShift will override this with random UID)
USER 1001

# Set the entrypoint (use invite-only mode - no channel config needed)
ENTRYPOINT ["python3", "slack_bot_invite_only.py"]

# Health check (optional - checks if Python process is running)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep python3 || exit 1

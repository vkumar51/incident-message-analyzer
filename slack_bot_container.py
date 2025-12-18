#!/usr/bin/env python3
"""
Containerized Slack Bot for Incident Message Analysis
Non-interactive version for Docker/OpenShift deployment
"""

import os
import sys
from slack_bot import IncidentSlackBot

def main():
    """Main entry point for containerized deployment"""

    # Get required environment variables
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    anthropic_project = os.getenv('ANTHROPIC_VERTEX_PROJECT_ID')
    anthropic_region = os.getenv('ANTHROPIC_VERTEX_REGION', 'us-central1')

    # Get channel name from environment variable
    channel_name = os.getenv('SLACK_CHANNEL_NAME')

    # Validate required environment variables
    if not bot_token:
        print("❌ ERROR: SLACK_BOT_TOKEN environment variable is required")
        sys.exit(1)

    if not anthropic_project:
        print("❌ ERROR: ANTHROPIC_VERTEX_PROJECT_ID environment variable is required")
        sys.exit(1)

    if not channel_name:
        print("❌ ERROR: SLACK_CHANNEL_NAME environment variable is required")
        print("   Set it to the channel you want to monitor (e.g., 'incident-alerts')")
        sys.exit(1)

    # Log startup information
    print("=" * 60)
    print("🤖 Claude Incident Message Analyzer - Container Mode")
    print("=" * 60)
    print(f"📊 GCP Project: {anthropic_project}")
    print(f"🌍 GCP Region: {anthropic_region}")
    print(f"📢 Monitoring Channel: #{channel_name}")
    print("=" * 60)

    try:
        # Initialize the bot
        print("\n🔄 Initializing Slack bot...")
        bot = IncidentSlackBot(bot_token=bot_token)

        print(f"✅ Bot initialized successfully (User ID: {bot.bot_user_id})")

        # Add the channel to monitor
        print(f"\n🔍 Adding channel '#{channel_name}' to monitoring list...")
        success = bot.add_channel_to_monitor(channel_name)

        if success:
            print(f"✅ Successfully joined and monitoring #{channel_name}")
            print(f"\n🎯 Bot will analyze messages every {bot.analysis_interval/60} minutes or after {bot.message_threshold} messages")
            print("💬 Waiting for incident messages...\n")

            # Display disclaimer
            print("⚠️  AI DISCLAIMER:")
            print("   All analysis results require human review before use.")
            print("   This tool uses Claude 3.5 Haiku for AI-powered analysis.")
            print()

            # Start monitoring (this runs indefinitely)
            print("🚀 Starting message monitoring...")
            print("   Press Ctrl+C to stop\n")
            bot.start_monitoring()

        else:
            print(f"❌ Failed to join channel '#{channel_name}'")
            print("   Please check:")
            print("   1. Channel name is correct")
            print("   2. Bot has been invited to the channel")
            print("   3. Bot has necessary permissions")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Received shutdown signal")
        print("👋 Stopping bot gracefully...")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

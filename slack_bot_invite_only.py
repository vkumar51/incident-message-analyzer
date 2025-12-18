#!/usr/bin/env python3
"""
Containerized Slack Bot for Incident Message Analysis
INVITE-ONLY MODE: Bot is available but only monitors channels it's invited to
No channel configuration required - just invite the bot when you need it!
"""

import os
import sys
import time
from datetime import datetime
from slack_bot import IncidentSlackBot

def discover_invited_channels(bot):
    """
    Discover channels where the bot has been invited (is a member)

    Args:
        bot: IncidentSlackBot instance

    Returns:
        Number of channels being monitored
    """
    try:
        # Get all channels where bot is a member
        response = bot.client.conversations_list(
            types="public_channel,private_channel",
            exclude_archived=True,
            limit=1000
        )

        invited_channels = []

        for channel in response.get('channels', []):
            # Only monitor channels where bot is explicitly a member (invited)
            if channel.get('is_member', False):
                channel_name = channel['name']
                channel_id = channel['id']
                invited_channels.append((channel_id, channel_name))

        # Add invited channels to monitoring
        for channel_id, channel_name in invited_channels:
            if channel_id not in bot.monitored_channels:
                bot.monitored_channels.add(channel_id)
                bot.message_buffer[channel_id] = []
                bot.processed_messages[channel_id] = set()
                bot.last_analysis[channel_id] = datetime.now()
                print(f"   ✅ Now monitoring #{channel_name} (ID: {channel_id})")

        return len(invited_channels)

    except Exception as e:
        print(f"⚠️  Error discovering channels: {e}")
        return 0


def main():
    """Main entry point for invite-only containerized deployment"""

    # Get required environment variables
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    anthropic_project = os.getenv('ANTHROPIC_VERTEX_PROJECT_ID')
    anthropic_region = os.getenv('ANTHROPIC_VERTEX_REGION', 'us-central1')

    # SLACK_CHANNEL_NAME is now completely optional (ignored)

    # Validate required environment variables
    if not bot_token:
        print("❌ ERROR: SLACK_BOT_TOKEN environment variable is required")
        sys.exit(1)

    if not anthropic_project:
        print("❌ ERROR: ANTHROPIC_VERTEX_PROJECT_ID environment variable is required")
        sys.exit(1)

    # Log startup information
    print("=" * 70)
    print("🤖 Claude Incident Message Analyzer - Invite-Only Mode")
    print("=" * 70)
    print(f"📊 GCP Project: {anthropic_project}")
    print(f"🌍 GCP Region: {anthropic_region}")
    print(f"🎯 Mode: Monitors only channels where bot is invited")
    print("=" * 70)

    try:
        # Initialize the bot
        print("\n🔄 Initializing Slack bot...")
        bot = IncidentSlackBot(bot_token=bot_token)

        print(f"✅ Bot initialized successfully (User ID: {bot.bot_user_id})")

        # Discover channels where bot has been invited
        print("\n🔍 Checking for channel invitations...")
        channel_count = discover_invited_channels(bot)

        if channel_count == 0:
            print("\n📢 Bot is ready but not invited to any channels yet")
            print("\n💡 To use this bot:")
            print("   1. Go to any Slack channel you want to monitor")
            print("   2. Type: /invite @claude_incident_analy")
            print("   3. The bot will automatically start monitoring that channel")
            print("\n⏳ Bot is running and waiting for invitations...")
            print("   (You can invite the bot at any time without restarting)")
        else:
            print(f"\n✅ Bot is monitoring {channel_count} channel(s)")
            print(f"\n🎯 Analysis triggers:")
            print(f"   • After {bot.message_threshold} messages in a channel")
            print(f"   • Every {bot.analysis_interval/60} minutes")
            print("\n💡 To monitor additional channels:")
            print("   Type in any channel: /invite @claude_incident_analy")

        # Display disclaimer
        print("\n" + "=" * 70)
        print("⚠️  AI DISCLAIMER:")
        print("   All analysis results require human review before use.")
        print("   This tool uses Claude 3.5 Haiku for AI-powered analysis.")
        print("=" * 70)

        # Start monitoring (this runs indefinitely)
        print("\n🚀 Bot is now active and listening...")
        print("   Press Ctrl+C to stop\n")

        # Periodic channel discovery (checks for new invitations every 5 minutes)
        print("🔄 Checking for new channel invitations every 5 minutes...\n")

        # Start the main monitoring loop
        bot.start_monitoring()

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

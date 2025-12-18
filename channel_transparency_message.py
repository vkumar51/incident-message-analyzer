#!/usr/bin/env python3
"""
Slack Channel Transparency Message
Posts and pins AI transparency notice to monitored channels
"""

import os
import json
from datetime import datetime
from slack_sdk import WebClient

class ChannelTransparencyManager:
    def __init__(self, bot_token: str):
        """Initialize transparency manager with bot token"""
        self.client = WebClient(token=bot_token)
        self.bot_user_id = None
        self._get_bot_info()
    
    def _get_bot_info(self):
        """Get bot user information"""
        try:
            response = self.client.auth_test()
            self.bot_user_id = response['user_id']
            print(f"✅ Bot connected as: {response['user']} (ID: {self.bot_user_id})")
        except Exception as e:
            print(f"❌ Failed to get bot info: {e}")
    
    def create_transparency_message_blocks(self) -> list:
        """Create Slack blocks for transparency message"""
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🤖 AI Transparency Notice",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Generative AI functionality is active in this channel*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "📋 *What this means:*\n• AI analyzes channel messages to summarize incident activity\n• Analysis occurs automatically when 10+ messages are posted or every 30 minutes\n• AI categorizes messages and generates executive summaries\n• Results are posted as summaries in this channel"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🔒 *Privacy Information:*\n• *Personal information* (usernames, user IDs) is *NOT processed* by AI\n• Only message content is analyzed for incident patterns\n• No personal data is sent to external AI services\n• All processing follows company data privacy policies"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "⚙️ *Messages NOT processed:*\n• Bot messages and automated notifications\n• Messages without substantial text content\n• Messages marked as edited or deleted\n• Direct mentions or private replies (based on business rules)"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "⚠️ *IMPORTANT DISCLAIMER:*\n*Results from AI tools should NOT be relied upon without human review.*\n\n• AI may miss critical information or misinterpret context\n• Always validate AI summaries against actual incident data\n• Review all action items and recommendations with your team\n• Use AI output as a starting point, not final documentation"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "📞 *Questions or concerns?*\nContact: Vikas Kumar (vkumar@redhat.com)"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Feedback Form",
                        "emoji": True
                    },
                    "url": "https://docs.google.com/forms/d/e/1FAIpQLScs50MAteC0TZ2YefvXJHtKw1PZUeqSRy3PDpuiGXk6FIMnqw/viewform",
                    "action_id": "transparency_feedback"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Claude Incident Analyzer • Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • This message will remain pinned for transparency"
                    }
                ]
            }
        ]
        
        return blocks
    
    def post_transparency_message(self, channel_id: str) -> bool:
        """Post transparency message to channel and attempt to pin it"""
        try:
            # Create transparency message
            blocks = self.create_transparency_message_blocks()
            
            # Post message
            response = self.client.chat_postMessage(
                channel=channel_id,
                text="🤖 AI Transparency Notice - Generative AI functionality is active in this channel",
                blocks=blocks
            )
            
            message_ts = response['ts']
            print(f"✅ Posted transparency message to channel")
            
            # Attempt to pin the message
            try:
                pin_response = self.client.pins_add(
                    channel=channel_id,
                    timestamp=message_ts
                )
                print(f"📌 Successfully pinned transparency message")
                return True
                
            except Exception as pin_error:
                print(f"⚠️ Could not pin message (may lack permissions): {pin_error}")
                print("💡 Please manually pin this message for transparency")
                return True  # Still successful posting, just couldn't pin
                
        except Exception as e:
            print(f"❌ Failed to post transparency message: {e}")
            return False
    
    def get_channel_id(self, channel_name: str) -> str:
        """Get channel ID from channel name"""
        try:
            if channel_name.startswith('#'):
                channel_name = channel_name[1:]
            
            response = self.client.conversations_list(types="public_channel,private_channel")
            
            for channel in response['channels']:
                if channel['name'] == channel_name:
                    return channel['id']
            
            print(f"❌ Channel '{channel_name}' not found")
            return None
            
        except Exception as e:
            print(f"❌ Error finding channel: {e}")
            return None
    
    def setup_channel_transparency(self, channel_name: str) -> bool:
        """Complete transparency setup for a channel"""
        print(f"\n🔍 Setting up transparency for #{channel_name}...")
        
        # Get channel ID
        channel_id = self.get_channel_id(channel_name)
        if not channel_id:
            return False
        
        # Join channel if needed
        try:
            self.client.conversations_join(channel=channel_id)
            print(f"✅ Joined #{channel_name}")
        except Exception as e:
            if "already_in_channel" not in str(e):
                print(f"⚠️ Could not join #{channel_name}: {e}")
        
        # Post transparency message
        success = self.post_transparency_message(channel_id)
        
        if success:
            print(f"✅ Transparency setup complete for #{channel_name}")
            # Log the action
            self._log_transparency_action(channel_name, channel_id, success=True)
        else:
            print(f"❌ Transparency setup failed for #{channel_name}")
            self._log_transparency_action(channel_name, channel_id, success=False)
        
        return success
    
    def _log_transparency_action(self, channel_name: str, channel_id: str, success: bool):
        """Log transparency message posting for audit trail"""
        log_entry = {
            'action': 'transparency_message_posted',
            'channel_name': channel_name,
            'channel_id': channel_id,
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'posted_by': self.bot_user_id
        }
        
        try:
            with open('transparency_audit.jsonl', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️ Failed to log transparency action: {e}")


def main():
    """Main function to post transparency messages"""
    
    # Check for bot token
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN environment variable not set")
        return
    
    print("🤖 Claude Incident Analyzer - Channel Transparency Setup")
    print("=" * 60)
    
    # Initialize transparency manager
    transparency_manager = ChannelTransparencyManager(bot_token)
    
    # Get channels to setup
    print("\n📋 Enter channels where AI functionality will be used:")
    print("💡 You can enter multiple channels separated by commas")
    
    channels_input = input("Channel names (e.g., 'claude-test,incident-room'): ").strip()
    
    if not channels_input:
        print("❌ No channels specified")
        return
    
    # Parse channel names
    channel_names = [name.strip() for name in channels_input.split(',')]
    
    print(f"\n🎯 Setting up transparency for {len(channel_names)} channel(s)...")
    
    # Setup transparency for each channel
    results = {}
    for channel_name in channel_names:
        results[channel_name] = transparency_manager.setup_channel_transparency(channel_name)
    
    # Summary
    print(f"\n📊 Setup Summary:")
    successful = sum(results.values())
    print(f"✅ Successful: {successful}/{len(channel_names)} channels")
    
    for channel, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  #{channel}: {status}")
    
    if successful > 0:
        print(f"\n📌 Next Steps:")
        print("1. Verify transparency messages are visible and pinned")
        print("2. Test that AI disclaimers appear in analysis summaries")
        print("3. Document channel setup for compliance records")
        print("4. Train incident responders on AI transparency requirements")


if __name__ == "__main__":
    main()
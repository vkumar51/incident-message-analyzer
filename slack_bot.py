#!/usr/bin/env python3
"""
Slack Bot for Incident Message Analysis
Monitors Slack channels and provides real-time incident analysis
"""

import os
import json
import time
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.rtm_v2 import RTMClient
from batch_analyzer import BatchMessageAnalyzer
from summary_generator import IncidentSummaryGenerator

class IncidentSlackBot:
    def __init__(self, bot_token: str, app_token: str = None):
        """
        Initialize the Slack bot
        
        Args:
            bot_token: Slack Bot User OAuth Token (starts with xoxb-)
            app_token: Slack App Token for Socket Mode (starts with xapp-)
        """
        self.client = WebClient(token=bot_token)
        self.bot_token = bot_token
        self.app_token = app_token
        
        # Analysis components
        self.batch_analyzer = BatchMessageAnalyzer()
        self.summary_generator = IncidentSummaryGenerator()
        
        # Bot state
        self.monitored_channels = set()
        self.message_buffer = {}  # channel_id -> list of messages
        self.processed_messages = {}  # channel_id -> set of message timestamps
        self.last_analysis = {}   # channel_id -> timestamp
        self.analysis_interval = 1800  # 30 minutes in seconds
        
        # Bot info
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
    
    def add_channel_to_monitor(self, channel_name: str) -> bool:
        """
        Add a channel to monitoring list
        
        Args:
            channel_name: Channel name (with or without #)
            
        Returns:
            True if successfully added
        """
        try:
            # Clean channel name
            if channel_name.startswith('#'):
                channel_name = channel_name[1:]
            
            # Get channel info
            response = self.client.conversations_list(types="public_channel,private_channel")
            
            channel_id = None
            for channel in response['channels']:
                if channel['name'] == channel_name:
                    channel_id = channel['id']
                    break
            
            if not channel_id:
                print(f"❌ Channel '{channel_name}' not found")
                return False
            
            # Join channel if not already a member
            try:
                self.client.conversations_join(channel=channel_id)
                print(f"✅ Joined channel #{channel_name}")
            except Exception as e:
                if "already_in_channel" not in str(e):
                    print(f"⚠️ Could not join #{channel_name}: {e}")
            
            # Add to monitoring
            self.monitored_channels.add(channel_id)
            self.message_buffer[channel_id] = []
            self.processed_messages[channel_id] = set()
            self.last_analysis[channel_id] = datetime.now()
            
            print(f"✅ Now monitoring #{channel_name} (ID: {channel_id})")
            return True
            
        except Exception as e:
            print(f"❌ Error adding channel: {e}")
            return False
    
    def process_message(self, channel_id: str, message_data: Dict[str, Any]):
        """Process incoming message"""
        
        # Skip bot messages
        if message_data.get('user') == self.bot_user_id:
            return
        
        # Skip messages without text
        if not message_data.get('text'):
            return
        
        # Get user info
        user_name = self._get_user_name(message_data.get('user', 'Unknown'))
        
        # Create message object
        message = {
            'text': message_data['text'],
            'timestamp': datetime.fromtimestamp(float(message_data.get('ts', time.time()))).isoformat(),
            'user': user_name,
            'raw_data': message_data
        }
        
        # Add to buffer
        if channel_id in self.message_buffer:
            self.message_buffer[channel_id].append(message)
            print(f"📝 [{self._get_channel_name(channel_id)}] {user_name}: {message['text'][:50]}...")
        
        # Check if analysis is needed
        self._check_analysis_trigger(channel_id)
    
    def _get_user_name(self, user_id: str) -> str:
        """Get user display name"""
        try:
            response = self.client.users_info(user=user_id)
            return response['user']['real_name'] or response['user']['name']
        except:
            return user_id
    
    def _get_channel_name(self, channel_id: str) -> str:
        """Get channel name"""
        try:
            response = self.client.conversations_info(channel=channel_id)
            return f"#{response['channel']['name']}"
        except:
            return channel_id
    
    def _check_analysis_trigger(self, channel_id: str):
        """Check if analysis should be triggered"""
        now = datetime.now()
        last_analysis = self.last_analysis.get(channel_id, now)
        messages_count = len(self.message_buffer.get(channel_id, []))
        
        # Trigger analysis if:
        # 1. 30+ minutes since last analysis
        # 2. OR 20+ new messages accumulated
        time_trigger = (now - last_analysis).total_seconds() > self.analysis_interval
        message_trigger = messages_count >= 20
        
        if time_trigger or message_trigger:
            trigger_reason = "time interval" if time_trigger else f"{messages_count} messages"
            print(f"🔍 Triggering analysis for {self._get_channel_name(channel_id)} ({trigger_reason})")
            self._perform_analysis(channel_id)
    
    def _perform_analysis(self, channel_id: str):
        """Perform incident analysis on channel messages"""
        
        messages = self.message_buffer.get(channel_id, [])
        if not messages:
            print(f"⚠️ No messages to analyze in {self._get_channel_name(channel_id)}")
            return
        
        try:
            print(f"🔬 Analyzing {len(messages)} messages...")
            
            # Perform batch analysis
            analysis_results = self.batch_analyzer.analyze_conversation(messages)
            
            # Generate comprehensive summary  
            comprehensive_summary = self.summary_generator.generate_comprehensive_summary(analysis_results)
            
            # Post summary to channel
            self._post_analysis_summary(channel_id, analysis_results, comprehensive_summary)
            
            # Reset for next analysis but keep track of processed messages
            analyzed_timestamps = {
                datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00')).timestamp() 
                for msg in messages
            }
            self.processed_messages[channel_id].update(analyzed_timestamps)
            
            self.message_buffer[channel_id] = []
            self.last_analysis[channel_id] = datetime.now()
            
            # Save analysis results
            self._save_analysis_results(channel_id, comprehensive_summary)
            self._log_basic_metrics(channel_id, True)
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            self._post_error_message(channel_id, str(e))
            self._log_basic_metrics(channel_id, False, e)
    
    def _post_analysis_summary(self, channel_id: str, analysis: Dict, summary: Dict):
        """Post analysis summary to Slack channel"""
        
        try:
            # Create Slack message blocks
            blocks = self._create_summary_blocks(analysis, summary)
            
            response = self.client.chat_postMessage(
                channel=channel_id,
                text="🤖 Incident Analysis Summary",
                blocks=blocks
            )
            
            print(f"✅ Posted analysis summary to {self._get_channel_name(channel_id)}")
            
        except Exception as e:
            print(f"❌ Failed to post summary: {e}")
    
    def _create_summary_blocks(self, analysis: Dict, summary: Dict) -> List[Dict]:
        """Create Slack blocks for the summary"""
        
        overview = summary['incident_overview']
        executive_summary = summary['executive_summary']
        action_items = summary['action_items']
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🤖 Incident Analysis Summary"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:* {overview['incident_status']}"
                    },
                    {
                        "type": "mrkdwn", 
                        "text": f"*Messages Analyzed:* {overview['total_messages_analyzed']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Significant Events:* {overview['significant_events']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Categories:* {', '.join([f'{k}:{v}' for k,v in overview['categories_detected'].items() if v > 0])}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Executive Summary:*\n{executive_summary}"
                }
            }
        ]
        
        # Add action items if any
        if action_items:
            action_text = ""
            for item in action_items[:5]:  # Limit to 5 items
                status_icon = "✅" if item['status'] == 'completed' else "⏳" if item['status'] == 'pending' else "💡"
                action_text += f"{status_icon} {item['description']}\n"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Key Actions:*\n{action_text}"
                }
            })
        
        # Add feedback section
        blocks.append({
            "type": "divider"
        })
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Help us improve!* 📋"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Give Feedback",
                    "emoji": True
                },
                "url": "https://docs.google.com/forms/d/e/1FAIpQLScs50MAteC0TZ2YefvXJHtKw1PZUeqSRy3PDpuiGXk6FIMnqw/viewform?usp=publish-editor",
                "action_id": "feedback_button"
            }
        })
        
        # Add footer
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Generated by Claude Incident Analyzer • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            ]
        })
        
        return blocks
    
    def _post_error_message(self, channel_id: str, error: str):
        """Post error message to channel"""
        try:
            self.client.chat_postMessage(
                channel=channel_id,
                text=f"🚨 Analysis Error: {error}"
            )
        except Exception as e:
            print(f"❌ Failed to post error message: {e}")
    
    def _save_analysis_results(self, channel_id: str, summary: Dict):
        """Save analysis results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        channel_name = self._get_channel_name(channel_id).replace('#', '').replace(' ', '_')
        filename = f"analysis_{channel_name}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(summary, f, indent=2)
            print(f"💾 Analysis saved to {filename}")
        except Exception as e:
            print(f"⚠️ Failed to save analysis: {e}")
    
    def _log_basic_metrics(self, channel_id: str, success: bool, error=None):
        """Simple lightweight logging for performance monitoring"""
        metrics = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'channel': self._get_channel_name(channel_id),
            'success': success,
            'error': str(error) if error else None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open('usage_metrics.jsonl', 'a') as f:
                f.write(json.dumps(metrics) + '\n')
        except Exception as e:
            print(f"⚠️ Failed to log metrics: {e}")
    
    def start_monitoring(self):
        """Start monitoring channels for messages"""
        
        if not self.monitored_channels:
            print("⚠️ No channels to monitor. Add channels first.")
            return
        
        print(f"🚀 Starting monitoring of {len(self.monitored_channels)} channels...")
        print("📡 Listening for messages... (Press Ctrl+C to stop)")
        
        try:
            # Simple polling approach (you can upgrade to RTM or Socket Mode later)
            while True:
                self._poll_messages()
                time.sleep(5)  # Poll every 5 seconds
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
    
    def _poll_messages(self):
        """Poll channels for new messages"""
        for channel_id in self.monitored_channels:
            try:
                # Get recent messages (last 5 minutes)
                oldest = time.time() - 300  # 5 minutes ago
                
                response = self.client.conversations_history(
                    channel=channel_id,
                    oldest=oldest,
                    limit=50
                )
                
                # Process new messages
                for message in reversed(response['messages']):
                    message_ts = float(message.get('ts', 0))
                    
                    # Skip if we've already processed this message
                    if message_ts in self.processed_messages.get(channel_id, set()):
                        continue
                    
                    # Check if message is already in current buffer
                    current_messages = self.message_buffer.get(channel_id, [])
                    already_in_buffer = any(
                        abs(datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00')).timestamp() - message_ts) < 1
                        for msg in current_messages
                    )
                    
                    if not already_in_buffer and message.get('text'):
                        self.process_message(channel_id, message)
            
            except Exception as e:
                print(f"⚠️ Error polling {self._get_channel_name(channel_id)}: {e}")


def main():
    """Test the Slack bot"""
    
    # Check environment variables
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN environment variable not set")
        print("\n📋 Setup Instructions:")
        print("1. Create a Slack App at https://api.slack.com/apps")
        print("2. Add Bot Token Scopes: channels:read, channels:join, chat:write, users:read")
        print("3. Install app to workspace and get Bot User OAuth Token")
        print("4. Set environment variable: export SLACK_BOT_TOKEN='xoxb-your-token'")
        return
    
    if not os.getenv('ANTHROPIC_VERTEX_PROJECT_ID'):
        print("❌ ANTHROPIC_VERTEX_PROJECT_ID environment variable not set")
        return
    
    print("🤖 Claude Incident Analysis Slack Bot")
    print("=" * 50)
    
    # Initialize bot
    bot = IncidentSlackBot(bot_token)
    
    # Add test channel
    test_channel = input("Enter channel name to monitor (e.g., 'claude-test'): ").strip()
    if test_channel:
        success = bot.add_channel_to_monitor(test_channel)
        if success:
            print(f"\n🎯 Bot will analyze messages every {bot.analysis_interval/60} minutes or after 20 messages")
            print("💬 Try posting some test incident messages to see analysis in action!")
            
            # Start monitoring
            bot.start_monitoring()
        else:
            print("❌ Failed to add channel. Please check channel name and permissions.")
    else:
        print("❌ No channel specified")

if __name__ == "__main__":
    main()
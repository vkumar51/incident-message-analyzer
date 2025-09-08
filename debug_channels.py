#!/usr/bin/env python3
"""
Debug script to see what channels the bot can access
"""

import os
from slack_sdk import WebClient

def debug_channels():
    """Check what channels the bot can see"""
    
    bot_token = os.getenv('SLACK_BOT_TOKEN')
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN not set")
        return
    
    client = WebClient(token=bot_token)
    
    try:
        # Test bot connection
        auth_response = client.auth_test()
        print(f"✅ Bot connected as: {auth_response['user']}")
        print(f"   Bot ID: {auth_response['user_id']}")
        print(f"   Team: {auth_response['team']}")
        print()
        
        # List all channels the bot can see
        print("🔍 Searching for channels...")
        response = client.conversations_list(
            types="public_channel,private_channel",
            limit=100
        )
        
        print(f"📋 Found {len(response['channels'])} channels:")
        for channel in response['channels']:
            is_member = channel.get('is_member', False)
            member_status = "✅ Member" if is_member else "❌ Not Member"
            privacy = "🔒 Private" if channel.get('is_private') else "🌐 Public"
            
            print(f"   {privacy} #{channel['name']} ({channel['id']}) - {member_status}")
        
        print()
        print("🎯 Channels the bot is a member of:")
        member_channels = [ch for ch in response['channels'] if ch.get('is_member', False)]
        
        if member_channels:
            for channel in member_channels:
                print(f"   ✅ #{channel['name']}")
        else:
            print("   ❌ Bot is not a member of any channels")
            print("   💡 Try manually inviting the bot to a channel first")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_channels()
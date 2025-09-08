#!/usr/bin/env python3
"""
Slack Bot Demo - Simulates Slack integration for testing
"""

import json
import time
from datetime import datetime
from batch_analyzer import BatchMessageAnalyzer
from summary_generator import IncidentSummaryGenerator

class SlackBotDemo:
    def __init__(self):
        """Initialize demo bot"""
        self.batch_analyzer = BatchMessageAnalyzer()
        self.summary_generator = IncidentSummaryGenerator()
    
    def simulate_incident_channel(self):
        """Simulate a realistic incident channel conversation"""
        
        print("🤖 Claude Incident Analysis Bot - DEMO MODE")
        print("=" * 60)
        print("Simulating live incident channel: #ITN-2025-12345")
        print("🔥 Incident: API performance degradation")
        print("-" * 60)
        
        # Realistic incident conversation
        incident_messages = [
            {
                'text': 'API response times are spiking to 5+ seconds globally',
                'timestamp': '2025-01-15T10:15:00Z',
                'user': 'Alice (SRE)'
            },
            {
                'text': 'Seeing same issue, checking our monitoring dashboard now',
                'timestamp': '2025-01-15T10:16:00Z', 
                'user': 'Bob (DevOps)'
            },
            {
                'text': 'Database connection pool is at 98% utilization',
                'timestamp': '2025-01-15T10:17:00Z',
                'user': 'Alice (SRE)'
            },
            {
                'text': 'Error rate increased from 0.1% to 3.2% in the last 10 minutes',
                'timestamp': '2025-01-15T10:18:00Z',
                'user': 'Charlie (Monitoring)'
            },
            {
                'text': 'Customer support receiving complaints about checkout failures',
                'timestamp': '2025-01-15T10:19:00Z',
                'user': 'Dana (Support)'
            },
            {
                'text': 'Impact assessment: approximately 60% of transactions affected',
                'timestamp': '2025-01-15T10:20:00Z',
                'user': 'Alice (SRE)'
            },
            {
                'text': 'Scaling database connection pool from 100 to 200 connections',
                'timestamp': '2025-01-15T10:21:00Z',
                'user': 'Bob (DevOps)'
            },
            {
                'text': 'Found correlation: spike started right after payment-service v2.1.0 deployment',
                'timestamp': '2025-01-15T10:23:00Z',
                'user': 'Eve (Engineer)'
            },
            {
                'text': 'Rolling back payment-service to v2.0.8 immediately',
                'timestamp': '2025-01-15T10:24:00Z',
                'user': 'Alice (SRE)'
            },
            {
                'text': 'Rollback initiated for payment-service deployment',
                'timestamp': '2025-01-15T10:25:00Z',
                'user': 'Bob (DevOps)'
            },
            {
                'text': 'API response times dropping back to normal (~300ms)',
                'timestamp': '2025-01-15T10:28:00Z',
                'user': 'Charlie (Monitoring)'
            },
            {
                'text': 'Error rate back down to 0.2% - within normal range',
                'timestamp': '2025-01-15T10:30:00Z',
                'user': 'Charlie (Monitoring)'
            },
            {
                'text': 'Customer complaints have stopped coming in',
                'timestamp': '2025-01-15T10:32:00Z',
                'user': 'Dana (Support)'
            },
            {
                'text': 'Incident resolved - all metrics back to baseline. Will monitor for 30 minutes',
                'timestamp': '2025-01-15T10:35:00Z',
                'user': 'Alice (SRE)'
            },
            {
                'text': 'Post-mortem scheduled for 2 PM today to analyze v2.1.0 issues',
                'timestamp': '2025-01-15T10:36:00Z',
                'user': 'Alice (SRE)'
            },
            {
                'text': 'Great response time team! 👏',
                'timestamp': '2025-01-15T10:37:00Z',
                'user': 'Manager'
            }
        ]
        
        print("\n📝 Messages received:")
        for i, msg in enumerate(incident_messages, 1):
            print(f"  {i:2d}. [{msg['timestamp'][11:16]}] {msg['user']}: {msg['text']}")
            time.sleep(0.3)  # Simulate real-time message flow
        
        print(f"\n🔍 Analyzing {len(incident_messages)} messages...")
        
        # Perform analysis
        analysis_results = self.batch_analyzer.analyze_conversation(incident_messages)
        comprehensive_summary = self.summary_generator.generate_comprehensive_summary(analysis_results)
        
        # Display Slack-style summary
        self.display_slack_summary(comprehensive_summary)
        
        # Save results
        with open('demo_incident_analysis.json', 'w') as f:
            json.dump(comprehensive_summary, f, indent=2)
        
        print(f"\n💾 Full analysis saved to 'demo_incident_analysis.json'")
        
        return comprehensive_summary
    
    def display_slack_summary(self, summary):
        """Display summary in Slack-style format"""
        
        print("\n" + "🤖 " + "="*55)
        print("🤖 CLAUDE INCIDENT ANALYSIS SUMMARY")
        print("🤖 " + "="*55)
        
        overview = summary['incident_overview']
        executive_summary = summary['executive_summary']
        action_items = summary['action_items']
        
        # Status overview
        print(f"\n📊 INCIDENT OVERVIEW")
        print(f"   Status: {overview['incident_status']}")
        print(f"   Messages Analyzed: {overview['total_messages_analyzed']}")
        print(f"   Significant Events: {overview['significant_events']}")
        
        categories = overview['categories_detected']
        category_text = ', '.join([f'{k}:{v}' for k,v in categories.items() if v > 0])
        print(f"   Categories: {category_text}")
        
        # Executive summary
        print(f"\n📋 EXECUTIVE SUMMARY")
        print(f"   {executive_summary}")
        
        # Action items
        if action_items:
            print(f"\n🎯 KEY ACTIONS")
            for item in action_items[:5]:
                status_icon = "✅" if item['status'] == 'completed' else "⏳" if item['status'] == 'pending' else "💡"
                print(f"   {status_icon} {item['description']}")
        
        # AI Insights (truncated for Slack)
        ai_insights = summary.get('ai_insights', '')
        if ai_insights:
            # Extract just the root cause section
            insights_lines = ai_insights.split('\n')
            root_cause_section = []
            in_root_cause = False
            
            for line in insights_lines:
                if 'Root Cause Analysis' in line:
                    in_root_cause = True
                    continue
                elif line.strip() and line[0].isupper() and ':' in line and in_root_cause:
                    break  # Next section
                elif in_root_cause and line.strip():
                    root_cause_section.append(line.strip())
            
            if root_cause_section:
                print(f"\n🧠 AI INSIGHTS")
                print(f"   {' '.join(root_cause_section)}")
        
        # Footer
        print(f"\n⏰ Generated by Claude Incident Analyzer • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🤖 " + "="*55)

def main():
    """Run the Slack bot demo"""
    
    demo = SlackBotDemo()
    
    print("Starting incident simulation in 3 seconds...")
    time.sleep(3)
    
    # Run simulation
    summary = demo.simulate_incident_channel()
    
    print(f"\n✨ DEMO COMPLETE")
    print(f"This shows how the bot would analyze and summarize a real incident!")
    print(f"\nTo connect to real Slack:")
    print(f"1. Follow setup instructions in SLACK_SETUP.md")
    print(f"2. Set SLACK_BOT_TOKEN environment variable")  
    print(f"3. Run: python3 slack_bot.py")

if __name__ == "__main__":
    main()
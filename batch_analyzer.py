#!/usr/bin/env python3
"""
Batch Message Analyzer - Process multiple incident messages for comprehensive analysis
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from message_analyzer import MessageAnalyzer

class BatchMessageAnalyzer:
    def __init__(self):
        """Initialize the batch analyzer"""
        self.analyzer = MessageAnalyzer()
    
    def analyze_conversation(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a conversation thread of incident messages
        
        Args:
            messages: List of message dicts with keys: 'text', 'timestamp', 'user'
            
        Returns:
            Dict with batch analysis results
        """
        results = []
        significant_messages = []
        actions_taken = []
        
        print(f"Analyzing {len(messages)} messages...")
        
        for i, msg in enumerate(messages, 1):
            try:
                # Analyze individual message
                analysis = self.analyzer.analyze_message(msg['text'])
                
                # Add metadata
                analysis.update({
                    'message_id': i,
                    'timestamp': msg.get('timestamp', ''),
                    'user': msg.get('user', 'Unknown'),
                    'original_text': msg['text']
                })
                
                results.append(analysis)
                
                # Track significant messages
                if analysis.get('significant'):
                    significant_messages.append(analysis)
                    if analysis.get('category') == 'actions':
                        actions_taken.append(analysis)
                
                status_icon = '✅' if analysis.get('significant') else '❌'
                print(f"  {i:2d}/{len(messages)}: {status_icon} {msg['text'][:50]}...")
                # Print error reason if analysis failed
                if not analysis.get('significant') and 'Error analyzing message' in analysis.get('reason', ''):
                    print(f"       ERROR: {analysis.get('reason')}")
                
            except Exception as e:
                error_analysis = {
                    'message_id': i,
                    'timestamp': msg.get('timestamp', ''),
                    'user': msg.get('user', 'Unknown'),
                    'original_text': msg['text'],
                    'significant': False,
                    'category': None,
                    'reason': f"Analysis error: {str(e)}"
                }
                results.append(error_analysis)
        
        # Categorize messages
        categories = self._categorize_messages(significant_messages)
        
        # Generate batch summary
        summary = self._generate_batch_summary(results, significant_messages, categories)
        
        return {
            'total_messages': len(messages),
            'significant_count': len(significant_messages),
            'categories': categories,
            'significance_rate': (len(significant_messages) / len(messages)) * 100 if messages else 0,
            'summary': summary,
            'significant_messages': significant_messages,
            'all_results': results
        }
    
    def _categorize_messages(self, significant_messages: List[Dict]) -> Dict[str, int]:
        """Categorize significant messages by type"""
        categories = {
            'diagnostics': 0,
            'actions': 0,
            'impact': 0,
            'resolution': 0
        }
        
        for msg in significant_messages:
            category = msg.get('category')
            if category in categories:
                categories[category] += 1
        
        return categories
    
    def _generate_batch_summary(self, all_results: List[Dict], significant: List[Dict], categories: Dict[str, int]) -> str:
        """Generate a comprehensive summary of the batch analysis"""
        if not significant:
            return "No significant incident activities detected in this conversation."
        
        summary_parts = []
        
        # Category breakdown
        category_summary = []
        for category, count in categories.items():
            if count > 0:
                category_summary.append(f"{count} {category}")
        
        if category_summary:
            summary_parts.append(f"Activity detected: {', '.join(category_summary)}")
        
        # Incident progression
        if len(significant) > 2:
            summary_parts.append(f"Tracked {len(significant)} significant updates showing incident progression")
        
        # Key insights from each category
        insights = []
        for msg in significant[:4]:  # Top 4 most significant
            category = msg.get('category', 'unknown')
            reason = msg.get('reason', '')[:80] + '...' if len(msg.get('reason', '')) > 80 else msg.get('reason', '')
            insights.append(f"[{category.upper()}] {reason}")
        
        if insights:
            summary_parts.append(f"Key insights: {' | '.join(insights)}")
        
        return ". ".join(summary_parts) + "."

def create_sample_incident_conversation() -> List[Dict[str, Any]]:
    """Create a realistic incident conversation for testing"""
    return [
        {
            'text': 'API latency is spiking to 2+ seconds',
            'timestamp': '2025-01-15T14:30:00Z',
            'user': 'alice'
        },
        {
            'text': 'Seeing the same here, checking the monitoring dashboard',
            'timestamp': '2025-01-15T14:31:00Z',
            'user': 'bob'
        },
        {
            'text': 'Database connection pool is maxed out at 100 connections',
            'timestamp': '2025-01-15T14:32:00Z',
            'user': 'alice'
        },
        {
            'text': 'Scaling up the database connection pool to 200 connections',
            'timestamp': '2025-01-15T14:33:00Z',
            'user': 'charlie'
        },
        {
            'text': 'Still seeing high latency, going to restart the API service',
            'timestamp': '2025-01-15T14:35:00Z',
            'user': 'alice'
        },
        {
            'text': 'Restarting api-service-deployment now',
            'timestamp': '2025-01-15T14:36:00Z',
            'user': 'alice'
        },
        {
            'text': 'Latency dropped back to normal (~200ms)',
            'timestamp': '2025-01-15T14:38:00Z',
            'user': 'bob'
        },
        {
            'text': 'Confirmed - issue resolved. Will monitor for next 30 minutes',
            'timestamp': '2025-01-15T14:39:00Z',
            'user': 'alice'
        },
        {
            'text': 'Thanks for the quick response team!',
            'timestamp': '2025-01-15T14:40:00Z',
            'user': 'david'
        }
    ]

def main():
    """Test batch message analysis"""
    
    if not os.getenv('ANTHROPIC_VERTEX_PROJECT_ID'):
        print("Error: ANTHROPIC_VERTEX_PROJECT_ID environment variable not set")
        return
    
    print("Batch Message Analyzer")
    print("=" * 50)
    
    # Initialize batch analyzer
    batch_analyzer = BatchMessageAnalyzer()
    
    # Get sample conversation
    conversation = create_sample_incident_conversation()
    
    print(f"\nProcessing incident conversation with {len(conversation)} messages...")
    print("-" * 50)
    
    # Analyze the conversation
    results = batch_analyzer.analyze_conversation(conversation)
    
    # Display results
    print(f"\n📊 BATCH ANALYSIS RESULTS")
    print("=" * 50)
    print(f"Total messages: {results['total_messages']}")
    print(f"Significant messages: {results['significant_count']}")
    print(f"Categories found: {results['categories']}")
    print(f"Significance rate: {results['significance_rate']:.1f}%")
    
    print(f"\n📋 SUMMARY:")
    print(results['summary'])
    
    print(f"\n🎯 SIGNIFICANT MESSAGES:")
    for msg in results['significant_messages']:
        timestamp = msg.get('timestamp', 'Unknown')[:16]
        user = msg.get('user', 'Unknown')
        text = msg['original_text'][:60]
        reason = msg.get('reason', '')[:80]
        
        print(f"  [{timestamp}] {user}: {text}...")
        print(f"    → {reason}")
    
    # Export results
    with open('incident_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Full results exported to 'incident_analysis.json'")

if __name__ == "__main__":
    main()
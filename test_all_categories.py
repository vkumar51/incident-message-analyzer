#!/usr/bin/env python3
"""
Test all categories: Diagnostics, Actions, Impact, Resolution
"""

import json
import os
from message_analyzer import MessageAnalyzer

def main():
    """Test message analyzer with all categories"""
    
    if not os.getenv('ANTHROPIC_VERTEX_PROJECT_ID'):
        print("Error: ANTHROPIC_VERTEX_PROJECT_ID environment variable not set")
        return
    
    analyzer = MessageAnalyzer()
    
    # Test messages organized by expected category
    test_cases = {
        "Category 1: Diagnostics & Root Cause": [
            "Found the root cause: memory leak in payment service after 6 hours uptime",
            "Correlation confirmed: failures started exactly when we deployed v2.1.4",
            "Error pattern identified: all failed requests have malformed JWT tokens",
            "Database deadlock detected in transactions table affecting order processing",
            "Network latency spike isolated to us-east-1a zone, other zones normal",
            "Hypothesis confirmed: rate limiting is causing 429 errors above 1000 req/s",
        ],
        
        "Category 2: Actions & Remediation": [
            "Rolling back authentication service to v4.12.1",
            "Restarting ingress controller to clear connection pool",
            "Scaling replica count from 3 to 8 to handle load",
            "Deploying hotfix v2.3.1 to production",
            "Cordoning node-7 and draining pods for maintenance",
            "Escalating to database team for urgent assistance",
        ],
        
        "Category 3: Impact & Scope Changes": [
            "Impact expanded: now affecting 75% of our customers in EU region",
            "Severity upgraded from degraded to complete outage",
            "New symptom: authentication is now failing in addition to payment issues",
            "Incident contained: isolated to staging environment, production unaffected",
            "Geographic spread: failures now reported in Asia-Pacific region too",
            "Service degradation: response times increased from 200ms to 5+ seconds",
        ],
        
        "Category 4: Resolution & Milestones": [
            "Incident officially resolved - monitoring shows all systems normal",
            "Post-mortem scheduled for tomorrow at 2 PM to review timeline",
            "Follow-up action: implement alerting for memory usage above 80%",
            "All services stable for 30 minutes, marking as resolved",
            "RCA document created and shared with engineering leadership",
            "Resolution confirmed: error rate back to baseline 0.01%",
        ],
        
        "Non-Significant (Should be rejected)": [
            "Thanks for the quick response!",
            "Any updates on the investigation?",
            "I'm looking into the logs now",
            "Still checking various dashboards",
            "Let me know if you need help",
            "Maybe it's related to the network?",
        ]
    }
    
    print("Multi-Category Message Analyzer Test")
    print("=" * 60)
    
    category_stats = {
        "diagnostics": 0,
        "actions": 0, 
        "impact": 0,
        "resolution": 0,
        "not_significant": 0
    }
    
    for category_name, messages in test_cases.items():
        print(f"\n🔍 Testing: {category_name}")
        print("-" * 50)
        
        for i, message in enumerate(messages, 1):
            try:
                result = analyzer.analyze_message(message)
                
                # Count categories
                detected_category = result.get("category")
                if detected_category in category_stats:
                    category_stats[detected_category] += 1
                elif not result.get("significant"):
                    category_stats["not_significant"] += 1
                
                # Display result
                if result.get("significant"):
                    print(f"  {i}. ✅ [{detected_category.upper()}]: {message[:50]}...")
                    print(f"     → {result.get('reason')}")
                else:
                    print(f"  {i}. ❌ NOT SIGNIFICANT: {message[:50]}...")
                    print(f"     → {result.get('reason')}")
                
            except Exception as e:
                print(f"  {i}. ❌ ERROR: {message[:50]}...")
                print(f"     → {str(e)}")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("📊 CATEGORY DETECTION SUMMARY")
    print("=" * 60)
    
    total_significant = sum(v for k, v in category_stats.items() if k != "not_significant")
    total_messages = sum(category_stats.values())
    
    for category, count in category_stats.items():
        percentage = (count / total_messages * 100) if total_messages > 0 else 0
        icon = "🔍" if category == "diagnostics" else "⚡" if category == "actions" else "📊" if category == "impact" else "✅" if category == "resolution" else "❌"
        print(f"{icon} {category.upper():15}: {count:2d} messages ({percentage:5.1f}%)")
    
    print(f"\n📈 Overall significance rate: {total_significant}/{total_messages} ({(total_significant/total_messages*100):.1f}%)")
    
    # Export detailed results
    print(f"\n💾 Test completed successfully!")

if __name__ == "__main__":
    main()
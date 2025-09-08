#!/usr/bin/env python3
"""
Test the Claude SDK Message Analyzer with multiple sample messages
"""

import json
import os
from message_analyzer import MessageAnalyzer

def main():
    """Test multiple incident messages"""
    
    if not os.getenv('ANTHROPIC_VERTEX_PROJECT_ID'):
        print("Error: ANTHROPIC_VERTEX_PROJECT_ID environment variable not set")
        return
    
    analyzer = MessageAnalyzer()
    
    # Comprehensive test cases covering different categories
    test_messages = [
        # Category 2: Actions (should be SIGNIFICANT)
        "We are rolling back the authentication operator to v4.12.1",
        "Restarting the ingress controller to resolve the connection issues",
        "Scaled the replica count from 3 to 5 to handle increased load",
        "Deploying hotfix v2.3.1 to production cluster",
        "Cordoning node-7 and draining all pods for maintenance",
        "Applied resource limit increase to billing-service deployment",
        "Reverting the network policy changes that caused the outage",
        
        # Non-significant messages (should be NOT SIGNIFICANT)
        "Just checking the pod status",
        "Any updates on the issue?",
        "Looking into the logs now",
        "Still investigating the root cause",
        "Thanks for the update",
        "I'll keep monitoring the situation",
        "No errors showing in the dashboard",
        
        # Edge cases / ambiguous messages
        "Thinking about rolling back but not sure yet",
        "We might need to restart if this doesn't work",
        "Preparing to scale up if needed",
        "Ready to deploy the fix once approved",
        
        # Potential other categories (testing how it categorizes)
        "Found the root cause: memory leak in payment service",
        "Error rate dropped to 0% after the fix",
        "Identified correlation between deployment and failures",
        "This is affecting 50% of our customers now",
    ]
    
    print("Claude SDK Message Analyzer - Comprehensive Testing")
    print("=" * 60)
    print()
    
    significant_count = 0
    total_count = len(test_messages)
    
    for i, message in enumerate(test_messages, 1):
        print(f"{i:2d}. Message: {message}")
        
        try:
            result = analyzer.analyze_message(message)
            
            # Pretty print the result
            print(f"    Analysis: {json.dumps(result, indent=14)[1:-1]}")
            
            if result.get("significant"):
                print(f"    ✅ SIGNIFICANT [{result.get('category', 'unknown')}]: {result.get('reason')}")
                significant_count += 1
            else:
                print(f"    ❌ NOT SIGNIFICANT: {result.get('reason')}")
                
        except Exception as e:
            print(f"    ❌ ERROR: {str(e)}")
        
        print()
    
    # Summary
    print("=" * 60)
    print(f"SUMMARY: {significant_count}/{total_count} messages marked as significant")
    print(f"Significance rate: {(significant_count/total_count)*100:.1f}%")

if __name__ == "__main__":
    main()
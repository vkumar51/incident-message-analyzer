#!/usr/bin/env python3
"""
Simple Message Analyzer - Uses direct Anthropic API as fallback
"""

import json
import os
from typing import Dict, Any

def analyze_with_mock(message: str) -> Dict[str, Any]:
    """
    Mock analyzer for testing the structure without API calls
    """
    # Simple keyword-based detection for demonstration
    action_keywords = [
        "rolling back", "rollback", "revert", "reverting",
        "restarting", "restart", "scaled", "scaling",
        "deployed", "deploying", "cordoned", "draining"
    ]
    
    message_lower = message.lower()
    has_action = any(keyword in message_lower for keyword in action_keywords)
    
    if has_action:
        # Find which action was detected
        detected_action = next((keyword for keyword in action_keywords if keyword in message_lower), "action")
        return {
            "significant": True,
            "category": "actions",
            "reason": f"Detected {detected_action} - indicates remediation action"
        }
    else:
        return {
            "significant": False,
            "category": None,
            "reason": "No action keywords detected"
        }

def main():
    """Test the message analyzer structure"""
    print("Simple Message Analyzer (Mock Mode)")
    print("=" * 40)
    
    # Test messages
    test_messages = [
        "We are rolling back the authentication operator to v4.12.1",
        "Just checking the pod status",
        "Restarting the ingress controller now",
        "Any updates on the issue?",
        "Scaled the replica count from 3 to 5"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Analyzing: {message}")
        result = analyze_with_mock(message)
        print(f"   Result: {json.dumps(result, indent=2)}")
        
        if result.get("significant"):
            print(f"   ✅ SIGNIFICANT: {result.get('reason')}")
        else:
            print(f"   ❌ NOT SIGNIFICANT: {result.get('reason')}")

if __name__ == "__main__":
    main()
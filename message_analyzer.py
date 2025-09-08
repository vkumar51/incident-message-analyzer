#!/usr/bin/env python3
"""
Simple Claude SDK Message Analyzer
Analyzes incident messages for significance detection
"""

import json
import os
from typing import Dict, Any
from anthropic import AnthropicVertex


class MessageAnalyzer:
    def __init__(self, project_id: str = None, region: str = "us-east5"):
        """Initialize the Claude SDK client for Vertex AI"""
        self.client = AnthropicVertex(
            project_id=project_id or os.getenv('ANTHROPIC_VERTEX_PROJECT_ID'),
            region=region
        )
    
    def analyze_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze a single incident message for significance
        
        Args:
            message: The incident message to analyze
            
        Returns:
            Dict with significance, category, and reason
        """
        prompt = f"""
        Analyze this incident message for significance across multiple categories:
        
        Message: "{message}"
        
        Determine if this message indicates significant incident activity in any of these categories:
        
        **Category 1: Diagnostics & Root Cause Analysis**
        - Specific error messages or patterns identified
        - Root cause discoveries or correlations established
        - Component or service implicated with evidence
        - Diagnostic tests revealing critical information
        - Hypotheses confirmed or refuted with data
        
        **Category 2: Actions & Remediation Efforts**
        - Rollbacks, reversions, deployments
        - Service restarts, scaling, configuration changes
        - Node/pod management (cordon, drain, restart)
        - Workarounds implemented
        - Escalations to external teams
        
        **Category 3: Impact & Scope Changes**
        - Number of affected users/services/nodes changing
        - Severity level changes (degraded → unavailable)
        - Geographic or environment scope changes
        - New symptoms or unexpected behaviors appearing
        - Incident containment status updates
        
        **Category 4: Resolution & Milestones**
        - Incident officially declared resolved
        - Post-mortem or RCA scheduled/started
        - Follow-up actions identified for prevention
        - Monitoring confirms stability
        - Final status updates and closures
        
        **Ignore these (Non-significant):**
        - General chatter, greetings, thanks
        - Pure speculation without evidence
        - Redundant confirmations of known facts
        - Vague statements without specifics
        - Simple status inquiries without answers
        
        Respond with JSON only:
        {{
            "significant": true/false,
            "category": "diagnostics|actions|impact|resolution|null",
            "reason": "brief explanation of significance and which category applies"
        }}
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku@20241022",
                max_tokens=200,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse the JSON response
            result = json.loads(response.content[0].text)
            return result
            
        except Exception as e:
            return {
                "significant": False,
                "category": None,
                "reason": f"Error analyzing message: {str(e)}"
            }


def main():
    """Test the message analyzer with sample data"""
    
    # Check for Vertex AI project ID
    if not os.getenv('ANTHROPIC_VERTEX_PROJECT_ID'):
        print("Error: ANTHROPIC_VERTEX_PROJECT_ID environment variable not set")
        print("Set it with: export ANTHROPIC_VERTEX_PROJECT_ID='your-gcp-project-id'")
        return
    
    # Initialize analyzer
    analyzer = MessageAnalyzer()
    
    # Sample message
    sample_message = "We are rolling back the authentication operator to v4.12.1"
    
    print("Claude SDK Message Analyzer")
    print("=" * 40)
    print(f"Analyzing message: {sample_message}")
    print()
    
    # Analyze the message
    result = analyzer.analyze_message(sample_message)
    
    # Display results
    print("Analysis Result:")
    print(json.dumps(result, indent=2))
    
    # Interpret results
    if result.get("significant"):
        print(f"\n✅ SIGNIFICANT: {result.get('reason')}")
        print(f"Category: {result.get('category')}")
    else:
        print(f"\n❌ NOT SIGNIFICANT: {result.get('reason')}")


if __name__ == "__main__":
    main()
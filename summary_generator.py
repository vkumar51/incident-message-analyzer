#!/usr/bin/env python3
"""
Enhanced Summary Generator - Creates executive and technical summaries from incident analysis
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
from message_analyzer import MessageAnalyzer

class IncidentSummaryGenerator:
    def __init__(self):
        """Initialize the summary generator"""
        self.analyzer = MessageAnalyzer()
    
    def generate_comprehensive_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive incident summary from batch analysis results
        
        Args:
            analysis_results: Results from BatchMessageAnalyzer
            
        Returns:
            Dict with multiple summary formats
        """
        
        # Extract key data
        significant_messages = analysis_results.get('significant_messages', [])
        categories = analysis_results.get('categories', {})
        total_messages = analysis_results.get('total_messages', 0)
        
        # Generate different summary types
        executive_summary = self._generate_executive_summary(significant_messages, categories)
        technical_timeline = self._generate_technical_timeline(significant_messages)
        action_items = self._generate_action_items(significant_messages)
        impact_assessment = self._generate_impact_assessment(significant_messages, categories)
        ai_insights = self._generate_ai_insights(significant_messages)
        
        return {
            'incident_overview': {
                'total_messages_analyzed': total_messages,
                'significant_events': len(significant_messages),
                'categories_detected': categories,
                'incident_status': self._determine_incident_status(significant_messages)
            },
            'executive_summary': executive_summary,
            'technical_timeline': technical_timeline,
            'action_items': action_items,
            'impact_assessment': impact_assessment,
            'ai_insights': ai_insights,
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_executive_summary(self, messages: List[Dict], categories: Dict[str, int]) -> str:
        """Generate executive-level summary"""
        
        if not messages:
            return "No significant incident activity detected."
        
        # Build summary components
        summary_parts = []
        
        # Status and scope
        status = self._determine_incident_status(messages)
        summary_parts.append(f"Incident Status: {status}")
        
        # Activity overview
        activity_desc = self._describe_activity_level(categories)
        summary_parts.append(activity_desc)
        
        # Key outcomes
        outcomes = self._extract_key_outcomes(messages)
        if outcomes:
            summary_parts.append(f"Key Outcomes: {outcomes}")
        
        # Business impact (if any)
        impact = self._assess_business_impact(messages)
        if impact:
            summary_parts.append(f"Impact: {impact}")
        
        return ". ".join(summary_parts) + "."
    
    def _generate_technical_timeline(self, messages: List[Dict]) -> List[Dict[str, Any]]:
        """Generate technical timeline of events"""
        
        timeline = []
        for msg in messages:
            timeline_entry = {
                'timestamp': msg.get('timestamp', ''),
                'user': msg.get('user', 'Unknown'),
                'category': msg.get('category', '').upper(),
                'event': msg.get('original_text', ''),
                'significance': msg.get('reason', ''),
                'message_id': msg.get('message_id', 0)
            }
            timeline.append(timeline_entry)
        
        return timeline
    
    def _generate_action_items(self, messages: List[Dict]) -> List[Dict[str, Any]]:
        """Extract and generate action items"""
        
        action_items = []
        
        # Extract actions taken
        actions_taken = [msg for msg in messages if msg.get('category') == 'actions']
        for action in actions_taken:
            action_items.append({
                'type': 'completed_action',
                'description': action.get('original_text', ''),
                'timestamp': action.get('timestamp', ''),
                'user': action.get('user', ''),
                'status': 'completed'
            })
        
        # Extract follow-up items from resolution messages
        resolutions = [msg for msg in messages if msg.get('category') == 'resolution']
        for resolution in resolutions:
            text = resolution.get('original_text', '').lower()
            if 'monitor' in text:
                action_items.append({
                    'type': 'follow_up',
                    'description': 'Continue monitoring system stability',
                    'timestamp': resolution.get('timestamp', ''),
                    'status': 'pending'
                })
            if 'post-mortem' in text or 'rca' in text:
                action_items.append({
                    'type': 'follow_up', 
                    'description': 'Complete post-mortem analysis',
                    'timestamp': resolution.get('timestamp', ''),
                    'status': 'pending'
                })
        
        # Suggest preventive actions based on diagnostics
        diagnostics = [msg for msg in messages if msg.get('category') == 'diagnostics']
        for diagnostic in diagnostics:
            reason = diagnostic.get('reason', '').lower()
            if 'memory leak' in reason:
                action_items.append({
                    'type': 'preventive',
                    'description': 'Implement memory usage monitoring and alerts',
                    'status': 'suggested'
                })
            elif 'connection pool' in reason:
                action_items.append({
                    'type': 'preventive',
                    'description': 'Review and optimize database connection pool configuration',
                    'status': 'suggested'
                })
        
        return action_items
    
    def _generate_impact_assessment(self, messages: List[Dict], categories: Dict[str, int]) -> Dict[str, Any]:
        """Assess incident impact"""
        
        impact_msgs = [msg for msg in messages if msg.get('category') == 'impact']
        
        assessment = {
            'severity': 'unknown',
            'scope': 'unknown',
            'customer_impact': 'unknown',
            'duration': 'unknown',
            'services_affected': []
        }
        
        # Extract impact details from messages
        for msg in impact_msgs:
            text = msg.get('original_text', '').lower()
            reason = msg.get('reason', '').lower()
            
            # Assess severity
            if 'outage' in text or 'unavailable' in text:
                assessment['severity'] = 'high'
            elif 'degraded' in text or 'slow' in text:
                assessment['severity'] = 'medium'
            
            # Extract customer impact
            if '%' in text:
                import re
                percentages = re.findall(r'(\d+)%', text)
                if percentages:
                    assessment['customer_impact'] = f"{percentages[0]}% affected"
        
        # Infer from other categories if no explicit impact messages
        if not impact_msgs:
            if categories.get('actions', 0) > 2:
                assessment['severity'] = 'medium'
                assessment['scope'] = 'service-level'
            if categories.get('resolution', 0) > 0:
                assessment['duration'] = 'resolved'
        
        return assessment
    
    def _generate_ai_insights(self, messages: List[Dict]) -> str:
        """Generate AI-powered insights using Claude"""
        
        if not messages:
            return "No significant messages to analyze for insights."
        
        # Prepare context for AI analysis
        context = "Incident Messages:\n"
        for i, msg in enumerate(messages[:10], 1):  # Limit to first 10 for context
            context += f"{i}. [{msg.get('category', 'unknown').upper()}] {msg.get('original_text', '')}\n"
        
        prompt = f"""
        Analyze this incident conversation and provide strategic insights:
        
        {context}
        
        Please provide:
        1. Root cause analysis summary
        2. Response effectiveness assessment  
        3. Preventive recommendations
        4. Process improvement suggestions
        
        Focus on executive-level insights that would help prevent similar incidents.
        Keep response to 2-3 sentences per point.
        """
        
        try:
            response = self.analyzer.client.messages.create(
                model="claude-3-5-haiku@20241022",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"AI insights unavailable: {str(e)}"
    
    def _determine_incident_status(self, messages: List[Dict]) -> str:
        """Determine current incident status"""
        
        if not messages:
            return "No Activity"
        
        # Check for resolution messages
        resolution_msgs = [msg for msg in messages if msg.get('category') == 'resolution']
        if resolution_msgs:
            latest_resolution = resolution_msgs[-1]
            text = latest_resolution.get('original_text', '').lower()
            if 'resolved' in text:
                return "Resolved"
            elif 'monitoring' in text:
                return "Monitoring"
        
        # Check for recent actions
        action_msgs = [msg for msg in messages if msg.get('category') == 'actions']
        if action_msgs:
            return "Active Response"
        
        # Check for diagnostics
        diagnostic_msgs = [msg for msg in messages if msg.get('category') == 'diagnostics']
        if diagnostic_msgs:
            return "Under Investigation"
        
        return "Active"
    
    def _describe_activity_level(self, categories: Dict[str, int]) -> str:
        """Describe the level and type of incident activity"""
        
        total_activity = sum(categories.values())
        if total_activity == 0:
            return "No significant incident activity detected"
        
        activity_types = []
        for category, count in categories.items():
            if count > 0:
                activity_types.append(f"{count} {category}")
        
        return f"Detected {total_activity} significant events: {', '.join(activity_types)}"
    
    def _extract_key_outcomes(self, messages: List[Dict]) -> str:
        """Extract key outcomes from the incident"""
        
        # Look for resolution and final state messages
        outcomes = []
        
        for msg in messages:
            text = msg.get('original_text', '').lower()
            if msg.get('category') == 'resolution':
                if 'resolved' in text:
                    outcomes.append("incident resolved")
                if 'monitor' in text:
                    outcomes.append("monitoring stability")
            elif 'normal' in text or 'baseline' in text:
                outcomes.append("performance restored")
        
        return ', '.join(outcomes) if outcomes else "incident response in progress"
    
    def _assess_business_impact(self, messages: List[Dict]) -> str:
        """Assess business impact from messages"""
        
        impact_indicators = []
        
        for msg in messages:
            text = msg.get('original_text', '').lower()
            if 'customer' in text and '%' in text:
                impact_indicators.append("customer impact detected")
            elif 'outage' in text:
                impact_indicators.append("service outage")
            elif 'degraded' in text:
                impact_indicators.append("service degradation")
        
        return ', '.join(impact_indicators) if impact_indicators else None


def main():
    """Test the summary generator"""
    
    if not os.getenv('ANTHROPIC_VERTEX_PROJECT_ID'):
        print("Error: ANTHROPIC_VERTEX_PROJECT_ID environment variable not set")
        return
    
    # Load previous analysis results
    try:
        with open('incident_analysis.json', 'r') as f:
            analysis_results = json.load(f)
    except FileNotFoundError:
        print("Error: incident_analysis.json not found. Run batch_analyzer.py first.")
        return
    
    print("Enhanced Incident Summary Generator")
    print("=" * 60)
    
    # Generate comprehensive summary
    summary_generator = IncidentSummaryGenerator()
    comprehensive_summary = summary_generator.generate_comprehensive_summary(analysis_results)
    
    # Display results
    print("\n📋 EXECUTIVE SUMMARY")
    print("-" * 40)
    print(comprehensive_summary['executive_summary'])
    
    print(f"\n📊 INCIDENT OVERVIEW")
    print("-" * 40)
    overview = comprehensive_summary['incident_overview']
    print(f"Status: {overview['incident_status']}")
    print(f"Total Messages: {overview['total_messages_analyzed']}")
    print(f"Significant Events: {overview['significant_events']}")
    print(f"Categories: {overview['categories_detected']}")
    
    print(f"\n🎯 ACTION ITEMS ({len(comprehensive_summary['action_items'])} total)")
    print("-" * 40)
    for item in comprehensive_summary['action_items']:
        status_icon = "✅" if item['status'] == 'completed' else "⏳" if item['status'] == 'pending' else "💡"
        print(f"  {status_icon} [{item['type'].upper()}] {item['description']}")
    
    print(f"\n📈 IMPACT ASSESSMENT")
    print("-" * 40)
    impact = comprehensive_summary['impact_assessment']
    print(f"Severity: {impact['severity']}")
    print(f"Customer Impact: {impact['customer_impact']}")
    print(f"Duration: {impact['duration']}")
    
    print(f"\n🧠 AI INSIGHTS")
    print("-" * 40)
    print(comprehensive_summary['ai_insights'])
    
    print(f"\n⏰ TECHNICAL TIMELINE")
    print("-" * 40)
    for event in comprehensive_summary['technical_timeline']:
        timestamp = event['timestamp'][:16] if event['timestamp'] else 'Unknown'
        print(f"  [{timestamp}] {event['user']}: [{event['category']}] {event['event']}")
    
    # Export comprehensive summary
    with open('incident_comprehensive_summary.json', 'w') as f:
        json.dump(comprehensive_summary, f, indent=2)
    
    print(f"\n💾 Comprehensive summary exported to 'incident_comprehensive_summary.json'")

if __name__ == "__main__":
    main()
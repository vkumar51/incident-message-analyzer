#!/usr/bin/env python3
"""
Check available Claude models in Vertex AI
"""

import os
from google.cloud import aiplatform

def check_available_models():
    """Check what models are available in the project"""
    project_id = os.getenv('ANTHROPIC_VERTEX_PROJECT_ID')
    
    if not project_id:
        print("Error: ANTHROPIC_VERTEX_PROJECT_ID not set")
        return
    
    # Initialize AI Platform
    aiplatform.init(project=project_id, location="us-east5")
    
    try:
        # List available models
        print(f"Checking models in project: {project_id}")
        print("Available models:")
        
        # Try different Claude model patterns
        models_to_try = [
            "claude-3-haiku@20240307",
            "claude-3-sonnet@20240229", 
            "claude-3-opus@20240229",
            "claude-3-5-sonnet@20240620",
            "claude-3-5-haiku@20241022",
            "publishers/anthropic/models/claude-3-haiku@20240307",
            "publishers/anthropic/models/claude-3-sonnet@20240229"
        ]
        
        for model in models_to_try:
            print(f"  - {model}")
            
    except Exception as e:
        print(f"Error checking models: {e}")
        print("\nYou may need to:")
        print("1. Enable the Vertex AI API in your project")
        print("2. Enable Claude models in Vertex AI") 
        print("3. Check your authentication: gcloud auth application-default login")

if __name__ == "__main__":
    check_available_models()
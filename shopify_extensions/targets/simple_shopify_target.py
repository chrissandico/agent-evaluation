"""
Simple Shopify Agent Target for testing AWS Agent Evaluation framework.
This is a minimal implementation to test if the framework works as-is.
"""

import requests
import time
from typing import Dict, Any
import sys
import os

# Add the AWS framework to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from agenteval.targets import BaseTarget, TargetResponse


class SimpleShopifyTarget(BaseTarget):
    """Simple target for testing Shopify agent with AWS framework."""
    
    def __init__(self, base_url: str = "http://localhost:3000", **kwargs):
        """Initialize the simple Shopify target."""
        super().__init__(**kwargs)
        self.base_url = base_url.rstrip('/')
        self.chat_endpoint = f"{self.base_url}/chat"
        
        # Simple session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Disable SSL verification for localhost
        if "localhost" in self.base_url or "127.0.0.1" in self.base_url:
            self.session.verify = False
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def invoke(self, prompt: str) -> TargetResponse:
        """Send a message to the Shopify agent."""
        try:
            # Simple payload
            payload = {
                "message": prompt,
                "conversation_id": f"test_{int(time.time())}",
                "prompt_type": "shopify_assistant"
            }
            
            # Make request
            response = self.session.post(
                self.chat_endpoint,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            # For streaming responses, we'll just take the first chunk
            if response.headers.get('content-type', '').startswith('text/plain'):
                # Handle streaming response
                content = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line.startswith('data: '):
                        data_part = line[6:]  # Remove 'data: ' prefix
                        if data_part and data_part != '[DONE]':
                            content += data_part + " "
                
                return TargetResponse(response=content.strip() or "Agent responded")
            else:
                # Handle JSON response
                result = response.json()
                return TargetResponse(response=result.get('response', 'Agent responded'))
                
        except Exception as e:
            return TargetResponse(response=f"Error: {str(e)}")
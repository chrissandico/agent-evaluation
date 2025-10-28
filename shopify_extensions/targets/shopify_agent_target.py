"""
Shopify Agent Target for AWS Agent Evaluation Framework

This target implementation follows AWS framework patterns exactly,
without any custom modifications or fixes.
"""

import requests
import time
import json
from typing import Dict, Any, Optional
import sys
import os

# Add the AWS framework to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from agenteval.targets import BaseTarget, TargetResponse


class ShopifyAgentTarget(BaseTarget):
    """Target for communicating with Shopify chat agent via HTTP API."""
    
    def __init__(self, 
                 base_url: str = "http://localhost:3000",
                 shop_id: str = "test-shop",
                 shop_domain: str = "https://test-shop.myshopify.com",
                 timeout: int = 30,
                 **kwargs):
        """Initialize the Shopify agent target.
        
        Args:
            base_url: Base URL of the Shopify agent
            shop_id: Shopify shop ID for testing
            shop_domain: Shopify shop domain
            timeout: Request timeout in seconds
            **kwargs: Additional arguments passed to BaseTarget
        """
        super().__init__(**kwargs)
        
        self.base_url = base_url.rstrip('/')
        self.shop_id = shop_id
        self.shop_domain = shop_domain
        self.timeout = timeout
        self.chat_endpoint = f"{self.base_url}/chat"
        
        # Initialize HTTP session
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream',  # Shopify agent returns Server-Sent Events
            'X-Shopify-Shop-Id': self.shop_id,
            'Origin': self.shop_domain
        })
        
        # Disable SSL verification for localhost development
        if "localhost" in self.base_url or "127.0.0.1" in self.base_url:
            self.session.verify = False
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Add required headers for Shopify proxy
        self.session.headers.update({
            'X-Shopify-Shop-Id': self.shop_id,
            'Origin': self.shop_domain
        })
        
        # Conversation tracking
        self.conversation_id: Optional[str] = None
    
    def invoke(self, prompt: str) -> TargetResponse:
        """Send a message to the Shopify agent and return the response.
        
        This method follows the AWS framework's TargetResponse pattern exactly.
        
        Args:
            prompt: The user message to send to the agent
            
        Returns:
            TargetResponse containing the agent's response
        """
        try:
            # Prepare request payload in Shopify agent's expected format
            payload = {
                "message": prompt,
                "conversation_id": self.conversation_id or f"eval_{int(time.time())}",
                "prompt_type": "shopify_assistant"
            }
            
            # Make HTTP request to Shopify agent
            response = self.session.post(
                self.chat_endpoint,
                json=payload,
                timeout=self.timeout,
                stream=True  # Handle streaming response
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Parse streaming response (Server-Sent Events format)
            agent_response = self._parse_streaming_response(response)
            
            # Update conversation ID for multi-turn conversations
            if not self.conversation_id:
                self.conversation_id = payload["conversation_id"]
            
            # Return response in AWS framework format
            return TargetResponse(response=agent_response)
            
        except requests.exceptions.RequestException as e:
            # Handle network/HTTP errors
            error_msg = f"HTTP error communicating with Shopify agent: {str(e)}"
            return TargetResponse(response=f"Error: {error_msg}")
            
        except Exception as e:
            # Handle any other errors
            error_msg = f"Unexpected error: {str(e)}"
            return TargetResponse(response=f"Error: {error_msg}")
    
    def _parse_streaming_response(self, response: requests.Response) -> str:
        """Parse Server-Sent Events streaming response from Shopify agent.
        
        Args:
            response: HTTP response object with streaming content
            
        Returns:
            Parsed agent response text
        """
        content_parts = []
        
        try:
            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith('data: '):
                    data_part = line[6:]  # Remove 'data: ' prefix
                    
                    # Skip empty lines and end markers
                    if not data_part or data_part == '[DONE]':
                        continue
                    
                    # Try to parse as JSON (Shopify agent sends JSON messages)
                    try:
                        data_json = json.loads(data_part)
                        
                        # Handle different message types from Shopify agent
                        if isinstance(data_json, dict):
                            if data_json.get('type') == 'chunk':
                                # Text chunk from Claude
                                content_parts.append(data_json.get('chunk', ''))
                            elif data_json.get('type') == 'id':
                                # Conversation ID - store it
                                if 'conversation_id' in data_json:
                                    self.conversation_id = data_json['conversation_id']
                            elif data_json.get('type') == 'tool_use':
                                # Tool usage message
                                tool_msg = data_json.get('tool_use_message', '')
                                content_parts.append(f"\n[{tool_msg}]\n")
                            elif data_json.get('type') == 'product_results':
                                # Product results
                                products = data_json.get('products', [])
                                if products:
                                    content_parts.append(f"\n[Found {len(products)} products]\n")
                        
                    except json.JSONDecodeError:
                        # If not JSON, treat as plain text
                        content_parts.append(data_part)
            
            # Join all content parts
            full_response = ''.join(content_parts).strip()
            
            # Return the response or a default message if empty
            return full_response if full_response else "Agent responded successfully"
            
        except Exception as e:
            return f"Error parsing response: {str(e)}"
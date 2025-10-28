#!/usr/bin/env python3
"""
Test the live Shopify agent with various scenarios.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shopify_extensions'))

from shopify_extensions.targets.shopify_agent_target import ShopifyAgentTarget

def test_live_agent():
    """Test the live Shopify agent with various scenarios."""
    print("Testing Live Shopify Agent")
    print("=" * 40)
    
    # Create target pointing to your running agent
    target = ShopifyAgentTarget(base_url="https://localhost:3458")
    
    test_cases = [
        "Hello, I need help",
        "Do you have any products?",
        "What's your return policy?",
        "I'm looking for a blue sweater"
    ]
    
    for i, test_message in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_message}")
        print("-" * 30)
        
        try:
            response = target.invoke(test_message)
            print(f"Response: {response.response}")
            
            # Check if response contains error
            if "Error" in response.response:
                print("⚠️  Agent returned an error")
            else:
                print("✅ Agent responded successfully")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n" + "=" * 40)
    print("Live agent testing complete!")

if __name__ == "__main__":
    test_live_agent()
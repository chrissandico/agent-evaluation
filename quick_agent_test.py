#!/usr/bin/env python3
"""
Quick test to check if agent is accessible.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shopify_extensions'))

from shopify_extensions.targets.shopify_agent_target import ShopifyAgentTarget

print("🧪 Quick Agent Test")
print("=" * 40)

# Test the configured port
print("\n1. Testing configured port (64085)...")
try:
    target = ShopifyAgentTarget(base_url='http://localhost:64085')
    response = target.invoke('Hello')
    
    if "Error" in response.response and "connection" in response.response.lower():
        print("   ❌ Agent not responding on port 64085")
        print("   💡 Your Shopify app may have restarted on a different port")
        print("\n   Please check your terminal where you ran 'npm run dev'")
        print("   Look for the line: ➜  Local:   http://localhost:XXXXX/")
        print("   Then update the port in agenteval.yml")
    else:
        print("   ✅ Agent is responding!")
        print(f"   Response: {response.response[:100]}...")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 40)
print("To update the port:")
print("1. Check your Shopify app terminal for the port number")
print("2. Edit shopify-agent-evaluation/agenteval.yml")
print("3. Change base_url to: http://localhost:YOUR_PORT")
print("4. Run tests again")
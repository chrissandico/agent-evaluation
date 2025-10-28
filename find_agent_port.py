#!/usr/bin/env python3
"""
Find which port the Shopify agent is running on.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shopify_extensions'))

from shopify_extensions.targets.shopify_agent_target import ShopifyAgentTarget

print("🔍 Scanning for Shopify agent...")
print("=" * 40)

# Common ports to check
ports_to_check = [3000, 3458, 61704, 64085, 5000, 8000, 8080, 9000]

# Also check dynamic port range that Remix uses
for port in range(60000, 65000, 100):
    ports_to_check.append(port)

found_port = None

for port in ports_to_check:
    try:
        target = ShopifyAgentTarget(base_url=f'http://localhost:{port}')
        response = target.invoke('test')
        
        if "Error" not in response.response or "connection" not in response.response.lower():
            print(f"✅ Found agent on port {port}!")
            print(f"   Response: {response.response[:100]}...")
            found_port = port
            break
    except:
        pass

if found_port:
    print(f"\n🎯 Update your config files to use port {found_port}")
else:
    print("\n❌ Could not find running agent")
    print("   Make sure your Shopify app is running with: npm run dev")
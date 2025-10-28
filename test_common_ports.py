#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shopify_extensions'))
from shopify_extensions.targets.shopify_agent_target import ShopifyAgentTarget

print("Testing common Remix ports...")
common_ports = [3000, 5173, 8080, 61704, 62000, 63000, 64000, 64085, 65000]

for port in common_ports:
    try:
        target = ShopifyAgentTarget(base_url=f'http://localhost:{port}')
        response = target.invoke('test')
        if 'Hi' in response.response or 'hello' in response.response.lower():
            print(f'✅ FOUND IT! Port {port}')
            print(f'Response: {response.response[:100]}')
            break
        elif 'Error' not in response.response:
            print(f'? Port {port} responded but unclear: {response.response[:50]}')
    except:
        pass
else:
    print('❌ Could not find Remix port')
    print('\nPlease check your terminal where shopify app dev is running')
    print('Look for a line like: ➜  Local:   http://localhost:XXXXX/')
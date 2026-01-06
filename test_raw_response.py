"""
Test to see the raw response from the agent
"""

import requests
import json

agent_url = "http://localhost:54597/chat"
conversation_id = "test-raw-001"
shop_domain = "https://theprofmeta-dev.myshopify.com"
shop_id = "test-shop-id"

payload = {
    "message": "Hello, can you help me?",
    "conversation_id": conversation_id
}

headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream",
    "Origin": shop_domain,
    "X-Shopify-Shop-Id": shop_id
}

print("Sending request...")
print(f"URL: {agent_url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print()

response = requests.post(
    agent_url,
    json=payload,
    headers=headers,
    timeout=30,
    stream=True
)

print(f"Status Code: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print()
print("=" * 70)
print("RAW RESPONSE:")
print("=" * 70)

line_count = 0
for line in response.iter_lines():
    if not line:
        print("[empty line]")
        continue
    
    line_count += 1
    line_str = line.decode('utf-8')
    print(f"Line {line_count}: {line_str}")
    
    if line_count > 50:  # Limit output
        print("... (truncated)")
        break

print()
print("=" * 70)
print(f"Total lines: {line_count}")

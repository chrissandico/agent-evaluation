"""
Basic connection test for Shopify Agent Evaluation Framework
Tests that the framework can connect to the running agent and execute a simple query.
"""

import sys
import requests
import json


def send_message(agent_url: str, message: str, conversation_id: str, shop_domain: str, shop_id: str) -> dict:
    """Send a message to the agent and return the response."""
    payload = {
        "message": message,
        "conversation_id": conversation_id
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Origin": shop_domain,
        "X-Shopify-Shop-Id": shop_id
    }
    
    try:
        response = requests.post(
            agent_url,
            json=payload,
            headers=headers,
            timeout=30,
            stream=True
        )
        
        if response.status_code != 200:
            return {
                "status": "error",
                "message": f"HTTP {response.status_code}: {response.text}",
                "tools_used": []
            }
        
        # Parse SSE stream
        full_message = ""
        tools_used = []
        
        for line in response.iter_lines():
            if not line:
                continue
                
            line = line.decode('utf-8')
            if not line.startswith('data: '):
                continue
                
            data_str = line[6:]  # Remove 'data: ' prefix
            
            try:
                data = json.loads(data_str)
                
                if data.get('type') == 'chunk':
                    full_message += data.get('chunk', '')
                elif data.get('type') == 'tool_use':
                    tool_msg = data.get('tool_use_message', '')
                    # Extract tool name from message like "Calling tool: search_shop_catalog with arguments: ..."
                    if 'Calling tool:' in tool_msg:
                        tool_name = tool_msg.split('Calling tool:')[1].split('with')[0].strip()
                        if tool_name not in tools_used:
                            tools_used.append(tool_name)
                elif data.get('type') == 'end_turn':
                    break
                    
            except json.JSONDecodeError:
                continue
        
        return {
            "status": "success",
            "message": full_message,
            "tools_used": tools_used
        }
        
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "Request timed out",
            "tools_used": []
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "Could not connect to agent. Is it running?",
            "tools_used": []
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
            "tools_used": []
        }


def test_basic_connection():
    """Test basic connection to the Shopify agent."""
    
    print("=" * 70)
    print("BASIC CONNECTION TEST")
    print("=" * 70)
    print()
    
    # Configuration
    agent_url = "http://localhost:54597/chat"  # Update this if your port is different
    conversation_id = "test-connection-001"
    shop_domain = "https://theprofmeta-dev.myshopify.com"
    shop_id = "test-shop-id"
    
    print(f"Agent URL: {agent_url}")
    print(f"Conversation ID: {conversation_id}")
    print(f"Shop Domain: {shop_domain}")
    print()
    
    # Test 1: Simple greeting
    print("-" * 70)
    print("TEST 1: Simple Greeting")
    print("-" * 70)
    
    test_message = "Hello, can you help me?"
    print(f"Sending: '{test_message}'")
    print()
    
    try:
        response = send_message(agent_url, test_message, conversation_id, shop_domain, shop_id)
        
        print("Response received:")
        print(f"  Status: {response.get('status', 'unknown')}")
        print(f"  Message length: {len(response.get('message', ''))} characters")
        print(f"  Tools used: {len(response.get('tools_used', []))}")
        print()
        print("Message preview:")
        message = response.get('message', '')
        preview = message[:200] + "..." if len(message) > 200 else message
        print(f"  {preview}")
        print()
        
        if response.get('status') == 'success':
            print("✅ TEST 1 PASSED: Agent responded successfully")
        else:
            print("❌ TEST 1 FAILED: Agent did not respond successfully")
            print(f"   Error: {response.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ TEST 1 FAILED: Error - {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    
    # Test 2: Tool usage (product search)
    print("-" * 70)
    print("TEST 2: Tool Usage (Product Search)")
    print("-" * 70)
    
    test_message = "Search for snowboards"
    print(f"Sending: '{test_message}'")
    print()
    
    try:
        response = send_message(agent_url, test_message, conversation_id, shop_domain, shop_id)
        
        print("Response received:")
        print(f"  Status: {response.get('status', 'unknown')}")
        print(f"  Message length: {len(response.get('message', ''))} characters")
        print(f"  Tools used: {response.get('tools_used', [])}")
        print()
        
        if response.get('tools_used'):
            print("✅ TEST 2 PASSED: Agent used tools")
            print(f"   Tools: {', '.join(response.get('tools_used', []))}")
        else:
            print("⚠️  TEST 2 WARNING: Agent responded but didn't use tools")
            print("   This might be expected if no products match")
            
    except Exception as e:
        print(f"❌ TEST 2 FAILED: Error - {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    
    # Test 3: One Piece Card search (if enabled)
    print("-" * 70)
    print("TEST 3: One Piece Card Search (Custom Tool)")
    print("-" * 70)
    
    test_message = "Show me card OP01-060"
    print(f"Sending: '{test_message}'")
    print()
    
    try:
        response = send_message(agent_url, test_message, conversation_id, shop_domain, shop_id)
        
        print("Response received:")
        print(f"  Status: {response.get('status', 'unknown')}")
        print(f"  Message length: {len(response.get('message', ''))} characters")
        print(f"  Tools used: {response.get('tools_used', [])}")
        print()
        
        if 'search_one_piece_cards' in response.get('tools_used', []):
            print("✅ TEST 3 PASSED: Custom tool (search_one_piece_cards) was used")
        else:
            print("⚠️  TEST 3 WARNING: Custom tool not used")
            print("   This might be expected if the tool is disabled")
            
    except Exception as e:
        print(f"❌ TEST 3 FAILED: Error - {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("=" * 70)
    print("BASIC CONNECTION TEST COMPLETE")
    print("=" * 70)
    print()
    print("✅ All tests completed successfully!")
    print()
    print("Next steps:")
    print("  1. Review the responses above")
    print("  2. Verify the agent is responding as expected")
    print("  3. Run full evaluation suite if basic tests pass")
    print()
    
    return True


def main():
    """Main entry point."""
    try:
        success = test_basic_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print()
    print("Starting basic connection test...")
    print("Make sure the Shopify agent is running on http://localhost:54597")
    print()
    
    main()

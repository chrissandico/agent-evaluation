# Shopify Agent Evaluation Setup

This project is configured to test a Shopify conversational agent using the AWS Agent Evaluation framework.

## Current Setup Status

✅ **Python 3.12.4** - Compatible with agent-evaluation
✅ **agent-evaluation 0.4.1** - Installed and working
✅ **AWS credentials** - Configured (us-east-1 region)
✅ **All dependencies** - Installed (boto3, pydantic, rich, jinja2, etc.)
✅ **Shopify target** - Implemented at `shopify_extensions/targets/shopify_agent_target.py`
✅ **Test configuration** - `agenteval.yml` configured for Shopify agent
✅ **CLI working** - `agenteval` command available

## Prerequisites to Run Tests

### 1. Start the Shopify Agent

The Shopify agent must be running before tests can execute:

```bash
cd shop-chat-agent
shopify app dev
```

The agent will be accessible at: `https://localhost:3458` (stable proxy port)

### 2. Verify Agent is Running

Check if the agent is accessible:

```bash
# Windows PowerShell
Test-NetConnection -ComputerName localhost -Port 3458

# Or use Python test script
python test_basic_connection.py
```

### 3. Run Evaluation Tests

Once the agent is running:

```bash
# Simple test
agenteval run agenteval.yml

# Or use Python scripts
python simple_final_test.py
python test_live_agent.py
```

## Configuration Files

### Main Configuration: `agenteval.yml`

```yaml
evaluator:
  model: claude-3  # Uses AWS Bedrock

target:
  type: shopify_extensions.targets.shopify_agent_target.ShopifyAgentTarget
  base_url: https://localhost:3458  # Stable proxy port
  shop_id: test-shop
  shop_domain: https://theprofmeta-dev.myshopify.com
  timeout: 30
```

### Additional Test Suites

Located in `shopify_extensions/configs/`:
- `simple_test.yml` - Basic greeting test
- `customer_service_scenarios.yml` - Customer service tests
- `product_search_scenarios.yml` - Product search tests
- `order_management_scenarios.yml` - Order handling tests
- `edge_cases_scenarios.yml` - Edge case testing
- `multi_turn_scenarios.yml` - Multi-turn conversations

## Shopify Target Implementation

The custom target at `shopify_extensions/targets/shopify_agent_target.py`:
- Extends `BaseTarget` from agent-evaluation framework
- Handles HTTP communication with Shopify agent
- Parses Server-Sent Events (SSE) streaming responses
- Maintains conversation context across turns
- Handles tool usage and product results

## Common Issues

### Agent Not Running
**Error**: Connection refused on port 3458
**Solution**: Start the Shopify agent with `shopify app dev`

### AWS Credentials
**Error**: Unable to locate credentials
**Solution**: Run `aws configure` or set AWS environment variables

### Import Errors
**Error**: Cannot import ShopifyAgentTarget
**Solution**: Ensure you're in the project root directory

## Testing Workflow

1. Start Shopify agent (`shopify app dev`)
2. Verify agent is accessible (port 3458)
3. Run evaluation: `agenteval run agenteval.yml`
4. Review results in terminal output
5. Check AWS Bedrock costs in AWS Cost Explorer

## Key Points

- **Port 3458** is the stable proxy port (won't change)
- **AWS Bedrock** is used for the evaluator (Claude model)
- **Anthropic API** is used by the Shopify agent itself
- Tests simulate real user conversations
- Multi-turn conversations maintain context
- Results show pass/fail for expected outcomes

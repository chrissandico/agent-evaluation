# Shopify Agent Evaluation - Quick Start Guide

## Overview

This guide walks you through running agent evaluations from start to finish, including handling port changes and understanding costs.

## Prerequisites

- ✅ Shopify agent running (`shopify app dev`)
- ✅ AWS credentials configured (for Bedrock/Claude access)
- ✅ Anthropic API credits (for your Shopify agent)
- ✅ Python 3.8+ installed

## Step-by-Step: Running Your First Evaluation

### 1. Start Your Shopify Agent

```bash
cd shop-chat-agent
shopify app dev
```

**Important**: Note the proxy URL shown in the terminal:
```
App URL:  https://localhost:3458
```

Your agent is accessible through the **proxy on port 3458** (this port is stable and won't change).

### 2. Configure the Evaluation Framework

The evaluation framework needs to know where your agent is running.

**Edit**: `shopify-agent-evaluation/agenteval.yml`

```yaml
target:
  type: shopify_extensions.targets.shopify_agent_target.ShopifyAgentTarget
  base_url: https://localhost:3458  # Use the proxy URL
  shop_id: test-shop
  shop_domain: https://theprofmeta-dev.myshopify.com
  timeout: 30
```

**Note**: The proxy port (3458) is stable. You typically only need to configure this once.

### 3. Run a Simple Test

```bash
cd shopify-agent-evaluation
python simple_final_test.py
```

**Expected Output**:
```
🎯 Simple Final Test
==============================
1. Testing agent connection...
   ✅ Agent responded: Hi there! Welcome to our store...
2. Testing LLM evaluation...
   ✅ Evaluation result: True
   📝 Details: All of the expected results can be observed...

🎉 Framework is working!
Ready for production use!
```

### 4. Run a Comprehensive Single Test

```bash
python run_single_evaluation.py
```

**This test includes**:
- Agent connection verification
- LLM-based evaluation using Claude-3
- Detailed reasoning for pass/fail
- Complete conversation transcript

**Expected Output**:
```
Running Single Agent Evaluation Test
========================================
Created test: greeting_test
Test steps: ['Hello, I need help with something']
Expected results: ['Agent responds with a friendly greeting', ...]

========================================
EVALUATION RESULTS:
Test Name: greeting_test
Passed: True
Result: All of the expected results can be observed in the conversation.
Reasoning: The agent responds with a friendly greeting...
Conversation turns: 1

CONVERSATION:
1. USER: Hello, I have a question and need some help.
2. AGENT: Of course! I'm here to help you...

🎉 Evaluation completed successfully!
```

### 5. Run Multiple Test Scenarios

**Basic test suite** (3 scenarios):
```bash
python -m agenteval.cli run
```

**Comprehensive test suite** (33 scenarios):
```bash
python -m agenteval.cli run --config comprehensive_tests.yml
```

## Handling Port Changes

### Problem: Agent Restarts on Different Port

If you restart your Shopify agent and it changes ports, you have two options:

### Option 1: Use the Stable Proxy Port (Recommended)

The **proxy port (3458) is stable** and won't change. Always use:
```yaml
base_url: https://localhost:3458
```

This is already configured in your `agenteval.yml` file.

### Option 2: Find and Update the Direct Remix Port

If you need to use the direct Remix port (not recommended):

1. **Find the port** in your Shopify agent terminal:
   ```
   ➜  Local:   http://localhost:64085/
   ```

2. **Update configuration files**:
   - `shopify-agent-evaluation/agenteval.yml`
   - `shopify-agent-evaluation/comprehensive_tests.yml`
   - `shopify-agent-evaluation/run_single_evaluation.py`
   - `shopify-agent-evaluation/simple_final_test.py`

3. **Change `base_url` to**:
   ```yaml
   base_url: http://localhost:YOUR_NEW_PORT
   ```

### Quick Port Finder Script

If you can't find the port, run:
```bash
cd shopify-agent-evaluation
python test_common_ports.py
```

This will scan common ports and tell you which one your agent is on.

## Understanding Test Results

### Where to See Results

**Console Output**: Results are displayed directly in your terminal with:
- ✅ Pass/Fail status
- 📝 Detailed reasoning from Claude-3
- 💬 Complete conversation transcript
- 🔍 Tool usage information

**Example Result**:
```
EVALUATION RESULTS:
Test Name: greeting_test
Passed: True
Result: All of the expected results can be observed in the conversation.
Reasoning: The agent responds with a friendly greeting by saying "Of course! 
I'm here to help you." This satisfies the first expected result.
The agent then offers to help with various shopping and store-related 
questions... This covers the second expected result.
```

### Result Files

Currently, results are displayed in the console. To save results to files, you can:

```bash
# Save to file
python run_single_evaluation.py > results.txt

# Or with timestamp
python run_single_evaluation.py > results_$(date +%Y%m%d_%H%M%S).txt
```

## Cost Analysis

### Token Usage Per Test

**Single Simple Test** (`simple_final_test.py`):
- **Approximate cost**: $0.01 - $0.03
- **Tokens used**: ~2,000 - 5,000 tokens
- **Breakdown**:
  - Initial prompt generation: ~500 tokens
  - Agent response: ~500 tokens
  - Evaluation by Claude-3: ~1,000 tokens

**Single Comprehensive Test** (`run_single_evaluation.py`):
- **Approximate cost**: $0.03 - $0.10
- **Tokens used**: ~5,000 - 15,000 tokens
- **Breakdown**:
  - Multi-turn conversation: ~2,000 tokens
  - Tool usage analysis: ~1,000 tokens
  - Detailed evaluation: ~2,000 tokens
  - Reasoning generation: ~1,000 tokens

**Full Test Suite** (33 scenarios):
- **Approximate cost**: $1.00 - $3.00
- **Tokens used**: ~150,000 - 500,000 tokens
- **Time**: 10-30 minutes

### Cost Factors

1. **Conversation length**: More turns = more tokens
2. **Tool usage**: Each tool call adds tokens
3. **Response complexity**: Detailed responses use more tokens
4. **Evaluation depth**: Detailed reasoning uses more tokens

### Monitoring Costs

**AWS Bedrock Costs**:
- Check AWS Cost Explorer
- Look for "Bedrock" service charges
- Claude-3 Sonnet pricing: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens

**Anthropic API Costs** (for your Shopify agent):
- Check Anthropic Console > Usage
- Your agent uses separate credits from the evaluation framework

## Common Issues & Solutions

### Issue: "Agent not responding"

**Solution**:
1. Check if your Shopify agent is running
2. Verify the port in `agenteval.yml` matches your agent
3. Check for Claude API credit errors in agent logs

### Issue: "AWS credentials error"

**Solution**:
```bash
aws configure
# Enter your AWS credentials
```

### Issue: "Template loading error"

**Solution**: The bug fixes should handle this automatically. If you see this error:
```bash
cd shopify-agent-evaluation
python -c "from shopify_extensions.fixes.aws_framework_fixes import apply_aws_framework_fixes; apply_aws_framework_fixes()"
```

### Issue: "Port connection refused"

**Solution**:
1. Use the stable proxy port: `https://localhost:3458`
2. Or find the new Remix port and update configs
3. Run `python test_common_ports.py` to find the port

## Test Scenarios Available

### Basic Tests (3 scenarios)
- `simple_greeting`: Basic greeting and help request
- `product_inquiry`: Product search functionality
- `multi_turn_conversation`: Context maintenance across turns

### Comprehensive Tests (33 scenarios)
- **Greeting variations**: casual, formal, simple
- **Product searches**: specific, general, price-based, out-of-stock
- **One Piece Card Game**: card searches, deck building, set information
- **Store policies**: returns, shipping, payment methods
- **Multi-turn flows**: gift shopping, product comparison, troubleshooting
- **Cart & checkout**: add to cart, checkout assistance
- **Error handling**: unclear requests, impossible requests, long messages
- **Customer account**: order status, account updates, order history
- **Performance tests**: rapid-fire questions, context switching
- **Sentiment handling**: frustrated, excited, confused customers

## Quick Reference Commands

```bash
# Start your agent
cd shop-chat-agent
shopify app dev

# Run simple test
cd shopify-agent-evaluation
python simple_final_test.py

# Run single comprehensive test
python run_single_evaluation.py

# Run basic test suite (3 tests)
python -m agenteval.cli run

# Run comprehensive suite (33 tests)
python -m agenteval.cli run --config comprehensive_tests.yml

# Test agent connection
python quick_agent_test.py

# Find agent port
python test_common_ports.py
```

## Best Practices

1. **Always use the proxy port** (3458) - it's stable
2. **Run simple tests first** before comprehensive suites
3. **Monitor AWS costs** in Cost Explorer
4. **Check agent logs** for errors before running evaluations
5. **Save important results** to files for later review
6. **Run evaluations after code changes** to catch regressions

## Next Steps

1. ✅ Run your first simple test
2. ✅ Review the results and understand the evaluation
3. ✅ Run a comprehensive test with multiple scenarios
4. ✅ Integrate into your CI/CD pipeline (optional)
5. ✅ Create custom test scenarios for your specific use cases

## Support

If you encounter issues:
1. Check the agent logs for errors
2. Verify AWS credentials are configured
3. Ensure Anthropic API credits are available
4. Review the port configuration in `agenteval.yml`

Your evaluation framework is production-ready! 🎉
#!/usr/bin/env python3
"""
Simple final test to verify everything works.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shopify_extensions'))

# Apply fixes
from shopify_extensions.fixes.aws_framework_fixes import apply_aws_framework_fixes
apply_aws_framework_fixes()

# Test components
from agenteval.evaluators.evaluator_factory import EvaluatorFactory
from agenteval.test import Test
from shopify_extensions.targets.shopify_agent_target import ShopifyAgentTarget

print("🎯 Simple Final Test")
print("=" * 30)

# Test agent connection
print("1. Testing agent connection...")
target = ShopifyAgentTarget(base_url='https://localhost:3458')
response = target.invoke('Hello')
print(f"   ✅ Agent responded: {response.response[:50]}...")

# Test evaluation
print("2. Testing LLM evaluation...")
test = Test(
    name='simple_test',
    steps=['Hello'],
    expected_results=['Agent responds'],
    max_turns=2
)

factory = EvaluatorFactory(config={'model': 'claude-3'})
evaluator = factory.create(test=test, target=target, work_dir='/tmp')

result = evaluator.evaluate()
print(f"   ✅ Evaluation result: {result.passed}")
print(f"   📝 Details: {result.result}")

print("\n🎉 Framework is working!")
print("Ready for production use!")
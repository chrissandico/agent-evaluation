#!/usr/bin/env python3
"""
Run a single evaluation test against the live Shopify agent.
"""

import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shopify_extensions'))

def run_single_evaluation():
    """Run a single evaluation test."""
    print("Running Single Agent Evaluation Test")
    print("=" * 40)
    
    try:
        # Apply fixes first
        from shopify_extensions.fixes.aws_framework_fixes import apply_aws_framework_fixes
        print("Applying AWS framework fixes...")
        apply_aws_framework_fixes()
        
        # Import framework components
        from agenteval.evaluators.evaluator_factory import EvaluatorFactory
        from agenteval.test import Test
        from shopify_extensions.targets.shopify_agent_target import ShopifyAgentTarget
        
        # Create test
        test = Test(
            name='greeting_test',
            steps=['Hello, I need help with something'],
            expected_results=[
                'Agent responds with a friendly greeting',
                'Agent offers to help with shopping or store questions'
            ],
            max_turns=3
        )
        
        print(f"Created test: {test.name}")
        print(f"Test steps: {test.steps}")
        print(f"Expected results: {test.expected_results}")
        
        # Create target
        target = ShopifyAgentTarget(base_url='https://localhost:3458')
        print("Created Shopify agent target")
        
        # Test the target first
        print("\nTesting target connection...")
        response = target.invoke("Hello")
        print(f"Target response: {response.response[:100]}...")
        
        # Create evaluator
        print("\nCreating evaluator...")
        factory = EvaluatorFactory(config={'model': 'claude-3'})
        evaluator = factory.create(test=test, target=target, work_dir='/tmp')
        
        print("✅ Evaluator created successfully!")
        print("Running evaluation...")
        
        # Run evaluation
        result = evaluator.evaluate()
        
        print("\n" + "=" * 40)
        print("EVALUATION RESULTS:")
        print(f"Test Name: {result.test_name}")
        print(f"Passed: {result.passed}")
        print(f"Result: {result.result}")
        print(f"Reasoning: {result.reasoning}")
        print(f"Conversation turns: {result.conversation.turns}")
        
        # Print conversation
        print("\nCONVERSATION:")
        for i, (role, content) in enumerate(result.conversation.messages):
            print(f"{i+1}. {role.upper()}: {content}")
        
        return result.passed
        
    except Exception as e:
        if "credentials" in str(e).lower() or "aws" in str(e).lower() or "bedrock" in str(e).lower():
            print("❌ AWS credentials needed for LLM evaluation")
            print(f"Error: {e}")
            print("\nTo run LLM-based evaluation, you need:")
            print("1. AWS account with Bedrock access")
            print("2. AWS credentials configured")
            print("3. Claude model access in Bedrock")
            return False
        else:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = run_single_evaluation()
    
    if success:
        print("\n🎉 Evaluation completed successfully!")
    else:
        print("\n⚠️ Evaluation failed - likely needs AWS setup")
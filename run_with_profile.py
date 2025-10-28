#!/usr/bin/env python3
"""
Run agent evaluation with a specific AWS profile.
"""

import os
import sys

def run_with_aws_profile(profile_name="default"):
    """Run evaluation with specific AWS profile."""
    
    # Set AWS profile environment variable
    os.environ['AWS_PROFILE'] = profile_name
    
    print(f"🔐 Using AWS Profile: {profile_name}")
    
    # Verify the profile works
    import subprocess
    try:
        result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            import json
            identity = json.loads(result.stdout)
            print(f"✅ Account: {identity['Account']}")
            print(f"✅ User: {identity['Arn'].split('/')[-1]}")
        else:
            print(f"❌ Error with profile {profile_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking AWS profile: {e}")
        return False
    
    # Add paths for evaluation framework
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shopify_extensions'))
    
    # Apply fixes and run evaluation
    from shopify_extensions.fixes.aws_framework_fixes import apply_aws_framework_fixes
    apply_aws_framework_fixes()
    
    from agenteval.evaluators.evaluator_factory import EvaluatorFactory
    from agenteval.test import Test
    from shopify_extensions.targets.shopify_agent_target import ShopifyAgentTarget
    
    # Create and run test
    test = Test(
        name='profile_test',
        steps=['Hello, I need help'],
        expected_results=['Agent responds helpfully'],
        max_turns=3
    )
    
    target = ShopifyAgentTarget(base_url='http://localhost:61704')
    factory = EvaluatorFactory(config={'model': 'claude-3'})
    evaluator = factory.create(test=test, target=target, work_dir='/tmp')
    
    print("🚀 Running evaluation...")
    result = evaluator.evaluate()
    
    print(f"\n✅ Test Result: {result.passed}")
    print(f"📝 Reasoning: {result.reasoning}")
    
    return True

if __name__ == "__main__":
    # You can specify a different profile here
    profile = sys.argv[1] if len(sys.argv) > 1 else "default"
    
    print(f"Running agent evaluation with AWS profile: {profile}")
    success = run_with_aws_profile(profile)
    
    if not success:
        print("\n💡 To create a new AWS profile:")
        print("aws configure --profile my-new-profile")
        sys.exit(1)
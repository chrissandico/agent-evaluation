#!/usr/bin/env python3
"""
Run AWS Agent Evaluation with bug fixes applied.
This script applies the necessary fixes and then runs the evaluation.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shopify_extensions'))

def main():
    """Apply fixes and run evaluation."""
    print("AWS Agent Evaluation with Bug Fixes")
    print("=" * 40)
    
    # Apply bug fixes first
    print("Applying AWS framework bug fixes...")
    try:
        from shopify_extensions.fixes.aws_framework_fixes import apply_aws_framework_fixes
        
        if apply_aws_framework_fixes():
            print("✅ Bug fixes applied successfully")
        else:
            print("❌ Failed to apply bug fixes")
            return 1
    except Exception as e:
        print(f"❌ Error applying bug fixes: {e}")
        return 1
    
    # Now run the AWS CLI
    print("\nRunning AWS Agent Evaluation...")
    try:
        from agenteval.cli import main as cli_main
        
        # Set up sys.argv for the CLI
        sys.argv = ['agenteval', 'run']
        
        # Run the CLI
        cli_main()
        
    except Exception as e:
        if "credentials" in str(e).lower() or "aws" in str(e).lower() or "bedrock" in str(e).lower():
            print("\n⚠️  AWS credentials needed for evaluation")
            print("Please configure AWS credentials with Bedrock access:")
            print("  aws configure")
            print("  # or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
            return 0
        else:
            print(f"\n❌ Error running evaluation: {e}")
            return 1

if __name__ == "__main__":
    sys.exit(main())
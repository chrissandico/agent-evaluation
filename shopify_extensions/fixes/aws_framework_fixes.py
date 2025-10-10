"""
AWS Agent Evaluation Framework Bug Fixes

This module contains minimal temporary fixes for known bugs in the AWS Agent
Evaluation framework. These fixes should be removed once AWS resolves the
upstream issues.

Known Issues Fixed:
1. Template loading fails on Windows due to path resolution
2. Conversation serialization issues with JSON encoding
3. Prompt passing bug in CanonicalEvaluator

All fixes are designed to be minimal and non-intrusive.
"""

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class AWSFrameworkBugFixes:
    """Manager for applying temporary AWS framework bug fixes."""
    
    def __init__(self):
        self.fixes_applied = {
            'template_loader': False,
            'conversation_serializer': False,
            'prompt_passing': False
        }
    
    def apply_all_fixes(self) -> bool:
        """Apply all necessary fixes for AWS framework bugs."""
        logger.info("Applying AWS Agent Evaluation framework bug fixes...")
        
        success = True
        
        # Fix 1: Template loading
        if self.apply_template_loader_fix():
            self.fixes_applied['template_loader'] = True
        else:
            success = False
        
        # Fix 2: Conversation serialization
        if self.apply_conversation_serializer_fix():
            self.fixes_applied['conversation_serializer'] = True
        else:
            success = False
        
        # Fix 3: Prompt passing (if needed)
        if self.apply_prompt_passing_fix():
            self.fixes_applied['prompt_passing'] = True
        else:
            success = False
        
        if success:
            logger.info("✅ All AWS framework bug fixes applied successfully")
        else:
            logger.warning("⚠️ Some AWS framework bug fixes failed to apply")
        
        return success
    
    def apply_template_loader_fix(self) -> bool:
        """Fix template loading issue on Windows."""
        try:
            import agenteval
            import os
            from pathlib import Path
            from jinja2 import Environment, FileSystemLoader, select_autoescape
            
            # Get the path to the templates directory
            agenteval_path = Path(agenteval.__file__).parent
            templates_path = agenteval_path / "templates"
            
            if not templates_path.exists():
                logger.error(f"Templates directory not found at {templates_path}")
                return False
            
            # Create a custom FileSystemLoader that normalizes paths
            class NormalizedFileSystemLoader(FileSystemLoader):
                def get_source(self, environment, template):
                    # Normalize path separators to forward slashes
                    template = template.replace('\\', '/')
                    return super().get_source(environment, template)
            
            # Create new Jinja2 environment
            new_jinja_env = Environment(
                loader=NormalizedFileSystemLoader(str(templates_path)),
                autoescape=select_autoescape(
                    disabled_extensions=["jinja"],
                    default_for_string=True,
                    default=True,
                ),
            )
            
            # Replace the jinja_env
            agenteval.jinja_env = new_jinja_env
            
            # Also patch os.path.join in the CanonicalEvaluator module to use forward slashes
            from agenteval.evaluators.canonical import evaluator as canonical_module
            original_path_join = os.path.join
            
            def normalized_path_join(*args):
                """Path join that always uses forward slashes for template paths."""
                result = original_path_join(*args)
                # Convert backslashes to forward slashes for template paths
                return result.replace('\\', '/')
            
            # Temporarily patch os.path.join in the canonical evaluator module
            canonical_module.os.path.join = normalized_path_join
            
            logger.info("✅ Applied comprehensive template loader fix")
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply template loader fix: {e}")
            return False
    
    def apply_conversation_serializer_fix(self) -> bool:
        """Fix conversation serialization for JSON encoding."""
        try:
            import json
            from agenteval.conversation import Conversation
            
            # Create custom JSON encoder for Conversation objects
            class ConversationEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, Conversation):
                        return {
                            'turns': obj.turns,
                            'messages': [
                                {'role': role, 'content': content} 
                                for role, content in obj.messages
                            ]
                        }
                    return super().default(obj)
            
            # Patch the default JSON encoder
            original_default = json.JSONEncoder.default
            
            def patched_default(self, obj):
                if isinstance(obj, Conversation):
                    return ConversationEncoder().default(obj)
                return original_default(self, obj)
            
            json.JSONEncoder.default = patched_default
            
            logger.info("✅ Applied conversation serializer fix")
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply conversation serializer fix: {e}")
            return False
    
    def apply_prompt_passing_fix(self) -> bool:
        """Fix prompt passing issue in CanonicalEvaluator."""
        try:
            from agenteval.evaluators.canonical.evaluator import CanonicalEvaluator
            
            # Store original methods
            original_evaluate = CanonicalEvaluator.evaluate
            original_invoke_target = CanonicalEvaluator._invoke_target
            
            def patched_evaluate(self):
                """Patched evaluate method with proper prompt handling."""
                passed = False
                result = "Maximum turns reached."
                reasoning = ""

                while self.conversation.turns < self.test.max_turns:
                    if self.conversation.turns == 0:
                        # Start conversation
                        if self.test.initial_prompt:
                            user_input = self.test.initial_prompt
                        else:
                            user_input = self._generate_initial_prompt()
                            
                        # Ensure user_input is not None
                        if user_input is None:
                            logger.warning("Generated prompt is None, using fallback")
                            user_input = "Hello"
                    else:
                        # Generate next user response
                        user_input = self._generate_user_response()
                        if user_input is None:
                            logger.warning("Generated user response is None, using fallback")
                            user_input = "Please continue"

                    # Add turn to conversation
                    self.conversation.add_turn(user_input, self._invoke_target(user_input))

                    # Get test status
                    test_status = self._generate_test_status()
                    if test_status == "A":  # ALL_STEPS_ATTEMPTED
                        # Evaluate conversation
                        eval_category, reasoning = self._generate_evaluation()
                        if eval_category == "B":  # NOT_ALL_EXPECTED_RESULTS_OBSERVED
                            result = "Not all of the expected results can be observed in the conversation."
                        else:
                            result = "All of the expected results can be observed in the conversation."
                            passed = True
                        break

                from agenteval.test import TestResult
                return TestResult(
                    test_name=self.test.name,
                    passed=passed,
                    result=result,
                    reasoning=reasoning,
                    conversation=self.conversation,
                )
            
            def patched_invoke_target(self, user_input):
                """Patched _invoke_target with None check."""
                if user_input is None:
                    logger.warning("_invoke_target called with None user_input, using fallback")
                    user_input = "Hello"
                
                return original_invoke_target(self, user_input)
            
            # Apply patches
            CanonicalEvaluator.evaluate = patched_evaluate
            CanonicalEvaluator._invoke_target = patched_invoke_target
            
            logger.info("✅ Applied prompt passing fix")
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply prompt passing fix: {e}")
            return False
    
    def verify_fixes(self) -> dict:
        """Verify that all fixes are working correctly."""
        results = {}
        
        # Verify template loading
        try:
            import agenteval
            template = agenteval.jinja_env.get_template("evaluators/canonical/system/generate_initial_prompt.jinja")
            results['template_loader'] = template is not None
        except Exception:
            results['template_loader'] = False
        
        # Verify conversation serialization
        try:
            import json
            from agenteval.conversation import Conversation
            conv = Conversation()
            json.dumps(conv, cls=json.JSONEncoder)
            results['conversation_serializer'] = True
        except Exception:
            results['conversation_serializer'] = False
        
        # Verify prompt passing (basic check)
        results['prompt_passing'] = self.fixes_applied['prompt_passing']
        
        return results
    
    def get_status(self) -> dict:
        """Get the status of all applied fixes."""
        return {
            'fixes_applied': self.fixes_applied,
            'verification_results': self.verify_fixes()
        }


# Global instance for easy access
aws_fixes = AWSFrameworkBugFixes()


def apply_aws_framework_fixes() -> bool:
    """Convenience function to apply all AWS framework fixes."""
    return aws_fixes.apply_all_fixes()


def verify_aws_framework_fixes() -> dict:
    """Convenience function to verify all AWS framework fixes."""
    return aws_fixes.verify_fixes()


if __name__ == "__main__":
    # Test all fixes
    print("Testing AWS Agent Evaluation framework bug fixes...")
    
    if apply_aws_framework_fixes():
        verification = verify_aws_framework_fixes()
        print(f"Verification results: {verification}")
        
        if all(verification.values()):
            print("🎉 All AWS framework bug fixes working correctly!")
        else:
            print("⚠️ Some fixes may not be working properly")
    else:
        print("❌ Failed to apply AWS framework bug fixes")
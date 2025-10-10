"""
Minimal Template Loading Fix for AWS Agent Evaluation Framework

This fix addresses the template loading issue on Windows where the Jinja2
PackageLoader can't find templates due to path resolution problems.

This is a TEMPORARY fix until AWS resolves the upstream bug.
"""

import os
import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)


def apply_template_loader_fix():
    """Apply minimal fix for template loading issue."""
    try:
        # Import the agenteval module to patch its jinja_env
        import agenteval
        
        # Get the path to the templates directory
        agenteval_path = Path(agenteval.__file__).parent
        templates_path = agenteval_path / "templates"
        
        if not templates_path.exists():
            logger.error(f"Templates directory not found at {templates_path}")
            return False
        
        # Create a custom FileSystemLoader that handles Windows path issues
        class CrossPlatformFileSystemLoader(FileSystemLoader):
            def get_source(self, environment, template):
                # Convert backslashes to forward slashes for template names
                template = template.replace('\\', '/')
                return super().get_source(environment, template)
        
        # Create a new Jinja2 environment with our custom loader
        new_jinja_env = Environment(
            loader=CrossPlatformFileSystemLoader(str(templates_path)),
            autoescape=select_autoescape(
                disabled_extensions=["jinja"],
                default_for_string=True,
                default=True,
            ),
        )
        
        # Replace the problematic jinja_env with our working one
        agenteval.jinja_env = new_jinja_env
        
        logger.info("✅ Applied template loader fix successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to apply template loader fix: {e}")
        return False


def verify_template_loading():
    """Verify that templates can be loaded after applying the fix."""
    try:
        import agenteval
        
        # Try to load a known template
        template = agenteval.jinja_env.get_template("evaluators/canonical/system/generate_initial_prompt.jinja")
        
        if template:
            logger.info("✅ Template loading verification successful")
            return True
        else:
            logger.error("❌ Template loading verification failed - template is None")
            return False
            
    except Exception as e:
        logger.error(f"❌ Template loading verification failed: {e}")
        return False


if __name__ == "__main__":
    # Test the fix
    print("Testing template loader fix...")
    
    if apply_template_loader_fix():
        if verify_template_loading():
            print("🎉 Template loader fix working correctly!")
        else:
            print("⚠️ Template loader fix applied but verification failed")
    else:
        print("❌ Template loader fix failed to apply")
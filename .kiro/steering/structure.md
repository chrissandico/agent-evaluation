# Project Structure

## Source Code Layout

```
src/agenteval/           # Main package source
├── cli.py              # CLI entry point (agenteval command)
├── conversation.py     # Conversation management
├── defaults.py         # Default configurations
├── hook.py            # Hook system for integration testing
├── metrics.py         # Metrics collection and reporting
├── summary.py         # Test summary generation
├── trace.py           # Execution tracing
├── evaluators/        # Evaluator implementations
│   ├── base_evaluator.py
│   ├── canonical/     # Canonical evaluator (LLM-based)
│   ├── bedrock_request/  # Bedrock API handling
│   ├── model_config/  # Model configurations
│   └── evaluator_factory.py
├── plan/              # Test plan management
│   ├── plan.py
│   ├── logging.py
│   └── exceptions.py
├── targets/           # Target agent implementations
├── test/              # Test execution framework
│   ├── test.py
│   ├── test_result.py
│   └── test_suite.py
├── templates/         # Jinja2 templates for prompts
│   ├── evaluators/
│   └── summary/
└── utils/             # Utility modules
    ├── aws.py
    └── imports.py
```

## Key Directories

### `/src/agenteval/`
Main package containing all framework code. Uses `src/` layout for clean separation.

### `/tests/`
Mirror structure of `src/agenteval/` for unit tests. Uses pytest framework.

### `/docs/`
MkDocs documentation with Material theme. Includes user guides, API reference, and target configurations.

### `/samples/`
Example implementations and integrations:
- `aws_step_functions_deployment/` - AWS Step Functions deployment example
- `streamlit_app/` - Streamlit UI for test management
- `test_plan_templates/` - Template test plans

### `/shopify_extensions/`
Custom extensions (appears to be project-specific customizations):
- `configs/` - Test scenario configurations
- `targets/` - Custom target implementations
- `fixes/` - Framework patches/workarounds

## Configuration Files

- `pyproject.toml` - Build system and tool configurations
- `setup.py` - Package metadata and dependencies
- `setup.cfg` - Flake8 and coverage settings
- `mkdocs.yml` - Documentation site configuration
- `requirements.txt` - Runtime dependencies
- `requirements-dev.txt` - Development dependencies

## Template System

Templates are stored in `src/agenteval/templates/` and packaged with the distribution. Uses Jinja2 for:
- Evaluator prompts (system and runtime)
- Summary report generation

## Entry Points

- CLI: `agenteval` command (defined in setup.py)
- Python API: Import from `agenteval` package

## Testing Structure

Tests mirror the source structure under `tests/src/agenteval/`. Coverage excludes `hook.py` and test files.

## Extension Points

- **Custom Targets**: Extend base target classes in `targets/`
- **Custom Evaluators**: Implement base evaluator interface
- **Hooks**: Use `Hook` class for integration testing
- **Templates**: Add Jinja2 templates for custom prompts

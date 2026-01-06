# Source of Truth

All changes to this project MUST align with the official Agent Evaluation project standards.

## Official Resources

- **Documentation**: https://awslabs.github.io/agent-evaluation/
- **Repository**: https://github.com/awslabs/agent-evaluation

## Critical Rules

### Before Making Changes

1. **Check official docs first** - Always reference the official documentation before implementing features or making architectural decisions
2. **Follow upstream patterns** - Study existing code patterns in the official repo and replicate them
3. **Verify against docs** - Cross-reference any new features or changes with the official user guide and API reference

### Contributing Standards

All contributions must follow the official [CONTRIBUTING.md](https://github.com/awslabs/agent-evaluation/blob/main/CONTRIBUTING.md):

- Use **Conventional Commits** specification for all commit messages
- Ensure linting, formatting, and tests pass before committing
- Update `CHANGELOG.md` under "Unreleased" section for notable changes
- Include unit tests for new functionality
- Test CLI functionality when relevant to changes

### Code Quality Gates

Before any change is complete:

```bash
# 1. Linting and formatting must pass
flake8 src/ && black --check src/ && isort src/ --check --diff

# 2. All tests must pass
python -m pytest .

# 3. CLI must work (if relevant)
pip install -e .
agenteval --help
```

### Documentation Alignment

- **Targets**: Reference https://awslabs.github.io/agent-evaluation/targets/ for target implementations
- **Evaluators**: Reference https://awslabs.github.io/agent-evaluation/evaluators/ for evaluator patterns
- **Hooks**: Reference https://awslabs.github.io/agent-evaluation/hooks/ for hook system usage
- **CLI**: Reference https://awslabs.github.io/agent-evaluation/cli/ for CLI behavior
- **Configuration**: Reference https://awslabs.github.io/agent-evaluation/configuration/ for config structure

### Architecture Principles

Follow the established architecture:
- **Evaluators** orchestrate conversations and evaluate responses
- **Targets** represent the agents being tested
- **Tests** define scenarios with expected outcomes
- **Hooks** enable integration testing and side effects
- **Templates** use Jinja2 for prompt generation

### When in Doubt

1. Search the official documentation for similar functionality
2. Look at existing code in `src/agenteval/` for patterns
3. Check the official GitHub repo for recent changes or discussions
4. Refer to the samples in the official repo for implementation examples

## Forbidden Actions

- Do NOT introduce patterns that conflict with official documentation
- Do NOT bypass the established linting/formatting/testing requirements
- Do NOT create custom architectures that diverge from the evaluator/target/test model
- Do NOT ignore the Conventional Commits specification

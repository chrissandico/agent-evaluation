# Technology Stack

## Language & Version

- Python 3.9+ (supports 3.9, 3.10, 3.11, 3.12)
- Package name: `agent-evaluation`
- Current version: 0.4.1

## Build System

- Build backend: `setuptools` (>=61.0)
- Package manager: `pip`
- Source directory: `src/`

## Core Dependencies

- `pyyaml` - YAML configuration parsing
- `boto3` - AWS SDK for Python
- `click` - CLI framework
- `pydantic` (v2) - Data validation and settings
- `rich` - Terminal formatting and logging
- `jinja2` - Template engine for prompts
- `jsonpath-ng` - JSON path queries

## Development Tools

- **Linting**: `flake8` (ignores E501 line length)
- **Formatting**: `black` (code formatter)
- **Import sorting**: `isort` (black profile)
- **Testing**: `pytest`, `pytest-cov`, `pytest-mock`
- **Security**: `bandit`, `pip-audit`
- **Documentation**: `mkdocs`, `mkdocs-material`, `mkdocstrings`

## Code Style

- Follow `black` code style (line length flexible per flake8 config)
- Use `isort` with black profile for import ordering
- Conventional Commits specification for commit messages
- Tests and `__init__.py` excluded from formatting checks

## Common Commands

### Installation
```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Linting & Formatting
```bash
# Check linting and formatting
flake8 src/ && black --check src/ && isort src/ --check --diff

# Auto-format code
black src/
isort src/
```

### Testing
```bash
# Run all tests
python -m pytest .

# Run with coverage
pytest --cov
```

### CLI Testing
```bash
# Install locally and test CLI
pip install -e .
agenteval --help
```

### Documentation
```bash
# Build and serve docs locally
mkdocs serve
```

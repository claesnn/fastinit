# fastinit Development

## Setup Development Environment

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

4. Install dev dependencies:
   ```bash
   pip install pytest black flake8 mypy
   ```

## Running Tests

```bash
pytest
```

## Code Formatting

```bash
black fastinit/
```

## Linting

```bash
flake8 fastinit/
```

## Type Checking

```bash
mypy fastinit/
```

## Building and Publishing

### Build the package

```bash
python -m build
```

### Publish to PyPI

```bash
python -m twine upload dist/*
```

## Project Structure

- `fastinit/` - Main package code
  - `cli.py` - CLI entry point
  - `commands/` - CLI commands
  - `generators/` - Code generators
  - `models/` - Data models
  - `templates/` - Jinja2 templates
  - `utils.py` - Utility functions
- `tests/` - Test suite
- `pyproject.toml` - Package configuration
- `README.md` - User documentation

## Adding New Features

### Adding a new CLI command

1. Create a new file in `fastinit/commands/`
2. Define the command using Typer
3. Add it to `cli.py`

### Adding new templates

1. Create a new Jinja2 template in `fastinit/templates/`
2. Update the generator to use the template
3. Add any necessary context variables

### Adding new generators

1. Create a new generator class in `fastinit/generators/`
2. Implement the generation logic
3. Use the TemplateRenderer to render templates

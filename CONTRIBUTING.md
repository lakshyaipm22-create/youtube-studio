# Contributing

## CI Workflow

This repository uses GitHub Actions for continuous integration.

### What CI Does

The workflow (`.github/workflows/ci.yml`) runs on every push to `main` and every pull request:

1. **Install** — Sets up Python 3.12, installs system dependencies, and installs the project with `pip install -e ".[dev]"`
2. **Validate** — Verifies that `studio` and `pipeline` packages import correctly
3. **Lint** — Runs Ruff for code quality checks and formatting validation
4. **Test** — Runs pytest if a `tests/` directory exists (skips gracefully if not)

### Running Locally

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check .

# Check formatting
ruff format --check .

# Auto-fix formatting
ruff format .

# Run tests (when they exist)
pytest tests/ -v
```

### Linting Rules

Ruff is configured in `pyproject.toml` with these rule sets:

- **E** — pycodestyle errors
- **F** — pyflakes (unused imports, undefined names)
- **I** — isort (import ordering)
- **UP** — pyupgrade (modern Python syntax)
- **B** — flake8-bugbear (common bugs)

Wildcard imports (`from studio.styles import *`) are permitted in scene files and `studio/__init__.py` since this is the established convention.

### Adding Tests

Create a `tests/` directory at the project root. CI will automatically detect and run them:

```bash
mkdir tests
# Add test files: tests/test_styles.py, tests/test_pipeline.py, etc.
```

### Extending CI

To add new CI steps, edit `.github/workflows/ci.yml`. Keep the workflow:

- **Fast** — Under 3 minutes total
- **Focused** — Only validate code quality, not render videos
- **Reliable** — No flaky tests or network-dependent checks

### Auto-Merge Setup

After merging the CI workflow, enable these GitHub settings for auto-merge support:

1. **Settings → General → Pull Requests** — Enable "Allow auto-merge"
2. **Settings → Branches → Add rule** for `main`:
   - Require status checks to pass: select `Validate & Lint`
   - Require branches to be up to date before merging
   - (Optional) Require pull request reviews

Once configured, PRs that pass CI can be auto-merged without manual intervention.

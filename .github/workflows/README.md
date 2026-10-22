# GitHub Actions Workflows

This directory contains CI/CD workflows for SuperClaude Framework.

## Workflows

### 1. **test.yml** - Test Suite

**Triggers**: Push/PR to `master` or `integration`, manual dispatch
**Jobs**:

- **test**: Run the full test suite on Python 3.10
  - Set up uv and Python 3.10, install dependencies
  - Sync `src/superclaude/` → `.claude/` mirrors
  - Run the full test suite once, with coverage
  - Upload coverage to Codecov
- **swarm-marker-matrix**: Run the swarm `imm` and `inv` acceptance lanes
- **lint**: Lint, plugin, sync and dependency checks in one job
  - `ruff check` and `ruff format --check`
  - Verify the pytest plugin loads and its fixtures are available
  - `make verify-deps` (dependency allow-list)
  - `make sync-dev`, then `make verify-sync`
  - `make lint-architecture`
- **doctor-check**: Run `superclaude install` and `superclaude doctor` health check
- **test-summary**: Aggregate check that fails if any job above failed or was cancelled

**Status Badge**:

```markdown
[![Tests](https://github.com/SuperClaude-Org/SuperClaude_Framework/actions/workflows/test.yml/badge.svg)](https://github.com/SuperClaude-Org/SuperClaude_Framework/actions/workflows/test.yml)
```

### 2. **boundary-guard.yml** - Mechanical-merge Boundary Guard

Flags PRs that touch the swarm mechanical-merge boundary (`src/superclaude/cli/swarm/merge.py` and its four guard tests) with a warning and a reviewer-checklist job summary.

### 3. **contract3-generator-constraint-lint.yml** - Contract #3 PR-body Check

Runs only on PRs that touch `gates.py`, `structural_checkers.py` or `*_validator.py` (paths filter), and fails if the PR body lacks a `## Generator-Constraint Considered` section.

### 4. **pull-sync-framework.yml** - Framework Sync

Scheduled (every 6 hours) and manual sync from the upstream SuperClaude_Framework repository.

## Local Testing

Before pushing, run these commands locally:

```bash
# Run full test suite
uv run pytest -v

# Run with coverage
uv run pytest --cov=superclaude --cov-report=term

# Run linter
uv run ruff check src/ tests/

# Check formatting
uv run ruff format --check src/ tests/

# Auto-fix formatting
uv run ruff format src/ tests/

# Verify plugin loads
uv run pytest --trace-config | grep superclaude

# Run doctor check
uv run superclaude doctor --verbose
```

## CI/CD Pipeline

```
┌─────────────────────┐
│   Push/PR Created   │
└──────────┬──────────┘
           │
    ┌──────▼─────────────────────┐
    │  test.yml (Python 3.10)    │
    │                            │
    │ • test (full suite +       │
    │   coverage)                │
    │ • swarm imm / inv lanes    │
    │ • lint (ruff, plugin,      │
    │   deps, sync, arch)        │
    │ • doctor-check             │
    │ • test-summary             │
    └────────────────────────────┘
```

## Coverage Reporting

Coverage reports are generated on Python 3.10 and uploaded to Codecov.

To view coverage locally:

```bash
uv run pytest --cov=superclaude --cov-report=html
open htmlcov/index.html
```

## Troubleshooting

### Workflow fails with "UV not found"

- uv and Python are set up in each job by the `astral-sh/setup-uv` action (with `activate-environment: true`)
- If setup fails, check the action's release tag and UV's status page

### Tests fail locally but pass in CI (or vice versa)

- Check Python version: `python --version`
- Reinstall dependencies: `uv pip install -e ".[dev]"`
- Clear caches: `rm -rf .pytest_cache .venv`

### Plugin not loading in CI

- Verify entry point in `pyproject.toml`: `[project.entry-points.pytest11]`
- Check plugin is installed: `uv run pytest --trace-config`

### Coverage upload fails

- This is non-blocking (fail_ci_if_error: false)
- Check Codecov token in repository secrets

## Maintenance

### Adding a New Workflow

1. Create new `.yml` file in this directory
2. Follow existing structure (checkout, astral-sh/setup-uv)
3. Add status badge to README.md if needed
4. Document in this file

### Updating Python Versions

1. Edit the setup-uv `python-version` input in `test.yml`
2. Update `pyproject.toml` classifiers
3. Test locally with new version first

### Modifying Test Strategy

- **test.yml**: For comprehensive validation (full suite on Python 3.10)

## Best Practices

1. **Keep workflows fast**: Use caching, parallel jobs
2. **Clear names**: Job and step names should be descriptive
3. **Version pinning**: Pin action versions (@v4, @v5)
4. **Python version**: Test on the minimum supported Python (3.10)
5. **Non-blocking coverage**: Don't fail on coverage upload errors
6. **Manual triggers**: Add `workflow_dispatch` for debugging

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [UV Documentation](https://github.com/astral-sh/uv)
- [Pytest Documentation](https://docs.pytest.org/)
- [SuperClaude Testing Guide](../../docs/developer-guide/testing-debugging.md)

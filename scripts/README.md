# SuperClaude Scripts

This directory contains maintenance and development scripts. Package publishing is not done by a local script; it is handled by the GitHub Actions workflow described below.

## Publishing (GitHub Actions)

The `.github/workflows/publish-pypi.yml` workflow builds the package with `python -m build`, validates it with `twine check`, and uploads it:

- **On a published GitHub release**: uploads to PyPI.
- **Manual run (`workflow_dispatch`)** with the `target` input:
  - `testpypi` (default): uploads to TestPyPI, then a separate job installs the package from TestPyPI as a smoke test.
  - `pypi`: uploads to PyPI. No install test runs for this target.

The workflow publishes under the PyPI project name `SuperClaude`; whether a given fork can publish to that name depends on the PyPI project's ownership.

### Required Secrets

Set these in your GitHub repository settings → Secrets and variables → Actions:

- `PYPI_API_TOKEN`: Production PyPI token
- `TEST_PYPI_API_TOKEN`: TestPyPI token

### Release steps

1. Update the version (see Version Management)
2. Commit and push changes
3. Optionally run the workflow manually with `target=testpypi` to check the TestPyPI upload and install
4. Publish a GitHub release; the workflow builds and uploads to PyPI

The former local publishing wrapper (`scripts/publish.sh`) and its `build_and_upload.py` helper have been retired. Their local-only modes (clean, check, build-only, standalone test-install) have no workflow equivalent; to build locally without uploading, run `uv build`.

## Version Management

Before publishing, ensure version consistency across:

- `pyproject.toml`
- `src/superclaude/__init__.py`

The workflow's "Verify package structure" step prints both versions.

## Troubleshooting

### Build Failures

- Check Python version compatibility (≥3.10)
- Ensure all required files are present
- Validate `pyproject.toml` syntax

### Upload Failures

- Verify the repository secrets are set and correct
- Check if version already exists on PyPI
- Ensure package name is available

### Import Failures

- Check package structure (`__init__.py` files)
- Verify all dependencies are listed
- Test local installation first

## Security Notes

- Never commit API tokens to version control
- Store publishing tokens only as GitHub Actions secrets
- Tokens should have minimal required permissions
- Consider using Trusted Publishing for GitHub Actions

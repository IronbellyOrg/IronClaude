# SuperClaude Scripts

This directory contains maintenance and development scripts. This fork is not published to PyPI, so there is no publishing script or workflow.

## Installing

The `.github/workflows/publish-pypi.yml` workflow was removed in PR 280. This fork is not published to PyPI; it is installed from git, as CLAUDE.md states:

- `pipx install git+https://github.com/IronbellyOrg/IronClaude`, then `superclaude install`

The former local publishing wrapper (`scripts/publish.sh`) and its `build_and_upload.py` helper have been retired. To build locally without uploading, run `uv build`.

## Version Management

Keep the version consistent across:

- `pyproject.toml`
- `src/superclaude/__init__.py`

## Troubleshooting

### Build Failures

- Check Python version compatibility (≥3.10)
- Ensure all required files are present
- Validate `pyproject.toml` syntax

### Import Failures

- Check package structure (`__init__.py` files)
- Verify all dependencies are listed
- Test local installation first

## Security Notes

- Never commit API tokens to version control

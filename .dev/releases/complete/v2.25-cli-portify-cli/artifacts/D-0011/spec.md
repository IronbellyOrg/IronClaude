# D-0011: Output Destination Validation — Implementation Spec

**Task:** T02.04 | **Roadmap Item:** R-011 | **Status:** COMPLETE

## Implementation

Implemented in `validate_portify_config()` (config.py:119) and `run_validate_config()` (steps/validate_config.py:88)

### Logic
1. If output_dir.exists() and not writable → OUTPUT_NOT_WRITABLE error
2. If output_dir does not exist → attempt `mkdir(parents=True, exist_ok=True)`
   - PermissionError/OSError → OUTPUT_NOT_WRITABLE error
3. Valid writable destination → proceeds without error

### Error Code
- `OUTPUT_NOT_WRITABLE` — via OutputNotWritableError / "Cannot create" error string

## Verification
`uv run pytest tests/cli_portify/test_config.py::TestConfigValidationErrors::test_non_writable_output -v` → passed

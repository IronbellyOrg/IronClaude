# D-0037: --resume Logic with YAML Parse + Schema Validation

## Status: COMPLETE

## Deliverables

### `src/superclaude/cli/cli_portify/executor.py`
- `_validate_phase1_approval(workdir: Path) -> None`
  - Reads `workdir/phase1-approval.yaml`
  - Parses with `yaml.safe_load()` — NOT raw string matching (Risk 8)
  - Validates schema: `status` field must exist and equal `"approved"`
  - Raises `PortifyValidationError(INVALID_PATH, ...)` on:
    - Missing file
    - Malformed YAML (YAMLError)
    - Non-mapping YAML (list, scalar)
    - Missing `status` field
    - `status != "approved"` (pending, rejected, etc.)
    - `status` only in YAML comment (not actual field)

## Acceptance Criteria Verification

```
uv run pytest tests/cli_portify/test_phase5_analysis_pipeline.py -k "resume_validation" -v
# Result: 9 passed
```

- `status: approved` passes validation without error ✓
- `status: pending` raises `PortifyValidationError` ✓
- Missing file raises `PortifyValidationError` ✓
- Malformed YAML raises `PortifyValidationError` ✓
- Missing `status` field raises `PortifyValidationError` ✓
- `# status: approved` (comment only) raises `PortifyValidationError` — not raw string matched ✓
- `status: rejected` raises `PortifyValidationError` ✓
- List YAML (non-mapping) raises `PortifyValidationError` ✓
- Error code is `INVALID_PATH` ✓

# D-0044: Template Loader and Working Copy (T07.01)

## Status: COMPLETE

## Implementation

### `load_release_spec_template(project_root: Path) -> str`
- Located in: `src/superclaude/cli/cli_portify/prompts.py`
- Reads `src/superclaude/examples/release-spec-template.md` relative to project_root
- Raises `PortifyValidationError(INVALID_PATH)` if template file absent

### `create_working_copy(template_content: str, workdir: Path) -> Path`
- Located in: `src/superclaude/cli/cli_portify/prompts.py`
- Writes byte-identical copy to `workdir/release-spec-working.md`
- Creates workdir if missing

## Verification

```
uv run pytest tests/cli_portify/test_phase7_release_spec.py -k "release_spec_template or working_copy" -v
```

Result: **8/8 PASSED**

## Acceptance Criteria

- [x] `load_release_spec_template()` raises `PortifyValidationError` when template absent
- [x] Working copy at `workdir/release-spec-working.md` is byte-identical to source template
- [x] Template has ≥13 `{{SC_PLACEHOLDER:*}}` sentinels confirmed (actual: 57)

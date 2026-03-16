# D-0047: Inline Embed Guard and 900s Timeout (T07.04)

## Status: COMPLETE

## Implementation

### `_EMBED_SIZE_LIMIT = 120 * 1024` in `prompts.py`
- Defined at module level (OQ-008 resolution)

### `CONTENT_TOO_LARGE` error constant in `models.py`
- `CONTENT_TOO_LARGE: str = "CONTENT_TOO_LARGE"`

### `build_release_spec_prompt()` guard
- `if len(template_content) > _EMBED_SIZE_LIMIT: raise PortifyValidationError(CONTENT_TOO_LARGE, ...)`
- Content ≤ limit: passed inline via `-p` (no `--file` anywhere)

### STEP_REGISTRY entry
```python
"release-spec-synthesis": {
    "step_id": "release-spec-synthesis",
    "phase_type": PortifyPhaseType.SYNTHESIS,
    "timeout_s": 900,
    "retry_limit": 1,
}
```

## Verification

```
uv run pytest tests/cli_portify/test_phase7_release_spec.py -k "embed_guard or content_too_large or timeout_900 or STEP_REGISTRY" -v
```

Result: **All PASSED**

## Acceptance Criteria

- [x] Content of 121 * 1024 bytes raises `PortifyValidationError(failure_type=CONTENT_TOO_LARGE)`
- [x] Content of 100 * 1024 bytes passes inline (no `--file` call anywhere)
- [x] `timeout_s = 900` confirmed in STEP_REGISTRY for release-spec-synthesis
- [x] `--file` flag does NOT appear anywhere in `prompts.py` code paths

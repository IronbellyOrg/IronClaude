# D-0011 Evidence: detect_prompt_too_long() error_path Parameter

## Deliverable
`detect_prompt_too_long()` in `src/superclaude/cli/sprint/monitor.py` accepts `error_path: Path | None = None` keyword-only parameter.

## Implementation

**File:** `src/superclaude/cli/sprint/monitor.py`
**Function:** `detect_prompt_too_long(output_path: Path, *, error_path: Path | None = None) -> bool`

### Changes:
- Extracted inner `_scan(path: Path) -> bool` helper containing the existing last-10-lines logic
- `_scan(output_path)` called first — backward compatible
- If `error_path is not None`, `_scan(error_path)` called second
- Returns `True` if pattern found in **either** file
- `error_path=None` (default) → identical behavior to previous implementation

### Backward compatibility:
All existing callers (`detect_prompt_too_long(output_file)`) unchanged — `error_path` defaults to `None`.

## Verification

`uv run pytest tests/sprint/ -v --tb=short` → **629 passed** in 37.22s

## Milestone
M3.2 satisfied.

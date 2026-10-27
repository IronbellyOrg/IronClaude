# D-0002 Evidence — discover_phases() Execution Mode Parsing

## Task
T01.02 — Extend `discover_phases()` to Read Execution Mode Column

## Change Location
- File: `src/superclaude/cli/sprint/config.py`
- Function: `discover_phases()` (lines 27–107)

## Change Made
Extended `discover_phases()` to:
1. Scan all markdown pipe-table rows in the index file
2. Detect a header row containing "file" and optionally "execution mode" columns
3. For each data row, extract the execution mode value with case-normalization (`.strip().lower()`)
4. Raise `click.ClickException` for unrecognized values (not in `{"claude", "python", "skip"}`)
5. Default to `"claude"` when the `Execution Mode` column is absent

## Key Implementation Details
- Separator rows (`|---|---|---|`) detected via `re.compile(r"^[\s\-|:]*$")`
- Markdown link syntax (`[text](url)`) stripped from filenames
- `exec_mode_by_file` dict maps filename → execution_mode before Phase construction

## Verification
- `uv run pytest tests/sprint/test_preflight.py -v -m integration` → **4 passed**
- `uv run pytest tests/sprint/ -q` → **666 passed, 0 failed**
- Round-trip: python/claude/skip values all parse correctly
- Case normalization: "Python" → "python" ✓
- Invalid mode raises ClickException ✓
- Absent column defaults all phases to "claude" ✓

## Date
2026-03-16

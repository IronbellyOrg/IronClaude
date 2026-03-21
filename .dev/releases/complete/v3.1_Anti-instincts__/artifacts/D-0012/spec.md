# D-0012: Anti-Instinct Step in _build_steps()

## Status: COMPLETE

## Changes

`src/superclaude/cli/roadmap/executor.py`:
- Anti-instinct step added to `_build_steps()` between merge and test-strategy
- `timeout_seconds=30`, `retry_limit=0`, `gate=ANTI_INSTINCT_GATE`
- Inputs: `[config.spec_file, merge_file]`
- Output: `out / "anti-instinct-audit.md"`

## Verification
- `uv run pytest tests/roadmap/ -x` → 1247 passed, 0 failed

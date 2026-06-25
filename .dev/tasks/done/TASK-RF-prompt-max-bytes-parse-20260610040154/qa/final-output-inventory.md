# Final QA Gate — Input Inventory

**Date:** 2026-06-10
**Worktree (read the files HERE):** `/config/workspace/IronClaude-pr156` (branch `fix/pipeline-stdin-large-prompts`, base `3a2db5f0`)
**Diff stat:** 2 files changed, +124 / -18

## Files under review

1. **`src/superclaude/cli/pipeline/process.py`**
   - Added module-level helper `_parse_prompt_max_bytes(raw: Optional[str], default: int = 16 * 1024 * 1024) -> int` (defined after `_log` at L21, before the `PROMPT_MAX_BYTES` assignment). Returns `default` on `None`; catches `(TypeError, ValueError)` from `int(raw)` → warn + default; guards `value <= 0` → warn + default; else returns parsed value. No new imports.
   - Swapped the bare `PROMPT_MAX_BYTES: int = int(os.environ.get(...))` for `PROMPT_MAX_BYTES: int = _parse_prompt_max_bytes(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES"))`. Still typed `int`; no redundant default at call site; `# Default 16 MiB` comment preserved.

2. **`tests/pipeline/test_process_stdin.py`**
   - Added `_parse_prompt_max_bytes` to the import from `superclaude.cli.pipeline.process`.
   - Added `class TestPromptMaxBytesEnvParse` with 6 methods: non-integer→default+warning, empty-string→default+warning, "0"→default+warning, "-1"→default+warning, valid "2048"→2048 no-warning, None→default no-warning. caplog scoped to the `superclaude.pipeline.process` logger.

## Verification already on record (Phase 3 / Phase 4)
- 19 passed (targeted) · 1302 passed / 1 skipped (regression) · import-safety repro green (16MB/0→16777216, 2048→2048) · ruff format + check clean (scoped).

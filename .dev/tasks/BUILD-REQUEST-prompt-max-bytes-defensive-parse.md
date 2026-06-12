# BUILD_REQUEST — Defensive parse for `SUPERCLAUDE_PROMPT_MAX_BYTES`

**GOAL:** Apply the fix described in `.dev/troubleshoot/bug-prompt-max-bytes-import-hardfail-20260610035732/REPORT.md` — make `PROMPT_MAX_BYTES` parsing in `src/superclaude/cli/pipeline/process.py` defensive so a misconfigured `SUPERCLAUDE_PROMPT_MAX_BYTES` env var can never hard-fail module import.

**WHY:** PR #156 review comment `r3385368388` (augmentcode bot, severity medium). The current `PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16*1024*1024))` runs at module import time; a non-integer env value (`"16MB"`, `""`, `"0x10"`) raises `ValueError` during import of `superclaude.cli.pipeline.process`, cascading an `ImportError` to every dependent module and preventing the CLI from loading. A config typo becomes a total import outage. The documented intent is a "sanity guard … env-overridable for operators," so a bad override must degrade gracefully, not brick the module.

**WHERE:**
- `src/superclaude/cli/pipeline/process.py` (lines ~23-26) — replace the bare `int(os.environ.get(...))` with a `_parse_prompt_max_bytes(raw, default)` helper that:
  - returns `default` when `raw is None` (var absent),
  - catches `(TypeError, ValueError)` on `int(raw)` → log `_log.warning` + return `default`,
  - guards `value <= 0` → log `_log.warning` + return `default`,
  - otherwise returns the parsed value.
  - `Optional` (typing) and `_log` (module logger at line ~21) are already in scope — no new imports needed. Keep `PROMPT_MAX_BYTES` typed `int`; no call-site changes.
- `tests/pipeline/test_process_stdin.py` — add a `TestPromptMaxBytesEnvParse` class covering: non-integer env → default (+ warning via `caplog`), non-positive (`"0"`, `"-1"`) → default, valid int string → parsed value, absent var → default. Test the helper directly (call `_parse_prompt_max_bytes(...)`); do not rely on import-time env state.

**TARGET BRANCH:** `fix/pipeline-stdin-large-prompts` (the PR #156 head). NOT `fix/prd-parallel-gate-advisory` (current working tree — unrelated in-progress work; do not disturb). Execute in an isolated worktree.

**ACCEPTANCE:**
- Setting `SUPERCLAUDE_PROMPT_MAX_BYTES` to a non-integer no longer raises on import; `PROMPT_MAX_BYTES` falls back to 16 MiB with a logged warning.
- `uv run pytest tests/pipeline/test_process_stdin.py` passes including the new env-parse tests.
- No regression: `uv run pytest tests/pipeline/ tests/cli_portify/` green.
- Behavior unchanged for absent-var and valid-int cases.

**TEMPLATE:** 01 (generic) — 2 files, < 1 hour, single-domain.

**SoT NOTE:** `process.py` and the test are source files under `src/` and `tests/` — no `.claude/` involvement. Standard `git add` of the two paths only.

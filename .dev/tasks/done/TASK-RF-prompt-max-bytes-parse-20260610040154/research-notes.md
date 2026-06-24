# Research Notes: Defensive parse for SUPERCLAUDE_PROMPT_MAX_BYTES

**Date:** 2026-06-10
**Scenario:** A (explicit — fix fully specified in REPORT + BUILD_REQUEST)
**Depth Tier:** Quick (2 files, single concern, no discovery needed)
**Track Count:** 1
**Source of evidence:** Direct read of `origin/fix/pipeline-stdin-large-prompts` + a clean cherry-pick worktree where the existing suite was run GREEN (13 stdin tests + 1296 pipeline/cli_portify) earlier this session.

---

## EXISTING_FILES

- `src/superclaude/cli/pipeline/process.py` — the module under fix. Relevant region (on PR branch `fix/pipeline-stdin-large-prompts`):
  - line ~21: `_log = logging.getLogger("superclaude.pipeline.process")` — module logger, in scope for a warn-on-fallback path.
  - lines ~24-26: `PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))` — **the defect**. Module-import-time bare `int()` over the env value.
  - line ~2 of header block: `from typing import Callable, Optional` — `Optional` already imported (helper signature can use it without new imports).
  - `os` and `logging` already imported at module top.
  - Downstream consumer: `ClaudeProcess.start()` reads `PROMPT_MAX_BYTES` for the pre-spawn size guard; it expects an `int`. The fix MUST keep `PROMPT_MAX_BYTES` an `int` — no call-site changes.
- `tests/pipeline/test_process_stdin.py` — the test module to extend. Relevant region:
  - lines ~123-175: `class TestPromptMaxBytesGuard` — patches the **constant** via `monkeypatch.setattr("superclaude.cli.pipeline.process.PROMPT_MAX_BYTES", 1024)`; it does NOT exercise env-var parsing. The new env-parse path is currently untested.
  - Test style: pytest classes grouping related tests, `tmp_path`/`monkeypatch`/`caplog` fixtures, no inline `python -c`.

## PATTERNS_AND_CONVENTIONS

- Module-level comment style is dense and explanatory (see the existing `# Default 16 MiB; ...` block); the new helper docstring should match that register.
- Logging via the module `_log` (e.g., `_log.warning(...)` is already used elsewhere in `start()`/`wait()`/`terminate()` for `_stdin_error`).
- Tests: UV-run pytest (`uv run pytest tests/pipeline/...`), class-grouped, fixture-based. Project rule: no `python -m`/bare pytest — UV only.
- SoT: `process.py` and the test are under `src/` and `tests/` — standard `git add`, NO `.claude/` involvement.

## GAPS_AND_QUESTIONS

- None blocking. The fix shape, the in-scope imports, and the test seam are all confirmed by direct read. Edge values to cover: non-integer string, empty string, non-positive (`"0"`, `"-1"`), valid string, absent var.

## RECOMMENDED_OUTPUTS

- Modify `src/superclaude/cli/pipeline/process.py`: add `_parse_prompt_max_bytes(raw, default)` helper; replace the bare `int(...)` assignment with a call to it.
- Modify `tests/pipeline/test_process_stdin.py`: add `TestPromptMaxBytesEnvParse` exercising the helper directly (non-integer→default+warning, non-positive→default+warning, valid→parsed, absent→default).

## SUGGESTED_PHASES

- Phase 1 (Implementation): helper + assignment swap in process.py.
- Phase 2 (Test): add env-parse test class.
- Phase 3 (Verification): run targeted + regression pytest; confirm no import-time crash on bad env; lint.
- Phase 4 (Completion): POST reflect gate + status update.

## TEMPLATE_NOTES

- Template 01 (generic): known inputs/outputs, direct transformation, 2 files, <1 hour. No discovery phase needed.
- Target branch: `fix/pipeline-stdin-large-prompts` (PR #156 head) — execute in an isolated worktree; do NOT touch the current `fix/prd-parallel-gate-advisory` working tree.

## AMBIGUITIES_FOR_USER

None — intent is clear from the PR review comment, the REPORT, and the codebase. The fix is small, fully grounded, and its surrounding suite is already proven green.

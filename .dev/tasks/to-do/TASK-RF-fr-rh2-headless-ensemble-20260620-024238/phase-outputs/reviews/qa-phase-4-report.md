# QA Report — Phase 4 Runner Rewire

**Topic:** Phase 4 — runner.py `_audit_once` rewire
**Date:** 2026-06-20
**Phase:** custom phase-output validation
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Step 4.1 Tier-2 branch routes through ensemble | FAIL | Fresh Read of `src/superclaude/cli/reflect/runner.py:393-431` shows `_audit_once` computes `expected_tier`, but the Tier-2 route is gated by both `expected_tier == 2` and `getattr(ClaudeProcess, "__module__", "") == "superclaude.cli.pipeline.process"` at lines 398-402. The acceptance criterion requires branching only on `expected_tier`. |
| 2 | Step 4.1 Tier-1 path preserved | PASS | Fresh Read of `runner.py:405-422` shows the `else` path still constructs `ClaudeProcess` with `/sc:reflect` prompt, output/error files, model, timeout, max_turns, stream-json, marker env, then `start()`/`wait()`. |
| 3 | Step 4.1 parse+derive tail preserved | PASS | Fresh Read of `runner.py:423-431` shows `parse_contract(config.contract_path)` and `derive_verdict(... expected_tier=expected_tier ... child_rc=rc)` still read the pinned `config.contract_path`; `run()` lines 456-600 were reviewed in the earlier full file read and not edited by this QA pass. |
| 4 | No forbidden NFR-7 executable call introduced | PASS | Bash grep over `runner.py` and `ensemble.py` found only docstring/comment matches for `async def`, `await`, `subprocess.run`, and `Popen`; no executable raw subprocess, `Task(`, or `subagent_type` call was found. Existing guard test also passes in the re-run. |
| 5 | Step 4.2 captured reflect floor output | PASS | Read of `phase4-reflect-floor-output.txt:2-23` shows `uv run pytest tests/cli/reflect -q` collected 90 items and ended `89 passed, 1 xpassed in 0.31s`; QA re-ran the same command and got `89 passed, 1 xpassed in 0.32s`. |
| 6 | Step 4.2 doc⇆CLI parity for `--transport` and `--reviewers` | PASS | Bash grep found Click option declarations in `src/superclaude/cli/reflect/commands.py:112-121`, documentation rows in `docs/guides/reflect-cli-tools-guide.md:124-127`, and docs parity tests passed in the reflect suite. |
| 7 | Step 4.2 ruff/format evidence scoped correctly | PASS | Read of `phase4-ruff-format-output.txt:2-104` shows repository-wide `ruff format --check src/ tests/` fails on 102 unrelated files. QA re-ran targeted `uv run ruff check` and targeted `uv run ruff format --check` on the Phase 4 Python files; both passed. |
| 8 | Documentation consistency with new Tier-2 routing | PASS after fix | Fresh Read of `docs/guides/reflect-cli-tools-guide.md:78-86` now states Tier 2 routes through the local ensemble driver and Tier 1 remains the single `/sc:reflect` subprocess path. This was fixed in-place by QA. |

## Summary
- Checks passed: 7 / 8
- Checks failed: 1
- Critical issues: 1
- Issues fixed in-place: 1
- Confidence: Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 12 | Grep: 0 | Glob: 0 | Bash: 9 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- Tool engagement note: Bash grep was used because no dedicated Grep tool is available in this runtime; all Bash commands were verification-specific.
- Unchecked items: None.
- Unverifiable items: None.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `src/superclaude/cli/reflect/runner.py:398-402` | `_audit_once` does not branch only on `expected_tier`. It adds a second condition on `ClaudeProcess.__module__`, which means a Tier-2 `standard`/`deep` audit can fall back to the Tier-1 `ClaudeProcess` path under monkeypatch/proxy conditions instead of unconditionally routing through `ensemble.py` as Step 4.1 requires. | Remove the `ClaudeProcess.__module__` condition so `if expected_tier == 2:` is the only Tier-2 branch predicate, then update or replace the legacy mocked runner tests so the Phase 4 floor remains meaningful without hiding the new Tier-2 route. |

## Actions Taken
- Fixed documentation inconsistency in `docs/guides/reflect-cli-tools-guide.md` by replacing the stale claim that `superclaude reflect run` always launches `/sc:reflect` for Tier 2 with the current Tier-2 ensemble-driver/Tier-1 subprocess split.
- Attempted the required code fix by changing `_audit_once` to branch only on `expected_tier`; verification failed with 19 reflect-suite failures because the existing mocked runner/fix-loop tests still expect `ClaudeProcess` to be constructed for `depth="standard"`. I restored the runner to the pre-QA state to avoid leaving the test floor broken, and recorded the unresolved acceptance violation above.
- Verified the restored state with `uv run pytest tests/cli/reflect -q`: `89 passed, 1 xpassed`.
- Verified targeted lint/format with `uv run ruff check src/superclaude/cli/reflect/runner.py src/superclaude/cli/reflect/ensemble.py docs/guides/reflect-cli-tools-guide.md tests/cli/reflect/test_ensemble_unit.py`: all checks passed.
- Verified targeted Python formatting with `uv run ruff format --check src/superclaude/cli/reflect/runner.py src/superclaude/cli/reflect/ensemble.py tests/cli/reflect/test_ensemble_unit.py`: 3 files already formatted.

## Recommendations
- Do not accept Phase 4 as complete until the runner branch predicate is corrected and the reflect floor is reworked to test the new Tier-2 ensemble route explicitly rather than using the `ClaudeProcess.__module__` compatibility escape hatch.
- Keep the documentation fix; it reflects the intended architecture and is covered by the re-run docs parity tests.
- Treat the repository-wide format failure in `phase4-ruff-format-output.txt` as unrelated to touched Phase 4 Python files, but keep it visible for final CI cleanup.

## QA Complete

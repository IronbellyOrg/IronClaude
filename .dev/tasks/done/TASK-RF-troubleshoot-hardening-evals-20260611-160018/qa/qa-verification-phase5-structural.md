# QA Report — Phase 5 Fix Verification (Structural)

**Topic:** Phase 5 fixes — flaky no-leak test (concurrency artifact), orphaned ReplayExecutor seam, conftest nits
**Date:** 2026-06-12
**Phase:** fix-cycle (report-only verification)
**Fix authorization:** false (modified NO file)

---

## Overall Verdict: PASS

All six fixes (P5-1 through P5-6, plus N-1 confirmed no-change) are correctly applied and verified by independent tool evidence. The rewritten no-leak test is deterministic across 8 serial runs (8/8 green). The full backtest suite is green-or-correctly-skips (38 passed, 11 skipped, 0 failed/errored). Ruff check + format are clean on the Phase 5 fix surface.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| P5-1 | No-leak test rewritten to scoped, concurrency-robust assertion | PASS | `test_git_replay_integration.py:95-140` — see breakdown below |
| P5-2 | `test_replay_executor.py` exercises the seam, FAST | PASS | `test_replay_executor.py:1-125` — 6 tests, pure stub+inspect |
| P5-3 | `checkout_worktree` teardown adds best-effort `git worktree unlock` before remove | PASS | `git_replay.py:206-216` (unlock) precedes `:217-227` (remove --force) |
| P5-4 | conftest yield fixture annotated `Iterator[Path]` | PASS | `conftest.py:21` `replay_scratch_root() -> Iterator[Path]`; `:41` `catch_rate_output_dir -> Path` (returns, correct) |
| P5-5 | conftest docstring no longer overclaims pollution guard | PASS | `conftest.py:4-7` + `:44-46` softened to "never writes under docs/" |
| P5-6 | Determinism / suite-green re-capture | PASS | 8/8 green stress run + 38 passed / 11 skipped |
| N-1 | E4 "UNMERGED" comment unchanged (correct) | PASS | `git_replay.py:52-54` comment intact, no change required |

### P5-1 detailed breakdown (CRITICAL — the flaky test)

| Sub-requirement | Result | Evidence |
|---|---|---|
| Passes a known scratch_root (tmp_path) | PASS | `:95` fixture `tmp_path`; `:111-113` `checkout_worktree(e1.prefix_parent_sha, scratch_root=tmp_path)` |
| Asserts `wt.exists()` in-body (non-vacuous) | PASS | `:116` `assert wt.exists(), f"worktree was not created at {wt}"` |
| Raises inside the body | PASS | `:110` `pytest.raises(RuntimeError)` + `:118` `raise RuntimeError("simulated replay failure")` |
| Asserts checkout dir is gone after raise | PASS | `:124` `assert not wt.exists()` |
| Asserts no worktree under that scratch_root remains | PASS | `:131-136` scopes to `str(tmp_path)`, filters `worktree ` stanzas containing scratch, asserts `not leaked` |
| NO global `after == baseline` byte-compare | PASS | No `baseline`/`before`-vs-`after` byte-compare anywhere in file; assertion is scratch-root-scoped only |

### P5-2 detailed breakdown (orphaned seam)

| Sub-requirement | Result | Evidence |
|---|---|---|
| stub → ReplayResult returned verbatim | PASS | `test_replay_executor.py:28-49` `result is expected` |
| missing invoker → VERDICT_ERROR | PASS | `:51-60` `result.verdict == VERDICT_ERROR`, `"no invoker registered" in detail` |
| raising invoker → VERDICT_ERROR (fold) | PASS | `:63-77` `"ValueError" in result.detail` |
| resolve_callable module-level function | PASS | `:79-91` `is_class_bound is False`, signature read, `content` param |
| resolve_callable class-bound method | PASS | `:104-118` `is_class_bound is True`, `owning_class is _LocalOwner`, sig params |
| Protocol satisfaction | PASS | `:121-125` `isinstance(executor, ReplayExecutor)` |
| FAST (no real git/subprocess) | PASS | Imports only `inspect`/`Path`; stub invokers; module suite ran in subset of 10.34s total; no `_subprocess`/`checkout_worktree` calls |

---

## Summary

- Checks passed: 7 / 7 (P5-1..P5-6 + N-1)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; verification agent modified no file)

## Command Evidence

| Command | Expected | Actual | Result |
|---|---|---|---|
| `for i in seq 1..8: pytest test_git_replay_integration.py -q` | 8/8 green | `2 passed in ~2.6s` ×8 (all green, zero flake) | PASS |
| `pytest tests/troubleshoot/backtest/ -q` | 38 passed, 11 skipped, 0 fail/err | `38 passed, 11 skipped in 10.34s` | PASS |
| `ruff check tests/troubleshoot/backtest/` | clean | `All checks passed!` | PASS |
| `ruff format --check tests/troubleshoot/backtest/` | clean | `21 files already formatted` | PASS |

**Scope note on repo-wide ruff:** A repo-wide `uv run ruff check` and `uv run ruff format --check src/ tests/` surface 127 check errors / 101 format diffs, but a grep confirms NONE are in the four Phase 5 files (`git_replay.py`, `conftest.py`, `test_replay_executor.py`, `test_git_replay_integration.py`). These are pre-existing, out-of-scope failures (e.g. `tests/swarm/*`) unrelated to this fix. The Phase 5 fix surface is clean. Tagged `[OUT-OF-SCOPE]` — not introduced by P5 and not this task's responsibility.

## Issues Found

None within scope.

| # | Severity | Location | Issue | Note |
|---|----------|----------|-------|------|
| 1 | INFO `[OUT-OF-SCOPE]` | repo-wide (`tests/swarm/*` et al.) | Pre-existing repo-wide ruff check/format failures | Not in any Phase 5 file; predates this fix; not remediated (report-only + out of scope) |

## Confidence

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 5 | Grep: 1 | Glob: 0 | Bash: 5

Every check was verified against actual file content (Read) and live command output (Bash). P5-1's non-vacuous + scoped assertion structure, P5-2's seam coverage, P5-3's unlock-before-remove ordering, and P5-4/P5-5's annotations + softened docstrings were each confirmed at specific line numbers. Determinism (the original CRITICAL) was re-proven by an 8× serial stress run with zero flake.

## QA Complete

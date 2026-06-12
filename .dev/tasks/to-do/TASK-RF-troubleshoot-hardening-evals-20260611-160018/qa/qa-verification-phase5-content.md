# QA Verification — Phase 5 Fixes (Content / Semantics)

**Phase:** report-qualitative (Phase 5 fix-VERIFICATION, report-only, fix_authorization: false)
**Date:** 2026-06-12
**Top-line verdict: PASS**

All three Phase 5 fixes (P5-1 rewritten no-leak test, P5-2 new `test_replay_executor.py`, P5-6 re-captured summary) are genuine, non-vacuous, and truthful. No new vacuity introduced. Every claim independently verified against source code and live test execution.

---

## VERIFY-1 — Rewritten no-leak test genuinely proves G3 (not weakened to a tautology): **PASS**

File: `tests/troubleshoot/backtest/test_git_replay_integration.py:95-140`

(a) **Non-vacuous — proves the worktree was created.** `test_git_replay_integration.py:116` asserts `wt.exists()` INSIDE the `with` body (`assert wt.exists(), f"worktree was not created at {wt}"`) before teardown is exercised. This is a real creation proof, not assumed.

(b) **Exercises the raise/teardown path.** `test_git_replay_integration.py:110-118` wraps the checkout in `pytest.raises(RuntimeError)` and the body explicitly `raise RuntimeError("simulated replay failure")` at line 118 — the failure path that triggers the `finally` teardown in `checkout_worktree`. Line 120 (`assert captured`) guards that the body actually ran (the context manager yielded), preventing a vacuous pass where the `with` never executed.

(c) **Asserts teardown reaped it — two independent checks.**
  - Line 124 `assert not wt.exists()` — the checkout dir is gone (rmtree + `remove --force` fired).
  - Lines 131-136 read `git_replay.worktree_list_porcelain()` (the REAL porcelain reader, verified at `git_replay.py:143-151`) and assert NO `worktree ` stanza under this test's `tmp_path` scratch_root survives — proving the `.git/worktrees/<name>/` admin record was pruned.

**Scoping to `tmp_path` is legitimate, not a dodge.** The assertion still fires the full create→raise→teardown→reap cycle; it only narrows the leak SEARCH to this test's own `scratch_root` (line 131-135, `scratch in ln`). The `checkout_worktree` signature genuinely accepts `scratch_root` (`git_replay.py:154-157`: `def checkout_worktree(commitish, *, scratch_root=None)`), and minting a unique `replay-<uuid>` subdir under it (`git_replay.py:175-179`) means the assertion can only see THIS replay's worktree — immune to concurrent unrelated worktrees while still proving G3 for this escape. The root-cause note (qa-consolidated-findings-phase5.md:18) correctly identifies the original global byte-compare flake as a concurrency artifact; the scoped rewrite is the proper fix, not a weakening.

**Determinism + non-vacuity confirmed by live execution:** ran the no-leak test 8× serially → 8/8 PASS, 0 skip, 0 fail. Critically it RAN (did not skip) on this full-history clone — so `wt.exists()` and both teardown assertions actually executed (the skip-guard at `test_git_replay_integration.py:56-68` did not fire locally).

---

## VERIFY-2 — New `test_replay_executor.py` genuinely closes BL-1 orphaned-seam gap: **PASS**

File: `tests/troubleshoot/backtest/test_replay_executor.py` (6 tests, all real assertions — zero `assert True`)

- `test_replay_executor.py:28-48` — stub invoker → asserts `replay()` returns the exact `ReplayResult` (`result is expected`), verdict `MISS`, escape_id `E1`. Real field assertions.
- `test_replay_executor.py:51-60` — missing invoker → asserts `VERDICT_ERROR` + `"no invoker registered" in result.detail`. Matches `replay_executor.py:180-185`.
- `test_replay_executor.py:63-76` — raising invoker → asserts `VERDICT_ERROR` and `"ValueError" in result.detail` (error-fold). Matches `replay_executor.py:188-193` (`type(exc).__name__`).
- `test_replay_executor.py:79-91` — `resolve_callable` on MODULE-LEVEL function: asserts `is_class_bound is False`, `owning_class is None`, real `inspect.Signature` read, and `"content" in signature.parameters`. **Signature claim independently verified:** `src/superclaude/cli/prd/gates.py:197` is `def _check_parallel_instructions(content: str) -> bool | str:` — one positional `content` param, exactly as the test asserts. This reads from the LIVE module, a genuine signature read.
- `test_replay_executor.py:104-118` — `resolve_callable` on `Class.method`: asserts `is_class_bound is True`, `owning_class is _LocalOwner`, real signature with `prefix` + keyword-only `flag`. Matches `resolve_callable`'s `"." in qualname` branch (`replay_executor.py:130-146`).
- `test_replay_executor.py:121-125` — asserts `InProcessReplayExecutor` satisfies the `runtime_checkable` `ReplayExecutor` Protocol (`isinstance` + `hasattr "replay"`). Matches `replay_executor.py:80-91`.

**Seam now referenced + exercised honestly.** The previously-orphaned symbols (`ReplayExecutor`, `InProcessReplayExecutor`, `ReplayResult`, `ResolvedCallable`, `resolve_callable` — all defined in `replay_executor.py`) are now imported and driven by real tests. Import resolution verified: the test imports `ReplayEscape` from `replay_executor` (`test_replay_executor.py:17-25`); `replay_executor.py:37` imports `ReplayEscape` into module scope, so it is a legitimate re-exported attribute (no broken import). Live run: 6/6 PASS in 0.14s.

The tests exercise the in-process executor CONTRACT directly without forcing the per-escape runners to route through it (the runners still use `run_prefix_replay_snippet` / `read_source_from_worktree`) — an honest closure of the orphaned-seam gap, exactly as P5-2 prescribed.

---

## VERIFY-3 — Re-captured summary accurate (38 passed / 11 skipped / 0 failed) + concurrency note truthful: **PASS**

File: `phase-outputs/test-results/pytest-backtest-summary.md`

- Live full-suite run: `uv run pytest tests/troubleshoot/backtest/` → **38 passed, 11 skipped** in 10.51s. Matches the summary Counts table (`pytest-backtest-summary.md:18-24`: passed 38, skipped 11, failed 0, errored 0) exactly.
- The +6 attribution (`pytest-backtest-summary.md:11-14`: no-leak rewritten in place = still 1 test, plus 6 new executor tests) is arithmetically consistent — confirmed the new file contributes exactly 6 tests.
- Concurrency-robust note (`pytest-backtest-summary.md:6-14`) is truthful: the scoped-assertion description matches the actual test code (`tmp_path` scratch_root, scoped porcelain check), and the "8/8 serial reruns green" determinism claim was independently reproduced (8/8 PASS above).
- Skip attribution (`pytest-backtest-summary.md:29-41`) is internally coherent: 5 NEW=CATCH proxies + 1 waiver-latch + 5 catch-rate aggregation parametrize = 11 skips, all designed (impl refs not yet landed), not collection errors.

---

## VERIFY-4 — No new vacuity introduced: **PASS**

- No `assert True` / `assert 1` / bare `pass`-body tests in either touched test file (read both end-to-end).
- The no-leak test's `assert captured` (line 120) is an explicit anti-vacuity guard against a non-yielding context manager.
- The executor tests assert on concrete `ReplayResult` fields, verdict tokens, and real `inspect.Signature` contents — no stubs asserting against themselves.
- Lint + format parity confirmed clean on all four touched/underlying files: `ruff check` → "All checks passed!"; `ruff format --check` → "2 files already formatted".

---

## Self-Audit

**(a) Reliance list — items relied on without re-deriving:**
- Relied on prior structural lens (qa-structural-test-green-report.md PASS) for raw collection integrity → independently re-ran the full suite anyway (38/11/0 reproduced).

**(b) Independent semantic checks (tool-verified, INV-019):**
- `_check_parallel_instructions` signature — verified by `grep -n` against `src/superclaude/cli/prd/gates.py:197` (one positional `content` param), confirming the test's signature assertion is not fabricated.
- `checkout_worktree` accepts `scratch_root` — verified by `Read` of `git_replay.py:154-179` (kwarg present, unique subdir minted), confirming the scoped rewrite is wired to a real API, not aspirational.
- No-leak determinism — verified by 8× serial live re-run (8/8 PASS, RAN not skipped), confirming non-vacuity claim (a/b/c) actually executes here.
- 38/11/0 counts — verified by live `uv run pytest tests/troubleshoot/backtest/`.
- 6 executor tests genuine — verified by live `uv run pytest test_replay_executor.py` (6 PASS, 0.14s) + Read of every assertion.
- Lint/format parity — verified by live `ruff check` + `ruff format --check`.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 6 | Grep: 2 | Glob: 0 | Bash: 5
**Web research:** none performed (all checks local-file / live-execution bound).

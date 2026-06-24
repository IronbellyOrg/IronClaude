# Phase 5 QA — Consolidated Findings

**Consolidated verdict: FAIL** (2 lenses FAIL + conftest lens PASS-with-nits; FAIL if ANY agent reports ANY issue).

## Lens verdicts (6 lens agents)

| Lens | Agent | Report | Verdict |
|------|-------|--------|---------|
| Structural — conftest + pollution-guard | rf-qa | `qa-structural-conftest-report.md` | PASS (5 nits) |
| Structural — test-green evidence | rf-qa | `qa-structural-test-green-report.md` | PASS |
| Structural — lint + format parity | rf-qa | `qa-structural-lint-format-report.md` | PASS |
| Content — UV-only discipline | rf-qa-qualitative | `qa-content-uv-discipline-report.md` | PASS |
| Content — green-means-correct-skip | rf-qa-qualitative | `qa-content-green-semantics-report.md` | **FAIL** (1 CRITICAL flaky test, 1 IMPORTANT summary determinism) |
| Domain — end-to-end harness coherence | rf-qa-qualitative | `qa-domain-harness-coherence-report.md` | **FAIL** (BL-1 orphaned seam IMPORTANT, BL-2 = same flake CRITICAL, N-1 MINOR) |

## Root-cause note (verified by executor)

A serial single-process stress run (8× `test_backtest_replay_leaves_no_leaked_worktree`) → **8/8 PASS, zero leaks**. The flake is a CONCURRENCY ARTIFACT: 6 QA agents ran real-git worktree operations against the shared git common-dir simultaneously; the `locked initializing` worktree (`/tmp/backtest-replay-*/wt`) the no-leak test flagged was ANOTHER concurrent process's in-flight `git worktree add`, which the test's GLOBAL `after == baseline` byte-compare wrongly attributed as a leak (and which prune correctly refuses to reap — it isn't this process's worktree). The real fix is to SCOPE the assertion to this escape's own record (agent recommendation #1b) so it is robust to concurrent unrelated worktrees while still proving G3.

## Deduplicated issues

| # | Severity | File | Issue | Required fix | Lens |
|---|----------|------|-------|--------------|------|
| P5-1 | CRITICAL | `test_git_replay_integration.py::test_backtest_replay_leaves_no_leaked_worktree` | The global `after == baseline` porcelain byte-compare is fragile in this multi-worktree shared repo: any concurrent/unrelated `git worktree add` (or a pre-existing stanza) breaks it. | REWRITE the no-leak test to a SCOPED assertion: pass a known `scratch_root` (e.g. `tmp_path`) to `checkout_worktree`, assert inside the `with` body that `wt.exists()` (non-vacuous: the worktree really was created), then after the body raises, assert (a) the checkout dir `wt` no longer exists AND (b) NO worktree path under that `scratch_root` appears in `worktree_list_porcelain()`. This proves THIS replay left no leak and is immune to concurrent unrelated worktrees. Keep the try/finally teardown contract (G3 intent preserved; document the scoping rationale). | green-semantics / coherence |
| P5-2 | IMPORTANT | `replay_executor.py` (orphaned seam) | `ReplayExecutor` / `InProcessReplayExecutor` / `ReplayResult` / `ResolvedCallable` / `resolve_callable` / `load_module_from_worktree` are defined (Step 3.1 required the seam) but never exercised by a test (the runners use `run_prefix_replay_snippet` / `read_source_from_worktree`). | Add a NEW `tests/troubleshoot/backtest/test_replay_executor.py` that exercises the seam: a stub invoker → `InProcessReplayExecutor.replay(...)` returns the expected `ReplayResult`; a missing-invoker → `VERDICT_ERROR`; a raising invoker → `VERDICT_ERROR` (error folding); `resolve_callable` correctly distinguishes a module-level function from a class-bound method and reads its signature (resolve against the live `superclaude.cli.prd.gates` module-level `_check_parallel_instructions` and a class method, or a small local module). This makes the seam exercised (no longer orphaned) without forcing the runners to route through it. | coherence |
| P5-3 | MINOR | `git_replay.py` `checkout_worktree` teardown | Robustness: if THIS process's own worktree somehow ends up locked, `remove --force` + `prune` cannot reap it. | Add a best-effort `git worktree unlock <wt>` (wrapped in the same `try/except (TimeoutExpired, FileNotFoundError, OSError)`) BEFORE the `remove --force` in the `finally`, so a lock on our own worktree is cleared first. Does NOT touch other processes' worktrees. | green-semantics |
| P5-4 | MINOR | `conftest.py` | `replay_scratch_root` / `catch_rate_output_dir` yield-fixtures are annotated `-> Path` but should be `-> Iterator[Path]` (they `yield`). | Annotate the yield fixtures `-> Iterator[Path]` (import `Iterator` from `collections.abc`). `catch_rate_output_dir` returns (not yields) — it stays `-> Path`. | conftest |
| P5-5 | MINOR | `conftest.py` docstrings | The docstrings overclaim that `_pollution_snapshot` "fails the session on ANY `docs/` write"; the root guard actually watches specific `docs/` paths (e.g. `docs/mistakes/`, `docs/memory/`). | Soften the docstring to say the report-output fixture is `tmp_path`-rooted and never writes under `docs/`, without overstating the guard's exact scope. | conftest |
| P5-6 | IMPORTANT | `phase-outputs/test-results/pytest-backtest-summary.md` | The summary presents "0 failed / exit 0 / GREEN" as deterministic, but a re-run under concurrent load produced 1 failed (the P5-1 flake). | After P5-1 lands, RE-RUN `uv run pytest tests/troubleshoot/backtest/` and re-capture the raw output + summary; add a one-line note that the no-leak test is now concurrency-robust (scoped assertion) and that the integration tests SKIP on CI (shallow clone). | green-semantics |
| N-1 | MINOR (NO change) | `test_backtest_e4.py` "UNMERGED" comment | Agent nit: `b97c9960` object exists but isn't a HEAD ancestor. | NO change — research/08 confirms `b97c9960` is NOT merged into master (`git merge-base --is-ancestor b97c9960 master` → not merged); "UNMERGED" (into master) is accurate. | coherence |

## Fix routing

All code fixes are under `tests/troubleshoot/backtest/` (+ a new `test_replay_executor.py` + a re-captured summary under `phase-outputs/`). Per I20, ONE serialized rf-qa fix agent applies P5-1..P5-6, must keep the suite green-or-correctly-skips, re-run + re-capture the summary (P5-6), and confirm `ruff check` + `ruff format --check` clean. Stress-test the rewritten no-leak test serially (e.g. 8×) to confirm determinism.

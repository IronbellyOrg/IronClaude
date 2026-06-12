# QA Report — Domain Harness Coherence (E1-E5 Differential Backtest)

**Topic:** End-to-end wiring of the troubleshoot-hardening differential backtest harness
**Date:** 2026-06-12
**Phase:** doc-qualitative (adapted: domain end-to-end chain coherence audit)
**Fix cycle:** N/A
**Stance:** Adversarial — assumed ≥3 broken links; hunted, did not confirm.

---

## Overall Verdict: **FAIL**

Three broken links found (one of which fires an actual, reproducible test failure). The
catch-rate / `backtest_status` half of the chain is sound; the replay-execution half has a
fully-orphaned designed seam and a teardown-robustness gap that intermittently breaks the
G3 no-leak invariant.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Chain wired end-to-end: git-replay-helper → ReplayExecutor seam → per-escape runner → CatchRateReport → backtest_status | **FAIL** | `ReplayExecutor` seam is orphaned — see BL-1. The other links (`run_prefix_replay_snippet`/`checkout_worktree` → EscapeResult → CatchRateReport → backtest_status) ARE wired and exercised. |
| 2 | `backtest_status` reads `not_run` today / `partial` / `complete` correctly | **PASS** | `not_run` confirmed live (all 6 refs absent → `_collect_escape_results()` returns `[]`); `complete`/`partial` arms exercised hermetically by `test_catch_rate_aggregation.py:159-277` (passed). See Verified Behavior. |
| 3 | No orphaned module / no missing link | **FAIL** | `replay_executor.py` executor seam orphaned (BL-1). Teardown chain incomplete for locked worktrees (BL-2). Stale "UNMERGED" comment is a non-blocking nit (N-1). |

---

## Summary

- Checks passed: 1 / 3
- Checks failed: 2 (concern #1 wiring, concern #3 orphan/missing-link)
- Critical issues: 1 (BL-2 — reproducible test failure)
- Issues fixed in-place: 0 (report-only, `fix_authorization: false`)
- **Confidence:** Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 16 | Grep: 4 | Glob: 1 (find) | Bash: 11

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| BL-1 | IMPORTANT | `replay_executor.py:80-193` (+ `read_module_from_worktree`, `resolve_callable`, `ResolvedCallable`, `ReplayResult`, `ReplayInvoker`, `VERDICT_ERROR`) | The designed `ReplayExecutor` Protocol / `InProcessReplayExecutor` "spawn → observe" seam — named explicitly in concern #1 as the chain's middle link — is **never imported or exercised by any test**. Repo-wide grep returns ZERO external references. The 5 per-escape runners bypass it entirely, calling `run_prefix_replay_snippet` (E1-E4) / `read_source_from_worktree` (E5) directly. The seam, its `ResolvedCallable`/`resolve_callable`/`load_module_from_worktree` signature-adaptation machinery, and the `VERDICT_ERROR` fold-to-ERROR path are dead code. | Either (a) route the per-escape runners through `InProcessReplayExecutor.replay(escape, worktree)` via injected invokers (the design the docstring claims), making the seam live and unit-testable with a stub `ReplayExecutor`; or (b) delete the orphaned seam and document that `run_prefix_replay_snippet` IS the executor. As-is, concern #1's named chain is not wired. |
| BL-2 | CRITICAL | `git_replay.py:204-211` (teardown `remove --force`) and `:217-224` (`prune`) | The G3 "no leaked worktree" teardown cannot reap a worktree caught in a `locked` state. Mechanically confirmed (git 2.43): single `git worktree remove --force` on a locked worktree FAILS `fatal: cannot remove a locked working tree; use 'remove -f -f' to override or unlock first` (exit 128), AND `git worktree prune` does NOT reap a locked admin record. `test_backtest_replay_leaves_no_leaked_worktree` FAILED on ~2 of ~9 full-suite runs, leaking `/tmp/backtest-replay-*/wt HEAD 94d5baa0… detached / locked initializing`. The leak originates from a `run_prefix_replay_snippet` checkout (E1's parent 94d5baa0) racing into `locked initializing` against the shared common-dir (`/config/workspace/IronClaude/.git`) while running from inside a worktree. | Make teardown locked-safe: `git worktree unlock <wt>` (best-effort) before remove, OR use `remove --force --force` (double `-f`), AND/OR `git worktree prune --expire=now`. Without this the G3 invariant — the harness's whole reason for existing as a no-side-effect replay — is intermittently violated. |

### Non-blocking nit (documented, not a chain break)

| # | Severity | Location | Issue | Note |
|---|----------|----------|-------|------|
| N-1 | MINOR | `git_replay.py:52-54`, `test_backtest_e4.py:14-17,76` | Comments label E4 fix `b97c9960` as "UNMERGED", but the object IS present in local history. Verified harmless: `b97c9960` is NOT an ancestor of HEAD (cherry-picked/dangling), so "unmerged" is effectively true; and E4 replays against the *parent* `1b0264f1` regardless of the fix sha. Comment-only; does not affect the chain. |

---

## Verified Behavior (concern #2 — the part that PASSES)

- **`not_run` TODAY:** All 6 hardening refs (`runtime-entrypoint-verification.md`,
  `unmask-and-sweep.md`, `contract-enumeration.md`, `effective-input-proof.md`,
  `pipeline-hardening-closure.md`, `hardening-output-contract.md`) are ABSENT under
  `src/superclaude/skills/sc-troubleshoot-protocol/refs/` (verified by `ls`). So
  `_collect_escape_results()` (`test_catch_rate_aggregation.py:53-91`) returns `[]` →
  `_derive_backtest_status(())` → `not_run` (`catch_rate.py:126-130`). The aggregation test
  asserts `total_escapes == 0, caught == 0, backtest_status == "not_run"` and PASSES (the 5
  parametrized escape tests SKIP with the not_run reason).
- **`complete` / `partial` once refs land:** Exercised hermetically with synthetic
  `EscapeResult`s by `test_backtest_aggregation_complete_and_partial_derivations`
  (`test_catch_rate_aggregation.py:159-277`) — `complete` (5×CATCH+witness+card, rate 1.0,
  no missing ids) and `partial` (1 MISS surfaces its id). The anti-vacuity invariant
  (`catch_rate.py:119-130`, `:158-201`) correctly blocks `complete` on all-CATCH-but-missing
  witness/card (`test_catch_rate_schema.py:201-252`). All passed. The "once all 5 refs land"
  path will derive `complete` only via `_collect_escape_results`'s present-ref→CATCH+card
  mapping — that live arm is currently unreachable but its logic is proven by the hermetic test.
- **Separation invariant:** `production_signoff` stays `advisory` for not_run/partial and only
  mirrors the run-level verdict at complete (`catch_rate.py:207-217`,
  `test_backtest_status_separation.py`, passed).
- **Wired links that DO exist:** `checkout_worktree` (used by E5 + integration + unit + the
  `run_prefix_replay_snippet` subprocess path) → `EscapeResult` (built in every E1-E5 runner) →
  `build_catch_rate_report` → `CatchRateReport.__post_init__` derivation → `backtest_status`
  serialized through `to_dict()` → schema-validated (`test_catch_rate_schema.py`). This spine is sound.

---

## Reproduction (BL-2)

```
# ~15-20% of full-dir runs fail; reproduced twice independently:
uv run pytest tests/troubleshoot/backtest/ -q     # observed: 1 failed, 31 passed, 11 skipped
#   FAILED test_git_replay_integration.py::test_backtest_replay_leaves_no_leaked_worktree
#   leaked: worktree /tmp/backtest-replay-fscq0g7p/wt / HEAD 94d5baa0… / detached / locked initializing

# Mechanism proof (git 2.43):
git worktree lock <wt>; git worktree remove --force <wt>   # -> exit 128 "cannot remove a locked working tree"
git worktree prune                                          # -> locked record survives
git worktree remove --force --force <wt>                    # -> only this cleans it
```

E1-E5 parents are ALL present locally (`git cat-file -e`), so the E1-E4 OLD=MISS tests
genuinely run real `git worktree add` via `run_prefix_replay_snippet` — 4 real adds + E5's
checkout + 2 integration checkouts per session, all against one shared common-dir, which is what
surfaces the `locked initializing` race the single-`--force`/`prune` teardown cannot reap.

---

## Self-Audit

**(a) Reliance — none.** No inherited structural verdict supplied; ran standalone, verified every
claim with own tool engagement (no reliance on other reports).

**(b) Independent semantic checks (≥1 required):**
- Orphan claim (BL-1): repo-wide `grep` for the executor-seam symbols → ZERO external refs (own Grep).
- Leak claim (BL-2): reproduced the live test failure 2× via `pytest` + characterized flake rate
  over 9 runs; proved the git-locked-worktree mechanism with a controlled `worktree lock/remove/prune`
  experiment (own Bash).
- `not_run` TODAY (concern #2): `ls` of the refs dir + ran the aggregation test → confirmed empty
  collection → not_run (own Bash + Read).
- E4 provenance nit (N-1): `git merge-base --is-ancestor b97c9960 HEAD` → not an ancestor; confirmed
  comment-only (own Bash).

---

## Recommendations

1. **BL-2 (CRITICAL) first** — make `checkout_worktree` teardown locked-safe (unlock + double-force
   + `prune --expire=now`). This is the only finding that fails CI today.
2. **BL-1 (IMPORTANT)** — decide: wire `InProcessReplayExecutor` into the per-escape runners (honor
   the documented design) OR delete the orphaned seam and re-document `run_prefix_replay_snippet` as
   the executor. Current state contradicts concern #1's named chain.
3. **N-1 (MINOR)** — refresh the E4 "UNMERGED" comments to "present-but-not-in-HEAD (cherry-picked),
   replayed against parent regardless."

## QA Complete

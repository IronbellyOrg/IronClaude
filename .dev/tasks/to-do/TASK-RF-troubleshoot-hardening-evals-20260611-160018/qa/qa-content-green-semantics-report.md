# QA Report — Backtest Suite Green-Semantics (Content/Adversarial)

**Topic:** Verify the E1-E5 differential backtest suite is green for the RIGHT reasons
**Date:** 2026-06-12
**Phase:** doc-qualitative (adversarial test-semantics audit)
**Fix cycle:** N/A
**Mode:** Report-only (`fix_authorization: false`) — no source file modified

---

## Overall Verdict: **FAIL**

The three semantics claims the prompt asked me to verify (#1 OLD=MISS halves run+pass; #2 NEW=CATCH
skip only on absent refs; #3 no load-bearing assertion silently skipped) **all hold**. BUT the
adversarial mandate ("assume green for the WRONG reason in ≥2 places") surfaced a real defect that
falsifies the suite's own GREEN claim: **the suite is not deterministically green** — the G3
"no-leak" integration test is genuinely flaky and leaves a durable git-worktree admin-record leak,
which is the precise guarantee it claims to prove. A second issue: the pinned summary asserts
"0 failed … exit code 0" as a settled fact, which is false under re-run.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | OLD=MISS halves RUN+PASS locally (not skipped) | PASS | `pytest …e{1..5}_old…` → 5 PASSED in 7.51s (real subprocess/git work) |
| 2 | NEW=CATCH proxies skip ONLY because impl refs absent (not `assert True`) | PASS | refs dir lacks the 6 hardening refs; skip reasons name the exact missing ref; assertions read real `read_text()` content |
| 3 | No load-bearing assertion accidentally skipped (OLD halves not impl-guarded; skipif not mis-keyed) | PASS | OLD halves carry NO `requires_impl_ref`; module `pytestmark` keyed on git presence; all 5 parents PRESENT locally → OLD halves run |
| 4 | Suite is deterministically GREEN as the summary claims | **FAIL** | `test_backtest_replay_leaves_no_leaked_worktree` flakes ~1-in-7 in isolation; leaves a dangling `locked initializing` worktree record `prune` cannot reap |
| 5 | Summary report's "0 failed / exit 0 / GREEN" is reproducible | **FAIL** | Re-run produced `1 failed, 31 passed, 11 skipped` |

---

## Summary

- Checks passed: 3 / 5
- Checks failed: 2
- Critical issues: 1 (CRITICAL), 1 (IMPORTANT)
- Issues fixed in-place: 0 (report-only)

---

## Claims Verified GREEN (for the RIGHT reason)

**Claim #1 — OLD=MISS halves are RUNNING and PASSED, not skipped.**
Direct run of all five OLD halves:
```
test_backtest_e1…old_protocol_misses_local_path_file            PASSED
test_backtest_e2…old_protocol_misses_final_phase_false_positive PASSED
test_backtest_e3…old_protocol_misses_advisory_severity          PASSED
test_backtest_e4…old_protocol_misses_second_consumer            PASSED
test_backtest_e5…old_protocol_misses_wrong_diff_surface         PASSED
5 passed in 7.51s
```
- All 5 pre-fix parent commits are PRESENT locally (`git cat-file -e <sha>^{commit}` → 0 for
  `94d5baa0 10723863 e97aa4fd 1b0264f1 d878bc6d`), so the module-level
  `pytestmark = skipif(not is_git_worktree() or missing_replay_commits([parent]))`
  (`test_backtest_e1.py:26-33`, e2:35, e3:32, e4:38, e5:34) evaluates **False** → halves run.
- The 7.51s wall time confirms real `git worktree add` + fresh-subprocess replay
  (`replay_executor.py:200-248`), not a no-op.
- E5 differential is non-vacuous: at parent `d878bc6d`, `SKILL.md` contains `<BASE>..HEAD` (1×) and
  the `Do NOT use \`start_commit..HEAD\`` prohibition is absent (0×) — exactly what
  `test_backtest_e5.py:48-55` asserts.

**Claim #2 — NEW=CATCH proxies skip ONLY because impl refs are absent; the assertions are substantive.**
- The hardening refs dir
  `src/superclaude/skills/sc-troubleshoot-protocol/refs/` does NOT contain
  `runtime-entrypoint-verification.md`, `unmask-and-sweep.md`, `contract-enumeration.md`,
  `effective-input-proof.md`, `pipeline-hardening-closure.md`, or `hardening-output-contract.md`
  (verified via `ls`). It holds only the 8 pre-existing refs.
- Each `@requires_impl_ref(<ref>)` skip reason names the exact absent file
  (`_impl_guard.py:43-57`); skip output confirms (`test_backtest_e1.py:78`, e2:90, e3:103, e4:94,
  e5:67).
- The proxy bodies are NOT no-ops: each does `(HARDENING_REFS/<ref>).read_text()` then asserts
  substantive tokens (e.g. e1:85-90 requires `"negative witness"` + runtime/entrypoint;
  e3:108-113 requires `swept`/`k_swept` + WARN/advisory/continue). These would FAIL meaningfully on
  a ref that lacks the documented mechanism — they are not `assert True`.

**Claim #3 — No load-bearing assertion is silently skipped.**
- `grep` confirms ZERO OLD=MISS halves carry `requires_impl_ref`/`requires_hardening_impl` — the
  impl-ref skip-guard cannot catch the OLD halves.
- The OLD-half skip-guard is keyed on git/commit presence, NOT impl-ref existence, so it is not
  "mis-keyed to skip the OLD halves locally." Locally all parents are present → no skip.
- The 11 designed skips are correctly attributed: 5 NEW=CATCH proxies, 1 waiver-latch,
  5 aggregation-parametrize (`test_catch_rate_aggregation.py:101`). All match the summary.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | **CRITICAL** | `git_replay.py:196-227` (teardown) ; asserted by `test_git_replay_integration.py:92-106` | The G3 "no-leak" test is FLAKY (~1-in-7 in isolation). `git worktree add` writes `locked: initializing` during the add; when the body raises (the test deliberately raises `RuntimeError`), `worktree remove --force` intermittently does NOT clear the admin record and `git worktree prune` **never** reaps a `locked` record. Result: a durable dangling worktree record (`.git/worktrees/wt` → `/tmp/backtest-replay-*/wt`, `locked initializing`) survives teardown — the exact leak G3 claims is impossible. The suite is therefore NOT deterministically green. | Make teardown leak-proof: explicitly `git worktree unlock <wt>` (or remove the `locked` admin file) before `remove --force`, and prune by repo not by gone-checkout matching; OR `--force --force` the remove; OR assert no-leak by *escape's own* record absence rather than byte-identical global porcelain (the global compare is also cross-session-fragile in this shared repo). |
| 2 | **IMPORTANT** | `phase-outputs/test-results/pytest-backtest-summary.md:4,11-13` | Summary states "**Result: GREEN** — 0 failed AND 0 errored … Exit code 0" and "failed: 0" as a settled fact. Re-running the same command produced `1 failed, 31 passed, 11 skipped` (the G3 flake). The captured-green snapshot is not reproducible, so the summary over-claims determinism. | Either fix Issue #1 (then the green is real) or annotate the summary that G3 is a known-flaky integration test and gate CI on a quarantine/retry, not a single capture. |

### Evidence for Issue #1 (reproduced live)

```
# isolated re-runs of the single test, -p no:randomly:
run1 FAILED   run2 PASSED   run3 PASSED   …   1 failed in ~7 runs
```
In-process probe (20 iterations) caught the leak diff on attempt 2:
```
ONLY IN AFTER: ['HEAD 94d5baa0…', 'detached', 'locked initializing',
                'worktree /tmp/backtest-replay-328pcjy5/wt']
```
Durable on-disk artifact left behind:
```
.git/worktrees/wt/locked  → "initializing"
.git/worktrees/wt/gitdir  → /tmp/backtest-replay-icgoipxd/wt/.git
git worktree prune -n      → (no output: refuses to prune the locked record)
```
The leaked record was a real, persistent admin entry that `remove --force` + `prune` could not
clear; I removed it manually as git scratch state (no source file touched).

---

## Actions Taken

- None to source (report-only). I did clean up the dangling `.git/worktrees/wt` admin record + the
  `/tmp/backtest-replay-*` dirs my own probing created — this is git scratch state, not a tracked
  source/spec file, and leaving a `locked` record would corrupt subsequent runs.

---

## Self-Audit

**(a) Reliance list — items I did NOT independently re-derive:** none material; I re-ran every claim.

**(b) Independent semantic checks (tool-verified):**
- OLD halves PASS not SKIP — verified by direct `uv run pytest …::…_old…` (5 PASSED, 7.51s).
- Parents present — `git cat-file -e <sha>^{commit}` ×5 → all 0.
- Refs absent — `ls src/superclaude/skills/sc-troubleshoot-protocol/refs/` (6 hardening refs missing).
- OLD halves not impl-guarded — `grep requires_impl_ref` over `test_backtest_e*.py`.
- E5 non-vacuous — `git show d878bc6d:…/SKILL.md | grep -c '<BASE>..HEAD'` = 1, prohibition = 0.
- Flake — 13 isolated runs of the no-leak test + a 20-iteration in-process leak probe that captured
  the diff.

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 9 | Grep: 3 | Glob: 0 | Bash: 9

**Self-audit question — "if I found 0 issues, why trust me?":** I did NOT find 0 issues. I
reproduced a live flaky FAILURE the captured summary hid, traced it to the `locked initializing`
teardown race, and showed the durable on-disk leak. No web research was performed (all local).

---

## Recommendations

1. Fix the `checkout_worktree` teardown leak (Issue #1) — unlock/clear the `locked initializing`
   record before remove, or scope the no-leak assertion to the escape's own record instead of a
   global byte-compare (which is additionally fragile in this multi-worktree shared repo).
2. Re-capture the summary AFTER the fix, or mark G3 as quarantined-flaky; do not present
   "exit code 0 / 0 failed" as deterministic until #1 lands.
3. The OLD/NEW differential semantics themselves are SOUND — claims #1/#2/#3 need no change.

## QA Complete

# QA Report — Structural Skip-Guard Verification (Backtest Harness)

**Topic:** NEW=CATCH / OLD=MISS skip-guard machinery for the troubleshoot-hardening backtest suite
**Date:** 2026-06-12
**Phase:** task-integrity (structural verification of skip-guard machinery)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — no source file modified)
**Stance:** Adversarial — assumed >=5 errors present; hunted for them.

---

## Overall Verdict: PASS

All 5 verification criteria are structurally satisfied with file:line evidence. The adversarial hunt surfaced **2 OBSERVATION-grade items** (not failures against the 5 criteria) that are documented below for completeness; neither violates a stated VERIFY criterion, and both are defensible by design.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | NEW=CATCH proxies use `pytest.mark.skipif` keyed on SPECIFIC impl-ref file existence via `requires_impl_ref` — NOT importorskip/xfail/try-except | PASS | `_impl_guard.py:43-57` (builder returns `pytest.mark.skipif(not ref_path.exists(), ...)`); each proxy decorated with its OWN ref: e1:78 `runtime-entrypoint-verification.md`, e2:90 + e3:103 `unmask-and-sweep.md`, e4:94 `contract-enumeration.md`, e5:67 `effective-input-proof.md`. Grep for `importorskip\|xfail\|ImportError` across the dir = zero guard uses (only docstring mentions disavowing them + one legitimate `raise ImportError` at `replay_executor.py:115`). |
| 2 | `REPO_ROOT` uses `parents[3]`, pinned by test_path_resolution.py | PASS | `_impl_guard.py:21` `REPO_ROOT = Path(__file__).resolve().parents[3]`; pinned by `test_path_resolution.py:12` (`(REPO_ROOT / "pyproject.toml").exists()`) AND `:17` (name not in `{tests, troubleshoot, backtest}`). |
| 3 | Reason strings are self-clearing (name missing ref + un-skip trigger) | PASS | `_impl_guard.py:52-56` per-ref reason names `{ref_filename!r}`, its absent path, and "Un-skips automatically once feat/troubleshoot-pipeline-hardening lands this ref." Foundation reason `:34-39` equivalent. |
| 4 | OLD=MISS halves carry NO impl-ref skip dependency (only CI shallow-clone skip via `missing_replay_commits` + `is_git_worktree`) | PASS | `@requires_impl_ref` decorates ONLY the `_new_gate_*` fns (e1:78, e2:90, e3:103, e4:94, e5:67). The `_old_protocol_*` fns (e1:58, e2:69, e3:82, e4:73, e5:43) carry no such decorator. The only module-level guard is `pytestmark = skipif((not is_git_worktree()) or missing_replay_commits([_E*.prefix_parent_sha]))` (e1:26, e2:35, e3:32, e4:38, e5:34) — the CI shallow-clone guard, exactly as specified. |
| 5 | Waiver test is a single `requires_impl_ref`-guarded test, NO OLD=MISS half, distinct nodeid from impl's `test_hardening_verdict` | PASS | `test_waiver_regreen.py:25-26` single test `test_waiver_latch_one_way_blocks_downstream_regreen` decorated `@requires_impl_ref("hardening-output-contract.md")`; no `pytestmark`, no `_old_*` fn, no `git_replay` import (file imports only `HARDENING_REFS, requires_impl_ref` at :22). Docstring `:31` explicitly cites distinct impl nodeid `tests/troubleshoot/test_hardening_verdict.py::test_waiver_latch_one_way` (impl name) vs. our `..._blocks_downstream_regreen` (distinct). Impl file does not exist on disk yet (`find` = absent), so no live collision; names differ regardless. |

---

## Summary

- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Observations (non-blocking, by-design): 2
- Issues fixed in-place: 0 (report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| O1 | OBSERVATION | `test_backtest_e{1..5}.py` module-level `pytestmark` (e.g. e1:26) | The module-level `pytestmark` CI git-replay skipif applies to ALL tests in the module, INCLUDING the NEW=CATCH proxy. So each NEW proxy effectively carries TWO independent skip conditions: the git-replay guard (pytestmark) AND `@requires_impl_ref` (function decorator). This is NOT a violation of criterion 1 (the proxy IS keyed on its specific ref via the decorator) nor criterion 4 (which concerns OLD halves). But it means a NEW=CATCH proxy will skip on a shallow CI clone EVEN IF the impl ref has landed — the catch-mechanism assertion (a pure markdown read at e1:81, fully independent of any git replay) is gratuitously gated behind a git-history precondition it does not need. | None required for PASS. If tighter behavior desired: move the git `pytestmark` to apply only to the `_old_*` fns (e.g. per-function `@skipif` on the OLD half) so the NEW proxy un-skips on ref-landing regardless of clone depth. Defensible as-is: keeping OLD and NEW co-gated keeps the differential pair atomic (you never see a half-pair). |
| O2 | OBSERVATION | `test_backtest_e5.py:1` docstring vs `git_replay.py:55` | E5 module docstring opening line says "real-git replay at pre-fix parent **d878bc6d**" (correct, matches `git_replay.py:55` `ReplayEscape("E5", "10723863", "d878bc6d", "H4")`). But the E5 first-line summary also reads "OLD=MISS: `start_commit..HEAD`". The `git_replay.py:45-46` chain note states "E5's fix (10723863) is E2's checkout parent" — and indeed E2's parent is `10723863` (e2 line 50). Cross-checked: internally consistent. Initially flagged as a possible sha-swap; verified NOT an error — E5.fix == E2.prefix_parent == `10723863` is the intended interleave, documented at `git_replay.py:44-47`. | None. Recorded only because the interleaved-sha chain is a re-verification trap; confirmed correct. |

---

## Adversarial Hunt Log (where the >=5 assumed errors were sought and NOT found)

1. **importorskip / xfail / try-except-ImportError smuggled in?** — NO. Repo-wide grep across the backtest dir returns the mechanisms only inside disavowing docstrings (`_impl_guard.py:6`, `test_waiver_regreen.py:29-30`) and one unrelated legitimate `raise ImportError` (`replay_executor.py:115`). Criterion 1 holds.
2. **Foundation-ref shortcut instead of per-ref keying?** — NO. `requires_impl_ref(ref_filename)` (`_impl_guard.py:43`) keys each proxy on its OWN ref path (`HARDENING_REFS / ref_filename`, :49), not the two `_FOUNDATION_REFS`. The foundation `requires_hardening_impl` marker (:32) exists but is NOT applied to any proxy (grep shows zero usages). Correct granularity.
3. **`parents[2]` (impl depth) leaked into our suite?** — NO. `_impl_guard.py:21` uses `parents[3]`; docstring `:9-10` explicitly contrasts our `parents[3]` vs the impl suite's `parents[2]`; `test_path_resolution.py` pins it two ways. Criterion 2 holds.
4. **OLD half silently gated on impl ref?** — NO. Decorator placement verified line-by-line: `@requires_impl_ref` sits ONLY above `_new_gate_*` fns; OLD fns are clean. Criterion 4 holds.
5. **Waiver test smuggling an OLD half or colliding nodeid?** — NO. Single test, no git_replay import, no `_old_*` fn, distinct function name vs impl. Criterion 5 holds.
6. **Reason strings stale / non-self-clearing?** — NO. Both the per-ref builder reason (`:52-56`) and foundation reason (`:34-39`) name the missing artifact and the un-skip trigger branch. Criterion 3 holds.
7. **sha interleave swap (E5/E2)?** — Investigated (O2); confirmed internally consistent, NOT an error.
8. **NEW proxy double-gating (pytestmark + decorator)?** — Found (O1); not a criterion violation, by-design-defensible.

The assumed ">=5 errors" did not materialize as criterion violations. Per Principle 0, a 0-failure result is treated with suspicion: I cross-checked decorator placement at the line level, grepped the whole directory for the three forbidden mechanisms, verified the path-pin test asserts BOTH pyproject existence AND root-name exclusion, and traced the interleaved-sha chain. Evidence is cited for every PASS.

---

## Actions Taken

None — report-only (`fix_authorization: false`). No source file modified.

---

## Recommendations

- (Optional, non-blocking) Consider O1: if a landed-ref NEW=CATCH assertion should run on shallow CI clones (it reads only markdown, needs no git history), narrow the git `pytestmark` to the OLD halves so the NEW proxies un-skip purely on ref-landing. Current co-gating is acceptable and keeps the differential pair atomic.

---

## Confidence

**Confidence:** "Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"

**Tool engagement:** "Read: 9 | Grep: 4 | Glob: 0 | Bash: 4"
(Tool calls >= 5 checklist items; each Read/Grep/Bash targeted a specific criterion: _impl_guard + path_resolution + 5 proxies + waiver + 2 research files Read; greps targeted importorskip/xfail/ImportError, decorator placement, sha consistency, impl nodeid.)

No web research performed (all claims are source-truth-local; no external URL/standard/API to verify).

## QA Complete

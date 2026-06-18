# QA Report — Structural Concurrency-Correctness Lens

**Topic:** Sprint-CLI 429 / account-exhaustion recovery — Phase 4 re-spawn loop
**Date:** 2026-06-17
**Phase:** task-integrity (concurrency-correctness lens, READ-ONLY)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — no files modified)

---

## Overall Verdict: PASS

The re-spawn loop's concurrency design is correct. Spawn is unlocked; latch
check, latch trip, and the shared-budget increment+snapshot are all guarded;
the same `SessionResetPolicy` is shared per phase across all K workers; the loop
is hard-bounded by `max_session_resets`; and the one lock-split (budget-claim vs
latch-trip in separate `with guard:` blocks) is provably race-free because both
mutated quantities are monotonic/privately-owned. Adversarial pass found 0
CRITICAL and 0 IMPORTANT concurrency defects; 2 MINOR observations (non-blocking).

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Subprocess spawn stays OUTSIDE the lock (unlocked) | PASS | `executor.py:1024-1032` — `subprocess_factory(...)` / `_run_task_subprocess(...)` are NOT inside any `with guard:`. The two preceding (1013-1016) and the budget/latch blocks (1060-1062, 1069-1070) are the only guarded regions in the loop body; the spawn sits between the latch-precheck block and the detector, unguarded. Docstring 987-990 + comment 1024 corroborate. |
| 2 | Latch CHECK and latch TRIP both happen UNDER `guard` | PASS | CHECK: `with guard: _latched = reset_policy._latch_tripped` (`executor.py:1014-1015`). TRIP: `with guard: reset_policy._latch_tripped = True` (`executor.py:1069-1070`). `guard = lock if lock is not None else contextlib.nullcontext()` (`executor.py:995`). |
| 3 | Shared-budget increment + snapshot happen UNDER `guard` | PASS | `with guard: reset_policy._exhaustion_attempts += 1; attempt = reset_policy._exhaustion_attempts` (`executor.py:1060-1062`). Increment and snapshot are in the SAME critical section, so the read-modify-write and the ordinal capture are atomic together. This is exactly what makes the storm bound deterministic. |
| 4 | SAME `SessionResetPolicy` instance shared across K>1 workers | PASS | Constructed once per phase: `reset_policy = SessionResetPolicy(...)` at `executor.py:1328-1331` (guarded by `if reset_policy is None`, so an injected instance is reused; never reconstructed per worker). Threaded to the parallel path `reset_policy=reset_policy` (`executor.py:1350`), and inside `_execute_phase_tasks_parallel` every `_worker` closes over the same `reset_policy` and passes `reset_policy=reset_policy` to `_run_one_task` (`executor.py:1230`). `_latch_tripped` and `_exhaustion_attempts` are instance fields (`recovery_policy.py:47-48`), hence sprint-wide. |
| 5 | Loop bounded by `max_session_resets` (no unbounded/infinite loop) | PASS | `decide` returns `RETRY_NEW_SESSION` only while `attempt < self.max_session_resets`, else `HALT_MODEL_SWITCH` (`recovery_policy.py:68-71`). `attempt` is the monotonically-increasing shared ordinal (`executor.py:1062`), never reset within a phase, so it strictly climbs to `cap` and the loop `break`s (`executor.py:1071-1075`). The only `continue` (1066) is gated behind `RETRY_NEW_SESSION`. Single worker → exactly `cap` spawns; K>1 storm bounded `cap ≤ total ≤ cap+(K-1)` and `< K×cap` (see Storm-Bound Proof). |
| 6 | No lock-discipline hazard (no unsafe check-then-act on the latch) | PASS | The only split critical section is budget-claim (1060-1062) → unlocked `decide()` (1063) → latch-trip (1069-1070). Proven race-free: see Lock-Discipline Analysis below. |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 2 (non-blocking observations)
- Issues fixed in-place: 0 (read-only lens)

---

## Storm-Bound Proof (Claim 5, K>1, all-429 single-account)

Let `cap = max_session_resets`, `K` workers.

1. Each worker that observes a `SINGLE_ACCOUNT_LIMIT`/`ALL_ACCOUNT_COOLDOWN`
   signal claims a **unique, strictly-increasing** ordinal under the lock
   (`executor.py:1060-1062`). No two workers can claim the same ordinal (the
   `+=` and the read are in one critical section).
2. `decide` returns `RETRY` for ordinals `1..cap-1` and `HALT` at ordinal `==cap`
   (`recovery_policy.py:68-71`). The worker that claims ordinal `cap` trips the
   latch (`executor.py:1070`).
3. Because the spawn is **unlocked** (`executor.py:1024-1032`), at the instant the
   latch trips, up to `K-1` sibling workers may already be mid-spawn. Each such
   in-flight worker contributes **at most one** overshoot spawn: on its next loop
   iteration it either hits the locked latch-precheck and bails with 0 new spawn
   (`executor.py:1013-1022`), or — if it already 429'd this iteration — claims an
   ordinal `> cap`, gets `HALT`, and `break`s (no further spawn).
4. Therefore `cap ≤ total_spawns ≤ cap + (K-1)`. Strict upper bound vs storm:
   `cap + (K-1) < K·cap` holds for `cap ≥ 2` (the P3 K>1 test uses `cap=3`).
   Matches manifest invariant #2 and spec §4 Layer 3 / edge case #3, and the task
   item's literal "loop-local counter" wording is correctly superseded by the
   spec-mandated SHARED budget (per p3-aggregate IMPORTANT note, lines 6-11).

This bound is achievable **only** because the increment+snapshot is atomic
(Claim 3). A per-worker counter — the literal task wording — could not satisfy it
(each worker would burn its own `cap`, yielding `K×cap`). The deviation is
spec-correct.

## Lock-Discipline Analysis (Claim 6)

The budget-claim block (`executor.py:1060-1062`) and the latch-trip block
(`executor.py:1069-1070`) are SEPARATE `with guard:` acquisitions with an
unlocked `decide()` (1063) between them. This is **not** a hazardous
check-then-act, for two independent reasons:

- **`attempt` is privately owned.** Once a worker snapshots its ordinal under the
  lock, no other worker can observe or mutate that local. `decide(signal.kind,
  attempt)` (1063) is a pure function (`recovery_policy.py:50-72` — no side
  effects, confirmed) over already-captured values, so running it unlocked is
  safe. Releasing the lock before `decide` is correct: it keeps `decide` off the
  critical path (a real concurrency win, not a bug).
- **`_latch_tripped` is monotonic (write-once-direction).** It only ever
  transitions `False → True` (`executor.py:1070`; no code path sets it back —
  grep of all `_latch_tripped` references shows one read 1015 and one write 1070).
  Multiple workers writing `True` is idempotent. A stale-`False` read at the
  precheck (1015) can only cause **one extra** spawn, already counted in the
  `K-1` overshoot bound — it can never **skip** a spawn that should occur. Hence
  no torn-state, no lost-update, no missed-halt race.

The latch precheck uses the correct snapshot-then-act pattern: read into a local
`_latched` under the lock (1014-1015), then branch on the local (1016) — the
branch body does not re-read shared state, so there is no TOCTOU window that
matters given monotonicity.

The remaining shared mutations in the loop tail (ledger debit/credit, post-task
hooks, `TaskResult` build) all run under the same `with guard:` (`executor.py:1099`),
consistent with the K>1 contract documented at 988-990.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `executor.py:1052-1059` (comment) / loop | `attempt` is updated both as a local (`session_resets = attempt`, 1065/1073) and as the shared ordinal. The per-task `session_resets` persisted for a K>1 worker is therefore the **global** ordinal at claim time, not that task's private retry count (e.g., worker B's first 429 may persist `session_resets=2`). This is internally consistent with the shared-budget model and the comment at 1052-1059 documents it, but the field name `session_resets` reads as per-task. Non-blocking: telemetry semantics only, no control-flow impact. Consider a doc note on the field or a per-task counter for reporting. |
| 2 | MINOR | `executor.py:1013-1016` | Two lock acquisitions per iteration on the hot precheck path (one for latch read, later one for budget). Under high K this is mild lock churn but correctness is unaffected (each is a tiny critical section). No action required; noted for completeness. |

## Actions Taken
None — read-only lens (`fix_authorization: false`). No files modified.

## Recommendations
- Concurrency-correctness lens: GREEN. No blocking findings. Proceed.
- The two MINOR items are telemetry/perf observations, not correctness defects,
  and do not gate the phase. If a future phase persists `session_resets` into an
  operator-facing report, clarify it is a global ordinal under K>1.

## Confidence Gate

- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 2 | Glob: 0 | Bash: 2
  (All 4 source files read in full or in the relevant ranges: p3-aggregate.md,
  sprint-429-recovery-spec.md, recovery_policy.py, executor.py loop+both call
  sites+per-phase construction; monitor.py signal/detector cross-checked. Grep
  confirmed every referenced symbol — `detect_provider_failure`,
  `ProviderFailureSignal.kind/.resolved_model`, `_task_completed_before_overrun`,
  `SessionResetPolicy`, `import threading`/`contextlib`, all `reset_policy` and
  `_latch_tripped` references — exists.) No web research required (no external
  claims on this lens).
- Tool-call count (10) ≥ checklist items (6): not suspect.

## QA Complete

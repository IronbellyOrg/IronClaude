---
artifact: r1-3-proceed-decision
phase: 8
release: R1.3
task: TASK-RF-20260531-042405
created_date: 2026-06-02
gate: PG8.2
verdict_source: phase-outputs/reviews/r1-3-rf-qa-task-integrity.md
decision: PROCEED to Phase 9 (R1.4)
---

# PG8.2 — R1.3 Proceed Decision

## Verdict: PASS → PROCEED to Phase 9 (R1.4 tool-write rewrite)

PG8.1 rf-qa task-integrity gate returned **PASS** (cycle 1, 0 CRITICAL, 0
blocking, 14/14 criteria verified, 100% confidence). No fix cycle required.

## What R1.3 delivered (substrate complete)

- `GateCriteria.code_assertions: list[CodeAssertion] | None = None` slot
  (`cli/pipeline/models.py`) — additive, default None, backward-compatible.
- `CodeAssertion` dataclass with the §MVR §2 `(PipelineEnvelope, Path) ->
  Finding | None` widened-access contract.
- First two CodeAssertions in `cli/roadmap/code_assertions.py`:
  `assert_step_reachable` (dispatch-reachability, wired into CERTIFY_GATE)
  and `assert_envelope_artifacts_present` (envelope-coverage analogue).
- `gate_passed` dispatch branch for code_assertions (keyword-only
  `envelope`/`repo_root`, NFR-007-preserving duck typing).
- `build_certify_step` now has a genuine production caller
  (`_run_certify_after_remediate` ← `execute_roadmap`), killing the
  master:§Flaw 1 zero-caller condition for the certify case.
- `test_dispatch_reachability.py` (7 tests) makes Contract #2 CI-enforceable;
  mutation-verified by rf-qa to genuinely fail if wiring is removed.

## Mandatory carry-forward into R1.6 (do NOT lose)

The certify code_assertion is currently enforced via the **CI test only**.
The live runtime gate path (`cli/pipeline/executor.py`) calls `gate_passed`
WITHOUT `envelope`/`repo_root`, so the documented backward-compat shim
returns True and the assertion is dormant at pipeline runtime. **R1.6 MUST
delete the shim AND plumb `envelope` + `repo_root` into the live gate-eval
call sites**, or the assertion stays permanently dormant in production. This
is captured in Follow-Up Items (High priority) and in the Phase Gate
Findings PG8.1 entry.

## Step-count budget status (Acceptance gate #6)

Live executed step count = 14 (`ALL_GATES`/`_get_all_step_ids`), ≤ 14. R1.3
added certify execution dynamically (not in `_build_steps`), so no
consolidation was needed. The budget-pressure point is R1.5
(`verify-implementation`), which R1.6 consolidates (candidate:
`wiring-verification`, superseded by `verify-implementation`).

## Next phase

Proceed to **Phase 9 (R1.4 — Tool-Write Rewrite for the 9 LLM steps)**, the
longest sub-phase. Per the Phase 9 bundling-hardening notes (H3/H4/H5):
interim rf-qa checkpoints after Step 9.5 and Step 9.10; Step 9.11 secondary
migrations as individually-completable sub-actions; cutover-counter design
(`.dev/migrations/r1-4-cutover-counters.yaml`) before Step 9.2.

**Session-pacing note:** Phase 9 is a large, multi-step phase (Steps 9.1–9.12
+ interim gates + PG9). Per the established cadence (HALT for user
confirmation before launching a major new phase), Phase 9 launch is a
natural checkpoint for user review of the R1.3 result before committing to
the longest sub-phase.

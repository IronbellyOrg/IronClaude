# Remediation Report — v4.3.5 Sprint Auto-Resume UC-2 Reflection Audit (CG-4, F-3, F-2, F-4)

**Task:** TASK-RF-20260603-sprint-resume-remediation
**Date:** 2026-06-03
**Driving audit:** `.dev/reflect/post-sprint-auto-resume-20260603003009/REPORT.md` (UC-2; promotion BLOCKED on strict-gate conditions 4 & 8)

## Executive Summary

The four actionable items from the UC-2 reflection audit were remediated:

- **CG-4 (spec self-contradiction, HUMAN DECISION):** Surfaced; an operator-facing decision record was
  produced with both options neutral and a marked recommendation. **RULING = YES + F-2-as-prerequisite
  (operator Ryan W, 2026-06-02).** The executor (post-completion) applied the YES-branch reconciling
  amendment: `design.md` §4(c) conjunct re-worded to `(partial reported AND (quarantined OR
  --yes/assented))`; `merged-requirements.md` FR-2.4 clarified that "`--yes` + a printed partial-paths
  report" == "explicitly assessed-and-accepted". §7 and `integrity._verdict` unchanged (already §7). **F-1
  closed as-designed** (no gate change, no `--accept-partial`); the F-2 prerequisite already landed.
  §7/§4(c)/FR-2.4 are now consistent — the contradiction is **RESOLVED**. (Initially recorded PENDING
  during the run; the executor correctly did not auto-default — F-2/F-3/F-4 proceeded independently while
  CG-4 awaited the operator.)
- **F-3 (HIGH, regression-class):** Fixed with the principled whitespace-normalized-hash approach. Same-ID
  material edits to a completed task now score <0.8 (AC-5) while true whitespace-only edits stay 0.9 (AC-4).
- **F-2 (MED-HIGH, drift):** Fixed with Option A — `BoundaryReport.partial_paths`, populated unconditionally
  and printed on the report-only path.
- **F-4 (MED, coverage gap):** Fixed with the planner→model→integrity co-dependency — the PHASE hard-crash
  path now double-validates the prior completed phase's tail (AC-3 :141-143).

Each fix landed with its RED→GREEN coverage-gap test and passed an adversarial rf-qa task-integrity gate.

## Findings table

| Finding | Fix Applied | Coverage-Gap Test | RED→GREEN | QA Gate Verdict | Fix Cycles Used |
|---------|-------------|-------------------|-----------|-----------------|-----------------|
| **CG-4** | Decision record → **RULING: YES** (operator); YES-branch amendment applied (design §4(c) + merged-req FR-2.4; §7/`_verdict` unchanged); F-1 closed as-designed | n/a (consistency check, post-ruling PASS) | n/a | Phase-1 self-verification PASS | 0 |
| **F-3** | `_normalize_whitespace` + `_content_sha256_ws_excluding_rerun_block`; persist `tasklist_sha256_ws`; drift fall-through keeps 0.9 only on WS-hash match else <0.8 | CG-2 `test_drift_same_id_material_body_edit_low_conf` | ✅ (`0.9<0.8` fail → pass) | **PG.2 PASS** | 0 |
| **F-2** | `BoundaryReport.partial_paths` (Option A); assigned in `run()` independent of cleanup; printed in `_print_resume_decision` | CG-1 `test_boundary_partial_paths_surfaced_in_report` | ✅ (AttributeError → pass) | **PG.3 PASS** | 0 |
| **F-4** | `BoundaryTask.phase` field; planner `_emit_prior_tail_boundary` (write-free); integrity resolves transcript+deliverables under `lc.phase` (`_phase_file`) | CG-3 positive + negative companion | ✅ (`assert ([])` → pass) | **PG.4 PASS** | 0 |

## Source files modified

- `src/superclaude/cli/sprint/rerun_tasks.py` — new `_normalize_whitespace`, `_content_sha256_ws_excluding_rerun_block` (F-3).
- `src/superclaude/cli/sprint/executor.py` — `_write_phase_result_json` persists `tasklist_sha256_ws` (F-3).
- `src/superclaude/cli/sprint/resume/drift.py` — WS-hash gated fall-through + `_current_sha_ws`/`_recorded_sha_ws` (F-3).
- `src/superclaude/cli/sprint/resume/models.py` — `BoundaryReport.partial_paths` (F-2) + `BoundaryTask.phase` (F-4).
- `src/superclaude/cli/sprint/resume/integrity.py` — `partial_paths` assignment (F-2); `_validate_last_completed` phase-correct resolution + `_phase_file` (F-4).
- `src/superclaude/cli/sprint/resume/planner.py` — `_emit_prior_tail_boundary` + `parse_tasklist_file` import (F-4).
- `src/superclaude/cli/sprint/commands.py` — partial-paths print loop in `_print_resume_decision` (F-2).
- `tests/sprint/test_resume.py` — CG-1/CG-2/CG-3 + CG-3 negative; `_build_task_interrupted` WS-hash co-edit; `test_resume_hard_crash_phase_level` reconciliation.

## Spec files amended

- `.dev/brainstorms/20260602-sprint-auto-resume-default/design.md` — §2 (persisted-hash note + `BoundaryReport.partial_paths` + `BoundaryTask.phase`), §4(a) (prior-tail validation), §4(b) (`partial_paths` "always"), §5 (DD-4 `tasklist_sha256_ws` amendment).
- `.dev/brainstorms/20260602-sprint-auto-resume-default/merged-requirements.md` — **FR-2.4 amended** (CG-4 YES ruling): `--yes` + printed partial-paths report == "explicitly assessed-and-accepted".
- `.dev/brainstorms/20260602-sprint-auto-resume-default/design.md` §4(c) — partial conjunct re-worded per the YES ruling (`(partial reported AND (quarantined OR --yes/assented))`); §7 unchanged.
- New: `.dev/brainstorms/20260602-sprint-auto-resume-default/cg4-decision-record.md` (operator decision record; RULING: YES).

## Full-suite test result

`uv run pytest tests/sprint/ -v --continue-on-collection-errors` → **999 passed, 54 failed, 2 collection errors**.

- **Everything F-3/F-2/F-4 touched is GREEN:** `test_resume.py` 21/21 (incl. CG-1/CG-2/CG-3 + negative); `e2e_real/test_e2e_resume*` 7/7; all pre-existing resume invariants (AC-4, AC-5, quarantine-nondestructive, planner-no-writes, hard-crash).
- **All 54 failures + 2 errors are PRE-EXISTING and UNRELATED** (proof in `final-test-summary.md`): 48× fake-`Popen`-lacks-`.stdin` (executor subprocess tests; `executor.py` has no `.stdin` reference and my diff is 2 additive hunks in `_write_phase_result_json`); 6× `IndexError` in `test_e2e_success.py`; 2× `invoke_haiku` ImportError (F-5 rename, commit `70ef6486`).

## verify-sync / lint result

- `make verify-sync` → **✅ All components in sync** (this task touched only the pure-Python resume subsystem; no skills/agents/commands changed).
- `make lint` → **✅ All checks passed** (clean after every code change and final whole-repo pass).

## Promotion Readiness

**Both strict-gate conditions that blocked promotion are now CLEAR:**

- **Condition 4 (drift==0 AND regression==0):** ✅ F-3 (regression-class) fixed → AC-5 same-ID material edits STOP; F-2 (drift) fixed → partial paths surfaced. Locked by CG-2/CG-1.
- **Condition 8 (needs_human_decision==false):** ✅ **CLEARED** — operator Ryan W ruled CG-4 = YES (2026-06-02); the YES-branch spec amendment is applied and F-1 is closed as-designed. No outstanding human decision.
- **F-4 (coverage gap):** ✅ closed — the PHASE hard-crash path now double-validates the prior phase's tail (AC-3).

**Next step (operator):** (1) **Re-run sprint auto-resume promotion** — conditions 4 and 8 are both clear. (2) Optionally clear the pre-existing `invoke_haiku` collection failures (Follow-Up, Low) to unblock the full sprint suite collection. The CG-4 ruling and Step 1.5 amendment are DONE — no further executor action is required on the spec.

## Open Questions surfaced

- **CG-4 (HUMAN DECISION) — ✅ RESOLVED:** operator ruled YES + F-2-as-prerequisite (2026-06-02); spec amended, F-1 closed as-designed.
- **Pre-existing `invoke_haiku` collection failures** (Low) — unrelated F-5 rename; out of this task's scope.

## QA gate reports aggregated

- `phase-outputs/reviews/pg2-rf-qa-report.md` (F-3) — PASS, 4 MINOR citation fixes.
- `phase-outputs/reviews/pg3-rf-qa-report.md` (F-2) — PASS, 0 fixes.
- `phase-outputs/reviews/pg4-rf-qa-report.md` (F-4) — PASS, 0 fixes.
- `phase-outputs/reviews/cg4-consistency-check.md` (Phase 1) — PASS (PENDING-path during run; post-ruling re-check PASS, contradiction RESOLVED).

# QA Report — Task Integrity (Phase 4 / F-4 Remediation)

**Topic:** v4.3.5 sprint auto-resume gate — F-4 (PHASE hard-crash prior-tail double-validation)
**Date:** 2026-06-03
**Phase:** task-integrity (adversarial stance, fix_authorization: true)
**Fix cycle:** N/A (first pass)

---

## Overall Verdict: PASS

All 10 acceptance checks verified against the actual files with file:line evidence.
The multi-file co-dependency (model field + planner emit + integrity phase-correct
validation) landed and interlocks correctly. 10/10 CG-3 + invariant tests pass on an
independent re-run; the GREEN artifact matches byte-for-byte. No fixes were required.

One **out-of-scope, pre-existing** repo issue was found (2 unrelated test modules fail
collection due to an earlier `invoke_haiku`→`invoke_sonnet` rename); it is NOT an F-4
defect and does NOT block this gate. Documented below.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Full multi-file co-dependency present & interlocks | PASS | `models.py:58` `phase: int \| None = None`; planner sets `phase=prior` `planner.py:227`; integrity reads `lc.phase` `integrity.py:120,138-141`. Three pieces interlock. |
| 2 | Planner stayed write-free | PASS | `_emit_prior_tail_boundary` `planner.py:182-229` uses only `parse_tasklist_file`/`discover_phases` (read_text) + in-memory `plan.boundary_tasks.append`. `grep` for write surface in planner.py → NONE. `test_planner_performs_no_writes` PASS (byte-identical results/). |
| 3 | Guarded for no-prior-phase | PASS | `planner.py:202-206`: `prior = max((n for n in completed_phases if n < interrupted), default=None)`; `if prior is None: return` (emits nothing, preserves empty boundary). Also guards `prior_phase is None` `:207-209` and empty `entries`/missing `tail_id` `:214-217`. |
| 4 | Integrity resolves PRIOR phase (transcript AND deliverables), not interrupted_phase | PASS | Transcript: `lc_phase = lc.phase if lc.phase is not None else plan.interrupted_phase` `integrity.py:120`, passed to `_read_transcript(results_dir, lc_phase, ...)` `:126`. Deliverables (the critical one): `:138-141` branches to `self._phase_file(plan, lc.phase)` when `lc.phase != interrupted_phase`, NOT `phase_file`. Traced: if it had used `phase_file` (P3), `_declared_deliverables(P3, "T02.01")` → `block_match is None` → `[]` → `all([])`=vacuous True → negative test could never STOP. Confirmed via `_declared_deliverables` `rerun_tasks.py:961-985`. |
| 5 | Gate performs REAL (non-vacuous) double-validation | PASS | `test_resume_hard_crash_prior_tail_overclaim_stops` `test_resume.py:196-223`: P2 declares deliverable, never written → `artifacts_ok=False` → `validated_last is False`/`passed is False`. Traced logic at `integrity.py:142-152`. Test PASS on re-run. |
| 6 | Verdict deterministic (NFR-3) | PASS | `_verdict` unchanged: `return accept_suspect or report.validated_last` `integrity.py:336`. `grep` for git/subprocess in integrity.py → NONE. No git dependency introduced. |
| 7 | CG-3 RED→GREEN | PASS | `cg3-red.txt`: both tests FAIL on `assert ([])` (boundary empty). `cg3-green.txt`: 10 passed. GREEN matches my independent re-run byte-for-byte. |
| 8 | Transcript-source question resolved & documented | PASS | Task file `### Phase 4 Findings` lines 403-406 record RESOLVED → transcript; Signal B via `_classify_transcript(_read_transcript(results_dir, lc_phase, lc.task_id))` keyed on `lc.phase`; result.json rejected (carries only status). Matches code `integrity.py:126-129`. |
| 9 | §4(a) amendment matches code AND reconciles with AC-3:141-143 | PASS | `design.md` §4(a) `:164-191` describes prior-tail emit with `phase` field + resolution under `lc.phase`; §2 BoundaryTask note `:61`. AC-3 (`merged-requirements.md:141-143`) "last completed task (phase 2 tail) is double-validated first" — amendment is no longer narrower. |
| 10 | Reference-test reconciliation correct, not silent regression | PASS | `test_resume_hard_crash_phase_level` `:142-164` now asserts `[bt.role ...] == ["last_completed"]` and `boundary_tasks[0].task_id == "T02.01"`. Documented in `f4-test-summary.md` §"Reference-test reconciliation" + task Open Questions line 342. Correct: fixture's P2 has single task T02.01. |

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Confidence

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 5 | Glob: 0 | Bash: 6 (no web research performed)

Tool-call count (18) exceeds the 10-item checklist minimum — not suspect.
Every VERIFIED item cites a specific file:line or test-run result above.

## Adversarial probes performed (and what they ruled out)

1. **Vacuous-True deliverable trap (the central F-4 risk).** Traced that the deliverable
   lookup uses `_phase_file(plan, lc.phase)` (PRIOR phase P2), not `phase_file` (interrupted
   P3). Confirmed `_declared_deliverables` returns `[]` on an unmatched task block
   (`rerun_tasks.py:978`), which is exactly the silent-pass failure mode — and confirmed the
   code avoids it. The negative test genuinely exercises this path.
2. **Positive test passing for the wrong reason.** Checked the positive test's
   `validated_last is True` comes from a real re-derivation (PASS_TRANSCRIPT classified PASS +
   present absolute-path deliverable), not from a vacuous artifacts check.
3. **Regression in the Haiku PHASE case** (`test_haiku_coherence_advisory_only` (b)): the new
   prior-tail emit produces a `last_completed` on the PHASE path, but `_advisory_coherence` is
   gated on `granularity is TASK` (`integrity.py:357`), so `invoke_sonnet` stays at 0 calls.
   Test PASS confirms.
4. **Planner write surface** — grep for `write_text|mkdir|shutil|open|unlink` in planner.py: NONE.
5. **Git/non-determinism creep** in integrity — grep for `git|subprocess`: NONE.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | OUT-OF-SCOPE (pre-existing, non-blocking) | `tests/sprint/test_retrospective.py:34`, `tests/sprint/test_summarizer.py:28` | Both import `invoke_haiku` from `summarizer`, which was renamed to `invoke_sonnet` in commit `70ef6486` ("replace haiku defaults with sonnet"). Full `tests/sprint/` collection errors on these 2 modules. | NOT an F-4 defect — F-4 never touched `summarizer.py` or these test files, and F-4 code correctly uses `invoke_sonnet` (`integrity.py:385`). Recommend a separate follow-up to update the 2 stale test imports. Does not affect the F-4 gate. |

## Actions Taken

No fixes applied — all 10 F-4 acceptance checks passed on first verification. The one issue
found is a pre-existing, out-of-F-4-scope test-import staleness (item 1 above), which is
recorded as a recommendation rather than fixed in-place (fixing unrelated stale tests would
exceed the Phase 4 F-4 scope and the `task-integrity` mandate).

## Recommendations

- Proceed to Phase 5 — F-4 QA gate is PASS.
- (Separate, non-blocking) File a follow-up to rename `invoke_haiku`→`invoke_sonnet` in
  `tests/sprint/test_retrospective.py` and `tests/sprint/test_summarizer.py` so the full
  `tests/sprint/` suite collects. This is repo-wide debt from commit `70ef6486`, unrelated to F-4.

## QA Complete

VERDICT: PASS
FIXES APPLIED: (none — 0 F-4 issues; the one finding is pre-existing/out-of-scope and recorded as a recommendation)

# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: general-purpose agent, model inherited from the orchestrator (claude-gw-tier1b). Disclosure from the agent: it did not open the debate transcript; for counts, import safety and the per-cycle edit count it grepped the current worktree, which already holds code built from this design (commit `0b8a5801d`), used only for import facts.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | The plan gives the implementer enough to supply `applied_edits` as a per-cycle count to `release_decision` | UNADDRESSED | MEDIUM | Spec 107 says THIS cycle's count; plan 70, 75, 124 repeat it; nothing says where a per-cycle count comes from (the SKILL output table only has the run-wide field). Task 1 O1 covers the id, not the count. |
| INV-002 | state_variables | The fold's `cycle_id` always names the latest guarded cycle, because `held_cycle_published` compares against it | UNADDRESSED | MEDIUM | Spec 190 lists `cycle_id` as a fold field; effect table 196-206 never says when it is set. A fix-2 normal push after fix-1 could read as unpublished and keep the PR draft after resume (safe side, but uncaught by single-cycle fixtures at plan 60 and 62). |
| INV-003 | collection_boundaries | A single-guard-cycle run is the only boundary needing scenario coverage | UNADDRESSED | LOW | Plan 166 and 169 name no two-cycle sequence with the record in RELEASED at the next engage (spec 141, 143); `baseline` and `original_is_draft` must survive (spec 184). |
| INV-004 | guard_conditions | Wave 0's "or when the run log already holds guard events" trigger is tested with `--resume` | UNADDRESSED | LOW | Plan 137 and 140 assert `--resume`, position, gate wording and the off line only; spec 58 and 241 define two triggers. |
| INV-005 | collection_boundaries | Decision rows 2-7 can read `guard.phase` while `guard` is None on a first engage | ADDRESSED | LOW | Spec 134-138 vs 142; plan 70 requires one case per row, so the row 10 and 11 cases force None-safe code. |
| INV-006 | guard_conditions | Resume row 4 can re-enter `release_decision` without stating `applied_edits` and `target_sha` | UNADDRESSED | LOW | Plan 77 and spec 166 omit them; release row 7 (spec 155) precedes the head check (spec 156). |
| INV-007 | interaction_effects | Task 10's new SKILL.md Wave 6 text does not touch an already classified line | ADDRESSED | LOW | Plan 150 says new sentences after the pinned ones; plan 22 warns a classified line edit makes its entry stale; plan 155 runs `test_worker_contract.py`, so a break fails loudly. |

Checked and consistent (no finding): counts agree between plan and spec (45 members, 11/9/9 rows, 12 test names, 7 sets in `test_idempotency.py`); no import cycle for `merge_guard`; no front-matter edit needed for the new script (`test_allowed_tools_cover_every_program`).

## Summary

- **Total findings**: 7
- **ADDRESSED**: 2
- **UNADDRESSED**: 5
  - HIGH: 0
  - MEDIUM: 2 (INV-001, INV-002; warnings, do not block convergence)
  - LOW: 3 (INV-003, INV-004, INV-006)

Sufficiency verdict of the probe: "following this plan alone produces the feature" is falsified in the narrow sense by INV-001 and INV-002, which the plan and the spec both leave unspecified. None is HIGH.

# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis (opus class, general-purpose agent, independent of the advocates)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Writing three fixed values for the lens-scale cell plus one acceptance line is enough to repair C-001 | UNADDRESSED | HIGH | One `labels` cell feeds two readers that need different answers: the stage 2 import tier (STAGE2:57) and `ReviewerJudge` and the Task 12 matrix (PLAN:151, PLAN:192), which read IMPORTANT as blocking (SPEC:211, SPEC:592). `agents/rf-qa.md:111` also lets a reviewer grade an IMPORTANT finding minor ("a finding labelled IMPORTANT that is only wording is minor", re-read by the orchestrator). `IMPORTANT=Blocking`: reviewer-minor IMPORTANT rows are dropped by an importer that never writes Blocking rows; `IMPORTANT=Medium`: the shadow comparison reads IMPORTANT as non-blocking (the `card_convert` error SPEC:592 forbids) and reviewer-blocking IMPORTANT rows arrive without `why not blocking` and are refused; `IMPORTANT=Conditional`: no tier (the original C-001). Repair direction: stage 2 takes blocking or non-blocking from the reviewer's own grade (a filled `why not blocking`), and the scale map only splits non-blocking rows into Medium and Note, or Task 3 adds a second column |
| INV-002 | state_variables | `MINOR=Note`, the value all three advocates ended near, is safe for stage 2 | UNADDRESSED | HIGH | Non-blocking rows under the old rule are MINOR; with `MINOR=Note` every one goes to the Notes table, which has only `id`, `location`, one line and `status` (SPEC:371): no tags, `rests_on` or `why_not_blocking`; Notes are never swept (STAGE2:42); the `consumer-unknown` share would print a false 0 (STAGE2:148); the `protected-risk-dispute` tag has no column (PLAN:206). `MINOR=Medium` avoids all of this |
| INV-003 | interaction_effects | C-005 (consent logic unowned) and C-007 (`pending` not an item state) are separate nits | UNADDRESSED | MEDIUM | Both come from one gap: no task builds or writes the Offers table (grep of the four plans: only PLAN:82 reference text and STAGE2:148 "no stage 2 carrier writes it"); `pending` is an Offers state (SPEC:375); T8 is a stage 1 exit test (SPEC:945) and Task 8's acceptance line (PLAN:140) says it must be covered. Fault-finder asks to raise the grade or give Task 8 the REQ-11 check |
| INV-004 | collection_boundaries | Grading C-003 (`unsettled`) non-blocking is enough on its own | UNADDRESSED | MEDIUM | `unsettled` appears once across the four stage plans (PLAN:87) and no plan produces it; the spec requires it (SPEC:439, SPEC:596); a grade without an owner loses it |
| INV-005 | count_divergence | Every count in the consensus matches the live repo | ADDRESSED | LOW | 16 tasks, 15 `Depends on:` lines, 11 definition files, 11+1+2+5=19 registry rows, tasklist count 9, 12 families, 14 worked cases, 9 names in the `__init__.py` tuple (7 modules exist): all re-checked |
| INV-006 | guard_conditions | The T2 reverse scan in Task 15 covers the new stage 1 files | UNADDRESSED | LOW | The scans read `git ls-files` (`tests/skills/test_review_severity_rule.py:36-39`) and the plan stages only `.dev/tasks` (PLAN:30), so the scan sees tracked `doctor.py` but not `rule.md`, `scale-map.md` or `registry.yaml`; "the reverse scan accepts `refs/rule.md`" (PLAN:240) is meaningful only in a temporary tree (the plan says so) |
| INV-007 | state_variables | The "no `src/superclaude` path" fix (M-F7) is complete wherever needed | UNADDRESSED | LOW | Task 3 spells paths without the prefix (PLAN:62); Task 6 requires "a source path that exists" (PLAN:113) with no spelling rule; the folder grep at PLAN:115 catches a mistake, so the cost is a retry |
| INV-008 | sufficiency_challenge | F1-F9 and M-F1-M-F10 are fixed in every place they appear | ADDRESSED | LOW | Fixes that appear twice are fixed in both places (F2 at PLAN:64, 70, 234, 241, 242; F9 at PLAN:82, 88, 124); the only stale copy is STAGE2:27 (C-008) |

## Summary

- **Total findings**: 8
- **ADDRESSED**: 2
- **UNADDRESSED**: 6
  - HIGH: 2 (INV-001, INV-002)
  - MEDIUM: 2 (INV-003, INV-004)
  - LOW: 2 (INV-006, INV-007)

Gate result: CONVERGENCE BLOCKED by 2 HIGH-severity UNADDRESSED invariants (INV-001, INV-002) until the refactor plan addresses them (it does: PC-01 rewrites the C-001 repair so that it is no longer a three-value one-liner; see `refactor-plan.md`). The two MEDIUM items are logged as warnings and carried into the merged card (INV-003 into C-005, INV-004 into C-003).

fault_finder_model_self_report: claude-gw-tier1a[1m] (Anthropic Claude, opus class)

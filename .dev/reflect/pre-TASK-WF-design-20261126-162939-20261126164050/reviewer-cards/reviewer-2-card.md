# Reflect Reviewer — Deviation Findings (reviewer 2, qa, model class haiku)

**Reviewer persona**: qa (requirement coverage and acceptance evidence)
**Grounding root**: /home/coder/workspaces/worktrees/IronClaude/issue-326
**Diff scope**: not applicable (pre-execution audit of the plan)
**Total deviations**: 10
**Reviewer verdict**: FAIL (contradictory checks and acceptance gaps)

Paths are shortened by the orchestrator: `PLAN` = `.dev/tasks/to-do/TASK-WF-design-20261126-162939/TASK-WF-design-20261126-162939.md`, `DESIGN` = `.dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md`, `REQ` = `.dev/brainstorms/20261126-115614-git-pm-workflows-skills/merged-requirements.md`. Content is the reviewer's, not edited. These are findings about the plan, not about an implementation.

## Deviations

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|---|---|---|---|---|
| 1 | Regression | PLAN:29 | Blocking (Decision): the global prohibition says "No code or text uses" the forbidden tokens; Tasks 3 and 29 must put those tokens into safety constants and refusal instructions, so delivering the required deny-list breaches the plan's own constraint. Limit the prohibition to executing or recommending bypasses. | PLAN:60, 334; DESIGN:167, 319 | HIGH |
| 2 | Drift | PLAN:245 | Blocking (Missing): the design says every invariant is tested, including person-only commit authority. Task 20's acceptance checks registry/checklist existence, helper names and classification rows; Task 24 adds structural checks but no assertion for rejecting agent/plan-origin writes, printing no command lines on refusal, or restricting a grant to one operation. The authorization text can be absent or weakened while the checks pass. | DESIGN:75, 82, 155; PLAN:282 | HIGH |
| 3 | Drift | PLAN:223 | Blocking (Missing): T-21 only partly demonstrated. Tasks 18 and 28 do not require crashing after the resolution append, resuming twice, proving exactly one settlement, or preserving outstanding outside-change pins through both answers; Task 28 omits the no-key reply rule and the redisplay-and-ask-again rule when disclosure changes. | DESIGN:387-393, 451; REQ:610; PLAN:327-328 | HIGH |
| 4 | Drift | PLAN:168 | Blocking (Missing): the staging-rule list omits exclusion of legacy run files under `.dev/implement/`; Task 14 builds on it; no acceptance case tests it. | DESIGN:228; PLAN:171-174, 183-184 | HIGH |
| 5 | Drift | PLAN:286 | Blocking (Decision): the repository-wide check allows only the cleanup implementation to contain a branch-deletion call; existing cleanup tests already run such calls, so Task 24's check cannot pass literally without editing files Task 1 reserves unchanged. Keep the check scoped to new production code. | `tests/worktree_cleanup/test_git_facts.py:217`; PLAN:41; REQ:631 ("No new code") | MEDIUM |
| 6 | Drift | PLAN:193 | Blocking (Missing): T-04's acceptance proves helper outcome classes but not the required refused sidecar line or absence of a same-run retry; Task 15's helper is read-only; Task 29 checks only file shape and classification. | DESIGN:443; PLAN:190, 337-338 | MEDIUM |
| 7 | Drift | PLAN:384 | Blocking (Missing): the no-flag regression check is "driven through `vcs reconcile --flag off`"; a read-only helper call cannot prove the executor avoids all extra Bash calls and files when no sidecar exists, nor that it appends exactly one `off` record when one exists. | DESIGN:365; PLAN:318, 210 | MEDIUM |
| 8 | Drift | PLAN:95 | Blocking (Missing): the helper's field-level contract is not fully checked: Task 6 does not check the `header_len` and `rule` fields; Task 17 omits `runs` and `segments`; Task 18's contract acceptance checks size, determinism, exits and verb names, not these schemas. | DESIGN:194, 196; PLAN:92-95, 210, 224 | MEDIUM |
| 9 | Drift | PLAN:334 | Blocking (Missing): the interface catalog's 40-line refusal-log limit has no implementation instruction or acceptance assertion; Tasks 5 and 18 cover JSON/list caps (different limits). | DESIGN:431; REQ:501 | MEDIUM |
| 10 | Drift | PLAN:27 | Blocking (Missing): "Behavior changes ship with tests" weakens the design's required test-first order inside every phase; no task requires writing and observing the failing test before changing code or text. | DESIGN:458 | MEDIUM |

## Unmapped IDs checked (reviewer's table, summarized by the orchestrator)

The reviewer accounted for all 67 entries of the first slice (the corrected 29-id list arrived after it finished and it kept its result: every id already has a disposition, and no deviation was raised solely because an id was unnamed).
- Not real requirements, no task needed: FR-024 to FR-029, FR-037, FR-055, FR-068, FR-069, FR-083 to FR-089, FR-119 (no active definition found; FR-055 and FR-068/069 are recorded as deleted in the merged requirements).
- Covered by a task: FR-003, FR-004 (Task 19); FR-007 (Tasks 20-23); FR-015, FR-016 (Tasks 25, 35, 38); FR-020, FR-021 (Task 20); FR-061 (Task 29); FR-106 (Tasks 17, 26, 27); FR-123 (Tasks 18, 28); FR-056, FR-057, FR-059 (Tasks 12, 26, 29); FR-074, FR-075 (Task 14); FR-104, FR-105, FR-109 (Tasks 11, 12, 14, 17, 29, 30); FR-111, FR-114, FR-115 (Tasks 16, 21, 27, 29, 30); FR-121, FR-122, FR-124, FR-125 (Tasks 18, 28); NFR-016 (Tasks 3-5, 10, 14, 18, 20, 26, 27); AC-02 to AC-15 and NFR-004, NFR-005, NFR-011, NFR-013 to NFR-015 and T-14, T-18 (various tasks, see its design-section table).
- Partly covered: NFR-007 (Tasks 5, 13, 18 cover JSON/list bounds; refusal-log bound is a real gap, row 9).

## Design sections 3 to 8 and 10 (reviewer's table, summarized)

All sections have assigned tasks (3: Tasks 19-25; 4: 3-18; 5: 9-18, 26-34; 6: 15, 16, 18, 21, 27-30; 7: 19, 25, 30-38; 8: 5, 6, 15, 17, 18, 20, 26, 27, 31, 32; 10: 1-38). Acceptance gaps: person-authority invariant (row 2), legacy-path exclusion and field-level output checks (rows 4, 8), hook-side-effect and no-flag proof (rows 6, 7), owner-resolution details (row 3), refusal-log cap (row 9), test-first order (row 10).

## Adherence summary

- Spec units audited: 191 (181 active id-defined units, nine invariants, the test-first instruction).
- Fully adherent: 170. Authorized expansion 0 | Necessary 0 | Drift 18 | Regression 3 (distinct affected units, overlapping findings counted once).
- The 199-id denominator of the brief includes 18 unused or deleted ids introduced by range expansion; not 199 active requirements.

## Notes

- T1 F1 confirmed and upgraded to Blocking (Decision). F2 confirmed, not a blocker for this executor (source order). F3 retained as an open review decision; whether the owner confirmed the DD-11 reading is UNVERIFIED.
- Read all 38 task bodies and acceptance blocks and the complete design. No tests or commands were run. Real hook-framework behavior, the git version floor and CI submodule behavior remain UNVERIFIED. Reviewer isolation was disabled; no snapshot-isolation claim.

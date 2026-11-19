# Diff Analysis: reviewer cards for plan v4 (UC-1 pre-execution)

Variants: V1 = reviewer-1-card.md (analyzer, sonnet), V2 = reviewer-2-card.md (qa, haiku), V3 = reviewer-3-card.md (refactorer, opus). Folder of the cards: `.dev/reflect/pre-TASK-WF-requirements-20261119-140750-20261119141121/reviewer-cards/`. Plan = `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md`. Orchestrator checks done before the debate (read in this run): `approval_record.py:313-359` (record_create has no input that tells a claim-time event from a plan approval); `cli.py:279` and `reads.py:142,148` (reread/events/edits called without a repo) and `github.py:37` (`REPO` constant); `source.md` R6 and R9 versus Task 27's body.

## Metadata
- Variants compared: 3
- Total differences found: 14 content points, 3 status contradictions, 5 unique contributions, 5 shared assumptions
- Categories: structural (3), content (14), contradictions (3), unique (5), shared assumptions (5)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Shape | Prose summary, Q-list, M-/N- findings, checked/not-checked | Table of 4 deviations with a coverage table | B-/M-/N- findings with evidence and fix, checked/not-checked | Low |
| S-002 | Grading scheme | Blocking none; Medium and Note | Labels Blocking in prose but its own severity column says MEDIUM | Blocking (Safety, Decision), Medium, Note with the affected action named | Medium |
| S-003 | Remediation recheck | Q-1 to Q-10 line by line | Q-1 to Q-10 as a table | Q-1 to Q-10 line by line | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Repo threading for the coordinator's approval read (`stage-status`, `reads.py`) | not found | not found | B-1 Blocking (Safety): reads IronClaude's issue for any repo | High |
| C-002 | Empty Pipeline against the unreadable-time rule (Tasks 3, 5) | not found | not found | B-2 Blocking (Decision): every empty-Pipeline issue refused | High |
| C-003 | Task 11: claim-time event refused as plan approval | not found | QA-2: no enforcement point exists | not found | High |
| C-004 | Task 13 guard pattern: must-refuse list and over-matches | M-5: `git`/`sed` on the pattern's files refused; pins not decided; N-1 GRID_CLASSES and import-time assert | QA-3: `p.complete.run()` alone matches no alternative | M-4: option "accept the over-match" contradicts the must-allow case; N-4 ISSUE fires outside command position | High |
| C-005 | Task 27 lacks R6 and R9 lifecycle content | not found | QA-1 | not found | High |
| C-006 | Task 11 brief test at Worktree, Full, Full Submit but the brief is level None only; Debug at None | not found | not found | B-3 | Medium |
| C-007 | `status` retry command has no stored Status or Pipeline | M-2 | not found | M-2 | Medium |
| C-008 | Task 5 needs the one live Project item; the helper is added in Task 7 | M-1 | not found | not found | Medium |
| C-009 | Task 9 warning cites `self.account_id`, a runtime value; check-config is offline | M-3 | not found | N-1 | Medium |
| C-010 | Same-file edits not ordered (Tasks 2, 10, 11; WORKER-CONTRACT.md) | not found | says order is sound | M-1 | Medium |
| C-011 | `/sc:pr-submit --monitor 3` posts through `gh api`, which the guard refuses at Full Submit | not found | not found | M-3 | Medium |
| C-012 | Goal sentence "can never write ... at any level" | not found | not found | M-5 | Medium |
| C-013 | Gated issues re-examined every cycle (budget) | M-4 [INFERRED] | not found | not found | Low |
| C-014 | Task 24 acceptance omits the R14 recheck; Task 19 allows several Projects, Task 24 says exactly one | not found | QA-4 | not found | Medium |

## Contradictions

| # | Point of conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is Q-1 fixed | FIXED | PARTIAL (QA-3) | FIXED | Medium |
| X-002 | Is Q-6 fixed | FIXED | FIXED | PARTIAL (no test that `marker_comments` ignores a result comment) | Low |
| X-003 | Is Q-10 fixed | FIXED | FIXED | PARTIAL (ordering line incomplete) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V3 | B-1 cross-repo approval read (verified by the orchestrator) | High |
| U-002 | V3 | B-2 empty Pipeline vs unreadable time | High |
| U-003 | V2 | QA-2 claim-time approval test has no enforcement point (verified) | High |
| U-004 | V2 | QA-1 R6 and R9 lifecycle missing from Task 27 (verified) | High |
| U-005 | V1 | M-1 helper order and N-1 GRID_CLASSES import-time assert | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Line numbers carried from plan v3 and the remediation proposal (cycle.py, launch.py, github.py, tests) still hold | all three cite them | A wrong line misleads an implementer | STATED as "not checked" by each card; UNSTATED as a plan risk |
| A-002 | An executor can do Task 4 (owner steps) inside `/sc:implement` | none of the cards questions it | Task 4 stalls the run unless the executor stops and asks | UNSTATED |
| A-003 | The guard is text-only, so a script or other HTTP client bypasses any pattern | V1, V3 | Pattern fixes are best effort | STATED |
| A-004 | The claim session at level None is ungoverned and has no store record | V1 verified, V3 inferred | Boundary of the Task 13 refusals | STATED |
| A-005 | Every acceptance check is run by the executor against faked runners only, so a cross-repo defect (C-001) shows no failing test unless one is written | all three | A missing test hides a live defect | UNSTATED |

## Summary
- Total structural differences: 3
- Total content differences: 14
- Total contradictions: 3
- Total unique contributions: 5
- Shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, C-004, C-005

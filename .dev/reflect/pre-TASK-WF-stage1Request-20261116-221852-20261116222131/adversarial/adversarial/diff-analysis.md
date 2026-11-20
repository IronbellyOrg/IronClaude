# Diff Analysis: reflect reviewer-card Comparison (UC-1 pre audit of the stage 1 plan)

Variants: V1 = reviewer 1 (analyzer, model class sonnet), V2 = reviewer 2 (qa, haiku), V3 = reviewer 3 (refactorer, opus). Files: variant-1-original.md, variant-2-original.md, variant-3-original.md in this folder. "plan" = `.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md`, "source" = the same folder's `source.md`.

## Metadata
- Generated: 2026-11-16T22:40:00Z
- Variants compared: 3
- Total differences found: 27
- Categories: structural (3), content (12), contradictions (2), unique (7), shared assumptions (3 promoted)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Card length and shape | 10 findings, several are confirmations of the Tier 1 card items | 2 findings plus a short coverage note | 8 findings, each with a quoted anchor | Low |
| S-002 | Severity labelling | every finding non-blocking | one finding blocking, one non-blocking | every finding non-blocking | Medium |
| S-003 | Coverage estimate presentation | about 90 percent, names three misses | about 95 percent, names missing source spans 3, 17, 51 | about 95 percent, names one miss | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Task 1 entry check and the ledger's package id | F1: the go in the ledger names another package (`...blockerStage1-20261116-030154`) | not raised | not raised | Medium |
| C-002 | Owner summary as the stage 3 entry evidence | F2 and F6: cut by Revision 4 but the ledger still expects it | not raised | not raised | Medium |
| C-003 | The stored-tag name `protected-risk-dispute` | F4: write the string into the plan sentence | not raised | F7: add an acceptance grep that prints nothing | Low |
| C-004 | The 35 percent target in the do-not-change list | F5: add it to the Also-not-built bullet | not raised | not raised | Low |
| C-005 | The Constraints ban on code-assigned severity against Task 1's outcome function (the GR12 raise-only function in `safety_route.py`, an invariant that never lowers an outcome and promotes a hit to Blocking) | F8 says Task 1's criteria can pass; no conflict named | F1 (blocking): plan:23 bans "code-assigned severity in `src/superclaude/cli/**/*.py`" while Task 1 requires exactly that; narrow the ban | F8 confirms the pinned scans stay green; no conflict named | High |
| C-006 | Second byte-equal twin pin | not raised | not raised | F2: `tests/commands/test_workflow_command.py:204-220` is missing from Task 2's pytest list and from Constraints | Medium |
| C-007 | `make lint` scope and baseline | not raised | not raised | F3: `ruff check .` covers the whole repo; "no new findings" has no baseline; use `ruff check` on the four new files | Medium |
| C-008 | Wording "recorded as partial" (unattended hit) and "stays blocking" (what blocking means for FINAL; an unattended run state) | not raised | not raised | F4: the two phrases can be read as archive-blocking or as a recorded partial run no task writes | Medium |
| C-009 | "every non-superseded minor line" vs the live lines 2 to m (which also hold note and dispute lines) | not raised | not raised | F5: say "every live line (lines 2 to m)" | Low |
| C-010 | Task 1 acceptance grep over `classif\|codec\|follow_up\|ledger` | F8: add "docstrings and comments avoid those words" | not raised | F6: restrict the grep to import lines | Medium |
| C-011 | Task 2 smoke check is a manual walk-through | F9: require the literal command output in `print-smoke.txt` | notes it is manual, no fix | not raised | Medium |
| C-012 | Source lines 3, 17 and 51 (generation prerequisite, acceptance-endpoint rule, entry check before creation) have no disposition | not raised | F2: add dispositions, applying Revision 4 | not raised | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Overall verdict | revise | revise | ship | High |
| X-002 | Whether the plan is jointly satisfiable by an executor: Task 1's required outcome function against the Constraints ban | F8: "The criteria can pass" (plan:44-52) | F1: "compliance contradictory even if all tests pass" (plan:23 vs plan:38) | F8: "none of the existing pins break" (about tests, not this conflict) | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V2 | The Constraints/Task 1 contradiction (C-005); the only blocking finding | High |
| U-002 | V3 | The second twin-pin test file missing from Task 2's pytest list (C-006) | High |
| U-003 | V1 | The entry check passes on a go recorded for another package id, and the owner-summary gate gap (C-001, C-002) | Medium |
| U-004 | V3 | `make lint` has no baseline to compare "no new findings" against (C-007) | Medium |
| U-005 | V3 | "stays blocking" can be read as an archive block (C-008) | Medium |
| U-006 | V1 | The 35 percent target omission (C-004) | Low |
| U-007 | V2 | Source spans 3, 17, 51 undispositioned (C-012) | Low |

## Shared Assumptions

Agreement points: all three treat Revision 4 as authoritative over the older text; all three treat the parsed ids R-001 to R-008 and REQ-09 as artifacts; none of V1 and V3 saw a Constraints/Task conflict; V1 and V2 treat the pytest list of Task 2 as complete.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|-----------|----------------|----------|
| A-001 | V1 F3, V3 F1, V2 F1 (all apply Revision 4) | Revision 4 replaces the earlier request text wherever they differ (source:59 "authoritative where it differs") | STATED | no |
| A-002 | V1, V3 (no conflict named) | An executor and the task reviewer see only the task text and the Constraints section, so a Constraints versus Task conflict is a defect even if every acceptance line can pass | UNSTATED | yes |
| A-003 | V1, V2 (Task 2 list taken as complete) | The 14 test files named in Task 2 are the complete set of tests the two edited files can break (a guard on the edit, an invariant of the pytest list) | CONTRADICTED by V3 F2 | yes |
| A-004 | V2, V3 (entry check accepted) | The ledger go row satisfies Task 1's entry check as written even though it names another package id | UNSTATED, questioned by V1 F1 | yes |

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-002 | Constraints versus Task conflict is a defect | High | open for debate |
| A-003 | pytest list is complete | Medium | open for debate |
| A-004 | go row satisfies the entry check | Medium | open for debate |

## Summary
- Total structural differences: 3
- Total content differences: 12
- Total contradictions: 2
- Total unique contributions: 7
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 1, CONTRADICTED: 1)
- Highest-severity items: C-005, X-001, X-002
- Debate points (S + C + X + A promoted): 20

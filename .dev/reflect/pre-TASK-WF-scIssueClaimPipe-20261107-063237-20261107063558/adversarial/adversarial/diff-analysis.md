# Diff Analysis: reviewer-card Comparison (UC-1 plan review, TASK-WF-scIssueClaimPipe-20261107-063237)

## Metadata

- Generated: 2026-11-07T06:50:00Z
- Variants compared: 3 (V1 = reviewer 1 / sonnet / analyzer; V2 = reviewer 2 / haiku / qa; V3 = reviewer 3 / opus / refactorer)
- Method note: the variants are structured review cards, not prose documents; "sections" are findings. Topic matching is by the plan task or design instruction each finding is about.
- Total difference points: 25 (structural 2, content 15, contradictions 4, unique contributions listed separately, promoted shared assumptions 4)
- Categories: structural (2), content (15), contradictions (4), unique (9 listed, not counted twice), shared assumptions (4 promoted of 6)
- Debate taxonomy tags (AD-5): L1 surface 4, L2 structural 14, L3 state-mechanics 7

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Advisory channel for no-spec correctness gaps | Present (3 gaps) plus a reviewer note on a citation | Absent | Present (3 gaps) plus notes | Low | L1 |
| S-002 | Use of the 4-class taxonomy | Regression x2, Drift x7 | Drift x5 only | Regression x1, Drift x9 | Medium | L2 |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | Existing inventory test goes red between Tasks 1/4 and 5/7 (intermediate repository state) | Found, Regression HIGH, with the Task 5 order hazard | Not found | Found, Regression HIGH | Medium | L3 |
| C-002 | Write-verb audit in test_worker_contract.py (per-line classification validation rule) hits the new template and script | Found, Regression HIGH, cites 1090-1155 and 2199-2208 | Not found | Not found | High | L3 |
| C-003 | Worktree output has no field for tracked files, but the final output needs it (interface gap) | Found, Drift MEDIUM | Not found | Advisory gap 2 | Medium | L2 |
| C-004 | launch output carries one warning but two can apply; enforcement_hook value on already_launched is undefined (state) | Found, Drift MEDIUM | Not found | Not found | Medium | L3 |
| C-005 | ST-4 forbidden-flag scan collides with existing text (--issue-url etc.) | Found, Drift MEDIUM | Not found | Advisory gap 1 | Medium | L2 |
| C-006 | Design test pins with no owning task: LA-7, ARG-1, ST-5 template row, ST-6 Wave 8 half | Found as one MEDIUM finding | LA-7 MEDIUM, ARG-1 LOW as two findings | ARG-1 + LA-7 MEDIUM, ST-5/ST-6 LOW | Medium | L2 |
| C-007 | Stale SKILL.md/command description and SKILL.md claim steps 6 and 7 | Description LOW | Description + step 6 LOW | Description MEDIUM, steps 6/7 MEDIUM | Medium | L1 |
| C-008 | Task 6 drops design step 5 and 6 safeguards (timeout detail, hand_command note, pending record stays) (launch-failure state) | LOW | MEDIUM | LOW | Medium | L3 |
| C-009 | No later task depends on Task 3 although Tasks 7 and 9 use its codes and text | Not found (says order is sound) | Not found | Found, Drift MEDIUM | Medium | L2 |
| C-010 | Orca-is-a-dependency constraint absent from plan Constraints | Not found | Found, LOW | Not found | Low | L2 |
| C-011 | Task 2 too large; lint gate only in last task; design-doc edits moved to Phase 3 (dependency/organization) | Not found | Not found | Found, three LOW findings | Low | L2 |
| C-012 | Other stale claim-mode text in the command file (issue.md:71, :100, Outputs row) | Found, LOW | Not found | Not found | Low | L1 |
| C-013 | Fork-safety guard: launch-prompt submit block implies a gh pr call; scan does not cover templates (validation rule) | Not found | Not found | Advisory gap 3 | Medium | L3 |
| C-014 | Pending-store intermediate directory modes: makedirs mode applies only to the leaf (boundary) | Advisory gap 1 | Not found | Not found | Low | L3 |
| C-015 | Naming and filter details: which field holds the already_launched time; -k "FO or worktree" over-matches | Advisory gaps 2 and 3 | Not found | Note on -k | Low | L1 |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is the C-001 red window a Regression? | Regression HIGH | Silent | Regression HIGH; calibrator called the label a stretch for a transient plan state | Medium |
| X-002 | Severity of C-007 (stale description / claim steps) | LOW | LOW | MEDIUM | Low |
| X-003 | Severity of C-008 (Task 6 dropped safeguards) | LOW | MEDIUM | LOW | Medium |
| X-004 | Is the ARG-1 gap real and how severe (inside C-006)? | MEDIUM (Task 1 cannot test it on preflight) | LOW (Task 1 tests bad args but only for preflight) | MEDIUM; calibrators note Task 1 has a bad-subcommand case and Task 5 has --submit with worktree | Low |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Write-verb audit in test_worker_contract.py would break on the new template and script (C-002); orchestrator re-Read confirms the test | High |
| U-002 | V1 | Single warning field cannot carry both launch warnings; precedence undefined (C-004) | Medium |
| U-003 | V3 | Missing dependency edge Task 7/9 on Task 3 (C-009) | Medium |
| U-004 | V3 | Existing test fails if the literal --repo appears in commands/issue.md; Task 3 must avoid it (orchestrator re-Read confirms test_issue_command.py:99-103) | High |
| U-005 | V3 | Fork-safety scan does not cover templates (C-013) | Medium |
| U-006 | V1 | Intermediate directory modes (C-014) | Low |
| U-007 | V2 | Four extra requirement units found in the spec body beyond the 56-row matrix | Low |
| U-008 | V3 | Lint and format gates only at the end (C-011) | Low |
| U-009 | V2 | Orca-dependency constraint missing (C-010) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Classification | Promoted | Level |
|---|---|---|---|---|---|
| A-001 | No reviewer ran pytest or any command; every test-state claim comes from reading | All three notes say so | STATED | No | - |
| A-002 | The design source.md is itself correct and complete; reviewers audit fidelity to it | All 56 matrix rows and every finding measure the plan against the design | UNSTATED | Yes | L2 |
| A-003 | The executor's only per-task check is each task's acceptance criteria, so cross-file failures between tasks stay invisible (state between tasks) | C-001 and C-002 findings assume red windows matter | UNSTATED | Yes | L3 |
| A-004 | A defect found here can be fixed only by changing the plan or its source before /sc:implement; the workflow protocol forbids editing the plan from findings | All three recommend plan edits | UNSTATED | Yes | L2 |
| A-005 | Staying green between tasks is required for the delivery, not only at the end | Severity grades of C-001 | UNSTATED | Yes | L2 |
| A-006 | The Orca JSON fixtures copied from one live list represent every installed Orca version | Plan Task 2 fixtures; no reviewer questions them | STATED (design section 15 marks the launch shape UNVERIFIED) | No | - |

Promoted shared assumptions: A-002, A-003, A-004, A-005.

## Summary

- Total structural differences: 2
- Total content differences: 15
- Total contradictions: 4
- Total unique contributions: 9
- Total shared assumptions surfaced: 6 (UNSTATED 4, STATED 2, CONTRADICTED 0)
- Highest-severity items: C-002 (High), U-004 (High); C-001 treated as High by two reviewers
- Total diff points for convergence: S 2 + C 15 + X 4 + A 4 = 25
- Taxonomy coverage: L1 4 (S-001, C-007, C-012, C-015), L2 14, L3 7 (C-001, C-002, C-004, C-008, C-013, C-014, A-003); all three levels present

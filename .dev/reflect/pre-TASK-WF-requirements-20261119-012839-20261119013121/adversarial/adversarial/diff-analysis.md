# Diff Analysis: v3 plan reviewer cards (UC-1)

## Metadata
- Variants: 3 (V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus). All three confirm the 11 earlier findings (P-1 to P-11) are fixed in plan v3.
- Categories: structural (2), content (10), contradictions (2), unique (6), shared assumptions (2)

## Structural Differences
| # | Area | V1 | V2 | V3 |
|---|---|---|---|---|
| S-001 | Severity labels | blocking/medium/note | every row Blocking with HIGH or MEDIUM inside | blocking/medium/note |
| S-002 | Evidence depth | about 30 cites, lists unread files | cites, no unread list | cites plus guard and claim.md reads |

## Content Differences (finding points)
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | The guard allows `gh issue edit/comment/create` at Full Submit (guard:653, :790), so a launched Full Submit agent can post issue comments and apply the approval label to another issue under the watcher's account, which is an approver; the plan's coordinator-only rule is unenforced there | A-4 (module form only) | QA-1 blocking | F-1 blocking | High |
| C-002 | claim.md:133 ship gate (OB-H1 item 1, OB-H2, OB-H3) is not met or checked, yet the watcher launches worktree, full and full submit on real issues | none | none | F-2 blocking | High |
| C-003 | The approval-void rule is untested against GitHub behaviour: does a label or field change bump the item's updatedAt | A-3 medium | none | F-3 blocking | High |
| C-004 | Task 4 gives `edited_after_approval` and Task 6 gives `revalidation_failed` for the same reread | A-1 blocking | QA-2 blocking | F-7 (part) note | Medium |
| C-005 | The guard pattern for the new verb is unnamed: verb form, module form, import form, false positives and negatives | A-4 medium | none | F-4 medium | Medium |
| C-006 | Task 9 has no configured Project id, so an issue on several Projects may get the wrong Status move | none | QA-3 blocking | none | High |
| C-007 | The level-None claim session has no level record, so it is not governed; plan:23 is too wide | none | none | F-5 medium | Medium |
| C-008 | Task 6 acceptance cannot pass before Task 7 rewrites the tests it names | A-2 medium | none | none | Medium |
| C-009 | Task 11 rewrite also hits the DF-14 `String!` assertion at test_security_invariants.py:919 | A-5 medium | none | F-6 note | Medium |
| C-010 | Ordering and note items (Task 4 vs Task 1, shared cycle.py edits, Task 15 scan, marker login, push-rule wording) | A-6, A-7 | none | F-7, F-8 | Low |

## Contradictions
| # | Point | V1 | V2 | V3 |
|---|---|---|---|---|
| X-001 | Severity of the updatedAt question | medium | not raised | blocking |
| X-002 | Is guard coverage of the verb alone enough? | add the module form | add Full Submit refusal tests | move the `issue` verbs out of SUBMIT |

## Unique Contributions
C-002, C-007 (V3); C-006 (V2); C-008 (V1); C-001 self-approval chain (V3).

## Shared Assumptions
| # | Assumption | Classification |
|---|---|---|
| A-001 | The account that launches the agent differs from the approving account | UNSTATED (false: the watcher runs under an approver's own login) |
| A-002 | The launch-level guard governs every session the watcher starts | UNSTATED |

## Summary
Total diff points: 2 structural + 10 content + 2 contradictions + 2 shared assumptions = 16.

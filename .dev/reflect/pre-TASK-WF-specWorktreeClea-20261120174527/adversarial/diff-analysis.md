# Diff Analysis: review-card Comparison

## Metadata

- Generated: 2026-11-20T17:58:00Z
- Variants compared: 2 (variant-1 = reviewer 1, analyzer lens, opus class; variant-2 = reviewer 2, qa lens, haiku class). Both are review cards of the same plan against the same spec; both were cut off by a transport limit after about 4,000 characters (variant 1 inside finding F3, variant 2 inside finding F4).
- Total differences found: 13 diff points (structural 2, content 7, contradictions 2, shared assumptions 2) plus 6 unique contributions
- Categories: structural (2), content (7), contradictions (2), unique (6), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity | Taxonomy |
|---|---|---|---|---|---|
| S-001 | Formatting of findings | Bold numbered headings (`**F1. BLOCKING (Decision: ...) ...**`) with Claim, Evidence, Consequence, Fix bullets; line cites use the short names `PLAN:` and `source.md:` | H3 headings (`### F1. BLOCKING: ...`) with bold Claim, Evidence, Consequence, Fix labels; line cites use full repository paths | Low | L1 (formatting, wording) |
| S-002 | Completeness of the visible card | Header, findings F1 to F3 (F3 cut mid-sentence); no "Checked and found sound" and no "Coverage gaps" section visible | Header, findings F1 to F4 (F4 cut mid-sentence); no "Checked and found sound" and no "Coverage gaps" section visible | Medium | L1 (presentation) |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity | Taxonomy |
|---|---|---|---|---|---|
| C-001 | Acceptance checks that depend on later tasks | BLOCKING. Tasks 2, 3, 4, 5, 11 and 12 cannot pass their checks without Task 7 fixtures or Task 13 tests; no task owns tests for the fact collectors (Orca parsers, `/proc` scan, four-place issue collection, landed-check chain). Fix: move Task 7 support after Task 2, add a collectors test module, rewrite the checks of Tasks 2, 11, 12 | BLOCKING. Tasks 3 and 4 need fixtures and a repo "by Task 7"; Task 7 depends on Task 6 and its "removal reports kept" check needs the Task 11 pipeline. Fix: fixture support right after the skeleton; keep raw git-fact tests apart from removal-result tests scheduled after the pipeline | High | L2 (component ordering, dependency) |
| C-002 | Real `branch-landed.sh` call in the proof (Task 1) and the dry run (Tasks 5, 20) | Not raised | BLOCKING. The helper runs `git fetch` (writes objects and `FETCH_HEAD`), makes a temp file and runs `rm -f`, so "read-only proof" and "dry run changes nothing" are contradicted; canned runner replies hide the child commands. Fix: prove it in a throwaway repo; define a no-write lookup for live dry runs | High | L3 (safety guard, invariant "dry run changes nothing") |
| C-003 | Patch-and-bundle manual archive | Not raised (the T1 card's R4 asked reviewers to check it; this reviewer is silent) | BLOCKING. Spec line 214 says manual `archive` "can still save them as a patch and a bundle"; the plan drops it on its own authority; spec line 374 sends other changes back to the owner. Fix: get a scope decision or build a bounded version | High | L2 (interface, verb behaviour) |
| C-004 | Pull-request step in the plan | Not raised | BLOCKING (headline only; the rest is cut off): the plan ends with recording and has no successful finish or pull-request step | Medium | L2 (organization) |
| C-005 | Row count of the spec section 12 table | BLOCKING. The table has 15 data rows, the plan says 14 (Task 19, lines 253 and 256); the spec also uses labels beyond "kept as is, changed, dropped" (Replaced, Reused, Not adopted, Adopted in spirit) | Not raised | Medium | L2 (provenance record, acceptance number) |
| C-006 | Task 1 fallback for unproved items 1 and 2 | BLOCKING. Task 1 gives item 2's fallback for both items; spec item 1's fallback is `git worktree remove` only and the two conflict when both are unproved (cut off after "source.md:374 says") | Not raised | High | L2 (removal path) |
| C-007 | Coverage matrix and unmapped rows | Not visible in the card | Not visible in the card (its brief asked for gaps; the section is cut off) | Low | L2 (coverage) |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|---|---|---|---|
| X-001 | Is the real landed-check call a blocking safety problem? | Silent: the plan's Task 1 and Task 20 use it without objection (variant 1 reviewed the same plan text at lines 33 and 82 and raised no safety finding) | `branch-landed.sh:182` "runs `git fetch --quiet origin ...`" so the call is a write; BLOCKING. Spec section 11 item 3 (source.md:299) tells the implementer to "run the check on a merged and an open pull request", and the helper's own header (lines 32 to 33) says its only write is the fetch | Medium: decides whether Task 1 and Task 20 must change |
| X-002 | How far does the "later task" dependency reach? | Tasks 2, 3, 4, 5, 11, 12 are affected, and Task 8 "tests the collectors" is false because it tests a pure decision function | Tasks 3, 4 and Task 7 itself are affected; Task 7's "removal reports kept" check needs Task 11 | Medium: sets how many tasks need a rewrite |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | Wrong number: the spec section 12 table has 15 rows, not 14 (Task 19 acceptance would force a silent drop) | High |
| U-002 | 1 | Task 1's fallback for item 1 conflicts with the spec; both items unproved means the plan picked one without saying so | High |
| U-003 | 1 | No task owns tests for the fact collectors | High |
| U-004 | 2 | `branch-landed.sh` writes (fetch, temp file); canned replies in the recorder hide child-command side effects | Medium |
| U-005 | 2 | Patch-and-bundle is dropped without the owner's decision | Medium |
| U-006 | 2 | The plan has no pull-request step (headline only) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The plan's tasks are checked one at a time as each finishes (per-task acceptance), so a forward reference to a later task is a defect | Both cards raise the ordering finding (C-001) and neither states how the executor verifies | If the executor verifies the whole plan at the end, C-001 loses its BLOCKING grade | UNSTATED, promoted |
| A-002 | The grade BLOCKING is applied the same way in both cards (a decision, a missing deliverable or a safety break), including for findings that only the card's own reading of the spec supports | Both cards grade every visible finding BLOCKING and none gives MEDIUM or NOTE | If the grading is looser than the rule, the verdict FAIL is unsafe | UNSTATED, promoted |

Classification record (AD-2): STATED: none. UNSTATED: A-001, A-002 (both promoted). CONTRADICTED: none.

## Summary

- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 2
- Total unique contributions: 6
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, C-006

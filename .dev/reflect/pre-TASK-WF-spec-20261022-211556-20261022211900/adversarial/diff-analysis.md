# Diff Analysis: reviewer-card Comparison

## Metadata
- Generated: 2026-10-22T21:33:00Z
- Variants compared: 2 (Variant 1 = reviewer-1 card, sonnet, analyzer; Variant 2 = reviewer-2 card, haiku slot grok-4.7, qa)
- Subject: pre-execution review of tasklist TASK-WF-spec-20261022-211556 against its source.md
- Focus: correctness, coverage, deviation-classification
- Total differences found: 17
- Categories: structural (2), content (8), contradictions (3), unique (8, listed separately; overlapping C-points not double-counted), shared assumptions (4)
- Calibration inputs (opus calibrator, blind): Variant 1 C=0.86, Variant 2 C=0.82; downgrades R1-8 medium to low, R2-1 medium to low, R2-3 medium to low.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Finding count and granularity | 12 findings, more sub-claims per finding | 10 findings, one claim each | Low | L1 |
| S-002 | Citation form | Absolute paths with line numbers | Paths relative to package / worktree | Low | L1 |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity | Level |
|---|-------|--------------------|--------------------|----------|-------|
| C-001 | Backslash-backtick check in Task 5 (tasklist:94) | R1-3 low: span is broken but intent recoverable; write as fenced command or words | R2-1 medium: broken span means a wrong render can pass; rewrite as fenced command and state nonzero fails | Medium | L3 |
| C-002 | Task 6 stub run (tasklist:114) | R1-4 medium: git stub must delegate non-push subcommands; also set GITHUB_REPOSITORY, bash -eo pipefail, clean third-run index | R2-2 medium: git stub must exec real git for non-push; gh stub prints scripted count | Low (same conclusion, V1 broader) | L3 |
| C-003 | Line-number-anchored greps in Task 5 (tasklist:88,91) | R1-2 low: anchor on text blocks | R2-6 low: anchor on text; also notes a wrong reword moving text to the next line passes | Low | L3 |
| C-004 | Placeholders (tasklist:84,87,112,125,144,156) | R1-10 low: define t1-head in Constraints | R2-7 low: also `<decided file input>`; tasks should fail if angle brackets survive | Low | L2 |
| C-005 | Depends on chain (tasklist:43-148) | R1-11 low: spurious links; optional fix; not worth blocking | R2-5 low: repoint Task 3/4/6 to Task 1, Task 7 to Task 2 | Low | L2 |
| C-006 | scripts/README.md "one paragraph" scope (source.md:35, tasklist:26,146-160) | R1-9 low: disclosed trade-off; add "read lines 1-30 first" and state contradiction in leftovers with offer to extend | R2-3 medium: ask user before Task 9 whether neighbours may be edited | Medium | L2 |
| C-007 | Path-filter 300 vs 3,000 question (source.md:46-47) | R1-8 medium: extend Task 3 docs read and Task 9 leftovers with a "Question for user" | R2-8 low: add a Constraint that the session report must quote docs and ask | Low | L2 |
| C-008 | Acceptance strength, unchanged-content checks | R1-1 (Task 5 header and ::warning checks pass a wrong reword) and R1-5 (Task 6 never diffs the unchanged run body, if, working-directory, --base/--head) | R2-4 (Task 8 README checks pass a wrong README; badge never required to name test.yml) | Medium | L3 |

## Contradictions

| # | Point of conflict | Variant 1 position | Variant 2 position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Overall readiness | `overall_verdict: ready_with_notes` (self_confidence 0.75) | `overall_verdict: not_ready` (self_confidence 0.82) | High |
| X-002 | Whether the scripts/README.md inconsistency needs a user decision before execution | No: spec (source.md:35, :44) already decided "one paragraph, change nothing else"; disclose only | Yes: add a user question before Task 9 | Medium |
| X-003 | Unmapped-row verdicts | INF-041 covered, INF-045 gap | INF-041 partial (where Task 3), INF-045 partial (where null) | Low |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | 1 | R1-1: Task 5 header-comment and ::warning bullets do not fail on a wrong reword | High |
| U-002 | 1 | R1-5: Task 6 does not compare the unchanged lines of the run body (incl. `git add -f docs/.framework-sync-commit`), the step's if/working-directory, or --base/--head | High |
| U-003 | 1 | R1-6: throwaway repo needs `git init -b master` and a commit identity | Low |
| U-004 | 1 | R1-7: render SHAs unspecified; if BASE is not an ancestor of HEAD the two-dot and three-dot file lists differ and the "only reworded lines differ" bullet fails a correct edit (also raised independently by the reviewer-2 calibrator) | Medium |
| U-005 | 1 | R1-12: porcelain parsing, deleted paths and untracked tool caches can break the Task 1/Task 9 scope tooling | Low |
| U-006 | 2 | R2-4: Task 8 README acceptance passes a wrong README | High |
| U-007 | 2 | R2-9: coverage matrix best_item points at wrong tasks for INF-025, INF-033, INF-036 (reflect artifact, not tasklist) | Low |
| U-008 | 2 | R2-10: coverage matrix misses four requirement-bearing clauses the plan does implement (reflect artifact, not tasklist) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | Task 3's `gh api repos/IronbellyOrg/IronClaude/actions/permissions/workflow` will run with an authenticated `gh` that can read the repo's Actions settings (admin read may be required) | Both accept Task 3 as written | UNSTATED | Medium | Promoted [SHARED-ASSUMPTION] |
| A-002 | `uv run python` in the worktree can import PyYAML (Tasks 5, 6, 7 checks) | Both accept the PyYAML checks | UNSTATED | Low | Promoted [SHARED-ASSUMPTION] |
| A-003 | tests/swarm/test_merge_boundary_guards.py passes on base a88f100b before any edit, so a post-edit pass is attributable to the edit being safe | Both accept the Task 5 pytest bullet | UNSTATED | Medium | Promoted [SHARED-ASSUMPTION] |
| A-004 | No finding rises to high severity; the plan's structure (scope, ordering, phases) is sound and only acceptance bullets need tightening | Neither card files a high | UNSTATED | High | Promoted [SHARED-ASSUMPTION] |

STATED (not promoted): both cards state the Fix 1/Fix 3 unverifiability is correctly handled (V1 self_audit; V2 self_audit "Confirmed Fix 1-4 bodies are tasked").

## Summary
- Total structural differences: 2
- Total content differences: 8
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 4 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: X-001, U-001, U-002, U-006, A-004
- Convergence denominator (S + C + X + A): 2 + 8 + 3 + 4 = 17
- Taxonomy coverage: L1 (S-001, S-002), L2 (C-004..C-007, X-002, X-003), L3 (C-001..C-003, C-008); all three levels present.

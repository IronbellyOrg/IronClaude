# Diff Analysis: reviewer-card comparison (pre-execution audit of the plan for issue 848)

## Metadata
- Generated: 2026-11-25T20:31:00Z
- Variants compared: 2 (variant-1 = reviewer 1, analyzer, opus class; variant-2 = reviewer 2, qa, haiku class)
- Total differences found: 11
- Categories: structural (1), content (7), contradictions (1), unique (4), shared assumptions (2)
- Taxonomy levels (auto-tagged): L1 surface = S-001, C-007; L2 structural = C-001, C-004, C-006; L3 state-mechanics = C-002, C-003, C-005, A-002

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Size and sections | 9 findings (A1-A9) plus a "What I checked and found correct" list; evidence as bullet lists with path:line and quotes | 3 findings (Q1-Q3), no list of what was checked; evidence as bullet lists with path:line and quotes | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | New `gh api` line has no entry in the write-verb classification table of tests/skills/test_worker_contract.py (L2) | A1 Blocking (Missing): confirmed, adds that a read-only entry would also pass the GET check, says keep `gh api` out of SKILL.md wording, says add the entry after wording is final | Q1 Blocking (Missing): confirmed, same consequence for Task 6's acceptance check, no wording advice | Low |
| C-002 | Strength of Task 6's ordering test (L3) | Not raised; says all plan references match | Q2 Blocking (Decision): the helper only checks the blocker item is after the closed-issue item, not after the assignee checks; a mutation moving it between them passes | Medium |
| C-003 | What wins when the blocker call fails but still prints output (L3) | A2 Blocking (Decision): Task 1 gives two clashing rules (any output line is a blocker; a non-zero exit continues); wants exit code checked first and pinned in Task 6 | Not raised | High |
| C-004 | Coverage record vs the referenced issue summary (L2) | Says every spec requirement maps to a task | Q3 Medium: the 5-row matrix omits requirements that only the issue summary states; the plan largely covers them, but the record cannot prove it | Low |
| C-005 | "Could not run" line when a later STOP follows (L3) | A3 Medium: the line is only in Final output item 4, so a claim that STOPs later never reports the skipped check | Not raised | Low |
| C-006 | Wording traps in existing tests (L2) | A4 Medium (forbidden phrase "Runs for every `--pipeline` value"), A5 Note (`## Final output` split), A6 Note (`--repo` banned in issue.md) | Not raised | Low |
| C-007 | Wording and housekeeping (L1) | A7 heading says orchestrator reads scout.md only, A8 no sync-dev step, A9 `git diff --stat` wording (all Notes) | Not raised | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Whether spec coverage is complete | "Spec coverage: every spec requirement maps to a task" (card 1, last list) | Q3: the coverage matrix omits requirements from the incorporated issue summary, so complete coverage "cannot be substantiated" | Low (the two statements are about different objects: the plan versus the matrix record) |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | A2 exit-code-first rule for the unreadable list (C-003) | High |
| U-002 | 1 | A4, A5, A6 test-wording traps (C-006) | Medium |
| U-003 | 2 | Q2 ordering-test gap against the assignee checks (C-002) | Medium |
| U-004 | 2 | Q3 coverage-record weakness (C-004) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The classification scan treats the new line as a hit and keys on the exact stripped line text, so the entry can only be written once Task 1's wording is final (STATED in card 1, implied in card 2) | C-001 | The fix order inside the plan matters (L3: ordering of edits) | UNSTATED in card 2; promoted |
| A-002 | Both cards assume the unreadable-list outcome means "the call exits non-zero", not "the call exits 0 with an error body" (UNSTATED in both) | C-001..C-005 | Decides whether A2 is real (L3: guard condition on failure) | UNSTATED; promoted |

Classification: A-001 STATED (card 1) / UNSTATED (card 2); A-002 UNSTATED. Both promoted as [SHARED-ASSUMPTION] diff points.

## Summary
- Total structural differences: 1
- Total content differences: 7
- Total contradictions: 1
- Total unique contributions: 4
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0 net, CONTRADICTED: 0)
- Highest-severity items: C-003
- total_diff_points (S + C + X + A) = 1 + 7 + 1 + 2 = 11

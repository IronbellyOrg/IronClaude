# Diff Analysis: owner-answer proposals for Q12 (routing entry for the observer)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A "no entry for now"; variant-2 = proposal-B "one bullet in the Orca coordination prose section"; variant-3 = proposal-C "one routing table row, own PR after #539")
- Performed by: the orchestrating worker directly (no separate analytical agent)
- Total differences found: 15
- Categories: structural (1), content (5), contradictions (3), unique (4), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section set | Same five H2 sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Whether to make the observer discoverable now | No | Yes | Yes | High |
| C-002 | Where the entry lives | Nowhere | Prose bullet in "Orca coordination" | Machine-read routing or other-commands table | High |
| C-003 | Test edits | None | None (tables untouched) | At least one routing test edit (INV-029) | Medium |
| C-004 | Timing | Revisit after guard flip and contract note | After #539 merges | After #539 merges | Medium |
| C-005 | Effect on `/sc:recommend` routing | Cannot suggest observer | UNVERIFIED for prose | Routes like any row | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Is advertising the observer before its question panel is on a problem | Yes, a reason to wait | Not addressed | Named as a cost, accepted | Medium |
| X-002 | Is a test edit to admit a CLI-only entry acceptable | Avoided | Avoided | Accepted | Medium |
| X-003 | Should OB-07's spec row change | Deferred | Reworded (row to bullet) | Unchanged | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 1 | Ties discoverability to the guard flip (Q6) and contract note, so the advertised tool is complete | Medium |
| U-002 | Variant 2 | Observes the two table tests read only the marked blocks (test file lines 22-24), so a prose bullet needs no test edit | High |
| U-003 | Variant 2 | Places "person only" next to the never-as-worker text in the same section | Medium |
| U-004 | Variant 3 | Uses the same table `/sc:recommend` and people already read; follows V5 D8 | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted | Impact | Status |
|-------|------------|------------------|----------------|----------|--------|--------|
| A-001 | Any guide edit must wait for PR #539 to merge because #539 edits the same files | Variants 2 and 3 wait; Variant 1 avoids edits | UNSTATED as a guard for the prose section (stated for the tables) | Yes | Medium | open |
| A-002 | The observer is stable enough to route people to (its CLI flags will not change soon) | All three treat the observer as a finished tool | UNSTATED | Yes | Low | open |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 2 (UNSTATED: 2)
- Highest-severity items: C-001, C-002, U-002
- Taxonomy tags: L1: S-001, X-003; L2: C-001, C-002, C-004, C-005, X-001, A-002; L3 (guard or validation rule): C-003, X-002, A-001

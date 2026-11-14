# Diff Analysis: owner-answer proposals for Q15 (v2 delivery to non-worker sessions)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A "never, as a standing rule"; variant-2 = proposal-B "report only; wider delivery is a later separate decision"; variant-3 = proposal-C "yes eventually, behind the #339 trust layer")
- Performed by: the orchestrating worker directly (no separate analytical agent)
- Total differences found: 14
- Categories: structural (1), content (5), contradictions (3), unique (3), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section set | Same five H2 sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Long-term direction | Never | Open (later decision) | Yes, a goal | High |
| C-002 | First release behaviour | Report only | Report only | Report only | Low |
| C-003 | Trust layer on v2's path | Never | Not for v2 as decided | Yes, for the delivery release | High |
| C-004 | #423 "relay them to affected agents" | Removed | Narrowed for non-workers | Kept as a goal | Medium |
| C-005 | Effect on other open questions | None | None now | Q14 gate widens for the delivery release; Q16 must be answered first | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Should a new inbound channel into non-worker sessions ever exist | No | Undecided | Yes, guarded | High |
| X-002 | Should the answer bind future designs (orchestrator of orchestrators) | Yes | No | Yes (toward delivery) | Medium |
| X-003 | Is designing a delivery path now worth it with no known channel | No | No | Yes | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 1 | Writing the rule beside the contract's "never messaged" sentence (by a separate approved PR) | Medium |
| U-002 | Variant 3 | Makes the trust layer's consumer concrete and names Q16 as a prerequisite | Medium |
| U-003 | Variant 3 | Unattended watcher-launched sessions as the case that most needs automatic correction | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted | Impact | Status |
|-------|------------|------------------|----------------|----------|--------|--------|
| A-001 | Corrections to Orca workers through the coordinator's pulled follow-ups (WC-12) are acceptable for v2 | All three keep the WC-12 route for workers | UNSTATED as a v2 permission (stated as a contract fact) | Yes | Medium | open |
| A-002 | A person reads and acts on v2's reports in reasonable time | All three report to the person for non-workers in the first release | UNSTATED | Yes | Medium | open |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2)
- Highest-severity items: C-001, C-003, X-001
- Taxonomy tags: L1: S-001, C-002; L2: C-004, C-005, X-002, X-003, A-002; L3 (boundary, guard): C-001, C-003, X-001, A-001

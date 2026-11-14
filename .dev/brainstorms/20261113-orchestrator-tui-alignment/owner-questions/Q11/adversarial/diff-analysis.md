# Diff Analysis: owner-answer proposals for Q11 (which static report goes in the coordinator's chat)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A "both, now"; variant-2 = proposal-B "sweep summary only until the contract note"; variant-3 = proposal-C "neither yet, park the clause")
- Performed by: the orchestrating worker directly (no separate analytical agent)
- Total differences found: 14
- Categories: structural (1), content (5), contradictions (3), unique (3), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section set | Same five H2 sections (Answer; What happens next; Unlocks; Costs; Unresolved) | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | What the chat report is | Sweep reply plus `observe --once` text | Sweep reply only | No recurring report; ledger only; sweep reply only when `/sc:sweep` is actually run | High |
| C-002 | Timing | Now, before the contract note | Until the note exists, then revisit | Parked until loop and note both exist | Medium |
| C-003 | Edits implied | Section 6.7 reworded; later WC-16, skill tools and style exception edits | None (6.7 already says this) | 6.7 last sentence removed; a #534 deferral row | Medium |
| C-004 | Treatment of #339's "3 to 5 minutes" | Observer fills the 3-minute gap the sweep cap cannot | Accepts the cap; not met at 3 minutes | Says nothing runs it, so do not promise it | Medium |
| C-005 | Fidelity to #339 "taking inspiration from #409" | Highest (dashboard-like text) | Narrow (counts and path) | None for now | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Should `observe` be named in coordinator rules before the contract note | Yes, eventually required ("would have to name") | No ("keep not naming") | No | High |
| X-002 | Does the sweep reply count as the #339 chat report | Yes, as one half | Yes, the whole | No, it is an on-demand reply only | Medium |
| X-003 | Spec section 6.7 text | Change to allow both | Keep as is | Drop its last sentence | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 1 | `observe --once` writes no file, so it can run between sweeps without breaking the one-report-per-run rule (NFR-001) | Medium |
| U-002 | Variant 1 | Flags Q-1 (unbound terminal cannot read another terminal's Run) as UNVERIFIED for the coordinator's own terminal | High |
| U-003 | Variant 3 | Points out the recurring coordinator loop is unbuilt, so a cadence promise has nothing to run it | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted | Impact | Status |
|-------|------------|------------------|----------------|----------|--------|--------|
| A-001 | The question has no work item behind it, so a wrong answer is cheap to reverse | All three treat the answer as recorded-only (spec row Q11 "none scheduled") | UNSTATED in the variants (stated in the spec) | Yes | Medium | open |
| A-002 | The contract note (XC-05) will eventually be written, so "until the note" is a real trigger | Variants 2 and 3 depend on it; Variant 1 lists it unresolved | UNSTATED | Yes | Medium | open |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001, U-002
- Taxonomy tags: L1: S-001; L2: C-001, C-002, C-003, C-005, X-002, X-003, A-001; L3 (guard or boundary): C-004 (cap boundary), X-001 (rule guard), A-002 (precondition)

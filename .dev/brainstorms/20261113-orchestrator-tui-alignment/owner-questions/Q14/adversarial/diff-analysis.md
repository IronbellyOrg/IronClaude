# Diff Analysis: owner-answer proposals for Q14 (what "#339 is complete" means for #423's gate)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A "#539 merged; capture gates only live-value features"; variant-2 = proposal-B "#539 merged + capture recorded + `working` class restored in code"; variant-3 = proposal-C "#539 merged + capture recorded")
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
| C-001 | Gate parts | #539 merged | #539 merged, capture recorded, SW-14 merged | #539 merged, capture recorded | High |
| C-002 | Role of the live capture | Per-feature gate inside v2 | Whole-gate prerequisite and input to a code change | Whole-gate prerequisite (record only) | High |
| C-003 | SW-14 (restore `working` class) | Follow-up, not gate | Required | Follow-up, not gate | Medium |
| C-004 | When the v2 brainstorm can start | At #539 merge | After SW-14 merges | After the capture is recorded | Medium |
| C-005 | Fidelity to ADJ's wording ("capture that restores the `working` class") | Departs | Most literal | Close, drops "restores" | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Should v2 design wait for live Orca values | No | Yes, and for the code change | Yes | High |
| X-002 | Is a v2 that shows working sessions as "could not determine" acceptable | Yes, marked pending | No | Yes, a carried gap | Medium |
| X-003 | Does a code change belong on a planning gate | No | Yes | No | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 1 | Per-feature gating: mark live-value fields pending instead of holding the whole design | Medium |
| U-002 | Variant 2 | The capture might show Rule 5 cannot be built from what Orca exposes, which would be a v2 risk | Medium |
| U-003 | Variant 3 | A gate made of records a ledger entry can check, not a code change | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted | Impact | Status |
|-------|------------|------------------|----------------|----------|--------|--------|
| A-001 | v2 will read the sweep's report JSON as a main input (so the sweep's classes matter to v2) | All three reason from what the sweep can classify | UNSTATED | Yes | Medium | open |
| A-002 | PR #539 will merge in a form close to today's (its read-only sweep and class list survive the INV-008 ruling, owner question Q1) | All three put #539 merged in the gate | UNSTATED | Yes | Medium | open |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2)
- Highest-severity items: C-001, C-002, X-001
- Taxonomy tags: L1: S-001, C-005; L2: C-001, C-004, X-003, A-001, A-002; L3 (state, guard, transition): C-002, C-003, X-001, X-002

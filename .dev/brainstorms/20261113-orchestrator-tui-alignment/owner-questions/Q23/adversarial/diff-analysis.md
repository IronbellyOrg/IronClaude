# Diff Analysis: owner-answer proposal comparison (Q23, `reclaimable`)

## Metadata
- Generated: 2026-11-14
- Mode: A (compare), depth quick (Round 1 only)
- Variants compared: 3 (variant-1 = proposal-A historical, variant-2 = proposal-B live side as built, variant-3 = proposal-C own state until known)
- Total differences found: 11
- Categories: structural (1), content (4), contradictions (3), unique (2), shared assumptions (1)
- Prerequisites validated: output path under `.dev/`; all three inputs exist.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Section layout | Same five sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Meaning recorded in the mapping table | historical | not historical, "awaiting release" | its own state, side undecided | High |
| C-002 | Observer code change | add `reclaimable` to `HISTORICAL_STATES` plus a test | none | none | Medium |
| C-003 | Observer default view | hides reclaimable rows | shows them (as today) | shows them (as today), no live wording | High |
| C-004 | Finality | final | final | provisional, reopened when Orca's meaning is recorded (for example via XC-03) | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Should a person see reclaimable workers by default? | No: they are finished; 27 reclaimable vs 0 active at the probe | Yes: next action `release` is a cleanup cue | Yes for now, without a meaning claim | High |
| X-002 | May a meaning be decided before Orca's definition is confirmed? | Yes, from the name and next action | Yes, from next action | No | High |
| X-003 | Is a code change in the built observer justified for this? | Yes, small | No | No, not yet | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | Notes the sweep's "historical" (6 h window) and "settled" (`outcome`) still differ from the observer's terminal-state meaning, so the note must say so whatever Q23 answers | Medium |
| U-002 | 3 | Names a concrete way to settle the meaning: one help-text or detail read of a reclaimable worker added to the shared capture XC-03 | High |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | [SHARED-ASSUMPTION] A reclaimable worker has finished running (none of the three claims it can still be doing work); all three treat Orca's next action `release` as the defining fact. No file read confirms that a reclaimable worker's session has exited | All variants reason from the word and from `classify.py:479-481` | If a reclaimable worker can still be running, variant 1 hides a live worker | UNSTATED, promoted |

## Summary
- Structural 1, content 4, contradictions 3, unique 2, shared assumptions 1.
- Highest-severity items: C-001, C-003, X-001, X-002.
- Taxonomy tags: L1 S-001; L2 C-002, C-004, X-003; L3 C-001, C-003, X-001, X-002, A-001 (state meaning and visibility boundary).

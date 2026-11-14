# Diff Analysis: owner-answer proposals for Q13 (bare `orca` for the observer)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A "yes, probe makes it safe; record both"; variant-2 = proposal-B "no, align the observer to the sweep's rule"; variant-3 = proposal-C "no ruling; record both as facts")
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
| C-001 | Verdict on the observer's bare-name fallback | Accepted | Rejected | None given | High |
| C-002 | Code change | None | Observer lookup and tests change | None | High |
| C-003 | Meaning of `ORCA_CLI_COMMAND` across programs | Stays different, documented | Same for observer and sweep | Stays different, undocumented as a decision | Medium |
| C-004 | Effect on hosts with only `orca` | Keeps working | Breaks until the variable is set | Keeps working | Medium |
| C-005 | What the contract note says | Both rules plus a verdict and reasons | One rule for the two read-only programs; watcher noted as separate | Both rules as facts, no verdict | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Is the `skills list --json` probe a sufficient guard | Yes | Sufficient against the screen reader but not against reading a different Orca | Not judged | High |
| X-002 | Is a fix worth it with no shown divergence (INV-016) | No | Yes | No | Medium |
| X-003 | Does the observer-sweep comparison (XC-03, XC-04) need one binary | Not addressed | Yes | Not addressed | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 1 | Inside Orca terminals `orca` is the Orca CLI shim; the fallback keeps the observer working there | Medium |
| U-002 | Variant 2 | Ties binary sameness to the shared capture and dispatch-id comparison | High |
| U-003 | Variant 3 | Uses the note's "record the Orca build string next to each capture" rule as the detector for divergence | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted | Impact | Status |
|-------|------------|------------------|----------------|----------|--------|--------|
| A-001 | PATH on the owner's host is trusted (a binary named `orca-ide` or `orca` on PATH is not hostile) | All three accept PATH lookup | UNSTATED | Yes | Medium | open |
| A-002 | Only one Orca app runs per host, so two binary names normally reach the same app | Variants 1 and 3 rely on it; Variant 2 guards against its failure | UNSTATED | Yes | Medium | open |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2)
- Highest-severity items: C-001, C-002, X-001, U-002
- Taxonomy tags: L1: S-001; L2: C-002, C-005, X-002, X-003; L3 (guard, boundary, state): C-001, C-003, C-004, X-001, A-001, A-002

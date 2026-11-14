# Diff Analysis: owner-answer proposals for Q17 (sweep facts on the observer screen)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A "yes, plan a sweep-facts panel for release 3"; variant-2 = proposal-B "not now, ask again later"; variant-3 = proposal-C "never, a standing boundary")
- Total differences found: 13
- Categories: structural (1), content (5), contradictions (3), unique (3), shared assumptions (2)
- Step 1 performed by: the orchestrating session (group 4 worker), not a separate analytical agent.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section layout | Five fixed sections | Same five | Same five | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | OB-09 (observer release 3) contract | Reads snapshot v1 and sweep facts; depends on SW-11 | Snapshot v1 only for now; SW-11 edge stays soft | Snapshot v1 only, permanently; SW-11 edge removed | High |
| C-002 | Effect on Q9 (where sweep JSON lives) and NFR-001 (one report file) | Q9 becomes a requirement now; capture or relax NFR-001 | Q9 keeps its default (not now, caller capture first) | Q9 decided on v2 and Coder#477 needs only | High |
| C-003 | Contract note (XC-05) wording | Adds a section on how the observer reads sweep rows | Keeps the verbatim-words rule for a future panel | States a no-cross-reading boundary; old rule kept as history | Medium |
| C-004 | Where a person sees Orca state and sweep classes together | On the observer screen | Two places for now | Two places, or later in v2 | Medium |
| C-005 | Freshness mismatch between live Orca rows and sweep reports | Named as a risk (sweep at most once per 5 minutes) | Not raised | Not raised | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Should the observer ever show sweep facts? | Yes, in release 3 | Undecided, not now | Never | High |
| X-002 | Does the debate's 78 percent judgement (ADJ line 361) settle the question? | Goes against it | Matches it ("now") | Extends it to "ever", which the variant admits goes further | Medium |
| X-003 | Is the decision reversible cheaply? | Costly once persistence and layout are built | Cheap; nothing built | Reversing a written boundary is harder than answering a deferred question | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 1 | Names the staleness gap: sweep facts are always older than the Orca rows beside them | Medium |
| U-002 | Variant 2 | Notes that "not now" has no written trigger and may drift into "never" | Medium |
| U-003 | Variant 3 | Two collectors, two contracts, no reader crossing between them; ends default re-opening | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Observer release 3 (Decision Desk) will actually be built, so the question has a real consumer | All three plan around OB-09 | If release 3 never comes, every answer is moot and "not now" costs nothing | UNSTATED, promoted |
| A-002 | The sweep merges (PR #539) and keeps its current fact set (frozen plans, safe-to-close, git state) | All three treat the sweep's facts as stable inputs | If PR #539 changes or stalls, a yes has nothing to read and a never is unnecessary | UNSTATED, promoted |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
- Taxonomy tags: L1 S-001; L2 C-001, C-003, C-004, X-001, X-002, U-001 to U-003; L3 C-002 (state: one-file rule), C-005 (state: freshness), X-003 (state transition), A-001, A-002 (guard preconditions)

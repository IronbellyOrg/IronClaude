# Diff Analysis: owner-answer proposals for Q5 (observer and sweep: note, panel or merge)

## Metadata
- Generated: 2026-11-14 (Step 1, sc-adversarial-protocol Mode A, depth quick)
- Variants compared: 3 (variant-1 = proposal-A "one shared set of facts: an observer panel reads a captured copy of the sweep's JSON, plus a note"; variant-2 = proposal-B "keep both separate, one written contract note"; variant-3 = proposal-C "keep both, write nothing yet, decide after #539 merges and the real ids are compared")
- Total differences found: 17
- Categories: structural (1), content (6), contradictions (3), unique (4), shared assumptions (3 promoted)
- Context file for all advocates: `../question.md`

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section set and order | five sections, same order | same | same | Low (identical by design of the brief) |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Runtime link between the programs in version 1 | yes: the observer reads a captured copy of the sweep JSON | none | none | High |
| C-002 | The contract note | written, with the captured JSON as a third registered artefact | written (draft now, land after #539) | deferred | High |
| C-003 | Implied answers to Q9 (keep the sweep JSON) and Q17 (show sweep facts on the observer) | Q9 caller-side capture now; Q17 yes, later | both "not now" | both "not now" (deferred) | Medium |
| C-004 | Timing | panel after #539 merges and the real-id comparison (XC-04) | draft now; land after #539 and XC-04 | nothing until #539 and XC-04 | Medium |
| C-005 | The live #409 body's "one shared set of facts" proposal | adopted | set aside for version 1 | deferred | Medium |
| C-006 | Changes to the programs | observer panel plus a capture step in the coordinator pass | none (a document and one comparison test) | none | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Is it acceptable for two programs to classify the same session differently? | no: "two programs would classify the same session and could disagree" (#409) | yes, if the note documents the difference | yes, for now | High |
| X-002 | Write the note before PR #539 merges? | yes (as part of the panel plan) | yes, draft on a master-based branch | no: "a moving target"; yet its own costs say the draft "could have been written now ... at low cost" | Medium (variant 3 is internally strained) |
| X-003 | Is the note wasted if a panel or merge is chosen later? | no, still needed | no, it is the base for any later choice | possibly, which is a reason to wait | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Capture the JSON the coordinator's WC-16 pass already prints, so the sweep's one-report-per-run rule (NFR-001) does not change | Medium |
| U-002 | 2 | One comparison test (XC-06) that fails when either program changes a shared word, verb or schema version without the note | High |
| U-003 | 3 | An explicit trigger to re-ask the question with the comparison result in hand | Medium |
| U-004 | 2 | Names the limit of the test: identical words can still mean different things ("stale" 45 seconds against 6 hours) | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-004 | PR #539 merges, in roughly its current shape, at some point; every option's main step waits on it, and none says what happens if it does not | UNSTATED | Yes |
| A-002 | X-001 | The person actually reads both the observer screen and the sweep's output, so a disagreement between them would be noticed and would matter | UNSTATED | Yes |
| A-003 | C-004 | The one real-id comparison (XC-04) can run: it needs the Q1 ruling applied, the sweep runnable on this host (Q29), Orca reachable and a named runner (Q24) | UNSTATED | Yes |
| A-004 | All | The two programs are not merged; merging was rejected by all five reviews (ADJ Part 8) | STATED (question.md; variant 1) | No |

Promoted shared-assumption points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | #539 merges in roughly its current shape | C-004 | If #539 stalls (for example on Q1) every option stalls; only a note drafted against master constants survives (L2, dependency) | UNSTATED |
| A-002 | The person reads both views | X-001 | If the person reads only one, a disagreement costs little and the panel's gain shrinks (L2) | UNSTATED |
| A-003 | The real-id comparison can run | C-004 | The note may never use the words "join key", and the panel may have no reliable join (L3, guard) | UNSTATED |

## Summary
- Total structural differences: 1
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
- Taxonomy levels: L1 (S-001, X-003), L2 (C-002, C-003, C-004, C-005, C-006, X-002, A-001, A-002), L3 (C-001, X-001, A-003)
- Similarity check: well above 10 percent difference; debate proceeds.

# Diff Analysis: owner-answer proposals for Q18 (snapshot copy channel to the TUIBBS host)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A "not yet; open at observer R4 or a TUIBBS statement"; variant-2 = proposal-B "yes; a TUIBBS screen is planned, design the channel now"; variant-3 = proposal-C "no; no TUIBBS screen planned, drop CO-04")
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
| C-001 | CO-04 (the copy channel item) | Stays deferred with two written triggers | Opens now as a design item | Closed as "not planned" | High |
| C-002 | Coder#477 reply text (CO-01) | No channel exists or is planned yet | A read-only, identity-tagged, aged copy is planned; nothing can be sent in | Single-host, no channel planned; supports closing #477 under Q3 | High |
| C-003 | Effect on Q22 (staleness age) and authentication design | Not pulled forward | Pulled forward now | Not needed | Medium |
| C-004 | Contract note "single owner, single OS user, single host" | Kept | Kept, plus a sentence about read-only copies off-host | Kept with no pending exception | Medium |
| C-005 | Data exposure of the snapshot (mode 0600, worker rows, Orca strings) | Not raised | Named as the main risk of copying off the workspace | Not raised | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Is a TUIBBS screen planned? | Unknown; wait for the owner to say | Yes (the owner states it now) | No (the owner states it now) | High |
| X-002 | What the owner's 2026-11-08 record ("may become a TUIBBS module", "Background, not deciding") supports | Matches it | Changes it to "deciding: yes" | Changes it to "deciding: no" | Medium |
| X-003 | Cost of being wrong later | A second Coder#477 edit | An undesigned receiving side and a widened readership of the snapshot | Design starts from nothing; #477 may already be closed | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 1 | Names Q4 (what "TUI Panel" means) as the only prompt that would surface the owner statement trigger | Medium |
| U-002 | Variant 2 | Lists the four design pieces as concrete first steps (transport, identity envelope, age rule, re-sanitising) and ties #477 to a read-only purpose | Medium |
| U-003 | Variant 3 | Links Q18 to the Q3 close option for Coder#477 | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The observer snapshot (observe snapshot v1) is the right and only thing a TUIBBS screen would read; no other data source is in play | All three talk only about copying the snapshot | If TUIBBS wanted sweep facts or workspace status from Coder#477 instead, the channel question changes shape | UNSTATED, promoted |
| A-002 | The Coder#477 issue still exists and the CO-01 reply will be posted, so the channel sentence has a place to live | All three route the answer into the CO-01 reply | If Q3 closes #477 first, or the owner withholds CO-01, the answer has no public home but the ledger | UNSTATED, promoted |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001
- Taxonomy tags: L1 S-001; L2 C-001, C-002, C-003, X-001, X-002, U-001 to U-003; L3 C-004 (boundary), C-005 (boundary: who can read the data), X-003 (state), A-001 (guard), A-002 (state)

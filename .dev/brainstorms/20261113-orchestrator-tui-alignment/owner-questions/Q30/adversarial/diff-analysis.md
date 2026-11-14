# Diff Analysis: owner-answer proposal comparison (Q30, which coordinator Run OB-04 reads)

## Metadata
- Generated: 2026-11-14T02:50Z
- Variants compared: 3 (V1 = proposal-A, hold OB-04; V2 = proposal-B, a real Run from the owner's ordinary work at a quiet moment; V3 = proposal-C, a disposable representative Run opened for the test)
- Total differences found: 15
- Categories: structural (1), content (4), contradictions (3), unique (3), shared assumptions (3: UNSTATED 2, STATED 1)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Section set | five sections, 4 steps | five sections, 4 steps | five sections, 4 steps | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Which Run is read | none | a real coordinator Run from other work | a disposable Run opened for the test | High |
| C-002 | Setup cost | none | none | a test coordinator session, a test worker and its worktree | Medium |
| C-003 | Written acceptance of consumption | none needed | for a Run carrying real work | for a disposable Run | High |
| C-004 | Effect on OB-06 (guard flip) | held indefinitely | can proceed if the attempt passes | can proceed if the attempt passes | Medium |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Representativeness against possible harm | no evidence, no harm | most representative, a real question may be lost | representative in mechanism (listener, acknowledgement), nothing of value lost | High |
| X-002 | OB-04 criterion (1): the Run "carries no work whose questions matter" (`merged-requirements.md:252`) | complies (no Run) | conflicts: a Run from real work carries questions that matter | complies | High |
| X-003 | Who opens the Run | n/a | already open (owner's own work) | the owner opens a coordinator session for the test (a coordinator is person-opened) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | OB-03 can still run and be recorded while OB-04 is held | Low |
| U-002 | V2 | Compare the coordinator's own view before and after the read to detect a lost question | Medium |
| U-003 | V3 | Tear down the test Run, worker and worktree afterwards | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | The observer can be run in "the holder terminal" while a Claude coordinator session holds the Run there (for example through that session's shell). Whether a person can use the panel in a terminal that already holds a Claude coordinator session is UNVERIFIED (INV-024; ADJ `:146`) | V2 and V3 both run the read "in that coordinator's own terminal" | High (state, L3) | UNSTATED, promoted |
| A-002 | A consumed question can be detected afterwards without itself consuming (plain `check` reads and removes, ADJ `:97`), so the record can truthfully say "whether any question disappeared" | V2 and V3 (OB-04 (2)) | High (guard, L3) | UNSTATED, promoted |
| A-003 | OB-03 (seeded test) passes before OB-04 | all | Medium | STATED (`merged-requirements.md:252` (1)), not promoted |

## Summary
- Total structural differences: 1
- Total content differences: 4
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, X-001, X-002, A-001, A-002
- Taxonomy tags: S-001 L1; C-001, C-002, C-004, X-003 L2; C-003, X-001, X-002, A-001, A-002 L3
- Diff points debated: S-001, C-001 to C-004, X-001 to X-003, A-001, A-002 (10)

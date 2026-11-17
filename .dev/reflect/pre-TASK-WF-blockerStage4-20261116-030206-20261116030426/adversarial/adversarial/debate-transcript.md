# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 (invariant probe)
- Convergence achieved: 95.65 percent on the unanimous basis (22 of 23 diff points unanimous after Round 2; the 23rd, A-003, has a 2 to 1 majority); 100 percent on the protocol's majority basis. Round 1: 13 of 23 unanimous.
- Convergence threshold: 80 percent
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (V1 sonnet class, V2 haiku class, V3 opus class; each argued its own variant)
- Statements are on disk, one file per advocate and round, not inlined here: `debate/round1-advocate-1.md`, `debate/round1-advocate-2.md`, `debate/round1-advocate-3.md`, `debate/round2-advocate-1.md`, `debate/round2-advocate-2.md`, `debate/round2-advocate-3.md`. The invariant probe is `invariant-probe.md`.

## Round 1: Advocate Statements
See `debate/round1-advocate-{1,2,3}.md`. Each holds position summary, steelman of the other two variants, strengths, weaknesses, concessions, ACCEPT/REJECT/QUALIFY on A-001 to A-003 (no omissions) and a grade for every point. Round 1 disagreements: C-002 (blocking, minor, blocking), C-010 (minor, drop, minor), C-011, C-012, C-015, X-001, X-002, X-003, S-001 and A-003 (accept, accept, reject).

## Round 2: Rebuttals
See `debate/round2-advocate-{1,2,3}.md`. Decisive moves: Advocate 1 read stage 3 Task 8 (S3:118-127) and showed it names no spec-panel text and that stage 3 edits none; Advocate 2 withdrew its claim that stage 3 migrates the spec-panel pins and moved C-002 from minor to blocking; Advocate 3 re-read the evidence behind every blocking grade and added the conditional point N-1. Advocate 1 moved C-010 to drop, C-011 to minor and C-015, S-002, X-003 to drop. All three agree on every final grade.

## Round 2.5: Invariant Probe
See `invariant-probe.md`: 21 findings, 9 addressed, 12 unaddressed (0 HIGH, 5 MEDIUM, 7 LOW). No HIGH unaddressed item, so the convergence gate is not blocked. MEDIUM items are warnings: INV-006, INV-007, INV-008, INV-012, INV-017.

## Scoring Matrix (final grades)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | drop (card layout) | 90% | The saved V2 card is already normalised; not a plan defect |
| S-002 | drop (card property) | 85% | Two labels on V2 rows; grading rule grades plan defects |
| C-001 | V1, V2, V3 (blocking) | 95% | P4:37 against S3:158 and S3:162; all three concede |
| C-002 | V1 (blocking, conditional on stage 3 as written) | 85% | MAP:55,58,71,72 pin the phrase P4:89 removes; S3:122 names no spec-panel; no stage 4 task runs MAP |
| C-003 | V1 and V3 (minor) | 90% | The allow-list is in `refs/scale-map.md` (S1:59, S3:144) |
| C-004 | V1 (minor) | 90% | tdd file holds only lowercase "after" at :125; P4:24 pins by content |
| C-005 | V1 (minor, folded under C-002) | 85% | FR-8 at spec-panel.md:332 is reached by P4:89's grep |
| C-006 | V1 and V3 (MEDIUM after probe INV-008) | 80% | Five pinning modules never run after the last edit |
| C-007 | V1 (minor) | 80% | P4:84 never orders the pointer that P4:90 expects |
| C-008 | V1 (MEDIUM with C-001 after probe INV-017) | 75% | Gate checks run after edits; a halted run cannot be corrected in place (README:3) |
| C-009 | V1 and V3 (minor) | 80% | "T1 passes", "consumer-line instruction" are not content pins |
| C-010 | drop (process note) | 85% | No edit to plan text can change when it was generated; P4:20 and P4:36 gate execution |
| C-011 | V2 (minor) | 70% | Task 2 has no cap pin; digest equality protects the cap content |
| C-012 | drop | 85% | A matrix omission of the review run, not a plan defect |
| C-013 | V3 (minor) | 75% | T2 reads tracked files (S1:209); only the reverse-scan half of P4:102 is vacuous |
| C-014 | V3 (minor) | 70% | S1:96 row model; origin is upstream |
| C-015 | drop | 80% | No instruction puts the consumer line in a fence; T1 runs at P4:102 |
| X-001 | drop (weight sits on C-002) | 90% | Different objects: acceptance lines, three named tests, one unrun test |
| X-002 | folded into C-006 | 85% | Byte identity attainable; the missing run is the gap |
| X-003 | drop | 85% | Same as S-002 |
| A-001 | QUALIFY (3 of 3) | 90% | Stage 1 and 3 plans are the contract, not completed evidence; C-002, C-013, C-014 are conditional on them |
| A-002 | QUALIFY (3 of 3) | 90% | Per-task QA fails on confirmed blocking findings; minor wording is cleared |
| A-003 | ACCEPT (2 of 3; V3 advocate REJECT) | 65% | P4:37 is a separate bullet from the ledger check P4:36 |

## Convergence Assessment
- Points resolved: 22 unanimous plus 1 by majority (A-003) of 23
- Alignment: 95.65 percent (unanimous basis)
- Threshold: 80 percent
- Status: CONVERGED (taxonomy levels L1, L2 and L3 all covered; no HIGH-severity UNADDRESSED invariant)
- Unresolved points: none (A-003 stands on a 2 to 1 majority)

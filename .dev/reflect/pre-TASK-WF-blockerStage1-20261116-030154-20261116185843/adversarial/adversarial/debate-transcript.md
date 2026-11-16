# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential), plus Round 2.5 invariant probe
- Convergence achieved: 100 percent of diff points have a majority winner (25 of 25; 12 unanimous on the winner); grade agreement is narrower (see Convergence Assessment)
- Convergence threshold: 80 percent
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (sonnet, haiku, opus classes; general-purpose agents)
- Full statements: `debate/round1-advocates.md`, `debate/round2-rebuttals.md`; invariant probe: `invariant-probe.md`; per-point tracking: `debate/convergence-tracking.tsv`

## Round 1: Advocate Statements
See `debate/round1-advocates.md` (condensed statements, steelmen, concessions, A-001 to A-003 answers and the three per-point tables, kept in full). Headline: advocate 3 withdrew variant 3's PASS in Round 1 and adopted C-001 and C-003 as blocking; advocate 1 held C-001 blocking at 58 percent; advocate 2 held C-001, C-002 and C-003 blocking.

## Round 2: Rebuttals
See `debate/round2-rebuttals.md`. Order: advocate 1, advocate 2, advocate 3. Movement in Round 2: advocate 1 held C-002 and C-003 non-blocking (as in Round 1; C-002 at 68 percent after conceding that the `source` fallback does not cover a row that exists, C-003 at 68 percent) and kept C-001 blocking at 55 percent; advocate 2 kept all three blocking but conceded that no named exit test or acceptance line fails for C-002 or C-003 (its basis is a wrong or missing result); advocate 3 kept C-002 non-blocking, moved C-003 from blocking (60 percent) to non-blocking (65 percent) because no stage 1 exit test or requirement needs the tag, and kept C-001 blocking at 65 percent. One grade moved after rebuttal: C-003 (advocate 3).

## Round 2.5: Invariant Probe
See `invariant-probe.md` (8 findings; 2 HIGH unaddressed: INV-001 and INV-002, both on the C-001 repair).

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | none | 85% | Layout differences carry no correctness advantage |
| S-002 | Variant 1 | 60% | A stated split condition matches the real ambiguity; the verdict turns on C-001 |
| S-003 | Variant 2 | 90% | Distinct finding ids; variant 1 has the `R3-Fk` slip |
| C-001 | Variant 1 | 65% | Task 3 gives no lens-scale values; STAGE2:57 reads the cell with no `Conditional` rule (blocking, 3 of 3 advocates) |
| C-002 | Variant 3 | 62% | Right mechanism and non-blocking grade; `ReviewerJudge` feeds no stage 2 figure (STAGE2:28, 135) |
| C-003 | Variant 2 | 70% | Real gap (no plan writes `unsettled`); no stage 1 requirement or exit test needs it (non-blocking, 2 of 3) |
| C-004 | Variant 1 | 75% | No NA supplier for C; REQ-18 lift is the designed fallback; shadow only |
| C-005 | Variant 1 | 70% | Offers/consent logic has no owner; T8 can still be met if consent is built into the filing code |
| C-006 | Variant 1 | 75% | Task 12 inputs are executor-invented; tests still pass |
| C-007 | Variant 1 | 90% | `pending` is an Offers state, not an item state |
| C-008 | all | 85% | Stale stage 2 quotes; harmless |
| C-009 | Variant 3 | 75% | A fence literal in `doctor.py` fails T2 only if written; stage 4 anticipates it |
| C-010 | Variant 3 | 75% | `STRICT_T2` effect unstated; stage 4 adds the behaviour if absent |
| C-011 | Variant 3 | 68% | Banned-phrase scans are tracked-file scans not run in stage 1 |
| C-012 | Variant 2 | 80% | Audit-artifact omission, not a plan defect |
| C-013 | all | 92% | All three verified the earlier fixes |
| X-001 | Variant 1 | 65% | Grade of C-001: blocking |
| X-002 | Variant 3 | 62% | Grade of C-002: non-blocking |
| X-003 | Variant 2 | 62% | Variant 2 found the unowned tag; its grade is non-blocking |
| X-004 | Variant 1 | 60% | NEEDS-REVISION on C-001 alone |
| X-005 | none | 80% | A MEDIUM row beside `blocking: yes` is an ambiguity of presentation, not a contradiction of substance |
| A-001 | QUALIFY | 90% | Executors may fill a gap from the spec only where the spec gives one answer |
| A-002 | ACCEPT | 70% | Stage 2 is read as it stands; stale quotes are harmless |
| A-003 | QUALIFY | 75% | A static read shows reachability and counterexamples, not passing tests |
| A-004 | n/a (STATED) | 100% | Named in each brief |

## Convergence Assessment
- Points resolved: 25 of 25 (majority winner on every point; unanimous on 14 including the stated A-004)
- Alignment: 100 percent on winners (weak evidence by itself: with three voters a point lacks a majority only when all three differ, risk RK18 of the spec)
- Grade agreement on the three contested findings: C-001 blocking 3 of 3 (confidences 55, 76, 65); C-002 non-blocking 2 of 3; C-003 non-blocking 2 of 3
- Threshold: 80 percent
- Status: CONVERGED on the diff points; the invariant gate was BLOCKED by INV-001 and INV-002 (HIGH) and is cleared only through refactor-plan change PC-01 (see `refactor-plan.md`)
- Unresolved points: none

# Base Selection

Disclosure: scoring was done once by the orchestrator in a single context. The dual-pass position-bias mitigation of the skill was NOT run with independent evaluators; the criterion verdicts below are single-pass. The merge below does not depend on the choice of base for correctness, because it is a union of adjudicated findings.

## Quantitative (50%)
Requirement set R = the 10 adjudicated real findings (sync-dev, baseline pids, sleep check, off-path review, contains/ends, setsid reasoning, scope wording, teardown assertion, dependency chain, pkill-vs-pid).

| Metric (weight) | V1 | V2 | V3 |
|---|---|---|---|
| RC (0.30): findings covered / 10 | 0.40 | 0.50 | 0.70 |
| IC (0.25): 1 - contradictions/claims | 1.00 | 0.92 (F2 labelled Blocking and MEDIUM) | 1.00 |
| SR (0.15): concrete / (concrete + vague) | 0.90 | 0.88 | 0.92 |
| DC (0.15): resolved references / references | 0.90 | 0.95 | 0.85 (one wrong test-line citation) |
| SC (0.15): sections / max sections | 0.60 | 1.00 | 0.60 |
| quant_score | 0.730 | 0.805 | 0.816 |

## Qualitative (50%): criteria met out of 30
| Dimension (5 each) | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|
| Completeness | 3 | 4 | 4 | V1 left Tasks 2-3 and the HC5/stream wording unaddressed |
| Correctness | 4 | 3 | 4 | V1: "before" grep claim missed line 52; V2: UC-2 class on plan findings, F2 double label; V3: C-009 citation wrong |
| Structure | 4 | 2 | 4 | V2 did not use the requested card shape |
| Clarity | 4 | 3 | 5 | |
| Risk coverage | 3 | 3 | 4 | |
| Invariant and edge-case coverage | 1 | 1 | 3 | V3: wrapper-launch setsid, pkill vs pid, teardown. Floor 1/5 met by all |
| qual_score | 19/30 = 0.633 | 16/30 = 0.533 | 24/30 = 0.800 | |

## Combined
| Variant | Combined | 
|---|---|
| V3 (refactorer, opus class) | 0.808 |
| V1 (analyzer, sonnet class) | 0.682 |
| V2 (qa, haiku class) | 0.669 |

Selected base: V3. Margin over the runner-up 12.6 points; no tiebreaker needed.
Strengths to incorporate: from V1 the scope-wording finding and the sync-dev detail; from V2 the HC5 and `contains` findings (graded minor by debate); from the probe INV-001, INV-002, INV-003.

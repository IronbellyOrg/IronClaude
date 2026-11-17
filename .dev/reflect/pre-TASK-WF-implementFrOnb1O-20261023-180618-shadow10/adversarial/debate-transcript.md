# Adversarial Debate Transcript — reflect-pre card merge
Depth: standard. Rounds: 2 + invariant probe. Advocates: the three cards' positions (card = Round 1 statement; calibrated spot-checks = independent cross-examination). Judge: inline orchestrator (sonnet class; collision with V1 recorded in panel/notes.md), consistent with the shadow03/04/06 configuration.

## Round 1 (card positions)
- V1 (analyzer): 3 findings; C-01/C-03 candidates dismissed with reasons; T6 diff coverage confirmed.
- V2 (qa): 6 findings; matrix maps 1:1 to source.md spans; INF-003 coverage caveat; 5 AC/ledger anchor defects.
- V3 (refactorer): 1 finding; three-copy sync verified sound; plugin-parity coverage verified; agent-rule gap.

## Round 2 (rebuttals via calibration cross-examination)
- vs V1-F3: calibrator-1 (independent) — plan:70 covers 3.4 step 1; V1 concedes the sub-item; remaining items (3.3 step 2, 3.1 step 1, 3.6 row) stand (plan:59,61 vs ACs plan:67-74). V2-F3's three items independently stand.
- vs V1 citations: calibrator-1 — progress.md has 18 lines; V1-F1 cites 40-42, V1-F2 cites 52 (out of range). Claims stand on other citations; citation objects go to the Wave-5 validator.
- vs V2-F1: V3's independent check (closed key list + example preserved) and t5-checks.log:5-6 rc=1 confirm names/examples unchanged; the changed lines (t5.diff:9-14) are description lines inside the key block. QUALIFIED: finding survives as evidence-scope ambiguity (the check does not name its scope), not as inaccuracy.
- vs V2-F5 count: orchestrator recount — T6 lists 10 doc lines; ledger anchors 5 (commands.md:43,70,456,695 + session:125). Count confirmed.
- vs V3-F1: no rebuttal; corroborated by repo's recorded mirror-drift class (deviation-patterns memory).

## Round 2.5 invariant probe
| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | guard_conditions | "AC coverage" claims must quote the AC text, else reviewer misreads (X-001 did) | ADDRESSED | MEDIUM | plan:70 vs V1-F3 |
| INV-002 | count_divergence | V2-F5's 5/10 anchor count | ADDRESSED | LOW | progress.md T6 row recount |
| INV-003 | interaction_effects | T7 regression test was the natural home for the agent-rule pin (U-003 x V1-F1) | ADDRESSED | LOW | t7.diff:47-54 helper scope |
| INV-004 | sufficiency_challenge | no "fix X greens test Y" claim produced by this debate | ADDRESSED | LOW | vacuous — category N/A per protocol |

## Scoring Matrix
| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 | merge (cluster) | 95% | two cards independently, cal 0.70 both |
| C-002 | V2 item list + V1 reduced list | 85% | plan text read resolves X-001 |
| C-003 | V2 | 80% | recount confirms |
| C-004 | V2 qualified | 75% | t5-checks scope unnamed |
| X-001 | V2/plan text | 90% | plan:70 explicit |
| X-002 | V2 qualified | 70% | ambiguity stands |
| U-001..U-003 | unique, kept | 85% | uncontradicted + corroborated |

## Convergence Assessment
Points resolved: 10/10 (after X-001 resolution). Alignment: 1.00. Threshold 0.80. Status: CONVERGED. Taxonomy coverage: L1 (C-001 wording-level), L2 (C-002/C-003 structure), L3 (X-001 guard-level AC semantics) all covered. Invariant gate: 0 HIGH UNADDRESSED. debate_skipped_similar: false (10 findings, 2 real contradictions).

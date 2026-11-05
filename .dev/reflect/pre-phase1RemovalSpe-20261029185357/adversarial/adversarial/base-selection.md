# Base Selection

Variants are reviewer cards, so "requirements" are the 12 original findings that the debate confirmed and kept, all of which the orchestrator verified against real files. Scores were computed by the orchestrator (debate-orchestrator role).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.833 | 0.167 | Confirmed findings covered: 10/12 vs 2/12 |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | No intra-card contradictions. Factual errors (R1-F1 overstated, R1-F4 fresh direction, R2-F2 "can pass") count under qualitative Correctness, not IC |
| Specificity ratio (SR) | 0.15 | 0.90 | 1.00 | R1-F10 was `grounded: false`; every other finding carries a concrete `file:line` and fix |
| Dependency completeness (DC) | 0.15 | 0.98 | 1.00 | V1 has one prospective citation (`load.md:27`, added by Task 11, per calibrator); all others resolve |
| Section coverage (SC) | 0.15 | 1.00 | 0.75 | Top-level keys 8 vs 6 |
| **quant_score** | | **0.932** | **0.713** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric (CEV)

| Dimension | Criterion | V1 | V2 | Evidence |
|---|---|---|---|---|
| Completeness | 1 covers the reviewed scope | MET | NOT MET | V1 spans Tasks 1, 4, 8, 10, 12, 13, 18; V2 only Constraints and Task 18 |
| | 2 edge/failure scenarios | MET | MET | V1 F5, F8; V2 F2 stale-file overwrite |
| | 3 dependencies | MET | NOT MET | V1 F3 (Task 4 to Task 5 dependency); V2 none |
| | 4 success criteria (fix per finding) | MET | MET | every finding has `fix:` |
| | 5 out of scope stated | MET | MET | V1 self_audit lists unfinished checks; V2 F1 is about scope limits |
| Correctness | 1 no factual errors | NOT MET | NOT MET | R1-F1 "many more files" and R1-F4 `$T/fresh` direction; R2-F2 "can pass" and R2-F1 "nothing stopping" |
| | 2 feasible fixes | MET | NOT MET | R2-F2's fix keeps the unfiltered rg, so Task 18 stays unpassable |
| | 3 terminology consistent | MET | MET | |
| | 4 no internal contradictions | MET | MET | |
| | 5 claims evidenced | MET | MET | calibrator: all findings confirmed |
| Structure | 1 logical order | MET | MET | IMPORTANT before MINOR |
| | 2 consistent hierarchy | MET | MET | |
| | 3 one concern per finding | NOT MET | MET | R1-F8 bundles 3 dirs; R1-F10 bundles two unrelated defects |
| | 4 navigation aids | MET | MET | finding IDs; V1 line remap |
| | 5 artifact conventions | MET | MET | both match the brief schema (`reviewer-briefs/reviewer-N.md`, about :500 and :1330) |
| Clarity | 1 unambiguous | MET | MET | |
| | 2 concrete | MET | MET | |
| | 3 each finding one sentence | MET | MET | |
| | 4 terms defined | NOT MET | MET | V1 uses "T1", "SER", "row C2" unexplained; V2 spells out the leftovers |
| | 5 actionable | MET | MET | |
| Risk coverage | 1 ≥ 3 risks with impact | MET | NOT MET | 10 vs 2 |
| | 2 mitigation each | MET | MET | |
| | 3 failure modes | MET | MET | V1 F3 test breakage; V2 F1 executor failure mode |
| | 4 external dependencies | MET | MET | V1 F5 env var; V2 F1 Coder-owned leftovers |
| | 5 validation mechanism | MET | MET | V1 F9 test addition; V2 F2 seed-and-assert |
| Invariant & edge | 1 collection boundaries (missing/empty) | MET | NOT MET | V1 F8 missing directories |
| | 2 state across components | MET | MET | V1 F5; V2 F2 stale HOME state |
| | 3 guard gaps | MET | MET | V1 F4 allowlist; V2 F1 constraint guard |
| | 4 count divergence / ranges | MET | NOT MET | V1 F6 (124-127 vs 128, 130) |
| | 5 interaction effects | MET | NOT MET | V1 F1/F2 cross-task ownership |

### Qualitative Summary

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 5 | 3 |
| Correctness | 4 | 3 |
| Structure | 4 | 5 |
| Clarity | 4 | 5 |
| Risk coverage | 5 | 4 |
| Invariant & edge | 5 | 2 |
| **Total / 30** | **27 (0.900)** | **22 (0.733)** |

### Edge Case Floor Check
V1 5/5 eligible; V2 2/5 eligible.

## Position-Bias Mitigation

| Pass | Order | Disagreements | Resolution |
|---|---|---|---|
| 1 | V1, V2 | none | |
| 2 | V2, V1 | 1: V2 Structure-5, first scored NOT MET for lacking `self_audit` | Re-evaluated against the brief schema: `self_audit` is required only for zero-finding cards, so the final verdict is MET |

Verdicts changed by re-evaluation: 1.

## Combined Scoring

| Variant | quant × 0.5 | qual × 0.5 | Final |
|---|---|---|---|
| Variant 1 | 0.466 | 0.450 | **0.916** |
| Variant 2 | 0.356 | 0.367 | **0.723** |

Margin: 19.3 points, so no tiebreaker is needed. Debate points won: V1 13, V2 3 (C-011, C-012 and its X-001 share), with 3 shared.

## Selected Base: Variant 1 (reviewer-1 card, analyzer)

- Selection rationale: it covers 10 of the 12 confirmed findings, including all three that end IMPORTANT (C-003, C-004, C-005), and scores 5/5 on invariant coverage. The weaker calibration (0.75 vs 0.77) is reflected by correcting its overstated claims (R1-F1, R1-F4's fresh half), not by down-weighting the whole card.
- Strengths to preserve: per-task executability checks; concrete per-finding fixes; the self-audit refuting T1 R-2.
- Strengths to incorporate from Variant 2: R2-F1 (narrowed per INV-007), R2-F2 (DoD-3 seeding), the spec-inherited deviation classification (A-002), and the correction that a filtered check must still prove something (X-001).
- Weaknesses to fix in base: severities that ignored plan:29 (F1, F2, F6 down to MINOR); the F3 claim strengthened with test mechanics; F4 corrected and extended (INV-001, INV-002, filter, seeds); F10 trimmed and grounded.

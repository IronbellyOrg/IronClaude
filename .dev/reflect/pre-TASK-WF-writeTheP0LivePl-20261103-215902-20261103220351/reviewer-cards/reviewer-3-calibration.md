# Wave 3C blind calibration of reviewer-3-card.yaml

Calibrator: confidence-calibrator, model class fable (disjoint from reviewer classes). All 29 citations Read and verified; no mismatches. Card self_confidence (0.80) ignored.

| Dimension | Score | Reason |
|---|---|---|
| Citation grounding | 0.92 | Every file:line quote matches its source; one interpretive misread in R3-03. |
| Coverage completeness | 0.85 | Touches Constraints, the procedure and Tasks 1-5 and all three assigned Tier 1 refs; no coverage ledger stated. |
| Deviation-classification clarity | 0.75 | One stance per finding with rationale; rubric taxonomy not used; R3-04 and R3-05 are plan-text defects a pre-execution edit removes. |
| Risk surface coverage | 0.95 | False AC-0.4 FAIL, lost evidence after --force removal, unreleased live worker, retry re-running a live check. |
| Recommendation actionability | 0.90 | Every fix names a plan location and concrete text; success criteria implicit. |

Calibrated confidence: 0.87.

Per finding:
- R3-01 sound.
- R3-02 sound.
- R3-03 weak: the downgrade of F-017 holds, but the stated cost is wrong; qa.md:310 lists "the current full plan" as FINAL input, so moving the procedure would not drop it from the reviewer's input.
- R3-04 sound (cross-run leakage inferred from capabilities:113/127; the departure from spec step 7 is direct).
- R3-05 sound.
- R3-06 sound.
- R3-07 sound (plan:104 already hedges "when they exist").
- R3-08 sound.
- R3-09 sound.

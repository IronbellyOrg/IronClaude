# Calibration Report

## Per-dimension scores

| Dimension | Score | Reason |
|---|---:|---|
| Citation grounding | 0.75 | All cited pending-row/report/plan references and intact-token captures match; some source checks and 6/12 metric lack precise references. |
| Coverage completeness | 0.80 | Every source requirement semantically maps on independent Read; card lacks explicit mapping/metric explanation. |
| Classification clarity | 0.70 | Zero findings with clear dismissal reasons, but no rubric categories. |
| Risk coverage | 0.70 | Main missing future proofs stated; no check for tests pinning old wording documented in card. |
| Actionability | 0.70 | PASS needs little action but card names no specific next target. |

## Confidence

C=(0.75+0.80+0.70+0.70+0.70)/5=**0.73**. Five-dimension arithmetic mean. Low score reflects thin documentation, not a discovered plan defect. No numeric self-confidence inherited; pending calibration slot ignored.

## Notes

Model-class diversity degraded. All spot-checked references match, including five pending rows and required applied-fix review. Current historical help captures show the rejected option intact. Source requirements were independently Read and all mapped semantically. Planned suites exist; root imports confirmed. Possible existing-test collision was explicitly UNVERIFIED by this calibrator, not promoted to a defect. No commands, writes or tests.

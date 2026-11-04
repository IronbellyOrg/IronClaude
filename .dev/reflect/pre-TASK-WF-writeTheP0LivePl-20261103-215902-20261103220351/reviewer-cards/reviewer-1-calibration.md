# Wave 3C blind calibration of reviewer-1-card.yaml

Calibrator: confidence-calibrator, model class fable (disjoint from reviewer classes). 27 citations Read and checked; card self_confidence (0.78) ignored.

| Dimension | Score | Reason |
|---|---|---|
| Citation grounding | 0.90 | Every spot-checked cite matches; R1-05's "no occurrence" claims and R1-06/R1-11 inferences are tagged but not artifact-backed. |
| Coverage completeness | 0.85 | All eight Tier 1 findings plus four new ones across Constraints and Tasks 1-5; no coverage ledger. |
| Deviation-classification clarity | 0.85 | One stance and one severity per finding; R1-05 split tag and R1-10 blocking severity are the only hedges. |
| Risk surface coverage | 0.90 | End-state staging breach, unbounded hang, retry-ladder evidence loss, double worker on resume, base-ref mismatch. |
| Recommendation actionability | 0.85 | R1-03's "stated maximum wall time" and R1-11's fallback lack a concrete value. |

Calibrated confidence: 0.87.

Per finding:
- R1-01 sound. R1-02 sound. R1-03 sound. R1-04 sound. R1-05 sound.
- R1-06 weak: the user-name branch prefix is inferred from one branch name, not from an Orca rule; the fix is still cheap and correct.
- R1-07 sound. R1-08 sound. R1-09 sound. R1-10 sound.
- R1-11 weak: CR-01:51 shows baseRef for a master-based worktree; it says nothing about how --base-branch <local branch> resolves, so the failure mode is speculative. A help check is still fine.
- R1-12 sound.

Advisory weighting: R1-06 and R1-11 advisory; the other ten carry full weight.

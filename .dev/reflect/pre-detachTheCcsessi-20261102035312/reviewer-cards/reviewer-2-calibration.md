# Calibration Report — reviewer-2 card (qa, haiku slot -> glm-5.3); calibrator opus (calibrator_diversity: full)

Persisted by the parent on receipt.

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.90 | every cite checked; finding 1 omits that the script also writes home/ and seen inside SCRATCH (orca_close_repro.py:81-88) |
| Coverage completeness | 0.90 | 23 units = 16 Aligned + 5 Refinement + 2 Drift; residual declared; no explicit coverage_pct |
| Deviation-classification clarity | 0.75 | finding 3 "weakened" filed as Refinement; finding 1 a wording error filed as Drift; finding 4 arguably Aligned |
| Risk surface coverage | 0.80 | phase ordering, fixture terminate(), no `$!`/wait verified; missed: Task 1 `pgrep -f <tmp copy path>` cannot see a leftover `sleep`; "kill any remaining root process" vs source "kill the root group" |
| Recommendation actionability | 0.55 | no recommendations; findings name gaps but no fixes |

C = (0.90 + 0.90 + 0.75 + 0.80 + 0.55) / 5 = **0.78** (self-reported 0.82; delta -0.04). Card-level verdict: ESCALATE (low_confidence).

Per-finding verdicts: 1 overstated (real wording defect; source intent "prints ... output saved as" is redirect-compatible -> LOW); 2 confirmed (LOW); 3 confirmed (category leans Drift); 4 confirmed (arguably Aligned); 5 confirmed; 6 confirmed (HTTP GET does not signal the shims).

input_absent: assertions_path, now_iso.

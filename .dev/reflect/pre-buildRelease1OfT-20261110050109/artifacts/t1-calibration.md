# Tier 1 blind calibration (confidence-calibrator, opus)

- calibrated_confidence: 0.30 (card self-report 0.80). The low value comes from the rubric default "runtime claim with no runtime evidence" (runtime check 0.0 caps the total at 0.30); scored as a static plan review the calibrator gives 0.75.
- Citations: 6 of 6 grounding citations spot-checked and correct (install_user_setup.py:198, sprint/monitor.py:443, sprint/tui.py:122, eval/pty_stream.py:94, main.py:559-561, pyproject.toml:16, 36-37, 78-83).
- Correction found: the card's union coverage arithmetic was wrong. With 20 covered and 1 partial, the union is 20.5/21 = 0.976 when the partial counts half, 1.00 when it counts as covered, 0.952 when it counts as zero.
- Weak spots named: task mappings not cited to tasklist lines; no recompute procedure for coverage; F-1 to F-4 propose no fixes; F-5 is not a finding.
- Recommendation: escalate to the heterogeneous ensemble (already forced by coverage_degraded: parsed-sparse).
- Class note: calibrator ran on opus, the same class as reviewer 2, so calibrator_diversity is degraded.

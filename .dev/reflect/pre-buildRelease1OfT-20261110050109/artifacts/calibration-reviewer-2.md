# Calibration of reviewer 2 card (confidence-calibrator, sonnet)

- calibrated_confidence: 0.80 (reviewer self-report 0.80). Scored as a static plan review. Dimensions: evidence grounding 0.5 (four findings claim more than their own citations show), runtime check 0.5, symptom coverage 1.0, reproducibility fit 1.0, fix directness 1.0, domain coherence 1.0.
- Supported: QA-01, QA-02, QA-03, QA-05 (with caveat: Task 7 reports "cycle overran" but does not bound the cycle), QA-06, QA-07, QA-09, QA-10.
- Partly supported (narrow before acting): QA-04 (plan line 118 already keeps the previous snapshot after a failed cycle; only the FAILED (shape) mapping is unpinned), QA-08 (Task 11 line 182 already asserts NOT AVAILABLE), QA-11 (plan line 126 defines the STALE and FAILED strip cells and header "as of"; only the per-value "as of HH:MM:SS" qualifier is unbuilt), QA-12 (plan line 20 already cites owner-decisions items 1 and 5 for the stack; only the unfailable spike criterion stands).

# Calibration of reviewer-2-card.md (persisted by the parent from the confidence-calibrator agent's returned report)

Calibrator: confidence-calibrator on the sonnet alias (claude-gw-tier1b), disjoint from the reviewer classes (opus, haiku); same class as the executor.

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.95 | All 11 file:line citations match the files on disk. The card also mentions a "coverage matrix" that is not in the card. |
| Coverage completeness | 0.80 | Says five requirements are covered but gives four evidence bullets and no per-requirement mapping or coverage figure; the claim is correct but implicit. |
| Deviation-classification clarity | 0.60 | "Findings: None" is vacuous; the plan's negative-control and ruff checks go beyond the one-line spec, but the card never labels them Aligned or Refinement. |
| Risk surface coverage | 0.65 | Three edge cases covered and verified (missing file, forced install, false-positive stale report); no blast-radius reasoning such as other `filecmp` users; says "None found" outright. |
| Recommendation actionability | 0.75 | "Accept the plan without changes" is a clear disposition; it names no command or artifact to check. |

Arithmetic mean: (0.95 + 0.80 + 0.60 + 0.65 + 0.75) / 5 = 0.75. Calibrated confidence: 0.75. No self-reported confidence in the card, so no delta.

Citations: 11 of 11 verified, 0 failed.

Notes from the calibrator:
- Mode mismatch: this is a pre-mode review, but the card cites post-execution artifacts (finished test, check log, `done/` location); it reviews the executed state.
- Unrepeated evidence: the reviewer ran nothing; the negative-control result is supplied evidence, which the card admits.
- Model label: the header says claude-gw-tier2 (haiku alias) while the card self-reports "GPT-5"; diversity checks use the recorded class, not the self-report.
- Not checked: other `filecmp.cmp` callers (the calibrator had Read only).

Escalation recommendation: ESCALATE (rule: C < 0.85). Practical read: the plan is small and every conclusion verifies; keep the card as a weighted input at 0.75.

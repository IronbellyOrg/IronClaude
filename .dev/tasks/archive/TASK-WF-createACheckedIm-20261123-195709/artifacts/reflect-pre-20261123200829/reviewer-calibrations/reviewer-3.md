# Calibration Report

## Per-dimension scores

| Dimension | Score | Reason |
|---|---:|---|
| Citation grounding | 0.85 | Each finding spot-check matched; broad scope/coverage claims lack per-row citations. |
| Coverage completeness | 0.80 | Assigned rows asserted covered; additional cross-task references in Task 3/4 bodies not enumerated as separate findings. |
| Classification clarity | 0.75 | Grades clear, but F1/F2 distinction thin and some categories outside rubric set. |
| Risk coverage | 0.75 | Per-task isolation blind spot and weak negative assertion found; limited blast-radius discussion. |
| Actionability | 0.90 | Exact three public commands and four baseline paths supplied; independent re-review proposed. |

## Confidence

C=(0.85+0.80+0.75+0.75+0.90)/5=**0.81**. Five-dimension mean. Model-class diversity degraded. Pending output placeholder not used as self-confidence.

## Notes

F1 supported: Task 4 lines 80/82 refer to prior observations/sibling commands while template line 15 and executor qa.md:9 restrict a reviewer to that task plus Constraints and diff. Blocking (Missing) is defensible; speculation about substituting CliRunner is unnecessary to establish it. F2 cross-task references verify but grade comparison needs debate. F3 hyphen splitting is demonstrated by captured warning-mode and opt-in text; F4 wording note verifies. No tests or commands were run; no files written.

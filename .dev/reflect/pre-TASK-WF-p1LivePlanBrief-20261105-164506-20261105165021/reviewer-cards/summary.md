# Reviewer cards (summary; reply text was returned by the agents, not written by them)

- Reviewer 1 (analyzer, sonnet): 3 deviations (2 Drift, 1 Authorized expansion), 27 of 30 units adherent, 1 advisory correctness gap (stale tip pin).
- Reviewer 2 (qa, haiku class label; the agent definition pins sonnet): 11 deviations (10 Drift, 1 Authorized expansion). 7 are coverage-matrix omissions, not plan defects. No Regression.
- Reviewer 3 (refactorer, opus): 6 deviations (2 Regression, 2 Drift, 2 Necessary). Regression 1 is the stale tip pin; Regression 2 is `--setup run`.
- Blind calibration of the T1 card: C = 0.55 (`artifacts/t1-calibration.md`). Per-card calibration of the three reviewer cards was not run.
- Model note: the `reflect-reviewer` agent file sets `model: sonnet`; the model parameter passed per spawn may not override it, so the real model classes of reviewers 2 and 3 are UNVERIFIED and class diversity is recorded as degraded.

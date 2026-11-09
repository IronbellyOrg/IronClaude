# Reflect deviation patterns: issue-438

## pre-design-20261108041729 (UC-1, /sc:issue --create issue type and Complexity field plan review)
- Verdict partial (tier 2, convergence 1.00, calibrated 0.81): 1 blocking and 10 minor plan defects; no Regression (nothing ran). One citation range was dropped by the validator and corrected.
- Recurring plan-defect class: a task that rewrites or adds a `gh api` or `gh pr` line in a skill, command or agent file breaks the exact-line classification table in `tests/skills/test_worker_contract.py` (`WRITE_VERB_CLASSIFICATION`, keyed on verbatim line text); the plan must update that table and run that file, not only `tests/skills/test_issue_protocol.py`.
- Recurring plan-defect class: plan acceptance checks that run one test file hide failures in neighbouring test files that read the same edited files (`tests/commands/test_issue_command.py`, `tests/skills/test_issue_worker_agents.py`).
- Recurring plan-defect class: new "must fail if behaviour breaks" tests specified as substring or name-presence checks do not fail on a swapped mapping or a broken format; specify the exact strings and a mutation check.
- Reflect mechanics: a spec with `Q1`-style labels (no `R-`/`REQ-`/`SPEC-` ids) gives 0 Pass-1 ids, so `coverage_degraded: parsed-sparse` forces tier 2 (same as the launch-level-hook plan review).

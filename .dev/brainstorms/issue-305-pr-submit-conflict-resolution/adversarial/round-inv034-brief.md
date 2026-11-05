# INV-034 focused round: brief (orchestrator)

Why this round: after the invariant-resolution round, INV-034 is the only HIGH finding still blocking convergence (debate-transcript.md, refactor-plan.md). All three advocates agree that an empty check list right after a push must be `polling`, not `clean`. They split on how the wait ends: B and C propose a short settle window; A rejects a time window as racy.

Candidate rule for the advocates to ACCEPT / REJECT / MODIFY (orchestrator proposal, derived from the round-inv files; not a variant's text):

- **R-034 (evidence-based, no time window):** when the CI wait starts on a head this run just pushed, look at the checks of the PR head the push replaced (`pre_push_sha`, already polled earlier in the run or readable once).
  - If the replaced head had at least one check run or required check, an empty list on the new head is `polling` until checks appear or `--timeout` expires (expiry is `TERMINAL_TIMEOUT` for the CI wait as today, never `clean`).
  - If the replaced head also had zero checks (both lists parsed and empty), the repo is treated as having no Actions and an empty list on the new head is `clean`, exactly as today.
  - A failed or unparsable read of the replaced head's checks counts as "had checks" (fail closed: keep polling).
  - Carrier: a keyword argument on `superclaude.pr_submit.ci.classify_checks` (for example `expect_checks: bool = False`, default preserving today's behaviour), set by the skill from the replaced head's result; tests in `tests/pr_submit/test_ci_classify.py`.

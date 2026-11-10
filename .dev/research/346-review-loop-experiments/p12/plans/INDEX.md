# A/B plans for the top 3 designs of RESEARCH-REPORT.md (baseline = Stage 2 arm 3, a3-r1..r6)

The owner decisions D1-D5 in `$SP/p14/DECISIONS-ADDENDUM.md` are applied to all three plans. Tokens are counted with each message id counted once. Cost rules decide on `R_LOOP` = test loop tokens / 100,424, where 100,424 is the loop-only baseline `A_BASE` and the AUD audits are excluded. `R_B` = (loop + one audit) / 169,468 is printed beside it and never decides. Each plan also has a Haiku robustness stratum: n=4 per test arm, Haiku loop workers, always two Sonnet audits, compared with `$SP/p14/haiku-baseline/results.json` and never pooled. Each plan also has a one-time 3-replicate Sonnet extension, used only when the n=6 result is INCONCLUSIVE.

- PLAN-1-k3-union-verify.md: design 3.1 (k=3 first reviews, deterministic merge, verify gate). Branch `346Claude-ab1-k3-union-verify`; runs b1-r1..r6 and Haiku runs b1h-r1..r4 in `$SP/p12/ab1`.
  - Sonnet stratum: about 50 workers (max 72); about 1.36M loop-only output tokens (2.19M with the audits).
  - Haiku stratum: about 33 workers (max 48); about 0.91M Haiku loop tokens (ceiling 1.36M) plus 0.55M Sonnet audit tokens.
  - Conditional extension: about 25 workers; 0.68M loop-only tokens.
  - Predicted `R_LOOP` about 2.26, against the DROP-2 cost limit of 2.0.
- PLAN-2-verify-gate.md: design 3.2 (verify-before-fix gate, k=1). Branch `346Claude-ab2-verify-gate`; runs b2-r1..r6 and b2h-r1..r4 in `$SP/p12/ab2`.
  - Sonnet stratum: about 40 workers (max 60); about 0.72M loop-only tokens (1.55M with the audits).
  - Haiku stratum: about 27 workers (max 40); about 0.48M Haiku loop tokens (ceiling 0.72M) plus 0.55M audit tokens.
  - Conditional extension: about 20 workers; 0.36M loop-only tokens.
  - Predicted `R_LOOP` about 1.20, against the ADOPT/DROP-2 limit of 1.25 (borderline).
- PLAN-3-final-gate.md: design 3.3 (final whole-document gate, at most one gate loop, stall rule, ceiling of 5 reviews / 3 fix cycles). Branch `346Claude-ab3-final-gate`; runs b3-r1..r6 and b3h-r1..r4 in `$SP/p12/ab3`.
  - Sonnet stratum: about 48 workers (max 60); about 1.24M loop-only tokens (2.07M with the audits).
  - Haiku stratum: about 32 workers (max 40); about 0.83M Haiku loop tokens (ceiling 1.24M) plus 0.55M audit tokens.
  - Conditional extension: about 24 workers; 0.62M loop-only tokens.
  - Predicted `R_LOOP` about 2.05, against the DROP-3 limit of 1.8 (expected to fire).

Every plan gives each final spec two frozen Sonnet audits and keeps both strata together at or under 6 concurrent workers. The product edits of all three plans were checked in a throwaway clone of 69ac8b33: the new tests fail before the edits and pass after them, the 273 pinned tests pass, and ruff is clean. With design 3 applied, `tests/skills` plus `tests/unit` gave 1 failure, `test_task_workspace_smoke.py::test_installer_ships_scripts_and_documented_invocation_runs`, which also fails on 69ac8b33 without the edits.

Under the loop-only convention, two cost rules change their expected result. Plan 1's DROP-2 cost clause is expected to hold (`R_LOOP` about 2.26; `R_B` about 1.74 would have passed), so the 0.75-1.20 blocker band becomes DROP-2 instead of INCONCLUSIVE. Plan 3's DROP-3 is expected to fire (`R_LOOP` about 2.05; `R_B` about 1.62 would have passed). Plan 2's 1.25 limit is borderline (`R_LOOP` about 1.20, range 1.13-1.27). The plans keep the stricter loop-only results.

Open questions (I could not resolve these from the files):
1. The Haiku baseline (`$SP/p14/haiku-baseline/results.json`) did not exist yet on 2026-11-10. Its runs were at R1. So the Haiku token figures above use Sonnet per-step costs, and a Sonnet ADOPT reads "ADOPT (Haiku robustness pending)" until the baseline lands.
2. The baseline second audits under `$SP/p12/baseline-audit2/` now exist for all six runs. The plans score them with `blocking_findings()` instead of trusting `results.json` `n_blocking`, so the PROVISIONAL label should not be needed. Re-check this at analysis time.
3. The three plans make no new baseline runs. The coordinator can ask for two fresh baseline replicates to check for drift (about 0.34M output tokens, deduplicated).

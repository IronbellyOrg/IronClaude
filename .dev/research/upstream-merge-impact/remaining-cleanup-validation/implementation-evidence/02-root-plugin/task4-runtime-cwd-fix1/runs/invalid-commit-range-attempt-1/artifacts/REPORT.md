# /sc:sc-reflect — STOPPED (precondition)

- **Status:** failed — stopped at Wave 0 input validation; no audit performed
- **Mode:** post (explicit `--mode post`)
- **launch_cwd:** `/tmp/ironclaude-reflect-runtime-bqyukdxl`
- **audit_repo_root:** `.../task4-runtime-cwd-fix1/fixtures/project` (from `git -C <scope> rev-parse --show-toplevel`)
- **Scope:** `src/`

## Reason

`--commit-range NOT_A_REAL_REF..ALSO_NOT_REAL` does not resolve:

- `git -C <audit_repo_root> rev-parse --verify NOT_A_REAL_REF^{commit}` → exit 1
- `git -C <audit_repo_root> rev-parse --verify ALSO_NOT_REAL^{commit}` → exit 1
- `HEAD^{commit}` → exit 1 (the repository has no commits)

An unresolved input is not evidence. Post mode needs a resolvable diff, commit range, or task log, and none was supplied, so the protocol STOPs (§3.3). No substitute range was invented. The untracked fixture files (`changes.patch`, `execution.log`) were not used in place of the requested range.

## What did not run

Tier 1 card, blind calibration, tier routing, Tier-2 reviewers/snapshot, the adversarial merge, the evidence-validator gate and Wave 7 promotion (also suppressed by `--no-promote`). No agents were dispatched. Calibrated confidence, deviation counts and merge method are all null. The repository was not mutated.

## To run a real audit

Re-run with a resolvable source, for example `--diff <path-to-patch>` or `--task-log <path>`, or `--commit-range` against real commits once the repo has history. Use a fresh output directory.

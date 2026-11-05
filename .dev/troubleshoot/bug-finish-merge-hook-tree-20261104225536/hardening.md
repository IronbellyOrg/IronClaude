# Pipeline Hardening Closure (Wave 4.5)

## HC0 — Applicability + boundary scan
| boundary_type | producer / transformers / consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|
| CLI/subprocess | finish-merge.sh -> `git commit` -> repository commit hooks | probe-c4.out:2-5 | a subprocess (hook) changes the artifact after validation | applicable | the defect is a subprocess altering what the gate proved |
| gate-status-enum | finish-merge.sh tokens -> refs/conflict-mechanical.md step 9 table -> merge_preflight_dirty | conflict-mechanical.md:124 | a false pass publishes unvalidated content | applicable | the gate controls HALT vs publish |

pipeline_hardening_applicable: true
Mechanism statement: a gate validated an intermediate artifact (the index) while a later step with external code (commit hooks) produced the published artifact (the commit); without a post-condition binding the two, the proof does not cover what is published.
known_escapes_caught: []

## HC1 — Runtime-entrypoint verification: PASS
The regression tests run the real script with a real pre-commit hook (test_hook_that_changes_staged_content_is_tree_dirty_after_the_commit, test_hook_that_changes_nothing_still_finishes); negative witness: the first fails against 62121669 (audit.log).

## HC2 — Contract enumeration: PASS
`tree_dirty` after the commit -> merge_preflight_dirty (conflict-mechanical.md:124) unchanged in meaning, row text and message extended; exit codes, one-line stdout and the single `git commit` unchanged (test_finish_script_static_rules); SKILL.md:331 (pinned E12) unchanged.

## HC3 — Unmask and sweep: N/A
Rationale: the check compares two tree object ids for equality; no parser or classifier is involved.

## HC4 — Effective-input proof: N/A
Rationale: no review/audit selector is involved.

## HC5 — Off-path review
off_path_review_decision: performed (independent troubleshoot-analyst self-review of the round-2 diff; result in audit.log and .dev/pr-monitor/pr-378-20261104214804/review-round2-1.md)

## Verdict
waiver_status: none; HC3, HC4 N/A with rationale -> pipeline_hardening_verdict: advisory (row 6). backtest_status: not_run.

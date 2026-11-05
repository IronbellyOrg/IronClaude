# Pipeline Hardening Closure (Wave 4.5)

## HC0 — Applicability + boundary scan
| boundary_type | producer / transformers / consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|
| CLI/subprocess | session -> scripts/collect-conflict-evidence.sh -> git read commands | probe-evidence.out:7-8 | a child command can outlive the budget the script promises | applicable | the defect lives in how the script bounds a subprocess |
| persisted-state | run-log `sync_started` -> resume row 5/7 restart -> evidence directory | refs/conflict-mechanical.md:71, :253 | a resumed attempt reuses state written by an earlier attempt | applicable | the defect is a resume path meeting persisted files |
| gate-status-enum | EVIDENCE_FAIL tokens -> refs/conflict-intent.md:30 -> sync_tier3 | collect-conflict-evidence.sh:25-26 | a wrong token or exit would misroute the cycle | applicable | tokens and exit codes must stay unchanged |

pipeline_hardening_applicable: true
Mechanism statement: a bounded-execution contract was enforced only between subprocess calls, and a write-once output directory was keyed by an identifier that a resume deliberately reuses; both let a proof substitution through (a "bounded" run that is not, a "fresh" directory that is not).
known_escapes_caught: [] (no E1-E5 escape ID is earned by a cited passing card here)

## HC1 — Runtime-entrypoint verification: PASS
The regression tests run the real script as a subprocess (tests/pr_submit/test_conflict_scripts.py test_without_timeout_a_hung_read_is_stopped_at_the_budget, test_without_timeout_a_normal_run_still_succeeds, test_restart_attempt_collects_into_a_fresh_attempt_directory; tests/pr_submit/test_conflict_e2e.py test_x3_resume_restart_collects_into_a_new_attempt_directory), not a helper or mock. Negative witness: the hang test fails against the HEAD script (audit.log).
runtime_entrypoint_card_path: this file, section HC1

## HC2 — Contract enumeration: PASS
| producer | consumer | contract | status |
|---|---|---|---|
| collect-conflict-evidence.sh fail() | refs/conflict-intent.md:30 | `EVIDENCE_FAIL timeout` token, exit 2 | unchanged (test asserts the token) |
| conflict_attempt() | refs/conflict-mechanical.md step 3 | attempt number of the cycle | new; unit tests |
| step 3 `cycle_dir` | conflict-intent.md (--out, resolution.md, validator output_dir); conflict-mechanical.md step 6, step 9; test_conflict_e2e.py | `<output-dir>/sync/<cycle_id>/a<attempt>/` | all consumers updated; protocol pin test_every_attempt_writes_under_its_own_attempt_directory |
contract_ledger_path: this file, section HC2

## HC3 — Unmask and sweep: N/A
Rationale: no generated-artifact parser, allow-list grammar or substring classifier is added or changed; the tokens are fixed literals asserted by equality.

## HC4 — Effective-input proof: N/A
Rationale: no review/audit selector consumes an indirect file selection in this fix; the evidence-validator's output_dir narrowing to `<cycle_dir>` is a direct path, covered by the protocol pin.

## HC5 — Off-path review
off_path_review_decision: performed (independent troubleshoot-analyst self-review lens over the full fix diff, review.md in the PR #378 round-1 monitor directory; result recorded in audit.log)

## Verdict
waiver_status: none; HC3 and HC4 N/A with rationale, no FAIL -> pipeline_hardening_verdict: advisory (truth table row 6: "ADVISORY — scoped closure with rationalized N/A"). backtest_status: not_run.

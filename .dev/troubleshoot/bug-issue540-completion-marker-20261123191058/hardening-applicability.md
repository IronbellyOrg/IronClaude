# Pipeline Hardening Applicability

## Boundary scan

| boundary_type | producer | transformers | consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|---|---|
| CLI/subprocess | run_cmd | dispatch/normalize/reduce/state | filesystem completion oracle | real foreground/restart commands, import paths and raw artifact checks | helper tests can pass while real CLI omits publication | applicable | Public entrypoint must be replayed. |
| persisted-state | _run_resume_branch | manifest recovery -> reduce -> state | resumed-job marker polling | real resume output and source continuation | normal-path-only repair leaves resume defective | applicable | Separate continuation has the same omitted call. |
| sibling-pipeline | normal run / detached child / kill / reflect | distinct execution ownership | common completion expectations | contract-ledger.md and child argv Read | shared-writer proof can mask caller omission | applicable | Every owning completion surface must be classified. |
| generated-artifact-parser | DoneSentinel | writer JSON serialization | external polling/JSON consumer | reduce.py:383-440 and monitoring docs | status/path/schema may diverge from the completed contract | applicable | Real marker must be parsed and compared after repair. |

## Mechanism statement

A lifecycle implementation can persist a terminal state and return success while omitting a required completion artifact. Tests that directly exercise the artifact helper or assert only terminal state substitute adjacent proof for the owning public-entrypoint behavior. Completion must be verified on actual emitted artifacts after the public operation, including sibling continuations and conditional policy.

## Applicability and escape coverage

pipeline_hardening_applicable: true (set once)
known_escapes_caught: [] (no generalized replay catch-rate claim)
backtest_status: not_run
waiver_status: none (no accepted waiver; absent repaired proof is an explicit FAIL)

## Wave verdicts

| Wave | Status | Evidence/reason |
|---|---|---|
| HC1 | FAIL | runtime-entrypoint.md: negative real CLI witness captured; no fix-applied positive witness or repaired ordering proof. |
| HC2 | PASS | contract-ledger.md: consumers and sibling completions classified, without claiming repair. |
| HC3 | N/A | unmask-sweep.md: no behavior-controlling prose parser; source sibling sweep recorded. |
| HC4 | N/A | effective-input.md: explicit evidence paths, not an indirect review selector. |
| HC5 | PASS | Independent diagnostic review completed; blocking B1 corrected and rechecked in cycle1. No waiver; not repaired-product approval. |

pipeline_hardening_verdict: blocked (truth-table priority2, sticky HC1 failure regardless of later reviewer result)
off_path_review_decision: performed (diagnostic review PASS after correction/recheck; product closure still blocked)
NOT PROVEN: repaired completion behavior. Diagnosis and repair closure are distinct. The mapping from an ordinary hardening failure to diagnostic report status is not explicit, and HC1 has no defined pending pre-fix state. This run conservatively chose HC1 FAIL/reportblocked; a rationalized pre-fix N/A/advisory interpretation is acknowledged but not adopted. No downstream stage may silently clear the recorded failure or use helper tests as repaired CLI acceptance.

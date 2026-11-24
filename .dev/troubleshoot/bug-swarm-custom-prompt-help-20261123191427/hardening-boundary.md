# Pipeline Hardening Closure

## Boundary scan

| boundary_type | producer | transformers | consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|---|---|
| CLI/subprocess | two help literals in commands.py | Click formatting and public command registration | operator and run option parser | actual full help/rejection captures | source-only wording check could substitute for accepted public invocation | applicable | Guidance crosses a public CLI boundary and can advertise an unsupported input. |
| file-stdin-prompt | JobSpec custom_prompt_dir | preflight directory materialization | schema/prompt consumers | preflight.py1569-1615 and schema.py685-734 | adding a flag to match prose would change supported delivery interface | applicable | Supported configuration belongs in spec-file input; semantics must remain unchanged. |
| review-selector | explicit source/capture paths | none | diagnosis reviewers | explicit brief paths | unrelated staged task packages could be mistaken for fix evidence | not_applicable | No indirect implementation-diff selector or repaired-state claim is used. |

## Mechanism

Human-readable guidance duplicates an input contract without registering that input at the consuming parser. Editing a help literal alone can look sufficient while the real public output remains stale or its recommended invocation remains unsupported. Proof must pair the actual negative public observation with a repaired public-output and parser regression witness.

pipeline_hardening_applicable=true (set once).
known_escapes_caught=[]; no broad replay coverage claimed.

## Off-path review

HC5 decision=required, status=FAIL for repaired-state closure: help producer and run consumer expose divergent guidance. No independent review of an applied fix/effective repaired surface exists because this is diagnosis-only. Independent formation/calibration and final citation validation do not substitute for that review. No waiver asserted for HC5.

## Verdict

HC1 FAIL, HC2 PASS, HC3 N/A with rationale, HC4 N/A with rationale, HC5 FAIL.
waiver_status=latched (absent mandatory positive runtime witness).
backtest_status=not_run.
pipeline_hardening_verdict=blocked, truth-table priority2 (any FAIL), also missing-proof priority3. NOT PROVEN: repaired-state public-entrypoint witness and independent repaired-surface review. No prohibition of help reruns was inferred; this is not blocked-on-authorization or a claim that the static wording observation is uncertain.

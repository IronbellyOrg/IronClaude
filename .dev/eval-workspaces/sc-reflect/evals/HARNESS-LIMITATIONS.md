# Eval Harness Known Limitations

## Offline-grader harness limitation (FR-RH1 reachability cases 42/43/44)

The offline grader (`grader.py grade_eval`) only grades `with_skill/`/`old_skill/`-prefixed
assertions against on-disk output files; it embeds no live producer. The reachability cases
(ids 42/43/44: `uc2-reachability-proxy-oracle-unproven`, `uc2-reachability-no-reachability-skip`,
`uc2-reachability-missing-inputs-skip`) assert against `with_skill/outputs/contract.yaml` /
`runtime-reachability-ledger.yaml` / `REPORT.md`, which exist ONLY after a live `/sc:reflect`
run. Therefore an offline grade of these 3 producer cases grades 0 of them — this is EXPECTED,
is LOGGED here, and is NOT a failure. These cases are validated by a live skill run, not the
offline grader.

> This is an authored statement of operational truth, not a citation of a pre-existing sentence
> in `grader.py`, the decision doc, or iteration logs.

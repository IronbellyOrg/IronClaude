# D-0078 — Evidence

## Implementation

* `tests/cli/eval/test_reporter_contract.py` (new test file, 4 cases).
* `.dev/releases/current/cliEval/artifacts/D-0078/spec.md` — test matrix
  + acceptance-criteria mapping.
* `.dev/releases/current/cliEval/artifacts/D-0078/notes.md` —
  implementation notes + hand-off to T04.10 / T04.19.

## Verification

Command (from `phase-4-tasklist.md` §T04.17 step 5):

```
uv run pytest tests/cli/eval/test_reporter_contract.py -v
```

Result: **4 passed, 0 failed** — full pytest log saved at
`.dev/releases/current/cliEval/evidence/T04.17/test-output.txt`.

Per-test PASS rows:

```
tests/cli/eval/test_reporter_contract.py::test_n_prime_equals_k_lets_every_emitter_render PASSED
tests/cli/eval/test_reporter_contract.py::test_skipped_rows_included_in_evals_with_skip_reason PASSED
tests/cli/eval/test_reporter_contract.py::test_n_prime_vs_k_mismatch_raises_and_maps_to_exit_code_two PASSED
tests/cli/eval/test_reporter_contract.py::test_reporter_json_validates_against_summary_schema PASSED
```

## Acceptance-criteria cross-reference

| AC (from phase-4-tasklist.md §T04.17) | Evidence |
|---|---|
| File `tests/cli/eval/test_reporter_contract.py` contains 4 tests covering N'-vs-K equality, skipped inclusion, mismatch failure, JSON schema fidelity. | The four pytest functions enumerated above (one per scenario). |
| `uv run pytest tests/cli/eval/test_reporter_contract.py -v` exits 0 with all 4 passing. | `evidence/T04.17/test-output.txt` — 4 passed, exit 0. |
| Mismatch test asserts process exit code 2 and `ReporterContractViolation` raised. | `test_n_prime_vs_k_mismatch_raises_and_maps_to_exit_code_two` — asserts `REPORTER_CONTRACT_VIOLATION_EXIT_CODE == 2` and `isinstance(..., ReporterContractViolation)` alongside per-emitter raise checks (markdown / json / yaml / junit / writer). |
| `TASKLIST_ROOT/artifacts/D-0078/spec.md` records the test matrix. | `spec.md` (this directory). |

## Files

```
tests/cli/eval/test_reporter_contract.py
.dev/releases/current/cliEval/artifacts/D-0078/spec.md
.dev/releases/current/cliEval/artifacts/D-0078/notes.md
.dev/releases/current/cliEval/artifacts/D-0078/evidence.md
.dev/releases/current/cliEval/evidence/T04.17/test-output.txt
```

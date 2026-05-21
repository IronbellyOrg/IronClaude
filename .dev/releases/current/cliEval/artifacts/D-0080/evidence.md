# D-0080 — Evidence

## Implementation

* `tests/cli/eval/test_artifact_reproducibility.py` — new test module,
  8 cases covering the FR-G4 reproducibility matrix (run-dir pattern,
  determinism, per-eval `logs.jsonl`, per-eval `tty.transcript`,
  stack-trace duality, summary.json cross-links, byte-stable replay,
  parser negative guard).
* `.dev/releases/current/cliEval/artifacts/D-0080/spec.md` — test
  matrix + reproducibility invariant + acceptance-criteria mapping.
* `.dev/releases/current/cliEval/artifacts/D-0080/notes.md` —
  implementation notes + fixture construction rationale + T04.10
  hand-off.

## Verification

Command (from `phase-4-tasklist.md` §T04.20 step 5):

```
uv run pytest tests/cli/eval/test_artifact_reproducibility.py -v
```

Result: **8 passed, 0 skipped, 0 failed — pytest exit 0** — full log
saved at `.dev/releases/current/cliEval/evidence/T04.20/test-output.txt`.

Per-test status:

```
tests/cli/eval/test_artifact_reproducibility.py::test_run_dir_matches_fr_g4_pattern                  PASSED
tests/cli/eval/test_artifact_reproducibility.py::test_run_dir_deterministic_for_inputs               PASSED
tests/cli/eval/test_artifact_reproducibility.py::test_per_eval_logs_jsonl_present_and_parsable       PASSED
tests/cli/eval/test_artifact_reproducibility.py::test_per_eval_tty_transcript_present_and_non_empty  PASSED
tests/cli/eval/test_artifact_reproducibility.py::test_errored_outcome_records_stack_trace            PASSED
tests/cli/eval/test_artifact_reproducibility.py::test_summary_json_cross_links_per_eval_artifacts    PASSED
tests/cli/eval/test_artifact_reproducibility.py::test_artifact_tree_reproducible_across_replays      PASSED
tests/cli/eval/test_artifact_reproducibility.py::test_parse_run_dir_rejects_non_layout_paths         PASSED
```

No skips — every guard runs today. Unlike D-0079, this module is not
gated on T04.10 because it anchors the contract at the layout +
Reporter seam (see notes.md §"Module-level decisions"). When T04.10
lands the orchestrator must produce a tree conformant to the
invariants pinned here; nothing has to change in this file.

## Acceptance-criteria cross-reference

| AC (from phase-4-tasklist.md §T04.20) | Evidence |
|---|---|
| File `tests/cli/eval/test_artifact_reproducibility.py` asserts run dir matches `.dev/eval-runs/<ISO>/<run-id>/`. | Tests `test_run_dir_matches_fr_g4_pattern` (regex pin on `<output_root>/.dev/eval-runs/YYYY-MM-DD/HHMMSSZ-<8-hex>/`) and `test_run_dir_deterministic_for_inputs` (same `(suite_name, started_at)` → byte-identical path). |
| Per-eval `logs.jsonl`, `tty.transcript` exist; stack trace recorded on ERRORED status. | `test_per_eval_logs_jsonl_present_and_parsable` (JSONL exists + parseable), `test_per_eval_tty_transcript_present_and_non_empty` (transcript exists + non-empty), `test_errored_outcome_records_stack_trace` (traceback in BOTH the JSONL event log AND the rendered `summary.json` `evals[].expects[].failure.traceback`). |
| summary.json `evals[]` entries reference per-eval artifact paths. | `test_summary_json_cross_links_per_eval_artifacts` resolves every `evals[].artifacts` value against the run directory and asserts the resulting path exists on disk. `test_artifact_tree_reproducible_across_replays` reinforces by asserting two replays produce byte-identical `summary.json` (modulo the absolute run-dir prefix). |
| `TASKLIST_ROOT/artifacts/D-0080/spec.md` records the reproducibility matrix. | `.dev/releases/current/cliEval/artifacts/D-0080/spec.md` — §2 enumerates all 8 tests + their AC mapping; §3 pins the FR-G4 layout; §4 pins the cross-link contract; §5 pins the stack-trace channel duality. |
| Evidence saved under `TASKLIST_ROOT/evidence/T04.20/`. | `.dev/releases/current/cliEval/evidence/T04.20/test-output.txt` — pytest log capturing `8 passed in 0.17s`. |

## Files touched

* `tests/cli/eval/test_artifact_reproducibility.py` (new, 691 lines)
* `.dev/releases/current/cliEval/artifacts/D-0080/spec.md` (new)
* `.dev/releases/current/cliEval/artifacts/D-0080/notes.md` (new)
* `.dev/releases/current/cliEval/artifacts/D-0080/evidence.md` (this file)
* `.dev/releases/current/cliEval/evidence/T04.20/test-output.txt` (new — pytest log)

# D-0074 — Evidence

## Implementation

* `src/superclaude/cli/eval/artifact_layout.py` (new module).
* `tests/cli/eval/test_artifact_layout.py` (new test file, 19 cases).
* `.dev/releases/current/cliEval/artifacts/D-0074/spec.md` — directory
  layout spec.
* `.dev/releases/current/cliEval/artifacts/D-0074/notes.md` —
  implementation notes + handoff to T04.10.

## Verification

Command (from `phase-4-tasklist.md` §T04.13 step 5):

```
uv run pytest tests/cli/eval/test_artifact_layout.py -v
```

Result: **19 passed, 0 failed** — see
`.dev/releases/current/cliEval/evidence/T04.13/test-output.txt` for
the full pytest log.

## Acceptance-criteria cross-reference

| AC (from phase-4-tasklist.md §T04.13) | Evidence |
|---|---|
| Each run produces a directory under `.dev/eval-runs/<ISO>/<run-id>/` containing `summary.md`, `summary.json`, and a `per-eval/` subtree per eval. | `test_compose_run_dir_shape`, `test_compose_run_dir_anchored_at_run_dir_prefix`. End-to-end run-through deferred to T04.11 smoke once T04.10 wires the worker (the smoke skip-reason already documents this dependency). |
| Per-eval subtree contains `logs.jsonl`, `tty.transcript`, and `artifacts/`. | `test_allocate_per_eval_paths_creates_subtree`. |
| Run-id is deterministic for a given start timestamp + suite name. | `test_compose_run_id_deterministic_for_same_inputs`, `test_compose_run_id_changes_with_suite_name`, `test_compose_run_id_changes_with_timestamp`. |
| `TASKLIST_ROOT/artifacts/D-0074/spec.md` documents the directory layout. | `spec.md` (this directory). |

## Files

```
src/superclaude/cli/eval/artifact_layout.py
tests/cli/eval/test_artifact_layout.py
.dev/releases/current/cliEval/artifacts/D-0074/spec.md
.dev/releases/current/cliEval/artifacts/D-0074/notes.md
.dev/releases/current/cliEval/artifacts/D-0074/evidence.md
.dev/releases/current/cliEval/evidence/T04.13/test-output.txt
```

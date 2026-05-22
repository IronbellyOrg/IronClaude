# D-0074 — Implementation notes

## Scope landed in T04.13

* `src/superclaude/cli/eval/artifact_layout.py` — single-source-of-truth
  layout helpers (`compose_run_dir`, `compose_run_id`,
  `compose_per_eval_dir`, `allocate_per_eval_paths`,
  `parse_run_dir_components`, `PerEvalPaths`, `RunDirComponents`).
* `tests/cli/eval/test_artifact_layout.py` — 19 unit tests covering
  shape, determinism, idempotency, traversal-rejection, and
  round-tripping.
* This `spec.md` / `notes.md` / `evidence.md` triplet under
  `artifacts/D-0074/`.
* `evidence/T04.13/test-output.txt` — pytest log capturing the green
  run.

## Scope deferred to T04.10

`commands.eval_run` already references `_new_run_id`,
`_default_output_dir`, `_run_one_spec`, etc. — these helpers belong to
T04.10 (FR-CLI1 `eval run` body). T04.13 intentionally does **not**
land them. When T04.10 lands, the module-level helpers it defines
delegate to `artifact_layout`:

```python
from .artifact_layout import compose_run_dir, compose_run_id, allocate_per_eval_paths

def _utc_iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _new_run_id(started_at: str, suite_name: str) -> str:
    return compose_run_id(started_at, suite_name)

def _default_output_dir(started_at: str, suite_name: str) -> Path:
    return compose_run_dir(Path.cwd(), started_at, suite_name)
```

The `eval_run` body should compute `started_iso` *before* the default
output dir is derived so the same instant feeds both the run-id and
the date segment. Today the body computes `started_iso` after
`requested_output` is resolved (line 1439); T04.10 will need to
re-order those two lines.

## Per-eval log routing — recommended T04.10 patch

The per-eval worker closure (`_run_one_spec`) should call
`allocate_per_eval_paths(run_dir, eval_id)` and thread the resulting
paths into both the `EvalRunner` and the PtyDriver:

```python
paths = allocate_per_eval_paths(run_dir, spec.id)
runner = EvalRunner(
    home=home,
    config=config,
    executor=executor,
    run_dir=run_dir,
    artifacts_dir=paths.artifacts_dir,
    stdout_path=...,
    stderr_path=...,
    transcript_path=paths.tty_transcript,
    expect_callables=spec.expects,
    ...
)
```

`EvalRunner._flush_log` currently hard-codes
`home_path/.eval-logs/<eval_id>.jsonl`. T04.10 should add a
`log_path` constructor parameter (default unchanged) so the worker can
pin the per-eval JSONL log to `paths.logs_jsonl` without breaking the
existing tests that use the default behaviour.

## Design alternatives considered

### Random suffix instead of hash

Rejected — the AC explicitly requires deterministic run-ids. A random
suffix would force operators to read the run's manifest to discover
the run-id rather than re-deriving it from `(started_at, suite_name)`.

### Full timestamp in run-id (no date bucket)

Rejected — over time, `.dev/eval-runs/` would accumulate thousands of
flat entries. The per-day bucket keeps `ls` readable and matches
common CI archive conventions.

### Embed date segment inside run-id (single-segment layout)

Rejected — the FR-G4 layout pin in the phase-4 tasklist explicitly
specifies `.dev/eval-runs/<ISO>/<run-id>/`, a two-segment shape. The
spec keeps the date and run-id parts separable so reviewers can
navigate by date.

### Module location

`artifact_layout` is a sibling of `reporter.py`, `runner.py`,
`run_report.py`, etc. — every other layout / file-emission module
lives in `cli/eval/`, so introducing a new top-level subpackage would
have been gratuitous.

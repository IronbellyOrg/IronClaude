# D-0074 — FR-G4 reproducible artifact layout

**Roadmap row:** R-074 (FR-G4)
**Phase task:** T04.13 (phase-4-tasklist.md §T04.13)
**Implementation module:** `src/superclaude/cli/eval/artifact_layout.py`
**Test module:** `tests/cli/eval/test_artifact_layout.py`

## 1. Goal

Pin the on-disk shape of every `superclaude eval run` invocation so a
reviewer (or CI consumer) can locate the artifacts produced by any past
run by date + run-id alone — without grep-and-prayer over the
filesystem. The layout is the contract every downstream tool (the
Reporter, the per-eval JSONL emitter, the JUnit converter) writes
against.

## 2. Layout

```
<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/
    summary.md
    summary.json
    summary.yaml
    junit.xml          (only when --junit is set)
    per-eval/
        <eval_id>/
            logs.jsonl
            tty.transcript
            artifacts/
```

| Segment | Source | Purpose |
|---|---|---|
| `<output_root>` | `Path.cwd()` by default; `--output-dir` overrides | Anchor under which `.dev/eval-runs/` lives. Default lands inside the canonical AC12 (T01.19 / D-0016) scratch-root allowlist. |
| `.dev/eval-runs/` | `artifact_layout.RUN_DIR_PREFIX` | Repo-relative prefix. Matches `EvalConfig._default_allowed_scratch_roots`. |
| `<YYYY-MM-DD>` | UTC ISO date of `started_at` | Per-day bucket so reviewers can navigate by date without exploding `ls`. |
| `<run-id>` | `compose_run_id(started_at, suite_name)` | `<HHMMSSZ>-<8-hex>` — see §3. |
| `summary.{md,json,yaml}` | `Reporter.write()` (COMP-008 / D-0055) | DM-004 aggregated run summary in three formats. |
| `junit.xml` | `Reporter(emit_junit=True).write()` | Optional; FR-RPT2 feature-gated. |
| `per-eval/<eval_id>/` | `allocate_per_eval_paths(run_dir, eval_id)` | Self-contained subtree for one eval. |
| `logs.jsonl` | `EvalRunner` JSONL emitter (T03.05 / D-0049) | Per-eval lifecycle event log. |
| `tty.transcript` | `PtyDriver` (T02.10 / D-0033) | PTY capture for failure forensics. |
| `artifacts/` | Per-eval ExpectCallables / executor | Free-form artifact drop for the eval (jsonl logs, screenshots, etc.). |

## 3. Run-id determinism

`compose_run_id(started_at, suite_name)` returns the same string for the
same `(started_at, suite_name)` pair — the FR-G4 acceptance criterion
the phase-4 tasklist pins ("Run-id is deterministic for a given start
timestamp + suite name").

* **Shape:** `<HHMMSSZ>-<8-hex>`
* **Time prefix:** `HHMMSSZ` is the UTC time-of-day of `started_at`.
  Pure-numeric so the id sorts lexicographically by wall-clock time
  within a date bucket.
* **Hash tail:** First 8 hex chars of
  `sha256(suite_name + "\n" + started_at)`. Folding `suite_name` in
  guarantees runs against different suites at the same instant land in
  distinct directories.
* **Collision risk:** 8 hex chars = 32 bits. The hash is keyed by an
  ISO-second timestamp, so collisions require two runs *of distinct
  suites* at the exact same wall-clock second. The CI fleet does not
  approach this density.

### Why not a random suffix?

A random suffix would prevent reproducibility — the AC explicitly
requires determinism so an operator can re-derive the run-id from
`(started_at, suite_name)` alone (e.g. to look up a historical run
without consulting the run's own manifest).

## 4. Construction vs. creation

`compose_run_dir` and `compose_per_eval_dir` are **path-construction**
helpers — they return paths but do not touch disk. Mkdir is the
caller's responsibility, and **must happen after**
`resolve_scratch_root` (the AC12 / T01.19 enforcement boundary)
validates the constructed path against the allowlist.

`allocate_per_eval_paths(run_dir, eval_id, create=True)` is the only
helper that creates directories — it mkdir's the per-eval directory and
the `artifacts/` subdirectory. The `logs.jsonl` and `tty.transcript`
files are not pre-created; the runner / PtyDriver open them lazily on
first write so an unused eval leaves a clean subtree.

## 5. Routing

* **Reporter writes** (`summary.md` / `summary.json` / `summary.yaml` /
  `junit.xml`) — routed via `Reporter(summary, emit_junit).write(run_dir)`
  in `commands.eval_run`. The run_dir is the path
  `compose_run_dir(...)` constructs when `--output-dir` is unset, or the
  operator-supplied directory otherwise (in which case the AC12
  allowlist still gates the resolution).
* **Per-eval logs** (`logs.jsonl`) — routed via the per-eval worker
  closure that T04.10 wires up. The worker calls
  `allocate_per_eval_paths(run_dir, eval_id)` and threads the resulting
  paths into the `EvalRunner` constructor (`log_dir` override) and the
  PtyDriver (`transcript_path`).
* **Eval artifacts** (`per-eval/<eval_id>/artifacts/`) — populated by
  whatever ExpectCallables or executors choose to drop files there.
  The directory is pre-created so callers do not need to repeat the
  `mkdir(parents=True)` boilerplate.

## 6. AC12 interaction

`artifact_layout` constructs paths under `.dev/eval-runs/` so a default
run lands inside the canonical AC12 prefix
(`_default_allowed_scratch_roots` in `config.py`). The CLI body still
calls `resolve_scratch_root(requested_output, config=base_config,
output_dir=output_dir)` before the first `mkdir`; that call is the
single enforcement boundary. This module does not duplicate the check.

If the operator passes `--output-dir <X>`, `compose_run_dir` is **not
called** — the CLI uses `X` directly. AC12 then validates `X` exactly
as it did before T04.13.

## 7. Backwards compatibility

* `--output-dir <X>` continues to write the four summary files directly
  under `X` (the T04.11 FR-G6 smoke contract).
* The default behaviour (no `--output-dir`) gains the nested
  `.dev/eval-runs/<date>/<run-id>/` structure that T04.13 introduces.
  This is a no-op for callers that already pass `--output-dir`.
* `EvalRunner` retains its existing
  `home_path/.eval-logs/<eval_id>.jsonl` log destination; T04.10 will
  add a `log_dir` constructor parameter so the per-run worker can
  re-route logs into the FR-G4 per-eval subtree without breaking the
  default-home path that existing tests rely on.

## 8. Acceptance criteria mapping

From phase-4-tasklist.md §T04.13:

| AC | Where verified |
|---|---|
| Each run produces a directory under `.dev/eval-runs/<ISO>/<run-id>/` containing `summary.md`, `summary.json`, and a `per-eval/` subtree per eval. | `test_compose_run_dir_shape`, `test_compose_run_dir_anchored_at_run_dir_prefix`, end-to-end via T04.11 smoke once T04.10 wires the worker. |
| Per-eval subtree contains `logs.jsonl`, `tty.transcript`, and `artifacts/`. | `test_allocate_per_eval_paths_creates_subtree`. |
| Run-id is deterministic for a given start timestamp + suite name. | `test_compose_run_id_deterministic_for_same_inputs`, `test_compose_run_id_changes_with_suite_name`, `test_compose_run_id_changes_with_timestamp`. |
| `TASKLIST_ROOT/artifacts/D-0074/spec.md` documents the directory layout. | This file. |

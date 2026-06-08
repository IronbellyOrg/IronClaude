# Discovery — --eval fan-out layout + MODE_MATRIX (Step 3.1)

**Date:** 2026-06-03

## Run-dir path template (verbatim from `eval_pipeline.py`)

`collect_run_records` reads, for each `model` in the panel and each `run_number` in
`range(1, runs_per_model + 1)`:

```
.claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/outputs/recommendation.md
.claude/cache/eval-runs/iteration-<N>/<key>/<model>/run-<i>/timing.json
```

(`eval_runs_dir` defaults to `.claude/cache/eval-runs/iteration-<N>/`; `key_dir = eval_runs_dir/<key>`;
`run_dir = key_dir/<model>/run-<run_number>`.) The fan-out MUST write deliverables at these EXACT
paths or `collect_run_records` finds empty text and grades 0.

## MODE_MATRIX panels (verbatim from `eval_aggregate.py:16-21`)

| mode | models | runs_per_model | total Agent calls |
|---|---|---|---|
| `none` | [] | 0 | 0 (no-op) |
| `quick` | [opus] | 1 | **1** |
| `normal` | [opus, sonnet] | 2 | **4** |
| `deep` | [opus, sonnet, haiku] | 3 | **9** |

## Finalizer shell command (from `commands.py::eval_run`)

```
uv run superclaude recommend eval run --key <key> --mode <mode> --iteration <N>
```

This is the deterministic half (grade → aggregate → select best_model → patch lookup row); it
assumes the per-(model,run) deliverables already exist on disk under the layout above.

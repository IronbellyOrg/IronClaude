# Task 1: accepted failures (inputs, not evidence)

Both test baselines were run on branch `ironbelly/OrcaCLICommandRefactor-P2` at HEAD 576b6659 with no source change.

| Baseline file | Result | Failing tests |
|---|---|---|
| `ac-c3-baseline.txt` (`tests/skills/`) | `1318 passed in 13.87s`, `rc=0` | none |
| `t1-baseline-wider.txt` (wider run, `--ignore=tests/cli/eval/test_perf_home_setup.py`) | `9164 passed, 30 skipped, 1 xpassed, 5 warnings in 434.43s`, `rc=0` | none |

There is no `pre-existing` failure to label. Any failure in a later run is therefore new.

The five other baseline files exist next to this one:

- `uv-sync.txt` (`rc=0`)
- `verify-sync-baseline.txt` (`sync-dev rc=0`, `verify-sync rc=0`)
- `lint-baseline.txt` (`Errors: 0`, `Warnings: 5`, `lint rc=0`)
- `format-baseline.txt` (`4 files already formatted`, `rc=0`)
- `status-baseline.txt` (empty: no change under `src`, `tests` or `plugins` before this plan)

The baselines were produced by `/tmp/impl2/baselines.sh` before the owner decisions were recorded in the plan (the plan text changed, no test or source file did). `.baselines-done` in this folder is that script's completion marker.

# Step 0 results: the three no-model checks (2026-11-14)

No model was started. Scratch scripts and outputs are in `/tmp/sweep-step0/` (not committed). Sub-steps 0.4 to 0.6 of `IMPLEMENTATION.md` were not run.

| # | Check | Result | Decision |
|---|---|---|---|
| 1 | `uv run --frozen --project <repo> pytest -p no:cacheprovider tests/review -q` | 126 passed in 0.72 s | Pass. The code the design imports is healthy. Go on. |
| 2 | Search cost: `git grep -n -I -F --no-color -f <40 patterns> -- <scope>` with `LC_ALL=C`, three runs | 1,464 of 38,062 tracked files in scope; 39 patterns (the plan said 40); 29,932 matching lines; 0.91, 0.90, 0.90 s (median 0.90 s) | Under the 4 s threshold. Go on. The time table in `DESIGN.md` 12 stays. |
| 3 | Merge-keys probe: one real ember report (4 findings) merged as is and again with `"class":"C1","probe":"P1","src":"sheet"` added to every findings line | Both exit 0 and report `block_ok: true`. The merged report and the ledger contain none of the three keys; the two outputs differ only in the report path and its hash | Accepted, and the keys are dropped on merge. Matches `DESIGN.md` 9.3 (the merged report carries no such key). Telemetry must be read from the checked report, never from the merged report. Go on. |

## Limits of these results

- Check 2 used 39 common strings, so 29,932 matches is far more output than rare fixed strings would give. The time is for that load on this one repository at HEAD, with the scope written from `IMPLEMENTATION.md` step 0.3 (tests, scripts and docs folders, root files, files named changelog, history or changes). The design's own scope list (DD-5, including named paths) was not read, so the scope may differ.
- Check 3 used one report and one reviewer. It shows the keys are accepted and dropped for that case. It does not show behaviour for a report with an invalid line.
- The merge test file for this (`test_merge_accepts_class_probe_src_keys`) is not written yet.

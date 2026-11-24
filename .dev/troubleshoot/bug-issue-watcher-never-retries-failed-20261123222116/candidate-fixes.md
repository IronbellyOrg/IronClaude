# Candidate fixes

| # | Fix | Supporting agents | Verdict |
|---|-----|-------------------|---------|
| 1 | In `run_sweep`, retry `first_run` for a disabled config whose own first-run report says `first-run: failed` (not on dry run); read the report in a helper in first_run.py that checks both `<state_dir>/first-run.txt` and `<stem>-first-run.txt` beside the config | tier1 (0.83), root-cause-analyst (0.83), quality-engineer (0.75) | consensus |

Open design choice (not a competing fix): back-off for non-`config` failures (root-cause-analyst proposes 1 hour) and whether an explicit "needs first run" marker should replace the report (quality-engineer's alternative). No `split-pending` cluster; Wave 4 skipped.

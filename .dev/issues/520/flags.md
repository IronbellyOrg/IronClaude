# Flags decision

- Decided by: issue-worker-t1
- Depth: standard

| Field | Value | Reason |
|---|---|---|
| Mode | feature | given by the user (--mode feature), taken as is |
| Type | cli | the panel's code lives in the Python CLI package `src/superclaude/cli/review/` on origin/master (panel.py, panel_cmd.py, findings.py, ledger.py, merge_cmd.py, telemetry.py, data/review-panel.*.json) with the reflect runner in `src/superclaude/cli/reflect/`; spec-panel, workflow and reflect call that CLI, so command and skill are secondary (checked with Glob/Grep and `git ls-tree origin/master`; the current branch docs/409-orca-dashboard-designs has no `cli/review/`; codegraph and auggie not used) |
| Issue type | Feature | derived from the mode and the area by the rule in `refs/labels.md` |
| Complexity | Medium | follows depth (quick = simple, standard = medium, deep = complex) |

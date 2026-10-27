# D-0024: Sprint Post-Task Wiring Hook

## Deliverable
Post-task wiring hook in `src/superclaude/cli/sprint/executor.py` that runs `run_wiring_analysis()` after each task and applies mode-aware behavior.

## Implementation
- `run_post_task_wiring_hook(task, config, task_result)` function added
- Called after each task in `execute_phase_tasks()` loop
- Mode behavior:
  - off: skip analysis entirely, return immediately
  - shadow: run analysis, log findings, task status unchanged (SC-006)
  - soft: warn on critical findings, task status unchanged
  - full: block (set FAIL + gate FAIL) on critical+major findings
- Import path: `from superclaude.cli.audit.wiring_gate import run_wiring_analysis`
- Lazy import inside function to avoid circular dependency
- Exception handling: analysis failures logged and continued (no crash)

## Performance
- off mode: zero overhead (immediate return)
- shadow/soft/full: bounded by `run_wiring_analysis()` scan time
- Analysis scopes to `config.release_dir` (task-local)

## Evidence
```
T05.02 PASS: run_post_task_wiring_hook basic functionality verified
```

# Reviewer Card — root-cause-analyst (scope: R4 / R5 / R6)

| Req | Verdict | Severity | Class | Confidence |
|-----|---------|----------|-------|-----------|
| R4.1 acquire placement | PASS (after install+preflight, before orphan cleanup+preflight_phases) | LOW | none | 0.97 |
| R4.2 release-before-uninstall | PASS (executor.py:2284-2294) | LOW | none | 0.95 |
| R4.3 refusal sentinel + no double-fire | PASS (acquire OUTSIDE try@1727; finally not entered on refusal) | LOW | none | 0.93 |
| R4.x post-acquire/pre-try leak window | PARTIAL — atexit backstop only (1715-1725) | MED | drift | 0.85 |
| **R5 escape hatch in default tmux path** | **FAIL** | **HIGH** | **regression** | **0.97** |
| R6 disjoint-path assertion | PASS (cannot false-fire; bundle=results_dir/rerun-<ts>) | LOW | none | 0.95 |

Headline: `_build_foreground_command` (tmux.py:176-210) never re-emits `--ignore-run-lock`; tmux is the default path (commands.py:410); the inner worker (where R4.3 acquires the lock) gets `ignore_run_lock=False`. Fix = 2-line addition mirroring sibling flag blocks.

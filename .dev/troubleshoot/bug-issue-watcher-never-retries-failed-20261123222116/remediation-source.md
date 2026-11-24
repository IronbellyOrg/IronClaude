# Remediation source: issue 751, retry a failed first run

Source report: /home/coder/workspaces/worktrees/IronClaude/issue-751/.dev/troubleshoot/bug-issue-watcher-never-retries-failed-20261123222116/REPORT.md
Owner approval: "Recos approved, proceed" (chat, 2026-11-23): report-based retry, back-off for non-`config` failures.

## Summary

`run_sweep` (src/superclaude/cli/issue_watch/dispatch.py:427) calls `first_run` only when it generates a config. A config left `enabled: false` after a failed first run (for example `worktree_invalid`) is skipped as `not_enabled` forever. Add a retry gated on the config's own first-run report.

## Required behaviour (acceptance)

1. In `run_sweep`, before the `enabled is not True` skip: when the config exists, `_enabled(config_path) is False`, the sweep is not a dry run, and the first line of its first-run report starts with `first-run: failed`, call `first_run(config_path, defaults, runner, deps_factory)` once and re-read `_enabled`.
2. Retry a `config`-step failure on every sweep. Retry a failure at `label`, `dry_run`, `lock`, `restart` or `init_state` only when the report is older than 1 hour (injected `now`).
3. A disabled config with no report, or a `first-run: passed` report, stays `not_enabled`. A dry-run sweep makes no call and no write.
4. The report check is a read-only helper in `first_run.py` that reuses `_raw_config`, `_report_dir` and the report-name rule, so it finds the report in an absolute `state_dir` as `first-run.txt` and beside the config as `<stem>-first-run.txt`. Read without following symlinks, bounded size, any read error means no retry.
5. Existing store, lock and launch history are preserved (`first_run` already keeps an existing store).
6. Update the `dispatch.py` module docstring (lines 7-8) and the `not_enabled` text in `SKIP_REASONS` (line 66).

## Files to change

- src/superclaude/cli/issue_watch/first_run.py (helper)
- src/superclaude/cli/issue_watch/dispatch.py (retry branch, docs)
- tests/issue_watch/test_dispatch.py (new tests; existing tests need no change)

## Tests

Failed first run, then valid worktree, then next sweep enables and starts the child; repeated failure stays `not_enabled` with one `first_run` call per sweep; no report or `passed` report means no call; dry run makes no call and writes nothing; report beside the config (relative `state_dir`) is found; non-config failure inside the back-off makes no call and outside it retries once. Keep the GitHub-write boundary in tests/issue_watch/test_security_invariants.py intact.

## References

- REPORT.md (above), candidate-fixes.md, tier2-*-hypothesis.md in the same folder
- .dev/releases/backlog/issue-watcher-zero-setup/requirements.md R18, R28

## Pipeline Hardening

Not applicable: a sweep-loop control-flow gap in one module (HC0 not run).

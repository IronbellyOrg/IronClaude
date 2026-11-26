# Watcher architecture analysis

## Scope and grounding

Target: `src/superclaude/cli/issue_watch/` (15 Python modules, the issue-watcher poller), architecture focus, quick depth. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`, HEAD `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. Codegraph: index_state=fresh, checked_at=2026-11-24T02:36:21Z; degraded: none. Graph rows used as leads were confirmed by Grep or Read. The run modifies no source.
## Architecture and metrics

The package is a read-mostly poller with one launch side effect and two GitHub writers.

- Entry points live in `src/superclaude/cli/issue_watch/cli.py`: `once_command` at line 125 calls `cycle.run_cycle` (`src/superclaude/cli/issue_watch/cycle.py:1310`); `run_all_command` at line 470 sweeps every Orca repository (`src/superclaude/cli/issue_watch/dispatch.py`).
- `_Cycle.run` (`src/superclaude/cli/issue_watch/cycle.py:712`) stops with `not_enabled` before any external call when the config is off and the run is not a dry run (`cycle.py:715-716`).
- `first_run` (`src/superclaude/cli/issue_watch/first_run.py:125`) is the switch-on path: six ordered steps (config, label, state, dry run, lock test expecting exit 75, restart test), then it rewrites the config to `enabled: true` only when all pass (`first_run.py:152-153`, `first_run.py:219-254`).
- Launch is one function, `launch_argv` (`src/superclaude/cli/issue_watch/launch.py:136`), which builds a fixed 12-element `orca agent launch` command and rejects any prompt that `build_claim_prompt` (`launch.py:112`) did not produce.
- The ship gate `GOVERNED_LEVELS_ALLOWED = False` (`launch.py:48`) is applied in `_examine` (`cycle.py:1031-1036`): any Pipeline value other than None ends with `level_gated` and touches no store and no probe.
- Impact of `run_cycle` (depth 1): `once_command` (`cli.py:125`), `first_run` (`first_run.py:125`), plus tests. Callers confirmed: `once_command` calls it at `cli.py:129`.

Metrics: 15 modules; `cycle.py` carries 130 symbols and is the coupling point (used by 24 files); `launch.py` 37 symbols (15 files). Tests live under `tests/issue_watch/`; 20 fixture files remain under `tests/issue_watch/fixtures/_assumed_shape/`.
## Severity-rated findings

- High: the deployment gate the design states is bypassed by the automatic path. `docs/designs/issue-watcher.md:33` and `docs/designs/issue-watcher-setup.md:581` say no cron entry and `enabled` stays false until an owner-run live test replaces every assumed fixture and commits `docs/designs/issue-watcher-live-test.md`. Section 17 of the same runbook (`issue-watcher-setup.md:701-706`) says the first-run check sets `enabled` to true with no live test. On this host the cron entry exists and runs every minute (`crontab -l`, line `* * * * * ... superclaude issue-watch run-all`), and `~/.config/superclaude/issue-watch.d/IronClaude.json` has `enabled: true`.
- Medium: the assumed fixtures were never replaced. All 20 files under `tests/issue_watch/fixtures/_assumed_shape/` are still the guessed shapes, and `docs/designs/issue-watcher-live-test.md` does not exist. `OPERATION_ID_PATHS` and `OP_UNKNOWN_TEXT` are still marked UNVERIFIED in code (`launch.py:67-76`).
- Medium: the design's status line is stale again. `docs/designs/issue-watcher.md:3` still says "never run live; enabled ships as false; no schedule is installed". The audit log shows real cycles since 2026-11-23T21:56:04Z.
- Low: `first-run.txt` for IronClaude records `first-run: failed config: worktree_invalid` (`~/.local/state/superclaude/issue-watch/IronClaude/first-run.txt`), while the config is enabled and the Coordinator worktree exists today. The report and the live state disagree; which event came first is UNVERIFIED.
## Recommendations and roadmap

1. Reconcile section 17 of the runbook with the deployment gate in section 14.1, and update the status line at `docs/designs/issue-watcher.md:3` to the live state.
2. Run the capture sheet (`docs/designs/issue-watcher-setup.md:588-616`) against the real replies already being produced, replace the 20 assumed fixtures, and commit the live-test record.
3. Investigate the two `launch_unknown` cycles (exit 7) at 2026-11-23T22:12:11Z and 2026-11-23T22:13:13Z before widening the ship gate, since an unknown launch outcome is exactly the case the assumed fixtures model.

## Verification limits

Graph caller rows give the definition line, not the call site; only the `once_command` call site was confirmed by Read. Test counts were not collected (a collection run writes caches). No dynamic run was executed.

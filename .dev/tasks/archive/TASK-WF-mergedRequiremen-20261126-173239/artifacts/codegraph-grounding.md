# Codegraph grounding (workflow Wave 1, 2 and 4)

## Run state
- index_state: fresh (codegraph_status: 4157 files, 58323 nodes, "Changes since index: 0 added, 0 modified, 0 removed")
- checked_at: 2026-11-26T17:33Z
- worktree_root: the run-ledger worktree (`.dev/tasks/to-do/` package root's checkout)
- projectPath: the same checkout root
- access mode: MCP tools (`codegraph_status`, `codegraph_node`, `codegraph_search`, `codegraph_callers`)
- graph tokens: none

## Resolved symbols (each confirmed by a bounded read of the file range)
- `src/superclaude/cli/sweep/commands.py`: `sweep_group` (:215), `run` (:242), `_check_run_ids` (:87), `_check_output`, `_publish`; in `run`, `if not runs:` calls `probes.bind_run(budget)` at :264-266 and `SweepContext(now, span, now - span, checkout, runs)` is built at :267.
- `src/superclaude/cli/sweep/probes.py`: `bind_run` (:397) raises `BindingError("no Run bound: pass --run <id>")` for no binding and a second message when Orca is unavailable; `ALLOWED_ORCA` (:49) pins ten call templates and has no `run-list`.
- `src/superclaude/cli/sweep/models.py`: `SweepContext` frozen dataclass (:75) with fields `now, window, window_start, root, runs`.
- `src/superclaude/cli/sweep/report.py`: `_header` (:182) builds the header lines from `ctx`; `render` (:608), `to_json` (:613).
- `src/superclaude/cli/sweep/__init__.py`: lazy `__getattr__` loads `commands` only when `sweep_group` is read; `src/superclaude/cli/main.py:585-587` imports it and calls `main.add_command(sweep_group, name="sweep")`.
- `src/superclaude/cli/install_hooks.py`: `_FRESHNESS_SCRIPTS` (:42-97) lists every script under `src/superclaude/hooks/scripts/`; `_copy_scripts` (:254) copies only the listed names; `_merge_settings` (:301) registers hooks from `src/superclaude/hooks/hooks.json`.
- `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` is the pattern for a hook script; its test `tests/cli/test_install_hooks.py:854` asserts it is listed, executable and byte-equal to `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh`.
- `src/superclaude/cli/issue_watch/launch.py`: `find_orca(runner, which, timeout)` (:212) needs an `issue_watch` Runner and runs `orca skills list --json`; not reused (decision in Task 2).
- Command file is `src/superclaude/commands/sweep.md` (not under `commands/sc/`); skill is `src/superclaude/skills/sc-sweep-protocol/SKILL.md`.

## Dependents
- `SweepContext` is constructed in `src/superclaude/cli/sweep/commands.py` and in `tests/sweep/test_classify.py`, `tests/sweep/test_probes_allowlist.py`, `tests/sweep/test_readonly.py`, `tests/sweep/test_report.py` (one call each); it is read by `classify.py`, `probes.py`, `report.py`. A new field with a default keeps all five calls valid.
- `sweep_group` is used by `src/superclaude/cli/main.py:585-587`, `tests/sweep/test_cli_contract.py`, `tests/sweep/test_cli_registration.py` (asserts `commands` is not imported until `sweep_group` is read, and `run` is in `sweep --help`), `tests/sweep/test_readonly.py`.
- `tests/sweep/conftest.py` has an autouse fixture that fails any test that starts a process; tests that need `bash` (the hook tests) therefore live outside `tests/sweep/`.
- `bind_run` callers: `commands.run`, `tests/sweep/test_probes_allowlist.py:831` and `:886`.
- `_FRESHNESS_SCRIPTS` consumers: `_copy_scripts`, `Makefile` verify-sync (lines 308-325: every `src/superclaude/hooks/scripts/*.sh` must be a member, and no stale member), `tests/cli/test_install_hooks.py` per-script tests, `src/superclaude/cli/doctor.py` and `install_user_setup.py` through `install_hooks`.
- Skill text is pinned: `tests/commands/test_sweep_command.py:497` requires the phrase "adds no flag, reads no environment variable and has no worker mode" to stay in the skill.

## Pre-check
Run after the plan passed the gate (2026-11-26, advisory, read-only; no plan edit).
- Files the tasks name that exist: `src/superclaude/cli/sweep/{commands,models,report,probes,__init__}.py`, `src/superclaude/cli/install_hooks.py`, `src/superclaude/hooks/scripts/`, `plugins/superclaude/hooks/scripts/`, `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `tests/sweep/{conftest,test_cli_contract,test_cli_registration,test_readonly,test_probes_allowlist,test_report}.py`, `tests/cli/test_install_hooks.py`, `tests/commands/test_sweep_command.py`, `docs/user-guide/`, `Makefile` (verify-sync). Files the tasks create (do not exist yet): `src/superclaude/cli/sweep/ledger.py`, `tests/run_ledger/*`, `src/superclaude/hooks/scripts/run-ledger-record.sh`, its plugin mirror, `docs/user-guide/run-ledger.md`, `.dev/issues/895/result.md`.
- Symbols that resolve: `sweep_group`, `run`, `_check_run_ids`, `probes.bind_run`, `probes.BindingError`, `probes.RUN_ID_RE` (used at commands.py:90), `SweepContext`, `_header`, `_FRESHNESS_SCRIPTS`, `_copy_scripts`.
- Corrected during planning: the command file is `src/superclaude/commands/sweep.md` (the brief said `commands/sc/sweep.md`); there is no plugin mirror of the sweep command or skill, so Task 7 needs only `make sync-dev`.
- Dependents no task names (advisory): `docs/user-guide/cli-groups.md` and `docs/user-guide/orchestrator-mode.md` mention `superclaude sweep`; they are not changed by the plan and can be synced by `/sc:post-release`. Count: 2 unnamed dependents, 0 missing files, 0 unresolved symbols.

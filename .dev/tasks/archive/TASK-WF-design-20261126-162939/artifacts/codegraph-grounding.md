# Codegraph grounding (TASK-WF-design-20261126-162939)

## Run state

- index_state: fresh (`codegraph_status`: 3773 files, changes since index 0 added, 0 modified, 0 removed)
- access: mcp (lookup tools listed: `codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files`)
- checked_at: 2026-11-26T16:32:04Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-326
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-326
- tokens: none for the readiness check. Most files this plan changes are Markdown and JSON fixtures, which codegraph does not index, so their lookups used Grep, Glob and Read (the permanent floor, normal evidence). The only existing Python symbols involved are read-only references.

## Resolved symbols

| Named by the source | Where it resolved | How |
|---|---|---|
| `archive_workspace.py` line regexes `_START`, `_VERDICT`, `_RULING`, `_RETRY`, `_HALT`, `_PLAN`, `_FINAL` and functions `_parse_ledger`, `validate`, `archive`, `print_state`, `main` | `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py:44-67`, `:181`, `:278`, `:477`, `:557`, `:579` | codegraph file outline (`symbolsOnly`), then Read of the regex block when a task copies it |
| `_remove_branch` (the only local branch deletion; stays unchanged) | `scripts/worktree_cleanup.py:2636` | codegraph search |
| implement Wave 0 steps 5, 6, 9 and the Q0..Q8 loop | `src/superclaude/skills/sc-implement-protocol/SKILL.md:71`, `:72`, `:75`, `:121-150` | Read |
| STOP table and the closed-code sentence | `SKILL.md:30-51` | Read |
| managed archive gate | `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:50-56` | Read |
| `/sc:git` routing row | `src/superclaude/core/HOW-WE-WORK.md:293` | Grep |
| K3 sentence | `src/superclaude/core/WORKER-CONTRACT.md:42` | Grep |
| `commands/sc-git.md`, plugin copy, source copy of `git.md` | `commands/sc-git.md`, `plugins/superclaude/commands/git.md`, `src/superclaude/commands/git.md` | Glob |
| no plugin copy of `WORKER-CONTRACT.md` | none found under `plugins/superclaude/**` | Glob |

## Dependents

Dependents of the Markdown anchors the plan edits (found with Grep and Read, no graph rows):

| Edited anchor | Dependents that must keep working or be updated |
|---|---|
| implement `SKILL.md` STOP table and the sentence starting "No other `E-*` codes" | `tests/skills/test_task_workspace_lifecycle.py:778-791` reads every `| E-... |` row, requires the `E-RESUME-NEEDED` row to end with `| Nothing written |` and mention `refs/retry.md`, and requires the "No other `E-*` codes" sentence to contain `E-RESUME-NEEDED` |
| `src/superclaude/commands/implement.md` (option row, `argument-hint`, Will Not line 100) | `tests/commands/test_workflow_command.py` (the plugin must ship the implement protocol with the same file set), `tests/commands/test_routing_plugin_parity.py:41` (byte parity of `implement.md` with `plugins/`); no test pins the Will Not text (Grep found none) |
| `src/superclaude/core/HOW-WE-WORK.md:293` (`/sc:git` row) | `tests/recommend/test_routing_refresh.py` and `tests/recommend/fixtures/routing_refresh_cases.json` (case S23), `tests/core/test_how_we_work_routing_table.py`, byte copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` |
| `src/superclaude/core/WORKER-CONTRACT.md:42` (K3 sentence) | `tests/skills/test_worker_contract.py` (classification tables); no test pins the K3 wording (Grep found none) |
| `src/superclaude/commands/README.md:9` (the four mirrored commands) | `tests/commands/test_routing_plugin_parity.py:41` |
| `commands/sc-git.md` (deleted) | `tests/docs/test_retired_docs_absent.py:10` (`_RETIRED`), nothing else references it |
| `docs/user-guide/commands.md:98`, `:1258-1273`; `docs/user-guide/flags.md:136-140` | user documentation only |
| implement `refs/ledger.md` lines 127, 139, Row 1; `refs/retry.md:41`, `:212`, `:504`; `refs/qa.md:254` | the commit-step tests listed in the plan; the existing `tests/skills/test_implement_*.py` files (retry_citation, adviser_family, launch_alias, retry_revert, saved_prompt_rule, severity_static, severity_replay) must stay green |

## Pre-check

Run after the plan passed the gate (advisory; it never edits the plan or changes its status). One bounded read-only batch of 73 checks (Grep, Glob, Read and `sed`/`grep` on fixed patterns; no new readiness check):

- Files the plan changes or reads: all 32 named existing files exist (commands, core, implement protocol and its refs and `archive_workspace.py`, the launch-level guard, `scripts/worktree_cleanup.py`, the legacy `commands/sc-git.md`, the plugin copies, eleven test files and fixtures, two user-guide pages, `Makefile`, the plugin build script).
- Files the plan creates: `src/superclaude/skills/sc-git-protocol/`, `tests/vcs/` and `refs/commit-step.md` do not exist yet, as planned.
- Line anchors the tasks cite all hold: implement `SKILL.md` lines 51, 57, 72, 124, 129, 150; `implement.md` lines 7 and 100; `README.md:9`; `refs/ledger.md` 127, 139, 239; `refs/retry.md` 41 and 504; `refs/qa.md:254`; `refs/managed-workspace.md:52`; `WORKER-CONTRACT.md` 23 and 42; `HOW-WE-WORK.md:293`; `worktrees.md:45`; `test_worker_contract.py` 474, 1894, 1899, 1927, 2946; `test_retired_docs_absent.py:10`; `test_routing_plugin_parity.py:41`; `test_task_workspace_lifecycle.py:790`; `test_workflow_archive.py` 22 and 1033; user guide `commands.md` 98 and 1258 and `flags.md:136`; `scripts/worktree_cleanup.py:2636`; `scripts/build_superclaude_plugin.py:16`.
- Symbols: all seven line regexes (`_START`, `_VERDICT`, `_RULING`, `_RETRY`, `_HALT`, `_PLAN`, `_FINAL`) exist in `archive_workspace.py`; `git_in` exists in `tests/worktree_cleanup/conftest.py`.
- Baseline facts: `git ls-files commands/` lists 21 files (20 after the planned deletion, AC-04); `archive_workspace.py`, `scripts/worktree_cleanup.py`, `worktrees.md` and the launch-level guard are identical to `origin/integration`; `plugins/superclaude/commands/git.md` is byte-identical to `src/superclaude/commands/git.md`.
- Dependents of the touched anchors that no task names: none found. Every test that reads a touched anchor appears in a task's acceptance criteria (`test_task_workspace_lifecycle.py` in Tasks 26 and 30, `test_worker_contract.py` in Tasks 19 to 23 and 26 to 36, `test_routing_refresh.py` in Tasks 19 and 35, `test_routing_plugin_parity.py` in Task 25, `test_retired_docs_absent.py` in Task 25, `test_workflow_archive.py` in Task 32, `test_workflow_command.py` in Tasks 26 and 38, `test_how_we_work_routing_table.py` in Task 35).
- Tokens: none. An empty graph answer was never used as proof of absence; absences were checked by Glob and file tests.

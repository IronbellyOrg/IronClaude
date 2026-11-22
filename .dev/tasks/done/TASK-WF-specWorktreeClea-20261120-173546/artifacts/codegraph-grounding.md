# Codegraph grounding: TASK-WF-specWorktreeClea-20261120-173546

## Run state

- index_state: fresh
- checked_at: 2026-11-20T17:38:06Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-687
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-687
- access: mcp (`codegraph_status` and the lookup tools are listed)
- status answer: 3518 files, 0 added, 0 modified, 0 removed since the index
- degraded tokens: graph:empty (the work is a new script, a new command and new tests, so almost every symbol the plan names does not exist yet; shell and markdown files are not symbol-indexed, so the files named below were read with Read and Grep)

## Resolved symbols

| Name the source or plan relies on | Result | How resolved |
|---|---|---|
| `scripts/worktree_cleanup.py`, `src/superclaude/commands/worktrees.md`, `scripts/worktree_cleanup_orca_automation.md`, `tests/worktree_cleanup/` | do not exist yet (new files, as spec section 5 says) | Glob and Grep |
| `src/superclaude/skills/sc-closeout-protocol/scripts/branch-landed.sh` | exists; one argument (a PR number, `#N` or a URL), one stdout line `MERGED|OPEN|CLOSED|NONE|UNKNOWN`, exit 0 only for MERGED, 1 OPEN, 2 UNKNOWN, 3 NONE, 4 CLOSED; reads `origin` of the current directory; needs `jq`; runs one `git fetch` of the base branch and `refs/pull/<N>/head` | Read, whole file |
| `scripts/merged_pr_log_orca_automation.md` | exists; fields Name, Trigger (UTC), Status, "Command to run (precheck shape)", environment names, human steps, "When a run fails" | Read, whole file |
| `scripts/merged_pr_log.py` | exists; stdlib script with `parse_args` and `main`; tests load it with `importlib.util.spec_from_file_location` | codegraph_search, Grep |
| `tests/merged_pr_log/` | exists: `__init__.py`, `fixtures/`, `test_merged_pr_log.py` | Glob |
| `_POST_REFRESH_ADDITIONS` | `tests/recommend/test_routing_refresh.py:36`, now `{"closeout", "graph", "impact", "issue", "sweep"}`; line 660 compares shipped commands minus this set | codegraph_search, Read |
| `_OTHER_COMMANDS` | `tests/core/test_how_we_work_routing_table.py:27`; line 287 requires the "other commands" table members to equal it | Read |
| `NEVER_AS_WORKER` | `tests/skills/test_worker_contract.py:474`; the pinned sentence is at line 89; `_check_no_unattended_sections` (line 830) requires only the named commands to have `## Unattended mode` | Read |
| `check_allowed` (Jay's runner) | not in this repo; the spec asks for the same idea in the new script | codegraph_search (no match for the name; only an unrelated class came back) |

## Dependents

Files that name `/sc:closeout`, the nearest registered command with the same shape (a person-run command that writes outside the checkout), so each is a place the new command's name must be added or consciously left out:

| File | What it holds | Plan task |
|---|---|---|
| `tests/recommend/test_routing_refresh.py` (line 36) | `_POST_REFRESH_ADDITIONS` set | Task 15 |
| `src/superclaude/core/HOW-WE-WORK.md` (other-commands table, about line 292) | one row per command | Task 15 |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | byte copy of the guide | Task 15 |
| `tests/core/test_how_we_work_routing_table.py` (line 27) | `_OTHER_COMMANDS` set | Task 15 |
| `src/superclaude/core/WORKER-CONTRACT.md` (line 23, and line 290 to read) | never-as-worker sentence | Task 16 |
| `tests/skills/test_worker_contract.py` (lines 89, 474) | the pinned sentence and the tuple | Task 16 |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (line 982; line 790 is the "worker eligibility decided" checklist item that makes the never-as-worker decision necessary) | copy of the never-as-worker sentence | Task 16 |
| `docs/user-guide/commands.md` (summary table near line 103, section near line 373) | user-facing command docs | Task 17 |
| `CHANGELOG.md` (`## [Unreleased]`) | one entry per change | Task 17 |
| `tests/commands/test_closeout_command.py` | static test of a command file (pattern for the new command test) | Task 14 |
| `src/superclaude/commands/sweep.md` (line 18) | the sentence a never-as-worker command carries in its own file | Task 14 |
| `NOTICE` (line 30, component 2) | Apache-2.0 component list | Task 19 |
| `src/superclaude/cli/install_commands.py` (line 42) | installs every `commands/*.md` by glob, so no list to edit | none |

`src/superclaude/commands/help.md` does not name `closeout` or `sweep`, so it needs no row. `tests/skills/test_closeout_protocol.py:3589` reads the never-as-worker sentence by the text "never-as-worker list" and `/sc:agent`; it is unaffected by adding a command at the end of the list (to be confirmed by running it in Task 16).

## Pre-check

Run after the plan was written, read-only (codegraph fresh at 2026-11-20T17:38:06Z; no second readiness check).

- Files the tasks edit that exist today: 12 of 12 confirmed by Read or Grep (`tests/recommend/test_routing_refresh.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/skills/test_worker_contract.py`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `src/superclaude/core/WORKER-CONTRACT.md`, the developer guide, `docs/user-guide/commands.md`, `CHANGELOG.md`, `NOTICE`, `src/superclaude/commands/closeout.md` and `scripts/merged_pr_log_orca_automation.md` as models).
- Files the tasks create that must not exist yet: 7 of 7 absent (`scripts/worktree_cleanup.py`, `scripts/worktree_cleanup_orca_automation.md`, `scripts/worktree_cleanup_PROVENANCE.md`, `src/superclaude/commands/worktrees.md`, `tests/worktree_cleanup/`, `tests/commands/test_worktrees_command.py`, `.dev/research/worktree-cleanup-proofs.md`).
- Symbols: `_POST_REFRESH_ADDITIONS` resolves (codegraph_search, `tests/recommend/test_routing_refresh.py:36`); `NEVER_AS_WORKER` and `_OTHER_COMMANDS` resolved by Read; `check_allowed` does not exist in this repo (it is the idea from Jay's `retire.py`, named in the plan as new code).
- Dependents of touched symbols that no task names: none found. Not edited on purpose: `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (a frozen research reference whose lines cite the never-as-worker list but do not enumerate it) and `docs/designs/orchestrator-mode.md` (a design record).
- Count: 20 tasks, 8 phases; 0 unnamed dependents; graph token: graph:empty (new code).

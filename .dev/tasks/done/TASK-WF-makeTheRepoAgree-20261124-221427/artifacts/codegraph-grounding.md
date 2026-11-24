# Codegraph grounding

## Run state

- index_state: unavailable (the codegraph MCP tools were not listed in this session; `codegraph_status` returned "No such tool")
- token: graph:unavailable
- access mode: Grep, Glob and Read floor (normal evidence)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/fix-default-branch-integration

## Resolved symbols

- `L2_PROTECTED` array: `src/superclaude/hooks/scripts/launch-level-pre-push.sh:17` (mirror `plugins/superclaude/hooks/scripts/launch-level-pre-push.sh:17`)
- `_DEFAULT_BASE_BRANCH`: `src/superclaude/cli/reflect/config.py:44`, sole reader `resolve_config` default at line 259, used by `_resolve_base` (line 81)
- `L2_VERSION_LINE`: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:877`; test pins `tests/cli/test_install_hooks.py:1100-1101`

## Dependents

- Hook byte pins: `tests/cli/test_install_hooks.py` (mirror equality, version line, sha256), `tests/hooks/test_launch_level_pre_push.py::test_t23_hook_sha256_pinned_with_version_line`
- Installer self-test: `orca_worktree.py` line 1363 loop; tests `tests/skills/test_issue_l2_install.py`, `tests/skills/test_issue_orca_worktree.py`
- Hook behaviour tests: `tests/hooks/test_launch_level_pre_push.py` (`BRANCHES` line 49), `tests/hooks/test_launch_level_pre_push_records.py`
- Not changed (separate layer): `src/superclaude/hooks/scripts/launch-level-guard.sh` lines 59 and 736; `tests/hooks/test_launch_job_identity.py:1203`
- Reflect default: tests mock `_git` (`tests/cli/reflect/test_cli_smoke.py`, `test_base_precedence.py`) and do not read the default value

## Pre-check

- Files named by Tasks 1-5 exist, except the new `tests/core/test_default_branch_agreement.py` (created by Task 5). Symbols resolve. Dependents above are named in the tasks. No unnamed dependent found by Grep. Tool: Grep/Read floor (graph:unavailable).

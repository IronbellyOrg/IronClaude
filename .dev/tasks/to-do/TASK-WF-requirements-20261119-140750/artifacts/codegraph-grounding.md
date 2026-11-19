# Codegraph grounding: TASK-WF-requirements-20261119-140750

## Run state

- index_state: fresh (codegraph_status: 3846 files, 58424 nodes, 0 added, 0 modified, 0 removed since the last index; latest file indexed 2026-11-19T02:30:47Z)
- checked_at: 2026-11-19T14:08Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
- projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
- access mode: MCP tools (`codegraph_status` called once for this run)
- graph tokens: none. Symbol and line citations below were confirmed with Grep and Read (the floor); no graph row is cited unread.

## Resolved symbols

Confirmed by Grep in this run:

- `src/superclaude/hooks/scripts/launch-level-guard.sh`: line 10 version stamp (value 1); line 70 `LL-SUBMIT)` message; line 444 coordinator-only TAMPER case (names `release-worker`, `adopt-`, `record-`, `issue_pipeline*release*`, `issue_pipeline*approval_record*`); line 653 SUBMIT row that holds `issue create`, `issue edit`, `issue comment`; line 764 tamper tokens (`.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git`; no `.config/superclaude`); line 786 `for LL_C in` class list (no ISSUE class).
- `plugins/superclaude/hooks/scripts/launch-level-guard.sh` line 10 (the tracked mirror, version 1).
- `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:839` `GUARD_VERSION_LINE`; test pins `tests/hooks/test_launch_level_guard.py:251`, `tests/skills/test_issue_orca_worktree.py:1283` and `:1914-1916`.
- `tests/hooks/test_launch_level_guard.py` lines 2743-2745 and 2875-2876 hold the three `gh issue` rows.
- `src/superclaude/cli/issue_watch/audit.py:26` `REASON_TABLE`; rows `edited_after_approval` (71) and `project_mismatch` (72).
- `src/superclaude/cli/issue_watch/cycle.py:58` `_TOP_KEYS`; `predicates.py:185` `approval_of`, `:258` `edited_after_approval`, `:262` `project_check`.
- `tests/hooks/test_launch_level_observations.py:79` `_PENDING` (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX), skipped at line 84.

Carried from the plan v3 grounding and the remediation proposal, not re-read in this run: cycle.py lines 880-892, 915, 958, 979, 998, 1007-1016, 1026-1058; launch.py lines 33, 84-102, 119, 233-249; github.py lines 37, 74-103, 187-259, 764-775; predicates.py lines 111-118, 216-233, 249-258; `src/superclaude/core/WORKER-CONTRACT.md` lines 23, 241-245, 291-300; test_security_invariants.py lines 5-10, 67, 911-919; record.py line 545-547.

## Dependents

- `project_check`: callers `cycle.py` `_examine` and `_revalidate`; test files `tests/issue_watch/test_predicates.py`, `test_cycle.py`, `conftest.py`.
- `ProjectItem`: constructors in `tests/issue_watch/` and `src/superclaude/cli/issue_pipeline/reads.py` (a dependent of `issue_watch/github.py`).
- `build_claim_prompt` and `PROMPT_PATTERN`: `launch.py`, `cycle.py` (`_launch`, `status_report`), seven test files under `tests/issue_watch` that hold `--pipeline none`.
- `approval_of`: call sites `cycle.py` `_approve` and `_revalidate`.
- Guard stamp: guard, plugin mirror, `orca_worktree.py`, three test pins.

## Pre-check

Advisory, test -e floor: all 71 source, test, doc and fixture files that the 28 tasks name exist (no MISSING). Symbols and lines confirmed by Grep are listed under Resolved symbols; the lines marked carried were not re-read. No dependent with no task was found beyond those listed. Gate: 28 tasks, 8 phases, contiguous numbers, every dependency names a lower task, every task has acceptance criteria, no checkbox or numbered lines, `source.md` identical to the requirements file (cmp).

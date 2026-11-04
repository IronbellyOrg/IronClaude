# Reviewer 3 brief: persona refactorer (model class opus)

Mode: UC-1 pre-execution review of a proposed plan. Working tree: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357 (read-only for you).
Spec: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/source.md
Tasklist under review: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md
Lens: structure, design and risk. Judge whether the hook design in Task 1 (bash + jq tokenizer, wrapper and keyword skipping, heredoc handling, fail-open, exit codes) is sound and simple enough, whether it will produce false positives or false negatives on common agent commands, whether the registration and installer changes fit existing patterns, and whether Task 7's live check is feasible and safe for the live ~/.claude. Assume mistakes exist.

## T1 card excerpt

- T1-R1 (Task 7 environment dependency): relies on `claude -p` auth and on `--settings` hooks merging with user hooks; Task 7 records a blocked status instead of passing if unavailable. Residual risk: the subagent proof may need a different prompt shape if the model refuses to spawn an Agent in -p mode.
- T1-R2 (Task 2 timing case): a hard under-1-second assertion on a 100 KB command can be flaky on a loaded CI runner.
- T1-R3 (blast radius after install): the hook runs on every Bash call in every workspace after `superclaude install`; a false positive blocks legitimate work. Mitigated by fail-open rules and the allowed-case table in Task 2; not mitigated for the heredoc ceiling.
- T1-R4 (live ~/.claude safety): Constraints and Task 4/Task 7 keep installs to temp targets; Task 7 acceptance compares before/after state of ~/.claude.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T13:08:56Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357 projectPath=/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357

### src/superclaude/hooks/scripts/freshness-pre-edit.sh:1-32
Model hook header, `set -u`, stdin via jq, fail-open.

### src/superclaude/hooks/scripts/freshness-pre-edit.sh:122-141
Block: stderr + exit 2.

### src/superclaude/cli/install_hooks.py:42-82 and :218-257
Script list and copy loop (chmod 0o755 after copy).

### src/superclaude/cli/install_hooks.py:348-443
Merge loop: framework ownership by exact command string; append when not owned.

### Makefile:137-146 and :254-325
sync-dev copies src/superclaude/hooks/scripts/*.sh|*.js to .claude/hooks; verify-sync checks mirror equality and installer registration.

### plugins/superclaude/hooks/hooks.json
Already differs from src/superclaude/hooks/hooks.json (no ccsession entries, no pragmatic-subagent, narrower auggie matcher). The plan adds only the new registration there.

### Claude Code hooks documentation (code.claude.com/docs/en/hooks, fetched 2026-11-04)
PreToolUse exit 2 blocks and returns stderr to Claude. Hooks run inside subagents. Hook entries merge across settings levels; identical handlers run once.

## Coverage slice

| Requirement | Task | Status |
|---|---|---|
| INF-001 PreToolUse Bash block | Task 1, Task 3 | covered semantically |
| INF-007 / INF-008 registration and scripts in src and plugins | Task 1, Task 3 | covered |
| INF-009 install_hooks.py | Task 3, Task 4 | covered |
| INF-010 freshness-pre-edit as model | Task 1 | covered semantically |

Return findings as a list: id, severity (blocking or minor: blocking = wrong behaviour, false claim, missing required deliverable, security or data-loss risk; minor = wording, style, nit), task number, tasklist line, evidence (file:line you Read), and the concrete fix. If nothing blocking, include a short self-audit. Do not write any file.

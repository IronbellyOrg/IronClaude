# Reviewer 1 brief: persona analyzer (model class sonnet)

Mode: UC-1 pre-execution review of a proposed plan. Working tree: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357 (read-only for you).
Spec: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/source.md (one-line prompt pointing at issue #357; the issue's Done-when list is quoted verbatim in the tasklist Constraints, first bullet).
Tasklist under review: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md
Lens: root cause and deviation. Find requirements the plan gets wrong, contradictions between tasks, wrong assumptions about the code, and any task whose acceptance criteria cannot be met as written. Assume mistakes exist.

## T1 card excerpt

- T1-F1 (Task 5 vs issue Done-when): Done-when says "`read-parse.md:8` uses `uv run python`"; Task 5 prescribes `uv run --no-project python`. The tasklist justifies it with two in-repo precedents. Classification: refinement of a requirement, not drift; a reviewer may still read it as a literal mismatch.
- T1-F2 (Task 6 CHANGELOG): not named in source.md or issue #357. Repo convention (CHANGELOG.md `## [Unreleased]` sections per PR) motivates it. Classification: scope addition (authorized-expansion candidate only if the owner accepts convention as authority; otherwise drift).
- T1-F3 (Task 1 quoted command word): rule "text inside quotes is never a command word" means `"python3" x.py` is not blocked. Not documented as a known ceiling in Task 1. Minor.
- T1-F4 (Task 1 heredoc ceiling): heredoc body lines are scanned; a heredoc that writes prose with a line starting `python3` is blocked. Documented in Task 1. Minor false-positive risk.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T13:08:56Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357 projectPath=/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357

### src/superclaude/hooks/scripts/freshness-pre-edit.sh:17-32
Model hook: reads stdin JSON with jq, fails open (exit 0) when no file_path. Read the range yourself.

### src/superclaude/hooks/scripts/freshness-pre-edit.sh:122-141
Block path: stderr message then `exit 2`; allow path `exit 0`.

### src/superclaude/cli/install_hooks.py:42-82
`_FRESHNESS_SCRIPTS`: the list `_copy_scripts` (:218-257) installs to ~/.claude/hooks/.

### src/superclaude/cli/install_hooks.py:265-463
`_merge_settings`: additive merge of hooks.json registrations into settings.json by command identity.

### src/superclaude/hooks/hooks.json
Current PreToolUse has one entry, matcher `Edit|Write`, command `~/.claude/hooks/freshness-pre-edit.sh`, timeout 1.

### src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md:8
`seekable=$(python3 -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)`

### Claude Code hooks documentation (code.claude.com/docs/en/hooks, fetched 2026-11-04)
PreToolUse exit 2 blocks the tool call and stderr is returned to Claude as the tool error. Hooks from settings files run inside subagents (input carries agent_id and agent_type). Bash command is at tool_input.command. Hook entries merge across settings levels.

## Coverage slice

| Requirement | Matched task (containment) | Status | Semantic note |
|---|---|---|---|
| INF-001 block bare python/python3/pip/pip3 with PreToolUse hook | none (0.58) | unmapped by rule | covered by Task 1 and Task 3 |
| INF-002 read the issue first | none (0.30) | unmapped by rule | process step; Constraints quote the issue |
| INF-010 freshness-pre-edit hook as the model | Task 3 (0.71) | covered | real coverage is Task 1 |
| INF-011 replace bare call in read-parse.md:8 | Task 5 (1.0) | covered | Task 5 uses uv run --no-project python |
| INF-012 Done-when list is the acceptance criteria | Task 1 (0.8) | covered | quoted in Constraints; mapped per bullet |

Return findings as a list: id, severity (blocking or minor, per definitions: blocking = wrong behaviour, false claim, missing required deliverable, security or data-loss risk; minor = wording, style, nit), task number, tasklist line, evidence (file:line you Read), and the concrete fix. If you find nothing blocking, include a short self-audit of what you checked. Do not write any file.

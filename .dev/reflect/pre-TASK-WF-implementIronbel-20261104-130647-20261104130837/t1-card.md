# Tier 1 reflection card (UC-1, pre-execution)

Spec: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/source.md
Tasklist: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md
Requirements context: issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), "Proposed fix" and "Done when", quoted verbatim in the tasklist Constraints (first bullet).

## Grounding (Wave 1A)

- Hook contract model: src/superclaude/hooks/scripts/freshness-pre-edit.sh:17-32 (stdin JSON via jq, fail-open exit 0) and :123-141 (block = stderr + exit 2, never exit 1).
- Registration model: src/superclaude/hooks/hooks.json PreToolUse `Edit|Write` entry; plugins/superclaude/hooks/hooks.json already drifts from src (ccsession, pragmatic-subagent, auggie matcher; `diff` observed in Wave 1A).
- Installer: src/superclaude/cli/install_hooks.py:42-82 `_FRESHNESS_SCRIPTS`; `_copy_scripts` :218-257 copies only listed names; `_merge_settings` :265-463 merges by command identity.
- verify-sync installer-registration check: Makefile:308-325 compares src/superclaude/hooks/scripts/*.sh|*.js against `_FRESHNESS_SCRIPTS`.
- Precedent tests: tests/cli/test_install_hooks.py:699-726 (codegraph hook registration parametrized over src/plugins; packaged, listed and mirrored), tests/hooks/test_freshness_pre_edit_create_case.py:24-35 (subprocess runner).
- Bare call: src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md:8.
- `uv run --no-project python` precedent: src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:199, src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:53.
- Claude Code docs (code.claude.com/docs/en/hooks, fetched 2026-11-04): PreToolUse exit 2 blocks and stderr is returned to Claude; hooks from settings files run inside subagents and carry agent_id/agent_type; Bash command is at tool_input.command; hook entries merge across settings levels. The docs do not explicitly state that `--settings <file>` hooks merge with user hooks [INFERRED: likely, since --settings is another settings source].

## Coverage (Wave 1B)

See artifacts/coverage-matrix.yaml (requirements-analyst, two-pass). Spec carries no labeled IDs, so every row is Pass-2 inferred; coverage_degraded is expected to be parsed-sparse.

## Deviation and risk findings (analyzer slice)

- T1-F1 (Task 5 vs issue Done-when): Done-when says "`read-parse.md:8` uses `uv run python`"; Task 5 prescribes `uv run --no-project python`. The tasklist justifies it with the two in-repo precedents above. Classification: refinement of a requirement, not drift; a reviewer may still read it as a literal mismatch.
- T1-F2 (Task 6 CHANGELOG): not named in source.md or issue #357. Repo convention (CHANGELOG.md `## [Unreleased]` sections per PR) motivates it. Classification: scope addition (authorized-expansion candidate only if the owner accepts convention as authority; otherwise drift).
- T1-F3 (Task 1 quoted command word): rule "text inside quotes is never a command word" means `"python3" x.py` is not blocked. Not documented as a known ceiling in Task 1 (heredoc ceiling is). Minor.
- T1-F4 (Task 1 heredoc ceiling): heredoc body lines are scanned; a heredoc that writes prose with a line starting `python3` is blocked. Documented in Task 1. Minor false-positive risk.

## Risk surface (refactorer / structural slice)

- T1-R1 (Task 7 environment dependency): relies on `claude -p` auth and on `--settings` hooks merging with user hooks; Task 7 records a blocked status instead of passing if unavailable. Residual risk: the subagent proof may need a different prompt shape if the model refuses to spawn an Agent in -p mode.
- T1-R2 (Task 2 timing case): a hard under-1-second assertion on a 100 KB command can be flaky on a loaded CI runner.
- T1-R3 (blast radius after install): the hook runs on every Bash call in every workspace after `superclaude install`; a false positive blocks legitimate work. Mitigated by fail-open rules and the allowed-case table in Task 2; not mitigated for the heredoc ceiling.
- T1-R4 (live ~/.claude safety): Constraints and Task 4/Task 7 keep installs to temp targets; Task 7 acceptance compares before/after state of ~/.claude.

## Coverage / acceptance slice (qa)

- Issue Done-when bullet 1 (block + message naming uv run python and jq): Task 1, Task 2.
- Bullet 2 (allow uv forms; text-only mentions not blocked): Task 1 rules, Task 2 allowed table.
- Bullet 3 (tests incl. &&, ; and |): Task 2 second acceptance criterion.
- Bullet 4 (install registers; fires for subagents): Task 3, Task 4 (install), Task 7 (subagent).
- Bullet 5 (read-parse.md:8): Task 5.
- Bullet 6 (fresh session blocked and pointed to uv run python or jq): Task 7.

## Self-reported confidence

0.86 (self-report; not used for routing, the calibrator score is).

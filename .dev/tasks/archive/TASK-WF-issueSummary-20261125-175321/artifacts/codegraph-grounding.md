# Codegraph grounding: TASK-WF-issueSummary-20261125-175321

## Run state

- index_state: stale (token `graph:stale`)
- checked_at: 2026-11-25T17:53:41Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-834
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-834
- access: cli status only (the MCP status tool was not listed); lookup tools `codegraph_search` and `codegraph_node` were listed but not used
- CLI version 1.6.2 matches the pin
- Why stale and not fresh: CLI `status` printed "Index is up to date" but also warned that the last index run never finished (index truncated) and that 200,286 references from an interrupted run await resolution. Caller and impact edges are therefore incomplete, so every lookup used the floor (Glob, Grep, Read).
- Later in the run the codegraph MCP server disconnected; no graph lookup was needed.

## Resolved symbols

All resolved with Read, Grep and Bash `grep -n` against the checkout (base `a6fec2448`):

- `src/superclaude/skills/sc-issue-protocol/refs/create.md` lines 57, 69, 82-84 (heading "Contradiction prompt rule (default D14)"), 97
- `src/superclaude/skills/sc-issue-protocol/SKILL.md` lines 4, 29, 76, 102, 103
- `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` lines 1-15
- `src/superclaude/agents/issue-worker-t1.md`, `issue-worker-t2.md`, `issue-worker-t3.md` line 24
- `src/superclaude/commands/issue.md` lines 19, 85
- `docs/designs/sc-issue-command.md` lines 223, 225, 381, 460; `docs/user-guide/commands.md` line 357
- `tests/skills/test_issue_protocol.py`: `ALLOWED_TOOLS` line 40, `plan_section_problems` line 744, `_mutated_template` line 778
- `tests/skills/test_issue_worker_agents.py`: `PLAN_SECTIONS_RULE` line 34
- `tests/skills/test_worker_contract.py`: `WRITE_VERB_CLASSIFICATION` line 1971, key for SKILL.md create step 6 at line 3060, `test_classification_table_has_no_stale_entries` line 3171
- `tests/commands/test_issue_command.py`: `_text` line 42, `test_no_source_tree_path` line 264, `test_rule_10_line_is_carried_verbatim` line 269

## Dependents

Found by Grep (not by graph; an empty graph answer would not have meant "none"):

- `draft-notes` is named in: `docs/designs/sc-issue-command.md`, the three worker files, `src/superclaude/commands/issue.md`, SKILL.md, `refs/create.md`, `refs/tiers.md` (tier-fallback note only, unrelated to the trigger) and `tests/skills/test_issue_worker_agents.py` (file-name lists only).
- The old trigger text ("lists new material", "keep all", "new material or a contradiction") appears only in: `refs/create.md` (69, 84), SKILL.md (76, 102), `docs/designs/sc-issue-command.md` (225, 460). No test pins it today.
- Exact-line pins: `tests/skills/test_worker_contract.py:3060` pins SKILL.md create step 6 (line 103) verbatim, so Task 4 updates that key with the line. `refs/create.md` lines for the GitHub-write rule, the lookup paragraph and Wave 5 step 6 are also pinned there and must not change.
- `PLAN_SECTIONS_RULE` is imported by `tests/skills/test_issue_protocol.py` and checked in each worker file; it sits in `refs/create.md` line 63 and each worker's line 24.
- No `plugins/superclaude/` copy of the skill exists (Glob found none). The project mirrors are gitignored and come from `make sync-dev`.

## Pre-check

- Files named by tasks: 15 of 15 exist.
- Symbols and line anchors named by tasks: all resolve at the lines cited (SKILL.md 103 is the create step 6 post line; design doc 223/225/460 and user guide 357 match).
- Dependents of the touched text that no task names: 1 (`refs/tiers.md:42`, checked, unaffected). No gap.

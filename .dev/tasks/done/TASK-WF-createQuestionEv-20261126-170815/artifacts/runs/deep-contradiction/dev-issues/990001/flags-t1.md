# Flags decision

- Decided by: issue-worker-t1
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | bug | The description reports a crash of `/sc:issue --create` on an empty description, which is broken behaviour, not a new capability. Note: `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` does not exist (the directory holds only `clickup_claim.py`, `origin_repo.py`, `orca_worktree.py`; Glob `**/create_issue*` finds nothing), so the named crash site does not match the code. |
| Type | skill | The named path is under `src/superclaude/skills/sc-issue-protocol/`; the create flow is defined by markdown in `refs/create.md` (step at line 16 writes `<D>/description.md` from `templates/description.md`; line 22 covers an empty worker file) and no `create_issue.py` script exists, so the likely area is the skill protocol, not a CLI or script. |
| Issue type | Bug | derived from the mode and the area by the rule in `refs/labels.md` (table at lines 20-23: bug maps to Bug; only feature in tests maps to Test); `Bug` is listed in the repo issue types in `scout.md:17`. |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex); depth is deep. |

Codebase pass: followed `~/.claude/commands/sc/analyze.md` with Glob, Grep and Read only (no codegraph used). Grep for `create_issue` outside `.dev/` finds only the unrelated `mcp__github__create_issue` entries in `tests/hooks/test_launch_level_guard.py:3609`.

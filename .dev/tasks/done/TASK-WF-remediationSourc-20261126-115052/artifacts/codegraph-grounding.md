# Codegraph grounding

## Run state

- index_state: fresh (codegraph_status: 3752 files indexed, 0 added, 0 modified, 0 removed)
- checked_at: 2026-11-26T04:46:00Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-780
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-780
- access: MCP tools listed
- graph tokens: none. Codegraph held no symbol lookup for this plan: the one repository change is a Markdown paragraph (CLAUDE.md) and the other change is to Orca's own state outside the repository, so Grep and Read did the resolving. This is the regenerated run of the plan for the same source (Wave 4R regenerate route); the readiness check was repeated once for the new package.

## Resolved symbols

- CLAUDE.md: the Orca paragraph begins `**Orca:**` at line 54, inside the section `## ABSOLUTE RULE: PR Target = Fork`. The Git worktree rules start at the heading `### Parallel Development with Git Worktrees`, separate from that paragraph.
- Orca installed code (outside the repository, read only): `/opt/Orca/resources/app.asar.unpacked/out/cli/runtime-client.js` exports `RuntimeClient`; `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/repo.js` is the only CLI caller of `repo.update`.
- `.dev/troubleshoot/` is a fixed exclusion of the /sc:implement retry revert domain (`~/.claude/skills/sc-implement-protocol/refs/retry.md`, line 206), so a marker file kept there survives a retry of a task.
- `.markdownlint.json` at the repository root is the lint configuration; `.pre-commit-config.yaml` lines 90 and 91 run the hook `markdownlint` with `--fix` and do not exclude CLAUDE.md. `npx --yes markdownlint-cli@0.38.0 CLAUDE.md` (no `--fix`) exits 0 on the unedited file.
- `Makefile` line 166 defines `verify-sync` (reads src/superclaude and .claude only). In this checkout it exits non-zero on the unedited tree.

## Dependents

- tests/core/test_claude_md_worktree_rule.py reads CLAUDE.md and pins text only inside the section starting at `### Parallel Development with Git Worktrees`; the Orca paragraph is outside it. It must keep passing.
- tests/core/test_how_we_work_routing_table.py (line 340) reads the root CLAUDE.md and AGENTS.md among the files it scans; tests/core/test_claude_md_routing_block.py, tests/core/test_orca_session_launch_guidance.py and tests/core/test_research_routing_rule.py read the packaged copy src/superclaude/core/CLAUDE.md (they cannot detect anything about the root edit); tests/core/test_default_branch_agreement.py reads the root CLAUDE.md for another section. Six files together give 80 passed on the unedited tree.
- tests/sweep/fixtures/captured-worktree-current.json (line 14) and tests/sweep/fixtures/captured-worktree-list.json (line 15) hold the old project id as captured history. They do not read the live id and must not change.
- docs/memory/reflect/deviation-patterns-orca-default-worktree-paths.md (line 14) names the old id in a memo. Static text; no change.

## Pre-check

Advisory, read-only (no new readiness check; Grep, Glob and Read floor), run before the reflect call:

- Files the tasks name all exist: CLAUDE.md, the six test files of Task 3, the two sweep fixtures, `.markdownlint.json`, `Makefile`, the Orca rollback export `orca-data.json.sqlite-export.1.json` and the installed Orca client module `runtime-client.js`.
- CLAUDE.md line 54 begins `**Orca:**`, as Task 3 says.
- Dependents of the touched paragraph that no task names: none found. The only other text naming the old id is static (two sweep fixtures, one memory memo), and Constraints already marks the fixtures as must-not-change.
- Tools the tasks rely on: node v24.22.2 is available; ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING and ORCA_ENVIRONMENT are unset in this session (Task 1 records them again before any `orca` command). The once-only marker and the script do not exist yet, as Task 1 requires.
- Not checkable by the pre-check: that `RuntimeClient` accepts the `id:<uuid>` selector for `repo.update` and what it returns, and the field names printed by `orca worktree list --json`; Tasks 1 and 2 record the real results.
- Count: 4 tasks, 0 missing files, 0 unresolved symbols.

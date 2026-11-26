# Codegraph grounding

## Run state

- index_state: fresh (codegraph_status: 3746 files indexed, 0 added, 0 modified, 0 removed)
- checked_at: 2026-11-26T03:45:44Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-780
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-780
- access: MCP tools listed
- graph tokens: none. Codegraph held no symbol lookup for this plan: the one repository change is a Markdown paragraph (CLAUDE.md) and the other change is to Orca's own state outside the repository, so Grep and Read did the resolving.

## Resolved symbols

- CLAUDE.md: the Orca paragraph begins `**Orca:**` at line 54, inside the section `## ABSOLUTE RULE: PR Target = Fork` (heading at line 39). The Git worktree rules start at the heading `### Parallel Development with Git Worktrees`, separate from that paragraph.
- Orca installed code (outside the repository, read only): `/opt/Orca/resources/app.asar.unpacked/out/cli/runtime-client.js` exports `RuntimeClient` (line 3); `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/repo.js:32-35` is the only CLI caller of `repo.update`.

## Dependents

- tests/core/test_claude_md_worktree_rule.py reads CLAUDE.md and pins text only inside the section starting at `### Parallel Development with Git Worktrees` (line 10 of the test, `_section`); the Orca paragraph at line 54 is outside it. It must keep passing.
- tests/core/test_claude_md_routing_block.py, tests/core/test_orca_session_launch_guidance.py, tests/core/test_default_branch_agreement.py and tests/core/test_research_routing_rule.py also open CLAUDE.md or its sections; none quotes the Orca paragraph (Grep for `Orca identified this project`, `source of that id is unverified` and `superclaude_framework` found only CLAUDE.md:54).
- tests/sweep/fixtures/captured-worktree-current.json (line 14) and tests/sweep/fixtures/captured-worktree-list.json (line 15) hold the old project id as captured history. They do not read the live id and must not change.
- docs/memory/reflect/deviation-patterns-orca-default-worktree-paths.md (line 14) names the old id in a memo. Static text; no change.

## Pre-check

Advisory, read-only (no new readiness check; Grep, Glob and Read floor), run before the reflect call:

- Files the tasks name all exist: CLAUDE.md, the five test files of Task 3, the two sweep fixtures, the Orca rollback export `orca-data.json.sqlite-export.1.json` and the installed Orca client module `runtime-client.js`.
- CLAUDE.md line 54 begins `**Orca:**`, as Task 3 says.
- Dependents of the touched paragraph that no task names: none found. The only other text naming the old id is static (two sweep fixtures, one memory memo), and Constraints already marks the fixtures as must-not-change.
- Tools the tasks rely on: node v24.22.2 is available; ORCA_PAIRING_CODE, ORCA_REMOTE_PAIRING and ORCA_ENVIRONMENT are unset in this session (Task 1 records them again before the script runs).
- Not checkable by the pre-check: that `RuntimeClient` accepts the `id:<uuid>` selector for `repo.update` and what it returns; Task 2 records the real result.
- Count: 4 tasks, 0 missing files, 0 unresolved symbols.

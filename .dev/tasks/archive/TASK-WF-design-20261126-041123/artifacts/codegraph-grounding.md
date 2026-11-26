# Codegraph grounding: TASK-WF-design-20261126-041123

## Run state

- index_state: fresh
- checked_at: 2026-11-26T04:11:45Z (`codegraph_status` answer: "Changes since index: 0 added, 0 modified, 0 removed")
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-826
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-826
- access: mcp (lookup tools listed)
- switch: `SUPERCLAUDE_CODEGRAPH_PRIMITIVES` unset
- graph tokens: none for the status. The files this plan changes are Markdown (not indexed), JSON and new test files; symbol lookups apply only to the one existing test module used as a pattern. Everything else was found with Grep, Glob and Read (the permanent floor).

## Resolved symbols

- `tests/docs/test_branch_protection_rulesets.py` (`codegraph_node` with `symbolsOnly:true`): `_REPO` (line 8), `_RULESETS` (9), `_GUIDE` (10), `_ADMIN_PR_BYPASS` (13), `_BRANCH_FILES` (19), `_load` (25), `test_branch_rulesets` (30, parametrized), `test_tag_ruleset` (47), `test_no_default_branch_token_anywhere` (66), `test_guide_has_apply_and_check_commands` (71). No other indexed file depends on it. It is the pattern for the new docs test.
- `tests/skills/test_primitive_dual_surface_lookup.py` (Read): `_SKILLS` constant and `_lines(rel)` helper read `src/superclaude/skills/...` text. It is the pattern for the new skill test.
- Files without symbols (Markdown): `docs/developer-guide/release-procedure.md`, `src/superclaude/skills/sc-post-release-protocol/SKILL.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `src/superclaude/commands/impact.md`, `src/superclaude/commands/auggie-review.md`, `docs/user-guide/codegraph.md`, `docs/user-guide/commands.md`; JSON: `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json`.

## Dependents

Found with Grep (graph:empty for Markdown, so no codegraph answer; the floor is normal evidence):

- `docs/developer-guide/release-procedure.md`: no other file links to one of its Step anchors (grep over `*.md`, `*.py`, `*.yaml`, `*.json` outside `.dev/` finds only its own Contents list). No test reads the page today.
- `src/superclaude/skills/sc-post-release-protocol/SKILL.md`: `tests/skills/test_worker_contract.py:2371-2384` names the path in a conversion note (pins no Wave 1 text); `tests/unit/test_cli_install.py:216-218` lists the skill's files for install (the file list does not change).
- `src/superclaude/commands/impact.md` and `auggie-review.md`: tests that open them are `tests/commands/test_impact_command.py`, `tests/commands/test_auggie_review_revagent.py`, `tests/commands/test_auggie_review_remediation_chain.py` (none contains `origin/master`: `grep -rn "origin/master" tests` finds only fixture strings in `tests/hooks/test_launch_level_guard.py`). `tests/unit/test_cli_install.py:180` lists `sc-auggie-review-protocol/evals/evals.json` in the install file list (name unchanged).
- `docs/user-guide/commands.md:1335`: `--base` is the option `"--base"` / `base_override` of `superclaude reflect run` (`src/superclaude/cli/reflect/commands.py:307-315`, used at line 557); the example value is documentation only.
- No plugin mirror: `plugins/superclaude/` has no `post-release`, `impact` or `auggie-review` copy.

## Pre-check

Run on 2026-11-26 (Grep, Glob, Read; the changed files are Markdown or JSON, so the graph has no rows for them; recorded as graph:empty for those files, with no effect on the status):

- Files named by tasks that exist: 19 of 19 (release page, `CLAUDE.md`, `CONTRIBUTING.md`, the skill, the two command files, `evals.json`, two user-guide pages, the two pattern tests, `conflict-mechanical.md`, `reflect/commands.py`, three command tests, `test_worker_contract.py`, `test_cli_install.py`, `branch-protection.md`).
- Files that tasks create and that do not exist yet (correct): `tests/docs/test_release_procedure.py`, `tests/skills/test_post_release_base_branch.py`.
- Lines that tasks name: `SKILL.md:91` starts with `**Anchor the scan to the tagged commit.**`; `auggie-review.md:37,113` and `impact.md:23` hold `origin/master`; `CLAUDE.md:297` is the step 4 line; `CONTRIBUTING.md:66` has `--base master`, `:73` the protection sentence; `evals.json:19-20` hold `origin/master...HEAD` and "diff against master"; `Makefile:109` `sync-dev`, `:166` `verify-sync`.
- Dependents of the touched files that no task names: none found. `tests/unit/test_cli_install.py:180,216-218` and `tests/skills/test_worker_contract.py:2371-2384` are named in the acceptance criteria of Tasks 8 (and 7); the three command test files are named in Task 9.
- Count: 19 of 19 named files exist, 0 unnamed dependents, 0 unresolved symbols.

# Codegraph grounding

## Run state

- index_state: fresh
- checked_at: 2026-11-26T04:11:48Z (status answer: 0 added, 0 modified, 0 removed)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-290
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-290
- access: mcp (lookup tools listed)
- tokens: none
- Note: every file this plan edits is Markdown, YAML or HTML. Markdown is not indexed, so structure and dependents were confirmed with Read and Grep (the floor); the graph located only the three test functions below.

## Resolved symbols

| Name | Kind | Location | Method |
|---|---|---|---|
| test_every_deck_command_and_flag_is_in_the_guide | function | tests/docs/test_onboarding_deck.py:83 | codegraph_search, then Read of lines 1-92 |
| test_guide_is_ascii_except_the_ruling_example | function | tests/core/test_how_we_work_routing_table.py:329 | codegraph_search, then Grep and Read |
| test_guide_and_plugin_twin_are_byte_equal | function | tests/skills/test_review_prompt_overrides.py:134 | codegraph_search, then Read of lines 128-232 |

All 26 files named by the source exist (checked with `test -e`): the guide and its plugin copy, `src/superclaude/core/CLAUDE.md`, `src/superclaude/commands/recommend.md`, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms, the PR template, the deck, and the 16 test files listed in the source section 5.

## Dependents

Markdown has no call edges, so dependents are the tests and files that read each target (Grep over `tests/`, `docs/`, `src/`):

| Target | Dependents that must keep working |
|---|---|
| src/superclaude/core/HOW-WE-WORK.md and its plugin copy | tests/core/test_how_we_work_routing_table.py (ASCII, `## 4.` boundary, section references), tests/commands/test_routing_plugin_parity.py and tests/skills/test_review_prompt_overrides.py (byte-equal twin, quota and removed-phrase scan), tests/commands/test_worktrees_command.py (phrase scan of both copies), tests/skills/test_issue_protocol.py (guide row), tests/docs/test_onboarding_deck.py (deck tokens must exist in the guide), tests/cli/test_how_we_work_install.py, tests/unit/test_cli_install.py, tests/skills/test_sc_recommend_routing_contract.py, tests/recommend/test_routing_refresh.py, tests/recommend/test_cache.py, tests/commands/test_help_command.py, tests/skills/test_spec_panel_review_loop.py, tests/skills/test_review_brief_placement.py, tests/core/test_claude_md_routing_block.py |
| .github/PULL_REQUEST_TEMPLATE.md | tests/core/test_default_branch_agreement.py (line 20 reads the "rebased onto" line) |
| docs/onboarding/ironclaude-onboarding.html | tests/docs/test_onboarding_deck.py (tokens inside `<code>` and SVG text; footer pattern) |
| docs/developer-guide/contributing-code.md | linked from docs/developer-guide/documentation-index.md and docs/developer-guide/README.md (deep links to the headings that receive reminders) |
| .github/ISSUE_TEMPLATE/feature_request.yml, bug_report.yml | no test reads them; GitHub's issue-form schema is the only guard |
| CONTRIBUTING.md | no test reads it; GitHub links it from new-issue and new-PR pages |

An empty graph answer is not used as evidence of absence anywhere above.

## Pre-check

Run after the gate passed, no new readiness check (index_state stays fresh from Run state). Read-only: it edits neither the plan nor its status.

| Check | Result |
|---|---|
| Files named by Tasks 1 to 8 exist | 10 edit targets and 16 test files exist (`test -e`); the new artifacts named in tasks are created under `./artifacts/` by the tasks |
| Symbols and line anchors resolve | The three test functions resolve at the cited lines (graph); section 4 of the guide (`## 4.` at line 251, "Where this guide says" at line 263), slide `s12` (lines 515-530), footer (line 579), the PR template line 23 and the `contributing-code.md` headings were read directly on 2026-11-26 |
| Dependents named in tasks are real | Task 1 names 5 tests that read the guide copies; Task 6 names `tests/core/test_default_branch_agreement.py`; Task 7 names `tests/docs/test_onboarding_deck.py`; Task 2 names the two docs that deep-link to the edited headings; Task 8 runs all 16 test files |
| Dependents of touched files that no task names | None found. 9 of the 16 test files (install, routing contract, spec-panel loop, issue protocol, brief placement, routing refresh, cache, help command, unit install) are covered by Task 8's full run rather than a named acceptance line; no other file under `tests/` or `docs/` matched `HOW-WE-WORK`, `onboarding` or `PULL_REQUEST_TEMPLATE` |
| Graph tokens | none |

Count: 8 tasks checked, 0 unresolved names, 0 unnamed dependents.

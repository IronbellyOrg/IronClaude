# Codegraph grounding: TASK-WF-design-20261126-134817

## Run state

- index_state: fresh (`codegraph_status`: 0 added, 0 modified, 0 removed since the index; latest file indexed 2026-11-26T13:43:37Z)
- checked_at: 2026-11-26T13:48:17Z (the status call at the start of Wave 1, once for this run)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-289
- projectPath passed on every call: /home/coder/workspaces/worktrees/IronClaude/issue-289
- access: mcp (lookup tools listed)
- tokens: none for the code files. The guide, the onboarding page and the design are Markdown or HTML, which the index does not hold; they were read with Read and Grep (floor, normal evidence). No `graph:*` token is needed for that.

## Resolved symbols

| Symbol or file | Where | Source of the fact |
|---|---|---|
| `_HEADING_RE` (numbered headings only) | `tests/core/test_how_we_work_routing_table.py:99` | `codegraph_node` file outline, then Read |
| `test_each_marker_appears_exactly_once`, `test_markers_are_ordered` | `tests/core/test_how_we_work_routing_table.py:149`, `:153` | outline, Read |
| `test_guide_is_ascii_except_the_ruling_example` | `tests/core/test_how_we_work_routing_table.py:329` | outline, Read |
| `test_every_deck_command_and_flag_is_in_the_guide`, `test_deck_keeps_its_build_commit_footer`, `test_checks_catch_planted_failures`, `_FOOTER_RE` | `tests/docs/test_onboarding_deck.py:83`, `:90`, `:94`, `:23` | outline, Read |
| `_section` helper pattern | `tests/core/test_claude_md_worktree_rule.py:8` | outline |
| `_NAME_NUMBER_RE`, `numbers_in_name` (the 2-4 digit bound) | `scripts/worktree_cleanup.py:1462`, `:1470-1472` | Read (probe and reviews) |
| `/sc:worktrees` row of the other-commands table | `src/superclaude/core/HOW-WE-WORK.md:299` | Read |
| `## Orca coordination` | `src/superclaude/core/HOW-WE-WORK.md:352` | Read |
| worktree card, issue 290 card, slide intro, build footer | `docs/onboarding/ironclaude-onboarding.html:520-524`, `:525-528`, `:516-518`, `:579` | Read |

## Dependents

Markdown and HTML are not indexed, so dependents of the guide, the mirror and the deck were found with Grep for `HOW-WE-WORK` and the deck path in `tests/`. Each file below reads the file a task changes, so the task's acceptance names it.

| Changed file | Dependent test (reads it) | What it checks |
|---|---|---|
| `src/superclaude/core/HOW-WE-WORK.md` | `tests/core/test_how_we_work_routing_table.py` | markers once and in order; numbered headings; ASCII except the Ruling line; no `@`-import |
| same | `tests/core/test_claude_md_routing_block.py:17,30` | the level table in `src/superclaude/core/CLAUDE.md` equals the guide's |
| same | `tests/commands/test_worktrees_command.py:124-137` | three banned phrasings, in the guide and the mirror |
| same | `tests/cli/test_how_we_work_install.py:13,32` | the installed copy equals the guide bytes |
| same | `tests/commands/test_help_command.py:39-40`, `tests/skills/test_sc_recommend_routing_contract.py:56-59` | pointers to the guide path |
| same | `tests/recommend/test_cache.py:146-152`, `tests/recommend/test_routing_refresh.py:27` | guide hash and routing refresh |
| same | `tests/skills/test_issue_protocol.py:1188-1189`, `tests/skills/test_review_brief_placement.py:18-19`, `tests/skills/test_spec_panel_review_loop.py:24-25` | texts that must stay in the guide and the mirror |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | `tests/skills/test_review_prompt_overrides.py:134-135`, `tests/commands/test_routing_plugin_parity.py:38` | byte equality with the guide |
| `docs/onboarding/ironclaude-onboarding.html` | `tests/docs/test_onboarding_deck.py` | every command and flag in a `<code>` element is in the guide; the build footer pattern |
| `tests/core/test_how_we_work_worktree_policy.py` (new) | none | no file imports it |

Not checked with a graph lookup: whether `tests/recommend/test_cache.py` and `tests/cli/test_how_we_work_install.py` depend on guide content or only on its bytes (they use temporary copies or byte equality); the plan runs both and the executor reports a failure.

## Pre-check

Run after the gate passed, read-only (Read, Grep, `ls`; no new readiness check; `graph:*` tokens: none).

- Files named by the tasks: all 19 existing files and the directory `tests/recommend/` exist; the new test file `tests/core/test_how_we_work_worktree_policy.py` does not exist yet, as Task 6 requires.
- Line anchors: `HOW-WE-WORK.md` line 299 holds "item 4 of issue 289" (Task 2); lines 350-352 are the closing routing-table marker comment, a blank line and `## Orca coordination` (Task 1); `ironclaude-onboarding.html` lines 520 and 524 open and close the worktree card, lines 525 and 528 open and close the issue 290 card, and line 579 holds `f3c1ef06` (Tasks 4 and 5); `scripts/worktree_cleanup.py:1462` holds `_NAME_NUMBER_RE = re.compile(r"(?<!\d)(\d{2,4})(?!\d)")`, the bound Task 6 copies.
- Mirror: `cmp` of the guide and the mirror is clean today, so Task 3 starts from a known equal pair.
- Dependents no task names: `tests/unit/test_cli_install.py:106,416` lists `HOW-WE-WORK.md` among installed file names only (file names, not content), so a content change does not affect it. `tests/recommend/test_cache.py` and `tests/recommend/test_routing_refresh.py` are covered by Task 7's run of `tests/recommend`.
- Not confirmed with a graph lookup (the index holds no Markdown or HTML): that no other file quotes the sentence changed in Task 2; Grep over the repository, excluding `.dev/` and generated docs, found it only in the guide and its mirror.

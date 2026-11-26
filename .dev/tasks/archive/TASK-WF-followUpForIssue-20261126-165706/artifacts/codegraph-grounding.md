# Codegraph grounding

## Run state
- index_state: fresh (codegraph_status: 4238 files, 0 added, 0 modified, 0 removed since index)
- access: mcp
- checked_at: 2026-11-26T16:58:56Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-289
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-289
- cli_version: 1.6.2
- token: graph:provenance_unproven (version pin not compared in this run); graph rows are leads only
- note: the index holds Python and YAML only; every file of this plan except the two test files is Markdown or HTML, so Grep and Read carry the grounding.

## Resolved symbols
- tests/core/test_how_we_work_worktree_policy.py: branch_errors, max_words_length, _section, _missing_phrases, _NUMBER_RUN, _BRANCH_RE, _ISSUE_PART_RE, _KEY_PHRASES (read; Grep floor)
- scripts/worktree_cleanup.py:1462 _NAME_NUMBER_RE and :1470 numbers_in_name (read)
- tests/worktree_cleanup/conftest.py:26 load_script (read)

## Dependents
- Dependents of the changed guide section: tests/core/test_how_we_work_worktree_policy.py (pins section, mirror, deck card), tests/core/test_how_we_work_routing_table.py (pins the /sc:worktrees row, not the section), the plugin mirror plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md.
- Dependents of CLAUDE.md lines 301-342: tests/core/test_claude_md_worktree_rule.py (pins --agent, ownership bullet, create line, kept rules).
- Dependents of the deck footer and slide 12: tests/docs/test_onboarding_deck.py (footer regex only), tests/core/test_how_we_work_worktree_policy.py::test_deck_card_is_replaced_and_neighbours_untouched.
- Stale worktree-name examples: only CLAUDE.md lines 319, 335-336, 341 (git grep over CLAUDE.md, src, docs, plugins); src/superclaude/core/CLAUDE.md has none.

# Codegraph grounding

## Run state

index_state: fresh
access: mcp
checked_at: 2026-11-26T04:48:38Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-758
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-758
Tokens: none. MCP reported zero pending changes. Switch unset; no init/index process found (pgrep exit 1 is the expected no-match). Markdown is outside the graph index and uses Read/Grep. Augment retrieval completed on integration; irrelevant rescued-worktree results were ignored.

## Resolved symbols

Read canonical pragmatic.md Decision requests and writing conventions; read test_pragmatic_plain_english.py (_text, _in_order, existing literal assertions). Read install_user_setup.py (_package_dir, _copy_tree, install_output_styles, install_user_setup) and its graph outline. Read test_install_user_setup.py:test_output_style_installs and existing test_install_keep.py style tests. Read Makefile sync targets: styles are not copied. No production callable changes planned.

## Dependents

Graph callers of install_output_styles: 9/9 rows, definition leads only except the direct call confirmed at install_user_setup.py:644 (resolution: call-site-verified). Existing content test and installed-style test depend on the style. Grep found tests/commands/test_sweep_command.py and tests/skills/test_review_{prompt_overrides,severity_mapping,severity_rule}.py as style readers; these require no edits because their sections are unchanged, but are included in regression runs. pragmatic-subagent.js reads the installed file wholesale and strips frontmatter; no hook change required. test_install_keep.py already covers keep, forced refresh, backups and failed-save preservation, so reuse those tests rather than duplicate them. No renamed/deleted/re-signed symbols; no export/config/fixture changes required.

## Pre-check

Two tasks grounded; all three delivery paths and seven scoped regression paths exist. No production symbol changes. Each dependency either has a named scoped regression or is inspected unchanged (installer wrapper and installed-style hook). No uncovered affected callable found in the bounded search. Markdown uses direct Read; no graph lookup pretends to index it. Phase 1 produces the style guidance; Phase 2 produces content/delivery test coverage; acceptance criteria carry verification, not a standalone verification-only task.

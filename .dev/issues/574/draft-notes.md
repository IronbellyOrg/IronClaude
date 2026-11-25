# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

- Tool prunes tool calls/results instead of writing a summary, via TypeSafe's Jev API (`jev-latest`, `https://api.typesafe.ai/v1/systemone`); prose unchanged — source-fast-jev-compaction.md:7,14,30,57.
- Requirements: `TYPESAFE_API_KEY`, Claude Code 2.1.274+, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`; replaces `/compact` and automatic compaction for the session — source-fast-jev-compaction.md:34,36.
- Each request sends conversation text (prose, tool inputs, output placeholders) to `https://api.typesafe.ai/v1/systemone` — source-fast-jev-compaction.md:57.
- README reports no benchmark numbers (latency, token savings, accuracy, comparisons); tags/releases/latest commit not shown — source-fast-jev-compaction.md:3,52.
- Key defaults: `maxStateTokens` 25000, `maxRequestTokens` 30000, `keepThreshold` 0.5, `preserveRecentMessages` 6, `truncateHeadChars` 300; MIT licence; commit count 30; branch `main` — source-fast-jev-compaction.md:30,46.
- `src/superclaude/cli/user_settings_defaults.json` (origin/master) has no `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`, no `TYPESAFE_API_KEY` and no fast-jev entry in `enabledPlugins` — `git show origin/master:src/superclaude/cli/user_settings_defaults.json`.
- IronClaude compaction-adjacent docs exist: `docs/reference/claude-code-history-management.md` and ccsession context/auto-compact window docs — Grep for `compaction|compact|context window` in the checkout.
- Relationships to #553, #552, #463 — scout.md:40-42,55-57.

## Contradictions

- None

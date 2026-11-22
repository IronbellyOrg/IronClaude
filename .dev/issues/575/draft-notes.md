# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Plugin id is `fast-jev-output`, not `jev-pruner`; keep-originals-not-summary behavior; archives under `.claude/fast-jev-output/`; needs TYPESAFE_API_KEY, TypeSafe credits, early-access function hooks (declarations generated with Claude Code 2.1.274, minimum not shown), CLAUDE_CODE_ENABLE_FUNCTION_HOOKS; each request sends command, output, task text and conversation history to https://api.typesafe.ai/v1/systemone; README states no transcript redaction; README reports no aggregate benchmark numbers. Source: source-jev-pruner.md:7,15,23-24,53-55,49.
- Data-sharing approval not established (open owner decision in #552) — source: task brief from orchestrator; scout.md:61 (#552 blocker classifier using Jev).
- Related issues #553/#552/#463 and that #553 is a different plugin — scout.md:40-42,59-62.
- Evaluation deliverable (verdict ADOPT/PILOT/REJECT/BLOCKED, baselines, sandbox, no IronClaude change) — task brief from orchestrator.
- IronClaude plugin-defaults facts: defaults in `src/superclaude/cli/user_settings_defaults.json` (`enabledPlugins`, `extraKnownMarketplaces`, `ironclaudeMarketplace`), installed by `src/superclaude/cli/install_user_setup.py` (marketplace catalog at ~/.claude/ironclaude-marketplace/, nested-key merge) — command: `git show origin/master:src/superclaude/cli/user_settings_defaults.json` and `git show origin/master:src/superclaude/cli/install_user_setup.py` (lines 11-19, 42-49); no repo references to CLAUDE_CODE_ENABLE_FUNCTION_HOOKS/TypeSafe — command: grep over `origin/master` (d4d1662a8) tree, zero matches.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None

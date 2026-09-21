# BUILD REQUEST

GOAL: Harden IronClaude's project-owned MCP installation surfaces with only verified upgrades: Tavily 0.2.20 to 0.2.22; Sequential Thinking to 2026.8.31; official Serena 1.7.0 replacing floating Git installation; official Auggie 0.36.0 guidance and project-local official executable configuration; and the supported Morph MCP successor replacing deprecated Morph Fast Apply.

WHY: Floating/deprecated/unofficial MCP sources make installations non-reproducible and leave users exposed to dependency drift. Preserve existing exact-command reconciliation.

OUTPUTS:
- Minimal source, test, documentation, and project `.mcp.json` changes.
- Tests for changed registry commands and the official project-local Auggie configuration.
- `make sync-dev` output only; never stage generated `.claude/` content.

CONSTRAINTS:
- Re-verify every included version and command from a primary vendor source before editing.
- Exclude Context7, Playwright, Chrome DevTools, Magic, AIRIS, Markdown Collab, and user-level Codebase Memory.
- Do not modify machine/user configuration outside the repository.
- Use UV for tests.
- `src/superclaude/` is source of truth.

TEMPLATE: 02
QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: FINAL_ONLY
VALIDATION_REQUIREMENTS: Targeted installer/document tests, then make sync-dev, make verify-sync, make lint, and relevant test suite.
TESTING_REQUIREMENTS: UNIT
POST_REFLECT_GATE: DISABLED

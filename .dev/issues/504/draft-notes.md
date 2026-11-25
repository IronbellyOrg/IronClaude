# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

- Proposed readiness-gated Codegraph usage, Grep/Read fallback, fallback recording, and fresh-index-only agent rule: user-intended scope in the task instructions; existing pattern evidenced by `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:33` and `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:446`.
- Source-of-truth and synchronization acceptance criterion (`src/superclaude/`, `make sync-dev`, `make verify-sync`): task instructions and the repository's component-sync workflow in `CLAUDE.md`.
- Related issue #323: `.dev/issues/draft-20261111-191459-add-codegraph-to-agents-analyze-design-i/scout.md:47`.

## Contradictions

- The description says “agents analyze, design, implement and workflow” (`.dev/issues/draft-20261111-191459-add-codegraph-to-agents-analyze-design-i/description.md:3`), but these are slash commands: the command definitions identify `/sc:analyze` and `/sc:design` at `src/superclaude/commands/analyze.md:10` and `src/superclaude/commands/design.md:10`, and `/sc:implement` and `/sc:workflow` at `src/superclaude/commands/implement.md:9` and `src/superclaude/commands/workflow.md:10`. The issue body corrects this by describing command definitions and backing skills separately from the general-purpose agent files.

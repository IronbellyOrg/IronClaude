## Feature Summary

Add conditional Codegraph support to `/sc:analyze`, `/sc:design`, `/sc:implement`, and `/sc:workflow`, while preserving Grep/Read as the fallback. Add a shared rule to the general-purpose agent files to use Codegraph only when the caller passes `index_state: fresh`.

## Problem Statement

These commands and their backing skills do not currently use Codegraph, so their codebase analysis and implementation planning lack the structural search available elsewhere in the project. General-purpose agents also need a consistent rule for using Codegraph safely when index freshness has been established by the caller.

## User Story

As a user of these commands and agents, I want them to use Codegraph when its index is fresh and retain Grep/Read otherwise, so that codebase work can benefit from structural search without depending on a stale or unavailable index.

## Proposed Solution

Add one Codegraph readiness check to each of the four slash-command workflows. When the index is fresh, use the available Codegraph tools above the existing Grep/Read floor; when it is not fresh or Codegraph is unavailable, continue with Grep/Read and record the fallback. Update the general-purpose agent files with a shared rule: use Codegraph only when the caller passes `index_state: fresh`; otherwise use Grep/Read. Apply the changes to the source files under `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. The affected entry points are slash commands and their backing skills where present, not agent files named “analyze,” “design,” “implement,” or “workflow.”

## Acceptance Criteria

- [ ] Each of `/sc:analyze`, `/sc:design`, `/sc:implement`, and `/sc:workflow` documents exactly one Codegraph readiness check for its run.
- [ ] Each command uses the available Codegraph tools above the Grep/Read floor only when readiness establishes a fresh index.
- [ ] Each command continues with Grep/Read and records a fallback note when Codegraph is unavailable or the index is not fresh.
- [ ] The general-purpose agent files in scope state that Codegraph may be used only when the caller passes `index_state: fresh`; otherwise agents use Grep/Read.
- [ ] Source changes are made under `src/superclaude/`, and `make sync-dev` followed by `make verify-sync` succeeds.

## Out of Scope

Changing `/sc:troubleshoot` or `/sc:reflect`, which already use Codegraph, and changing the Codegraph MCP server itself.

## Components Affected (from `/sc:analyze`)

- `src/superclaude/commands/analyze.md` — `/sc:analyze` command definition.
- `src/superclaude/commands/design.md` — `/sc:design` command definition.
- `src/superclaude/commands/implement.md` — `/sc:implement` command definition.
- `src/superclaude/commands/workflow.md` — `/sc:workflow` command definition.
- `src/superclaude/skills/sc-implement-protocol/SKILL.md` — backing implementation protocol.
- `src/superclaude/skills/sc-workflow-protocol/SKILL.md` — backing workflow protocol.
- `src/superclaude/agents/` — applicable general-purpose agent definitions, including `system-architect.md`, `root-cause-analyst.md`, `refactoring-expert.md`, `security-engineer.md`, `performance-engineer.md`, `python-expert.md`, `backend-architect.md`, `quality-engineer.md`, `self-review.md`, and `technical-writer.md`.
- `~/.claude/CODEGRAPH.md` — Codegraph usage guide referenced by the existing protocols.

## Related Issues/PRs

- [#323 — Replace Codememory-mcp with CodeGraph](https://github.com/IronbellyOrg/IronClaude/issues/323) (closed; related Codegraph integration work).

<!-- sc:issue:create template=issue-feature-simple -->

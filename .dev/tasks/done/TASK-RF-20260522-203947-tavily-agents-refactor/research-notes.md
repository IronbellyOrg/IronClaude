# Research Notes: Tavily-first Agents Refactor — task build

**Date:** 2026-05-22
**Scenario:** A (explicit) — 10 fully-formed refactor proposals already exist as inputs
**Depth Tier:** Standard
**Track Count:** 1 (single track, 10 sibling per-agent edits)

---

## EXISTING_FILES

Input proposals (each contains `Current state`, `Proposed refactor`, `Acceptance criteria`, `Reflection notes`):

- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/deep-research-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/deep-research-agent-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-task-researcher-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-task-builder-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-task-executor-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-assembler-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-analyst-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-qa-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-qa-qualitative-tavily-refactor.md`
- `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/_sweep-summary.md` — confirms no other agents in scope.

Target agent files (the SoT to edit):

- `src/superclaude/agents/deep-research.md`
- `src/superclaude/agents/deep-research-agent.md`
- `src/superclaude/agents/rf-task-researcher.md`
- `src/superclaude/agents/rf-task-builder.md`
- `src/superclaude/agents/rf-task-executor.md`
- `src/superclaude/agents/rf-team-lead.md`
- `src/superclaude/agents/rf-assembler.md`
- `src/superclaude/agents/rf-analyst.md`
- `src/superclaude/agents/rf-qa.md`
- `src/superclaude/agents/rf-qa-qualitative.md`

Build/sync targets verified in Makefile:

- `make sync-dev` — copies `src/superclaude/{skills,agents,commands}` → `.claude/`
- `make verify-sync` — fails if `src/` ↔ `.claude/` drift
- `make lint`, `make test` — exist
- `uv run pytest` — primary test runner per project CLAUDE.md

## PATTERNS_AND_CONVENTIONS

- Source of truth: `src/superclaude/agents/` (per project CLAUDE.md). Never edit `.claude/agents/` directly; sync-dev is the only legal way to populate it.
- `.claude/` (except `settings.json`) is **gitignored** — staging it is forbidden per CLAUDE.md absolute rule.
- Agent files use YAML frontmatter with `tools:` list. Tavily MCP tool IDs: `mcp__tavily__tavily-search`, `mcp__tavily__tavily-extract`. Fallback tools: `WebSearch`, `WebFetch`.
- Each proposal specifies its own diff-style edits (frontmatter reordering + body insertions + new Critical Rule). No invented edits beyond what proposals authorize.
- Per CLAUDE.md, no multi-line paste-ready heredocs in instructions to the user; Edits should be Edit tool calls, not sed/Python.

## GAPS_AND_QUESTIONS

- None blocking. The 10 proposals are already adversarially-reviewed (each ran /sc:reflect) and contain verbatim diff-style edits. The sweep summary confirms no additional agents need this refactor.
- One operational question for the executor: whether to commit per-agent edits as one batch commit or 10 sibling commits. **Default: one batch commit** ("feat(agents): Tavily-first web search precedence across 10 agents") — matches feedback `feedback_no_multiline_paste.md` and avoids 10 review-noise commits. Document as Open Question for user review.

## RECOMMENDED_OUTPUTS

- One MDTM task file at `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/TASK-RF-20260522-203947-tavily-agents-refactor.md`
- Template 02 (complex) — 10 per-agent items + sync gate + smoke gate + commit.

## SUGGESTED_PHASES

- **Phase 1 — Preparation**: Read all 10 proposals; verify target agent files exist and are unmodified vs. assumed baselines in each proposal's "Current state" section.
- **Phase 2 — Apply per-agent refactors (10 items, partitionable)**: One checklist item per agent. Each item embeds the verbatim frontmatter + body edits from its proposal, with per-agent acceptance criteria.
- **Phase 3 — Sync & verify**: `make sync-dev`, `make verify-sync`, `make lint`.
- **Phase 4 — Smoke tests**: `uv run pytest` (note: agent-surface coverage is documentation-style; expect no behavioral regressions but verify suite is still green).
- **Phase 5 — Stage & commit**: `git add src/superclaude/agents/<10 files>`; commit with conventional message. Explicitly NOT staging `.claude/agents/` (gitignored per CLAUDE.md absolute rule).
- **Phase 6 — Completion**: Update task frontmatter status → Done.

## TEMPLATE_NOTES

- Template 02 (complex) — has discovery (Phase 1), 10-item parallel-safe implementation (Phase 2), verify gates (Phase 3-4), staging/commit gate (Phase 5), completion (Phase 6).
- Tier: Standard. Scope (10 files, all under a single directory, all with explicit diff-style proposals) is moderate, not Deep.
- Each Phase-2 item is partitionable — the executor can fan out subagents per item.

## AMBIGUITIES_FOR_USER

- Commit grouping (batch vs. per-agent commits). Default chosen: batch. Surface in Open Questions.
- Whether to also update any downstream `.dev/` documentation referencing these agents. Default: out of scope for this task — the agent definitions are the surface; downstream doc updates can be a follow-up task.

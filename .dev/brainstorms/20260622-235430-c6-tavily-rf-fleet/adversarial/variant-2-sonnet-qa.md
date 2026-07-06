# Variant 2 — QA Advocate: RF Agent Fleet Tavily 0.2.x Change Spec

## QA position

`tavily-mcp` 0.2.x does not require RF agent frontmatter changes. The currently referenced tool IDs remain `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract`; all 8 scoped RF agents already list both in `tools:`. The change should therefore be regression-prevention around parity, fallback provenance, and capability creep, not a tool-list migration.

## Per-agent verdicts

| Agent | Verdict |
|---|---|
| `rf-qa.md` | Keep frontmatter. Prose references search/extract only and has auditable `Tool engagement:` fallback reporting. |
| `rf-qa-qualitative.md` | Keep frontmatter. Same search/extract-only posture; qualitative checks repeat Tavily-first reporting expectations. |
| `rf-task-researcher.md` | Keep frontmatter. Primary web researcher; fallback provenance uses `WEB SEARCH PROVENANCE` with `provider=tavily` default or `provider=WebSearch reason=<...>`. |
| `rf-task-builder.md` | Keep frontmatter. Builder only uses Tavily to validate checklist context; fallback annotation is item-scoped HTML `web-provenance`. |
| `rf-team-lead.md` | Keep frontmatter. Orchestration-level web checks only; pipeline fallback note is prose-form, not schema-like. |
| `rf-analyst.md` | Keep frontmatter. Rare external verification only; fallback marker is bracketed `WEB_RESEARCH_FALLBACK`. |
| `rf-assembler.md` | Keep frontmatter. Web use is explicitly unauthorized unless spawn/fix prompt requires it; fallback marker mirrors analyst. |
| `rf-task-executor.md` | Keep frontmatter. Web use is recovery-only; fallback provenance is `web-lookup: provider=<...>` in progress/error messages. |

## Fallback vocabulary decision

Do not standardize RF fallback output vocabulary in this C1/C6 change. The vocabulary differs because the agents emit fallback provenance into different artifacts: QA reports, research notes, task checklist comments, pipeline messages, analysis reports, assembled documents, and executor status messages. Forcing the deep-research C2 enum (`tavily_missing|tavily_error|tavily_rate_limit|tavily_auth`) or renaming RF's existing hyphen tokens would create backward-compat risk for parsers and human grep habits without being required by the 0.2.x version bump.

Instead, standardize only the semantic reason classes in tests: unavailable/missing, tool/server/auth/config error, and rate-limit/quota. Accept each agent's existing wire vocabulary as long as it maps to one of those classes and remains auditable.

## Fleet-wide parity and consistency test design

Add a shared agent-doc parity test that scans every `src/superclaude/agents/*.md`, not just RF agents:

1. Parse YAML frontmatter `tools:`.
2. Regex prose references for every `mcp__tavily__[A-Za-z0-9_-]+` token.
3. Fail if prose references a Tavily MCP token not present in that file's frontmatter.
4. Fail if frontmatter includes `mcp__tavily__tavily-map` or `mcp__tavily__tavily-crawl` outside the approved deep-research-only allowlist.
5. For the 8 RF agents, assert `tavily-search` and `tavily-extract` are present, and `map`/`crawl` are absent.
6. For the 8 RF agents, assert at least one fallback-provenance marker exists and contains a reason expression mappable to the semantic classes above.
7. Share the same helper/fixture with C2 so deep-research additions and RF restrictions are validated by one source of truth.

## Acceptance criteria

- No RF agent frontmatter changes are made for `tavily-mcp` 0.2.x.
- All 8 RF agents continue to reference only `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` in prose.
- The parity test fails on prose/frontmatter mismatch for any Tavily MCP tool across all agents.
- The parity test fails if map/crawl appear in RF agent frontmatter or prose.
- Existing RF fallback provenance strings remain valid; no migration is required for existing reports, notes, task files, or status messages.
- Future fallback-vocabulary consolidation, if desired, is a separate compatibility-aware change with fixture coverage for legacy tokens.

## Biggest QA risk

The highest-risk regression is capability completion: someone sees `tavily-mcp` 0.2.x exposes more tools and adds map/crawl to every Tavily-aware agent. That would expand RF agents beyond their narrow external-lookup roles and create new prose/frontmatter drift surfaces. The guardrail should be test-enforced absence, not reviewer memory.

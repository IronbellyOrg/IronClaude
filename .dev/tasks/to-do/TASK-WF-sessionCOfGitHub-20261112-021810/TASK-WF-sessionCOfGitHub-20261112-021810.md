---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-sessionCOfGitHub-20261112-021810
version: "1"
priority: Medium
created_date: "2026-11-12"
---

# Issue 512 session C: Tavily and Context7 tool names in research prompts

Source: ./source.md
Goal: The task-builder, tech-research, tdd and tech-reference primitives name the Tavily (and, where specified, Context7) tools in their web-research prompts, proxy name first and direct name second, with a WebSearch/WebFetch floor, and the dev copies are in sync.

## Constraints

- Edit only files under src/superclaude/; run make sync-dev afterwards and never stage .claude/. Do not edit plugins/, src/superclaude/skills/tdd/refs/build-request-template.md, or the rf-task-builder and rf-task-researcher agents. No commit or push by the session; the coordinator stages `.dev/tasks` and the source files and commits.
- The shared Tools paragraph is this single line, identical in every file that uses it (capital Tools: so the lowercase tool-key regex in tests/skills/test_mcp_proxy_names.py does not parse it):

```
Tools: mcp__litellm__Tavily-tavily_search and mcp__litellm__Tavily-tavily_extract (else mcp__tavily__tavily_search and mcp__tavily__tavily_extract) for web pages; mcp__litellm__context7-resolve-library-id then mcp__litellm__context7-query-docs (else mcp__context7__resolve-library-id then mcp__context7__query-docs) for library or framework docs. If none is available, use WebSearch and WebFetch.
```

- The metadata comment block used by E5, E6 and E9 is three lines, followed by a blank line and then the existing H1: an HTML comment opening line `<!-- Extended metadata (for documentation, not parsed):`, the `mcp-servers: [...]` line, and `-->`.
- Do not add an allowed-tools line to any skill (it would narrow tool access). Do not name tavily map or crawl.
- Re-verify each old-text anchor against the live file before editing; if an anchor drifted, adapt to the same intent and report it.

## Phase 1: Tavily-first wording in task-builder

## Task 1: Apply E4 in src/superclaude/skills/task-builder/SKILL.md

Make four in-place single-line changes, adding no lines (shipped docs cite this file's line numbers; the file is currently 2606 lines). Replace both occurrences (lines 643 and 1885) of `Use WebSearch to investigate:` with `Use mcp__litellm__Tavily-tavily_search (else mcp__tavily__tavily_search; WebSearch only when Tavily is unavailable) to investigate:`. Replace line 1209 `    - **External docs/syntax** → use WebSearch` with `    - **External docs/syntax** → use mcp__litellm__Tavily-tavily_search (else mcp__tavily__tavily_search; WebSearch only when Tavily is unavailable, and annotate the item per your Rule 13)`. Replace the single line `Research Protocol:` (line 949) with `Research Protocol (web search: mcp__litellm__Tavily-tavily_search, else mcp__tavily__tavily_search; WebSearch only when Tavily is unavailable):`. Leave line 1208 (the WebSearch-or-augment codebase line) untouched.

Acceptance criteria:
- src/superclaude/skills/task-builder/SKILL.md still has exactly 2606 lines and the four changes are present with Tavily first.
- tests/skills/test_task_builder_merge.py, tests/agents/test_tavily_tool_parity.py and tests/audit/test_hidden_input_guard.py pass.

## Phase 2: Tools paragraph and metadata in the other research primitives

## Task 2: Apply E5 in src/superclaude/skills/tech-research/SKILL.md

Replace the H1 line 6 `# Technical Research & Investigation` with the three-line metadata comment (`mcp-servers: [litellm, auggie, context7, tavily]`), a blank line, then the H1. In the Web Research Agent prompt code block, between `3. Never accumulate and one-shot` (occurs once, near line 752) with its following blank line and the `Research Protocol:` line (which occurs twice in the file, so anchor on the accumulate line), insert the shared Tools line and a blank line. Make no change near the line-455 escalation block.

Acceptance criteria:
- The metadata comment precedes the H1 and the shared Tools line appears exactly once, in the Web Research Agent prompt.
- tests/skills/test_review_severity_rule.py, tests/skills/test_review_prompt_overrides.py and tests/skills/test_mcp_proxy_names.py pass.

## Task 3: Apply E6 in src/superclaude/commands/tdd.md, src/superclaude/skills/tdd/SKILL.md and src/superclaude/skills/tdd/refs/agent-prompts.md

In src/superclaude/commands/tdd.md change line 7 `mcp-servers: [litellm, context7, auggie]` to `mcp-servers: [litellm, context7, auggie, tavily]` and leave allowed-tools and `> Skill tdd` untouched. In src/superclaude/skills/tdd/SKILL.md replace the H1 `# TDD Creator` with the three-line metadata comment (`mcp-servers: [litellm, context7, auggie, tavily]`), a blank line, then the H1. In src/superclaude/skills/tdd/refs/agent-prompts.md insert the shared Tools line and a blank line between `3. Never accumulate and one-shot` (line 120) with its following blank line and `Research Protocol:` (line 122). Preserve the literal `Only PASS or FAIL — no conditional pass.` with the em dash.

Acceptance criteria:
- The three files carry the changes above and the em-dash literal in agent-prompts.md is unchanged.
- tests/skills/test_review_severity_rule.py, tests/skills/test_worker_contract.py, tests/recommend/test_routing_refresh.py and tests/skills/test_sc_recommend_routing_contract.py pass.

## Task 4: Apply E9 in src/superclaude/skills/tech-reference/SKILL.md

Replace the H1 line 6 `# Technical Reference Creator` with the three-line metadata comment (`mcp-servers: [litellm, auggie, context7, tavily]`), a blank line, then the H1. Insert the shared Tools line and a blank line between `3. Never accumulate and one-shot` (occurs once, near line 737) with its following blank line and `Research Protocol:` (near line 739). Make no change near the line-481 escalation block.

Acceptance criteria:
- The metadata comment precedes the H1 and the shared Tools line appears exactly once.
- tests/core/test_how_we_work_routing_table.py, tests/skills/test_review_severity_rule.py and tests/skills/test_mcp_proxy_names.py pass.

## Phase 3: Sync dev copies

## Task 5: Sync the six edited files into .claude/ with make sync-dev

Depends on: Task 1, Task 2, Task 3, Task 4

Run `make sync-dev` (one re-run is allowed if another session's file shows as unsynced; never edit files owned by another session), then check with `make verify-sync`. Do not stage .claude/. Evidence of the run goes to ./artifacts/sync-verify.log.

Acceptance criteria:
- make verify-sync reports no difference for the six files this plan edits.
- `uv run pytest tests/skills tests/commands tests/agents tests/core tests/unit/test_cli_install.py tests/cli/eval -q` shows no failure caused by these six files, and `uv run ruff check src tests scripts` passes.

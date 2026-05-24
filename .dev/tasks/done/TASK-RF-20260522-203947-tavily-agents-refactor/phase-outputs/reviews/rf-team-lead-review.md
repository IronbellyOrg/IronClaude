# rf-team-lead Tavily-first Refactor — Acceptance Review

**Target:** `/config/workspace/IronClaude/src/superclaude/agents/rf-team-lead.md`
**Proposal:** `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/rf-team-lead-tavily-refactor.md`
**Phase:** 2 / Step 2.6
**Verification method:** Re-Read of target file after Edits applied.

## Acceptance Criteria Checklist

1. **[PASS]** Frontmatter `tools:` contains both Tavily entries — `mcp__tavily__tavily-search` (line 13) and `mcp__tavily__tavily-extract` (line 14).
2. **[PASS]** Frontmatter `tools:` still contains `WebSearch` (line 15) and `WebFetch` (line 16).
3. **[PASS]** Tavily entries (lines 13-14) appear before `WebSearch` / `WebFetch` (lines 15-16), with inline comments `# PRIMARY ...` and `# FALLBACK only — Tavily unavailable`.
4. **[PASS]** "WebSearch — Understanding Unfamiliar Technologies" subsection no longer exists (replaced; grep of file shows zero occurrences of that heading).
5. **[PASS]** New "Web Research — Tavily-first Protocol" subsection exists at line 294 under "## Extended Tools".
6. **[PASS]** New subsection explicitly names both `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` as PRIMARY (lines 299-304 under the "ALWAYS try Tavily MCP first:" bolded heading; frontmatter inline comments also tag them PRIMARY).
7. **[PASS]** Three Tavily-unavailable conditions defined (lines 309-316): (1) tool not loaded / unknown-tool error, (2) explicit server error after one retry, (3) rate-limit with no budget to wait.
8. **[PASS]** New subsection contains the literal phrase "Do NOT use WebSearch or WebFetch as a first choice" (line 322).
9. **[PASS]** New Critical Rule 11 added (line 389) covering Tavily-first; numbered after existing rules 1-10, does not displace rule 1's emphasis on three-teammate spawning.
10. **[PASS]** Fallback observability requirement present — the literal phrase `Tavily unavailable (<reason>); fell back to WebSearch/WebFetch.` appears at line 320, and Critical Rule 11 reiterates "Note any fallback in the pipeline output."
11. **[PASS]** No existing responsibilities removed or weakened — team spawning (lines 50-77), parallel tracks (Phase 2b), scope discovery (Phase 2c), multi-researcher model, research review protocol, AskUserQuestion section, /rf:opinion section, Phase 1-7 workflow, error handling, Critical Rules 1-10, agent memory, template selection, project mode, and cleanup all remain unchanged. The only structural change is the replacement of one Extended-Tools subsection and the append of one Critical Rule.
12. **[DEFERRED to Phase 3]** `make sync-dev && make verify-sync` will be executed in Phase 3 per task instructions.

## Anomalies

None. All three Edit operations succeeded on first attempt; Re-Read confirms exact-text application of the proposal blocks. The `.claude/agents/` mirror was not touched (sync deferred to Phase 3 per instructions and per the "Never stage .claude/" rule).

**Overall Verdict:** PASS

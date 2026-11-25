# Summary: #597 [BUG] Research routing bypasses available Context7 and Tavily MCP tools

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/597
- Type: bug
- Complexity: simple (rubric: `refs/claim.md`; up to 4 hours in one area: research-routing instructions and their verification)
- Effort estimate: 3 hours
- spec-route: design — Simple issue with explicit acceptance criteria: Context7-first documentation lookup, Tavily-first current-information lookup, capable delegation or direct orchestrator lookup, and valid native-tool fallback.

## What the issue asks for

Make ordinary research questions use the available research MCP tools (the connected documentation and web-search services), rather than bypassing them through an unsuitable delegated agent. Use Context7 for library/framework documentation and Tavily for current online information, confirming a likely answer's page before searching more; keep native web tools and local code search as valid fallbacks when appropriate. Before delegating research, check that the agent has the needed tools, or do the MCP lookup in the orchestrator itself. The issue records one interrupted historical lookup, not a measured default failure rate. Local trace recovery on 2026-11-23 found the original parent and child: the advertised guide roster lacks Context7/Tavily, and the child performed ten WebFetch calls without a research MCP call before interruption. Historical backend health and broader frequency remain unknown; see the trace-recovery addendum below.

The accuracy check is `out_of_date` for the recorded environment/current source citation, not because the substantive bug is resolved. Existing MCP-capable research agents predate the issue; a narrow core routing rule and focused verification are the smallest supported change, rather than a new agent or an installer/server change.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/core/CLAUDE.md` | Main framework instruction entry point. Names Context7/Tavily roles and advisory flag hints, but its ten core rules lack an explicit research-delegate capability check. Primary candidate for the bounded instruction fix. |
| `src/superclaude/core/RULES.md` | Already requires MCP > Native > Basic and Context7 for docs; preserve this existing preference rather than treating it as absent. The issue's old line citation shifted. |
| `src/superclaude/agents/deep-research.md` | Existing research destination with proxy/direct Tavily and Context7 tools, MCP-first guidance and disclosed fallback. |
| `src/superclaude/agents/deep-research-agent.md` | Another existing capable destination; selected by the research command. Neither agent needs a new MCP allowlist merely to satisfy this issue. |
| `src/superclaude/commands/research.md` | Explicit research command already points to deep-research-agent and Tavily. The incident concerns conversational delegation, not absence of this command. |
| `src/superclaude/commands/explain.md` | Already declares Context7 integration and supports delegation; useful documentation-routing regression surface. |
| `src/superclaude/mcp/MCP_Context7.md` and `src/superclaude/mcp/MCP_Tavily.md` | Existing documentation/web selection guidance and native fallback. Do not turn the preference into a blanket native-tool ban. |
| `src/superclaude/core/RESEARCH_CONFIG.md` | Defines research depth profiles, extraction routing and fallback. Quick research currently enables search only; avoid accidentally redesigning these profiles for a small routing fix. |
| `tests/agents/test_tavily_tool_parity.py` | Existing static tool-declaration/parity test pattern. Does not demonstrate a live orchestrator's first-tool or delegate choice. A focused instruction guard plus observed manual scenarios is appropriate. |
| Host-provided `claude-code-guide` agent | No repository-owned definition/reference found by scoped search. Recovered historical host context advertises Glob/Grep/Read/WebFetch/WebSearch only; original child events show native fetches. Route around an unsuitable delegate rather than assume its host definition is editable here. |
| `pyproject.toml` | Current package version is 6.1.0; the issue's 5.0.0 environment is historical incident context, not today's checkout. |
| Installed and development copies | Edit canonical distributable source, not installed/global or generated `.claude/` copies. Existing synchronization/install workflows can distribute an approved instruction change. |

Effort breakdown: 0.5 hour to pin the narrow routing wording and fallback conditions, 0.5 hour for the instruction change, 0.5 hour for a focused static guard, and 1.5 hours for documentation/web/delegation/fallback manual checks and recording evidence. This estimates implementation and verification; no tests or live MCP sessions were run during this accuracy pass. It does not assume changes to multiple runtime subsystems, permissions or server configuration. If verification establishes a separate host/runtime defect, rescope and re-estimate before implementation.

## Analysis

- [Recovered historical traces](trace-recovery/REPORT.md): direct owner-requested local follow-up, with original event provenance in [evidence.md](trace-recovery/evidence.md). Supersedes the earlier missing-transcript assessment; the settled worker contract remains a record of that earlier run, not the current evidence state. This describes the trace-recovery stage; the later uncommitted rule and single live replay are recorded below.

- [Delegation, Tavily and fallback replay](delegation-replay/REPORT.md): 8 real Sonnet 5.5 sessions, $1.81 total. With a reconstructed native-only guide agent in the roster, the before arm went straight to native WebFetch in 2 of 2 runs and the after arm used Context7 in 2 of 2. Current-information question: before used WebFetch first, after used Tavily search then extract. With the research server disconnected, both arms fell back to native tools without error. No session delegated to the guide, so the delegate-capability clause is still untested. Tiny samples, no statistical claim. Independent review (`delegation-replay/review.md`) first returned FAIL on three wording defects; all were corrected after the parent verified them, and no second review was run.

- [Matched non-Opus before/after](matched-replay/REPORT.md): both real sessions served Sonnet 5.5 with identical question/tools/config and only rule 11 changed. Both used Context7 resolve/query first and completed successfully, total reported API cost $0.1693183. No improvement demonstrated in this one pair; guide delegation, Tavily and fallback remain untested. Independent raw-trace reporting review PASS.

- [Changed-rule live replay](live-replay/REPORT.md): owner-approved single real CLI documentation replay with the current canonical core explicitly appended. Context7 resolve then query succeeded, zero native web/delegate calls, three turns, reported API cost $0.2274008. This is a one-model smoke pass, not full acceptance: custom guide agent absent from isolated roster; Tavily and fallback branches untested. The routing rule and three static guards remain uncommitted.

- [Research-routing analysis](analysis/analyze-core.md) — standard `/sc:analyze` source-text pass, no `--depth`; includes current evidence, relevant history, prioritized instruction-boundary findings and verification guidance. Codegraph MCP/Auggie tools were unavailable to this worker; the guarded CLI index check was fresh, but analysis used Glob/Grep/Read as required for CLI-only access.
- [Accuracy check](accuracy-check.md) — claim-by-claim evidence and merged-PR relevance. All 95 scout candidate rows were screened; 83 follow the exact issue-creation timestamp, while 12 are earlier that same day. No post-creation research-agent or research/explain/MCP-reference fix was found in the checked default-branch history.

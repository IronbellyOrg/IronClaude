# Diff Analysis: P3 codegraph access-model decision comparison

## Metadata
- Generated: 2026-10-29T17:55:00Z
- Variants compared: 3 (Variant A = `option-a.md` MCP-first; Variant B = `option-b.md` CLI-first with artifacts; Variant C = `option-c.md` hybrid)
- Copies: `variant-1-original.md` (A), `variant-2-original.md` (B), `variant-3-original.md` (C)
- Ground truth: `context.md` (CTX), `research/codegraph-evaluation.md` (EVAL §n), `brainstorm/P3-codegraph-opportunities/merged-requirements.md` (BR). Anything none of them measured is UNVERIFIED.
- Total differences found: 26 debatable points (structural 3, content 12, contradictions 5, shared assumptions promoted 6) plus 8 unique contributions
- Categories: structural (3), content (12), contradictions (5), unique (8), shared assumptions (6 promoted, 2 stated)
- Taxonomy (auto-tagged, L3 > L2 > L1): L1 = S-001..S-003; L2 = C-001, C-002, C-003, C-008, C-009, C-010, C-011, C-012, X-002, X-003, X-005, A-003, A-005, A-006; L3 = C-004, C-005, C-006, C-007, X-001, X-004, A-001, A-002, A-004

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section shape | H1 + Proposal / Strengths / Weaknesses (H2), 25 lines | Same three H2 sections plus a "Source:" line naming BR §2.1, FR-04, FR-11, D-28; 27 lines | Same three H2 sections, 24 lines | Low |
| S-002 | Self-critique depth | 4 proposal-level weaknesses | 6 weaknesses (latency, freshness, undocumented flags, allowlist matching, lost follow-up, change size) | 3 weaknesses | Low |
| S-003 | Citation style | Cites EVAL §3, §4 through CTX only | Cites BR IDs plus INV-001 | Cites INV-001 and CTX only | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | Path for main session and unrestricted-Bash orchestrators | MCP for every lookup | CLI through Bash (`codegraph query --json`, `callers`, `callees`, `impact`, `status`, `files`) | MCP for symbol, caller and impact lookups | Medium |
| C-002 | Closed-Bash orchestrators (pr-submit, auggie-review, cleanup-audit) | MCP; add exactly `Bash(codegraph affected *)` where `affected` is needed | One `Bash(codegraph <sub> *)` pattern per read subcommand in each | MCP; exact read subcommands only (affected, status) | Medium |
| C-003 | CLI verb scope | `affected --stdin`, `init` (user-typed only) | `query`, `callers`, `callees`, `impact`, `affected`, `status`, `files` | `affected`, `status` (scripts and new commands' file outputs), `init` (one user-typed command) | Medium |
| C-004 | Mutation-exclusion guard (grep test forbidding `init|index|sync|uninit|install|uninstall|upgrade|unlock|telemetry on/off`) | None stated, although A keeps CLI `affected` and `init` | Yes, over every primitive | Yes, over every primitive | High |
| C-005 | Readiness, freshness and worktree-provenance check | None; "nested-worktree answers come with a warning that must be read from tool output" is listed as a weakness | `codegraph status` once per run, labels `fresh|stale|not_initialized|foreign_index|absent`; stale = leads only | One check per run (`codegraph_status`, else CLI `status`); stale or foreign-index = leads only | High |
| C-006 | Behaviour when Phase 2 does not add `CODEGRAPH_MCP_TOOLS` | Unstated ("without it only explore is listed") | Not applicable (no dependency) | Fall back to Grep/Read exactly like "codegraph absent" | Medium |
| C-007 | Behaviour when codegraph or the index is missing | Unstated | `absent` / `not_initialized` labels | Grep/Read fallback plus labels | Medium |
| C-008 | Artifacts in agent briefs | None | All agent graph data arrives as artifact paths | Artifacts where the brief already works that way (troubleshoot producers, reflect hunks) | Medium |
| C-009 | Agent follow-up graph questions | Yes (MCP names in `tools:`) | No (everything precomputed) | Yes (MCP names in `tools:`) | Medium |
| C-010 | Deferral rule for MCP | None needed | MCP stage deferred until schema overhead measured and serial CLI calls exceed about 100 per run | None needed | Low |
| C-011 | Latency | 3-15 ms per call after 220 ms init (EVAL §5.6) | 290-300 ms per call (EVAL §5.5) | MCP latency for lookups; CLI only for CLI-only jobs | Medium |
| C-012 | Phase 3 change size | Name swap per primitive plus one roster-test edit | Probe, parsers, golden fixtures, artifacts, allowlists | Name swap plus readiness check plus reuse of existing artifact patterns | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | Read-only agents' `tools:` lines | Add codegraph MCP names (troubleshoot-analyst, reflect-reviewer: search, node, callers, impact; reuse-auditor: search, node, callers; auggie-reviewer: node, callers, callees) | No codegraph tools at all (BR FR-11: "In v1 no `tools:` line of a read-only agent gains `mcp__codegraph__*`") | Add matching MCP names to agents that already carried Serena symbol tools | High |
| X-002 | `CODEGRAPH_MCP_TOOLS` in Phase 2 | Add the full 8-tool list | Do not set it in v1 (BR D-28) | Add the full 8-tool list | High |
| X-003 | `codegraph_explore` use | Allowed for "how does this area work" questions with `maxFiles` set | "No primitive names it" (BR FR-10, D-01, D-27) | Listed; no stated ban or allowance | Medium |
| X-004 | Where freshness comes from | "MCP connection keeps the daemon and watcher alive" is a strength of MCP-first | "Without an MCP client there is no watcher" is a weakness of CLI-first, yet BR §2.1 (line 69) says the daemon role is "installer-owned": the registered `alwaysLoad` server connects in sessions whichever path primitives use | Same claim as A ("removes most of INV-001 for interactive sessions") | Medium |
| X-005 | Intra-A: "no allowlist patterns to get wrong" vs its own `Bash(codegraph affected *)` and CLI `init` | Claims no patterns, adds one pattern and one mutating verb | n/a | n/a | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Exact per-agent MCP tool subsets for four read-only agents | High |
| U-002 | A | Exactly one Bash pattern, `Bash(codegraph affected *)`, and only in orchestrators that need `affected` | Medium |
| U-003 | A | Explore only with `maxFiles` set and never as a default step | Low |
| U-004 | B | Five-value state vocabulary `fresh|stale|not_initialized|foreign_index|absent` with "stale = leads only" | High |
| U-005 | B | Measured re-entry trigger for any MCP stage (schema overhead measured, >100 serial calls per run) | Medium |
| U-006 | B | One orchestrator call serves many agents; artifacts on disk are reviewable and reproducible | Medium |
| U-007 | C | Explicit degrade rule if the Phase 2 env line is missing: behave exactly as "codegraph absent" | High |
| U-008 | C | Readiness check over MCP (`codegraph_status`) with CLI fallback for sessions without MCP | Medium |

## Shared Assumptions

Agreement points scanned: all three keep Phase 2's `alwaysLoad` registration; all three keep `affected` and `init` CLI-only; all three treat MCP tools as read-only; all three assume some sessions have no MCP; all three keep `explore` listed.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|-----------------|------------|----------------|----------|
| A-001 | X-004, C-005 | Freshness differs by access path. Evidence says the daemon and watcher start when an MCP client is connected (EVAL §4, §5.7), and Phase 2 registers the server with `alwaysLoad` in every option; CLI reads saw the daemon's update (EVAL §5.7, `codegraph query cg_eval_probe_fn` found after the watcher indexed it) | UNSTATED (evidence partly contradicts it) | Yes |
| A-002 | X-003 | `codegraph_explore` must stay listed. An explicit `CODEGRAPH_MCP_TOOLS` that omits `explore` would block it (EVAL §3, `tools.ts:2926-2929`), removing the 24,913-character risk (EVAL §5.6); no variant considers this | UNSTATED | Yes |
| A-003 | C-002 | Closed-Bash orchestrators can call MCP tools without editing their `allowed-tools`, because `mcp__codegraph__*` is pre-approved through IronClaude's settings handling (EVAL §7 step 6). Whether a skill's `allowed-tools` restricts other tools is UNVERIFIED | UNSTATED | Yes |
| A-004 | C-005, B weaknesses, A weaknesses | Which sessions lack an MCP client (headless `claude -p`, sprint runs, background subagents) is never enumerated; only background subagents are documented (`sc-cleanup-audit-protocol/SKILL.md:86`) | UNSTATED | Yes |
| A-005 | X-001, C-012 | The roster-test edit is a cost of A/C. Phase 1 removes `mcp__serena__*` from the same `tools:` lines, so `tests/troubleshoot/test_diagnostic_worker_contract.py:17-26` changes in Phase 1 under every option | UNSTATED | Yes |
| A-006 | C-011, A strengths | MCP is "structured". Its inputs are documented parameters (EVAL §3), but outputs are Markdown text ("**Callers of install_codebase_memory_mcp (5 found)**", EVAL §5.6), so output parsing is text in both paths | UNSTATED | Yes |
| A-007 | C-003 | Per-worktree `init` is user-typed only and has no automatic owner (EVAL §4; BR B2) | STATED (A, C) | No |
| A-008 | A strengths, C-001 | All 8 MCP tools are read-only (`readOnlyHint: true`, EVAL §3) | STATED (A, CTX) | No |

Promoted points:

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-001 | Freshness is a property of the access path | Decides whether criterion 1 separates the options at all | Open for debate |
| A-002 | Explore must stay listed | Changes token risk of the env line | Open for debate |
| A-003 | MCP needs no allowlist edits in closed-Bash orchestrators | Changes the safety and size count for A/C | Open for debate |
| A-004 | The no-MCP session set is known | Decides how much fallback A needs | Open for debate |
| A-005 | Roster-test edit is option-specific | Changes A/C change-size count | Open for debate |
| A-006 | MCP output is structured | Weakens one A strength | Open for debate |

## Summary
- Total structural differences: 3
- Total content differences: 12
- Total contradictions: 5
- Total unique contributions: 8
- Total shared assumptions surfaced: 8 (UNSTATED: 6, STATED: 2, CONTRADICTED: 0; A-001 is UNSTATED with partly contradicting evidence)
- Highest-severity items: C-004, C-005, X-001, X-002
- Similarity check: 26 debatable points across 3 short variants; well above the 10% threshold; debate proceeds.

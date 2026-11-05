# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

The fault-finder was an independent agent that did not advocate for any variant. It probed the post-Round-2 consensus ("amended C", items 1-9 in its brief) across the 6 categories. Before recording them, the orchestrator re-read the repo citations in INV-005, INV-006 and INV-007:
- `agents/auggie-reviewer.md:5` contains `Bash` plus `mcp__serena__find_symbol` and `find_referencing_symbols`.
- `agents/troubleshoot-analyst.md:5` and `agents/reflect-reviewer.md:5` carry 4 Serena tools, including `get_diagnostics_for_file`.
- `agents/reuse-auditor.md:5` carries `find_symbol`, `get_symbols_overview` and `find_referencing_symbols`.
- `allowed-tools` in `skills/sc-troubleshoot-protocol/SKILL.md:4` and `skills/sc-reflect-protocol/SKILL.md:5` list exact MCP names.
- `sc-implement-protocol/SKILL.md:4` and `sc-workflow-protocol/SKILL.md:4` list none.
- Reflect's snapshot is `<output>/_review-snapshot` (`sc-reflect-protocol/SKILL.md:283-288`).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Amended C alone gives every primitive class working codegraph access | UNADDRESSED | MEDIUM | A working call needs every gate to pass: registration, env list, listing, permission rule, `tools:`, `allowed-tools`, foreground availability, an initialized index, provenance and version. Sibling worktrees read "not initialized" until a user-typed `init` (EVAL §5.8; BR B2). Markdown is not indexed (EVAL §5.4) |
| INV-002 | guard_conditions | The readiness/provenance check can run over MCP alone in closed-Bash orchestrators | UNADDRESSED | HIGH | FR-03 and NFR-09 compare `codegraph --version` with the pin. The server version appears only in `serverInfo` (EVAL §5.6), which the model does not see. C Round 2 point 7 gives those orchestrators only `affected`. Whether `codegraph_status` prints the version is UNVERIFIED |
| INV-003 | guard_conditions | Agents that call MCP directly inherit the orchestrator's per-run readiness state | UNADDRESSED | HIGH | Subagents do not see server instructions (EVAL §3). FR-01, FR-05, FR-07 and `projectPath` live in the orchestrator, and nothing passes `index_state`, `worktree_root` or `projectPath` into agent briefs |
| INV-004 | interaction_effects | "Worktree root realpath" names one directory | UNADDRESSED | MEDIUM | The reflect `--isolate-reviewers` snapshot at `<output>/_review-snapshot` (`sc-reflect-protocol/SKILL.md:283-288`) and agents isolated in nested `.claude/worktrees/` both resolve to the parent `.codegraph/` (EVAL §3, §4) |
| INV-005 | guard_conditions | Only closed-Bash orchestrators need exact MCP names in `allowed-tools` | UNADDRESSED | MEDIUM | troubleshoot (`SKILL.md:4`) and reflect (`SKILL.md:5`) list exact MCP names; implement and workflow (`:4`) have `allowed-tools` with none. Whether `allowed-tools` restricts tools is UNVERIFIED (A-003) |
| INV-006 | count_divergence | auggie-reviewer is read-only, and node, callers, callees is a 1:1 replacement | UNADDRESSED | MEDIUM | `agents/auggie-reviewer.md:5` has Bash. Its Serena tools are `find_symbol` and `find_referencing_symbols`. The `find_symbol` equivalent is search plus node (EVAL §6.2), so the subset drops search and adds callees. FR-23 checks only primitive text |
| INV-007 | count_divergence | search, node, callers, impact covers the 4 Serena tools of troubleshoot-analyst and reflect-reviewer | UNADDRESSED | MEDIUM | `get_diagnostics_for_file` has no equivalent (EVAL §6.2); impact is new. `get_symbols_overview` maps to node `symbolsOnly` only if N-002 passes. The roster test pins an exact set (`tests/troubleshoot/test_diagnostic_worker_contract.py:17-26`) |
| INV-008 | count_divergence | B's five states plus "absent" cover every case | UNADDRESSED | MEDIUM | K-1 has 7 `index_state` values (adds `disabled`, `error`), `graph:unlisted` (FR-02) and `access: cli\|none`. FR-11, D-08, D-28, the §2.1 MCP-stage row and "not listed in v1" all contradict amended C |
| INV-009 | guard_conditions | "Measure NFR-06 first" is a usable gate | UNADDRESSED | MEDIUM | It has no threshold and no failure branch. If the measurement fails, item 7 sends every lookup to Grep/Read, and the CLI lookup path (B) is not built |
| INV-010 | interaction_effects | The seven env-listed tools are always loaded, and blocking explore is harmless | UNADDRESSED | MEDIUM | Only explore carries a per-tool always-load flag (EVAL §3). Whether server-level `alwaysLoad` stops deferral of the other seven is UNVERIFIED (`docs/README.md:459` via EVAL §3), and so is whether the server instructions steer the model toward the blocked explore. FR-21 wording becomes false |
| INV-011 | guard_conditions | One smoke test settles foreground-agent MCP access (OQ-9) | UNADDRESSED | HIGH | `sc-cleanup-audit-protocol/SKILL.md:86` says MCP is unavailable to background subagents. The actual spawn mode, permission scope outside IronClaude (EVAL §7 step 6), headless children and Claude Code version drift are all UNVERIFIED |
| INV-012 | state_variables | Headless runs have no MCP | UNADDRESSED | MEDIUM | Never measured. A-004 was rejected, and user-scope `alwaysLoad` servers may load in `claude -p` |
| INV-013 | state_variables | One readiness check per run is enough after in-run writes | ADDRESSED | LOW | B Round 2 carries FR-03..FR-08, including the FR-05 re-check, over whole. The watcher debounce is 2000 ms (EVAL §4). The MCP banner form is UNVERIFIED |
| INV-014 | count_divergence | The CLI is limited to 3-4 verbs | UNADDRESSED | MEDIUM | The probe and FR-22 need `--version` and `telemetry status`, and the resolver needs `query --json` (N-001), so the real count is 6. The resolver script runs only in unrestricted-Bash orchestrators until E-3 (FR-04) |
| INV-015 | interaction_effects | codegraph is the only call-graph MCP server | UNADDRESSED | LOW | codebase-memory instructions say "Graph first: search_graph… trace_path…". The FR-21 routing block does not name it |

## Summary

- **Total findings**: 15
- **ADDRESSED**: 1
- **UNADDRESSED**: 14
  - HIGH: 3 (INV-002, INV-003, INV-011)
  - MEDIUM: 10 (INV-001, INV-004, INV-005, INV-006, INV-007, INV-008, INV-009, INV-010, INV-012, INV-014)
  - LOW: 1 (INV-015)

## Invariant Probe Gate

CONVERGENCE BLOCKED: 3 HIGH-severity UNADDRESSED invariants detected.
Blocking items: INV-002, INV-003, INV-011.
At depth standard no Round 3 runs. All three are carried as accepted risks, and each gets an explicit closure rule in the merged recommendation (refactor-plan Changes #9, #10 and #11). The 10 MEDIUM items are warnings, also closed by named changes. LOW items: no action is required; INV-015 is still noted in the merged document.

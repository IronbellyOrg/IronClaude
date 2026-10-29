# Refactoring Plan: Merge into Base (Variant 1, option A)

## Overview
- Base: Variant 1 (option A, byte proxy over stdio; advocate default:analyzer)
- Incorporating strengths from: Variant 2 (option B), Variant 3 (option C), and rules agreed in the debate
- Planned changes: 10
- Risk level: Medium (overall)

## Planned Changes

Cite Phase 2 spec locations by section or task name (§2.4, T2, §4.2 layer 2, §7), not by line number: the spec is being edited in parallel and its line numbers move.

### Change 1: Self-contained Leg A with exact measurements (base, restructured)
- **Source**: Base Method; debate C-001, C-007, N-003, A-003
- **Target**: Base Method (restructure into numbered steps "Leg A")
- **Rationale**: C-001 unanimous (bytes always measured); C-007 majority (instructions from a real 7-tool run, because the instructions text says "There is a single tool, `codegraph_explore`" and may change); N-003 majority (full objects are the upper bound).
- **Integration point**: Leg A runs in a `mktemp -d` dir with sandbox HOME and `CLAUDE_CONFIG_DIR`, telemetry and update checks off, the verified and extracted pinned v1.6.2 binary, and a tiny `git init` repo. Run 1: `CODEGRAPH_MCP_TOOLS` unset. Run 2: exactly `node,search,callers,callees,impact,files,status`. Per run record: bytes of `JSON.stringify(tools/list .result.tools)` (full objects), model-facing bytes (`"mcp__codegraph__"+name`, `description`, `inputSchema`), bytes of `initialize .result.instructions`, and per-tool bytes. `D = (full tools bytes + instructions bytes)(run 2) - (same)(run 1)`. Also record `D - bytes(codegraph_node)` as data only.
- **Risk**: Low (refines the base method).

### Change 2: X-25 assertions become a hard stop (base, modified)
- **Source**: Base Method; debate C-004 (unanimous), N-006
- **Target**: Base Method, new step after the two runs
- **Rationale**: The spec's §2.4 makes T2 step 0 part of the X-25 proof; the `status` branch also relies on an explicit list hiding explore, so a failed assertion cannot fall back to `status`.
- **Integration point**: Run 2's tool-name set equals exactly the seven `codegraph_*` names (so it has `codegraph_callers` and `codegraph_status` and no `codegraph_explore`), and `tools/call codegraph_explore` in run 2 returns a JSON-RPC error or a result with `isError: true`. Any failure: stop, select no value, log a mid-level decision (§7).
- **Risk**: Low.

### Change 3: Three bands replace the single 6,000 B cut-off (base, modified)
- **Source**: Debate C-002 (unanimous structure), N-001, N-002, N-007, A-001 (rejected by all)
- **Target**: Base Method pass rule
- **Rationale**: The measured delta (+7,004 to 7,488 B, `diff-analysis.md` orchestrator evidence) is 1,751 to 2,496 tokens depending only on the bytes-per-token rate, so a single cut-off lets an unmeasured constant decide.
- **Integration point**: `D <= 6,000 B` PASS (under 2,000 tokens even at 3 B/token): `MCP_TOOLS` = the seven tools, Leg B not run. `D > 8,000 B` FAIL (over 2,000 tokens even at 4 B/token): `MCP_TOOLS = "status"`, Leg B not run. `6,000 B < D <= 8,000 B` UNDECIDED: Leg B decides (Change 6).
- **Risk**: Medium (new rule; constants are proposals).

### Change 4: Leg B session measurement inside the band (from Variant 2)
- **Source**: Variant 2 Method; U-002, U-003; debate C-003, N-004
- **Target**: Base, new section "Leg B"
- **Rationale**: C-001 and C-005 unanimous: the real token count decides inside the band; C-003 majority: real login with the `.mcpServers` hash guard (the spec already accepts that live sessions rewrite the rest of `~/.claude.json`).
- **Integration point**: Two config files in a private `mktemp -d`, identical except that arm 2 adds `CODEGRAPH_MCP_TOOLS`; each registers only codegraph (realpath of the extracted binary, `args ["serve","--mcp"]`, `alwaysLoad: true`, telemetry and update-check env off). Hash `jq -S '.mcpServers' ~/.claude.json` before and after all Leg B runs; a mismatch is a stop. Precondition: `claude --version` succeeds within 10 s, else "not run (no claude)". Run from the Leg A repo dir, in ABAB order (default, 7-tool, default, 7-tool), each with `timeout 120`: `claude -p "reply ok" --output-format stream-json --verbose --strict-mcp-config --mcp-config <cfg> --no-session-persistence --model <one alias, same for every run>`. A run that exits non-zero or times out makes Leg B "not run (<reason>)". Tokens per run = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` from the final result event. `T = max(7-tool runs) - min(default runs)`. The stream-json event and field names are UNVERIFIED; the guards in Change 5 fail closed if they differ.
- **Risk**: Medium (real HOME, network, UNVERIFIED fields).

### Change 5: Leg B validity guards, fail closed (merged rule)
- **Source**: Debate C-009, X-002, C-008, A-002; N-004, N-005
- **Target**: Base, Leg B section
- **Rationale**: V2's unguarded false pass if the tools are deferred (X-002); all three advocates require that a failed guard makes B invalid, never a pass.
- **Integration point**: B is valid only if all hold: (a) the init event of each 7-tool run lists all seven `mcp__codegraph__codegraph_*` names and not `mcp__codegraph__codegraph_explore`, and each default run lists `mcp__codegraph__codegraph_explore`; (b) `T >= D / 5`; (c) the two runs of each configuration agree within 50 tokens (one re-run of the whole ABAB set allowed); (d) the three usage fields are present and numeric. Record `Deferred: no|yes|unknown` from (a) and (b) (P3 §9.1 asks for it).
- **Risk**: Low (additive; fails closed).

### Change 6: Decision rule inside the band and the never-block rule (from Variant 3, repaired)
- **Source**: Variant 3 Method (never block, "not run" line); debate C-005, C-006, X-001
- **Target**: Base, new section "Decision"
- **Rationale**: C-005 unanimous: two-directional inside the band (V3's one-way rule cannot fire on the measured data, X-001); C-006: never block the unattended executor.
- **Integration point**: Valid B and `T <= 2,000`: PASS, seven tools. Valid B and `T > 2,000`: FAIL, `status`. B not run or invalid: `status` (the existing failure branch), the executor continues, and it logs a non-blocking human item containing the exact Leg B commands; if a person later gets a valid PASS, one commit changes `install_codegraph.MCP_TOOLS` and the spec literals back to the seven tools. Never PASS inside the band without a valid B.
- **Risk**: Medium (a missing login ships `status`).

### Change 7: Fixed evidence file shape (from Variant 3 U-004, extended)
- **Source**: Variant 3 Method; debate C-006, A-003; advocate proposals
- **Target**: Base, new section "Evidence"
- **Rationale**: The spec's T2 step 1 and test U2 read `Selected MCP_TOOLS: <value>` from `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md`.
- **Integration point**: One fact per line: `Bytes delta D:`, `Model-facing delta:`, `Instructions bytes run1/run2:`, `Per-tool bytes:`, `D without node (data only, P3-D1 owns any smaller list):`, `Band: pass|undecided|fail`, `Explore hidden: yes`, `Explore call blocked: yes`, `Session measurement: <per-run tokens, T> | not run (<reason>) | invalid (<guard>)`, `Deferred: no|yes|unknown`, `Decided by: A|B|default`, `Claude Code version:`, `Model:`, `INV-015: waived (<reason>)`, `Threshold status: proposed, not user-confirmed`, and last `Selected MCP_TOOLS: <value>`.
- **Risk**: Low.

### Change 8: Expected outcome on today's data (orchestrator evidence)
- **Source**: `diff-analysis.md` orchestrator evidence
- **Target**: Base, new section "Expected outcome"
- **Rationale**: Decision-changing fact: the W4 data predicts the undecided band, so the result depends on Leg B.
- **Integration point**: State: full-object delta +7,488 B, model-facing +7,004 B, instructions unchanged in the 8-tool run; seven-tool figures derived from the 8-tool run; so D is expected in the band and, without a valid Leg B, the value is `status`. The 2K threshold is "proposed, not measured"; the evidence file gives the user the real number to confirm or move it.
- **Risk**: Low.

### Change 9: INV-015 waiver (merged rule)
- **Source**: Advocate proposals (V2 item 3, V3 item 8)
- **Target**: Base, Leg B section
- **Rationale**: P3 §9.1 asked for the measurement in a session that also has codebase-memory registered. The delta is additive and the retire step removes the codebase-memory registration once codegraph is ready (spec §2.x retire step), so Leg B uses a codegraph-only config and records the waiver.
- **Integration point**: One sentence in Leg B and the `INV-015:` evidence line.
- **Risk**: Low.

### Change 10: Pros and Cons rewritten for the merged method
- **Source**: All three variants' Pros/Cons; debate concessions
- **Target**: Base Pros and Cons
- **Rationale**: Keep the base's honest error statement; add Leg B's cost and UNVERIFIED items.
- **Integration point**: Pros: deterministic Leg A in every case; X-25 proof; real tokens decide only where the constant would; never blocks. Cons: inside the band a missing login ships `status`; Leg B uses the real HOME and network; stream-json field names and server-level `alwaysLoad` under `--strict-mcp-config` are UNVERIFIED (guards fail closed); band edges and tolerances are proposals.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-003, C-006 | V2 as the sole method (session only, stop without auth) | Stops the unattended executor and cannot prove X-25 (V2 conceded; C-004 unanimous). |
| C-005, X-001 | V3's one-way rule (B may only turn a pass into a fail) | Cannot fire when A fails, which is the measured case (V3 conceded). |
| N-002 | V2's upper edge 10,000 B | Majority chose 8,000 B (2,000 tokens at 4 B/token). |
| N-001 | V3's lower edge 5,000 B | Majority chose 6,000 B (2,000 tokens at 3 B/token). |
| N-003 | V2's model-facing bytes as D | Majority chose full objects plus instructions as the upper bound; model-facing bytes are recorded beside it. |
| N-004 | V3's three runs per config with median and 200-token spread | Majority on two runs per config; 200 tokens is 10% of the threshold. |
| N-007 | V1's optional Leg B outside the band | Majority runs Leg B only inside the band, where it can change the outcome. |
| A-003 | Trying a smaller tool list (for example without `codegraph_node`) | P3-D1 owns the failure branch; F2 records `D without node` as data only. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Wrong D if byte basis mis-specified | Revert to base Method text |
| 2 | Low | Stop instead of fallback when X-25 fails | Revert to base assertions |
| 3 | Medium | Band constants mis-set | Revert to single 6,000 B cut-off |
| 4 | Medium | Leg B cannot run or reads wrong fields | Remove Leg B section (band then defaults to `status`) |
| 5 | Low | Guards too strict make B invalid | Relax a named guard |
| 6 | Medium | `status` shipped without a login | Remove Decision section |
| 7 | Low | Evidence line names drift from T2 step 1 parser | Keep only `Selected MCP_TOOLS:` |
| 8 | Low | Stale numbers if pin changes | Delete section |
| 9 | Low | Waiver disputed | Add codebase-memory to both configs |
| 10 | Low | None | Revert to base Pros/Cons |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-10-29T19:20:00Z

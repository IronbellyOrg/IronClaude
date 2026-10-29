# Merge Log: F2 schema-cost method

## Metadata

- Base: Variant 1 (`variant-1-original.md`, option A, byte proxy over stdio; advocate default:analyzer)
- Plan: `refactor-plan.md` (10 changes, auto-approved 2026-10-29T19:20:00Z)
- Executor: merge-executor agent
- Merged artifact: `.dev/codegraph-migration/decisions/F2-schema-cost-method/adversarial/F2-schema-cost-method-merged.md`
- Changes applied: 10 of 10
- Changes NOT made: all 8 rows of the plan's "Changes NOT Being Made" table respected (V2 as sole method; V3 one-way rule; 10,000 B upper edge; 5,000 B lower edge; model-facing bytes as D; three runs with median and 200-token spread; optional Leg B outside the band; trying a smaller tool list)
- Status: success
- Timestamp: 2026-10-29

## Changes Applied

### Change 1: Self-contained Leg A with exact measurements

- **Status**: Applied
- **Source**: Base Method; debate C-001, C-007, N-003, A-003
- **Target**: Merged opening purpose block and Section 1 (steps A1 to A8)
- **Before**: One Method paragraph: run a Node stdio client twice, record `JSON.stringify(tools/list .result.tools)` plus `initialize .result.instructions` bytes, delta = run2 - run1.
- **After**: Purpose block (two values, two legs, terms X-25, D, T) and numbered steps A1 to A8: `mktemp -d` sandbox with HOME and `CLAUDE_CONFIG_DIR`, telemetry and update checks off, verified pinned v1.6.2 binary, `git init` repo, run 1 env unset, run 2 exactly `node,search,callers,callees,impact,files,status`; per run full tools bytes, model-facing bytes, instructions bytes, per-tool bytes; D on full objects plus instructions; `D - bytes(codegraph_node)` as data only.
- **Provenance tag**: `Base (original, modified): ... merged per Change #1` (two tags: purpose block and Section 1)
- **Validation**: Every measurement named in the plan's integration point is present. Env key names come from the spec's §2.4 registration JSON; the checksum stop cites §0 and §7 human item 2 (both checked in the spec). Model-facing bytes defined as in `diff-analysis.md` (prefixed name, description, inputSchema).

### Change 2: X-25 assertions become a hard stop

- **Status**: Applied
- **Source**: Base Method; debate C-004, N-006
- **Target**: Section 2 (X1, X2)
- **Before**: "asserts `codegraph_explore` absent from run 2's list and that a `tools/call codegraph_explore` in run 2 returns an error (proves X-25)".
- **After**: X1 exact seven-name set (so `codegraph_callers` and `codegraph_status` present, no `codegraph_explore`); X2 JSON-RPC error or `isError: true`. Failure: stop, select no value, log a mid-level decision (§7), no fallback to `status`.
- **Provenance tag**: `Base (original, modified): ... merged per Change #2`
- **Validation**: "Select no value" is expressed as "write no `Selected MCP_TOOLS:` line", which makes T2 step 1's `test -n "$MT"` fail (checked in the spec's T2 step 1). The pointer to §4.2 layer 2 step 5b is quoted from §2.4.

### Change 3: Three bands replace the single 6,000 B cut-off

- **Status**: Applied
- **Source**: Debate C-002, N-001, N-002, N-007, A-001
- **Target**: Section 3
- **Before**: "pass when delta <= 6000 bytes" at 3 bytes per token.
- **After**: Table: pass `D <= 6,000 B` (seven tools, no Leg B); undecided `6,000 B < D <= 8,000 B` (Leg B decides); fail `D > 8,000 B` (`status`, no Leg B).
- **Provenance tag**: `Base (original, modified): ... merged per Change #3`
- **Validation**: Edges are inclusive and exclusive exactly as in the plan; the three bands cover every D with no overlap. Edges flagged as proposals in Section 10.

### Change 4: Leg B session measurement inside the band

- **Status**: Applied
- **Source**: Variant 2 Method; U-002, U-003; debate C-003, N-004
- **Target**: Section 4 (B1 to B6)
- **Before**: (not in base)
- **After**: B1 `timeout 10 claude --version` else `not run (no claude)`; B2 two configs in a private `mktemp -d`, codegraph only, realpath of the binary, `args ["serve","--mcp"]`, `alwaysLoad: true`, telemetry and update-check env off, arm 2 adds `CODEGRAPH_MCP_TOOLS`; B3 and B6 `.mcpServers` hash guard before and after all runs, mismatch is a stop; B4 ABAB order from the Leg A repo, `timeout 120`, the exact command from the plan, one model alias, non-zero exit or timeout makes Leg B `not run (<reason>)`; B5 token formula and `T = max(7-tool runs) - min(default runs)`. UNVERIFIED label on stream-json event and field names kept.
- **Provenance tag**: `Variant 2, Method ... merged per Change #4`
- **Validation**: Command flags copied verbatim from the plan. The config JSON adds `"type":"stdio"`, taken from the spec's §2.4 registration JSON (not a new field). On a failed run the executor still runs B6 before going to Section 6, so the hash guard covers every run.

### Change 5: Leg B validity guards, fail closed

- **Status**: Applied
- **Source**: Debate C-009, X-002, C-008, A-002; N-004, N-005
- **Target**: Section 5
- **Before**: (not in base)
- **After**: Guards (a) init-event inventory with all seven `mcp__codegraph__codegraph_*` names spelled out and explore absent, default runs list explore; (b) `T >= D / 5`; (c) two runs per configuration within 50 tokens, one re-run of the whole ABAB set; (d) three usage fields present and numeric. Failed guard makes B `invalid (<guard>)`, never a pass. `Deferred: no|yes|unknown` recorded.
- **Provenance tag**: `Merged rule agreed in debate ... merged per Change #5`
- **Validation**: Constants match N-004 and N-005. The plan says only "Record Deferred from (a) and (b)"; the exact mapping (no / yes / unknown) is this merge's reading and is listed as open item 14 in the merged file.

### Change 6: Decision rule inside the band and the never-block rule

- **Status**: Applied
- **Source**: Variant 3 Method; debate C-005, C-006, X-001
- **Target**: Section 6
- **Before**: (not in base; base had one pass rule)
- **After**: Five-row table (band x Leg B result to value and `Decided by`); rules: never PASS in the band without a valid B; never block, select `status`, continue, log a non-blocking human item with the exact Leg B commands, later one commit can revert to seven tools; `status` triggers the §2.4 failure branch; X-25 failure or hash mismatch is a stop.
- **Provenance tag**: `Variant 3, Method ... repaired ... merged per Change #6`
- **Validation**: Two-directional inside the band (fixes X-001). The plan does not name where the human item is logged; recorded as open item 15 rather than invented.

### Change 7: Fixed evidence file shape

- **Status**: Applied
- **Source**: Variant 3 Method (U-004); debate C-006, A-003; advocate proposals
- **Target**: Section 7
- **Before**: (not in base)
- **After**: Path `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md`; the 16 lines in the plan's order, last `Selected MCP_TOOLS: <value>`; note that explore lines are always `yes` in a written file; `not run (outside band)` wording for the session line.
- **Provenance tag**: `Variant 3, Method ... merged per Change #7`
- **Validation**: Line prefixes match the plan exactly; `Selected MCP_TOOLS: ` prefix matches the spec's T2 step 1 `sed -n 's/^Selected MCP_TOOLS: //p'` and test U2 reads the same file (both checked). What the version and model lines hold when Leg B did not run is not set by the plan; recorded as open item 16.

### Change 8: Expected outcome on today's data

- **Status**: Applied
- **Source**: `diff-analysis.md` orchestrator evidence
- **Target**: Section 8
- **Before**: (not in base)
- **After**: Table with 1,735 / 9,223 / +7,488 B (full objects), 1,610 / 8,614 / +7,004 B (model-facing), 6,786 / 6,786 / 0 B (instructions, 8-tool run); caveats (derived from the 8-tool run; instructions measured only with explore listed); token ranges at 3, 3.5 and 4 B/token; D expected in the undecided band, so without a valid Leg B the value is `status`; threshold "proposed, not measured".
- **Provenance tag**: `diff-analysis.md, "Orchestrator evidence" ... merged per Change #8`
- **Validation**: Every number copied from `diff-analysis.md`; no number computed by the merge.

### Change 9: INV-015 waiver

- **Status**: Applied
- **Source**: Advocate proposals (Variant 2 item 3, Variant 3 item 8)
- **Target**: Section 4, after B6, plus the `INV-015:` line in Section 7
- **Before**: (not in base)
- **After**: One sentence: P3 §9.1 asked for codebase-memory in the session; Leg B uses a codegraph-only config because the delta is additive and the retire step removes codebase-memory once codegraph is ready (§2.12); evidence records `INV-015: waived (<reason>)`.
- **Provenance tag**: `Merged rule from advocate proposals ... merged per Change #9`
- **Validation**: The plan wrote "spec §2.x retire step"; resolved to §2.12 ("Retiring Serena once codegraph is ready"), which the spec's preflight row describes as "the readiness-gated Serena and kind-B codebase-memory removal".

### Change 10: Pros and Cons rewritten for the merged method

- **Status**: Applied
- **Source**: All three variants' Pros and Cons; debate concessions
- **Target**: Section 9
- **Before**: Base Pros (deterministic and offline; same harness proves explore hidden and blocked; scriptable acceptance) and Cons (proxy, Claude Code may wrap or trim; 3 B/token heuristic may fail a list that would pass, dropping Phase 3 to `status`).
- **After**: Pros: deterministic Leg A always; X-25 proof with a stop; real tokens decide only in the band; never blocks; scriptable. Cons: missing login in the band ships `status` (base's honest false-fail statement kept); bytes still a proxy outside the band; Leg B real HOME and network; stream-json field names and server-level `alwaysLoad` under `--strict-mcp-config` UNVERIFIED with guards failing closed; band edges and tolerances are proposals.
- **Provenance tag**: `Base (original, modified): ... merged per Change #10`
- **Validation**: Every point in the plan's integration point appears; UNVERIFIED label kept on the same two items.

### Additional block: Open items (Section 10)

- **Status**: Applied (required by the task brief; collects items already in the plan and inputs)
- **Source**: Changes #3, #4, #5, #6, #8, #10; debate N-001 to N-007
- **Content**: 6 UNVERIFIED items, 7 proposal constants and rules (2,000-token threshold, 6,000 B, 8,000 B, 50-token tolerance with two runs and one re-run, `D / 5`, full-object basis, Leg B only in the band), and 3 points the plan leaves to the executor.
- **Validation**: Alternative values (5,000 B, 10,000 B, three runs with 200 tokens, D / 6) are cited as rejected proposals, never as rules.

## Post-Merge Validation

### Structural Integrity

- **Heading hierarchy**: PASS. One H1 (the required title), then H2 Sections 1 to 10 in numeric order. No H3 or deeper, so no level gaps. No leftover stub text (grep for `STUB` returns 0).
- **Section ordering**: PASS. Purpose, Leg A (1), X-25 stop (2), bands (3), Leg B (4, with the INV-015 waiver), guards (5), decision (6), evidence (7), expected outcome (8), Pros and Cons (9), open items (10). Each section only uses steps or terms defined in an earlier section, except forward pointers to Sections 5, 6 and 10, which are explicit.
- **Flow**: PASS. An executor can follow A1 to A8, then X1 and X2, then the band; outside the band it goes straight to Section 6; inside it runs B1 to B6, checks guards (a) to (d), then Section 6 and Section 7. Every exit path (`not run`, `invalid`, stop) names where to go next.
- **Provenance**: 12 `<!-- Source: ... -->` tags, one before every section and before the INV-015 block. Provenance header lines present at the top.
- **Style**: no em dashes or en dashes (grep returns none).

### Internal References

- **Total**: 86 references: 25 to Sections ("Section N", "Sections N to M", "Sections N and M"), 32 to steps (A1 to A8, B1 to B6, X1, X2), 9 to guards by letter, and 20 to Phase 2 spec locations and named tasks or tests (14 section signs: §0, §2.4, §2.12, §4.2 layer 2 step 5b, §7 and §7 human item 2; 6 task or test names: T2, T2 step 0, T2 step 1, U2).
- **Resolved**: 86. Every Section number is 1 to 10 and exists; every step label is defined in Sections 1, 2 or 4; guards (a) to (d) are defined in Section 5; every spec location was checked against `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md` by section or task name, never by line number.
- **Broken**: 0.
- **Not checked (external to Phase 2 spec, cited as the inputs cite them)**: P3 §9.1, P3-D1, INV-010, INV-015, X-25 as a review-finding label.

### Contradiction Re-Scan

- Constants stated once and used the same way everywhere: `6,000 B` (pass edge), `8,000 B` (fail edge), `2,000` tokens, `50 tokens`, `D / 5`, `timeout 10`, `timeout 120`. The seven-tool value `node,search,callers,callees,impact,files,status` appears 5 times, identical each time.
- The bands in Section 3 and the decision table in Section 6 agree on all five outcomes; Leg B is described as running only inside the band in Sections 3, 4, 6 and 10.
- Stop cases (X-25 failure, hash mismatch, checksum mismatch) are never also described as a fallback to `status`.
- Rejected values (5,000 B, 10,000 B, 200 tokens, D / 6) appear only in Section 10 as rejected proposals.
- **New contradictions introduced**: 0.

## Summary

All 10 planned changes were applied in order to Variant 1, and none of the 8 excluded approaches was introduced. The merged method keeps the base's sandboxed stdio harness and X-25 proof, adds three bands (6,000 B and 8,000 B), a guarded Leg B that decides only inside the band, a never-block decision rule, and the fixed evidence file ending with `Selected MCP_TOOLS: <value>`. Post-merge checks found no heading gaps, no broken references and no new contradictions.

Three points the plan does not fix were not invented; they are listed as open items 14 to 16 in the merged file: the `Deferred:` mapping, where the non-blocking human item is logged, and what the version and model evidence lines hold when Leg B did not run. On today's data the expected outcome is the undecided band, so the result depends on whether a valid Leg B runs.

Status: success.

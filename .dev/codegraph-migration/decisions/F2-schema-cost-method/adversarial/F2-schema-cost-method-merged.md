<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (option A, default:analyzer) -->
<!-- Merge date: 2026-10-29 -->

# F2 merged method: schema-cost check for CODEGRAPH_MCP_TOOLS (Phase 2, T2 step 0)

<!-- Source: Base (original, modified): Variant 1 opening line rewritten as a purpose statement so the method stands alone; facts from context.md and Phase 2 spec §2.4; merged per Change #1 -->
This method runs once, unattended, in Phase 2 task T2 step 0 (spec §2.4), before any registration code is written. It sets `install_codegraph.MCP_TOOLS` to one of two values:

- the seven tools `node,search,callers,callees,impact,files,status`, if listing them instead of the default `codegraph_explore` adds at most 2,000 tokens to every session;
- otherwise `status` (the P3-D1 failure branch, §2.4).

The 2,000-token threshold is proposed, not measured. The method has two legs. Leg A (Sections 1 to 3) always runs and needs no Claude login. Leg B (Sections 4 and 5) runs only when Leg A's byte delta falls in the undecided band. Section 6 turns the results into one value, and Section 7 records it.

Terms used below:

- **X-25**: the claim that an explicit `CODEGRAPH_MCP_TOOLS` list hides and blocks every tool it does not name (source-cited, never observed; §2.4).
- **D**: Leg A's byte delta (step A8).
- **T**: Leg B's token delta (step B5).

<!-- Source: Base (original, modified): Variant 1 Method restructured into numbered steps with exact measurements (full objects, model-facing bytes, instructions from a real 7-tool run, per-tool bytes, D without node); merged per Change #1 (debate C-001, C-007, N-003, A-003) -->
## 1. Leg A: byte measurement over stdio (always runs)

Leg A needs no Claude login and no network after the download, and it touches nothing outside its own temporary directory.

1. **A1. Sandbox.** Create `W=$(mktemp -d)` and `mkdir "$W/home"`. Run every Leg A command with `HOME="$W/home"` and `CLAUDE_CONFIG_DIR="$W/home"`, and with `CODEGRAPH_TELEMETRY=0` and `CODEGRAPH_NO_UPDATE_CHECK=1` (telemetry and update checks off, the same env keys as the §2.4 registration).
2. **A2. Pinned binary.** Download the pinned v1.6.2 tarball for this platform, verify it against the pinned checksum (§0) before extracting, and extract it under `$W`. Call the realpath of the extracted `codegraph` binary `CG`. A checksum mismatch is a stop (§7, human item 2).
3. **A3. Tiny repo.** `mkdir "$W/repo" && cd "$W/repo" && git init -q`. Both server runs start from this directory, and Leg B later runs from it too.
4. **A4. Client.** Write a small Node stdio client under `$W` that starts `"$CG" serve --mcp` as a child process, sends `initialize`, then `tools/list`, and saves both raw responses. In run 2 it also sends `tools/call` for `codegraph_explore` and saves that response (used by Section 2).
5. **A5. Run 1 (default).** Run the client with `CODEGRAPH_MCP_TOOLS` unset.
6. **A6. Run 2 (seven tools).** Run the client with `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status`, exactly this value.
7. **A7. Measure each run.** Record these UTF-8 byte counts for run 1 and run 2:
   - **full tools bytes**: `JSON.stringify(<tools/list response>.result.tools)`, the full tool objects;
   - **model-facing bytes**: the same list with each tool reduced to `"mcp__codegraph__" + name`, `description` and `inputSchema`;
   - **instructions bytes**: `<initialize response>.result.instructions`;
   - **per-tool bytes**: `JSON.stringify` of each tool object, by tool name.
8. **A8. Compute.**
   - `D = (full tools bytes + instructions bytes)(run 2) - (full tools bytes + instructions bytes)(run 1)`. D uses the full objects because they are the upper bound; the model-facing figure is recorded beside it.
   - Model-facing delta = model-facing bytes (run 2) minus model-facing bytes (run 1).
   - `D - bytes(codegraph_node)`, with run 2's per-tool bytes for `codegraph_node`. This is data only: no smaller tool list is tried here, because P3-D1 owns the failure branch.

The instructions bytes come from the real seven-tool run (A6), never from the default run, because the instructions text says "There is a single tool, `codegraph_explore`" and may change when explore is hidden.

<!-- Source: Base (original, modified): Variant 1 explore assertions ("absent from run 2's list", "tools/call codegraph_explore returns an error") made exact and turned into a hard stop with no fallback; merged per Change #2 (debate C-004, N-006) -->
## 2. X-25 check: a hard stop

Check both assertions on run 2 (A6) before applying any band:

1. **X1. Tool names.** Run 2's tool-name set equals exactly `codegraph_node`, `codegraph_search`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files` and `codegraph_status`. So it has `codegraph_callers` and `codegraph_status` and has no `codegraph_explore`.
2. **X2. Blocked call.** Run 2's `tools/call codegraph_explore` returns a JSON-RPC error, or a result with `isError: true`.

If either assertion fails: stop, select no value (write no `Selected MCP_TOOLS:` line, so T2 step 1's `test -n "$MT"` fails), and log a mid-level decision (§7). Do not fall back to `status`: the `status` value also relies on an explicit list hiding explore, so a failed X-25 check breaks both outcomes. §2.4 names this step, together with §4.2 layer 2 step 5b, as the X-25 proof.

<!-- Source: Base (original, modified): Variant 1's single "pass when delta <= 6000 bytes" rule replaced by three bands, because the measured delta straddles 2,000 tokens depending only on the bytes-per-token rate; merged per Change #3 (debate C-002, N-001, N-002, N-007, A-001) -->
## 3. Bands on D

| Band | Condition on D | Why this edge | Result |
|---|---|---|---|
| pass | `D <= 6,000 B` | under 2,000 tokens even at 3 B/token | `MCP_TOOLS` = the seven tools; Leg B is not run |
| undecided | `6,000 B < D <= 8,000 B` | between the two rates, so the rate would decide | Leg B decides (Sections 4 to 6) |
| fail | `D > 8,000 B` | over 2,000 tokens even at 4 B/token | `MCP_TOOLS = "status"`; Leg B is not run |

The real bytes-per-token rate is not known, so a single cut-off would let an unmeasured constant decide. Leg B runs only inside the undecided band, the one place where it can change the outcome. Both band edges are proposals (Section 10).

<!-- Source: Variant 2, Method (headless session runs with --strict-mcp-config and a codegraph-only config, U-003; token formula, U-002), extended with the .mcpServers hash guard, ABAB order, timeouts and the "not run" rule; merged per Change #4 (debate C-001, C-003, C-005, N-004) -->
## 4. Leg B: session measurement (undecided band only)

Run Leg B only when D is in the undecided band (Section 3). Leg B uses the executor's real Claude login, the real HOME and network to Anthropic. It never runs `claude mcp add` or `claude mcp remove`, and `--strict-mcp-config` keeps every user MCP server out of the session. The spec already accepts that live sessions rewrite the rest of `~/.claude.json`; the hash guard (B3, B6) protects `.mcpServers`.

1. **B1. Precondition.** `timeout 10 claude --version` must succeed. If it fails or times out, Leg B is `not run (no claude)`: skip to Section 6. Otherwise keep the printed version for the evidence file.
2. **B2. Config files.** Create a private directory `P=$(mktemp -d)`. Write two config files that are identical except that arm 2 adds `CODEGRAPH_MCP_TOOLS`. Each registers only codegraph, with `CG` from A2 (the realpath of the extracted binary). `$P/default.json`:
   ```json
   {"mcpServers":{"codegraph":{"type":"stdio","command":"<CG>","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1"}}}}
   ```
   `$P/seven.json` is the same file with `"CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,files,status"` added to `env`.
3. **B3. Hash before.** `H0=$(jq -S '.mcpServers' ~/.claude.json | sha256sum)`.
4. **B4. Four runs, ABAB order.** From `$W/repo` (A3), run default, seven, default, seven, in that order. Pick one model alias and use the same alias for every run. Each run:
   ```bash
   timeout 120 claude -p "reply ok" --output-format stream-json --verbose --strict-mcp-config --mcp-config "$P/<arm>.json" --no-session-persistence --model <alias> > "$P/run<N>-<arm>.jsonl"
   ```
   A run that exits non-zero or times out makes Leg B `not run (<reason>)`: do B6, then go to Section 6.
5. **B5. Tokens and T.** For each run, tokens = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` from the final result event. Then `T = max(seven-tool runs) - min(default runs)`.
6. **B6. Hash after.** After all Leg B runs, including any re-run allowed by guard (c) in Section 5, compute `H1` the same way as `H0`. If `H1` differs from `H0`, stop: the real registrations changed. Write no `Selected MCP_TOOLS:` line and do not continue.

The stream-json event and field names are UNVERIFIED; the guards in Section 5 fail closed if they differ.

<!-- Source: Merged rule from advocate proposals (Variant 2 item 3, Variant 3 item 8); merged per Change #9 -->
**INV-015 waiver.** P3 §9.1 asked for this measurement in a session that also has codebase-memory registered (INV-015), but Leg B uses a codegraph-only config because the delta is additive and the retire step removes the codebase-memory registration once codegraph is ready (§2.12), so the evidence file records `INV-015: waived (<reason>)`.

<!-- Source: Merged rule agreed in debate (C-009, X-002, C-008, A-002, N-004, N-005); no single variant contained it; merged per Change #5 -->
## 5. Leg B validity guards (fail closed)

Leg B is valid only if all four guards hold. A failed guard makes Leg B `invalid (<guard>)`, never a pass. This closes the false pass Variant 2 had if the tools were deferred behind tool search (X-002).

- **(a) Tool inventory.** The init event of each seven-tool run lists all seven names (`mcp__codegraph__codegraph_node`, `mcp__codegraph__codegraph_search`, `mcp__codegraph__codegraph_callers`, `mcp__codegraph__codegraph_callees`, `mcp__codegraph__codegraph_impact`, `mcp__codegraph__codegraph_files`, `mcp__codegraph__codegraph_status`) and does not list `mcp__codegraph__codegraph_explore`. The init event of each default run lists `mcp__codegraph__codegraph_explore`.
- **(b) Floor.** `T >= D / 5`.
- **(c) Repeatability.** The two runs of each configuration agree within 50 tokens. If they do not, re-run the whole ABAB set once (B4 and B5) and use the re-run set; if it still fails, Leg B is invalid.
- **(d) Fields.** The three token fields are present and numeric in the final result event of every run.

Record `Deferred: no|yes|unknown` from guards (a) and (b), because P3 §9.1 asks for it: `no` when (a) and (b) both hold, `yes` when (a) or (b) fails, `unknown` when Leg B was not run or stopped on (c) or (d) before (a) and (b) could be read.

<!-- Source: Variant 3, Method (never block the executor; "session measurement: not run"), repaired so the session measurement decides in both directions inside the band; merged per Change #6 (debate C-005, C-006, X-001) -->
## 6. Decision rule

| Band (Section 3) | Leg B (Sections 4 and 5) | `Selected MCP_TOOLS` | `Decided by` |
|---|---|---|---|
| pass | not run (outside band) | `node,search,callers,callees,impact,files,status` | A |
| fail | not run (outside band) | `status` | A |
| undecided | valid and `T <= 2,000` | `node,search,callers,callees,impact,files,status` | B |
| undecided | valid and `T > 2,000` | `status` | B |
| undecided | not run or invalid | `status` | default |

Rules:

1. Never PASS inside the undecided band without a valid Leg B.
2. Never block. When Leg B is not run or invalid, the executor selects `status` (the existing failure branch), continues T2, and logs a non-blocking human item that contains the exact Leg B commands (B1 to B6). If a person later gets a valid Leg B with `T <= 2,000`, one commit changes `install_codegraph.MCP_TOOLS` and the spec literals back to the seven tools.
3. When the value is `status`, the §2.4 failure branch applies as written there.
4. A failed X-25 check (Section 2) or a hash mismatch (B6) is a stop, not a decision: no value is selected.

<!-- Source: Variant 3, Method (mandatory "session measurement: not run" line, U-004), extended to a fixed one-fact-per-line list; merged per Change #7 (debate C-006, A-003; advocate proposals) -->
## 7. Evidence file

Write `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md`. T2 step 1 and test U2 read the value from its `Selected MCP_TOOLS:` line, so that line comes last and uses exactly this prefix. One fact per line, in this order:

```text
Bytes delta D: <bytes>
Model-facing delta: <bytes>
Instructions bytes run1/run2: <bytes>/<bytes>
Per-tool bytes: <tool name>=<bytes>, ... (every tool seen in either run)
D without node (data only, P3-D1 owns any smaller list): <bytes>
Band: pass|undecided|fail
Explore hidden: yes
Explore call blocked: yes
Session measurement: <per-run tokens, T> | not run (<reason>) | invalid (<guard>)
Deferred: no|yes|unknown
Decided by: A|B|default
Claude Code version: <output of claude --version>
Model: <alias used in B4>
INV-015: waived (<reason>)
Threshold status: proposed, not user-confirmed
Selected MCP_TOOLS: <value>
```

`Explore hidden` and `Explore call blocked` are always `yes` in a written file, because a failed X-25 check is a stop (Section 2). When D is outside the undecided band, the session line reads `Session measurement: not run (outside band)`.

<!-- Source: diff-analysis.md, "Orchestrator evidence" (W4 sandbox tools/list and initialize responses of the pinned v1.6.2 server, measured as UTF-8 bytes); merged per Change #8 -->
## 8. Expected outcome on today's data

The W4 sandbox kept the raw responses of the pinned v1.6.2 server with the env unset and with an 8-tool list that also named explore. Measured from those files:

| Quantity | Default (explore only) | Seven tools | Delta |
|---|---|---|---|
| Full tool objects | 1,735 B | 9,223 B | +7,488 B |
| Model-facing fields only | 1,610 B | 8,614 B | +7,004 B |
| Instructions | 6,786 B | 6,786 B (8-tool run) | 0 B in that run |

The seven-tool figures are derived from the 8-tool run minus `codegraph_explore`, and the instructions were measured only in runs that list explore. So D is expected near +7,488 B, inside the undecided band (Section 3). At 3, 3.5 and 4 bytes per token, +7,004 to +7,488 B is 2,335 to 2,496, 2,001 to 2,139, and 1,751 to 1,872 tokens, so the bytes alone cannot decide. The result therefore depends on Leg B: a valid Leg B decides by T, and without one the value is `status`.

The 2,000-token threshold is proposed, not measured. The evidence file gives the user the real number to confirm the threshold or move it.

<!-- Source: Base (original, modified): Variant 1 Pros and Cons rewritten for the merged method, keeping the base's honest error statement and adding Leg B's cost and UNVERIFIED items from Variants 2 and 3 and the debate concessions; merged per Change #10 -->
## 9. Pros and Cons

Pros:

- Leg A is deterministic, offline after the download, needs no login and costs nothing, and it runs in every case under a sandbox HOME.
- The same harness proves X-25 (explore hidden and blocked), and a failed proof stops instead of shipping a value.
- Real session tokens decide only where the bytes-per-token constant would otherwise decide (the undecided band).
- It never blocks the unattended executor: a missing login or an invalid Leg B ships `status` and leaves a human item.
- Acceptance is fully scriptable (`jq` and `node` assertions, fixed evidence lines).

Cons:

- Inside the band, a missing login ships `status`. That may be a false fail, which drops Phase 3 to the `status`-only branch until a person runs Leg B.
- Outside the band the bytes are still a proxy: Claude Code may wrap or trim schemas, so the real context cost can differ from the bytes.
- Leg B uses the real HOME and network to Anthropic; sessions rewrite parts of `~/.claude.json` outside `.mcpServers`.
- The stream-json field names and server-level `alwaysLoad` under `--strict-mcp-config` are UNVERIFIED; the guards fail closed.
- The band edges and tolerances are proposals.

<!-- Source: Collected from Changes #3, #4, #5, #6, #8 and #10 and from debate sub-points N-001 to N-007 (all flagged for review in debate-transcript.md) -->
## 10. Open items for user review

UNVERIFIED items:

1. The stream-json event and field names: the init event's tool list, the final result event, and the three token fields (Section 4, B5). Guards (a) and (d) fail closed.
2. Whether server-level `alwaysLoad: true` under `--strict-mcp-config` loads all seven listed tools in full (only `codegraph_explore` carries the per-tool flag; P3 INV-010 calls the server-level behaviour UNVERIFIED). Guards (a) and (b) fail closed.
3. Whether the unattended executor has a Claude login for Leg B. Without one, the undecided band ships `status` (Section 6).
4. X-25 itself, until Section 2 and §4.2 layer 2 step 5b run (§2.4).
5. The real tokenizer rate and any per-tool wrapping Claude Code adds (Section 8).
6. Whether the seven-tool schemas and the instructions change when explore is absent; today's figures are derived from the 8-tool run (Section 8).

Proposal constants and rules (majority or orchestrator choices, not user-confirmed):

7. The 2,000-token threshold itself: proposed, not measured.
8. Lower band edge `D <= 6,000 B` (N-001; Variant 3 proposed 5,000 B).
9. Upper band edge `D > 8,000 B` (N-002; Variant 2 proposed 10,000 B).
10. Repeat rule: two runs per configuration in ABAB order, agreement within 50 tokens, one re-run of the set (N-004; Variant 3 proposed three runs, median, spread within 200 tokens).
11. Validity floor `T >= D / 5` (N-005; Variant 3 proposed D / 6).
12. D measured on full tool objects plus instructions, with model-facing bytes recorded only (N-003).
13. Leg B runs only inside the undecided band (N-007).

Points the plan leaves to the executor:

14. The `Deferred:` mapping in Section 5 is this merge's reading of "from (a) and (b)".
15. The plan does not name where the non-blocking human item (Section 6, rule 2) is logged.
16. The plan does not say what the `Claude Code version:` and `Model:` evidence lines hold when Leg B did not run (Section 7).

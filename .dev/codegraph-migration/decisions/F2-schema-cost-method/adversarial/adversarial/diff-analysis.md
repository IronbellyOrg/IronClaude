# Diff Analysis: schema-cost measurement method comparison

## Metadata
- Generated: 2026-10-29T18:48:09Z
- Variants compared: 3 (V1 = option-a.md byte proxy; V2 = option-b.md real session tokens; V3 = option-c.md proxy gate plus session evidence)
- Total differences found: 19
- Categories: structural (1), content (9), contradictions (2), unique (4), shared assumptions (3 promoted)

## Orchestrator evidence (read-only, gathered before the debate)

The W4 sandbox still holds the raw `tools/list` and `initialize` responses of the pinned v1.6.2 server (`/tmp/codegraph-eval.fQfO/mcp-default.json`, env unset; `/tmp/codegraph-eval.fQfO/mcp-all.json`, `CODEGRAPH_MCP_TOOLS=explore,node,search,callers,callees,impact,files,status`; `research/codegraph-evaluation.md:205-216`). Measured with `jq -c … | wc -c` (UTF-8 bytes), no server started:

| Quantity | Default (explore only) | Seven tools (8-tool run minus `codegraph_explore`) | Delta |
|---|---|---|---|
| `tools/list .result.tools`, full objects (name, description, inputSchema, annotations) | 1,735 B | 9,223 B | **+7,488 B** |
| Model-facing fields only (`mcp__codegraph__` + name, description, inputSchema) | 1,610 B | 8,614 B | **+7,004 B** |
| `initialize .result.instructions` | 6,786 B | 6,786 B (8-tool run) | 0 B in that run |

Per tool (characters, full object): search 1,116; callers 1,080; callees 1,036; impact 1,012; node 2,864; status 712; files 1,373; explore 1,723.

What this means for the options:
- Option A's gate (pass when delta <= 6,000 B at 3 B/token) **fails** on this data by 1,000-1,500 B, so A (and C, whose gate is A) would set `MCP_TOOLS = "status"`.
- The real token delta is near the 2K line: 7,004-7,488 B is 2,335-2,496 tokens at 3 B/token, 2,001-2,139 at 3.5 B/token, 1,751-1,872 at 4 B/token. Which side of 2,000 it lands on depends on the real tokenizer and on any per-tool wrapping Claude Code adds. Both are UNVERIFIED.
- Caveats: the seven-tool figure is derived from the 8-tool run (assumes the other schemas do not change when explore is absent); the instructions were measured only in runs that list explore; the instructions text says "There is a single tool, `codegraph_explore`" (instructions line 17), so they may or may not change when explore is hidden.

## Structural Differences

| # | Area | V1 (A, byte proxy) | V2 (B, session tokens) | V3 (C, proxy gate + session evidence) | Severity |
|---|------|--------------------|------------------------|----------------------------------------|----------|
| S-001 | Document shape | H1, self-contained Method paragraph, Pros (3), Cons (2) | H1, self-contained Method paragraph, Pros (2), Cons (4) | H1, Method defined by reference to A and B plus a disagreement rule, Pros (3), Cons (3) | Low |

## Content Differences

| # | Topic | V1 (A) | V2 (B) | V3 (C) | Severity |
|---|-------|--------|--------|--------|----------|
| C-001 | Quantity measured | Bytes of `JSON.stringify(tools/list .result.tools)` plus `initialize .result.instructions`, run2 minus run1 | Reported session input tokens (input + cache creation + cache read), run2 minus run1 | A's bytes decide; B's tokens recorded when B can run | High |
| C-002 | Pass rule | delta <= 6,000 B (3 B/token, "conservative") | delta <= 2,000 tokens | A's rule decides; if B runs and exceeds 2,000 while A passed, B wins (value `status`) | High |
| C-003 | Environment and auth | Throwaway dir, sandbox HOME, offline after download, no login | Executor's real login and real HOME, network to Anthropic, `--strict-mcp-config` | A always; B only "when a logged-in `claude` is available" | High |
| C-004 | Proof that explore is hidden and blocked (X-25) | Same client asserts `codegraph_explore` absent from run 2 and `tools/call codegraph_explore` errors | Not covered ("needs the stdio client anyway") | Covered through A | Medium |
| C-005 | Rule when the two methods disagree | n/a (one method) | n/a (one method) | One-directional: B can turn A's pass into a fail; nothing can turn A's fail into a pass | High |
| C-006 | Behaviour when the method cannot run | Always runs | Unattended executor without auth stops (human item) | Never blocks; evidence says "session measurement: not run" | Medium |
| C-007 | Server instructions counted | Explicitly (instructions bytes added) | Implicitly (part of session context) | Through A | Low |
| C-008 | Noise and repeatability | Deterministic | Acknowledges "small run-to-run noise", no rule for it | Inherits B's noise when B runs, no rule | Medium |
| C-009 | Validity check on the measurement itself | None (bytes are exact) | None; whether `--strict-mcp-config` with `alwaysLoad` lists the tools is UNVERIFIED | None | Medium |

## Contradictions

| # | Point of Conflict | V1 (A) | V2 (B) | V3 (C) | Impact |
|---|-------------------|--------|--------|--------|--------|
| X-001 | Does C actually cross-check the heuristic? | Admits the 3 B/token rate "may fail a list that would pass a real measurement" | n/a | Pros claim "uses the real measurement whenever it is available, so the heuristic is cross-checked", but its rule lets B override only a pass. With the measured +7,004-7,488 B (orchestrator evidence) A fails, and C's cross-check can never fire in that case (intra-variant requirement-constraint conflict) | High |
| X-002 | Can B's number be trusted as "the real quantity"? | n/a | Pros: "Measures the real quantity the 2K threshold is about"; Cons: whether `--strict-mcp-config` with `alwaysLoad` lists the tools is UNVERIFIED. If the seven tools were deferred behind tool search in that config, B would measure a near-zero delta and pass falsely (intra-variant conflict, no guard) | Inherits the same gap when B runs | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Explicit conversion constant (3 B/token) and the instructions bytes added to the tools bytes | Medium |
| U-002 | V2 | Token accounting formula `input + cache creation + cache read` taken from the headless JSON result | Medium |
| U-003 | V2 | Isolation by `--strict-mcp-config --mcp-config <cfg>` with only codegraph registered, so every other server cancels out of the delta | High |
| U-004 | V3 | Two-method structure with an explicit disagreement rule and a mandatory "session measurement: not run" line in the evidence file | High |

## Shared Assumptions

Agreement points scanned: all three measure a delta between two runs of the same server (env unset vs the 7-tool key); all three keep the 2K-token threshold and the `status`-only failure branch; all three need the pinned, extracted v1.6.2 binary before registration code exists.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| (not promoted) | Pinned binary at T2 step 0 | The extracted v1.6.2 binary is available before registration code is written | STATED (V1 "verify and extract the pinned v1.6.2 tarball"; V2 "the extracted codegraph") | No |
| A-001 | Every variant has a single cut-off and no undecided band | The measured delta is far enough from 2K that the choice of method does not change the outcome | CONTRADICTED (orchestrator evidence: +7,004-7,488 B, 1,751-2,496 tokens depending on bytes per token) | Yes |
| A-002 | V1 and V2 both treat the listed tools as fully loaded | Server-level `alwaysLoad: true` makes all seven listed tools load in full; only `codegraph_explore` carries the per-tool `_meta.anthropic/alwaysLoad` flag (`research/codegraph-evaluation.md:85`); P3 invariant INV-010 calls server-level behaviour UNVERIFIED | UNSTATED | Yes |
| A-003 | All accept the binary outcome (7 tools or `status`) | No smaller list is tried when the 7-tool list fails, although `codegraph_node` alone is 2,864 of the 9,223 B | UNSTATED | Yes |

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Delta not near the threshold | Single cut-off in every variant | High: decides between 7 tools and `status` | CONTRADICTED, flagged for debate |
| A-002 | Server-level `alwaysLoad` loads every listed tool | Both measurement styles | High: if false, B under-measures and Phase 3 tools are deferred | Promoted |
| A-003 | Outcome is binary | Failure branch copied from P3-D1 | Medium: may be out of F2 scope (P3-D1 fixed the branch) | Promoted |

## Summary

- Total structural differences: 1
- Total content differences: 9
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 1, CONTRADICTED: 1); promoted: A-001, A-002, A-003
- Debatable points (convergence denominator S + C + X + A): 15
- Highest-severity items: C-001, C-002, C-003, C-005, X-001, X-002, U-003, U-004, A-001, A-002
- Similarity check: variants differ materially (15 debatable points of roughly 20 comparable items); debate not skipped.

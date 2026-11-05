# F2 recommendation: schema-cost measurement method (Phase 2, task T2 step 0)

- Decision: how Phase 2 measures whether listing 7 codegraph tools instead of `codegraph_explore` adds at most 2K tokens per session (context: `context.md`)
- Method: `/sc:adversarial --compare option-a.md,option-b.md,option-c.md --depth quick`
- Status: success (all 5 steps ran; post-merge validation PASS). Seven sub-point constants and 16 open items are flagged for user review.

## Winner

**Option A** (byte measurement over stdio, no Claude session) won as the base, but **not as written**. The merged method keeps A's harness as Leg A in every run and adds B's session measurement as Leg B, which decides only when the byte result is too close to call. It also takes C's rule that the executor never blocks.

Why A as written is not enough: the W4 sandbox still holds the pinned v1.6.2 `tools/list` responses. Measured from them, the 7-tool list adds +7,488 B (full tool objects) or +7,004 B (fields the model sees), and the server instructions are unchanged in the 8-tool run. Those bytes fail A's 6,000 B gate (3 bytes per token), so A, and also C (whose gate is A), would ship `status`. The same bytes are 1,751 to 2,496 tokens depending only on the unmeasured bytes-per-token rate, so the outcome sits right on the 2K line (`adversarial/adversarial/diff-analysis.md`, orchestrator evidence).

## Scores per option

| Option | Quantitative (50%) | Qualitative (50%, 30-criterion rubric, two passes) | Combined | Debate points won |
|---|---|---|---|---|
| A | 0.973 | 23/30 = 0.767 | **0.870** | 3 |
| C | 0.925 | 22/30 = 0.733 | **0.829** | 2 |
| B | 0.736 | 20/30 = 0.667 | **0.701** | 0 |

A and C are 0.041 apart, which is inside the 5% tie band. The level-1 tiebreaker (debate points won: A 3, C 2) selected A. The level-2 tiebreaker would agree (correctness: A 5/5, C 3/5). C lost points because its "cross-checked" claim is false on the measured data: its rule lets the session measurement overturn only a pass. B lost points because it stops an unattended executor that has no login, and it has no guard against a false pass if the tools are deferred.

## Convergence

100% (15 of 15 debated points), status CONVERGED, threshold 80%. Depth was quick, so the debate had one round and no invariant probe. All three advocates rejected the shared assumption that the delta is far from the threshold, and each one proposed the same three-band, two-leg structure on its own. The specific constants were settled by majority (sub-points N-001 to N-007 in `adversarial/adversarial/debate-transcript.md`).

## Changes the merge made to the winning method

1. **Leg A, exact measurement.** Two stdio runs in a `mktemp -d` dir with a sandbox HOME, the verified and extracted v1.6.2 binary, and a tiny `git init` repo. Run 1 has the env unset. Run 2 has exactly `node,search,callers,callees,impact,files,status`. `D` = the full `tools/list` objects bytes plus the instructions bytes, run 2 minus run 1. The model-facing delta, per-tool bytes and `D - bytes(codegraph_node)` are also recorded, as data only: P3-D1 owns any smaller list.
2. **X-25 proof (an explicit list hides and blocks every tool it does not name) is a hard stop.** Run 2's tool names must be exactly the seven, and a `tools/call codegraph_explore` must return a JSON-RPC error or `isError: true`. If either check fails, the executor stops, selects no value and logs a mid-level decision (§7). It does not fall back to `status`, because `status` also relies on the list hiding explore.
3. **Three bands replace the single cut-off.** `D <= 6,000 B` passes (seven tools). `D > 8,000 B` fails (`status`). `6,000 B < D <= 8,000 B` is undecided and Leg B decides. The edges are 2,000 tokens at 3 and at 4 bytes per token.
4. **Leg B, undecided band only.**
   - **Precondition:** `timeout 10 claude --version` must succeed.
   - **Configs:** two codegraph-only config files with `alwaysLoad: true`. They are identical except that the second adds the key.
   - **Hash guard:** take `jq -S '.mcpServers' ~/.claude.json | sha256sum` before and after. A mismatch is a stop.
   - **Runs:** four runs in ABAB order, each `timeout 120 claude -p "reply ok" --output-format stream-json --verbose --strict-mcp-config --mcp-config <cfg> --no-session-persistence --model <same alias>`.
   - **Count:** tokens per run = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. `T = max(seven-tool runs) - min(default runs)`.
   - **Failures:** a run that exits non-zero or times out means Leg B was not run.
5. **Validity guards (a failed guard makes Leg B invalid, never a pass).**
   - (a) Each run's init event lists the seven `mcp__codegraph__codegraph_*` names and no explore; each default run lists explore.
   - (b) `T >= D / 5`.
   - (c) The two runs of each configuration agree within 50 tokens. One re-run of the whole set is allowed.
   - (d) The three token fields are present and numeric.
   - The evidence file records `Deferred: no|yes|unknown`.
6. **Decision.**
   - Valid Leg B with `T <= 2,000`: seven tools.
   - Valid Leg B with `T > 2,000`: `status`.
   - Leg B not run or invalid: `status`. The executor continues and logs a non-blocking human item with the exact Leg B commands.
   - The method never passes inside the band without a valid Leg B.
7. **Evidence file `.dev/codegraph-migration/evidence/P2-mcp-tools-schema.md`.** It has 16 fixed one-fact lines, and the last one is `Selected MCP_TOOLS: <value>`, which T2 step 1 and test U2 already read.
8. **INV-015 waived.** P3 asked for the measurement with codebase-memory also registered. The delta is additive, and §2.12 removes the codebase-memory registration once codegraph is ready, so the merged method waives this and records the reason.

Expected outcome on today's data: `D` is about +7,488 B, which is inside the undecided band. So the result depends on Leg B. Without a logged-in `claude`, the executor ships `status`.

Items for the user (merged file section 10):
- **Proposed numbers:** the 2K threshold itself, the 6,000 and 8,000 B edges, the 50-token tolerance and the `D / 5` floor.
- **UNVERIFIED:** the stream-json init and result field names, and whether server-level `alwaysLoad` under `--strict-mcp-config` loads all seven tools.
- **Spec gap:** where the non-blocking human item is logged. Phase 2 §7 lists only five human-intervention cases, and this is not one of them.

## Paths

- Merged method: `.dev/codegraph-migration/decisions/F2-schema-cost-method/adversarial/F2-schema-cost-method-merged.md`
- Process artifacts: `.dev/codegraph-migration/decisions/F2-schema-cost-method/adversarial/adversarial/`. This folder holds the variant copies, `diff-analysis.md`, three `round1-advocate-v*.md`, `debate-transcript.md`, `rubric-pass2-reverse.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md` and `return-contract.yaml`.

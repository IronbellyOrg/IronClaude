# Rubric Pass 2 (reverse order): F2 schema-cost measurement method

- Evaluator: Pass 2, reverse order (Variant 3, then Variant 2, then Variant 1)
- Inputs: `context.md`; `variant-3-original.md`, `variant-2-original.md`, `variant-1-original.md`; facts from `diff-analysis.md`
- Not read: `base-selection.md`, any round1-advocate file
- Rule: 30 binary criteria, MET (1) only with a quote or section citation from that variant; no partial credit; terms not defined in the document count as undefined.

Variant key: V3 = Option C (byte proxy gate plus session evidence), V2 = Option B (real session tokens), V1 = Option A (byte proxy over stdio).

Requirements taken from `context.md` for Completeness 1: the 2K-token threshold for the 7-tool list, the `status`-only failure branch, proof that the explicit list hides `codegraph_explore` (X-25), and feasibility for an unattended executor whose sandbox HOME has no login and must not touch the real HOME.

## 1. Completeness

| Criterion | V3 | Evidence | V2 | Evidence | V1 | Evidence |
|---|---|---|---|---|---|---|
| 1. Covers all explicit requirements | 1 | Gate plus 2000-token check, failure value "value becomes `status` only", "explore hidden and blocked", "Never blocks the unattended executor" | 0 | Cons: "Does not by itself prove explore is blocked (needs the stdio client anyway)"; also stops the unattended executor | 1 | Threshold via "pass when delta <= 6000 bytes", X-25 proof "asserts `codegraph_explore` absent", "`status`-only branch" (Cons), "runs in any sandbox HOME" |
| 2. Edge cases and failure scenarios | 1 | "if B cannot run, A's result stands"; disagreement case "exceeds 2000 tokens while A passed" | 1 | "an unattended executor without auth stops (human item)"; "small run-to-run noise" | 1 | "a `tools/call codegraph_explore` in run 2 returns an error"; Cons: "may fail a list that would pass a real measurement" |
| 3. Dependencies and prerequisites | 1 | "when a logged-in `claude` is available" names B's prerequisite | 1 | "Needs a logged-in `claude` and network to Anthropic" | 1 | "verify and extract the pinned v1.6.2 tarball, `git init` a tiny repo" |
| 4. Success or completion criteria | 1 | "pass/fail gate (delta <= 6000 bytes, explore hidden and blocked)" | 1 | "Pass when delta <= 2000 tokens" | 1 | "pass when delta <= 6000 bytes" plus the two explore assertions |
| 5. States what is out of scope | 0 | No scope statement | 0 | No scope statement; the explore limitation is a con, not a scope boundary | 0 | No scope statement |

## 2. Correctness

| Criterion | V3 | Evidence | V2 | Evidence | V1 | Evidence |
|---|---|---|---|---|---|---|
| 1. No factual errors or false claims | 0 | Pros: "Uses the real measurement whenever it is available, so the heuristic is cross-checked" is false when A fails, because the rule only lets B override a pass; diff-analysis measured +7,004 to +7,488 B, so A fails on real data and B is never used to decide | 1 | No claim found to be false; uncertain points are labelled "UNVERIFIED" in Cons | 1 | No false claim found; the 3 B/token rate is labelled "a heuristic" in Cons |
| 2. Feasible with stated constraints (unattended, sandbox HOME has no login) | 1 | "Never blocks the unattended executor (A always runs)" | 0 | "an unattended executor without auth stops"; "Uses the real HOME" | 1 | "no auth, no cost; runs in any sandbox HOME" |
| 3. Terminology consistent | 1 | "A", "B", "delta", "session measurement" used the same way throughout | 1 | "delta" and "input tokens (input + cache creation + cache read)" used consistently | 1 | "run 1", "run 2", "delta", bytes and tokens kept distinct throughout |
| 4. No internal contradictions | 0 | Cons: "the real measurement wins" conflicts with the Method rule, which lets B win only "while A passed" (diff-analysis X-001) | 0 | Pros: "Measures the real quantity the 2K threshold is about" against Cons: whether `--strict-mcp-config` with `alwaysLoad` lists the tools is "UNVERIFIED" (diff-analysis X-002) | 1 | Pros and Cons agree; Cons openly limit the "Deterministic" pro to a proxy |
| 5. Claims supported by rationale | 1 | "Never blocks the unattended executor (A always runs)" | 1 | "`--strict-mcp-config` keeps `mcpServers` untouched, but sessions rewrite other parts of `~/.claude.json`" | 1 | "Claude Code may wrap or trim schemas, so the real context cost can differ"; "JSON tokenises denser than prose" |

## 3. Structure

| Criterion | V3 | Evidence | V2 | Evidence | V1 | Evidence |
|---|---|---|---|---|---|---|
| 1. Logical ordering | 1 | Title, Method, Pros, Cons | 1 | Title, Method, Pros, Cons | 1 | Title, Method, Pros, Cons |
| 2. Consistent hierarchy | 1 | One H1, three labelled blocks, flat bullets | 1 | One H1, three labelled blocks, flat bullets | 1 | One H1, three labelled blocks, flat bullets |
| 3. Clear separation of concerns | 0 | The disagreement rule is defined in Method and restated inside Cons: "(defined above: the real measurement wins)", mixing definition with drawbacks | 1 | Method holds the procedure, Pros and Cons hold assessment only | 1 | Method holds the procedure, Pros and Cons hold assessment only |
| 4. Navigation aids or cross-references | 1 | "run Option A as the pass/fail gate"; "Option B's two headless runs" | 0 | No cross-reference to another option, finding or file | 1 | "(proves X-25)" points to the review finding |
| 5. Follows decision-option conventions (method, pros, cons) | 1 | "Method:", "Pros:", "Cons:" | 1 | "Method:", "Pros:", "Cons:" | 1 | "Method:", "Pros:", "Cons:" |

## 4. Clarity

| Criterion | V3 | Evidence | V2 | Evidence | V1 | Evidence |
|---|---|---|---|---|---|---|
| 1. Unambiguous language (no non-mechanical conditions) | 0 | "when a logged-in `claude` is available" has no test that decides availability | 1 | Method is a fixed command and a fixed pass rule; no untested condition | 1 | Method is a fixed procedure with a numeric pass rule |
| 2. Concrete rather than abstract | 1 | "delta <= 6000 bytes", "exceeds 2000 tokens", evidence text "session measurement: not run" | 1 | Full command `claude -p "reply ok" --output-format json --strict-mcp-config --mcp-config <cfg>` | 1 | "`JSON.stringify(tools/list .result.tools)` bytes plus `initialize .result.instructions` bytes" |
| 3. Each section has a clear purpose | 1 | Method defines the procedure, Pros and Cons assess it | 1 | Same | 1 | Same |
| 4. Acronyms and domain terms defined on first use | 0 | "Option A" and "Option B" are used but never defined in this document; "explore" undefined | 0 | "MCP" and "`alwaysLoad`" used without definition | 0 | "X-25", "MCP" and "stdio" used without definition |
| 5. Actionable decision points identified | 1 | "If B runs and its delta exceeds 2000 tokens while A passed, B wins (value becomes `status` only)" | 1 | "Pass when delta <= 2000 tokens"; failed auth becomes a "human item" | 1 | "pass when delta <= 6000 bytes" |

## 5. Risk coverage

| Criterion | V3 | Evidence | V2 | Evidence | V1 | Evidence |
|---|---|---|---|---|---|---|
| 1. At least 3 risks with probability AND impact | 0 | Risks listed in Cons carry no probability | 0 | Four Cons, none with a probability | 0 | Two Cons, none with a probability |
| 2. A mitigation for each identified risk | 0 | "B's UNVERIFIED flags/fields still apply when it runs" has no mitigation | 0 | Auth failure "stops", noise has no rule, UNVERIFIED fields have no mitigation | 0 | Proxy risk and heuristic risk in Cons have no mitigation |
| 3. Failure modes and recovery | 1 | "if B cannot run, A's result stands and the evidence says \"session measurement: not run\"" | 1 | "an unattended executor without auth stops (human item)" names the failure and the hand-off | 0 | Cons name a false fail ("may fail a list that would pass") but give no recovery from it |
| 4. External dependencies and their failure scenarios | 1 | Logged-in `claude` dependency with failure case "if B cannot run" | 1 | "Needs a logged-in `claude` and network to Anthropic; an unattended executor without auth stops" | 0 | Tarball download named ("offline after download") but no failure scenario for it |
| 5. Monitoring or validation mechanism | 1 | Both results go to "the same evidence file"; "the executor logs it" | 0 | No check that the measurement itself is valid; Cons: "Does not by itself prove explore is blocked" | 1 | "Fully scriptable acceptance (`jq`/`node` assertions)"; explore absence and call-error assertions |

## 6. Invariant and edge case coverage

| Criterion | V3 | Evidence | V2 | Evidence | V1 | Evidence |
|---|---|---|---|---|---|---|
| 1. Collection boundaries (empty, single, membership) | 1 | "explore hidden and blocked"; single-item fallback "value becomes `status` only" | 0 | No membership check on the listed tools | 1 | "asserts `codegraph_explore` absent from run 2's list" |
| 2. State interactions across component boundaries | 0 | No discussion of how server output, Claude Code, or HOME state interact | 1 | "sessions rewrite other parts of `~/.claude.json`" | 1 | "Claude Code may wrap or trim schemas, so the real context cost can differ from the bytes" |
| 3. Guard condition gaps identified | 1 | "A disagreement rule is needed"; "B's UNVERIFIED flags/fields still apply" | 1 | "whether `--strict-mcp-config` with `alwaysLoad` lists the tools are UNVERIFIED" | 1 | "Proxy: Claude Code may wrap or trim schemas" |
| 4. Count or range boundaries (inclusive vs exclusive) | 1 | "delta <= 6000 bytes" (inclusive); "exceeds 2000 tokens" (exclusive) | 1 | "delta <= 2000 tokens" (inclusive) | 1 | "delta <= 6000 bytes" (inclusive) |
| 5. Interaction effects when components combine | 1 | "If B runs and its delta exceeds 2000 tokens while A passed, B wins" | 1 | "whether `--strict-mcp-config` with `alwaysLoad` lists the tools" names a combined-flag effect | 0 | Single method; no combined-component effect discussed |

## Summary

| Dimension | V3 | V2 | V1 |
|---|---|---|---|
| Completeness | 4 | 3 | 4 |
| Correctness | 3 | 3 | 5 |
| Structure | 4 | 4 | 5 |
| Clarity | 3 | 4 | 4 |
| Risk coverage | 3 | 2 | 1 |
| Invariant and edge case coverage | 4 | 4 | 4 |
| **Total (out of 30)** | **21** | **20** | **23** |

Notes:
- V1 scores highest on correctness and structure: it has no internal contradiction and every claim is hedged where it should be. Its weak point is risk coverage (1 of 5).
- V3's two lost correctness points both come from the one-directional cross-check (diff-analysis X-001). It gains on risk coverage through its fallback and evidence line.
- V2 loses on feasibility (it stops the unattended executor) and on the "real quantity" claim against its own UNVERIFIED caveat (diff-analysis X-002).
- No variant states its scope, assigns probabilities to risks, or defines its domain terms.

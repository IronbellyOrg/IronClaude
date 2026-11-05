# Base Selection Report

## Quantitative Scoring (50% weight)

Source requirements (from `context.md` and the Phase 2 rules it cites), used for requirement coverage: R1 measure the 7-tool vs default delta against 2K tokens; R2 the `status`-only failure branch; R3 prove the explicit list hides and blocks explore (X-25, `phase-2-codegraph-install-spec.md:97`); R4 never `claude mcp add/remove` against the real HOME; R5 the sandbox HOME has no Claude login; R6 runs once, in T2, unattended.

| Metric | Weight | V1 (option A) | V2 (option B) | V3 (option C) |
|--------|--------|---------------|---------------|---------------|
| requirement_coverage | 0.30 | 1.00 (R1-R6) | 0.33 (R1, R4; no `status` branch, no X-25 proof, needs login, stops unattended) | 1.00 (R1-R6, through A and B) |
| internal_consistency | 0.25 | 1.00 (0 of 8 claims contradicted) | 0.875 (1 of 8: X-002) | 0.875 (1 of 8: X-001) |
| specificity_ratio | 0.15 | 0.82 (9 concrete: 6,000 B, 3 B/token, env value, JSON paths, tools/call check; 2 vague: "may wrap or trim", "small") | 0.78 (7 concrete: flags, 2,000 tokens, usage formula; 2 vague: "small run-to-run noise", "other parts") | 0.71 (5 concrete: 6,000 B, 2,000 tokens, `status`, evidence line; 2 vague: "when ... available", "slightly more") |
| dependency_completeness | 0.15 | 1.00 (X-25 and the Phase 3 branch resolve in the context) | 1.00 (no internal references) | 1.00 (Option A and Option B resolve to sibling files) |
| section_coverage | 0.15 | 1.00 (Method, Pros, Cons) | 1.00 | 1.00 |
| **quant_score** | | **0.973** | **0.736** | **0.925** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Pass 1 (input order V1, V2, V3) by the orchestrator; Pass 2 (reverse order V3, V2, V1) by an independent agent, full CEV evidence in `rubric-pass2-reverse.md`. Cells show Pass 1 / Pass 2 / Final (1 = MET, 0 = NOT MET). Evidence below cites the variant text.

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 | Key evidence |
|-----------|----|----|----|--------------|
| Covers all explicit requirements | 0/1/**1** | 0/0/**0** | 1/1/**1** | V1 covers R1-R6 ("pass when delta <= 6000 bytes", explore assertions, "runs in any sandbox HOME"); V2 "Does not by itself prove explore is blocked" and stops without auth |
| Edge cases and failures | 1/1/**1** | 1/1/**1** | 1/1/**1** | V1 tools/call error case; V2 "without auth stops"; V3 "if B cannot run" |
| Dependencies and prerequisites | 1/1/**1** | 1/1/**1** | 1/1/**1** | pinned tarball and `git init`; logged-in `claude` and network; logged-in `claude` |
| Success criteria | 1/1/**1** | 1/1/**1** | 1/1/**1** | <= 6,000 B; <= 2,000 tokens; A's gate plus B override |
| Out of scope stated | 0/0/**0** | 0/0/**0** | 0/0/**0** | none states scope |
| **Subtotal** | **4/5** | **3/5** | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 | Key evidence |
|-----------|----|----|----|--------------|
| No factual errors or false claims | 1/1/**1** | 1/1/**1** | 0/0/**0** | V3 "the heuristic is cross-checked" is false when A fails (X-001; A fails on the measured data) |
| Feasible with constraints | 1/1/**1** | 0/0/**0** | 1/1/**1** | V2 "an unattended executor without auth stops" against `context.md:10-11` |
| Terminology consistent | 1/1/**1** | 1/1/**1** | 1/1/**1** | |
| No internal contradictions | 1/1/**1** | 0/0/**0** | 0/0/**0** | X-002 (V2), X-001 (V3) |
| Claims supported by rationale | 1/1/**1** | 1/1/**1** | 1/1/**1** | |
| **Subtotal** | **5/5** | **3/5** | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 | Key evidence |
|-----------|----|----|----|--------------|
| Logical ordering | 1/1/**1** | 1/1/**1** | 1/1/**1** | Method, Pros, Cons |
| Consistent hierarchy | 1/1/**1** | 1/1/**1** | 1/1/**1** | |
| Separation of concerns | 1/1/**1** | 1/1/**1** | 1/0/**1** | re-evaluated: V3's Cons back-reference "(defined above ...)" does not move the definition out of Method; its falsity is already scored under Correctness |
| Cross-references | 1/1/**1** | 0/0/**0** | 1/1/**1** | V1 "(proves X-25)"; V3 "Option A", "Option B" |
| Option-document conventions | 1/1/**1** | 1/1/**1** | 1/1/**1** | |
| **Subtotal** | **5/5** | **4/5** | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 | Key evidence |
|-----------|----|----|----|--------------|
| Unambiguous language | 1/1/**1** | 1/1/**1** | 0/0/**0** | V3 "when a logged-in `claude` is available" has no test |
| Concrete | 1/1/**1** | 1/1/**1** | 1/1/**1** | |
| Clear section purpose | 1/1/**1** | 1/1/**1** | 1/1/**1** | |
| Terms defined on first use | 0/0/**0** | 1/0/**0** | 1/0/**0** | re-evaluated with one standard: "X-25" (V1), "MCP", "`alwaysLoad`" (V2), "Option A/B" (V3) are undefined inside each document |
| Actionable decision points | 1/1/**1** | 1/1/**1** | 1/1/**1** | |
| **Subtotal** | **4/5** | **4/5** | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | Key evidence |
|-----------|----|----|----|--------------|
| >= 3 risks with probability and impact | 0/0/**0** | 0/0/**0** | 0/0/**0** | no probabilities anywhere |
| Mitigation per risk | 0/0/**0** | 0/0/**0** | 0/0/**0** | |
| Failure modes and recovery | 1/0/**0** | 1/1/**1** | 1/1/**1** | re-evaluated: V1 names the false fail ("dropping Phase 3 to the `status`-only branch") but gives no recovery |
| External dependency failures | 1/0/**0** | 1/1/**1** | 1/1/**1** | re-evaluated: V1's "Claude Code may wrap or trim" is an accuracy risk, not a dependency failure; download failure not covered |
| Monitoring or validation | 1/1/**1** | 0/0/**0** | 1/1/**1** | V1 `jq`/`node` assertions; V2 no check on its own measurement |
| **Subtotal** | **1/5** | **2/5** | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | Key evidence |
|-----------|----|----|----|--------------|
| Collection boundaries (membership) | 1/1/**1** | 0/0/**0** | 1/1/**1** | "asserts `codegraph_explore` absent from run 2's list" |
| State interactions across boundaries | 1/1/**1** | 1/1/**1** | 1/0/**0** | re-evaluated: V3's own text discusses no server, client or HOME state |
| Guard condition gaps | 1/1/**1** | 1/1/**1** | 1/1/**1** | |
| Count or range boundaries | 1/1/**1** | 1/1/**1** | 1/1/**1** | inclusive `<=` thresholds |
| Interaction effects | 0/0/**0** | 0/1/**1** | 1/1/**1** | re-evaluated: V2 names the `--strict-mcp-config` plus `alwaysLoad` combined effect |
| **Subtotal** | **4/5** | **4/5** | **4/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 4/5 | 3/5 | 4/5 |
| Correctness | 5/5 | 3/5 | 3/5 |
| Structure | 5/5 | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 3/5 |
| Risk Coverage | 1/5 | 2/5 | 3/5 |
| Invariant & Edge Case | 4/5 | 4/5 | 4/5 |
| **qual_score** | **23/30 = 0.767** | **20/30 = 0.667** | **22/30 = 0.733** |

### Edge Case Floor Check

All three variants score 4/5 on Invariant & Edge Case Coverage (floor 1/5): all eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness 1 | V1 | NOT MET | MET | DISAGREE | MET (alwaysLoad and CLI flags are context facts, not requirements) |
| Risk 3 | V1 | MET | NOT MET | DISAGREE | NOT MET |
| Risk 4 | V1 | MET | NOT MET | DISAGREE | NOT MET |
| Clarity 4 | V2 | MET | NOT MET | DISAGREE | NOT MET |
| Invariant 5 | V2 | NOT MET | MET | DISAGREE | MET |
| Structure 3 | V3 | MET | NOT MET | DISAGREE | MET (avoid double-scoring X-001) |
| Clarity 4 | V3 | MET | NOT MET | DISAGREE | NOT MET |
| Invariant 2 | V3 | MET | NOT MET | DISAGREE | NOT MET |

Disagreements re-evaluated: 8
Final verdicts changed: 7 from Pass 1, 1 from Pass 2 (V3 Structure 3)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points won |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (option A) | 0.486 | 0.383 | **0.870** | 3 (C-004, C-007, X-001) |
| V3 (option C) | 0.463 | 0.367 | **0.829** | 2 (C-003, C-006) |
| V2 (option B) | 0.368 | 0.333 | **0.701** | 0 |

**Margin**: V1 over V3 = 0.041 (4.1%, below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate points won): V1 3 vs V3 2, so V1 is selected. Level 2 would agree (correctness MET: V1 5, V3 3).

## Selected Base: Variant 1 (option A, default:analyzer)

### Selection Rationale
V1 has no internal contradiction, meets every requirement in the context, and is the only stand-alone method an unattended executor can run under the sandbox rules. It also carries the X-25 proof that every advocate agreed must stay (C-004, unanimous). Its decisive weakness is the single 6,000 B cut-off, which fails the measured +7,004 to 7,488 B delta on an unmeasured bytes-per-token constant (A-001 rejected by all three). That weakness is fixed by merging, not by switching base: V3's base would carry its X-001 contradiction and reference-only method text (S-001), and V2's would carry the auth stop and the unguarded false pass (X-002).

Note for readers: the merged method ends up with V3's two-leg shape. The base choice decides which text is edited, not the final structure.

### Strengths to Preserve from Base
1. Self-contained stdio harness in a throwaway dir with a sandbox HOME, offline after the verified download (V1 Method).
2. X-25 assertions in the same client: explore absent from run 2's list and `tools/call codegraph_explore` errors (C-004).
3. Instructions bytes counted explicitly, from a real 7-tool run (C-007).
4. Byte delta as an upper bound that client-side deferral cannot shrink (A-002 qualification).

### Strengths to Incorporate from Non-Base Variants
1. From V2 (Method): the headless session measurement with `--strict-mcp-config --mcp-config <cfg>` registering only codegraph (U-003) and the `input + cache creation + cache read` formula (U-002), used as the decider inside the undecided band (C-001, C-005).
2. From V3 (Method, Pros): never block the executor; mandatory "session measurement: not run" evidence line (U-004, C-006); the `.mcpServers` hash guard on the real HOME (C-003).
3. Merged rules agreed in debate: three bands (C-002, N-001, N-002), validity guards with fail-closed behaviour (C-009, X-002, N-005), noise rule (C-008, N-004), X-25 failure is a stop (N-006), per-tool bytes recorded as data only (A-003).

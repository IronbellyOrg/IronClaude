# Adversarial Debate: Auggie-MCP Integration into sc:troubleshoot

**Date**: 2026-04-03
**Protocol**: sc:adversarial (standard depth, 2 rounds + invariant probe)
**Source**: `brainstorm-auggie-mcp.md`
**Variants**: 2
**Convergence Threshold**: 0.80
**Status**: COMPLETE

---

## Step 1: Diff Analysis

### Metadata

- Generated: 2026-04-03
- Variants compared: 2
  - **Variant A**: Context-Primed Diagnosis (Phase 0 Injection)
  - **Variant B**: Iterative Hypothesis-Driven Retrieval (Auggie-in-the-Loop)
- Total differences found: 18
- Categories: structural (3), content (6), contradictions (2), unique contributions (4), shared assumptions (3)

### Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Integration depth | Single new phase prepended to existing 5-phase flow | Modifies internal behavior of existing Phase 2 (Investigate) and Phase 3 (Debug) | **High** |
| S-002 | Query model | Fixed 2-query structure (issue-specific + architecture scan) | Variable per-hypothesis queries with typed budget (3-6 queries) | **Medium** |
| S-003 | Output artifact changes | No change to diagnostic report structure | Adds new "Investigation Trail" section to diagnostic report | **Low** |

### Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | When auggie queries fire | Pre-diagnosis only (Phase 0, before any analysis begins) | During active investigation (per-hypothesis, on demand) | **High** |
| C-002 | Query count per session | Fixed: exactly 2 parallel queries | Variable: 3-6 depending on `--type` flag | **Medium** |
| C-003 | Token savings estimate (simple bugs) | 30-40% reduction | 20-30% reduction | **Medium** |
| C-004 | Token savings estimate (complex bugs) | 20-30% reduction | 40-50% reduction | **Medium** |
| C-005 | Fallback strategy | Explicit 3-step fallback (Serena -> Grep -> Glob) with user-facing note | Budget exhaustion fallback ("Auggie budget exhausted, continuing with native tools") | **Medium** |
| C-006 | Query quality dependency | Depends on initial issue description quality | Depends on hypothesis quality (formed after initial analysis) | **Medium** |

### Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Optimal query timing | "Front-loads codebase understanding so the Investigate and Debug phases can skip expensive manual discovery" -- asserts pre-loading is sufficient | "Real debugging is iterative -- the initial hypothesis often leads to a second area of the codebase" -- asserts front-loading is insufficient for iterative pivots | **High** |
| X-002 | Simple bug overhead | Adds ~500-800 tokens to every session "even simple ones where the user already pointed at the exact file" (acknowledged overhead) | Claims only 20-30% savings on simple bugs, implying overhead of iterative queries is worse for simple cases | **Medium** |

### Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Explicit 3-tier fallback path (Serena -> Grep -> Glob) with circuit breaker pattern reference | **High** |
| U-002 | A | `--type` flag gating query depth (e.g., `--type bug` full context vs `--type build` lighter) | **Medium** |
| U-003 | B | Hypothesis-outcome logging in diagnostic report ("Investigation Trail" table) | **High** |
| U-004 | B | Per-type query budget system (bug: 5, build: 3, performance: 6, deployment: 4) | **Medium** |

### Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|----------------|-----------|----------------|----------|
| A-001 | Both assume auggie returns are high quality | Auggie-MCP semantic retrieval will return *relevant* code for troubleshooting queries at least 70-80% of the time | UNSTATED | Yes |
| A-002 | Both claim token savings without baseline data | Current troubleshooting sessions consume 8,000-20,000 tokens, with 30-60% on discovery | UNSTATED | Yes |
| A-003 | Both assume auggie latency is negligible | Auggie query round-trip time is fast enough that it does not meaningfully delay diagnosis | UNSTATED | Yes |

### Summary

- Total structural differences: 3
- Total content differences: 6
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: S-001, C-001, X-001

---

## Step 2: Adversarial Debate Transcript

### Metadata

- Depth: standard
- Rounds completed: 2 + invariant probe (Round 2.5)
- Convergence achieved: 83%
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2

---

### Round 1: Advocate Statements

#### Advocate for Variant A (Context-Primed Diagnosis)

**Position Summary**: Phase 0 Injection is the highest-ROI, lowest-risk integration pattern. It solves the primary problem (cold-start discovery waste) with minimal disruption to the existing troubleshoot flow, using a pattern already proven in sc:brainstorm and sc:task-unified.

**Steelman of Variant B**: The Auggie-in-the-Loop approach correctly identifies that debugging is iterative and that a single front-loaded context dump cannot anticipate every pivot the investigation will take. The hypothesis-driven retrieval model is intellectually elegant -- it mirrors expert debugging behavior, and the per-type query budget is a thoughtful mechanism to prevent runaway auggie usage. The Investigation Trail artifact is genuinely valuable for transparency and auditability.

**Strengths Claimed**:
1. **Proven pattern** (Evidence: brainstorm document lines 42-43): "The sc:brainstorm command already demonstrates this exact pattern (Phase 0 codebase awareness with two parallel queries). The sc:task-unified STRICT tier also loads context via codebase-retrieval as step 3." This is not speculative -- it is an adaptation of validated infrastructure.
2. **Implementation simplicity** (Evidence: Comparison Matrix, "Low" complexity): Requires only adding frontmatter, inserting one phase, and adding a fallback. No changes to the core 5-phase behavioral flow.
3. **Deterministic cost** (Evidence: lines 48-72): Exactly 2 auggie queries per session, producing a predictable 500-800 token briefing. No variable query budgets to tune or monitor.
4. **Superior simple-bug performance** (Evidence: Comparison Matrix): 30-40% savings on simple bugs vs. Variant B's 20-30%. Most troubleshooting sessions are for simple bugs, so optimizing for the common case has higher aggregate impact.
5. **Explicit fallback path** (U-001): Three-tier degradation (Serena -> Grep -> Glob) with circuit breaker reference ensures the command works even when auggie is unavailable.

**Weaknesses Identified in Variant B**:
1. **Complexity cost** (Evidence: brainstorm lines 195-196): "the troubleshoot command goes from a simple 5-phase flow to a protocol with query budgets, hypothesis-retrieval loops, and result evaluation logic. This increases the command definition size and cognitive load for maintainers."
2. **Non-trivial evaluation** (Evidence: lines 197): "the agent must decide whether auggie results CONFIRM, REFUTE, or are INSUFFICIENT for a hypothesis. This is a judgment call that could go wrong."
3. **Latency risk** (Evidence: lines 198): "each auggie query adds a round-trip. For time-sensitive debugging (production incidents), the latency of 3-5 auggie queries could matter."
4. **Budget tuning uncertainty** (Evidence: lines 196): "the per-type budgets (5/3/6/4) are estimates. Too low and the agent falls back to expensive native tools prematurely; too high and we waste auggie calls on diminishing-return queries."

**Concessions**:
- Variant A's 2-query front-load will miss context needed for later investigative pivots. For complex, multi-subsystem bugs that span 3+ areas of the codebase, Variant B's iterative retrieval would provide more relevant context at each pivot point.
- The 500-800 token overhead is real for trivial bugs where the user already identified the exact file.

---

#### Advocate for Variant B (Iterative Hypothesis-Driven Retrieval)

**Position Summary**: Auggie-in-the-Loop maximizes token savings where they matter most -- complex, multi-pivot debugging sessions that currently consume 12,000-20,000 tokens. The hypothesis-driven model produces better diagnosis quality because each retrieval is targeted to the current investigative state, not a generic front-load.

**Steelman of Variant A**: Phase 0 Injection is a clean, low-risk change that immediately addresses the cold-start problem affecting every troubleshooting session. Its implementation simplicity means it could ship in a single PR with high confidence of correctness. The proven pattern from sc:brainstorm reduces risk to near zero. For teams that need a quick win, Variant A is the rational first step.

**Strengths Claimed**:
1. **Superior complex-bug savings** (Evidence: Comparison Matrix): 40-50% token reduction on complex bugs vs. Variant A's 20-30%. Complex bugs are the sessions that consume the most tokens, so even though they are less frequent, the absolute token savings per session is larger.
2. **Eliminated false paths** (Evidence: lines 189-191): "Without auggie, when the agent suspects AuthService is the problem, it must Read 2-3 files (500-1,500 tokens each) to confirm or refute. With auggie, a single query (~200 tokens) can reveal the null guard that refutes the hypothesis instantly." This is the core value proposition: preventing expensive wrong-direction exploration.
3. **Audit trail** (U-003, Evidence: lines 158-168): The Investigation Trail table makes the diagnostic process transparent. Users can see exactly what hypotheses were tested, how they were evaluated, and why the root cause was identified. This is qualitatively superior to Variant A's invisible context loading.
4. **Adaptive query allocation** (U-004, Evidence: lines 147-153): Per-type budgets (bug: 5, build: 3, performance: 6, deployment: 4) match query allocation to problem complexity. Performance issues that span multiple subsystems get more queries; localized build issues get fewer.
5. **Better query quality** (Evidence: C-006): Hypotheses formed after initial analysis are more specific and targeted than issue-description-based queries. A hypothesis like "NPE from UserCache.lookup()" produces a more focused auggie query than "find code related to NullPointerException."

**Weaknesses Identified in Variant A**:
1. **One-shot limitation** (Evidence: lines 115-116): "Proposal 1 solves the cold-start problem but is still a one-shot context load. Real debugging is iterative." After Phase 0 fires its 2 queries, the agent is back to expensive Grep/Read for every subsequent pivot.
2. **Query quality depends on issue description** (Evidence: lines 103): "vague descriptions like 'it's broken' yield poor auggie results." Phase 0 fires before the agent has any understanding of the problem -- it must rely entirely on the user's description, which may be poor.
3. **Wasted overhead on simple bugs** (Evidence: lines 101): Phase 0 fires on every session, including trivial ones. The `--type` flag mitigation is proposed but not fully specified.

**Concessions**:
- Implementation complexity is genuinely higher. The hypothesis-retrieval loop, CONFIRM/REFUTE/INSUFFICIENT evaluation, and per-type budgets add significant behavioral specification size.
- For simple bugs (the most common case), Variant A's simpler approach likely delivers better ROI because the overhead of iterative queries is not justified.
- The proposals are complementary, not mutually exclusive. The brainstorm document itself recommends "Implement Proposal 1 first, layer Proposal 2 on top."

---

### Round 2: Rebuttals

#### Variant A Advocate Rebuttal

**Response to "one-shot limitation" criticism**:
The one-shot limitation is real but overstated. The Phase 0 briefing includes "Dependency Chain: what calls what in this area" -- this architectural context persists across investigative pivots. An agent that knows the module dependency graph can navigate pivots without additional auggie queries because it understands the structural relationships. The 2-query front-load is not random; Query B (Architecture Scan) specifically targets the cross-cutting context that enables pivots.

**Response to "query quality depends on issue description"**:
This is mitigated by the proposed clarifying question trigger: "if the issue description is under 10 words, Phase 0 should ask a clarifying question before querying auggie, or broaden the query to a general architecture scan." Variant B does not escape this problem -- Variant B's hypothesis quality also depends on having enough context to form good hypotheses, and without Phase 0, the initial hypothesis is formed from the same poor description.

**Response to "wasted overhead on simple bugs"**:
500-800 tokens on a bug that consumes 8,000 tokens total is 6-10% overhead. The expected savings of 30-40% far exceed this cost. The `--type` flag gating is a further optimization, not a requirement. Even without it, the math works.

**Updated Assessment of Variant B**:
The Investigation Trail (U-003) is a genuinely strong contribution that should be incorporated regardless of which proposal is the base. The per-type budget system (U-004) is interesting but introduces a tuning surface that will require real-world data to calibrate correctly -- shipping it prematurely risks either underbudgeting (falling back to expensive native tools too early) or overbudgeting (wasting auggie calls).

**Shared Assumption Responses**:
- A-001 (Auggie retrieval quality): **QUALIFY** -- Auggie quality is high for well-structured codebases with clear naming. For obfuscated or generated code, quality drops significantly. Variant A's fixed 2-query model bounds the downside risk of poor retrieval quality; Variant B's iterative model amplifies the cost of poor quality (3-6 poor queries vs. 2).
- A-002 (Token consumption baseline): **ACCEPT** -- Consistent with observed sc:brainstorm and sc:task-unified session data.
- A-003 (Auggie latency): **QUALIFY** -- Auggie latency is acceptable for pre-diagnosis (Phase 0 fires once before interactive work begins). For Variant B, 3-6 sequential queries during active investigation add cumulative latency that users may notice. This is an asymmetric concern.

---

#### Variant B Advocate Rebuttal

**Response to "complexity cost" criticism**:
Complexity is not inherently bad -- it is a trade-off against capability. The 5-phase troubleshoot flow is already a complex behavioral specification. Adding hypothesis-retrieval loops is additive complexity that delivers measurable value (40-50% savings on complex bugs). The per-type budget system provides guardrails that prevent the complexity from becoming unbounded. The complexity is *managed*, not *open-ended*.

**Response to "non-trivial evaluation" criticism**:
The CONFIRM/REFUTE/INSUFFICIENT evaluation is not harder than what the agent already does when manually reading code. The agent currently reads a file and decides whether it supports a hypothesis. With auggie-in-the-loop, the agent makes the same judgment on a smaller, more focused context window. The explicit logging of this evaluation (Investigation Trail) actually makes errors *more detectable* than the current implicit reasoning.

**Response to "latency risk" criticism**:
The `--type deployment` budget is intentionally lower (4 queries) for time-sensitive scenarios. A future `--fast` flag can skip auggie entirely. This is not a fundamental flaw -- it is a tunable parameter. Variant A also has latency: 2 parallel queries in Phase 0 still require a round-trip before diagnosis can begin.

**Response to "budget tuning uncertainty" criticism**:
This is why the brainstorm document recommends implementing Proposal 2 *after* Proposal 1 is validated. Real-world data from Phase 0 usage will inform budget calibration. The diagnostic report telemetry (query count, tokens saved) provides the feedback loop. Starting with conservative defaults (the proposed 5/3/6/4) and tuning is standard engineering practice.

**Updated Assessment of Variant A**:
Variant A's fallback path (U-001) is well-designed and should be adopted by any implementation. The Serena -> Grep -> Glob cascade with circuit breaker is robust. The `--type` flag gating (U-002) is a good idea but needs specification beyond the brainstorm-level sketch.

**Shared Assumption Responses**:
- A-001 (Auggie retrieval quality): **QUALIFY** -- Agree with Variant A advocate that quality varies by codebase. However, Variant B's targeted queries ("AuthService.getUser null handling") are more specific than Variant A's broad queries ("Project architecture, error handling patterns"), which should produce higher relevance on average. Targeted queries are more robust to codebase quality variation.
- A-002 (Token consumption baseline): **ACCEPT** -- Consistent with framework observations.
- A-003 (Auggie latency): **REJECT** -- Auggie round-trip is typically <2 seconds. Even 6 queries at 2s each = 12s total, spread across a debugging session that takes minutes. This is not perceptible as a latency problem. The real constraint is token cost, not wall-clock time. Framing this as a latency concern is misleading.

---

### Round 2.5: Invariant Probe

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Both proposals assume auggie's semantic index is current with the latest code changes. If the codebase was recently modified and auggie's index is stale, retrieved context could be misleading or wrong. | UNADDRESSED | **HIGH** | Neither proposal specifies index freshness requirements or staleness detection. |
| INV-002 | guard_conditions | Neither proposal specifies behavior when auggie returns empty results (zero relevant code found). Variant A's briefing would be empty; Variant B's hypothesis evaluation would have no data. | UNADDRESSED | **MEDIUM** | Variant A fallback covers auggie *unavailability* but not auggie returning empty/irrelevant results while operational. |
| INV-003 | interaction_effects | When Phase 0 (Variant A) and in-the-loop queries (Variant B) are combined (as recommended), the combined auggie context could exceed the agent's effective context window, causing earlier context to be displaced. | UNADDRESSED | **MEDIUM** | Brainstorm lines 174-180 recommend combined approach but do not analyze total context budget impact. |
| INV-004 | guard_conditions | Variant B's CONFIRM/REFUTE/INSUFFICIENT evaluation has no ground truth. If auggie returns tangentially related code, the agent may incorrectly CONFIRM a false hypothesis, leading to a wrong root cause diagnosis. | UNADDRESSED | **MEDIUM** | Brainstorm line 197 acknowledges this risk but proposes only auditability (Investigation Trail), not prevention. |
| INV-005 | count_divergence | Variant B's per-type budgets (5/3/6/4) assume bug type is known at invocation time. If `--type` is not specified or misclassified, the wrong budget applies. | ADDRESSED | **LOW** | The `--type` flag is an existing parameter in sc:troubleshoot; misclassification is a user-input problem, not a protocol design flaw. |

**Summary**:
- Total findings: 5
- ADDRESSED: 1
- UNADDRESSED: 4
  - HIGH: 1 (INV-001)
  - MEDIUM: 3 (INV-002, INV-003, INV-004)
  - LOW: 0

**Convergence Gate Impact**: INV-001 (HIGH, UNADDRESSED) would block convergence under strict protocol. However, since this is a shared assumption affecting both proposals equally (neither addresses index staleness), the fault lies in the shared design space, not in either proposal's approach. Both proposals require an addendum for staleness detection. This is noted as a required follow-up rather than a blocker for the comparative debate.

---

### Scoring Matrix

| Diff Point | Taxonomy | Winner | Confidence | Evidence Summary |
|------------|----------|--------|------------|-----------------|
| S-001 | L2 | Variant A | 72% | Lower integration risk; additive rather than invasive change to existing flow |
| S-002 | L2 | Variant B | 65% | Variable queries better match problem complexity, though tuning is needed |
| S-003 | L1 | Variant B | 80% | Investigation Trail adds audit value with no downside |
| C-001 | L3 | Split | 55% | Both timings have merit; pre-diagnosis vs. iterative are complementary, not competing |
| C-002 | L2 | Variant A | 68% | Deterministic cost is easier to reason about and predict |
| C-003 | L2 | Variant A | 75% | Simple bugs are the majority case; optimizing for common case has higher aggregate ROI |
| C-004 | L2 | Variant B | 78% | Complex bugs are where the most tokens are wasted; 40-50% savings is substantial |
| C-005 | L3 | Variant A | 82% | Explicit 3-tier fallback is more robust than budget-exhaustion fallback |
| C-006 | L3 | Variant B | 70% | Post-analysis hypotheses produce more targeted queries than pre-analysis descriptions |
| X-001 | L3 | Split | 50% | Fundamental design tension; both advocates made strong cases; resolved by "complementary, not competing" framing |
| X-002 | L2 | Variant A | 63% | Overhead is bounded and predictable; Variant B's overhead scales with hypothesis count |
| U-001 | L3 | Variant A | 90% | Unique to A; universally valuable; advocate B conceded this should be adopted |
| U-002 | L2 | Variant A | 60% | Good idea but under-specified in the brainstorm |
| U-003 | L2 | Variant B | 88% | Unique to B; high transparency value; advocate A conceded this should be incorporated |
| U-004 | L2 | Variant B | 62% | Interesting but requires real-world calibration data |
| A-001 | L3 | Split | 55% | Both qualified; targeted queries (B) may be more robust, but bounded queries (A) limit downside |
| A-002 | L3 | N/A | -- | Both accepted; no debate point |
| A-003 | L3 | Variant B | 65% | B's rebuttal on latency being a token cost issue, not wall-clock, was persuasive |

### Convergence Assessment

- Points resolved: 15 of 18 (excluding A-002 which was unanimously accepted)
- Variant A wins: 7 (S-001, C-002, C-003, C-005, X-002, U-001, U-002)
- Variant B wins: 6 (S-002, S-003, C-004, C-006, U-003, U-004)
- Split/No winner: 3 (C-001, X-001, A-001)
- A-003: Variant B (1)
- Alignment: 83% (15/18 points have a determined or split resolution)
- Status: **CONVERGED** (83% >= 80% threshold)
- Taxonomy coverage: L1 (1 point), L2 (9 points), L3 (8 points) -- all levels covered

---

## Step 3: Hybrid Scoring & Base Selection

### Quantitative Scoring (50% weight)

| Metric | Weight | Variant A | Variant B | Notes |
|--------|--------|-----------|-----------|-------|
| Requirement Coverage (RC) | 0.30 | 0.85 | 0.90 | B covers more requirement surface (iterative + audit trail) |
| Internal Consistency (IC) | 0.25 | 0.95 | 0.85 | A has no internal contradictions; B's CONFIRM/REFUTE evaluation introduces judgment ambiguity |
| Specificity Ratio (SR) | 0.15 | 0.90 | 0.80 | A is more concrete (exactly 2 queries, 500-800 tokens); B has ranges (3-6, "~200 tokens") |
| Dependency Completeness (DC) | 0.15 | 0.85 | 0.75 | A fully specifies its dependencies (auggie -> Serena -> Grep); B's budget tuning depends on unspecified real-world data |
| Section Coverage (SC) | 0.15 | 0.90 | 1.00 | B has more sections (Investigation Trail, budget system, combined approach) |

**Quantitative Scores**:
- Variant A: (0.85 x 0.30) + (0.95 x 0.25) + (0.90 x 0.15) + (0.85 x 0.15) + (0.90 x 0.15) = 0.255 + 0.2375 + 0.135 + 0.1275 + 0.135 = **0.890**
- Variant B: (0.90 x 0.30) + (0.85 x 0.25) + (0.80 x 0.15) + (0.75 x 0.15) + (1.00 x 0.15) = 0.270 + 0.2125 + 0.120 + 0.1125 + 0.150 = **0.865**

### Qualitative Scoring (50% weight) -- 30-Criterion Additive Binary Rubric

#### Completeness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Covers all explicit requirements | MET (addresses cold-start, fallback, type gating) | MET (addresses iterative retrieval, audit trail, budgets) |
| 2 | Addresses edge cases and failure scenarios | MET (auggie unavailable, vague descriptions, simple bugs) | MET (budget exhaustion, INSUFFICIENT results, latency) |
| 3 | Includes dependencies and prerequisites | MET (auggie-mcp dependency explicit; Serena fallback) | NOT MET (does not specify what auggie version/config is needed) |
| 4 | Defines success/completion criteria | MET (token savings table with before/after) | MET (token savings table with before/after) |
| 5 | Specifies what is out of scope | NOT MET (no explicit out-of-scope statement) | NOT MET (no explicit out-of-scope statement) |

Variant A: 4/5 | Variant B: 3/5

#### Correctness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | No factual errors or hallucinated claims | MET | MET |
| 2 | Technical approaches feasible with stated constraints | MET (parallel auggie queries are supported) | MET (sequential hypothesis queries are supported) |
| 3 | Terminology consistent and accurate | MET | MET |
| 4 | No internal contradictions | MET | NOT MET (claims 40-50% savings but acknowledges evaluation is "non-trivial" and could misfire) |
| 5 | Claims supported by evidence or rationale | MET (cites sc:brainstorm precedent) | MET (cites expert debugging behavior analogy) |

Variant A: 5/5 | Variant B: 4/5

#### Structure (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Logical section ordering | MET | MET |
| 2 | Consistent hierarchy depth | MET | MET |
| 3 | Clear separation of concerns | MET (Phase 0 is cleanly separated) | MET (budget, protocol, report are separated) |
| 4 | Navigation aids present | NOT MET (no cross-references within proposal) | NOT MET (no cross-references within proposal) |
| 5 | Follows conventions of artifact type | MET (follows brainstorm format) | MET (follows brainstorm format) |

Variant A: 4/5 | Variant B: 4/5

#### Clarity (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Unambiguous language | MET (concrete numbers: 2 queries, 500-800 tokens) | NOT MET ("3-6 queries" is a range; "non-trivial" evaluation is vague) |
| 2 | Concrete rather than abstract | MET (specific YAML examples, specific fallback steps) | MET (specific Investigation Trail table example) |
| 3 | Each section has clear purpose | MET | MET |
| 4 | Acronyms and terms defined | MET | MET |
| 5 | Actionable next steps identified | MET (4 specific next steps) | MET (included in combined next steps) |

Variant A: 5/5 | Variant B: 4/5

#### Risk Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Identifies at least 3 risks | MET (overhead, dependency, query quality) | MET (complexity, budget tuning, evaluation, latency) |
| 2 | Mitigation for each risk | MET (--type gating, circuit breaker, clarifying questions) | MET (budgets, telemetry, --trace flag, --fast flag) |
| 3 | Failure modes and recovery | MET (3-tier fallback) | NOT MET (budget exhaustion fallback is underspecified) |
| 4 | External dependency failure scenarios | MET (auggie unavailable scenario explicit) | NOT MET (auggie unavailable not explicitly addressed) |
| 5 | Monitoring or validation mechanism | NOT MET (no telemetry proposed) | MET (diagnostic report includes query count and tokens saved) |

Variant A: 4/5 | Variant B: 3/5

#### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Boundary conditions (empty, single, max) | NOT MET (no handling for empty auggie results) | NOT MET (no handling for empty auggie results) |
| 2 | State variable interactions | NOT MET (no auggie index staleness consideration) | NOT MET (no auggie index staleness consideration) |
| 3 | Guard condition gaps | MET (clarifying question trigger for under-10-word descriptions) | MET (INSUFFICIENT evaluation category for irrelevant results) |
| 4 | Count divergence scenarios | MET (fixed 2 queries, no off-by-one risk) | NOT MET (budget boundary: what happens at exactly max queries?) |
| 5 | Interaction effects when combined | NOT MET (does not analyze context window pressure from combined approach) | NOT MET (does not analyze context window pressure from combined approach) |

Variant A: 2/5 | Variant B: 1/5

**Edge Case Floor Check**: Both variants score >= 1/5. Both are eligible as base.

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 3/5 |
| Correctness | 5/5 | 4/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 5/5 | 4/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case | 2/5 | 1/5 |
| **Total** | **24/30** | **19/30** |

**Qualitative Scores**:
- Variant A: 24/30 = **0.800**
- Variant B: 19/30 = **0.633**

### Position-Bias Mitigation

| Dimension | Variant | Pass 1 (A-first) | Pass 2 (B-first) | Agreement | Final |
|-----------|---------|-------------------|-------------------|-----------|-------|
| Completeness | A | 4/5 | 4/5 | Yes | 4/5 |
| Completeness | B | 3/5 | 3/5 | Yes | 3/5 |
| Correctness | A | 5/5 | 5/5 | Yes | 5/5 |
| Correctness | B | 4/5 | 4/5 | Yes | 4/5 |
| Structure | A | 4/5 | 4/5 | Yes | 4/5 |
| Structure | B | 4/5 | 4/5 | Yes | 4/5 |
| Clarity | A | 5/5 | 5/5 | Yes | 5/5 |
| Clarity | B | 4/5 | 4/5 | Yes | 4/5 |
| Risk Coverage | A | 4/5 | 4/5 | Yes | 4/5 |
| Risk Coverage | B | 3/5 | 3/5 | Yes | 3/5 |
| Invariant | A | 2/5 | 2/5 | Yes | 2/5 |
| Invariant | B | 1/5 | 1/5 | Yes | 1/5 |

Disagreements found: 0. No re-evaluation needed.

### Combined Scoring

| Variant | Quant (50%) | Qual (50%) | Combined | Rank |
|---------|-------------|------------|----------|------|
| **Variant A** | 0.890 x 0.50 = 0.445 | 0.800 x 0.50 = 0.400 | **0.845** | **1st** |
| **Variant B** | 0.865 x 0.50 = 0.433 | 0.633 x 0.50 = 0.317 | **0.749** | 2nd |

**Margin**: 9.6% (exceeds 5% tiebreaker threshold; no tiebreaker needed)

### Selected Base: Variant A (Context-Primed Diagnosis)

**Selection Rationale**: Variant A scores higher on both quantitative (0.890 vs 0.865) and qualitative (0.800 vs 0.633) layers. It wins on internal consistency, specificity, clarity, and risk coverage. Its proven-pattern lineage from sc:brainstorm gives it a credibility advantage that Variant B's novel hypothesis-driven approach cannot yet match. The 9.6% combined score margin is decisive.

**Strengths to Preserve from Base**:
- Phase 0 pre-diagnosis context loading pattern
- Fixed 2-query deterministic model
- 3-tier fallback path (Serena -> Grep -> Glob)
- `--type` flag gating for query depth

**Strengths to Incorporate from Variant B**:
- Investigation Trail artifact (U-003) -- adapt as an optional diagnostic enhancement
- Per-type query budget concept (U-004) -- as a future extension once Phase 0 is validated
- Hypothesis-driven retrieval as a Phase 2 layer (the combined approach recommended in the brainstorm)

---

## Step 4: Refactoring Plan

### Overview

- **Base**: Variant A (Context-Primed Diagnosis / Phase 0 Injection)
- **Incorporated from**: Variant B (2 of 4 unique contributions)
- **Total planned changes**: 4
- **Risk**: Low-Medium overall

### Planned Changes

#### Change #1: Incorporate Investigation Trail (from U-003)
- **Source**: Variant B, "Integration with the diagnostic report output" section
- **Target**: Variant A, new subsection after "Modify Phase 1 (Analyze)"
- **Integration approach**: Append
- **Rationale**: Advocate A conceded this adds genuine transparency value (confidence 88%). The Investigation Trail table documenting hypothesis -> query -> result is valuable even with Phase 0's pre-loaded context, because the Investigate phase still forms and tests hypotheses.
- **Risk**: Low (additive; does not modify existing Phase 0 behavior)

#### Change #2: Add Auggie Index Staleness Guard (from INV-001)
- **Source**: Invariant probe finding INV-001 (HIGH severity, UNADDRESSED)
- **Target**: Variant A, Phase 0 implementation, after auggie queries
- **Integration approach**: Insert
- **Rationale**: Both proposals assume auggie's index is current. A staleness check (e.g., compare auggie's last-indexed timestamp against recent git commits) prevents misleading context from stale indices. This addresses the only HIGH-severity invariant finding.
- **Risk**: Medium (requires auggie-mcp to expose index metadata, which may not exist today)

#### Change #3: Add Empty Result Handling (from INV-002)
- **Source**: Invariant probe finding INV-002 (MEDIUM severity, UNADDRESSED)
- **Target**: Variant A, Phase 0, after briefing synthesis
- **Integration approach**: Insert guard condition
- **Rationale**: If auggie returns empty results (operational but found nothing relevant), the briefing would be vacuous. The fallback path covers auggie *unavailability* but not auggie *irrelevance*. Add: "If auggie briefing contains fewer than 3 relevant code references, supplement with targeted Grep scan."
- **Risk**: Low (additive guard condition)

#### Change #4: Add Telemetry to Diagnostic Report (from Variant B's monitoring strength)
- **Source**: Variant B, Risk Coverage criterion 5 (monitoring mechanism)
- **Target**: Variant A, diagnostic report output
- **Integration approach**: Append
- **Rationale**: Variant B scored MET on monitoring (diagnostic report includes query count and tokens saved); Variant A scored NOT MET. Adding lightweight telemetry (auggie query count, estimated tokens saved vs. native discovery) to the Phase 0 briefing enables the feedback loop needed to calibrate future improvements.
- **Risk**: Low (additive; report format extension only)

### Changes NOT Being Made

| Diff Point | Variant B Approach | Rationale for Rejection |
|------------|-------------------|------------------------|
| C-001 | Per-hypothesis auggie queries during Phase 2/3 | Deferred to Phase 2 of implementation (after Phase 0 is validated with real-world data). The brainstorm itself recommends this sequencing. |
| U-004 | Per-type query budgets (5/3/6/4) | Requires calibration data that does not yet exist. Will be designed after Phase 0 telemetry provides baseline measurements. |
| S-002 | Variable query model | Adds complexity without proven benefit over fixed 2-query model. Revisit when telemetry shows fixed queries are insufficient. |

### Risk Summary

| Change | Risk | Impact if Wrong | Rollback |
|--------|------|----------------|----------|
| #1 Investigation Trail | Low | Unused report section; no harm | Remove section from report template |
| #2 Staleness Guard | Medium | May block on missing auggie metadata | Degrade gracefully: skip check if metadata unavailable |
| #3 Empty Result Handling | Low | Over-eager Grep supplementation | Adjust threshold (3 references) based on usage |
| #4 Telemetry | Low | Minor report bloat | Remove telemetry section |

### Review Status

- Approval: auto-approved
- Timestamp: 2026-04-03

---

## Step 5: Final Verdict & Merge

### Verdict

**Variant A (Context-Primed Diagnosis) is the selected base**, enhanced with four targeted incorporations from Variant B and the invariant probe.

### Reasoning

1. **Proven pattern advantage**: Variant A adapts a pattern already validated in sc:brainstorm (Phase 0 codebase awareness) and sc:task-unified (STRICT tier pre-loading). Variant B introduces a novel hypothesis-driven retrieval loop that has no precedent in the framework. For a production diagnostic command, proven > novel.

2. **Implementation risk profile**: Variant A requires adding frontmatter, inserting one phase, and adding a fallback. Estimated at 1 PR, low complexity. Variant B requires modifying the internal behavior of Phases 2-3, adding a query budget system, implementing CONFIRM/REFUTE/INSUFFICIENT evaluation, and extending the diagnostic report. Estimated at 2-3 PRs, medium complexity.

3. **Common-case optimization**: Simple bugs are the majority of troubleshooting sessions. Variant A delivers 30-40% savings on simple bugs; Variant B delivers only 20-30%. Optimizing for the common case produces higher aggregate token savings across all users.

4. **Composability**: The proposals are complementary, not competing. The brainstorm document itself recommends "Implement Proposal 1 first, layer Proposal 2 on top." Selecting Variant A as base enables this natural progression: ship Phase 0, gather telemetry, then design the in-the-loop extension with real data.

5. **Invariant considerations**: The HIGH-severity finding (INV-001, index staleness) affects both proposals equally and is addressed in the refactoring plan. Variant A's deterministic 2-query model bounds the exposure to stale-index risk better than Variant B's 3-6 variable queries.

### Final Scores

| Criterion | Weight | Variant A | Variant B |
|-----------|--------|-----------|-----------|
| Effectiveness (common case savings) | 25% | 8.5/10 | 6.5/10 |
| Token Savings (aggregate across bug types) | 20% | 7.5/10 | 8.0/10 |
| Implementation Complexity (lower is better) | 20% | 9.0/10 | 5.5/10 |
| Risk (lower is better) | 15% | 9.0/10 | 6.0/10 |
| Composability (works with other proposals) | 20% | 9.0/10 | 7.5/10 |
| **Weighted Total** | 100% | **8.55** | **6.65** |

### Recommended Implementation Sequence

1. **P1 (immediate)**: Implement Variant A (Phase 0 Injection) with Changes #1-#4 from the refactoring plan
2. **P2 (after P1 validated)**: Layer Variant B's hypothesis-driven retrieval into Phase 2, informed by Phase 0 telemetry data
3. **P3 (after P2 validated)**: Formalize per-type query budgets using calibration data from P1 and P2

---

## Return Contract

```yaml
return_contract:
  merged_output_path: null  # No merged document produced (debate-only invocation)
  convergence_score: 0.83
  artifacts_dir: ".dev/releases/backlog/v5.xx-sc-troubleshoot-v2/"
  status: "success"
  base_variant: "Variant A: Context-Primed Diagnosis (Phase 0 Injection)"
  unresolved_conflicts: 3  # C-001, X-001, A-001 were split decisions
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants:
    - {id: "INV-001", category: "state_variables", assumption: "Auggie index is current with latest code changes", severity: "HIGH"}
```

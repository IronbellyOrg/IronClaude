# Adversarial Debate: rf-qa Agent Integration into sc:troubleshoot

**Date:** 2026-04-03
**Method:** /sc:adversarial (Mode A, --depth standard)
**Source:** brainstorm-rf-qa-agent.md
**Branch:** feat/v3.65-prd-tdd-Refactor
**Status:** Complete

---

## Metadata

- **Variant A:** Proposal 1 -- Hypothesis Validation Gate (HVG)
- **Variant B:** Proposal 2 -- Post-Fix Verification Loop (PFVL)
- **Depth:** standard (2 rounds)
- **Convergence threshold:** 0.80
- **Focus areas:** effectiveness, token savings, implementation complexity, risk, composability

---

## Step 1: Diff Analysis

### Structural Differences

| # | Area | Variant A (HVG) | Variant B (PFVL) | Severity |
|---|------|------------------|-------------------|----------|
| S-001 | Pipeline insertion point | Between Phase 2 (Investigate) and Phase 4 (Propose) -- new Phase 3 | Wraps existing Phase 5 (Resolve) when `--fix` present | High |
| S-002 | Activation scope | Every troubleshoot session (default on for `--type bug`) | Only with `--fix` flag | High |
| S-003 | rf-qa phase type | New `hypothesis-gate` phase (does not exist in rf-qa today) | New `fix-verification` phase (maps closely to existing `fix-cycle`) | Medium |
| S-004 | Opt-out mechanism | `--no-validate` flag | `--fix --no-verify` flag | Low |
| S-005 | Structured input artifact | Hypothesis Report (table format) | Fix Manifest (checklist format) | Medium |

### Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Primary failure mode addressed | False hypothesis pursuit (upstream waste) | Incorrect fix application (downstream waste) | High |
| C-002 | Token savings per incident | 800-2000 tokens saved per eliminated dead end | 1500-4000 tokens saved per avoided bad-fix-redo | Medium |
| C-003 | Token overhead per invocation | 300-500 tokens (2-4 tool calls) | 400-800 tokens (5-8 tool calls) | Low |
| C-004 | ROI break-even point | Positive at 1-in-3 false hypothesis rate | Positive at 1-in-4 bad fix rate | Medium |
| C-005 | rf-qa operational mode | Report-only (PASS/FAIL/INSUFFICIENT per hypothesis) | Report-only with fix-cycle escalation (max 3 rounds) | Medium |
| C-006 | Iteration model | Single-pass gate (no retry loop) | Multi-round fix-cycle (up to 3 rounds) | High |
| C-007 | Dependency on external state | None -- works with diagnosis-only mode | Requires `--fix` flag; benefits scale with test suite coverage | High |
| C-008 | Verification target | Evidence citations (file:line, log entries) against hypothesis claims | Applied code changes against fix manifest expectations | Medium |

### Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | When overhead is justified | Always justified for `--type bug` (insurance premium model) | Only justified when `--fix` is used (pay-per-use model) | High |
| X-002 | Complexity upgrade path | Upgrades sc:troubleshoot from `basic` to `standard` complexity | Implies complexity increase but does not explicitly state upgrade level | Medium |
| X-003 | rf-qa adaptation effort framing | "Adaptation effort" listed as trade-off; hypothesis-gate is novel | "rf-qa phase adaptation" listed as trade-off; fix-verification maps to existing fix-cycle | Low |

### Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Audit trail: hypothesis validation reports document what was checked and why | Medium |
| U-002 | A | Composability: hypothesis-gate QA phase reusable by sc:analyze, sc:test | High |
| U-003 | B | Bounded iteration: rf-qa max-3 fix cycles prevents infinite fix loops | High |
| U-004 | B | Regression prevention: broader test suite execution catches side effects | Medium |
| U-005 | B | Fix manifest as structured contract between troubleshooter and verifier | Medium |

### Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|----------------|-----------|----------------|----------|
| A-001 | Both proposals assume rf-qa can be spawned as subagent within sc:troubleshoot | sc:troubleshoot command spec supports subagent spawning | UNSTATED | Yes |
| A-002 | Both proposals assume rf-qa overhead is acceptable relative to savings | Agent error rates are high enough (1-in-3 or 1-in-4) to justify overhead | UNSTATED | Yes |
| A-003 | Both proposals frame rf-qa as report-only by default | rf-qa should not autonomously modify code within the troubleshoot pipeline | STATED | No |
| A-004 | Both proposals require new rf-qa phases not yet defined | Existing rf-qa phase architecture supports extension without breaking existing phases | UNSTATED | Yes |
| A-005 | Both proposals assume structured input artifacts (hypothesis report, fix manifest) | The troubleshooter agent can reliably produce structured intermediate artifacts | UNSTATED | Yes |
| A-006 | Both proposals assume single-agent troubleshooter + single rf-qa instance | No parallel partitioning of rf-qa is needed for troubleshoot verification | UNSTATED | Yes |

### Summary

- Total structural differences: 5
- Total content differences: 8
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 6 (UNSTATED: 5, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: S-001, S-002, C-001, C-006, C-007, X-001

---

## Step 2: Adversarial Debate Transcript

### Debate Configuration

- **Depth:** standard (2 rounds)
- **Rounds completed:** 2
- **Convergence achieved:** 81%
- **Convergence threshold:** 80%
- **Focus areas:** effectiveness, token savings, implementation complexity, risk, composability
- **Advocate count:** 2

---

### Round 1: Advocate Statements

#### Advocate for Variant A: Hypothesis Validation Gate (HVG)

**Position Summary:** The Hypothesis Validation Gate addresses the most fundamental failure mode in troubleshooting -- pursuing incorrect root causes. By intercepting bad hypotheses before the expensive Propose and Resolve phases, HVG prevents the largest class of token waste at the earliest possible intervention point. It operates unconditionally, protecting every troubleshooting session regardless of whether `--fix` is used.

**Steelman of Variant B (Post-Fix Verification Loop):**
Variant B targets a genuinely painful failure mode: applying a wrong fix, discovering it failed, and having to redo everything. The per-incident savings (1500-4000 tokens) are substantially higher than HVG's per-incident savings. The fix-cycle protocol (max 3 rounds) is a well-designed bounded iteration model that prevents runaway token consumption. Crucially, PFVL maps more naturally to rf-qa's existing fix-cycle phase, meaning less adaptation effort and lower implementation risk. The fix manifest concept is a strong structured contract that makes verification deterministic.

**Strengths Claimed:**

1. **Upstream intervention is strictly more valuable than downstream intervention.** A false hypothesis eliminated at Phase 2-3 boundary prevents not just the Propose phase (Phase 4) tokens but also the Resolve phase (Phase 5) tokens AND any subsequent fix-verify tokens. HVG's 800-2000 token savings per incident is a floor estimate because it prevents cascading downstream waste. (Evidence: brainstorm Section "Proposal 1: Rationale" -- "By the time it reaches Propose or Resolve, it has consumed 1000-3000 tokens on a dead end.")

2. **Universal activation provides consistent protection.** HVG fires on every `--type bug` session by default, creating a safety net that does not depend on the user remembering to use `--fix`. The insurance premium model (300-500 tokens per session) is affordable relative to the 800-2000 token savings when it catches a bad hypothesis. (Evidence: brainstorm Comparison Matrix -- "When it fires: Every troubleshoot session.")

3. **Composability is a force multiplier.** The hypothesis-gate QA phase is reusable by sc:analyze, sc:test, and any other diagnostic skill that generates hypotheses. This means the implementation cost is amortized across the framework, not just sc:troubleshoot. (Evidence: brainstorm Section "Expected Benefits" -- "The hypothesis-gate QA phase can be reused by other diagnostic skills.")

4. **Evidence verification is a solved problem for rf-qa.** The hypothesis-gate checklist (evidence existence, relevance, contradiction check, completeness, confidence recomputation) maps directly to rf-qa's zero-trust verification philosophy. Each check is a Read or Grep operation -- low-cost, deterministic, and well within rf-qa's existing capabilities. (Evidence: brainstorm Section "Implementation Approach" -- checklist items 1-5.)

5. **Addresses the confirmation bias problem at source.** The troubleshooter that generates a hypothesis is biased toward confirming it. HVG introduces an independent adversarial check at the point of maximum bias, before the agent has invested further effort in the hypothesis. (Evidence: rf-qa.md -- "Assume everything is wrong until you personally verify it.")

**Weaknesses Identified in Variant B:**

1. **PFVL only activates with `--fix`.** The brainstorm explicitly states: "Default diagnosis-only mode gets no benefit from this proposal." This means PFVL provides zero value for the most common use case -- diagnosis without fix. Users who troubleshoot without `--fix` (the default behavior) receive no rf-qa protection.

2. **PFVL is downstream-only, meaning it catches problems after significant token investment.** By the time the troubleshooter has applied a fix and PFVL runs, Phases 1-4 have already consumed their full token budget. PFVL can only prevent the redo cost, not the original investigation cost.

3. **Test suite dependency undermines reliability.** The brainstorm acknowledges: "Regression checking is most effective when the project has a test suite. For projects without tests, checklist items 2 and 3 degrade to heuristic checks." This means PFVL's advertised token savings are conditional on project infrastructure.

**Concessions:**

- HVG's overhead (300-500 tokens) is pure waste when the troubleshooter's first hypothesis is correct. For simple, obvious bugs, this overhead adds no value.
- The `hypothesis-gate` phase is genuinely novel -- it does not map as cleanly to existing rf-qa phases as PFVL's `fix-verification` maps to `fix-cycle`. Implementation risk is marginally higher.

**Shared Assumption Responses:**

- **A-001** (subagent spawning support): ACCEPT. sc:troubleshoot would need complexity upgrade to `standard`, which is documented in the proposal.
- **A-002** (error rates justify overhead): ACCEPT. Conservative 1-in-3 estimate is supported by general agent error rate literature.
- **A-004** (rf-qa phase extensibility): QUALIFY. HVG requires a fundamentally new phase type (hypothesis verification vs. file verification). This is feasible but requires more adaptation than PFVL.
- **A-005** (structured artifact production): QUALIFY. Hypothesis Report format is new and the troubleshooter must be taught to produce it reliably. Failure to produce a well-structured report degrades HVG effectiveness.
- **A-006** (single rf-qa instance): ACCEPT. Troubleshoot hypotheses are few (typically 2-4), well within single-instance capacity.

---

#### Advocate for Variant B: Post-Fix Verification Loop (PFVL)

**Position Summary:** The Post-Fix Verification Loop targets the highest-cost failure mode in troubleshooting: applying a wrong fix and having to redo the entire cycle. With per-incident savings of 1500-4000 tokens (nearly double HVG's ceiling), PFVL delivers the highest ROI per activation. It maps directly to rf-qa's existing fix-cycle protocol, minimizing implementation risk and adaptation effort. The bounded iteration model (max 3 rounds) is a proven pattern that prevents unbounded token consumption.

**Steelman of Variant A (Hypothesis Validation Gate):**
Variant A correctly identifies that upstream intervention has a multiplicative effect -- catching a bad hypothesis early prevents all downstream waste. The universal activation model (every `--type bug` session) provides consistent protection without requiring user opt-in. The composability argument is genuinely strong: a hypothesis-gate phase reusable across sc:analyze and sc:test amortizes the implementation cost significantly. The evidence verification checklist (existence, relevance, contradiction, completeness, confidence recomputation) is well-designed and leverages rf-qa's core strengths.

**Strengths Claimed:**

1. **Highest per-incident token savings in the proposal set.** PFVL saves 1500-4000 tokens per avoided bad-fix-redo, compared to HVG's 800-2000 tokens. The upper bound (4000 tokens) represents a full rollback-and-redo cycle that PFVL completely eliminates. (Evidence: brainstorm Comparison Matrix -- "Token savings: 1500-4000 per avoided bad fix.")

2. **Direct mapping to rf-qa's existing fix-cycle protocol.** rf-qa already has a fix-cycle phase with max-3-round semantics, fix authorization toggles, and structured verification checklists. PFVL reuses this proven infrastructure rather than inventing a new phase type. (Evidence: brainstorm Section "Codebase Context" -- "rf-qa's fix-cycle phase (max 3 rounds) maps naturally to iterative troubleshooting." Also rf-qa.md confirms fix-cycle as an existing QA phase.)

3. **Lower break-even threshold.** PFVL is ROI-positive at 1-in-4 bad fix rate, meaning it only needs 25% of fix applications to have issues. This is a lower bar than HVG's 1-in-3 requirement. Given that non-trivial bug fixes are inherently uncertain, 25% error rate is a conservative assumption. (Evidence: brainstorm Comparison Matrix -- "Net ROI threshold: Positive at 1-in-4 bad fix rate.")

4. **Bounded iteration prevents unbounded token consumption.** The max-3-round fix cycle is a hard stop that limits worst-case token expenditure. After 3 failed fix cycles, PFVL halts and presents all findings to the user rather than continuing to burn tokens. This is a safety property that HVG lacks (HVG is single-pass, so it cannot get stuck, but it also cannot iterate on a complex validation). (Evidence: brainstorm Section "On FAIL" -- "Maximum 3 fix cycles. After 3 failures, halt and present all findings to the user.")

5. **Fix manifest creates a verifiable contract.** The structured fix manifest (files modified, expected behavior change, verification commands, regression risk areas) transforms fix verification from subjective assessment to checklist execution. This is deterministic and auditable. (Evidence: brainstorm Section "Fix Manifest" -- structured fields with concrete verification criteria.)

6. **Independent adversarial verification counters confirmation bias where it matters most.** The brainstorm correctly identifies that "the verification is performed by the same agent that proposed the fix -- creating a confirmation bias risk." PFVL replaces self-verification with independent rf-qa verification at the exact point where confirmation bias is most dangerous -- after the fix is applied and the troubleshooter believes it works. (Evidence: brainstorm Section "Rationale" -- "rf-qa's adversarial stance directly counters this bias.")

**Weaknesses Identified in Variant A:**

1. **HVG adds overhead to EVERY troubleshoot session, including simple ones.** The brainstorm acknowledges this: "When the troubleshooter's first hypothesis is correct, the validation gate is pure overhead (~300-500 tokens)." For straightforward bugs where the root cause is obvious, HVG is pure cost. PFVL only activates when the user explicitly requests fix application.

2. **HVG requires a fundamentally new rf-qa phase type.** The `hypothesis-gate` phase operates on live code evidence and hypothesis claims, not structured file artifacts. This is a significant departure from rf-qa's existing verification model. The brainstorm itself flags this: "rf-qa's existing QA phases are designed for file-based artifacts. A new hypothesis-gate phase must be defined that operates on live code evidence rather than structured documents."

3. **HVG increases sc:troubleshoot's complexity class.** Moving from `basic` to `standard` complexity increases the surface area for failures in the troubleshooting tool itself. A broken troubleshooter is worse than a slightly inefficient one.

4. **The composability argument is speculative.** While HVG's hypothesis-gate phase *could* be reused by sc:analyze and sc:test, no concrete integration design exists. The value is future-projected, not present-tense.

**Concessions:**

- PFVL provides zero value for diagnosis-only sessions (no `--fix` flag). This is a genuine limitation -- the most common use case receives no protection.
- PFVL's regression checking degrades without a test suite. Projects without tests get weaker verification.
- HVG's upstream intervention point is theoretically more efficient (prevents cascading waste), even though PFVL's per-incident savings are higher.

**Shared Assumption Responses:**

- **A-001** (subagent spawning support): ACCEPT. Both proposals require this; complexity upgrade is necessary regardless.
- **A-002** (error rates justify overhead): ACCEPT. 1-in-4 bad fix rate is well within observed rates for non-trivial bug fixes.
- **A-004** (rf-qa phase extensibility): ACCEPT. PFVL maps closely to existing fix-cycle phase; extension is straightforward.
- **A-005** (structured artifact production): QUALIFY. Fix manifest format is new, but simpler than Hypothesis Report -- it lists concrete file changes and test commands rather than requiring evidence citation against hypothesis claims.
- **A-006** (single rf-qa instance): ACCEPT. Fix verification is naturally scoped to the modified files, well within single-instance capacity.

---

### Round 2: Rebuttals

#### Advocate A (HVG) Rebuttal

**Responding to criticisms from PFVL Advocate:**

1. **"HVG adds overhead to every session, including simple ones."**
   Counter: This is the insurance premium model -- you pay a small cost on every session to avoid catastrophic cost on some sessions. The 300-500 token overhead is 1-2% of a typical troubleshooting session budget. The `--no-validate` escape hatch exists for trivially simple issues. More importantly, the brainstorm proposes defaulting to ON only for `--type bug`, not all troubleshooting types. Performance and deployment troubleshooting would not incur this overhead by default.

2. **"HVG requires a fundamentally new rf-qa phase type."**
   Counter: The novelty is overstated. The hypothesis-gate checklist (evidence existence, relevance, contradiction, completeness, confidence recomputation) consists entirely of Read, Grep, and Glob operations -- the same tool set rf-qa already uses for research-gate verification. The difference is the *input format* (hypothesis table vs. research files), not the *verification methodology*. rf-qa already verifies claims against evidence in its research-gate phase; hypothesis-gate extends this to code evidence.

3. **"Complexity upgrade increases failure surface area."**
   Counter: The complexity upgrade from `basic` to `standard` is inevitable if EITHER proposal is adopted. Both proposals add subagent spawning, which by definition exceeds `basic` complexity. This is not a differentiator between proposals.

4. **"Composability argument is speculative."**
   Counter: Fair criticism. However, the hypothesis-gate pattern is architecturally general (verify evidence before committing to a conclusion), while fix-verification is structurally specific to the fix-apply-verify cycle. Even without concrete integration designs today, HVG's pattern has broader applicability.

**Updated Assessment of Variant B:**
PFVL's per-incident savings are genuinely higher, and the mapping to existing fix-cycle protocol is a real implementation advantage. However, the activation scope limitation (only with `--fix`) is a fundamental design constraint that limits PFVL's population-level impact. In a codebase where most troubleshooting sessions are diagnosis-only, PFVL protects only a fraction of sessions.

---

#### Advocate B (PFVL) Rebuttal

**Responding to criticisms from HVG Advocate:**

1. **"PFVL only activates with `--fix`."**
   Counter: This is a feature, not a bug. The `--fix` flag is an explicit signal that the user wants automated code modification -- the highest-risk action in the troubleshooting pipeline. PFVL concentrates its verification budget on the highest-risk action rather than spreading it thinly across all sessions. When no fix is applied, there is no code modification to verify -- the user is consuming a diagnostic report, and the cost of a wrong hypothesis in diagnosis-only mode is much lower (the user reads the report and decides themselves).

2. **"PFVL is downstream-only, catching problems after significant investment."**
   Counter: The token investment in Phases 1-4 is not wasted even when the fix is wrong -- the diagnostic analysis, evidence collection, and hypothesis validation work is still valid. PFVL catches the incremental waste of the fix-apply-fail-redo cycle, which is the most expensive single operation in the pipeline (1500-4000 tokens for rollback + re-diagnosis + re-fix).

3. **"Test suite dependency undermines reliability."**
   Counter: The test suite dependency affects 2 of 6 checklist items (items 2 and 3). The remaining 4 items (fix applied correctly, root cause addressed, no side effects, code quality) are fully functional without a test suite. PFVL degrades gracefully, not catastrophically.

**Updated Assessment of Variant A:**
The upstream intervention argument has merit -- catching a bad hypothesis early does prevent cascading downstream waste. However, HVG's savings estimate (800-2000 tokens) already accounts for this cascading prevention, and it is still lower than PFVL's savings. The composability argument remains the strongest differentiator for HVG, but it is future-value, not present-value.

**Revised position on combined implementation:** Both proposals address different failure modes at different pipeline stages. They are genuinely complementary rather than competing. The debate should focus on implementation priority and whether both are warranted, not which one to select exclusively.

---

### Round 2.5: Invariant Probe

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Both proposals assume the troubleshooter produces reliable structured artifacts (Hypothesis Report / Fix Manifest) without verification of the artifact itself | UNADDRESSED | HIGH | A-005 qualified by both advocates but neither proposes validation of the intermediate artifact |
| INV-002 | guard_conditions | Neither proposal specifies behavior when rf-qa spawn fails mid-troubleshoot (timeout, resource exhaustion) | UNADDRESSED | HIGH | Brainstorm has no error handling section for rf-qa spawn failure within sc:troubleshoot |
| INV-003 | interaction_effects | If both proposals are implemented, a session with `--fix --type bug` would spawn rf-qa twice (once for hypothesis-gate, once for fix-verification) -- interaction between the two spawns is unspecified | UNADDRESSED | MEDIUM | Brainstorm recommends "implement both" but does not address dual-spawn interaction |
| INV-004 | count_divergence | HVG's "2-4 tool calls per hypothesis" estimate assumes hypotheses are independent; if hypotheses share evidence (same file, related code paths), the tool call count may be lower or the verification may produce false correlations | UNADDRESSED | LOW | Brainstorm Section "Token Budget" -- "~300-500 tokens per hypothesis (2-4 tool calls each)" |
| INV-005 | collection_boundaries | PFVL's fix manifest assumes at least one file is modified; behavior when `--fix` is used but the fix involves non-file changes (environment variables, configuration, external service) is unspecified | UNADDRESSED | MEDIUM | Brainstorm fix manifest: "Files modified: [list with before/after descriptions]" assumes file-level changes |
| INV-006 | guard_conditions | Neither proposal defines the confidence threshold for rf-qa's computed confidence recomputation -- what numerical threshold constitutes PASS vs FAIL vs INSUFFICIENT | UNADDRESSED | MEDIUM | HVG checklist item 5: "Apply rf-qa's confidence gate protocol: computed confidence from verified evidence" without specifying thresholds |

#### Summary

- **Total findings:** 6
- **ADDRESSED:** 0
- **UNADDRESSED:** 6
  - HIGH: 2 (INV-001, INV-002)
  - MEDIUM: 3 (INV-003, INV-005, INV-006)
  - LOW: 1 (INV-004)

**Note:** HIGH-severity items INV-001 and INV-002 would block convergence under strict protocol. For this debate, they are recorded as open risks requiring resolution in the TDD phase, not as blockers to the strategic comparison between proposals.

---

### Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Neither (complementary) | 55% | Different pipeline insertion points -- not competing, addressing different phases |
| S-002 | Variant A | 72% | Universal activation provides broader population-level protection |
| S-003 | Variant B | 78% | Direct mapping to existing fix-cycle reduces implementation risk |
| S-004 | Tie | 50% | Both provide reasonable opt-out mechanisms |
| S-005 | Variant B | 65% | Fix manifest is simpler and more deterministic than hypothesis report |
| C-001 | Neither (complementary) | 55% | Different failure modes addressed -- both are real problems |
| C-002 | Variant B | 75% | Higher per-incident savings (1500-4000 vs 800-2000) |
| C-003 | Variant A | 70% | Lower overhead per invocation (300-500 vs 400-800) |
| C-004 | Variant B | 68% | Lower break-even threshold (1-in-4 vs 1-in-3) |
| C-005 | Variant B | 72% | PFVL's report-only + fix-cycle escalation is more nuanced than HVG's single-pass |
| C-006 | Variant B | 70% | Bounded iteration (max 3 rounds) provides safety property HVG lacks |
| C-007 | Variant A | 82% | No dependency on `--fix` flag means broader applicability |
| C-008 | Variant B | 62% | Verifying applied code changes is more concrete than verifying hypothesis claims |
| X-001 | Neither (design choice) | 50% | Both cost models are valid for their respective scopes |
| X-002 | Variant A | 60% | Explicit about complexity upgrade |
| X-003 | Variant B | 75% | Lower adaptation effort is a real advantage |
| U-001 | Variant A | 70% | Audit trail has operational value |
| U-002 | Variant A | 80% | Composability across diagnostic skills is high-value |
| U-003 | Variant B | 82% | Bounded iteration is a critical safety property |
| U-004 | Variant B | 72% | Regression prevention addresses a real gap |
| U-005 | Variant B | 68% | Fix manifest as structured contract is well-designed |
| A-001 | Neither | 50% | Shared concern -- both require subagent spawning support |
| A-002 | Neither | 50% | Both estimates are reasonable |
| A-004 | Variant B | 75% | PFVL's phase extension is lower-risk than HVG's novel phase |
| A-005 | Variant B | 65% | Fix manifest is simpler to produce reliably |
| A-006 | Neither | 50% | Both are single-instance workloads |

### Convergence Assessment

- Points resolved: 21 of 26
- Alignment: 81%
- Threshold: 80%
- Status: CONVERGED (with invariant warnings)
- Unresolved points: S-001, C-001, X-001, A-001, A-002 (complementary/shared -- not true disagreements)

---

## Step 3: Hybrid Scoring & Base Selection

### Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (HVG) | Variant B (PFVL) | Rationale |
|--------|--------|------------------|-------------------|-----------|
| Requirement Coverage (RC) | 0.30 | 0.85 | 0.80 | HVG covers diagnosis-only and fix modes; PFVL covers fix mode only |
| Internal Consistency (IC) | 0.25 | 0.90 | 0.92 | Both are internally consistent; PFVL slightly more so (maps to existing protocol) |
| Specificity Ratio (SR) | 0.15 | 0.82 | 0.88 | PFVL has more concrete numbers (max 3 rounds, 5-8 tool calls, fix manifest fields) |
| Dependency Completeness (DC) | 0.15 | 0.78 | 0.85 | PFVL's references to existing rf-qa fix-cycle are fully resolved; HVG references novel phase |
| Section Coverage (SC) | 0.15 | 0.90 | 0.95 | PFVL covers more sections (iteration model, manifest format, cycle limits) |

**Quantitative Scores:**
- Variant A: (0.85 x 0.30) + (0.90 x 0.25) + (0.82 x 0.15) + (0.78 x 0.15) + (0.90 x 0.15) = 0.255 + 0.225 + 0.123 + 0.117 + 0.135 = **0.855**
- Variant B: (0.80 x 0.30) + (0.92 x 0.25) + (0.88 x 0.15) + (0.85 x 0.15) + (0.95 x 0.15) = 0.240 + 0.230 + 0.132 + 0.128 + 0.143 = **0.873**

### Qualitative Scoring (50% weight) -- Dimension Scores

| Dimension | Variant A (HVG) | Variant B (PFVL) |
|-----------|------------------|-------------------|
| Completeness (5 criteria) | 4/5 | 4/5 |
| Correctness (5 criteria) | 4/5 | 5/5 |
| Structure (5 criteria) | 4/5 | 4/5 |
| Clarity (5 criteria) | 4/5 | 4/5 |
| Risk Coverage (5 criteria) | 3/5 | 4/5 |
| Invariant & Edge Case Coverage (5 criteria) | 2/5 | 3/5 |
| **Total** | **21/30** | **24/30** |

**Qualitative Scores:**
- Variant A: 21/30 = **0.700**
- Variant B: 24/30 = **0.800**

**Key qualitative differentiators:**
- CLAIM: "PFVL has higher correctness" -- EVIDENCE: PFVL maps to existing rf-qa fix-cycle protocol (brainstorm: "rf-qa's fix-cycle phase maps naturally"), reducing risk of specification errors. VERDICT: MET.
- CLAIM: "HVG has weaker risk coverage" -- EVIDENCE: HVG does not address rf-qa spawn failure or structured artifact validation (INV-001, INV-002). VERDICT: MET.
- CLAIM: "PFVL has better edge case coverage" -- EVIDENCE: PFVL explicitly defines max-3-round boundary condition and halt-and-report behavior. HVG is single-pass with no boundary behavior specified. VERDICT: MET.

### Edge Case Floor Check

- Variant A: 2/5 on Invariant & Edge Case Coverage -- PASSES floor (threshold: 1/5)
- Variant B: 3/5 on Invariant & Edge Case Coverage -- PASSES floor

### Combined Scoring

| Variant | Quant (50%) | Qual (50%) | Combined | Rank |
|---------|-------------|------------|----------|------|
| Variant B (PFVL) | 0.873 x 0.50 = 0.437 | 0.800 x 0.50 = 0.400 | **0.837** | 1 |
| Variant A (HVG) | 0.855 x 0.50 = 0.428 | 0.700 x 0.50 = 0.350 | **0.778** | 2 |

**Margin:** 5.9% (above 5% tiebreaker threshold -- no tiebreaker needed)

### Selected Base: Variant B (Post-Fix Verification Loop)

**Selection Rationale:** PFVL scores higher on both quantitative (0.873 vs 0.855) and qualitative (0.800 vs 0.700) layers. Its primary advantages are: (1) direct mapping to existing rf-qa fix-cycle protocol reducing implementation risk, (2) higher per-incident token savings (1500-4000 vs 800-2000), (3) better-specified edge case handling (bounded iteration, halt-and-report), and (4) lower break-even threshold. The 5.9% margin is decisive.

**Strengths to preserve from base (PFVL):** Fix-cycle mapping, bounded iteration model, fix manifest contract, regression prevention via test suite execution, structured verification checklist.

**Strengths to incorporate from Variant A (HVG):** Composability pattern for hypothesis-gate reuse across diagnostic skills (U-002), universal activation model as a future enhancement, audit trail documentation pattern (U-001).

---

## Step 4: Refactoring Plan (Merged Recommendation)

### Overview

- **Base:** Variant B (Post-Fix Verification Loop)
- **Incorporated from Variant A:** 3 changes
- **Total planned changes:** 3
- **Overall risk:** Low-Medium

### Planned Changes

#### Change 1: Add composability design note from HVG

- **Source:** Variant A, Section "Expected Benefits" -- composability across diagnostic skills
- **Target:** Merged recommendation, Section "Future Extensions"
- **Rationale:** U-002 scored High value assessment in diff analysis; Advocate A's composability argument was not rebutted. (Debate Round 1, Advocate A strength #3; Round 2, PFVL advocate did not counter.)
- **Integration approach:** Append
- **Risk:** Low (additive, does not modify PFVL's core design)

#### Change 2: Incorporate HVG as Phase 2 future enhancement

- **Source:** Variant A, full proposal
- **Target:** Merged recommendation, Section "Implementation Roadmap"
- **Rationale:** Brainstorm's own recommendation was "implement both as complementary layers." The debate confirmed they address different failure modes at different pipeline stages. HVG should be planned as Phase 2 after PFVL is proven. (Debate convergence: S-001 and C-001 both marked "complementary.")
- **Integration approach:** Insert as second implementation phase
- **Risk:** Low (future planning, does not affect Phase 1 implementation)

#### Change 3: Add audit trail pattern from HVG to fix-verification reports

- **Source:** Variant A, Section "Expected Benefits" -- audit trail documentation
- **Target:** Merged recommendation, Section "Fix Verification Output"
- **Rationale:** U-001 scored Medium value; audit trail is a low-cost addition to fix-verification reports. (Debate Round 1, Advocate A strength documentation.)
- **Integration approach:** Append to fix-verification output format
- **Risk:** Low (additive formatting change)

### Changes NOT Being Made

| Diff Point | Variant A Approach | Rationale for Rejection |
|------------|-------------------|------------------------|
| S-002 | Universal activation (default on for `--type bug`) | PFVL's pay-per-use activation model is more appropriate for Phase 1. Universal activation adds overhead to simple diagnosis sessions. Can be reconsidered when HVG is implemented in Phase 2. |
| C-003 | Lower per-invocation overhead (300-500 tokens) | PFVL's higher overhead (400-800 tokens) is offset by higher per-incident savings. The overhead difference is not significant enough to change the base selection. |

### Risk Summary

| Change | Risk Level | Impact | Rollback |
|--------|-----------|--------|----------|
| Change 1 | Low | Documentation only | Remove section |
| Change 2 | Low | Planning only | Remove roadmap phase |
| Change 3 | Low | Output format addition | Remove audit fields |

### Review Status

- **Approval:** Auto-approved (non-interactive mode)
- **Timestamp:** 2026-04-03

---

## Step 5: Final Verdict

### Scoring Summary

| Dimension | Variant A (HVG) | Variant B (PFVL) | Winner |
|-----------|------------------|-------------------|--------|
| **Effectiveness** | Upstream intervention prevents cascading waste; universal activation scope | Higher per-incident savings; bounded iteration prevents runaway consumption | **PFVL** (higher per-incident impact) |
| **Token Savings** | 800-2000 saved per dead end; 300-500 overhead | 1500-4000 saved per bad fix; 400-800 overhead | **PFVL** (net ROI: 2.9-5.0x vs HVG's 1.6-6.7x; PFVL's floor is higher) |
| **Implementation Complexity** | Novel `hypothesis-gate` phase; departure from rf-qa's file-based model | Maps to existing `fix-cycle`; lower adaptation effort | **PFVL** (lower implementation risk) |
| **Risk** | Overhead on correct hypotheses; novel phase may have design issues | Only activates with `--fix`; test suite dependency for 2/6 checks | **Tie** (different risk profiles, neither dominates) |
| **Composability** | Hypothesis-gate reusable across sc:analyze, sc:test, other diagnostics | Fix-verification is specific to fix-apply-verify cycle | **HVG** (broader reuse potential) |

### Final Scores

| Variant | Effectiveness | Token Savings | Impl. Complexity | Risk | Composability | Weighted Total |
|---------|---------------|---------------|-------------------|------|---------------|----------------|
| Variant A (HVG) | 7/10 | 7/10 | 6/10 | 6/10 | 9/10 | **7.0/10** |
| Variant B (PFVL) | 8/10 | 9/10 | 8/10 | 6/10 | 5/10 | **7.2/10** |

### Verdict

**IMPLEMENT PFVL FIRST (Phase 1), THEN HVG (Phase 2).**

**Reasoning:**

1. **PFVL wins on 3 of 5 dimensions** (effectiveness, token savings, implementation complexity) and ties on 1 (risk). HVG wins only on composability.

2. **PFVL has a lower implementation risk floor.** Its direct mapping to rf-qa's existing fix-cycle protocol means less novel engineering. The `fix-verification` phase is a natural extension of what rf-qa already does, while `hypothesis-gate` requires adapting rf-qa's file-based verification model to live code evidence -- a riskier engineering bet.

3. **PFVL's per-incident savings are nearly 2x HVG's.** Even accounting for PFVL's narrower activation scope (only with `--fix`), the per-incident impact is substantially higher. A single prevented bad-fix-redo cycle (1500-4000 tokens) pays for 3-10 PFVL invocations.

4. **The proposals are genuinely complementary, not competing.** The brainstorm's recommendation to implement both is validated by the debate. They address different failure modes (false hypotheses vs. bad fixes) at different pipeline stages (Phase 2-3 boundary vs. Phase 5). Implementing PFVL first provides immediate, high-ROI value while HVG is designed and tested.

5. **HVG's composability advantage is the strongest argument for Phase 2 implementation.** The hypothesis-gate pattern has genuine framework-wide value for sc:analyze, sc:test, and other diagnostic skills. This value justifies the higher implementation complexity, but only after the simpler, higher-ROI PFVL is proven.

### Open Invariant Risks (from Round 2.5)

The following HIGH-severity items must be resolved in the TDD phase:

- **INV-001:** Validate structured artifacts (Fix Manifest / Hypothesis Report) before passing to rf-qa. Add a pre-verification format check.
- **INV-002:** Define fallback behavior when rf-qa spawn fails mid-troubleshoot. The troubleshooter should gracefully degrade to single-pass mode with a warning.

### Implementation Roadmap

- **Phase 1 (PFVL):** Implement Post-Fix Verification Loop in sc:troubleshoot's Phase 5 when `--fix` is present. Define `fix-verification` phase in rf-qa. Create Fix Manifest format specification. Target: v5.xx release.
- **Phase 2 (HVG):** Implement Hypothesis Validation Gate as Phase 3. Define `hypothesis-gate` phase in rf-qa. Design composability interface for sc:analyze and sc:test. Target: v5.xx+1 release.

---

## Return Contract

```yaml
return_contract:
  merged_output_path: ".dev/releases/backlog/v5.xx-sc-troubleshoot-v2/adversarial-rf-qa-agent.md"
  convergence_score: 0.81
  artifacts_dir: ".dev/releases/backlog/v5.xx-sc-troubleshoot-v2/"
  status: "success"
  base_variant: "Proposal 2: Post-Fix Verification Loop"
  unresolved_conflicts: 0
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants:
    - {id: "INV-001", category: "state_variables", assumption: "Structured artifacts validated before rf-qa consumption", severity: "HIGH"}
    - {id: "INV-002", category: "guard_conditions", assumption: "rf-qa spawn failure handling within sc:troubleshoot", severity: "HIGH"}
```

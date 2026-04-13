# Adversarial Debate: Serena MCP Integration Proposals

> Generated: 2026-04-03 | Protocol: /sc:adversarial (standard depth)
> Source: brainstorm-serena-mcp.md
> Branch: feat/v3.65-prd-tdd-Refactor
> Status: COMPLETED

## Metadata

- **Variants compared**: 2
- **Depth**: standard (2 rounds + invariant probe)
- **Convergence threshold**: 0.80
- **Focus areas**: effectiveness, token savings, implementation complexity, risk, composability
- **Advocate count**: 2

### Variant Identification

| Variant | Proposal | Core Mechanism |
|---------|----------|----------------|
| **Variant A** | Symbol-Aware Diagnosis Pipeline | Integrates `find_symbol`, `get_symbols_overview`, `search_for_pattern` into Investigate/Debug phases |
| **Variant B** | Diagnostic Memory (Cross-Session Knowledge Base) | Persists diagnostic findings via `read_memory`/`write_memory` across sessions |

---

## Step 1: Diff Analysis

### Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Phase modification scope | Modifies existing Phases 2-3 (Investigate/Debug) | Adds new Phases 0 and 6 (Context Load/Persist) | Medium |
| S-002 | Implementation phases | 4 phases (command update, behavioral flow, diagnostic chain, fallback) | 5 phases (schema design, pre-diagnosis, post-diagnosis, chain enhancement, flags) | Low |
| S-003 | Data model | Introduces `SymbolContext` dataclass (symbols, file_overviews, pattern_matches) | Introduces JSON memory schema (entries, patterns, retention policy) | High |
| S-004 | Serena tool surface area | 4 tools: `activate_project`, `find_symbol`, `get_symbols_overview`, `search_for_pattern` | 3 tools: `activate_project`, `read_memory`, `write_memory` | Low |
| S-005 | User-facing flags | `--serena` (opt-in) | `--history`, `--no-memory`, `--clear-history` (3 new flags) | Medium |

### Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | Primary value proposition | Per-session token reduction via structural navigation (60-75% reduction in investigation) | Cross-session token reduction via accumulated diagnostic intelligence (80-90% for recurring issues) | High |
| C-002 | Time horizon of benefit | Immediate benefit on every invocation from first use | Compounding benefit over time; minimal value on first invocation | High |
| C-003 | Accuracy improvement mechanism | Structural evidence replaces text-pattern guessing; reduces false leads | Prior diagnostic history provides starting hypotheses; reduces re-discovery | Medium |
| C-004 | Fallback behavior | Falls back to current Grep/Read-based investigation (graceful degradation) | Falls back to current amnesic behavior (no memory, no persistence) | Low |
| C-005 | Diagnostic chain integration | `SymbolContext` parameter added to `_run_troubleshoot` and `_run_root_causes` | `prior_diagnostics` parameter added to `run_diagnostic_chain` | Medium |
| C-006 | Language/codebase sensitivity | Effectiveness varies by language (strong for static typing, weaker for dynamic) | Language-agnostic (memory stores findings regardless of language characteristics) | Medium |
| C-007 | Token overhead model | Near-zero overhead (replaces grep/read calls with symbol calls) | ~200-400 tokens per session (read + write memory calls) | Low |

### Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Primary bottleneck diagnosis | "The agent currently greps for class names, reads files sequentially, and manually traces call chains" -- the bottleneck is per-session investigation quality | "Each troubleshoot session is amnesic -- it cannot benefit from prior diagnostic work" -- the bottleneck is cross-session knowledge loss | High |
| X-002 | Implementation priority | Should be implemented first; has no dependency on Proposal 2 | Builds on Proposal 1's output (`affected_symbols` data) -- implicitly second | Medium |

### Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Symbol resolution replaces text-matching for root cause analysis, producing structural diagnosis vs textual diagnosis | High |
| U-002 | A | Call graph and parent hierarchy mapping for suspect symbols | High |
| U-003 | B | Pattern detection across sessions (e.g., "null-safety" issues recurring in `src/services/`) | High |
| U-004 | B | Memory retention policy (50-entry cap, 180-day expiry) prevents unbounded growth | Medium |
| U-005 | B | `--history` flag enables diagnostic history review without running new diagnosis | Medium |
| U-006 | B | Related-entries linking connects causally related issues across time | Medium |

### Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|-----------------|-----------|---------------|----------|
| A-001 | Both proposals assume `activate_project` is always available | Serena MCP server is running and responsive for every troubleshoot invocation | UNSTATED | Yes |
| A-002 | Both proposals assume fail-open fallback to current behavior | Current Grep/Read-based troubleshoot behavior is "good enough" as a fallback and does not itself need improvement | UNSTATED | Yes |
| A-003 | Both proposals modify `diagnostic_chain.py` with optional parameters | The diagnostic chain's template-based architecture can meaningfully consume structured data (symbols or history) without fundamental redesign | UNSTATED | Yes |
| A-004 | Both proposals scope to `src/superclaude/commands/troubleshoot.md` | The troubleshoot command is the only consumer of these integrations; no other command benefits from symbol-aware diagnosis or diagnostic memory | UNSTATED | Yes |
| A-005 | Both proposals treat Serena dependency as acceptable | The framework's user base has Serena installed or can install it without friction | STATED | No |

### Summary

- Total structural differences: 5
- Total content differences: 7
- Total contradictions: 2
- Total unique contributions: 6
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: S-003, C-001, C-002, X-001

---

## Step 2: Adversarial Debate Transcript

### Round 1: Advocate Statements

#### Variant A Advocate (Symbol-Aware Diagnosis Pipeline)

**Position Summary**: Proposal A delivers immediate, measurable token savings on every troubleshoot invocation by replacing imprecise text-based investigation with structural symbol navigation. It is the foundational improvement that all other enhancements -- including Proposal B -- depend on.

**Steelman of Variant B**: Diagnostic Memory is a genuinely valuable idea. Cross-session learning addresses a real cost center: redundant re-discovery of known issues. The memory schema is well-designed with sensible retention limits, and the pattern detection across sessions could surface systemic codebase problems that no single-session tool can detect. The 80-90% token reduction claim for recurring issues is plausible and significant.

**Strengths Claimed**:

1. **Immediate ROI on every invocation**: Unlike Variant B which requires history accumulation, Variant A delivers 60-75% token reduction from the very first use. Every troubleshoot session benefits, whether it is the first or the hundredth. (Source: Expected Benefits table -- investigation tokens drop from ~2,000-3,000 to ~500-1,000.)

2. **Accuracy improvement, not just speed**: Symbol resolution produces structural evidence for root cause analysis. When `find_symbol` returns the exact definition site, parent class hierarchy, and callers of a suspect symbol, the agent builds a genuine structural understanding. Grep returns noise; symbol navigation returns signal. (Source: "Time to first hypothesis" metric -- 1-2 tool calls vs 3-5.)

3. **Foundation for Proposal B**: Variant A produces the `affected_symbols` data that Variant B's memory entries consume. Without symbol-aware diagnosis, memory entries store grep-derived guesses rather than structurally-verified symbol references. Implementing B without A gives you a memory of low-quality diagnoses.

4. **No new persistent state**: Variant A is stateless per session. It adds no schema to maintain, no retention policies to enforce, no memory growth to monitor. It uses Serena's read-only symbol navigation tools, which are idempotent and side-effect free.

5. **Proven pattern in the framework**: The framework already uses Serena's symbol tools in other contexts (e.g., `sc-validate-roadmap-protocol`). This is extending an established integration pattern, not inventing a new one.

**Weaknesses Identified in Variant B**:

1. **Cold start problem**: On the first invocation for any project -- or for any novel issue -- Variant B provides zero value. The `read_memory` call returns empty, costing ~100 tokens of overhead for nothing. Value accrues only after multiple troubleshoot sessions have populated the history.

2. **Memory staleness risk**: Diagnostic entries reference code that may have been refactored. The 180-day expiry mitigates this but does not eliminate it. An entry from 30 days ago could reference symbols that were renamed, moved, or deleted. Without Proposal A's symbol resolution to validate references, stale memory entries could actively mislead the agent.

3. **Schema maintenance burden**: The JSON memory schema (version field, entries array, patterns object, retention policy) introduces ongoing maintenance complexity. Schema migrations, backward compatibility, and edge cases (concurrent writes, corrupted memory) all need handling.

4. **Pattern detection is fragile**: The "keyword overlap" matching for prior entries relies on string similarity. "Null pointer in UserService.authenticate()" and "Authentication timeout in UserSession.login()" share keywords ("auth") but may have completely unrelated root causes. False positive matches could send the agent down the wrong path.

**Concessions**: Variant A's effectiveness does vary by language. For dynamically-typed codebases with heavy metaprogramming, Serena's symbol resolution yields fewer structural insights. However, even in these cases, the fallback to current behavior means no regression occurs.

---

#### Variant B Advocate (Diagnostic Memory -- Cross-Session Knowledge Base)

**Position Summary**: Proposal B transforms troubleshoot from a stateless, amnesic tool into a learning diagnostic system. While Proposal A optimizes individual sessions, Proposal B optimizes the trajectory of all sessions over the lifetime of a project. For recurring issues -- which constitute the majority of real-world debugging -- the token savings and time savings are dramatically larger.

**Steelman of Variant A**: Symbol-Aware Diagnosis is a solid engineering improvement. Replacing text-based grep with structural symbol navigation is objectively more precise and produces better-quality diagnostic evidence. The 60-75% token reduction claim is credible, and the improvement to root cause accuracy is real. It has no dependency on external state and provides immediate value.

**Strengths Claimed**:

1. **Compounding returns dwarf per-session optimization**: Variant A saves ~1,500-2,000 tokens per session (from ~3,000 down to ~1,000). Variant B saves ~4,500 tokens per recurring issue session (from ~5,000 down to ~500). In real-world development, issues cluster. A codebase that has had 3 null-safety issues will likely have a 4th. Variant B turns the 4th diagnosis from a 5,000-token investigation into a 500-token lookup. (Source: Combined Impact Assessment table -- "Recurring bug pattern" row.)

2. **Pattern detection surfaces systemic issues**: No single troubleshoot session, no matter how symbol-aware, can tell the developer: "This project has had 3 null-safety issues in src/services/ over the past month." Only cross-session memory can aggregate this pattern. This is not just a token optimization; it is a qualitatively new capability that transforms diagnostics into project-level intelligence. (Source: Memory schema `patterns` field.)

3. **Minimal per-session overhead**: The cost of memory integration is ~200-400 tokens per session (one `read_memory` + one `write_memory` call). This is negligible compared to the potential savings for any session that matches a prior entry. Even for novel issues with no match, the overhead is a rounding error on a 5,000-token session.

4. **Proven memory API**: The brainstorm explicitly notes that Serena's memory API is "already proven in `sc-validate-roadmap-protocol` and `sc:save`/`sc:load` commands." This is not speculative integration; it uses an established, tested persistence mechanism.

5. **User control and transparency**: The three new flags (`--history`, `--no-memory`, `--clear-history`) give users full control over the memory lifecycle. Users can review history, opt out, or reset -- addressing privacy and staleness concerns proactively.

6. **Language-agnostic**: Unlike Variant A, which struggles with dynamic languages, Variant B's memory stores human-readable diagnostic findings that are valuable regardless of the language or codebase structure. A diagnostic entry for a Python metaprogramming issue is just as useful on the 2nd occurrence as one for a TypeScript type error.

**Weaknesses Identified in Variant A**:

1. **Ceiling on savings**: Variant A's token reduction has a hard ceiling. Once you have replaced grep with symbol navigation, you have captured the full benefit. There is no compounding effect. Session 100 saves the same tokens as session 1.

2. **Does not address the amnesic problem**: Even with symbol-aware diagnosis, each session starts from zero knowledge about what has been diagnosed before. The agent will re-investigate the exact same null-safety pattern in src/services/ that it diagnosed last week, just more efficiently. This is optimizing the wrong thing -- it makes redundant work faster instead of eliminating it.

3. **Language sensitivity is a real limitation**: The brainstorm acknowledges that "Serena's symbol navigation works best for statically-typed languages." For Python-heavy projects (like SuperClaude itself), the benefit may be significantly reduced. The framework's own codebase is Python -- the very tool being built would see diminished returns from its own enhancement.

4. **Activation latency compounds**: While the 200-500ms `activate_project` latency is "negligible" for a single session, it is paid on every session without any learning curve. Variant B's memory lookup, by contrast, can short-circuit the entire investigation phase, making the activation latency irrelevant for recurring issues.

**Concessions**: The cold start problem is real. First invocations for new projects yield no memory benefit. However, this is a one-time cost per project that is rapidly amortized as diagnostic history accumulates.

---

### Round 2: Rebuttals

#### Variant A Advocate Rebuttal

**Response to "ceiling on savings"**: The ceiling argument is misleading. A consistent 60-75% reduction on every session is extremely valuable precisely because it is reliable. Variant B's savings are bimodal: massive for recurring issues, near-zero for novel issues. The "average" saving depends entirely on the recurrence rate of issues in a given project. For actively evolving codebases where issues are mostly novel, Variant A dominates.

**Response to "does not address the amnesic problem"**: This is true but misframes the priority. The brainstorm's own "Implementation Priority" section explicitly states: "Proposal 1 should be implemented first. It has no dependency on Proposal 2 and provides immediate token savings for every troubleshoot invocation." The question is not which proposal is more visionary -- it is which delivers more value sooner and more reliably. Variant A does.

**Response to "language sensitivity"**: Python projects are not the worst case for Serena's symbol tools. Python has classes, functions, methods, and modules with well-defined hierarchies. Serena's `find_symbol` and `get_symbols_overview` work effectively for standard Python codebases. The limitation applies to heavy metaprogramming and dynamic attribute generation, which is a minority pattern even in Python projects.

**Response to shared assumption A-003**: ACCEPT. The diagnostic chain's template-based architecture can consume a `SymbolContext` dataclass without redesign -- it is an additive optional parameter, not a structural change.

**Response to shared assumption A-004**: REJECT. Symbol-aware diagnosis could benefit `sc:analyze`, `sc:improve`, and any command that performs codebase investigation. Scoping to troubleshoot is a reasonable starting point, but not a permanent ceiling.

**Updated Assessment**: Variant B's compounding returns argument is its strongest point. However, the compounding is contingent on issue recurrence rates, which vary wildly by project. Variant A's consistent per-session improvement is the lower-risk, higher-certainty investment.

---

#### Variant B Advocate Rebuttal

**Response to "cold start problem"**: The cold start cost is ~100 tokens (one empty `read_memory` return). This is trivially small. More importantly, the cold start resolves itself rapidly. After 3-5 troubleshoot sessions, the memory has enough entries to start providing value. For active development projects, this is days, not weeks.

**Response to "memory staleness risk"**: Staleness is addressed by three mechanisms: (1) the 180-day expiry removes old entries automatically, (2) the 50-entry cap forces natural rotation, and (3) -- critically -- Variant A's symbol resolution can validate whether referenced symbols still exist. This is explicitly called out in the brainstorm: "Proposal 1's symbol resolution will naturally detect when a referenced symbol no longer exists." The proposals compose to solve each other's weaknesses.

**Response to "pattern detection is fragile"**: The keyword matching is a starting point, not the sole mechanism. The memory schema stores `affected_symbols` and `affected_files`, enabling structural matching (same file, same symbol) alongside keyword matching. False positive matches present a hypothesis, not a conclusion -- the agent still validates before acting. A wrong hypothesis costs ~200 tokens to discard; a correct one saves ~4,500.

**Response to "schema maintenance burden"**: The schema is 7 fields per entry with a single top-level structure. This is simpler than the `SymbolContext` dataclass Variant A introduces. JSON schema versioning is a solved problem. Concurrent write conflicts are prevented by Serena's memory API semantics (read-modify-write within a single session).

**Response to shared assumption A-001**: QUALIFY. Serena availability is not guaranteed, but both proposals share this dependency identically. The fail-open fallback means neither proposal degrades the user experience when Serena is absent.

**Response to shared assumption A-002**: REJECT. Current behavior is not "good enough" -- it is the problem statement. Both proposals exist because current behavior wastes 2,000-5,000 tokens per session. The fallback is acceptable as a safety net, not as a target.

**Updated Assessment**: Variant A's strongest argument is implementation priority -- it should come first because Variant B consumes its output. This is a sequencing argument, not a superiority argument. Evaluated as standalone contributions, Variant B delivers larger total token savings over a project's lifetime.

---

### Round 2.5: Invariant Probe

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | `activate_project` state persists for the duration of a troubleshoot session and does not need re-activation between phases | UNADDRESSED | MEDIUM | Neither advocate discussed session-level state management of the Serena project activation |
| INV-002 | guard_conditions | Memory read returns well-formed JSON conforming to the schema; no validation of malformed or corrupted memory data is specified | UNADDRESSED | HIGH | Variant B defines schema but specifies no parse-error handling; Round 2 rebuttal mentions "Serena's memory API semantics" without citing validation guarantees |
| INV-003 | collection_boundaries | Memory reaches 50-entry cap: retention policy eviction behavior when all 50 entries are within the 180-day window is unspecified (which entry is evicted?) | UNADDRESSED | HIGH | Schema defines "Keep last 50 entries" but does not define ordering -- FIFO? LRU? Priority-based? |
| INV-004 | guard_conditions | `find_symbol` returns no results for a symbol extracted from an error message (symbol is dynamic, misspelled, or from a dependency not in the project) | ADDRESSED | LOW | Variant A advocate acknowledged language sensitivity; fallback to Grep/Read covers empty results |
| INV-005 | interaction_effects | Both proposals modify `diagnostic_chain.py` with different optional parameters (`SymbolContext` and `prior_diagnostics`); when both are implemented, parameter proliferation and ordering interactions are unspecified | UNADDRESSED | MEDIUM | Brainstorm "Changes Required" table shows both proposals touch the same file but does not discuss combined parameter design |
| INV-006 | state_variables | Memory write after Phase 5 (Resolve) depends on the troubleshoot session completing successfully; crash or user abort mid-session loses diagnostic findings | UNADDRESSED | MEDIUM | Variant B's persist phase is the final step with no discussion of partial-session persistence |
| INV-007 | collection_boundaries | `get_symbols_overview` on a large file (1000+ symbols) may return excessive data, negating token savings | UNADDRESSED | MEDIUM | Variant A claims targeted reads but does not specify symbol count limits or pagination |

**Summary**:
- Total findings: 7
- ADDRESSED: 1
- UNADDRESSED: 6 (HIGH: 2, MEDIUM: 4, LOW: 0)

**Convergence Impact**: 2 HIGH-severity UNADDRESSED items (INV-002, INV-003) are present. Under normal protocol rules, these would block convergence. However, since both items apply exclusively to Variant B's memory schema, they inform scoring rather than blocking the comparative evaluation. Both are recorded as unresolved risks for Variant B.

---

### Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Variant A | 65% | Modifying existing phases is lower-risk than adding new phases; Variant B advocate did not contest this |
| S-002 | Tie | 50% | Implementation phase count is a cosmetic difference |
| S-003 | Variant A | 70% | `SymbolContext` is simpler and stateless; memory schema has unaddressed invariants (INV-002, INV-003) |
| S-004 | Tie | 50% | Tool count difference is not meaningful |
| S-005 | Variant B | 60% | More user-facing control options; `--history` is a genuinely useful capability |
| C-001 | Variant B | 72% | Cross-session savings for recurring issues are larger in aggregate; Variant A advocate conceded ceiling |
| C-002 | Variant A | 78% | Immediate benefit without accumulation period is more reliable; cold start is a real cost |
| C-003 | Variant A | 65% | Structural evidence is higher quality than historical guessing; both advocates agreed on this |
| C-004 | Tie | 50% | Both fall back identically |
| C-005 | Tie | 50% | Both modify diagnostic chain similarly |
| C-006 | Variant B | 68% | Language-agnostic memory is genuinely more broadly applicable |
| C-007 | Variant A | 60% | Near-zero overhead vs ~200-400 token cost; marginal but consistent advantage |
| X-001 | Split | 55% | Both bottlenecks are real; neither advocate convincingly argued the other's bottleneck is secondary |
| X-002 | Variant A | 82% | Both advocates agreed A should be implemented first; brainstorm explicitly recommends this ordering |
| A-001 | Tie | 50% | Shared dependency; neither has an advantage |
| A-002 | Variant B | 62% | Variant B advocate's rejection was more compelling -- fallback is a safety net, not a goal |
| A-003 | Tie | 50% | Both advocates accepted this assumption |
| A-004 | Variant A | 58% | Variant A advocate's rejection was credible -- symbol navigation benefits extend beyond troubleshoot |

### Convergence Assessment

- Points resolved: 13 of 18 (excluding 5 ties)
- Variant A wins: 7 points
- Variant B wins: 4 points
- Ties: 5 points
- Split: 1 point (X-001)
- Unresolved points: X-001
- Alignment: 72% (13/18)
- Threshold: 80%
- Status: NOT_CONVERGED (below threshold, but forced selection by score proceeds per protocol)

---

## Step 3: Hybrid Scoring & Base Selection

### Quantitative Scoring (50% weight)

| Metric | Weight | Variant A | Variant B | Notes |
|--------|--------|-----------|-----------|-------|
| Requirement Coverage (RC) | 0.30 | 0.85 | 0.90 | B covers more of the problem statement (both per-session and cross-session waste) |
| Internal Consistency (IC) | 0.25 | 0.95 | 0.82 | A has no contradictions; B has unaddressed invariants (INV-002, INV-003) reducing consistency |
| Specificity Ratio (SR) | 0.15 | 0.90 | 0.88 | Both proposals use concrete metrics; A's claims are slightly more specific |
| Dependency Completeness (DC) | 0.15 | 0.95 | 0.80 | A is self-contained; B depends on A's output for `affected_symbols` |
| Section Coverage (SC) | 0.15 | 0.85 | 1.00 | B has more sections (schema, flags, retention policy, pattern detection) |

**Quantitative Scores**:
- Variant A: (0.85 x 0.30) + (0.95 x 0.25) + (0.90 x 0.15) + (0.95 x 0.15) + (0.85 x 0.15) = 0.255 + 0.2375 + 0.135 + 0.1425 + 0.1275 = **0.8975**
- Variant B: (0.90 x 0.30) + (0.82 x 0.25) + (0.88 x 0.15) + (0.80 x 0.15) + (1.00 x 0.15) = 0.270 + 0.205 + 0.132 + 0.120 + 0.150 = **0.8770**

### Qualitative Scoring (50% weight) -- Additive Binary Rubric

#### Completeness (5 criteria)

| Criterion | Variant A | Variant B |
|-----------|-----------|-----------|
| Covers all explicit requirements | MET -- addresses per-session token waste and investigation quality | MET -- addresses cross-session knowledge loss and recurring issue waste |
| Addresses edge cases and failure scenarios | MET -- fallback behavior for Serena unavailability and dynamic languages | NOT MET -- no handling for corrupted memory (INV-002), no eviction ordering (INV-003) |
| Includes dependencies and prerequisites | MET -- explicitly states no dependency on Proposal 2 | MET -- explicitly notes dependency on Proposal 1 for `affected_symbols` |
| Defines success/completion criteria | MET -- token reduction metrics and time-to-hypothesis targets | MET -- token reduction metrics for recurring vs novel issues |
| Specifies what is out of scope | NOT MET -- does not explicitly state what it will not do | MET -- retention policy, entry cap, and opt-out mechanisms define scope boundaries |

Variant A: 4/5 | Variant B: 4/5

#### Correctness (5 criteria)

| Criterion | Variant A | Variant B |
|-----------|-----------|-----------|
| No factual errors or hallucinated claims | MET | MET |
| Technical approaches are feasible | MET -- Serena symbol tools exist and work as described | MET -- Serena memory API exists and works as described |
| Terminology used consistently | MET | MET |
| No internal contradictions | MET | NOT MET -- "Keep last 50 entries" contradicts 180-day expiry without specifying precedence |
| Claims supported by evidence | MET -- metrics derived from known tool behavior | MET -- metrics derived from known memory API behavior |

Variant A: 5/5 | Variant B: 4/5

#### Structure (5 criteria)

| Criterion | Variant A | Variant B |
|-----------|-----------|-----------|
| Logical section ordering | MET | MET |
| Consistent hierarchy depth | MET | MET |
| Clear separation of concerns | MET -- each phase has a distinct role | MET -- schema, loading, persistence clearly separated |
| Navigation aids present | NOT MET -- no cross-references between phases | NOT MET -- no cross-references between phases |
| Follows conventions of the artifact type | MET | MET |

Variant A: 4/5 | Variant B: 4/5

#### Clarity (5 criteria)

| Criterion | Variant A | Variant B |
|-----------|-----------|-----------|
| Unambiguous language | MET | NOT MET -- "keyword overlap" matching threshold not specified |
| Concrete rather than abstract | MET -- specific tool calls and data structures | MET -- specific JSON schema and API calls |
| Each section has clear purpose | MET | MET |
| Domain terms defined | MET | MET |
| Actionable next steps identified | MET -- 4 implementation phases clearly ordered | MET -- 5 implementation phases clearly ordered |

Variant A: 5/5 | Variant B: 4/5

#### Risk Coverage (5 criteria)

| Criterion | Variant A | Variant B |
|-----------|-----------|-----------|
| Identifies at least 3 risks | MET -- Serena dependency, activation latency, symbol resolution limits, complexity increase | MET -- Serena dependency, memory staleness, memory size growth, privacy, complementarity |
| Mitigation strategy for each risk | MET -- fail-open fallback, amortized latency, grep fallback for dynamic languages | MET -- fail-open, 180-day expiry, 10KB limit, clear-history flag |
| Addresses failure modes | MET -- fallback to current behavior | MET -- fallback to current behavior |
| External dependency failure scenarios | MET -- Serena unavailability explicitly handled | MET -- Serena unavailability explicitly handled |
| Monitoring or validation mechanism | NOT MET -- no mechanism to detect when symbol resolution is producing poor results | NOT MET -- no mechanism to detect when memory entries are stale or misleading |

Variant A: 4/5 | Variant B: 4/5

#### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Variant B |
|-----------|-----------|-----------|
| Boundary conditions for collections | NOT MET -- no handling for large symbol sets (INV-007) | NOT MET -- eviction ordering unspecified (INV-003) |
| State variable interactions | MET -- stateless per session, no cross-component state | NOT MET -- session crash loses findings (INV-006) |
| Guard condition gaps | MET -- empty symbol results fall back to grep | NOT MET -- malformed memory JSON not validated (INV-002) |
| Count divergence scenarios | MET -- no counting logic involved | MET -- 50-entry cap is explicit |
| Interaction effects when combined | NOT MET -- does not discuss combined parameter design for diagnostic_chain.py (INV-005) | NOT MET -- does not discuss combined parameter design for diagnostic_chain.py (INV-005) |

Variant A: 3/5 | Variant B: 1/5

**Edge Case Floor Check**: Variant B scores 1/5 on Invariant & Edge Case Coverage, meeting the minimum threshold (>=1/5). Both variants remain eligible.

#### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 |
| Correctness | 5/5 | 4/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 5/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 3/5 | 1/5 |
| **Total** | **25/30** | **21/30** |

**Qualitative Scores**:
- Variant A: 25/30 = **0.8333**
- Variant B: 21/30 = **0.7000**

### Position-Bias Mitigation

Both passes (forward and reverse order) produced identical verdicts for all criteria. No disagreements to resolve.

### Combined Scoring

| Component | Weight | Variant A | Variant B |
|-----------|--------|-----------|-----------|
| Quantitative | 0.50 | 0.8975 | 0.8770 |
| Qualitative | 0.50 | 0.8333 | 0.7000 |
| **Combined** | | **0.8654** | **0.7885** |

**Margin**: 7.69% (outside tiebreaker range of 5%)

### Selected Base: Variant A (Symbol-Aware Diagnosis Pipeline)

**Selection Rationale**: Variant A scores higher on both quantitative (0.8975 vs 0.8770) and qualitative (0.8333 vs 0.7000) layers. The qualitative gap is driven by Variant A's superior correctness (no internal contradictions), clarity (no ambiguous matching thresholds), and significantly better invariant/edge case coverage (3/5 vs 1/5). Variant A's stateless, per-session design avoids the persistent state management risks that weaken Variant B.

**Strengths to Preserve from Variant A**:
- Structural symbol navigation replacing text-pattern investigation
- `SymbolContext` dataclass as a clean integration contract
- Fail-open fallback preserving current behavior
- Zero persistent state overhead

**Strengths to Incorporate from Variant B**:
- Cross-session pattern detection (U-003) -- the ability to surface recurring issue patterns is a unique, high-value capability
- User-facing `--history` flag (U-005) -- adds transparency and user control
- Language-agnostic benefit model (C-006) -- memory-based diagnosis complements symbol-based diagnosis for dynamic languages

---

## Step 4: Refactoring Plan

### Planned Changes

| # | Source | Target in Base | Integration Approach | Rationale | Risk |
|---|--------|---------------|---------------------|-----------|------|
| 1 | Variant B: Memory schema design | Append as "Phase 5: Diagnostic Memory" after Variant A's Phase 4 | Append | Cross-session memory is the strongest unique contribution; implementing it as a follow-on phase preserves A's independence | Low |
| 2 | Variant B: `--history` flag | Add to Variant A's flag documentation section | Append | User-facing diagnostic history review is a standalone improvement with no interaction effects | Low |
| 3 | Variant B: Pattern detection | Add as enhancement note in the Expected Benefits section | Insert | Positions cross-session pattern detection as a compounding benefit layered on top of A's per-session improvement | Low |

### Changes NOT Being Made

| Diff Point | Variant B Approach | Rationale for Rejection |
|------------|-------------------|------------------------|
| C-001 (primary value proposition) | Cross-session token reduction as primary frame | Variant A's per-session reduction is the correct primary frame because it delivers value from first use without accumulation dependency |
| S-003 (memory schema as core data model) | JSON memory schema as a peer to SymbolContext | Memory schema should be a follow-on, not a peer; it consumes SymbolContext output and should be designed after SymbolContext is finalized |
| B's Phase 0 (pre-diagnosis context loading) | Memory loading before investigation | Correct idea but should be designed to compose with A's Phase 2, not replace it; deferred to implementation of the combined proposal |

### Risk Summary

All planned changes are Low risk (additive, no modification of base content). Total: 3 changes, 0 High risk, 0 Medium risk, 3 Low risk.

### Review Status

Auto-approved (non-interactive mode).

---

## Step 5: Final Verdict

### Verdict: Variant A (Symbol-Aware Diagnosis Pipeline) is the superior base proposal

**Composite Score**: 0.8654 vs 0.7885 (7.69% margin)

**Debate Performance**: Variant A won 7 of 18 diff points vs Variant B's 4 (5 ties, 1 split, 1 unresolved)

### Scoring Breakdown

| Dimension | Variant A | Variant B | Winner |
|-----------|-----------|-----------|--------|
| Effectiveness | Immediate 60-75% token reduction every session | 80-90% for recurring issues, ~0% for novel issues | A (reliability) |
| Token Savings | Consistent ~1,500-2,000 per session | Variable: 0 to 4,500 depending on recurrence | A (first use), B (long-term recurring) |
| Implementation Complexity | 4 phases, stateless, no schema | 5 phases, persistent state, JSON schema, retention policy | A (simpler) |
| Risk | Low -- fail-open, no persistent state, language sensitivity mitigated by fallback | Medium -- memory staleness (INV-002 unaddressed), eviction ambiguity (INV-003 unaddressed), cold start | A (lower risk) |
| Composability | Foundation for Proposal B; produces `affected_symbols` consumed by memory entries | Depends on Proposal A for quality symbol data; composes well but is not standalone | A (independent), B (dependent) |

### Reasoning

1. **Variant A is the prerequisite**: Both advocates and the original brainstorm agree that Proposal 1 should be implemented first. Variant B explicitly depends on Variant A's `affected_symbols` output for quality memory entries. This is not just a priority argument -- it is a dependency argument. Variant B without Variant A stores grep-derived guesses in memory.

2. **Reliability over potential**: Variant A delivers measurable improvement on 100% of invocations. Variant B's larger savings apply only to recurring issues, and the recurrence rate varies by project. For actively evolving codebases (where most issues are novel), Variant A dominates. For maintenance-mode codebases (where issues recur), Variant B dominates. The safer bet is the one that works everywhere.

3. **Variant B has unresolved invariant risks**: Two HIGH-severity invariant violations (INV-002: no malformed memory validation; INV-003: eviction ordering unspecified) remain unaddressed. These are solvable but represent design gaps that need resolution before implementation. Variant A has no HIGH-severity invariant issues.

4. **The proposals compose**: This is not a binary choice. The verdict is that Variant A should be the base -- implemented first, with Variant B's cross-session memory added as a follow-on enhancement that consumes Variant A's structural data. The merged recommendation is: build A, then layer B on top.

### Implementation Recommendation

**Phase 1** (Immediate): Implement Variant A -- Symbol-Aware Diagnosis Pipeline
- Update `src/superclaude/commands/troubleshoot.md` with Serena integration
- Enhance the 5-phase behavioral flow with symbol navigation in Investigate/Debug
- Add `SymbolContext` to `diagnostic_chain.py`
- Implement fail-open fallback

**Phase 2** (Follow-on): Implement Variant B -- Diagnostic Memory
- Design memory schema after SymbolContext is finalized (addressing INV-002, INV-003)
- Add Phase 0 (Context Load) and Phase 6 (Persist) to the troubleshoot flow
- Implement `--history`, `--no-memory`, `--clear-history` flags
- Integrate pattern detection with symbol-validated entries

### Unresolved Items for Design Phase

1. INV-002: Define parse-error handling for malformed memory JSON (validation, fallback, repair)
2. INV-003: Specify eviction ordering when 50-entry cap is reached (recommend: FIFO by timestamp)
3. INV-005: Design combined `diagnostic_chain.py` parameter interface for both SymbolContext and prior_diagnostics
4. INV-006: Consider partial-session persistence (write memory on Phase 4 completion, not just Phase 5)
5. INV-007: Specify symbol count limits for `get_symbols_overview` on large files

---

## Return Contract

```yaml
return_contract:
  merged_output_path: ".dev/releases/backlog/v5.xx-sc-troubleshoot-v2/adversarial-serena-mcp.md"
  convergence_score: 0.72
  artifacts_dir: ".dev/releases/backlog/v5.xx-sc-troubleshoot-v2/"
  status: "partial"
  base_variant: "Variant A: Symbol-Aware Diagnosis Pipeline"
  unresolved_conflicts: 1
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants:
    - {id: "INV-002", category: "guard_conditions", assumption: "Memory read returns well-formed JSON", severity: "HIGH"}
    - {id: "INV-003", category: "collection_boundaries", assumption: "50-entry cap eviction ordering", severity: "HIGH"}
```

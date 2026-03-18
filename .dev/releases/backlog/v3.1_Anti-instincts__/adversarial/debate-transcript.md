# Adversarial Debate Transcript: Anti-Instinct Proposals 01-05

**Pipeline**: 5-variant adversarial debate
**Depth**: deep (3 rounds)
**Timestamp**: 2026-03-17T00:00:00Z
**Scoring**: Custom 4-dimension framework (D1 Efficacy, D2 Generalizability, D3 Implementation Complexity, D4 Determinism)
**Convergence threshold**: 0.80
**Focus**: efficacy, implementability, coverage

**Advocates**:
- V1-Advocate (Completeness Bias) -- primary: defense-in-depth A+D+E
- V2-Advocate (Implicit Obligation) -- primary: Solution A (obligation scanner)
- V3-Advocate (Local Coherence) -- primary: Solution 1 (coherence graph)
- V4-Advocate (Self-Audit Blindness) -- primary: Solution 4 (hybrid: IDs + fingerprints + adversarial prompt)
- V5-Advocate (Pattern-Matching Trap) -- primary: Solution 1 (integration contract extractor)

---

## Round 1: Opening Positions

### V1-Advocate (Completeness Bias) -- Opening Position

**Core thesis**: The cli-portify bug is fundamentally a completeness failure -- a requirement existed in the spec and was absent from the roadmap. The most reliable way to catch completeness failures is layered defense: a deterministic ID cross-reference (Solution A) to catch formally-tagged omissions, a prompt constraint (Solution D) to reduce generation-time omissions, and a structured LLM pass (Solution E) to catch semantic gaps that escape ID matching.

**Strongest arguments for V1 primary (A+D+E defense-in-depth)**:

1. **Quantifiable miss rate**: V1 is the only proposal that computes a joint failure probability. With three independent checks (D at 75% catch rate, A at 90%, E at 90%), the combined miss rate is approximately 0.25%. No other variant provides a comparable reliability calculation.

2. **Upstream guard (Solution C)**: V1 is the only proposal that addresses the extraction step itself. If the extraction LLM drops a requirement before it ever reaches the roadmap, every other variant's post-merge checks are vacuous. Solution C (spec structural audit) is a unique contribution that no other proposal replicates.

3. **Incremental deployability**: The A+D combination ships immediately with near-zero latency cost (regex matching + prompt text). Solution E layers on afterward. This phasing means the team gets 90%+ protection in v2.27 and 99.75%+ protection in v2.28.

4. **ID cross-reference is the simplest deterministic check**: ~100 LOC, 1 new file, 2 modified files, zero LLM calls, sub-100ms execution. It hooks cleanly into the existing SemanticCheck pattern via a pre-gate executor hook.

**Steelmanning V2**: The scaffold-discharge vocabulary (V2-A) catches a genuinely different failure class -- undischarged deferred commitments -- that ID cross-referencing misses entirely. The obligation concept is formally distinct from the omission concept. A roadmap that mentions FR-047 in a throwaway sentence passes V1-A but still fails V2-A if the scaffold was never discharged.

**Steelmanning V3**: The coherence graph (V3-1) has the broadest coverage of any single proposal. It catches any cross-phase data flow gap, not just dispatch wiring. Its mapping to 5 existing infrastructure modules (dataflow_graph.py, dataflow_pass.py, deliverables.py, conflict_detector.py, contract_extractor.py) means it is not building from scratch but extending proven patterns.

**Steelmanning V4**: Fingerprint extraction (V4-2) has the highest single-check efficacy for the cli-portify bug specifically. The spec contained `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, and `test_programmatic_step_routing` in backtick-delimited spans. These are hard signals that cannot be rationalized away. V4-2 catches this regardless of whether formal FR-NNN IDs were used.

**Steelmanning V5**: The 7-category integration mechanism taxonomy is the most thorough analysis of the problem space. By categorizing dispatch tables, plugin registries, callback injection, strategy patterns, middleware chains, event binding, and DI containers as distinct integration mechanisms that LLMs commonly miss, V5 makes the problem concrete and bounded.

---

### V2-Advocate (Implicit Obligation) -- Opening Position

**Core thesis**: The cli-portify bug is not primarily an omission -- it is an **undischarged obligation**. Phase 2 said "mocked steps" (creating an implicit promise that real steps would replace them) and no later phase fulfilled that promise. This is a fundamentally different failure mode from "requirement absent from roadmap." The roadmap *mentioned* the executor, *mentioned* step implementations, and *mentioned* mocking. What it failed to do is connect the scaffold to its replacement. V2-A's obligation scanner is the only proposal that detects this specific failure pattern.

**Strongest arguments for V2 primary (obligation scanner)**:

1. **Unique detection axis**: V1/V4/V5 detect omissions (something should be in the roadmap but is not). V2 detects broken promises (something IS in the roadmap but was never fulfilled). These are orthogonal failure modes. A roadmap can pass all omission checks while still containing undischarged scaffolding.

2. **Nearly production-ready code**: The obligation scanner in the proposal is ~200 LOC of fully specified Python with scaffold/discharge term vocabularies, phase splitting logic, component context extraction, and a clean `ObligationReport` dataclass. It is the most implementation-ready code of any proposal.

3. **Zero LLM involvement for the primary solution**: The scanner is pure regex with phase-aware context matching. It runs in <100ms. It cannot be fooled by the same LLM biases that created the bug.

4. **Extensible vocabulary**: The scaffold/discharge term mapping is a data structure, not hardcoded logic. New terms can be added without changing the scanner algorithm. The bidirectional mapping table (10 scaffold terms, 10+ discharge terms) is documented and testable.

5. **Clean gate integration**: Hooks as a SemanticCheck on the existing MERGE_GATE. No new pipeline steps, no model changes, no multi-file access needed (operates on the single merged roadmap).

**Steelmanning V1**: V1's defense-in-depth calculation is sound: three independent layers beat any single layer. The upstream guard (V1-C) catches a failure that V2 cannot -- if the extraction step drops the requirement entirely, there is nothing for V2 to scan for in the roadmap.

**Steelmanning V4**: Negative-space prompting (V4-3) is the most innovative LLM-side mitigation. Inverting the review question from "confirm completeness" to "find gaps" is a genuine cognitive reframing that the forensic evidence supports -- the existing spec-fidelity check uses positive framing and failed.

**Steelmanning V5**: The integration contract extractor (V5-1) is mechanism-aware in a way V2 is not. V2 detects scaffold language; V5 detects dispatch-table-shaped patterns in the spec itself. V5 asks "did the spec define a dispatch table that the roadmap does not plan to populate?" -- a more targeted question than V2's "did the roadmap make promises it did not keep?"

---

### V3-Advocate (Local Coherence) -- Opening Position

**Core thesis**: The cli-portify bug is a **cross-phase coherence failure**. Each phase was locally correct -- the executor skeleton was well-designed, the step implementations were well-structured, the tests were reasonable. The bug exists only in the gap between phases: Phase 2 produces artifacts that Phases 4-7 consume, but no phase wires them together. The producer-consumer coherence graph (V3-1) is the only proposal that models this relationship as a first-class graph structure and detects disconnected pairs.

**Strongest arguments for V3 primary (coherence graph)**:

1. **Broadest coverage of any single solution**: The coherence graph catches ANY cross-phase data flow gap, not just dispatch wiring, not just scaffolding, not just formally-tagged requirements. Orphaned producers, unsatisfied consumers, disconnected pairs -- all are graph-theoretic properties computable from the roadmap text. This catches bugs that no other single proposal catches.

2. **Architectural grounding in existing infrastructure**: V3 maps to 5 existing modules: `dataflow_graph.py` (graph model), `dataflow_pass.py` (tracing pattern), `deliverables.py` (deliverable classification), `conflict_detector.py` (conflict detection), `contract_extractor.py` (contract extraction). The coherence graph is not a new abstraction -- it extends the existing data flow infrastructure from state-variable-level to phase-deliverable-level. This is the lowest-risk implementation path.

3. **The disconnected-pair concept**: V1-B (orphan detection) finds nodes with wrong degree. V3-1 goes further: it finds pairs where both producer and consumer exist but no wiring edge connects them. This is the precise pattern of the cli-portify bug -- `steps/*.py` (produced in Phases 4-7) and `PortifyExecutor._execute_step` (consumed in Phase 2) both existed, but no integration task bridged them.

4. **Prevention AND detection**: V3-2 (manifest injection) complements V3-1 by injecting prior-phase deliverables into subsequent prompts. This reduces the frequency of coherence failures at generation time. V3-1 then catches what slips through.

**Steelmanning V2**: The obligation scanner addresses a specific failure mode -- undischarged scaffolding -- that the coherence graph handles awkwardly. A scaffold term like "mocked" is a linguistic signal, not a producer-consumer relationship. The graph can detect that steps are produced but never consumed by the executor, but it cannot detect that the word "mocked" in Phase 2 creates an expectation that V2 explicitly tracks.

**Steelmanning V4**: Fingerprint extraction is faster to implement and has higher single-check efficacy for the cli-portify case specifically. The coherence graph requires heuristic extraction of producers and consumers from natural language, which is the hard part. V4-2's fingerprint matching is simpler (backtick identifiers) and more precise for code-heavy specs.

---

### V4-Advocate (Self-Audit Blindness) -- Opening Position

**Core thesis**: The root cause of the cli-portify bug is not one failure but two: (1) the generation LLM dropped the requirement, and (2) the review LLM failed to notice the drop. The existing SPEC_FIDELITY_GATE uses an LLM to validate the roadmap, but that LLM shares the same blindspot -- it sees structural completeness and confirms it. The solution must provide a **deterministic floor** under LLM judgment: programmatic checks that cannot be fooled by the same bias. V4-4 (hybrid) provides this with three layers: ID cross-reference (deterministic), fingerprint coverage (deterministic), and negative-space prompting (adversarial LLM reframing).

**Strongest arguments for V4 primary (hybrid: IDs + fingerprints + adversarial prompt)**:

1. **Highest single-check efficacy (fingerprints)**: V4-2 has 95% confidence for the cli-portify bug -- the highest of any single solution across all 5 proposals. The spec contained `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` in backticks and code blocks. None appeared in the roadmap. Fingerprint coverage would have been near 0%, triggering the gate regardless of threshold tuning.

2. **Negative-space prompting is a unique innovation**: V4-3 reframes the review question from "is the roadmap complete?" (which triggers completion bias) to "what specific spec requirements are NOT covered?" This is the only proposal that directly addresses the psychological mechanism of self-audit blindness at the prompt level. The anti-bias instructions ("Do NOT assume a roadmap phase 'covers' something unless it explicitly names it") are concrete countermeasures.

3. **Explicit determinism boundary**: V4 is the only proposal with a layered table showing which checks the LLM can override and which it cannot. Layer 1 (IDs) and Layer 2 (fingerprints) are deterministic and non-overridable. Layer 3 (negative-space) is LLM-assisted but uses adversarial reframing. Layer 4 (existing fidelity) is the current baseline. This makes the defense-in-depth architecture transparent.

4. **Works regardless of spec format**: ID cross-reference works when specs use FR-NNN tags. Fingerprint extraction works when specs use code identifiers. Negative-space prompting works on any spec. Together they cover every spec format -- formal, semi-formal, and prose-only.

**Steelmanning V2**: The obligation scanner catches a class of bugs (undischarged scaffolding) that V4's fingerprint checker misses entirely. If a roadmap says "mocked steps" in Phase 2 and never discharges them, V4 would only catch this if "mocked" happens to be a fingerprint identifier (it likely is not, since it is a description, not a code identifier). V2's scaffold vocabulary is a specialized tool for a specialized failure mode.

**Steelmanning V3**: The coherence graph has broader coverage than fingerprints. Fingerprints only check what the spec mentions; the coherence graph checks whether the roadmap's own internal dependencies are satisfied. A roadmap could drop an entire spec section (caught by fingerprints) AND introduce new internal inconsistencies (caught only by the graph).

**Steelmanning V5**: The integration contract extractor is mechanism-aware. It does not just check "is this identifier present?" (V4-2) but "is there an explicit task that populates this dispatch table?" The distinction matters: a roadmap that mentions PROGRAMMATIC_RUNNERS in a design overview section would pass V4-2 but fail V5-1 if no population task exists.

---

### V5-Advocate (Pattern-Matching Trap) -- Opening Position

**Core thesis**: The LLM reproduced a familiar pattern (skeleton + implement + test) without verifying it covered all integration points. The problem is not that the LLM forgot something (V1), failed to track an obligation (V2), produced an incoherent graph (V3), or could not audit itself (V4). The problem is that the LLM applied a memorized template to a situation that required custom integration. The integration contract extractor (V5-1) is the only solution that directly addresses this by identifying non-standard integration mechanisms in the spec and verifying the roadmap explicitly plans for them.

**Strongest arguments for V5 primary (integration contract extractor)**:

1. **Mechanism-aware detection**: V5-1 does not just check whether identifiers appear in the roadmap. It checks whether the roadmap contains explicit wiring tasks for specific integration mechanisms. A roadmap that mentions `PROGRAMMATIC_RUNNERS` in a design section passes V4-2 (fingerprint present) but fails V5-1 (no task to populate the table). This semantic distinction is the difference between "mentioned" and "planned."

2. **7-category integration taxonomy**: The appendix taxonomy (dict dispatch, plugin registry, callback injection, strategy pattern, middleware chain, event binding, DI container) maps the full problem space. Each category represents a class of integration mechanism that LLMs routinely assume is handled implicitly. This taxonomy is not just documentation -- it drives the pattern library in `DISPATCH_PATTERNS`.

3. **Extensible rule framework (Solution 3)**: The anti-pattern rule engine provides a framework for adding new detection rules without changing the pipeline. AP-001 (skeleton without wiring) catches the cli-portify pattern. AP-002 (implicit integration assumption) catches vague integration phases. AP-003 (dict dispatch without population) catches the specific mechanism. New rules can be added as new bug patterns are discovered.

4. **Deterministic, zero-LLM**: The contract extractor and anti-pattern rules are pure Python regex matching. No LLM calls. Sub-500ms execution. The pattern libraries are data, not code -- new patterns are added by extending lists, not modifying algorithms.

**Steelmanning V1**: V1's upstream guard (Solution C, spec structural audit) catches a failure mode that V5 cannot: if the extraction LLM drops the dispatch requirement entirely, V5 has nothing to extract contracts from. V1-C is the only proposal that validates the extraction step itself.

**Steelmanning V2**: The obligation scanner is simpler and catches a complementary failure mode. A roadmap with "mocked steps" that is never discharged does not look like a contract violation -- the mock is not a dispatch table, registry, or injection point. V2 catches linguistic promises; V5 catches structural omissions.

**Steelmanning V4**: The fingerprint approach is simpler to implement (~150 LOC vs ~250 LOC) and has broader applicability. Fingerprints catch any code-level identifier omission; contracts catch only dispatch/registry/injection patterns. For specs that do not use integration mechanisms (e.g., a pure data-processing pipeline), V4-2 still provides value while V5-1 finds nothing.

---

## Round 1 Convergence Matrix

| Dimension | Agreement Level | Notes |
|-----------|----------------|-------|
| ID cross-ref is valuable | 90% (V1, V4 agree; V2, V3, V5 concede utility) | V2 notes it is insufficient alone; V3 notes it misses structural coherence |
| Scaffold-discharge is a unique axis | 85% (all steelman V2) | No variant argues V2's concept is wrong; they argue it is narrow |
| Coherence graph has broadest coverage | 80% (V1, V4, V5 concede) | V4 argues graph extraction heuristics are fragile; V1 argues implementation cost |
| Fingerprints have highest single-check efficacy | 85% (V1, V2, V3, V5 concede) | V5 argues "mentioned" does not equal "planned" |
| Negative-space prompting is a genuine innovation | 75% (V1, V2, V3, V5 partially concede) | V2 argues it is still LLM-dependent; V3 argues it does not add coverage beyond deterministic checks |
| Multi-file access is an architectural gap | 95% (all variants) | 3 of 5 variants independently discovered the SemanticCheck limitation |
| Post-merge insertion is the consensus gating point | 90% (12 of 16 solutions) | Only V1-C, V1-D, V2-B, V3-2, V3-3, V5-2 operate upstream |

---

## Round 2: Rebuttals

### V1-Advocate Rebuttal

**Responding to V4's claim of highest single-check efficacy**:

V4-2 (fingerprints) scores 95% confidence on the cli-portify bug, but this is partly because the cli-portify spec was code-heavy with many backtick identifiers. On a prose-heavy spec that describes requirements without code examples, fingerprint coverage degrades to near-zero utility. V1-A (ID cross-reference) degrades similarly on specs without FR-NNN tags, but V1's defense-in-depth means it does not depend on any single check. The A+D+E combination has three independent failure paths -- losing one layer still leaves two.

**Responding to V2's claim of a unique detection axis**:

V2-A's scaffold-discharge detection is genuinely unique, but its false positive risk is underweighted. The term "mock" appears in test descriptions ("unit test uses mock"), documentation ("see mock API section"), and legitimate scaffolding strategies ("this test fixture uses a mock server that IS the production implementation"). V2 acknowledges this risk but rates it MEDIUM; I argue it is closer to HIGH without context-aware filtering. The vocabulary approach is powerful but requires more engineering than the proposal suggests.

**Responding to V3's claim of broadest coverage**:

V3-1's coverage breadth is real but its implementation complexity is the highest of any primary solution (~300 LOC across 2 new files, heuristic NLP extraction from roadmap text). The extraction of producer-consumer relationships from natural language is the hard problem. V3's proposal shows dataclass sketches but not the `_extract_components()` and `_extract_relationships()` functions that contain all the difficulty. The implementation risk is concentrated in unspecified code.

**Concession**: V4's fingerprint extraction is a stronger single check than V1-A's ID cross-reference. If I could pick one deterministic check, it would be fingerprints. My variant's strength is not any single check but the layered combination.

---

### V2-Advocate Rebuttal

**Responding to V1's false positive concern**:

The false positive risk is real but manageable. The scanner already uses component context extraction -- it does not just find "mock" anywhere, it associates each scaffold term with a nearby component name and then checks whether the discharge term in a later phase references that same component. A "mock" in a test description is unlikely to share component context with a scaffold in a phase milestone. The proposal includes `_extract_component_context()` which uses backtick-delimited terms and capitalized phrases within a 60-character window. This is not naive keyword matching.

**Responding to V4's efficacy claim**:

V4-2 has 95% efficacy on the specific cli-portify bug, but the obligation scanner catches a **different class of bugs that V4 misses entirely**. Consider: a roadmap that says "Phase 2: Implement executor with placeholder dispatch" and "Phase 5: Implement step runners" but never says "Phase 6: Replace placeholder dispatch with real dispatch." V4-2 would not flag this because the fingerprints (`PortifyExecutor`, `dispatch`) are present. V2-A would flag it because "placeholder" is a scaffold term with no discharge. The question is not which catches the cli-portify bug better -- it is which catches more bugs total.

**Responding to V5's mechanism-awareness claim**:

V5-1 is mechanism-aware, which is more precise than V2-A for dispatch-table-type bugs. But mechanism-awareness is also a limitation: V5's `DISPATCH_PATTERNS` only fires on dispatch tables, registries, injection points, and routing tables. A scaffold obligation that is not one of these 7 categories (e.g., "hardcoded configuration values" or "temporary file paths") would be missed by V5 but caught by V2-A's vocabulary.

**Concession**: V2-A's biggest weakness is that it only operates on the merged roadmap. If the extraction step itself drops the requirement, V2-A has nothing to scan. V1-C (spec structural audit) addresses this gap. I would adopt V1-C as a complement.

---

### V3-Advocate Rebuttal

**Responding to V1's implementation complexity concern**:

V1 correctly identifies that `_extract_components()` and `_extract_relationships()` are the hard part. But the proposal maps to 5 existing modules that already solve analogous extraction problems. `contract_extractor.py` already extracts implicit contracts between deliverables. `conflict_detector.py` already identifies conflicting producer-consumer relationships. `deliverables.py` already classifies deliverables as behavioral or non-behavioral. The coherence extractor would reuse these patterns -- the ~300 LOC estimate is for integration and adaptation, not greenfield NLP.

**Responding to V4's fragility concern**:

Heuristic extraction is fragile on arbitrary text, but roadmap text is semi-structured. Phase headings follow predictable patterns (## Phase N: Title). Task descriptions use consistent vocabulary ("Implement X", "Create Y", "Define Z"). The extraction heuristics do not need to handle arbitrary English -- they need to handle the output format that the roadmap generation prompt constrains.

**Responding to V2's complementary detection claim**:

V2-A catches undischarged scaffolding; V3-1 catches disconnected producer-consumer pairs. But the cli-portify bug is BOTH: it is a scaffolded executor (V2's territory) whose consumer dependencies are disconnected (V3's territory). V3-1 subsumes V2-A's coverage for the structural dimension while V2-A adds the linguistic dimension. They are complementary, not competing.

**Concession**: V3-1's implementation risk is higher than V2-A's or V4-2's because of the NLP extraction challenge. If implementation speed matters more than coverage breadth, V4-2 is the better first deploy. V3-1 is the better long-term investment.

---

### V4-Advocate Rebuttal

**Responding to V5's "mentioned is not planned" critique**:

V5 makes a valid distinction between presence and adequacy. A roadmap mentioning `PROGRAMMATIC_RUNNERS` in a design overview passes V4-2 but might not plan to populate it. However: (1) the cli-portify roadmap mentioned ZERO spec fingerprints, so V4-2 catches it unambiguously in the actual case; (2) V4-4 (hybrid) includes Layer 3 (negative-space prompting) which assesses adequacy, not just presence; (3) the fingerprint threshold (0.7) is calibrated for coverage ratio, not exact-match presence, so a single mention in a design section would not inflate coverage enough to mask widespread omissions.

**Responding to V3's coverage breadth claim**:

V3-1's broader coverage comes at the cost of precision. A coherence graph that heuristically extracts "producers" and "consumers" from roadmap prose will produce false edges and miss real edges. V4-2's fingerprints have a clean signal: either `_run_programmatic_step` appears in the roadmap or it does not. No heuristic ambiguity. For the class of bugs where the spec is code-specific, fingerprints dominate. For the class of bugs where the spec is abstract, the coherence graph adds value. Both classes exist.

**Responding to V1's defense-in-depth argument**:

V1 argues A+D+E together achieve 0.25% miss rate. But this calculation assumes independence of failure modes (A-010 from the diff analysis). The 5 LLM tendencies are correlated: if the completeness bias causes the LLM to drop dispatch in generation, the same bias affects Solution E's LLM pass (even with structured output). V4's approach is different: Layers 1-2 are fully deterministic (zero correlation with LLM biases) and Layer 3 uses adversarial reframing (reduced correlation). V4's independence assumption is more defensible than V1's.

**Concession**: V4-4 (hybrid) requires 2 new modules + 1 prompt + gate wiring, making it the most complex primary solution after V3. If forced to ship one check immediately, V4-2 (fingerprints alone) is the right choice. The hybrid should be built incrementally.

---

### V5-Advocate Rebuttal

**Responding to V4's claim that fingerprints suffice**:

V4-2 catches omissions (identifier absent from roadmap). V5-1 catches inadequate coverage (identifier present but no explicit wiring task). The real-world failure mode going forward is likely the second kind: LLMs, once prompted to include identifiers (via V1-D/V5-2 prompt constraints), will mention them without planning to wire them. V4-2 would then produce false confidence: "all fingerprints present, coverage 100%" while the roadmap still has no population task for the dispatch table.

**Responding to V2's vocabulary breadth claim**:

V2-A's vocabulary is broader (any scaffold term), but V5-1's taxonomy is deeper (categorized by mechanism type). Breadth catches more surface-level patterns; depth catches the specific integration gap that caused the cli-portify bug. Going forward, after prompt constraints are added, the remaining bugs will be the deep ones -- not "we forgot to mention dispatch" but "we mentioned dispatch but did not plan to implement the wiring." V5-1 is optimized for the post-mitigation landscape.

**Responding to V3's coverage breadth advantage**:

V3's coherence graph catches more bug classes, but V5's rule engine is more extensible in practice. Adding a new detection rule to V5 is: define a regex pattern, add it to a list, done. Adding a new producer-consumer relationship to V3's graph requires modifying the extraction heuristics. The rule engine scales better with the number of known anti-patterns.

**Concession**: V5-1's pattern library currently covers only 4 dispatch pattern types and 2 wiring task pattern types. On a novel integration mechanism not in the taxonomy, V5-1 finds nothing. V4-2's fingerprint approach is mechanism-agnostic and would catch the novel case if the spec used code identifiers. V5-1 needs continuous expansion of its pattern library.

---

## Round 2 Convergence Matrix

| Dimension | Agreement Level | Shift from R1 | Notes |
|-----------|----------------|---------------|-------|
| Fingerprints > IDs for single-check efficacy | 90% | +5% | V1 concedes; V5 argues "present != planned" |
| Obligation scanner is a unique detection axis | 85% | 0% | Stable; all concede V2 catches different bugs |
| Coherence graph = broadest but riskiest | 85% | +5% | V3 argues existing infra reduces risk; V4 argues fragility |
| V5 "mentioned != planned" critique is valid | 80% | NEW | V4 partially concedes; argues threshold + adversarial layer mitigates |
| LLM tendency correlation (A-010) undermines independence | 85% | NEW | V4's rebuttal accepted; V1's miss-rate calculation weakened |
| False positive risk of V2-A is manageable | 75% | +5% | V2's component-context rebuttal partially addresses V1's concern |
| V3-1 extraction difficulty is the key risk | 80% | 0% | V3 argues existing modules help; others remain skeptical |

---

## Round 3: Final Positions on Unresolved Disagreements

### Unresolved Disagreement 1: Presence vs. Adequacy (V4 vs. V5)

**V4 final position**: Fingerprint presence is a necessary condition, and the adversarial LLM layer (Layer 3) provides the adequacy check. The hybrid covers both: deterministic presence + LLM-assessed adequacy. The "mentioned but not planned" failure mode is real but is addressed by the layered architecture.

**V5 final position**: The deterministic layer should itself assess adequacy where possible, not delegate it to an LLM. The integration contract extractor checks for explicit wiring *tasks*, not just identifier presence. This is deterministic adequacy assessment for the specific class of dispatch/registry/injection mechanisms.

**Resolution assessment**: Both positions have merit. V4's hybrid is more general (works on any identifier omission). V5's contract extractor is more precise (distinguishes mention from plan) for mechanism-specific bugs. In a merged solution, both contribute: fingerprints as a broad net, contracts as a targeted spear.

### Unresolved Disagreement 2: Coverage Breadth vs. Implementation Risk (V3 vs. V4/V5)

**V3 final position**: The coherence graph is the right long-term investment. Its implementation risk is overstated because the existing data flow infrastructure provides patterns to follow. The graph catches bug classes that no other proposal addresses (orphaned producers, unsatisfied consumers across any artifact type).

**V4/V5 final position**: The coherence graph should be a Phase 2 or Phase 3 deliverable, not the primary solution. Fingerprints (V4-2) and contracts (V5-1) ship faster, catch the cli-portify bug with higher confidence, and have lower implementation risk. The graph adds coverage later.

**Resolution assessment**: V3-1 should be adopted as a medium-priority complement, not as a primary base. The primary bases should be solutions that ship fast and catch the target bug with high confidence.

### Unresolved Disagreement 3: LLM Layers (V1-E positive framing vs. V4-3 negative framing)

**V1 final position**: Structured enumeration (V1-E) produces more auditable output. The per-pair table forces the LLM to name every producer-consumer pair, making gaps visible.

**V4 final position**: Negative-space prompting (V4-3) is more effective at counteracting completion bias. The evidence: the existing positive-framing spec-fidelity check failed. The structured table format from V1-E should be adopted for the output schema, but the prompt framing must be adversarial.

**Resolution assessment**: Merge V1-E's structured output format with V4-3's adversarial framing. The prompt should say "find gaps" (V4) and the output should be a per-deliverable table (V1-E).

### Unresolved Disagreement 4: Scaffold Vocabulary Scope (V2 vs. V5)

**V2 final position**: Scaffold-discharge is a universal pattern. Any roadmap with deferred commitments can be scanned. The vocabulary is extensible.

**V5 final position**: The anti-pattern rule engine (V5-3) should house V2-A's scaffold logic as one rule (AP-001 delegates to the obligation scanner). This gives V2's detection the organizational home of V5's extensible framework.

**Resolution assessment**: Agreement reachable. V2-A's scanner becomes the implementation of V5-3's AP-001 rule. The rule engine framework is V5's contribution; the scanner algorithm is V2's contribution.

---

## Scoring Matrix

Scoring each variant's **primary recommended solution** on the 4-dimension custom framework.

### V1 Primary: Defense-in-depth (A + D + E)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Efficacy (0.35) | 8 | Three layers together provide ~99% catch rate for the cli-portify class. But the joint-miss calculation assumes independence (A-010), which V4 correctly challenges. Individual layers: A=8, D=6, E=8. Composite efficacy is high but not 9+ because of correlation risk. |
| D2: Generalizability (0.25) | 7 | ID cross-ref applies to any spec with FR-NNN tags. Prompt constraint applies to any generation step. Integration LLM pass applies to any roadmap. But ID cross-ref degrades on informal specs, and the LLM pass shares the blindspots it mitigates. |
| D3: Implementation Complexity (0.20) | 5 | The combined A+D+E requires 1 new file + prompt changes + 1 new LLM pipeline step + gate wiring. Total ~330 LOC across 4 modified files. Not trivial, though each piece is individually small. |
| D4: Determinism (0.20) | 6 | Solution A is fully deterministic. Solution D is prompt-only (non-deterministic in effect). Solution E adds an LLM call. The combination is semi-deterministic: the deterministic floor (A) prevents the worst failures, but the LLM layer (E) can still produce false negatives. |

**V1 Composite**: (8 x 0.35) + (7 x 0.25) + (5 x 0.20) + (6 x 0.20) = 2.80 + 1.75 + 1.00 + 1.20 = **6.75**

---

### V2 Primary: Obligation Scanner (Solution A)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Efficacy (0.35) | 7 | Catches the cli-portify bug with ~85% confidence ("mocked steps" is a clear scaffold term, no discharge found). Misses cases where scaffolding uses non-standard vocabulary. Does not catch pure omissions (requirement absent entirely vs. obligation undischarged). |
| D2: Generalizability (0.25) | 7 | Applies to any roadmap with deferred commitments. Transfers to tasklist validation ("stub API" in task description -> check later tasks for real implementation). Vocabulary-dependent but extensible. |
| D3: Implementation Complexity (0.20) | 8 | ~200 LOC, 1 new file, 1 modified file (add SemanticCheck to MERGE_GATE). Clean integration with existing gate pattern. No model changes. Single-file operation (merged roadmap). |
| D4: Determinism (0.20) | 9 | Pure Python regex matching. Zero LLM calls. Identical results on same input. Phase splitting and component context extraction are fully deterministic. |

**V2 Composite**: (7 x 0.35) + (7 x 0.25) + (8 x 0.20) + (9 x 0.20) = 2.45 + 1.75 + 1.60 + 1.80 = **7.60**

---

### V3 Primary: Coherence Graph (Solution 1)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Efficacy (0.35) | 6 | Catches the cli-portify bug with ~75% confidence. The heuristic extraction of producers/consumers from natural language is the weak link -- if the roadmap uses abstract language ("implement step runners" rather than naming specific modules), the graph has insufficient nodes. |
| D2: Generalizability (0.25) | 9 | Broadest coverage of any single solution. Catches any cross-phase data flow gap: orphaned modules, unsatisfied imports, disconnected pairs. Transfers to tasklist and sprint validation. Not limited to specific vocabulary or mechanism types. |
| D3: Implementation Complexity (0.20) | 4 | ~300 LOC across 2 new files + 2 modified files. Requires heuristic NLP extraction (the hard part). Maps to existing infrastructure but still requires new extraction logic. Medium-high effort. |
| D4: Determinism (0.20) | 8 | Pure Python graph analysis after extraction. The extraction step is heuristic (regex-based) but deterministic. No LLM calls. Reproducible results on same input. Slight deduction for heuristic fragility. |

**V3 Composite**: (6 x 0.35) + (9 x 0.25) + (4 x 0.20) + (8 x 0.20) = 2.10 + 2.25 + 0.80 + 1.60 = **6.75**

---

### V4 Primary: Hybrid IDs + Fingerprints + Adversarial Prompt (Solution 4)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Efficacy (0.35) | 9 | Three layers with the highest-efficacy single check (fingerprints at 95%). Layer 1 (IDs) catches formal omissions. Layer 2 (fingerprints) catches code-level omissions. Layer 3 (negative-space) catches semantic gaps. Independence between deterministic and adversarial layers is stronger than V1's all-positive-framing independence. |
| D2: Generalizability (0.25) | 7 | IDs work on formal specs; fingerprints work on code-heavy specs; negative-space works on any spec. Together they cover the format spectrum. But ID and fingerprint checks are roadmap-specific; transferring to tasklist/sprint requires separate implementation. |
| D3: Implementation Complexity (0.20) | 4 | 2 new files (id_crossref.py, fingerprint.py) + 1 new prompt + 3 modified files. ~350 LOC total. Requires multi-file access workaround for gates (SemanticCheck limitation). Most complex primary solution. |
| D4: Determinism (0.20) | 6 | Layers 1-2 are fully deterministic. Layer 3 is LLM-dependent (though adversarially reframed). The hybrid is semi-deterministic: the deterministic floor prevents catastrophic failures, but the LLM layer adds token cost and non-repeatability. |

**V4 Composite**: (9 x 0.35) + (7 x 0.25) + (4 x 0.20) + (6 x 0.20) = 3.15 + 1.75 + 0.80 + 1.20 = **6.90**

---

### V5 Primary: Integration Contract Extractor (Solution 1)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| D1: Efficacy (0.35) | 8 | Catches the cli-portify bug with ~90% confidence. The spec contained `PROGRAMMATIC_RUNNERS` dispatch table definition; the contract extractor's `DISPATCH_PATTERNS` would match it; the roadmap had no wiring task matching `WIRING_TASK_PATTERNS`. Clear detection. Slight deduction because pattern library coverage is finite. |
| D2: Generalizability (0.25) | 7 | Applies to any spec with dispatch tables, registries, injection points, or routing mechanisms (V5's 7-category taxonomy). Does not catch non-mechanism omissions (e.g., dropped NFRs, missed test requirements). The rule engine framework (Solution 3) extends coverage to other anti-patterns. |
| D3: Implementation Complexity (0.20) | 6 | ~250 LOC, 1 new file, 2 modified files. Requires multi-file access (spec + roadmap). The pattern library needs calibration. More complex than V2-A but simpler than V3-1 or V4-4. |
| D4: Determinism (0.20) | 9 | Pure Python regex matching against two pattern libraries. Zero LLM calls. Reproducible. Mechanism classification is deterministic. |

**V5 Composite**: (8 x 0.35) + (7 x 0.25) + (6 x 0.20) + (9 x 0.20) = 2.80 + 1.75 + 1.20 + 1.80 = **7.55**

---

## Scoring Summary Table

| Variant | Primary Solution | D1 (0.35) | D2 (0.25) | D3 (0.20) | D4 (0.20) | Composite |
|---------|-----------------|-----------|-----------|-----------|-----------|-----------|
| **V2** | Obligation Scanner | 7 | 7 | **8** | **9** | **7.60** |
| **V5** | Integration Contract Extractor | 8 | 7 | 6 | **9** | **7.55** |
| **V4** | Hybrid (IDs + Fingerprints + Adversarial) | **9** | 7 | 4 | 6 | 6.90 |
| **V1** | Defense-in-depth (A + D + E) | 8 | 7 | 5 | 6 | 6.75 |
| **V3** | Coherence Graph | 6 | **9** | 4 | 8 | 6.75 |

**Top 2**: V2 (7.60) and V5 (7.55) are co-bases for merge.

---

## Complementary Elements from Non-Selected Variants

### From V4 (rank 3, score 6.90)

- **V4-2 (Fingerprint extraction)**: Cherry-pick as an additional deterministic layer. Fingerprints have the highest single-check efficacy (95%) and complement V5's mechanism-specific contracts with mechanism-agnostic identifier matching. ~150 LOC, clean integration.
- **V4-3 (Negative-space prompting)**: Cherry-pick the adversarial prompt framing (merged with V1-E's structured output format) as the LLM validation layer. Addresses the self-audit blindness that the existing spec-fidelity gate suffers from.

### From V1 (rank 4, score 6.75)

- **V1-C (Spec structural audit)**: Cherry-pick as the upstream guard. The only solution that validates the extraction step itself. ~80 LOC, zero LLM, sub-100ms.
- **V1-A / V4-1 (ID cross-reference)**: Already subsumed by V4-4 (Layer 1). If V4-2 fingerprints are adopted, the ID cross-ref is lower priority but still low-cost to include.

### From V3 (rank 5, score 6.75)

- **V3-1 (Coherence graph)**: Defer to Phase 2 as a medium-priority enhancement. Broadest coverage but highest implementation risk. Should build on existing dataflow infrastructure when ready.
- **V3-2 (Manifest injection)**: Consider merging with V2-B (obligation ledger) into a single "prior phase context" injection block for generation prompts. Prevention-layer complement to detection-layer solutions.

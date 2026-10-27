# Diff Analysis: Anti-Instinct Proposals 01-05

**Date**: 2026-03-17
**Protocol**: sc:adversarial Step 1 (Diff Analysis)
**Depth**: deep
**Focus**: efficacy, implementability, coverage

---

## 1. Structural Differences (S-NNN)

| ID | Category | V1 (Completeness Bias) | V2 (Implicit Obligation) | V3 (Local Coherence) | V4 (Self-Audit Blindness) | V5 (Pattern-Matching Trap) | Severity |
|----|----------|----------------------|------------------------|--------------------|--------------------------|-----------------------------|----------|
| S-001 | Section count | 8 sections (incl. Open Questions) | 8 sections (incl. Risks/Mitigations table) | 5 sections + success criteria | 8 sections (incl. Open Questions) | 5 sections + appendix taxonomy | LOW |
| S-002 | Solution count | 5 solutions (A-E) | 4 solutions (A-D) | 4 solutions (1-4) | 5 solutions (1-5) | 3 solutions (1-3) | MEDIUM |
| S-003 | Code specificity | Full implementation code for Solutions A, B, C; prompt text for D; structured prompt for E | Full implementation for Solution A (~200 LOC); JSON schema for B; prompt for C; one-liner for D | Dataclass sketches for Solution 1; markdown template for Solution 2; Step extension for Solution 3; function signature for Solution 4 | Full implementation for Solutions 1, 2; full prompt text for Solution 3; layered table for Solution 4; full registry for Solution 5 | Full implementation for Solution 1 (~250 LOC); prompt block for Solution 2; full rule engine for Solution 3 | HIGH |
| S-004 | Files-to-modify table | Explicit table with new/modified split | Inline in implementation plan | Referenced in "Relationship to Existing Infrastructure" section | Explicit table (Section 7) | Explicit table (Files Changed) | MEDIUM |
| S-005 | Implementation phasing | 3 phases mapped to versions (v2.27, v2.28, v2.29+) | 3 phases (Priority: High/Medium/Low) | 3 phases (A/B/C by priority) | 4 phases (incremental build-up) | 4 phases (deterministic first, prompt second, gate third, test fourth) | LOW |
| S-006 | Evidence section depth | Detailed propagation chain diagram (Spec -> Roadmap -> Tasklist -> Code) with 4-system pattern table | Detailed root cause analysis of prompt mechanics; explains why existing gates failed per-gate | Brief 3-bullet summary of the phase disconnect | Full gate failure analysis including frontmatter field names and line numbers in gates.py | Focused on why spec-fidelity dimensions missed dispatch tables; identifies the missing 6th dimension | HIGH |
| S-007 | Existing infra mapping | Section 7 maps to specific file:line references (gates.py:633-656, gates.py:712-758) | References executor.py, prompts.py, gates.py by function name | Section "Relationship to Existing Infrastructure" maps to 5 existing modules (dataflow_graph.py, dataflow_pass.py, deliverables.py, conflict_detector.py, contract_extractor.py) | References gates.py semantic check signatures and pipeline model constraints | References prompts.py::build_spec_fidelity_prompt and its 5 comparison dimensions | HIGH |
| S-008 | Risk/limitation treatment | Per-solution limitation paragraphs + combined open questions section | Dedicated risk table (4 rows with severity + mitigation) | Success criteria section with 4 measurable targets | Per-solution limitation bullets + 5 open debate questions | Per-solution pros/cons; appendix with integration mechanism taxonomy | MEDIUM |
| S-009 | Vocabulary/taxonomy | No taxonomy; ID-pattern focused | Scaffold/discharge vocabulary table (10 scaffold terms, 10 discharge terms, bidirectional mapping) | Producer/consumer/wiring action pattern lists | Fingerprint categories (identifier, definition, constant) + exclusion list | Integration mechanism taxonomy (7 categories: dict dispatch, plugin registry, callback injection, strategy, middleware, event binding, DI container) | HIGH |

### S-NNN Summary

V1 and V4 are the most structurally complete documents with explicit file tables, open questions, and per-solution confidence ratings. V2 has the most operationally detailed implementation (the obligation scanner is nearly production-ready code). V3 is the most architecturally grounded, mapping extensively to existing pipeline infrastructure. V5 has the most thorough taxonomy of the problem space (7-category integration mechanism table) but the fewest solutions.

---

## 2. Content Differences (C-NNN)

### 2.1 Detection Mechanism Philosophy

| ID | Dimension | V1 | V2 | V3 | V4 | V5 |
|----|-----------|----|----|----|----|-----|
| C-001 | Primary detection type | Deterministic (ID cross-ref) | Deterministic (regex term matching) | Deterministic (graph analysis) | Hybrid (deterministic floor + adversarial LLM) | Deterministic (contract pattern matching) |
| C-002 | LLM involvement | Solutions D, E use LLM; A, B, C are deterministic | Solution C uses LLM; A, D are deterministic; B injects into LLM prompt | Solution 2 injects manifest into LLM prompt; Solutions 1, 3, 4 are deterministic | Solutions 3, 4 use LLM (adversarial reframing); Solutions 1, 2 are deterministic | Solution 2 uses LLM (prompt augmentation); Solutions 1, 3 are deterministic |
| C-003 | Detection granularity | Per-requirement-ID | Per-scaffolding-term-per-phase | Per-artifact-per-phase (producer/consumer pairs) | Per-code-identifier (fingerprints) + per-requirement-ID | Per-integration-contract (dispatch tables, registries, injection points) |
| C-004 | False positive risk | Low (IDs are precise) but depends on extraction quality | Medium (scaffold terms in test descriptions, code examples) | Medium (heuristic component extraction from natural language) | Low for IDs; medium for fingerprints (illustrative examples vs requirements) | Low-medium (dispatch patterns are specific but may match non-requirement text) |
| C-005 | Novel detection concept | Traceability coverage ratio as a metric | Scaffold-discharge pairing as a formal concept | Producer-consumer graph with disconnected pair detection | Negative-space prompting (invert the review question) | Integration contract as a first-class extractable entity |

### 2.2 Pipeline Insertion Point

| ID | Variant | Where it gates | Pre-generation | Post-generation | Post-merge | Post-fidelity |
|----|---------|---------------|----------------|-----------------|------------|---------------|
| C-010 | V1-A | Post-merge, before spec-fidelity | | | X | |
| C-011 | V1-C | Between extract and generate | X | | | |
| C-012 | V1-D | During generation (prompt constraint) | X | | | |
| C-013 | V1-E | Post-merge, alongside spec-fidelity | | | X | |
| C-014 | V2-A | Post-merge (MERGE_GATE semantic check) | | | X | |
| C-015 | V2-B | During generation (injected into each phase prompt) | X | | | |
| C-016 | V2-C | Post-merge, new step before spec-fidelity | | | X | |
| C-017 | V3-1 | Post-all-phases, after merge | | | X | |
| C-018 | V3-2 | During generation (manifest injected per-phase) | X | X | | |
| C-019 | V3-3 | Pre-generation (step declarations) | X | | | |
| C-020 | V4-1 | Post-merge, pre-spec-fidelity | | | X | |
| C-021 | V4-2 | Post-merge, pre-spec-fidelity | | | X | |
| C-022 | V4-3 | Post-merge, parallel with spec-fidelity | | | X | |
| C-023 | V5-1 | Post-merge, between merge and spec-fidelity | | | X | |
| C-024 | V5-2 | During generation (prompt block) | X | | | |
| C-025 | V5-3 | Post-merge (anti-pattern scan) | | | X | |

**Pattern**: 12 of 16 solutions gate post-merge. Only V1-C (spec structural audit), V1-D, V2-B, V3-2, V3-3, and V5-2 operate upstream of or during generation. This reveals a collective bias toward detection over prevention.

### 2.3 Bug Class Coverage

| ID | Bug class | V1 | V2 | V3 | V4 | V5 |
|----|-----------|----|----|----|----|-----|
| C-030 | Omitted requirement IDs | A (primary) | -- | -- | 1 (primary) | -- |
| C-031 | Missing wiring/dispatch | B, D, E | -- | 1 (primary) | 2 (fingerprints) | 1 (primary), 3 |
| C-032 | Undischarged scaffolding | -- | A (primary) | -- | -- | 3 (AP-001) |
| C-033 | Orphaned components | B (primary) | -- | 1 (orphan_producers) | -- | -- |
| C-034 | Extraction dropping requirements | C (primary) | -- | -- | 1, 5 (if extraction drops) | -- |
| C-035 | Self-audit blindspot | E (structured constraint) | -- | -- | 3 (negative-space prompting, primary) | -- |
| C-036 | Pattern-matching overgeneralization | D (prompt) | -- | -- | -- | 1, 2, 3 (primary) |
| C-037 | Cross-phase coherence failure | -- | A, B (primary) | 1, 2, 3, 4 (primary) | -- | -- |
| C-038 | Implicit obligation loss | -- | A, B, C, D (primary) | 2 (manifest) | -- | -- |
| C-039 | Code-level identifier omission | -- | -- | -- | 2 (primary) | 1 (identifier extraction) |

**Key finding**: V2 and V3 are the only variants that address cross-phase coherence. V4 is the only variant with negative-space prompting. V5 is the only variant with a pattern taxonomy. V1-C is the only solution that guards the extraction step itself.

### 2.4 Implementation Complexity

| ID | Solution | New files | Modified files | LOC estimate | LLM calls added | Execution time |
|----|----------|-----------|---------------|-------------|-----------------|----------------|
| C-040 | V1-A (Traceability) | 1 | 2 | ~100 | 0 | <100ms |
| C-041 | V1-B (Orphan detector) | 1 | 1 | ~200 | 0 | <500ms |
| C-042 | V1-C (Spec structural audit) | 1 | 1 | ~80 | 0 | <100ms |
| C-043 | V1-D (Prompt constraint) | 0 | 1 | ~30 lines prompt | 0 | 0 (prompt only) |
| C-044 | V1-E (Integration LLM pass) | 0 | 3 | ~200 | 1 | ~60s |
| C-045 | V2-A (Obligation scanner) | 1 | 1 | ~200 | 0 | <100ms |
| C-046 | V2-B (Obligation ledger) | 1 | 2 | ~300 | 0 (but modifies LLM prompts) | <100ms + prompt overhead |
| C-047 | V2-C (Dual-pass LLM) | 0 | 2 | ~100 | 1 | ~60s |
| C-048 | V3-1 (Coherence graph) | 2 | 2 | ~300 | 0 | <5s |
| C-049 | V3-2 (Manifest injection) | 1 | 2 | ~200 | 0 (modifies prompts) | <100ms + prompt overhead |
| C-050 | V3-3 (Phase DAG) | 1 | 1 | ~150 | 0 | <100ms |
| C-051 | V3-4 (Integration test synth) | 1 | 1 | ~200 | 0 | <1s |
| C-052 | V4-1 (ID cross-ref) | 1 | 2 | ~100 | 0 | <100ms |
| C-053 | V4-2 (Fingerprints) | 1 | 1 | ~150 | 0 | <100ms |
| C-054 | V4-3 (Negative-space prompt) | 0 | 3 | ~100 | 1 | ~60s |
| C-055 | V4-4 (Hybrid) | 2 | 3 | ~350 | 1 | <60s |
| C-056 | V4-5 (Requirement registry) | 1 | 3 | ~200 | 0 (but requires LLM to update) | <100ms |
| C-057 | V5-1 (Integration contracts) | 1 | 2 | ~250 | 0 | <500ms |
| C-058 | V5-2 (Prompt augmentation) | 0 | 1 | ~50 lines prompt | 0 | 0 (prompt only) |
| C-059 | V5-3 (Anti-pattern rules) | 1 | 1 | ~150 | 0 | <100ms |

### 2.5 Integration with Existing Gate Infrastructure

| ID | Aspect | V1 | V2 | V3 | V4 | V5 |
|----|--------|----|----|----|----|-----|
| C-060 | Gate pattern used | New GateCriteria + SemanticCheck | SemanticCheck on existing MERGE_GATE | New COHERENCE_GATE (GateCriteria) | SemanticCheck on existing SPEC_FIDELITY_GATE + new NEGATIVE_SPACE_GATE | New INTEGRATION_AUDIT_GATE (GateCriteria) |
| C-061 | Requires model.py changes | No (V1-A Option A); Yes (V1-A Option B: extend SemanticCheck) | No | No | Yes (Option B: extend SemanticCheck with context_files) | No (uses placeholder semantic check; real logic in executor) |
| C-062 | Enforcement tier | Not stated (implied STRICT for A) | Not stated for MERGE_GATE | TRAILING in v1, promote to STRICT | Implied STRICT (deterministic layers cannot be overridden) | STRICT from the start |
| C-063 | Multi-file access needed | Yes (extraction.md + roadmap.md) | No (single merged roadmap) | Yes (per-phase outputs + merged roadmap) | Yes (spec + roadmap for fingerprints) | Yes (spec + roadmap for contract checking) |

**Key finding**: The SemanticCheck signature `check_fn: Callable[[str], bool]` takes only one content string. V1, V4, and V5 all need multi-file access for their deterministic checks but handle it differently: V1 proposes a pre-gate executor hook (Option A) or model extension (Option B); V4 proposes the same two options; V5 sidesteps with a placeholder semantic check and runs real logic in the executor. V2 and V3 avoid the problem by operating on the single merged roadmap. This is a real architectural tension that the proposals handle inconsistently.

---

## 3. Contradictions (X-NNN)

| ID | Variants | Contradiction | Severity | Resolution |
|----|----------|--------------|----------|------------|
| X-001 | V1-A vs V4-1 | Both propose nearly identical requirement-ID cross-reference solutions (regex extraction of FR-NNN/NFR-NNN/SC-NNN from extraction.md, set difference against roadmap). V1 calls it "traceability.py"; V4 calls it "id_crossref.py". Same logic, different module names, different gate integration patterns. Implementing both would be pure duplication. | HIGH | Must be merged into one module. V4's naming (`id_crossref.py`) is clearer. V1's gate integration (standalone traceability gate) is cleaner than V4's executor-hook approach. |
| X-002 | V1-D vs V5-2 | Both propose prompt-level interventions for the generate step. V1-D focuses on integration task injection ("Wire X into Y"); V5-2 focuses on forced integration enumeration ("enumerate ALL integration points before generating"). They overlap significantly but V5-2 is more structured (demands an enumeration section). Both modify `build_generate_prompt()` in prompts.py. | MEDIUM | Merge into a single prompt block. V5-2's enumeration requirement subsumes V1-D's constraint. |
| X-003 | V1-B vs V3-1 | Both build producer-consumer graphs from roadmap text. V1-B calls them "orphaned components" and focuses on in-degree/out-degree analysis. V3-1 calls them "coherence graphs" and adds the "disconnected pair" concept (producer and consumer both exist but no wiring edge). V3-1 is strictly more capable. | MEDIUM | V3-1 subsumes V1-B. The "disconnected pair" detection is the key addition. Implement V3-1; V1-B adds nothing V3-1 does not cover. |
| X-004 | V2-A vs V5-3 (AP-001) | V2-A scans for scaffold terms and checks for discharge terms in later phases. V5-3's AP-001 rule does the same thing (scaffold + implement without wiring = flag). They use different term lists and different matching strategies (V2-A does per-phase sequential scan with component context; V5-3 does whole-document boolean scan). V2-A is more precise (tracks which component the scaffold refers to); V5-3 is coarser but simpler. | MEDIUM | V2-A is strictly better for this specific check. V5-3's rule engine framework is useful for housing other anti-patterns, but AP-001 should delegate to V2-A's scanner. |
| X-005 | V1-E vs V4-3 | Both add a new LLM pipeline step for gap detection, but with opposing framing. V1-E asks the LLM to enumerate producer-consumer pairs and name the wiring task for each (positive framing: "name what exists"). V4-3 asks the LLM to find what is missing (negative framing: "find gaps"). V4 explicitly argues that negative framing counteracts completion bias better than positive framing. These are incompatible philosophies: you cannot do both in one prompt without diluting the framing. | HIGH | This is a genuine design disagreement. V4's argument is well-supported by the forensic evidence (the existing spec-fidelity check uses positive framing and failed). Negative-space prompting (V4-3) should be preferred, but V1-E's structured table output format should be adopted for the response schema. |
| X-006 | V2-B vs V3-2 | Both inject accumulated state into phase prompts during generation. V2-B injects an "obligation ledger" (what earlier phases deferred). V3-2 injects a "deliverable manifest" (what earlier phases produced). These are complementary, not contradictory, but both modify the same function (`build_generate_prompt`) and add competing context blocks. Injecting both would bloat the prompt. | MEDIUM | Merge into a single "prior phase context" injection that includes both deliverables (manifest) and outstanding obligations (ledger). One block, not two. |
| X-007 | V3 vs V4 on enforcement tier | V3 recommends TRAILING enforcement for the coherence gate in v1 ("emits warnings rather than failing"). V4 recommends deterministic layers be non-overridable from the start. V5 recommends STRICT from the start. | MEDIUM | V4/V5 are correct for deterministic checks (they have zero false-positive risk on true positives). V3 is correct for heuristic graph extraction (higher false-positive risk). Resolution: deterministic checks = STRICT; heuristic checks = TRAILING initially. |
| X-008 | V4-5 vs all others on statefulness | V4-5 (Requirement Registry) introduces a stateful JSON artifact that persists across pipeline steps and requires each step to update it. All other solutions operate statelessly (each is a pure function of its inputs). V4 itself acknowledges this as a "significant architectural change." | LOW | V4-5 is architecturally incompatible with the current stateless pipeline model. The other 4 variants implicitly reject this approach by not proposing it. Defer V4-5 unless the pipeline moves to stateful execution. |

---

## 4. Unique Contributions (U-NNN)

| ID | Variant | Unique contribution | Why no other variant covers it | Value for efficacy/implementability/coverage |
|----|---------|-------------------|------------------------------|---------------------------------------------|
| U-001 | V1 | **Spec structural audit (Solution C)**: Guards the extraction step itself by counting structural indicators in the raw spec and comparing against the extraction's requirement count | V2-V5 all assume the extraction is correct and validate downstream artifacts. V1-C is the only proposal that asks "did the extraction LLM drop something?" | HIGH efficacy: catches the root cause (extraction loss) that makes all downstream checks vacuous. MEDIUM implementability: simple regex counting. HIGH coverage: protects against any extraction failure, not just dispatch. |
| U-002 | V1 | **Combined miss-rate calculation**: Explicitly computes the joint probability of all three checks missing the same bug (0.25 * 0.10 * 0.10 = 0.0025) | No other variant quantifies defense-in-depth effectiveness | MEDIUM value: useful for design justification but the numbers are estimates. |
| U-003 | V2 | **Scaffold-discharge vocabulary as a formal concept**: Defines the bidirectional mapping between scaffold terms and their expected discharge terms | V1/V3/V4/V5 detect omissions by looking for what should be present. V2 detects by looking for what was promised but not fulfilled -- a fundamentally different detection axis | HIGH efficacy: catches a bug class (undischarged scaffolding) that pure ID-matching or graph analysis misses if the scaffold was never a formal requirement. MEDIUM coverage: limited to scaffolding language specifically. |
| U-004 | V2 | **Obligation ledger as pipeline state (Solution B)**: Accumulates deferred commitments across phases and injects them into subsequent prompts | V3-2's manifest injection tracks deliverables (what was built) but not obligations (what was promised for later). The obligation ledger is the inverse. | HIGH efficacy: preventive rather than detective. MEDIUM implementability: requires state management and prompt injection. |
| U-005 | V3 | **Mapping to existing dataflow infrastructure**: Identifies 5 existing modules (dataflow_graph.py, dataflow_pass.py, deliverables.py, conflict_detector.py, contract_extractor.py) that provide architectural precedent | No other variant maps to existing non-gate infrastructure. V1/V4/V5 reference only gates.py and executor.py. | HIGH implementability: reduces implementation risk by building on proven patterns. |
| U-006 | V3 | **Integration test synthesis (Solution 4)**: Programmatically generates integration test specifications from the coherence graph | No other variant proposes generating tests as a mitigation. All others focus on gates/prompts. | MEDIUM efficacy: tests expose the bug at code-generation time. LOW implementability: complex to make test specs actionable. HIGH coverage: test generation is reusable across all bug classes. |
| U-007 | V3 | **Phase DAG with declared inputs/outputs (Solution 3)**: Extends the Step model with typed I/O declarations | No other variant proposes modifying the pipeline Step model itself | LOW implementability (high upfront cost). HIGH long-term coverage: enables compile-time-like validation of pipeline structure. |
| U-008 | V4 | **Negative-space prompting**: Inverts the review question from "confirm completeness" to "find gaps" with explicit anti-bias instructions | No other variant addresses the review framing problem. V1-E uses structured output but still asks "enumerate pairs" (positive framing). | HIGH efficacy: directly counteracts the specific LLM tendency (completion bias) that caused the gate failure. MEDIUM implementability: prompt-only change. MEDIUM coverage: applies to any spec-vs-artifact comparison. |
| U-009 | V4 | **Structural fingerprint extraction (Solution 2)**: Extracts backtick-delimited identifiers, code-block definitions, and ALL_CAPS constants as a coverage baseline | V1-A and V4-1 match formal IDs only. V4-2 matches any code-level identifier, catching specs that don't use formal FR-NNN tags. | HIGH efficacy: directly catches the cli-portify bug regardless of ID tagging. HIGH coverage: works on any spec with code examples. |
| U-010 | V4 | **Layered defense table with explicit "can be overridden by LLM?" column** | No other variant explicitly categorizes which checks the LLM can bypass and which it cannot | HIGH architectural value: makes the deterministic/non-deterministic boundary visible. |
| U-011 | V5 | **Integration contract as a first-class entity**: Defines IntegrationContract dataclass with mechanism type, spec evidence, and explicit_wiring flag | V1-B and V3-1 detect missing wiring generically. V5 categorizes the specific mechanism type (dispatch_table, registry, dependency_injection, routing, etc.) | HIGH efficacy: mechanism-aware matching is more precise than generic graph analysis. MEDIUM coverage: requires pattern library to be comprehensive. |
| U-012 | V5 | **Integration mechanism taxonomy (7 categories)**: Dict dispatch, plugin registry, callback injection, strategy pattern, middleware chain, event binding, DI container | No other variant enumerates the categories of integration that LLMs typically miss | HIGH coverage: provides a roadmap for expanding pattern libraries. Makes the problem space concrete and bounded. |
| U-013 | V5 | **Anti-pattern rule engine**: Extensible rule-based system for detecting known dangerous roadmap patterns | V2-A detects one pattern (undischarged scaffolding). V5-3 provides a framework for multiple patterns. | MEDIUM implementability: simple rule framework. HIGH long-term coverage: new rules can be added without pipeline changes. |

---

## 5. Shared Assumptions (A-NNN)

| ID | Assumption | All variants assume this? | Why it could be wrong | Risk if wrong | Severity |
|----|-----------|--------------------------|----------------------|---------------|----------|
| A-001 | **The extraction step produces requirement IDs (FR-NNN, etc.)** | V1 (A), V4 (1, 5) depend on this explicitly. V2, V3, V5 do not. | The extraction prompt may produce prose descriptions without formal IDs. The ID format is a convention of the extraction prompt, not a guaranteed output format. If the prompt changes or the LLM deviates, IDs may be absent or inconsistent. | V1-A and V4-1 become vacuous (0 IDs to check = 100% coverage). V4 mitigates this with fingerprints (Solution 2) as fallback. | HIGH |
| A-002 | **The merged roadmap uses natural-language phase descriptions that are parseable by regex** | All 5 variants assume roadmap text contains detectable patterns (scaffold terms, component names, integration language, phase headings). | A roadmap could use highly abstract language ("Phase 3: Core implementation") without naming specific modules, functions, or mechanisms. All regex-based solutions would extract zero signals. | All deterministic checks produce false negatives. The roadmap passes all gates while still being incomplete. | HIGH |
| A-003 | **The pipeline has a `merge` step that produces a single consolidated roadmap** | V1 (A, B, E), V2 (A, C), V3 (1), V4 (1, 2, 3), V5 (1, 3) all gate on the merged output. | If the pipeline architecture changes (e.g., phases are validated independently without merging first), the post-merge gates have no insertion point. | All post-merge solutions become homeless. Mitigation: V2-B and V3-2 (prompt injection) work regardless of merge step existence. | MEDIUM |
| A-004 | **Scaffolding language is detectable via keyword matching** | V2 explicitly and V5-3 implicitly. | LLMs can express deferral without using standard scaffold vocabulary: "for now, use direct calls" (no scaffold term), "the executor handles steps sequentially" (implies mocks without saying "mock"), "Phase 2 output is a working skeleton" (only "skeleton" matches, but context is ambiguous). | V2-A's scanner misses non-vocabulary deferral. V2 acknowledges this and proposes LLM fallback (Solution D). | MEDIUM |
| A-005 | **The spec defines requirements at a level of specificity that survives extraction** | All 5 variants. | Some specs are high-level ("build an executor that runs steps") without naming dispatch tables, registries, or specific functions. The more abstract the spec, the less signal any gate can extract. | All solutions degrade gracefully but lose efficacy on abstract specs. V5's integration contract extractor finds nothing if the spec uses no dispatch patterns. V4's fingerprint checker finds nothing if the spec uses no code-level identifiers. | HIGH |
| A-006 | **A single point of gate insertion (post-merge, pre-fidelity) is architecturally stable** | 12 of 16 solutions assume this insertion point exists and will persist. | The pipeline step ordering is defined in executor.py and could be refactored. If steps are reordered, parallelized, or the fidelity check is moved, gate insertion points shift. | Solutions need re-wiring. Low-cost fix but adds maintenance burden. | LOW |
| A-007 | **The SemanticCheck model is the right abstraction for these checks** | V1, V2, V4, V5 add semantic checks to existing gates. V3 creates new gates. | The SemanticCheck signature (`Callable[[str], bool]`) cannot access multiple files. V1, V4, V5 all hit this limitation and propose workarounds (executor hooks, model extensions). This suggests the abstraction is insufficient for cross-artifact validation. | Workarounds add complexity and fragility. The underlying model may need to evolve. | HIGH |
| A-008 | **False positives are manageable at proposed thresholds** | V1-A (95% coverage), V4-2 (70% fingerprint coverage), V2-A (zero undischarged = pass). | No empirical data exists. The thresholds are educated guesses. Too strict = pipeline blocks on valid roadmaps. Too lenient = bugs pass through. | Requires shadow-mode validation on real roadmap runs before enforcement. V1 and V4 acknowledge this; V2, V3, V5 do not. | MEDIUM |
| A-009 | **The bug is detectable from the roadmap text alone** | All post-generation solutions assume the roadmap contains enough signal to detect the omission. | If the roadmap says "Implement executor with step dispatch" (technically mentioning dispatch), all text-matching solutions may conclude the requirement is covered -- even though "implement executor with step dispatch" is a vague task that does not specify the PROGRAMMATIC_RUNNERS dictionary or three-way branching. | Presence of a keyword is not presence of a sufficient task. All regex-based solutions conflate mention with coverage. V1-E and V4-3 (LLM-based) are better at judging sufficiency but are non-deterministic. | HIGH |
| A-010 | **The 5 LLM tendencies are independent failure modes** | Implicit across all 5 proposals (each targets one tendency). | The tendencies are correlated. Completeness bias (V1) enables self-audit blindness (V4). Pattern-matching (V5) causes the local coherence trap (V3). Implicit obligation loss (V2) is a manifestation of local coherence failure (V3). Mitigating one tendency may partially mitigate another, or -- critically -- mitigating one while ignoring a correlated one may leave a residual path for the same bug. | Defense-in-depth calculations (V1's 0.25% joint miss rate) overestimate effectiveness if failure modes are correlated rather than independent. | HIGH |

---

## 6. Cross-Variant Synthesis: Focus Area Analysis

### Efficacy (Would it catch the cli-portify bug?)

| Rank | Solution | Confidence | Rationale |
|------|----------|-----------|-----------|
| 1 | V4-2 (Fingerprints) | VERY HIGH (95%) | The spec contained `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` in backticks/code blocks. These are hard signals. The roadmap contained none. Fingerprint coverage would have been near 0%. No threshold tuning ambiguity. |
| 2 | V5-1 (Integration contracts) | HIGH (90%) | The spec contained `PROGRAMMATIC_RUNNERS` dispatch table definition. The contract extractor pattern library includes this pattern. The roadmap had no wiring task. Clear detection. |
| 3 | V2-A (Obligation scanner) | HIGH (85%) | "Mocked steps" in Phase 2 milestone is a clear scaffold term. No discharge term in later phases. Clean detection. |
| 4 | V1-A / V4-1 (ID cross-ref) | HIGH (80%) | Depends on extraction having produced FR-NNN for the dispatch requirement. Likely but not certain. |
| 5 | V3-1 (Coherence graph) | MEDIUM-HIGH (75%) | Depends on heuristic extraction of producer-consumer relationships from natural language. The roadmap used abstract language ("implement step runners") that may or may not parse cleanly into graph nodes. |
| 6 | V4-3 (Negative-space prompt) | HIGH (80%) | The adversarial reframing is well-designed, but LLM-dependent. |
| 7 | V1-D / V5-2 (Prompt constraints) | MEDIUM (65%) | Reduces probability of the bug during generation but cannot guarantee it. |

### Implementability (How hard to build?)

| Rank | Solution | Effort | Rationale |
|------|----------|--------|-----------|
| 1 | V1-D / V5-2 (Prompt constraints) | Trivial | 30-50 lines of prompt text added to one function. No new files, no new gates, no model changes. |
| 2 | V1-A / V4-1 (ID cross-ref) | Low | ~100 LOC new module + 1 semantic check. Well-understood pattern. |
| 3 | V2-A (Obligation scanner) | Low-Medium | ~200 LOC with phase splitting and component context extraction. More regex complexity than ID cross-ref but still straightforward. |
| 4 | V4-2 (Fingerprints) | Low-Medium | ~150 LOC. Identifier extraction is well-defined. Threshold tuning is the main risk. |
| 5 | V5-1 (Integration contracts) | Medium | ~250 LOC with two pattern libraries (dispatch patterns + wiring task patterns). Requires multi-file access workaround in gates. |
| 6 | V5-3 (Anti-pattern rules) | Medium | Rule framework is simple; writing good rules requires domain expertise and iteration. |
| 7 | V3-1 (Coherence graph) | Medium-High | ~300 LOC across 2 new files. Heuristic extraction of producers/consumers from natural language is the hard part. |
| 8 | V2-B / V3-2 (Prompt injection) | Medium-High | Requires state management between pipeline steps, prompt modification, and testing that the LLM actually reads the injection. |
| 9 | V4-5 (Requirement registry) | High | Stateful JSON artifact, state machine transitions, requires every pipeline step to participate. Architectural change. |

### Coverage (What other bug classes does it catch beyond cli-portify?)

| Rank | Solution | Coverage breadth | Bug classes beyond cli-portify |
|------|----------|-----------------|-------------------------------|
| 1 | V3-1 (Coherence graph) | VERY HIGH | Any cross-phase data flow gap: orphaned modules, unsatisfied imports, disconnected producer-consumer pairs, missing test coverage for produced artifacts |
| 2 | V2-A (Obligation scanner) | HIGH | Any undischarged scaffolding: mocked configs, placeholder UIs, stub APIs, temporary workarounds, hardcoded values never parameterized |
| 3 | V4-2 (Fingerprints) | HIGH | Any spec with code-level identifiers that the roadmap drops: API endpoints, class names, configuration keys, test names |
| 4 | V5-1 (Integration contracts) | HIGH | Any custom dispatch/registry/injection pattern: plugin systems, middleware chains, event handlers, DI containers |
| 5 | V1-A / V4-1 (ID cross-ref) | MEDIUM | Any formally-tagged requirement omission. Limited to specs that use FR-NNN tags. |
| 6 | V1-C (Spec structural audit) | MEDIUM | Extraction failures of any kind (dropped code blocks, missed MUST/SHALL clauses, lost test names) |
| 7 | V5-3 (Anti-pattern rules) | MEDIUM-HIGH (expandable) | Any known-bad roadmap pattern. Coverage grows with the rule library. |
| 8 | V4-3 (Negative-space prompt) | MEDIUM | Any semantic gap detectable by an LLM when properly framed. Non-deterministic but broad. |

---

## 7. Summary and Recommendations

### Duplicate solutions that must be merged

1. **V1-A and V4-1** are the same solution (requirement ID cross-reference). Merge into one module.
2. **V1-B and V3-1** are the same concept (producer-consumer graph). V3-1 is strictly better; discard V1-B.
3. **V1-D and V5-2** are the same approach (prompt constraint for integration). V5-2's enumeration requirement is stronger; merge.
4. **V2-A and V5-3 AP-001** overlap (scaffold detection). V2-A is more precise; V5-3's rule engine framework should house V2-A's logic.

### Genuine unique contributions per variant

- **V1**: Spec structural audit (Solution C) -- the only upstream guard
- **V2**: Scaffold-discharge vocabulary and obligation ledger -- the only deferred-commitment tracker
- **V3**: Existing infrastructure mapping and integration test synthesis -- the only proposal grounded in what already exists
- **V4**: Negative-space prompting and fingerprint extraction -- the only adversarial review reframing and the highest-efficacy single check
- **V5**: Integration contract taxonomy and anti-pattern rule engine -- the only mechanism-aware detection and extensible rule framework

### Highest-value implementation sequence (combining all 5 variants)

| Priority | Solution(s) | Source variant(s) | Type | Catches cli-portify? |
|----------|------------|-------------------|------|---------------------|
| P0 | Prompt constraint with integration enumeration | V1-D + V5-2 merged | Prevention | Likely (65%) |
| P1 | Fingerprint coverage check | V4-2 | Detection (deterministic) | Yes (95%) |
| P1 | Obligation scanner | V2-A | Detection (deterministic) | Yes (85%) |
| P2 | ID cross-reference | V1-A / V4-1 merged | Detection (deterministic) | Yes if IDs exist (80%) |
| P2 | Integration contract extractor | V5-1 | Detection (deterministic) | Yes (90%) |
| P3 | Spec structural audit | V1-C | Upstream guard (deterministic) | Yes (85%) |
| P3 | Negative-space prompting | V4-3 | Detection (LLM, adversarial) | Yes (80%) |
| P4 | Coherence graph | V3-1 | Detection (deterministic, broad) | Yes (75%) |
| P4 | Deliverable manifest + obligation ledger injection | V2-B + V3-2 merged | Prevention | Likely (70%) |

### Critical open risks

1. **A-009**: All regex-based solutions conflate keyword presence with task adequacy. A roadmap that mentions "dispatch" in passing would pass ID/fingerprint/contract checks without actually planning the dispatch implementation.
2. **A-010**: The 5 tendencies are correlated, not independent. Joint miss-rate calculations are optimistic.
3. **A-007**: The SemanticCheck model needs multi-file access. Three of five variants independently discovered this limitation, suggesting it should be addressed before implementing any cross-artifact checks.

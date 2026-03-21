# Refactoring Plan: Anti-Instincts Gate (Unified Merge Spec)

**Protocol**: sc:adversarial Step 4 (Refactoring Plan)
**Date**: 2026-03-17
**Co-bases**: V2 (Implicit Obligation Tracking, 7.60) + V5 (Pattern-Matching Trap Mitigation, 7.55)
**Cherry-picks**: V4-2 (Fingerprints), V1-C (Spec Structural Audit), V1-D+V5-2 (Prompt Constraint)

---

## 1. Changes from Non-Base Strengths

### Change 1: Fingerprint Extraction Module (V4-2)

- **Source variant and section**: V4, Solution 2 (Structural Fingerprint Extraction), `04-self-audit-blindness-mitigation.md` lines 232-336
- **Target location**: New file `src/superclaude/cli/roadmap/fingerprint.py`; semantic check wired into `ANTI_INSTINCT_GATE` in `gates.py`
- **Rationale citing debate evidence**:
  - Fingerprints scored highest single-check efficacy at 95% confidence (diff analysis C-030, rank 1)
  - V4-2 is mechanism-agnostic: catches any code-level identifier omission regardless of whether the spec uses FR-NNN tags (U-009)
  - The cli-portify spec contained `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` in backticks -- none appeared in the roadmap (debate transcript, V4-Advocate opening position point 1)
  - V5-Advocate conceded in Round 2 that fingerprints catch novel integration mechanisms not in V5's taxonomy (V5-Advocate concession)
  - V1-Advocate conceded fingerprints are stronger than ID cross-ref as a single check (V1-Advocate Round 2 concession)
  - Fills D1 gap: V2's D1 is 7; fingerprints raise the combined gate's catch rate
- **Integration approach**: INSERT -- new module, new `SemanticCheck` entry on `ANTI_INSTINCT_GATE`
- **Risk level**: LOW
  - ~150 LOC, well-defined regex patterns
  - Threshold tuning (default 0.7) is the main calibration question (A-008)
  - Requires multi-file access (spec + roadmap) -- use executor-level workaround per V5's approach (C-063)

**Implementation detail**: The `SemanticCheck` model signature `Callable[[str], bool]` takes only one content string. Fingerprint checks need both spec and roadmap. Resolution: use a placeholder `SemanticCheck` that always returns True on the gate; the real check runs in the executor between merge and spec-fidelity as a Python function call (not an LLM step). The executor reads both `extraction.md` (for spec fingerprints) and `roadmap.md`, runs `check_fingerprint_coverage()`, and halts the pipeline on failure. This matches V5's precedent (C-063, V5's Solution 1 uses an executor-level audit for the same reason).

### Change 2: Spec Structural Audit (V1-C)

- **Source variant and section**: V1, Solution C (Spec-to-Extraction Structural Audit), `01-completeness-bias-mitigation.md` lines 279-346
- **Target location**: New file `src/superclaude/cli/roadmap/spec_structural_audit.py`; wired into executor between `extract` and `generate` steps
- **Rationale citing debate evidence**:
  - V1-C is the only proposal that guards the extraction step itself (U-001, "HIGH efficacy")
  - V2-Advocate explicitly conceded this gap: "If the extraction step itself drops the requirement, V2-A has nothing to scan" (V2-Advocate Round 2 concession)
  - V5-Advocate agreed: "if the extraction LLM drops the dispatch requirement entirely, V5 has nothing to extract contracts from" (V5-Advocate opening position, steelmanning V1)
  - Neither co-base (V2, V5) validates the extraction output against the raw spec -- all downstream checks are vacuous if extraction drops a requirement (A-001)
  - Fills D2 gap: neither co-base guards the extraction step, so the upstream pipeline has zero coverage for extraction-quality failures
- **Integration approach**: INSERT -- new module, new executor logic between extract gate pass and generate step launch
- **Risk level**: LOW
  - ~80 LOC, pure regex counting
  - Does not modify the pipeline model or gate infrastructure
  - Runs as a Python function in the executor, not as a pipeline Step
  - If the structural count is suspiciously low relative to extraction's `total_requirements`, the executor logs a warning and optionally re-triggers extraction (phase 1: warning-only; phase 2: STRICT enforcement after shadow-mode validation)

**Implementation detail**: The audit runs after `EXTRACT_GATE` passes but before any `generate-*` step begins. It reads both `config.spec_file` and `output_dir / "extraction.md"`, counts structural indicators in the spec (code blocks, MUST/SHALL clauses, function signatures, test names, registry patterns), and compares against the extraction's `total_requirements` frontmatter value. If `total_requirements < structural_indicators * 0.5`, it emits a warning. The threshold is conservative (0.5) because structural indicators overcounts: code examples, alternatives, and non-requirement prose inflate the indicator count.

### Change 3: Prompt Constraint for Integration Enumeration (V1-D + V5-2 merged)

- **Source variant and section**: V1, Solution D (`01-completeness-bias-mitigation.md` lines 356-393); V5, Solution 2 (`05-pattern-matching-trap-mitigation.md` lines 346-393)
- **Target location**: `src/superclaude/cli/roadmap/prompts.py`, function `build_generate_prompt()` (lines 130-165)
- **Rationale citing debate evidence**:
  - Diff analysis X-002 identified the overlap: "Both propose prompt-level interventions for the generate step... V5-2's enumeration requirement subsumes V1-D's constraint"
  - V5-2 demands an explicit integration enumeration section in the roadmap output; V1-D adds the constraint that wiring tasks must be separate from component implementation tasks
  - Combined, these two produce a stronger prompt block than either alone
  - Ranked P0 in the diff analysis implementation sequence (highest priority due to trivial cost and immediate effect)
  - 65% detection confidence as prevention -- reduces bug frequency before post-merge detection runs
  - Zero implementation cost: ~50 lines of prompt text, no new files, no new gates
- **Integration approach**: APPEND -- add a new block to the return value of `build_generate_prompt()` in `prompts.py`
- **Risk level**: NEGLIGIBLE
  - Prompt-only change, no code logic
  - Does not affect pipeline model, gate infrastructure, or step ordering
  - Semi-deterministic: reduces probability but does not guarantee prevention (A-009)

**Implementation detail**: Use V5-2's `INTEGRATION_ENUMERATION_BLOCK` as the base text, incorporating V1-D's specific examples (dispatch tables, constructor injection, import chains, registration). The merged block should:
1. Require the LLM to enumerate ALL integration points before generating phases (V5-2)
2. Mandate separate wiring tasks distinct from component implementation tasks (V1-D)
3. Include the `## Integration Wiring Tasks` output section requirement (V5-2)
4. Name the dispatch-table-to-functions anti-pattern explicitly (V1-D)

Also add V5-2's 6th comparison dimension ("Integration Wiring") to `build_spec_fidelity_prompt()` to harden the downstream LLM validation check.

---

## 2. Co-Base Integration Details

### V2-A: Obligation Scanner (Co-Base Primary)

- **Source**: `02-implicit-obligation-tracking.md`, Solution A (lines 58-274)
- **Target**: New file `src/superclaude/cli/roadmap/obligation_scanner.py`
- **Integration approach**: DIRECT ADOPTION -- the proposal's code is nearly production-ready (C-045)
- **Gate integration**: New `SemanticCheck` on `ANTI_INSTINCT_GATE` with check function `_no_undischarged_obligations`
- **Key design points**:
  - Operates on single merged roadmap content (no multi-file access needed)
  - Pure Python regex, zero LLM calls, <100ms execution
  - Phase-splitting algorithm parses H2/H3 headings containing "Phase/Step/Stage/Milestone"
  - Component context extraction uses 60-char window with backtick and capitalized term matching
  - Scaffold-discharge vocabulary is extensible data (not hardcoded logic)

**Adaptation from proposal**: The proposal wires V2-A as a `SemanticCheck` on `MERGE_GATE`. In the merged spec, it becomes a check on the new `ANTI_INSTINCT_GATE` instead. The gate runs after merge, before spec-fidelity. This is functionally equivalent but groups all anti-instinct checks under one gate rather than scattering them across existing gates.

### V5-1: Integration Contract Extractor (Co-Base Primary)

- **Source**: `05-pattern-matching-trap-mitigation.md`, Solution 1 (lines 35-279)
- **Target**: New file `src/superclaude/cli/roadmap/integration_contracts.py`
- **Integration approach**: DIRECT ADOPTION with executor-level workaround for multi-file access
- **Key design points**:
  - Requires both spec text and roadmap text (multi-file access -- C-063)
  - `DISPATCH_PATTERNS` (4 patterns) match spec text for dispatch tables, registries, injection points, type annotations
  - `WIRING_TASK_PATTERNS` (3 patterns) match roadmap text for explicit wiring tasks
  - `IntegrationContract` dataclass with mechanism classification (dispatch_table, registry, dependency_injection, explicit_wiring, routing, integration_point)
  - `IntegrationAuditResult` with `uncovered_count` and `all_covered` property

**Adaptation from proposal**: The proposal creates a separate `INTEGRATION_AUDIT_GATE`. In the merged spec, the contract check becomes a `SemanticCheck` on `ANTI_INSTINCT_GATE` (placeholder that always returns True), with the real logic running in the executor as a Python function call. This matches the resolution for V4-2 fingerprints (both need multi-file access, both use the same workaround).

### V5-3 AP-001 Subsumption by V2-A

Per diff analysis X-004 and debate Round 3 resolution: V2-A's obligation scanner is the implementation of V5-3's AP-001 rule ("skeleton_without_wiring"). The rule engine framework from V5-3 is not adopted in Phase 1 because:
1. V2-A's scanner is more precise (tracks component context, per-phase scan vs. whole-document boolean)
2. The rule engine adds structural overhead without adding detection capability
3. AP-002 and AP-003 from V5-3 are either subsumed by V5-1's contract extractor (AP-003) or too imprecise for STRICT enforcement (AP-002)

If additional anti-pattern rules are needed in Phase 2, the rule engine can be introduced at that time with V2-A as a delegate for AP-001.

---

## 3. Gate Definition

### New Gate: `ANTI_INSTINCT_GATE`

**Location**: `src/superclaude/cli/roadmap/gates.py`

```python
ANTI_INSTINCT_GATE = GateCriteria(
    required_frontmatter_fields=[
        "undischarged_obligations",    # V2-A: integer count
        "uncovered_contracts",         # V5-1: integer count
        "fingerprint_coverage",        # V4-2: float 0.0-1.0
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="no_undischarged_obligations",
            check_fn=_no_undischarged_obligations,
            failure_message="Undischarged scaffolding obligations detected: early-phase mocks/stubs/skeletons have no corresponding replace/integrate/wire task in later phases",
        ),
        SemanticCheck(
            name="integration_contracts_covered",
            check_fn=_integration_contracts_covered,  # placeholder: True
            failure_message="Spec integration contracts missing from roadmap (enforced by executor)",
        ),
        SemanticCheck(
            name="fingerprint_coverage_sufficient",
            check_fn=_fingerprint_coverage_check,  # placeholder: True
            failure_message="Spec code-level identifiers missing from roadmap (enforced by executor)",
        ),
    ],
)
```

**Why a new gate instead of extending MERGE_GATE**: The `MERGE_GATE` validates the merge step's output quality (heading hierarchy, cross-refs, duplicates). The anti-instinct checks validate cross-artifact semantic fidelity -- a different concern. Keeping them separate follows the existing pattern where each gate corresponds to one validation concern. The `MERGE_GATE` runs on the merged roadmap; the `ANTI_INSTINCT_GATE` also runs on the merged roadmap but with additional executor-level context (spec file for contracts and fingerprints).

**Position in ALL_GATES**: Between `merge` and `test-strategy`:
```python
ALL_GATES = [
    ...
    ("merge", MERGE_GATE),
    ("anti-instinct", ANTI_INSTINCT_GATE),   # NEW
    ("test-strategy", TEST_STRATEGY_GATE),
    ("spec-fidelity", SPEC_FIDELITY_GATE),
    ...
]
```

### Anti-Instinct Audit Report

The executor produces `output_dir / "anti-instinct-audit.md"` with frontmatter:
```yaml
---
undischarged_obligations: 0
uncovered_contracts: 0
fingerprint_coverage: 0.85
total_obligations: 3
discharged_obligations: 3
total_contracts: 2
covered_contracts: 2
total_fingerprints: 15
matched_fingerprints: 13
structural_audit_passed: true
---
```

This file is the gate artifact. The `ANTI_INSTINCT_GATE` validates its frontmatter. The executor writes it after running all three deterministic checks.

---

## 4. Executor Wiring

### File: `src/superclaude/cli/roadmap/executor.py`

#### Change 1: Add structural audit after extract

**Location**: After `EXTRACT_GATE` passes in the pipeline, before `generate-*` steps

**Approach**: Add a post-extract hook in the executor (not a pipeline Step) that:
1. Reads `config.spec_file` and `extraction.md`
2. Runs `audit_spec_structure()` from `spec_structural_audit.py`
3. Compares structural indicator count against extraction's `total_requirements`
4. Logs warning if ratio < 0.5 (phase 1: warning-only)

This is NOT a new pipeline Step. It is executor-level logic that runs between steps. The existing executor already has post-step hooks (e.g., `_inject_pipeline_diagnostics` after extract). The structural audit follows the same pattern.

#### Change 2: Add anti-instinct audit step after merge

**Location**: Between the `merge` Step and the `test-strategy` Step in `_build_steps()`

**Approach**: Insert a synthetic step that:
1. Is NOT an LLM call (no `claude -p` subprocess)
2. Reads `config.spec_file`, `extraction.md`, and `roadmap.md`
3. Runs all three deterministic checks:
   - `scan_obligations(roadmap_content)` from `obligation_scanner.py`
   - `extract_integration_contracts(spec_content)` + `check_roadmap_coverage(contracts, roadmap_content)` from `integration_contracts.py`
   - `check_fingerprint_coverage(spec_content, roadmap_content)` from `fingerprint.py`
4. Writes `anti-instinct-audit.md` with frontmatter
5. The `ANTI_INSTINCT_GATE` validates the frontmatter

**Implementation options**:

*Option A: Custom step runner* -- Create a non-LLM step that the executor handles specially (check `step.id == "anti-instinct"` and run Python logic instead of a subprocess). This parallels how `_inject_pipeline_diagnostics` works for the extract step.

*Option B: Pre-gate executor hook* -- Run the checks after the merge step produces output but before the next step begins. Write the audit report, then add a `Step` with an empty prompt that simply validates the report against `ANTI_INSTINCT_GATE`.

**Recommended**: Option A. The audit is a deterministic Python function, not an LLM call. The executor should have a code path for non-LLM steps. The step should appear in the pipeline step list so it shows up in progress reporting and halt diagnostics.

#### Change 3: Import additions

Add to executor.py imports:
```python
from .gates import ANTI_INSTINCT_GATE
```

Add to `_build_steps()` between merge and test-strategy:
```python
Step(
    id="anti-instinct",
    prompt="",  # Non-LLM step; executor handles directly
    output_file=out / "anti-instinct-audit.md",
    gate=ANTI_INSTINCT_GATE,
    timeout_seconds=30,  # Pure Python, <1s expected
    inputs=[config.spec_file, extraction, merge_file],
    retry_limit=0,  # Deterministic; retry would produce same result
),
```

#### Change 4: Add `_get_all_step_ids` update

Add `"anti-instinct"` to the step ID list in `_get_all_step_ids()` between `"merge"` and `"test-strategy"`.

---

## 5. Prompt Changes

### File: `src/superclaude/cli/roadmap/prompts.py`

#### Change 1: Integration enumeration block in `build_generate_prompt()`

**Location**: Append before the `_OUTPUT_FORMAT_BLOCK` in the return value (after line 164)

**Content**: Merged V1-D + V5-2 block (~50 lines of prompt text):

```
## CRITICAL: Integration Point Enumeration

Before generating the roadmap phases, you MUST first enumerate ALL
integration points from the extraction document. An integration point
is any place where:
- A data structure maps identifiers to implementations (dispatch table,
  registry, router, lookup dict)
- A constructor/factory accepts injectable dependencies (Callable,
  Protocol, ABC, Factory parameters)
- An explicit wiring/binding step is described ("populate X with Y",
  "register Z in W")
- A lookup/dispatch mechanism is defined (match/case, dict dispatch,
  plugin registry)

For EACH integration point, your roadmap MUST contain an explicit task that:
1. Names the integration artifact (e.g., 'PROGRAMMATIC_RUNNERS dispatch table')
2. Lists what gets wired into it (e.g., 'all step runner implementations')
3. Specifies which phase owns this wiring task
4. Is NOT the same phase that implements the components being wired

WARNING: Do NOT assume that implementing components automatically wires them.
Building a class does not register it in a dispatch table. Building a function
does not add it to a lookup dict. Import-time side effects are NOT wiring.
The wiring is a separate, explicit task.

Include an '## Integration Wiring Tasks' section in your roadmap that
cross-references each integration point to its wiring task and phase.
```

#### Change 2: Integration wiring dimension in `build_spec_fidelity_prompt()`

**Location**: After dimension 5 ("NFRs") in the "Comparison Dimensions" section (after line 322)

**Content**:
```
6. **Integration Wiring**: For every dispatch table, registry, or
dependency injection point defined in the spec, verify the roadmap
contains an explicit task that creates and populates the mechanism --
not just tasks that implement the components being dispatched. Flag any
integration point where the spec defines custom wiring (e.g., a dispatch
dict, plugin registry, callback injection) but the roadmap only has
component implementation tasks without an explicit wiring phase.
```

---

## 6. Base Weakness Fixes

### Weakness 1: V2-A false positive risk on scaffold terms in non-scaffold contexts

**Identified by**: V1-Advocate Round 2 rebuttal; diff analysis A-004
**Better variant reference**: V2-Advocate Round 2 rebuttal (component context extraction mitigates)
**Fix approach**: The V2-A proposal already includes `_extract_component_context()` which uses a 60-char window to associate scaffold terms with nearby component names. This reduces false positives from "the test uses mocks" because test description scaffold terms will not share component context with phase milestone scaffold terms. Additionally:
- Scaffold terms inside code blocks (backtick-fenced) should be treated as potential false positives and flagged at MEDIUM severity rather than failing the gate
- Add an `# obligation-exempt` comment mechanism for legitimate scaffolding strategies
- Phase 1: STRICT enforcement on undischarged obligations, but with the component-context filter active

### Weakness 2: V5-1 limited pattern library (4 dispatch patterns, 2 wiring patterns)

**Identified by**: V5-Advocate Round 2 concession; diff analysis S-009
**Better variant reference**: V5's own taxonomy (appendix, 7 categories)
**Fix approach**: Expand `DISPATCH_PATTERNS` to cover all 7 categories from V5's taxonomy:
1. Dict dispatch (covered) -- `DISPATCH_TABLE`, `RUNNERS`, `HANDLERS`
2. Plugin registry (covered) -- `registry`, `register`
3. Callback injection (partially covered) -- `Callable`, `Protocol`
4. Strategy pattern (not covered) -- add patterns for `Context(strategy=...)`, `Strategy`, `ConcreteStrategy`
5. Middleware chain (not covered) -- add patterns for `middleware`, `app.use`, `pipeline.add`
6. Event binding (not covered) -- add patterns for `emitter.on`, `addEventListener`, `subscribe`
7. DI container (not covered) -- add patterns for `container.bind`, `container.register`, `Provider`

Expand `WIRING_TASK_PATTERNS` correspondingly. Each new pattern pair should have at least one test case.

### Weakness 3: V2-A does not catch pure omissions (requirement absent entirely)

**Identified by**: V2 scoring D1=7 (debate transcript, V2 scoring rationale)
**Better variant reference**: V4-2 fingerprints (catches pure omissions at 95% confidence)
**Fix approach**: This is addressed by the V4-2 cherry-pick. The fingerprint check catches the case where a requirement is entirely absent from the roadmap (no scaffold, no mention, no trace). The obligation scanner catches the case where the requirement is mentioned as deferred but never fulfilled. Together they cover both failure modes.

### Weakness 4: Neither co-base handles A-009 ("mentioned is not planned")

**Identified by**: V5-Advocate Round 2 rebuttal (debate transcript); diff analysis A-009
**Better variant reference**: V5-1's "mentioned vs. planned" distinction
**Fix approach**: V5-1's `check_roadmap_coverage()` already addresses this for integration contracts: it checks for explicit *wiring tasks* (verbs like "create", "build", "populate", "wire"), not just identifier presence. However, V4-2's fingerprint check is presence-based and susceptible to A-009. Mitigation: the fingerprint check's 0.7 threshold is for *coverage ratio*, not exact-match. A single mention in a design overview section would add 1 to the numerator but not inflate the ratio enough to mask wholesale omissions. For the V5-1 contracts, the wiring task patterns are verb-anchored (e.g., "create ... dispatch ... table"), so passive mentions ("the dispatch table is defined in the spec") do not match. No additional fix needed beyond the existing mechanism designs.

### Weakness 5: SemanticCheck single-file limitation (A-007)

**Identified by**: V1, V4, V5 all discovered independently; diff analysis C-063, A-007
**Better variant reference**: V5's executor-level workaround approach
**Fix approach**: Phase 1 uses the executor-level workaround (run multi-file checks in the executor, write results to a report file, validate report frontmatter via standard single-file SemanticCheck). This is the approach V5 proposed and is the lowest-risk path. Phase 2 (deferred): consider extending the `SemanticCheck` model to support `context_files: list[str] | None` (V4's Option B), which would allow multi-file checks to be expressed declaratively in `GateCriteria` rather than imperatively in executor code. This is an architectural improvement that benefits future gates, not just anti-instinct checks.

---

## 7. Changes NOT Being Made (Rejected Alternatives)

### Rejected: V1-A / V4-1 (Requirement ID Cross-Reference)

**Source**: V1 Solution A, V4 Solution 1
**Rationale for rejection**:
- Duplicated by V4-2 fingerprints for code-heavy specs (diff analysis X-001)
- Depends on extraction producing FR-NNN IDs -- vacuous if extraction uses different ID format (A-001)
- V4-2 fingerprints subsume ID cross-ref for the merge: fingerprints catch ANY code-level identifier, including but not limited to formal FR-NNN tags (U-009)
- Adding ID cross-ref alongside fingerprints adds ~100 LOC for marginal incremental detection value
- If formal ID tracking is wanted later, it can be added as a separate module without conflicting with the anti-instinct gate

### Rejected: V4-3 (Negative-Space Prompting)

**Source**: V4 Solution 3
**Rationale for deferral to Phase 2**:
- Adds one LLM call per pipeline run (~60s, ~$0.10) (C-054)
- Three new deterministic checks (V2-A, V5-1, V4-2) provide sufficient detection depth without LLM cost
- The existing spec-fidelity check already serves as an LLM validation layer; adding a second LLM layer compounds cost without guaranteed independence (A-010: LLM tendency correlation)
- V4-Advocate's dissent is recorded (convergence 0.75, below threshold) but the counter-argument holds: "defer until deterministic checks are validated"
- Phase 2 adoption plan: merge V4-3's adversarial framing with V1-E's structured output table (debate Round 3 resolution) into a single prompt that replaces the existing spec-fidelity prompt

### Rejected: V3-1 (Coherence Graph)

**Source**: V3 Solution 1
**Rationale for deferral to Phase 2**:
- Highest implementation risk: extraction heuristics for producer-consumer relationships from natural language are underspecified (S-003, V1 Round 2 rebuttal)
- D1=6 (lowest efficacy of any primary solution) because heuristic extraction may not parse abstract roadmap language (debate transcript, V3 scoring)
- D3=4 (highest implementation complexity alongside V4) -- ~300 LOC across 2 new files
- V3-Advocate conceded: "If implementation speed matters more than coverage breadth, V4-2 is the better first deploy" (V3-Advocate Round 2 concession)
- V3's mapping to existing infrastructure (U-005: dataflow_graph.py, deliverables.py, etc.) is valuable context for Phase 2 implementation
- Phase 2 adoption plan: build on existing dataflow infrastructure, using V3-1's "disconnected pair" concept as the core detection mechanism

### Rejected: V2-B + V3-2 (Obligation Ledger + Deliverable Manifest Injection)

**Source**: V2 Solution B, V3 Solution 2
**Rationale for deferral to Phase 2**:
- Both modify `build_generate_prompt()` to inject per-phase state, requiring state management between pipeline steps (C-046, C-049)
- Diff analysis X-006: injecting both would bloat the prompt; merge into single "prior phase context" block
- Prevention-layer complements detection-layer but adds complexity to the currently-stateless pipeline model
- Phase 2 adoption plan: merge V2-B (obligation ledger) and V3-2 (deliverable manifest) into a single "prior phase context" injection after deterministic detection gates prove effective

### Rejected: V4-5 (Requirement Registry)

**Source**: V4 Solution 5
**Rationale for rejection (not just deferral)**:
- "Architecturally incompatible with the current stateless pipeline model" (diff analysis X-008)
- All other 4 variants implicitly reject this approach by not proposing it
- Requires every pipeline step to participate in state updates -- a major architectural change
- The deterministic checks (V2-A, V5-1, V4-2) achieve comparable detection without state management

### Rejected: V1-B (Orphaned Component Detection)

**Source**: V1 Solution B
**Rationale for rejection**:
- Subsumed by V3-1 (diff analysis X-003: "V3-1 is strictly more capable" with "disconnected pair" detection)
- V3-1 itself is deferred to Phase 2
- V1-B adds nothing that V3-1 does not cover; implementing V1-B now would be throwaway work

### Rejected: V1-E (Integration Completeness LLM Pass with Positive Framing)

**Source**: V1 Solution E
**Rationale for rejection**:
- Debate Round 3 resolved that negative framing (V4-3) is preferred over positive framing (V1-E) for the LLM review step (X-005)
- The existing spec-fidelity check already uses positive framing and failed (forensic evidence)
- V1-E's structured table output format is adopted for V4-3's Phase 2 implementation, but the positive framing is not
- The structured output schema (per-deliverable table with Producer/Consumer/Wiring Task/Status columns) is preserved as the output format for Phase 2's negative-space prompt

### Rejected: V5-3 (Anti-Pattern Rule Engine as Separate Module)

**Source**: V5 Solution 3
**Rationale for consolidation into V2-A**:
- V2-A's scanner is more precise than V5-3's AP-001 rule (diff analysis X-004: "V2-A is strictly better for this specific check")
- AP-001 ("skeleton_without_wiring") is functionally identical to V2-A's scaffold-discharge detection
- AP-002 ("implicit_integration_assumption") is too imprecise for STRICT enforcement -- "phases labeled 'integration' that do not name specific artifacts" would produce false positives
- AP-003 ("dict_dispatch_without_population_phase") is subsumed by V5-1's contract extractor which does the same check more precisely
- The rule engine framework adds organizational overhead without Phase 1 value

---

## 8. File Manifest

### New Files (4)

| File | Source | LOC | Purpose |
|------|--------|-----|---------|
| `src/superclaude/cli/roadmap/obligation_scanner.py` | V2-A | ~200 | Scaffold-discharge obligation detection |
| `src/superclaude/cli/roadmap/integration_contracts.py` | V5-1 | ~250 | Integration contract extraction and roadmap coverage verification |
| `src/superclaude/cli/roadmap/fingerprint.py` | V4-2 | ~150 | Code-level identifier extraction and coverage check |
| `src/superclaude/cli/roadmap/spec_structural_audit.py` | V1-C | ~80 | Upstream extraction quality guard |

### Modified Files (3)

| File | Changes | Source |
|------|---------|--------|
| `src/superclaude/cli/roadmap/gates.py` | Add `ANTI_INSTINCT_GATE` definition with 3 semantic checks; add 3 check functions; update `ALL_GATES` list | V2-A + V5-1 + V4-2 |
| `src/superclaude/cli/roadmap/executor.py` | Add anti-instinct step to `_build_steps()`; add structural audit hook after extract; add `_run_anti_instinct_audit()` function; add import for `ANTI_INSTINCT_GATE`; update `_get_all_step_ids()` | All |
| `src/superclaude/cli/roadmap/prompts.py` | Add integration enumeration block to `build_generate_prompt()`; add 6th comparison dimension to `build_spec_fidelity_prompt()` | V1-D + V5-2 |

### Test Files (4, to be created)

| File | Covers |
|------|--------|
| `tests/roadmap/test_obligation_scanner.py` | V2-A: scaffold/discharge detection, phase splitting, component context |
| `tests/roadmap/test_integration_contracts.py` | V5-1: contract extraction, coverage checking, mechanism classification |
| `tests/roadmap/test_fingerprint.py` | V4-2: fingerprint extraction, coverage ratio, threshold behavior |
| `tests/roadmap/test_spec_structural_audit.py` | V1-C: structural indicator counting, ratio comparison |

### Total Impact

- **New files**: 4 source + 4 test = 8 files
- **Modified files**: 3 files
- **Total new LOC**: ~680 (source) + ~400 (tests, estimated) = ~1,080
- **LLM calls added**: 0 (all checks are pure Python)
- **Pipeline latency added**: <1s (combined deterministic execution)
- **Existing model changes**: 0 (no changes to `SemanticCheck`, `GateCriteria`, `Step`, or `PipelineConfig`)

---

## 9. Execution Order

### Implementation Sequence

1. **obligation_scanner.py** -- Adopt V2-A code nearly verbatim. Highest implementation readiness (C-045). Write tests.
2. **integration_contracts.py** -- Adopt V5-1 code with expanded pattern library (Section 6, Weakness 2). Write tests.
3. **fingerprint.py** -- Adopt V4-2 code. Write tests.
4. **spec_structural_audit.py** -- Adopt V1-C code. Write tests.
5. **gates.py** -- Add `ANTI_INSTINCT_GATE` with all 3 semantic checks + helper functions.
6. **executor.py** -- Wire anti-instinct step into `_build_steps()`. Add structural audit hook. Add `_run_anti_instinct_audit()`.
7. **prompts.py** -- Add integration enumeration block + 6th fidelity dimension.
8. **Integration test** -- End-to-end test using cli-portify spec/roadmap as regression case.

### Dependencies

```
obligation_scanner.py ─┐
integration_contracts.py ─┼─> gates.py ─> executor.py
fingerprint.py ─┘                           │
spec_structural_audit.py ──────────────────>─┘
prompts.py (independent, can be done in parallel)
```

---

## 10. Phase 2 Backlog (Deferred Items)

Items explicitly deferred from Phase 1 with adoption conditions:

| Item | Source | Adoption Condition | Depends On |
|------|--------|--------------------|-----------|
| Negative-space prompting | V4-3 + V1-E output schema | After Phase 1 deterministic checks validated in shadow mode (3+ pipeline runs with zero false positives) | Phase 1 complete |
| Coherence graph | V3-1 | After existing dataflow infrastructure assessed for reuse; requires extraction heuristic design doc | Phase 1 complete |
| Obligation ledger + manifest injection | V2-B + V3-2 merged | After pipeline state management design approved; requires prompt injection testing | Phase 1 complete |
| SemanticCheck model extension for multi-file access | V4 Option B | After 2+ multi-file checks are in production and the executor workaround proves limiting | Phase 1 complete |
| Anti-pattern rule engine framework | V5-3 | After 3+ anti-pattern rules are identified beyond AP-001 (which is already covered by V2-A) | Phase 1 complete |

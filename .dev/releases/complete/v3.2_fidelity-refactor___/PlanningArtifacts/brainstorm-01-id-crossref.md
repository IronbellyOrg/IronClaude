# Brainstorm 01: Requirement ID Cross-Referencing for Fidelity Gates

**Date**: 2026-03-17
**Context**: cli-portify executor no-op forensic report findings
**Problem**: SPEC_FIDELITY_GATE and TASKLIST_FIDELITY_GATE rely entirely on LLM semantic comparison. No programmatic cross-referencing of requirement IDs exists. The LLM missed that the roadmap dropped the spec's three-way dispatch design, and the corruption propagated through the entire pipeline.
**Scope**: 10 solutions total -- 5 for Spec-to-Roadmap, 5 for Roadmap-to-Tasklist

---

## Section A: Spec-to-Roadmap Fidelity (5 Solutions)

These solutions target the validation phase where the roadmap is checked against the specification. The forensic report showed that FR-NNN, NFR-NNN, and SC-NNN identifiers in the spec had no programmatic verification of their presence in the roadmap.

---

### A1. Pre-Gate ID Extraction and Set-Difference Check

**Summary**: Parse all requirement IDs from the spec extraction, parse all referenced IDs from the roadmap, compute the set difference, and fail the gate if any spec IDs are missing from the roadmap.

**Mechanism**: A pure function `extract_requirement_ids(content: str) -> set[str]` uses regex patterns (`FR-\d{3}`, `NFR-\d{3}`, `SC-\d{3}`) to parse IDs from both the spec extraction output and the roadmap output. Before invoking the LLM-based SPEC_FIDELITY_GATE, a new programmatic pre-check computes `spec_ids - roadmap_ids`. If the difference is non-empty, the gate fails immediately with a list of missing IDs, bypassing the LLM entirely. This runs as an additional `SemanticCheck` on the existing `SPEC_FIDELITY_GATE` `GateCriteria`.

**What it would catch**: Any spec requirement ID that is entirely absent from the roadmap text. In the cli-portify case, the spec's FR-NNN IDs for three-way dispatch, PROGRAMMATIC_RUNNERS, and test_programmatic_step_routing would have been flagged as missing from the roadmap, blocking generation before the LLM even evaluated severity.

**Integration point**: `src/superclaude/cli/roadmap/gates.py` -- add a new `SemanticCheck` entry to `SPEC_FIDELITY_GATE.semantic_checks` list. The check function would need access to both the spec extraction content and the roadmap content. Since `SemanticCheck.check_fn` currently accepts only `content: str` (the gate output), this would require either (a) embedding the spec ID manifest in the fidelity report frontmatter so the check can parse it, or (b) extending `SemanticCheck` to accept a second file path.

**Limitations**: Only catches IDs that follow the exact `FR-NNN`/`NFR-NNN`/`SC-NNN` naming convention. Specs that use prose descriptions without formal IDs would not benefit. Does not verify semantic coverage -- a roadmap could mention `FR-007` in a throwaway sentence without actually planning for it. Also requires that the spec extraction step reliably preserves all IDs from the source spec (if extraction itself drops IDs, the cross-check has a false baseline).

---

### A2. Bidirectional ID Manifest with Coverage Matrix

**Summary**: Generate a structured ID manifest during spec extraction, embed it as a YAML block in the extraction output, then require the roadmap generator to produce a corresponding coverage matrix mapping each spec ID to a roadmap phase/action.

**Mechanism**: The spec extraction prompt (`build_extract_prompt` in `roadmap/prompts.py`) is extended to require a `## Requirement ID Manifest` section at the end of its output, listing every FR-NNN, NFR-NNN, and SC-NNN found in the spec. The roadmap generation prompt is extended to require a `## Coverage Matrix` section that maps each manifest ID to the roadmap phase and key action that addresses it. The SPEC_FIDELITY_GATE then programmatically parses both sections and verifies: (1) every manifest ID appears in the coverage matrix, (2) every coverage matrix entry references a valid roadmap phase. The LLM fidelity check still runs afterward for semantic depth.

**What it would catch**: Dropped requirements (manifest ID missing from matrix), fabricated coverage (matrix references a phase that does not exist), and incomplete coverage (ID present but mapped to "[Not Addressed]" or similar). The cli-portify three-way dispatch IDs would have appeared in the manifest but had no matrix entry, triggering a hard failure.

**Integration point**: `src/superclaude/cli/roadmap/prompts.py` -- modify `build_extract_prompt()` to require the manifest section, and modify `build_generate_prompt()` (or equivalent roadmap generation prompt) to require the coverage matrix. `src/superclaude/cli/roadmap/gates.py` -- add a new `SemanticCheck` that parses and cross-references both sections.

**Limitations**: Adds token cost to both extraction and generation steps (manifest + matrix). LLM may still fabricate matrix entries that look correct but map to insufficiently detailed roadmap actions. Requires discipline in spec authoring -- specs without formal IDs produce empty manifests. The coverage matrix is itself LLM-generated, so it introduces a new surface for hallucination (claiming coverage that does not exist in the roadmap body).

---

### A3. Two-Pass Validation: Programmatic Sweep Then LLM Deep Dive

**Summary**: Split SPEC_FIDELITY_GATE into two sequential passes -- a fast programmatic sweep that catches all ID-level gaps, followed by the existing LLM semantic analysis that catches nuanced deviations.

**Mechanism**: Pass 1 (programmatic, ~0 tokens): Regex-extract all requirement IDs from spec. Regex-extract all requirement ID references from roadmap. Compute missing, added, and present sets. If any spec IDs are missing, emit a structured pre-report with each missing ID flagged as HIGH severity. Pass 2 (LLM, existing cost): Run the existing `build_spec_fidelity_prompt()` comparison, but inject the Pass 1 findings as context: "The following IDs were programmatically determined to be missing: [list]. Verify each and include in your severity assessment." The final gate output merges both passes. The programmatic pass has veto power: if it finds missing IDs, the gate fails even if the LLM somehow classifies them as LOW.

**What it would catch**: All ID-level omissions (Pass 1) plus semantic deviations like misinterpretation, insufficient detail, or contradictions (Pass 2). The programmatic pass provides a deterministic floor that the LLM cannot override. In the cli-portify case, Pass 1 would have caught the missing dispatch IDs before Pass 2 even ran.

**Integration point**: `src/superclaude/cli/pipeline/gates.py` -- extend `gate_passed()` to support a `pre_checks` list on `GateCriteria` that run before the main semantic checks. Alternatively, implement as a new step in the roadmap pipeline's `_build_steps()` that runs between roadmap generation and the existing spec-fidelity step. `src/superclaude/cli/roadmap/gates.py` -- define the Pass 1 function and wire it as a pre-check.

**Limitations**: Pass 1 is purely syntactic -- it cannot detect when a requirement is addressed under a different name or decomposed across multiple roadmap items without referencing the original ID. Pass 2 context injection increases prompt length, which may reduce LLM attention on non-injected deviations. The two-pass architecture adds complexity to the gate enforcement flow.

---

### A4. Spec ID Registry with Lifecycle Tracking

**Summary**: Maintain a persistent JSON registry of all spec requirement IDs with lifecycle states (DEFINED, ROADMAPPED, TASKED, IMPLEMENTED, VERIFIED), updated by each pipeline phase, and gate-checked at each transition.

**Mechanism**: When the spec extraction step runs, it writes a `spec-id-registry.json` file containing every extracted ID with state `DEFINED`. When the roadmap generation step runs, it updates each ID's state to `ROADMAPPED` and records the roadmap phase reference, or leaves it as `DEFINED` if not covered. The SPEC_FIDELITY_GATE reads this registry and fails if any ID remains in `DEFINED` state (meaning the roadmap did not claim coverage). Subsequent pipeline phases (tasklist, sprint) continue to update states. The registry provides a single source of truth for requirement coverage across the entire pipeline.

**What it would catch**: Any requirement that stalls at any lifecycle stage. In the cli-portify case, the three-way dispatch IDs would have remained at `DEFINED` after roadmap generation, triggering the gate. Additionally, the registry enables downstream detection: if a requirement reaches `TASKED` but never `IMPLEMENTED`, a future code-fidelity gate could catch it.

**Integration point**: New file `src/superclaude/cli/pipeline/id_registry.py` containing `IdRegistry` class with `load()`, `save()`, `update_state()`, `check_transition()` methods. Each pipeline step's prompt builder would need to be told about the registry so the LLM can update it. Gate checks would read the registry file. `src/superclaude/cli/roadmap/gates.py` -- add a `SemanticCheck` that loads the registry and verifies all IDs have advanced past `DEFINED`.

**Limitations**: Relies on the LLM accurately updating registry states during generation steps (the LLM must be prompted to produce registry updates, which is itself fallible). Adds a stateful artifact to what is currently a stateless document pipeline. Registry file could become stale or corrupted if a pipeline step fails mid-execution. Requires all specs to use formal ID conventions for the registry to be populated.

---

### A5. Structural Signature Fingerprinting

**Summary**: Extract not just IDs but structural signatures (function names, class names, data structure names, dispatch patterns) from the spec, fingerprint them, and verify each fingerprint appears in the roadmap.

**Mechanism**: Beyond `FR-NNN` IDs, the spec often contains concrete design elements: function signatures like `_run_programmatic_step()`, data structures like `PROGRAMMATIC_RUNNERS`, test names like `test_programmatic_step_routing`. A fingerprint extractor parses the spec for: (1) formal IDs (FR-NNN, etc.), (2) code-fenced identifiers (function/class/variable names in backticks or code blocks), (3) explicitly named design patterns (e.g., "three-way dispatch"). Each is hashed into a fingerprint set. The roadmap is scanned for the same fingerprints. Missing fingerprints are reported as potential coverage gaps. The SPEC_FIDELITY_GATE treats missing code-level fingerprints as HIGH severity (since these represent concrete implementation commitments, not abstract requirements).

**What it would catch**: Dropped implementation details that may not have formal IDs. In the cli-portify case, even if the spec lacked `FR-NNN` tags for the dispatch design, the fingerprinter would have caught that `_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`, `PROGRAMMATIC_RUNNERS`, and `test_programmatic_step_routing` all appeared in the spec but not in the roadmap.

**Integration point**: New module `src/superclaude/cli/pipeline/fingerprint.py` with `extract_fingerprints(content: str) -> set[str]` function. `src/superclaude/cli/roadmap/gates.py` -- add a `SemanticCheck` that loads both spec and roadmap content, extracts fingerprints, and fails on missing code-level fingerprints. The fingerprint extractor would need to distinguish between casual mentions and commitment-level references (e.g., a spec saying "unlike `_run_sync()`" should not create a requirement for `_run_sync`).

**Limitations**: High false-positive risk. Specs mention many identifiers for context, comparison, or rejection ("we considered X but chose Y"). Distinguishing commitment-level references from contextual mentions requires heuristics that may be fragile. Code-fenced content varies widely in format. The fingerprinter cannot assess semantic equivalence -- if the roadmap renames a function, the fingerprint will not match even if the concept is preserved. Requires tuning of the extraction heuristics per-project or per-spec-format.

---

## Section B: Roadmap-to-Tasklist Fidelity (5 Solutions)

These solutions target the validation phase where the tasklist is checked against the roadmap. The forensic report showed that the TASKLIST_FIDELITY_GATE correctly validated the tasklist against its parent (the roadmap), but since the roadmap was already corrupted, the tasklist faithfully reproduced the corruption. These solutions add programmatic D-NNNN and R-NNN cross-referencing.

---

### B1. Deliverable ID Completeness Check

**Summary**: Parse all D-NNNN deliverable IDs and R-NNN roadmap item IDs from the roadmap, parse all referenced IDs from the tasklist files, and fail if any roadmap ID has no corresponding tasklist entry.

**Mechanism**: A pure function `extract_deliverable_ids(content: str) -> set[str]` uses regex (`D-\d{4}`, `R-\d{3}`) to parse IDs from the roadmap output. A second function scans all tasklist files in the tasklist directory and extracts all D-NNNN and R-NNN references. The TASKLIST_FIDELITY_GATE runs a programmatic pre-check: `roadmap_ids - tasklist_ids`. If non-empty, the gate fails with a list of unaddressed deliverables/items. This is added as a `SemanticCheck` on the existing `TASKLIST_FIDELITY_GATE`.

**What it would catch**: Any roadmap deliverable or item that has no tasklist task. In the cli-portify case, if the roadmap HAD contained dispatch deliverables (which it did not -- the corruption was upstream), this gate would have caught them being dropped during tasklist generation. More importantly, this gate establishes a pattern that makes Section A fixes effective: once Section A ensures the roadmap contains all spec requirements, Section B ensures the tasklist contains all roadmap deliverables, completing the deterministic chain.

**Integration point**: `src/superclaude/cli/tasklist/gates.py` -- add a new `SemanticCheck` to `TASKLIST_FIDELITY_GATE.semantic_checks`. Since `SemanticCheck.check_fn` accepts only the gate output content (the fidelity report), the check would need to either (a) require the fidelity report to embed a deliverable coverage summary in its frontmatter, or (b) extend the check interface to accept additional file paths (roadmap + tasklist directory).

**Limitations**: Only catches ID-level gaps. A tasklist could mention `D-0042` in a single sentence without creating a meaningful task for it. Does not verify that the task's scope, acceptance criteria, or effort actually address the deliverable. Depends on consistent ID formatting in both documents. If the roadmap generator omits IDs from deliverable descriptions, the extractor will miss them.

---

### B2. Reverse Traceability Validation (Tasklist-to-Roadmap Backlink Audit)

**Summary**: For every task in the tasklist, verify that its claimed parent R-NNN and D-NNNN IDs actually exist in the roadmap. Catch fabricated traceability where the LLM invents IDs.

**Mechanism**: Parse the tasklist files to extract every R-NNN and D-NNNN reference along with its task context (which task file, which task ID). Parse the roadmap to build a canonical set of valid IDs. For each tasklist reference, check that the ID exists in the canonical set. Flag two failure modes: (1) **orphan references** -- tasklist cites an ID that does not exist in the roadmap (fabricated traceability), (2) **ID collisions** -- multiple tasks claim the same deliverable without explicit sharing notation. Report orphan references as HIGH severity.

**What it would catch**: LLM hallucination of traceability IDs. The tasklist prompt already asks for traceability, but the LLM sometimes generates plausible-looking IDs (e.g., `D-0099`) that do not correspond to any roadmap deliverable. This is the inverse of B1: B1 catches roadmap items missing from the tasklist, B2 catches tasklist items referencing nonexistent roadmap entries. Together they enforce bijective traceability.

**Integration point**: `src/superclaude/cli/tasklist/gates.py` -- add as a second `SemanticCheck`. The check function needs access to both the roadmap content and the tasklist directory. Could be implemented by requiring the fidelity report to include a `## Traceability Audit` section with structured data, or by extending the gate interface. `src/superclaude/cli/tasklist/prompts.py` -- modify `build_tasklist_fidelity_prompt()` to instruct the LLM to include a traceability table that the programmatic check can parse.

**Limitations**: Only validates ID existence, not semantic alignment. A task could reference a valid R-NNN but describe completely different work. Does not catch the case where the roadmap itself has corrupted IDs (garbage-in, garbage-out). Requires that the LLM-generated tasklist consistently uses the ID format -- if a task describes work related to `D-0042` without using the formal ID, the backlink audit will not associate them.

---

### B3. Acceptance Criteria Decomposition Verifier

**Summary**: For each roadmap deliverable, extract its success criteria, then verify that the corresponding tasklist tasks collectively cover all criteria through programmatic keyword and ID matching.

**Mechanism**: Parse the roadmap to build a map: `{D-NNNN: [list of success criteria text]}`. Parse tasklist files to build a map: `{D-NNNN: [list of acceptance criteria text from tasks referencing this deliverable]}`. For each deliverable, run a programmatic similarity check between roadmap success criteria and tasklist acceptance criteria. The check uses: (1) exact ID matching (if criteria reference specific identifiers like function names), (2) keyword overlap scoring (TF-IDF or simpler Jaccard similarity on key terms), (3) count comparison (roadmap has 5 criteria but tasklist only has 2 -- flag as potential gap). Deliverables where the tasklist acceptance criteria cover less than a configurable threshold (e.g., 70% keyword overlap) are flagged for LLM review.

**What it would catch**: Cases where a tasklist task references a deliverable but waters down or omits specific acceptance criteria. In the cli-portify case, even the weakened "sequential execution with mocked steps" roadmap had some criteria that could have been checked. More broadly, this catches the pattern where a tasklist says "implement executor" without preserving the roadmap's specific success criteria (e.g., "all 12 steps execute real work").

**Integration point**: New module `src/superclaude/cli/tasklist/criteria_verifier.py` with `verify_criteria_coverage(roadmap_content: str, tasklist_dir: Path) -> list[CoverageGap]`. Called from `TASKLIST_FIDELITY_GATE` as a `SemanticCheck`, or as a separate pipeline step that runs before the LLM-based fidelity check.

**Limitations**: Keyword overlap is a rough proxy for semantic coverage. Paraphrased criteria may have low keyword overlap despite being equivalent. The similarity threshold requires tuning -- too strict produces false positives, too loose misses real gaps. Structured criteria (numbered lists with IDs) work much better than prose criteria. Does not work well for criteria that are qualitative ("clean architecture") rather than specific ("function X calls function Y").

---

### B4. Task Dependency Graph Consistency Check

**Summary**: Build a dependency graph from the roadmap's phase/item ordering and a separate graph from the tasklist's dependency declarations, then verify structural consistency between them.

**Mechanism**: Parse the roadmap to extract the phase ordering and inter-item dependencies (R-NNN depends on R-MMM, Phase 3 requires Phase 2 completion). Parse tasklist files to extract task dependency declarations (T03.04 depends on T03.03, etc.) and map them back to their parent R-NNN/D-NNNN IDs. Build two directed acyclic graphs: `roadmap_dag` and `tasklist_dag`. Verify: (1) **topological consistency** -- if R-002 depends on R-001 in the roadmap, then all tasks under R-002 must depend (directly or transitively) on all tasks under R-001 in the tasklist, (2) **no orphan subgraphs** -- every connected component in the tasklist DAG must trace back to a roadmap phase, (3) **critical path preservation** -- the roadmap's critical path items must appear on the tasklist's critical path.

**What it would catch**: Dependency inversions where the tasklist reorders work in ways that violate the roadmap's sequencing. Also catches orphan tasks that have no roadmap parent (potentially fabricated work) and missing dependency edges that could lead to tasks executing before their prerequisites are complete. In pipelines where dispatch wiring depends on step implementation (as in cli-portify), the dependency graph would flag that "wire executor to steps" has no task but is a prerequisite for E2E testing.

**Integration point**: New module `src/superclaude/cli/tasklist/dep_graph.py` with `build_roadmap_dag()`, `build_tasklist_dag()`, and `verify_consistency()` functions. Integrated as a `SemanticCheck` on `TASKLIST_FIDELITY_GATE` or as a standalone pipeline step. Requires extending the `GateCriteria` model to support multi-file checks (needs both roadmap and tasklist directory).

**Limitations**: Dependency information in roadmaps and tasklists is often implicit or incomplete. The parser may miss dependencies expressed in prose ("after completing the executor, implement steps"). Graph comparison is computationally simple but semantically shallow -- structural consistency does not guarantee that the tasks actually do the right work. Requires that both documents use consistent ID schemes for the mapping to work.

---

### B5. Deliverable-to-Task Cardinality Enforcement

**Summary**: For each roadmap deliverable, enforce minimum task cardinality rules based on deliverable complexity signals, catching cases where complex deliverables are collapsed into trivially few tasks.

**Mechanism**: Parse the roadmap to extract deliverables with their complexity signals: (1) number of success criteria, (2) number of sub-items or bullet points, (3) presence of keywords indicating complexity ("integration", "wiring", "cross-module", "dispatch"), (4) explicit effort estimates if present. Assign each deliverable an expected minimum task count based on a heuristic: e.g., `min_tasks = max(1, len(success_criteria), complexity_keyword_count)`. Parse tasklist files to count how many tasks reference each D-NNNN. Flag deliverables where `actual_tasks < min_tasks` as potential under-decomposition. A deliverable with 5 success criteria addressed by a single task is suspicious.

**What it would catch**: The pattern where a complex, multi-faceted roadmap deliverable is collapsed into a single shallow task. In the cli-portify case, if the roadmap had contained the executor dispatch deliverable with its three-way dispatch, PROGRAMMATIC_RUNNERS, and integration test criteria, and the tasklist reduced this to a single "implement executor" task, the cardinality check would flag the mismatch. More generally, this catches insufficient decomposition that leads to tasks being marked "complete" without addressing all aspects of a deliverable.

**Integration point**: `src/superclaude/cli/tasklist/gates.py` -- add as a `SemanticCheck` on `TASKLIST_FIDELITY_GATE`. The heuristic could be defined in a configuration file to allow per-project tuning. Alternatively, implement as a separate `DECOMPOSITION_GATE` that runs after tasklist generation but before sprint execution.

**Limitations**: Cardinality is a weak proxy for coverage. A deliverable could have 10 tasks that all address the same narrow aspect while ignoring others. The complexity heuristic is necessarily rough -- keyword-based complexity detection will have both false positives (mentioning "integration" in a simple context) and false negatives (complex work described with simple language). The minimum task count is arbitrary and may need per-domain calibration. Does not verify task content, only task count per deliverable.

---

## Cross-Cutting Observations

1. **Section A solutions are higher-leverage than Section B**: The cli-portify failure originated at Spec-to-Roadmap (Link 1). Section B solutions would not have caught this specific bug because the roadmap was already corrupted before the tasklist was generated. However, Section B solutions prevent future failures where the roadmap is correct but the tasklist degrades it.

2. **Programmatic checks provide a deterministic floor**: All 10 solutions share the principle that LLM-only validation has an irreducible failure rate. Programmatic cross-referencing creates a minimum coverage guarantee that the LLM cannot override or miss.

3. **The SemanticCheck interface needs extension**: The current `check_fn(content: str) -> bool` signature only receives the gate output (the fidelity report). Cross-referencing requires access to both the upstream document (spec or roadmap) and the downstream document (roadmap or tasklist). Solutions A1-A5 and B1-B5 all require either (a) embedding cross-reference data in the fidelity report frontmatter, or (b) extending `SemanticCheck` to accept additional context. Option (b) is cleaner but requires changes to `src/superclaude/cli/pipeline/models.py` and `src/superclaude/cli/pipeline/gates.py`.

4. **Formal ID conventions are a prerequisite**: All 10 solutions depend on specs and roadmaps using consistent, parseable ID formats. Projects that use prose-only requirements without formal identifiers would not benefit. This suggests a complementary investment in spec extraction prompts that enforce ID assignment.

5. **Recommended implementation order**: A1 (simplest, highest immediate value) -> B1 (symmetric counterpart) -> A3 (adds LLM context injection) -> B2 (catches fabrication) -> A2 (adds coverage matrix). The remaining solutions (A4, A5, B3, B4, B5) are higher-effort and should be evaluated based on observed failure modes after the first wave is deployed.

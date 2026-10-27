# Brainstorm 02: Wiring Verification Solutions

**Date**: 2026-03-17
**Context**: cli-portify executor no-op forensic report findings
**Scope**: 10 solutions across two validation phases
**Problem class**: "Defined but not wired" -- components specified in architecture that lack integration tasks

---

## Section A: Spec-to-Roadmap -- "Defined But Not Wired" Detection

### A1: Deterministic Requirement ID Cross-Reference Gate

**Summary**: Parse all requirement IDs from the spec and verify each appears in the roadmap body text before the fidelity gate can pass.

**Mechanism**: A new semantic check function added to `SPEC_FIDELITY_GATE` that runs alongside the existing LLM-generated severity report. It uses regex to extract all identifiers matching patterns `FR-\d+`, `NFR-\d+`, `SC-\d+`, `D-\d+` from the spec extraction artifact. It then scans the roadmap text for each ID. Any ID present in the spec but absent from the roadmap triggers an automatic HIGH severity deviation injected into the frontmatter counts, overriding whatever the LLM reported. The Python enforcer in `gate_passed()` then blocks on `high_severity_count > 0` as it already does.

**What it would catch**: The cli-portify bug's three-way dispatch requirement would have been tagged as FR-NNN in the spec. If that FR-NNN was absent from the roadmap, this gate would have blocked roadmap generation regardless of LLM classification. It catches any requirement that is silently dropped during roadmap generation -- the exact failure mode in Link 1 of the fidelity chain.

**Integration point**: `src/superclaude/cli/roadmap/gates.py` -- add a new `SemanticCheck` entry to the `SPEC_FIDELITY_GATE.semantic_checks` list. The check function receives the fidelity report content but would also need access to the spec and roadmap files. This means either (a) embedding extracted IDs into the fidelity report prompt output so they appear in the content string, or (b) extending `SemanticCheck` to accept a context dict with file paths, which requires a change to `pipeline/gates.py:gate_passed()`.

**Limitations**: Only works if specs consistently use tagged identifiers. Free-text requirements without IDs (like "three-way dispatch" described in prose) would not be caught. Requires discipline in spec authoring to tag every functional requirement. Also, an ID appearing in roadmap text does not guarantee the roadmap actually addresses it -- it could appear in a "deferred" or "out of scope" note.

---

### A2: Architectural Dependency Graph Extraction and Matching

**Summary**: Extract module dependency graphs from the spec and verify the roadmap preserves all specified import/call relationships.

**Mechanism**: The spec fidelity prompt is augmented with an additional comparison dimension (dimension 6: "Module Dependencies") that instructs the LLM to extract every `module_A --> module_B` dependency declared in the spec (e.g., `executor.py --> steps/validate_config.py`) and verify each edge appears in the roadmap. A structured output section `## Dependency Coverage` lists each spec dependency edge with status COVERED/MISSING. A new semantic check parses this section and counts MISSING entries. Any MISSING dependency edge is treated as HIGH severity.

**What it would catch**: The cli-portify spec explicitly declared `executor.py --> steps/*.py` import chains and `PROGRAMMATIC_RUNNERS` dispatch mappings. This gate would detect that the roadmap's "sequential execution with mocked steps" description dropped all dependency edges from executor to step modules. It specifically targets the "two parallel tracks never joined" failure mode.

**Integration point**: `src/superclaude/cli/roadmap/prompts.py:build_spec_fidelity_prompt()` -- add dimension 6 to the comparison dimensions list. `src/superclaude/cli/roadmap/gates.py` -- add a semantic check that parses the `## Dependency Coverage` section for MISSING entries.

**Limitations**: Still LLM-dependent for extraction accuracy. If the spec describes dependencies in prose rather than diagrams, the LLM may miss edges. The roadmap may legitimately restructure dependencies (e.g., using a different dispatch pattern than the spec proposed), which would trigger false positives. No way to distinguish "intentionally redesigned" from "accidentally dropped" without human judgment.

---

### A3: Integration Task Completeness Heuristic

**Summary**: When the spec defines component A and component B separately, require the roadmap to contain an explicit integration task connecting them.

**Mechanism**: A post-generation analysis step (new pipeline step between `spec-fidelity` and `tasklist-generation`) that uses an LLM prompt to enumerate all "component pairs" from the spec that require integration. For each pair, it checks whether the roadmap contains a phase, milestone, or key action that explicitly describes connecting them. The prompt instructs: "For each component pair (e.g., executor + step implementations), verify the roadmap contains a task whose description includes both components and uses integration language (wire, connect, dispatch, route, bind, inject, register)." Output is a coverage matrix with WIRED/UNWIRED status per pair.

**What it would catch**: The spec defined the executor (Track A) and step implementations (Track B) as separate components. This heuristic would flag that the roadmap has no task containing both "executor" and "step" in integration context. It directly addresses the "two parallel development tracks built independently and never joined" pattern identified in the forensic report.

**Integration point**: New step in `src/superclaude/cli/roadmap/` pipeline, inserted after `spec-fidelity` in `_build_steps()`. Gate criteria would be a new `INTEGRATION_COMPLETENESS_GATE` in `roadmap/gates.py` with STRICT enforcement. The step would consume both the spec extraction and the roadmap as inputs.

**Limitations**: Relies on LLM judgment to identify component pairs and integration language. Could produce false positives for components that are intentionally decoupled (e.g., plugin interfaces designed for late binding). The heuristic of looking for "integration language" is fragile -- a roadmap could say "ensure executor handles steps" without using the specific verb patterns. Adds pipeline latency with an extra LLM call.

---

### A4: Callable Wiring Declaration Extraction

**Summary**: Parse the spec for all callable injection points (constructor parameters, registry entries, dispatch maps) and verify each has a corresponding roadmap deliverable.

**Mechanism**: A deterministic pre-check runs before the LLM-based fidelity analysis. It scans the spec for patterns indicating callable wiring: `step_runner`, `DISPATCH`, `RUNNERS`, `registry.*function`, `handler.*callable`, constructor parameters with `Callable` or `Optional[Callable]` types, and dictionary literals mapping string keys to function references. Each discovered injection point is logged as a "wiring requirement." The roadmap is then scanned for each injection point name. Missing injection points are flagged.

**What it would catch**: The cli-portify spec defined `PROGRAMMATIC_RUNNERS` (a dispatch dictionary) and `step_runner` (a constructor callable). Both would have been extracted as wiring requirements. The roadmap's omission of both would trigger the gate. This solution specifically targets the pattern where architecture specs define pluggable extension points that are never connected in implementation.

**Integration point**: New function in `src/superclaude/cli/roadmap/gates.py` added as a `SemanticCheck` on `SPEC_FIDELITY_GATE`. The function would need to read both the spec and roadmap files. Alternatively, implemented as a pre-check in `src/superclaude/cli/roadmap/validate_gates.py` that runs before the main fidelity step.

**Limitations**: Pattern-based extraction is brittle -- it relies on naming conventions (`RUNNERS`, `DISPATCH`, `Callable`) that may not be used in all specs. Specs written in natural language prose without code snippets would yield zero extractions. Does not handle cases where the roadmap uses different terminology for the same concept (e.g., "step execution routing" instead of `PROGRAMMATIC_RUNNERS`). High false-negative rate for specs that describe wiring abstractly.

---

### A5: Dual-Pass Fidelity with Adversarial Reviewer

**Summary**: Run two independent LLM passes on spec-to-roadmap fidelity -- a standard pass and an adversarial pass specifically hunting for "defined but not wired" omissions -- then merge results.

**Mechanism**: The existing `spec-fidelity` step becomes pass 1 (unchanged). A new `spec-fidelity-adversarial` step runs as pass 2 with a specialized prompt: "You are an adversarial reviewer. Your goal is to find components, modules, dispatch mechanisms, registries, and integration points that the spec defines but the roadmap omits or defers. For each component the spec defines, verify the roadmap contains: (a) a task to build it, (b) a task to wire it to its consumers, (c) a test to verify the wiring. Flag any component missing (b) or (c) as HIGH severity." A merge step combines both reports, taking the higher severity for any deviation found by both passes, and adding unique findings from the adversarial pass.

**What it would catch**: The adversarial reviewer is specifically prompted to look for missing wiring tasks. It would flag that the roadmap has tasks to build the executor and tasks to build step modules, but no task to wire them together and no test for wiring verification. This directly targets the systemic blind spot where document-level review passes because individual components look complete in isolation.

**Integration point**: Two new steps in `src/superclaude/cli/roadmap/` pipeline: `spec-fidelity-adversarial` (after `spec-fidelity`) and `spec-fidelity-merge` (after adversarial). New prompt function `build_spec_fidelity_adversarial_prompt()` in `roadmap/prompts.py`. New gate `SPEC_FIDELITY_ADVERSARIAL_GATE` in `roadmap/gates.py`. The merge step's gate replaces the original `SPEC_FIDELITY_GATE` as the blocking gate.

**Limitations**: Doubles the LLM cost for fidelity checking. The adversarial reviewer is still an LLM and may miss the same omissions if the spec describes wiring implicitly. Merge logic must handle conflicting severity classifications. The adversarial prompt could produce false positives by flagging intentional design simplifications as "missing wiring." Pipeline latency increases by two additional LLM steps.

---

## Section B: Roadmap-to-Tasklist -- Integration Wiring Verification

### B1: Deliverable-to-Task Traceability Matrix

**Summary**: Parse all deliverable IDs from the roadmap and verify each has at least one corresponding task in the tasklist, with special attention to deliverables tagged as integration or wiring.

**Mechanism**: After tasklist generation, a new verification step extracts all deliverable identifiers (`D-NNNN`, `R-NNN`) from the roadmap. For each deliverable, it searches the tasklist files for a task that references the same identifier. It then classifies deliverables as "standalone" (single-component) or "integration" (cross-component). Integration deliverables are identified by keywords: "wire," "connect," "dispatch," "integrate," "bind," "route," "register," or by referencing two or more distinct modules. Integration deliverables require at least TWO tasks: one for implementation and one for wiring/connection verification. The output is a traceability matrix with COVERED/UNCOVERED status.

**What it would catch**: If the roadmap had included a deliverable like "D-0042: Executor dispatches to step implementations," this gate would verify the tasklist contains tasks referencing D-0042. More importantly, it would catch the actual failure: since the roadmap omitted this deliverable entirely, the traceability matrix would show no integration deliverables between executor and steps -- which, combined with Section A solutions, creates a layered defense. At the tasklist level alone, it catches cases where the roadmap does mention integration but the tasklist decomposes it into build-only tasks without a wiring task.

**Integration point**: `src/superclaude/cli/tasklist/gates.py` -- add a new `DELIVERABLE_TRACEABILITY_GATE` alongside `TASKLIST_FIDELITY_GATE`. The gate runs as a semantic check that parses both the roadmap and tasklist files. Requires extending the tasklist gate infrastructure to accept the roadmap path as context, similar to how `build_tasklist_fidelity_prompt()` already receives it.

**Limitations**: Depends on consistent deliverable ID usage across roadmap and tasklist. If deliverables are described in prose without IDs, the regex-based extraction fails. The "integration" classification heuristic (keyword-based) may miss integration deliverables that use different terminology. Does not verify that the task actually performs wiring -- only that a task referencing the deliverable ID exists.

---

### B2: Import Chain Verification Task Injection

**Summary**: For every roadmap phase that produces multiple code modules, automatically inject a tasklist task requiring import chain verification between the modules.

**Mechanism**: During tasklist generation, a post-processing step analyzes the roadmap's per-phase deliverables. When a phase produces two or more code files in the same package (e.g., `executor.py` and `steps/*.py` in the same `cli_portify/` package), the system injects a synthetic task: "Verify that [module A] imports and calls [module B] as specified in the roadmap." The injected task includes acceptance criteria: "All public functions in [module B] are imported by [module A] or documented as intentionally unused." These synthetic tasks are marked with a `[GENERATED]` tag so they are distinguishable from LLM-generated tasks.

**What it would catch**: The cli-portify roadmap Phase 2 produced both `executor.py` and `steps/*.py`. This solution would inject a task requiring verification that `executor.py` imports from `steps/*.py`. When the sprint runner executes this task, the acceptance criteria would fail because `executor.py` never imports any step module. It directly prevents the "two parallel tracks never joined" failure.

**Integration point**: New post-processing function in `src/superclaude/cli/tasklist/` that runs after LLM-generated tasklist content is written but before the `TASKLIST_FIDELITY_GATE`. The function parses roadmap phases for multi-module deliverables and appends synthetic tasks to the relevant tasklist group files. The `TASKLIST_FIDELITY_GATE` would need a carve-out to not flag `[GENERATED]` tasks as deviations from the roadmap.

**Limitations**: Only triggers when a single phase produces multiple modules. If the executor and steps are produced in different phases (as happened in cli-portify across v2.24 and v2.24.1), the cross-phase relationship would not be detected. Requires the roadmap to specify output file paths explicitly -- if the roadmap says "implement executor" without naming `executor.py`, the module extraction fails. Synthetic task injection may conflict with the fidelity gate's expectation that tasklist tasks trace 1:1 to roadmap deliverables.

---

### B3: Acceptance Criteria Wiring Keyword Audit

**Summary**: Scan all tasklist acceptance criteria for tasks involving code components and flag any group that lacks wiring-specific acceptance criteria.

**Mechanism**: After tasklist generation, a keyword audit scans every task's acceptance criteria. Tasks are classified as "code-producing" if their descriptions reference creating, implementing, or building code artifacts (functions, classes, modules, registries). For each code-producing task group, the audit checks whether at least one task's acceptance criteria contains wiring verification language: "imports," "calls," "dispatches to," "routes to," "is invoked by," "is reachable from," "is connected to." If a task group produces 2+ code modules but no acceptance criterion verifies cross-module connectivity, the audit emits a WARNING that must be acknowledged (not auto-blocking, but surfaced in the gate report).

**What it would catch**: The cli-portify tasklist group T03 produced both executor infrastructure and step implementations across multiple tasks. None of the acceptance criteria in T03 contained wiring verification language -- they checked sequential flow, resume behavior, and interrupt handling, but never "executor calls step functions" or "step implementations are imported by executor." This audit would have flagged the gap. It catches the specific failure where acceptance criteria validate individual component behavior but not cross-component integration.

**Integration point**: New semantic check in `src/superclaude/cli/tasklist/gates.py` added to `TASKLIST_FIDELITY_GATE.semantic_checks`. The check function receives the tasklist content and performs keyword analysis. Alternatively, implemented as a standalone gate `WIRING_CRITERIA_GATE` at STANDARD enforcement tier (warning, not blocking) to avoid over-constraining the pipeline.

**Limitations**: Keyword-based detection is inherently noisy. Acceptance criteria may describe wiring using domain-specific language that the keyword list does not cover. False positives when components are intentionally decoupled (e.g., plugin APIs where the consumer is a third party). False negatives when acceptance criteria use vague language like "works end-to-end" that implies wiring but does not use specific wiring verbs. WARNING-level enforcement means the gap can still be acknowledged and bypassed.

---

### B4: Constructor Dependency Completeness Check

**Summary**: For every class constructor defined in the roadmap's deliverables, verify the tasklist includes a task that provides all non-default parameters in production code paths.

**Mechanism**: A targeted analysis step runs after tasklist generation. It extracts class constructor signatures from the roadmap (or from the spec if the roadmap references them). For each constructor parameter that has a default value of `None` and a type annotation including `Callable`, `Optional`, or `Protocol`, it records this as a "pluggable dependency." It then searches the tasklist for a task whose description or acceptance criteria explicitly mentions providing that parameter. The check emits HIGH severity for any pluggable dependency that has no corresponding provisioning task.

**What it would catch**: `PortifyExecutor.__init__()` has `step_runner: Optional[Callable] = None`. The spec defined this parameter and expected production code to provide it. This check would flag that no tasklist task says "provide step_runner to PortifyExecutor" or "wire step_runner callback." It specifically targets the constructor injection pattern where a parameter exists for extensibility but is never provided in the production call site -- the exact mechanism of the cli-portify no-op bug.

**Integration point**: New gate in `src/superclaude/cli/tasklist/gates.py` as `CONSTRUCTOR_COMPLETENESS_GATE`. Requires access to both the spec (for constructor signatures) and the tasklist (for task descriptions). Could alternatively be implemented as an LLM-prompted analysis step in the tasklist pipeline with deterministic post-validation of the LLM's output.

**Limitations**: Only works when specs include constructor signatures with type annotations. Many specs describe constructors in prose without formal signatures. Requires the roadmap to preserve constructor details from the spec (which is exactly the failure this solution tries to prevent -- creating a chicken-and-egg problem). Parameters with `None` defaults are sometimes legitimately optional in production (e.g., logging callbacks). Would need a whitelist mechanism for intentionally-optional parameters to avoid false positives.

---

### B5: End-to-End Call Path Task Verification

**Summary**: For every user-facing entry point defined in the roadmap, verify the tasklist contains tasks that cover the complete call path from entry point to leaf implementation.

**Mechanism**: The roadmap defines user-facing entry points (CLI commands, API endpoints, pipeline entry functions). For each entry point, the solution traces the expected call path through the architecture: entry point -> orchestrator -> dispatch -> implementation -> output. It then verifies that the tasklist contains at least one task per call-path segment. If any segment has no corresponding task, the verification fails. The call path is extracted from the roadmap's architectural description or module dependency graph. A structured output format lists each entry point with its call path segments and TASKED/UNTASKED status.

**What it would catch**: The `run_portify()` entry point has an expected call path: `commands.py:run()` -> `run_portify()` -> `PortifyExecutor.run()` -> `_execute_step()` -> `step_runner()` -> `steps/*.py`. The tasklist covered segments 1-3 (command, entry point, executor loop) but not segments 4-5 (dispatch to step_runner, step_runner invoking step implementations). This check would flag segments 4-5 as UNTASKED. It catches incomplete task decomposition where the "last mile" of a call path -- the actual work -- is left untasked.

**Integration point**: New pipeline step in `src/superclaude/cli/tasklist/` that runs after tasklist generation and before (or as part of) the fidelity gate. Implemented as an LLM-prompted analysis step with a specialized prompt: "Trace each entry point through the roadmap's architecture to its leaf implementation. For each call-path segment, find a tasklist task that covers it." Gate criteria: `CALL_PATH_COVERAGE_GATE` in `tasklist/gates.py` at STRICT enforcement, blocking if any entry point has UNTASKED segments.

**Limitations**: Call path extraction from roadmap prose is LLM-dependent and error-prone. The roadmap may not describe call paths explicitly -- it may describe components without specifying their invocation chain. Deep call paths (5+ segments) are harder for the LLM to trace accurately. The granularity question is hard: should `_execute_step() -> step_runner()` be one segment or two? Over-segmentation leads to false positives; under-segmentation misses the gaps this solution aims to catch. Adds significant LLM cost for entry points with complex call graphs.

---

## Cross-Cutting Observations

### Solution Pairing Recommendations

The strongest defense combines one deterministic solution with one LLM-based solution per phase:

- **Spec-to-Roadmap**: A1 (ID cross-reference) + A2 (dependency graph) -- deterministic ID checking catches tagged requirements; dependency graph extraction catches architectural wiring
- **Roadmap-to-Tasklist**: B1 (deliverable traceability) + B5 (call path verification) -- traceability catches missing deliverable coverage; call path verification catches incomplete task decomposition

### Implementation Priority

Solutions are ordered by estimated impact-to-effort ratio:

1. **A1** (ID cross-reference) -- highest ROI; purely deterministic; hooks into existing gate infrastructure with minimal changes
2. **B3** (acceptance criteria audit) -- low implementation cost; keyword scan of existing content; catches the exact acceptance criteria gap from the forensic report
3. **B1** (deliverable traceability) -- moderate cost; extends existing fidelity gate pattern; addresses the core "vacuous pass" problem at Link 2
4. **A5** (adversarial reviewer) -- high cost but catches novel omission patterns that deterministic checks miss
5. **B5** (call path verification) -- highest detection power but also highest LLM cost and complexity

### Shared Infrastructure Needed

Several solutions require extending the gate infrastructure beyond its current `(content: str) -> bool` signature:

- A1, A4, B1, B4 need access to source documents (spec, roadmap) in addition to the gate output file
- B2 needs write access to inject synthetic tasks
- A5 needs multi-step pipeline coordination

The `gate_passed()` function in `src/superclaude/cli/pipeline/gates.py` and the `SemanticCheck` model in `src/superclaude/cli/pipeline/models.py` would need to support a `context: dict` parameter to pass additional file paths and metadata to semantic check functions.

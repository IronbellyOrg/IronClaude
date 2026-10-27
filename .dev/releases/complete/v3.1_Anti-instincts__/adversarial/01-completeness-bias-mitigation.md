# Anti-Instinct 01: Completeness Bias Mitigation

**Date**: 2026-03-17
**Status**: Brainstorm -- ready for design spec
**Category**: LLM tendency mitigation (programmatic)
**Pipeline target**: `src/superclaude/cli/roadmap/`

---

## 1. The LLM Tendency: Surface-Level Completeness

LLMs produce outputs that *look* complete before they *are* complete. When generating a roadmap from a specification, the model gravitates toward architecturally interesting components (executor loops, gate systems, convergence patterns, phase structures) and away from mundane connective tissue (dispatch wiring, import chains, constructor parameter provision, validation call insertion).

The result: a roadmap with 10 phases, milestones, timelines, success criteria, and a validation matrix -- that is missing the single unglamorous integration task connecting an executor loop to its step implementations.

This is not laziness. The LLM has a strong prior that "a well-structured document with phases, milestones, and success criteria" equals "a complete document." The structure itself signals completeness to the model, making it less likely to notice that a low-glamour requirement was never assigned to any phase.

### Key characteristics of this bias

1. **Structural completeness masks semantic incompleteness**: The roadmap has all the expected sections, correct heading hierarchy, proper frontmatter, and passes all format gates.
2. **Integration tasks are systematically under-represented**: Tasks that wire component A to component B are less "interesting" than designing either component. They rarely merit their own phase heading, so they get absorbed into vague language ("implement executor") or dropped entirely.
3. **The bias is invisible to same-model validation**: Asking the same LLM to validate the roadmap against the spec triggers the same bias -- the validator sees the structural completeness and classifies omissions as LOW severity or misses them entirely.

---

## 2. The Evidence: CLI-Portify Executor No-Op Bug

Full forensic report: `.dev/releases/backlog/fidelity-refactor/cli-portify-executor-noop-forensic-report.md`

### What the spec defined (correct design)

The v2.24/v2.25 specifications defined a three-way dispatch architecture:

```python
# From spec Appendix D
if step.is_programmatic:
    step_result = _run_programmatic_step(step, config)
elif step.phase_type == PortifyPhaseType.USER_REVIEW:
    step_result = _run_review_gate(step, config, result)
else:
    step_result = _run_claude_step(step, config, handler, monitor, tui, ledger)
```

Plus a `PROGRAMMATIC_RUNNERS` dictionary mapping step IDs to real Python functions, a module dependency graph (`executor.py --> steps/validate_config.py`, etc.), and an integration test `test_programmatic_step_routing`.

### What the roadmap produced (dropped requirement)

The roadmap reduced the executor to:

> "Implement executor: sequential execution only, --dry-run, --resume <step-id>, signal handling"

And milestone M2:

> "Sequential pipeline runs end-to-end with **mocked steps**"

Zero mentions of `PROGRAMMATIC_RUNNERS`, three-way dispatch, or the `executor.py --> steps/*.py` import chain. The dispatch wiring -- the single task that connects all other components into a working system -- was never assigned to any phase.

### How the corruption propagated

```
Spec (correct) --[ROADMAP GENERATION dropped dispatch]--> Roadmap (incomplete)
    --[SPEC_FIDELITY_GATE LLM missed it]--> Roadmap certified as faithful
    --[TASKLIST GENERATION faithfully reproduced roadmap]--> Tasklist (incomplete)
    --[TASKLIST_FIDELITY_GATE passed vacuously]--> Tasklist certified
    --[SPRINT EXECUTION built what tasklist said]--> Code (no-op executor)
```

The `SPEC_FIDELITY_GATE` at `src/superclaude/cli/roadmap/gates.py:633-656` enforces `high_severity_count == 0` in YAML frontmatter. But the severity classification is entirely LLM-generated. The LLM validator either missed the dispatch omission or classified it below HIGH. The Python gate enforcement was sound; the LLM input to that gate was wrong.

### The pattern is systemic

The forensic report found the same "defined but not wired" pattern in four systems:

| System | What exists | What is missing |
|--------|-------------|-----------------|
| cli-portify executor | `step_runner=None` default; step implementations in `steps/` | Dispatch map connecting executor to steps |
| `DEVIATION_ANALYSIS_GATE` | Gate defined at `roadmap/gates.py:712` | Not included in `_build_steps()` |
| `SprintGatePolicy` | Policy class at `sprint/executor.py:46-89` | Never invoked from sprint loop |
| Trailing gate framework | `TrailingGateRunner` exists | `execute_sprint()` never calls it |

---

## 3. Proposed Solutions

### Solution A: Requirement ID Traceability Pass (Deterministic)

**Concept**: After roadmap generation and before the spec-fidelity LLM pass, run a deterministic cross-reference check that parses requirement IDs from the extraction document and verifies each appears in the roadmap body text.

**How it works**:

1. Parse all structured IDs from `extraction.md`: `FR-NNN`, `NFR-NNN`, `SC-NNN`, `R-NNN` (risks), `D-NNN` (dependencies)
2. Parse the generated `roadmap.md` body text for occurrences of these same IDs
3. Compute a coverage ratio: `mentioned_ids / total_ids`
4. Any ID present in extraction but absent from the roadmap is flagged as an **untraced requirement**
5. Emit a structured report with per-ID status (TRACED / UNTRACED) and a coverage percentage

**Gate integration**:

```python
# New file: src/superclaude/cli/roadmap/traceability.py

import re
from pathlib import Path
from dataclasses import dataclass

# Canonical ID patterns extracted by the extraction step
_ID_PATTERNS = [
    re.compile(r"\bFR-\d{3}\b"),      # Functional requirements
    re.compile(r"\bNFR-\d{3}\b"),     # Non-functional requirements
    re.compile(r"\bSC-\d{3}\b"),      # Success criteria
    re.compile(r"\bR-\d{3}\b"),       # Risks
    re.compile(r"\bDEP-\d{3}\b"),     # Dependencies
]

@dataclass
class TraceabilityResult:
    total_ids: int
    traced_ids: int
    untraced: list[str]  # IDs found in extraction but not in roadmap
    coverage: float       # traced / total

def check_requirement_traceability(
    extraction_path: Path,
    roadmap_path: Path,
) -> TraceabilityResult:
    """Deterministic cross-reference: every ID in extraction must appear in roadmap."""
    extraction_text = extraction_path.read_text(encoding="utf-8")
    roadmap_text = roadmap_path.read_text(encoding="utf-8")

    # Extract all IDs from the extraction document
    extraction_ids: set[str] = set()
    for pattern in _ID_PATTERNS:
        extraction_ids.update(pattern.findall(extraction_text))

    # Check which IDs appear in the roadmap
    traced: set[str] = set()
    untraced: list[str] = []
    for req_id in sorted(extraction_ids):
        if req_id in roadmap_text:
            traced.add(req_id)
        else:
            untraced.append(req_id)

    total = len(extraction_ids)
    coverage = len(traced) / total if total > 0 else 1.0

    return TraceabilityResult(
        total_ids=total,
        traced_ids=len(traced),
        untraced=untraced,
        coverage=coverage,
    )
```

**Gate criteria** (added to `src/superclaude/cli/roadmap/gates.py`):

```python
def _traceability_coverage_sufficient(content: str) -> bool:
    """traceability_coverage must be >= 0.95 (allow 5% for genuinely deferred items)."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("traceability_coverage")
    if value is None:
        return False
    try:
        coverage = float(value)
    except (ValueError, TypeError):
        return False
    return coverage >= 0.95

def _untraced_count_zero_or_justified(content: str) -> bool:
    """untraced_high_severity must be 0."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("untraced_high_severity")
    if value is None:
        return False
    try:
        return int(value) == 0
    except (ValueError, TypeError):
        return False
```

**Where this runs in the pipeline**: As a new step between `merge` and `spec-fidelity`, or as a pre-check embedded in the spec-fidelity step. The traceability report is deterministic -- no LLM involved -- so it runs in milliseconds.

**How it would have caught the cli-portify bug**: The extraction step would have produced IDs for the three-way dispatch requirement (e.g., `FR-047: Three-way executor dispatch`). The traceability pass would have flagged `FR-047` as UNTRACED in the roadmap. The gate would have blocked progression before the LLM-based spec-fidelity check even ran.

**Limitation**: This only works if the extraction step itself captures the requirement with an ID. If the extraction LLM also drops the dispatch requirement, this gate passes vacuously. See Solution C for mitigation of that failure mode.

---

### Solution B: Orphaned Component Detection (Graph-Based)

**Concept**: After roadmap generation, build a dependency graph of all components mentioned in the roadmap and detect "orphaned" components -- things that are built but never consumed, or things that consume interfaces that are never provided.

**How it works**:

1. Parse the roadmap for component definitions (classes, modules, registries, functions mentioned in phase tasks)
2. Parse for integration relationships (imports, wiring, dispatch, registration)
3. Build a directed graph: `component_A --uses--> component_B`
4. Detect orphans: nodes with in-degree 0 (built but never consumed) or out-degree 0 when they have declared dependencies (consume interfaces never provided)
5. Flag the "producer-consumer gap" pattern: when a roadmap defines both a producer (step implementations) and a consumer (executor loop) but never defines the edge between them

**Implementation sketch**:

```python
# New file: src/superclaude/cli/roadmap/orphan_detector.py

import re
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ComponentNode:
    name: str
    phase: str
    node_type: str  # "class", "module", "registry", "function", "interface"
    producers: list[str] = field(default_factory=list)  # components that create/define this
    consumers: list[str] = field(default_factory=list)   # components that use this

@dataclass
class OrphanReport:
    total_components: int
    orphaned_producers: list[str]  # built but never consumed
    orphaned_consumers: list[str]  # expected but never provided
    missing_edges: list[tuple[str, str]]  # (producer, consumer) pairs with no wiring task

def detect_orphaned_components(roadmap_path: Path) -> OrphanReport:
    """Parse roadmap for producer-consumer relationships and find gaps."""
    roadmap_text = roadmap_path.read_text(encoding="utf-8")

    # Heuristic extraction of component names and their relationships
    # This uses pattern matching on roadmap phase descriptions
    components = _extract_components(roadmap_text)
    edges = _extract_relationships(roadmap_text, components)

    # Build adjacency sets
    produced_by: dict[str, set[str]] = {}  # component -> set of phases that produce it
    consumed_by: dict[str, set[str]] = {}  # component -> set of phases that consume it

    for comp in components:
        produced_by[comp.name] = set(comp.producers)
        consumed_by[comp.name] = set(comp.consumers)

    # Find orphans
    orphaned_producers = [
        name for name, producers in produced_by.items()
        if producers and not consumed_by.get(name)
    ]
    orphaned_consumers = [
        name for name, consumers in consumed_by.items()
        if consumers and not produced_by.get(name)
    ]

    # Find missing wiring: both producer and consumer exist, but no integration task
    missing_edges = []
    for edge in edges:
        if not _has_wiring_task(roadmap_text, edge):
            missing_edges.append(edge)

    return OrphanReport(
        total_components=len(components),
        orphaned_producers=orphaned_producers,
        orphaned_consumers=orphaned_consumers,
        missing_edges=missing_edges,
    )
```

**Where this runs**: Post-merge, before spec-fidelity. The component extraction is heuristic (regex + keyword matching on the roadmap text), so it has false-positive potential and should run in STANDARD enforcement tier initially.

**How it would have caught the cli-portify bug**: The roadmap mentions `steps/validate_config.py`, `steps/discover_components.py` etc. as deliverables in Phase 2, and `PortifyExecutor.run()` as a deliverable in Phase 3. The orphan detector would flag: "steps/*.py modules are produced in Phase 2 but no phase consumes them (imports from executor)." The `PortifyExecutor` would be flagged as a consumer of step implementations with no wiring task.

**Limitation**: Heuristic parsing of natural-language roadmaps is fragile. Component names must be mentioned with sufficient specificity for regex extraction. Works best when the roadmap uses code-level names (function names, module paths) rather than abstract descriptions.

---

### Solution C: Spec-to-Extraction Structural Audit (Upstream Guard)

**Concept**: Add a deterministic check between the spec input and the extraction output to catch the case where the extraction LLM itself drops a requirement before it ever reaches the roadmap.

**How it works**:

1. Parse the raw spec for structural markers that indicate requirements:
   - Code blocks containing function signatures, class definitions, dispatch tables
   - Sections with "MUST", "SHALL", "REQUIRED" language
   - Pseudocode blocks
   - Explicit test names (`test_programmatic_step_routing`)
   - Dictionary/registry definitions (`PROGRAMMATIC_RUNNERS`)
2. Count these structural markers in the spec
3. Compare against the extraction's `functional_requirements` + `nonfunctional_requirements` count
4. If the spec has N structural requirement indicators but the extraction reports fewer than N * threshold, flag for re-extraction

**Implementation sketch**:

```python
# New file: src/superclaude/cli/roadmap/spec_structural_audit.py

import re
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SpecStructuralAudit:
    code_block_count: int          # Number of code blocks in spec
    must_shall_count: int          # Sentences with MUST/SHALL/REQUIRED
    function_signature_count: int  # def foo() patterns in code blocks
    class_definition_count: int    # class Foo patterns in code blocks
    test_name_count: int           # test_* patterns
    registry_pattern_count: int    # UPPERCASE_DICT = { patterns
    pseudocode_blocks: int         # Blocks showing control flow (if/else/for)
    total_structural_indicators: int

def audit_spec_structure(spec_path: Path) -> SpecStructuralAudit:
    """Count structural requirement indicators in the raw spec."""
    text = spec_path.read_text(encoding="utf-8")

    code_blocks = re.findall(r"```[\s\S]*?```", text)
    code_text = "\n".join(code_blocks)

    return SpecStructuralAudit(
        code_block_count=len(code_blocks),
        must_shall_count=len(re.findall(
            r"\b(?:MUST|SHALL|REQUIRED)\b", text
        )),
        function_signature_count=len(re.findall(
            r"\bdef\s+\w+\s*\(", code_text
        )),
        class_definition_count=len(re.findall(
            r"\bclass\s+\w+", code_text
        )),
        test_name_count=len(re.findall(
            r"\btest_\w+", text
        )),
        registry_pattern_count=len(re.findall(
            r"\b[A-Z][A-Z_]+\s*=\s*\{", code_text
        )),
        pseudocode_blocks=len(re.findall(
            r"```[\s\S]*?(?:if\s|elif\s|else:|for\s|while\s)[\s\S]*?```", text
        )),
        total_structural_indicators=0,  # computed below
    )
```

Post-init computes `total_structural_indicators` as a weighted sum. The extraction's `total_requirements` count is then compared: if `total_requirements < total_structural_indicators * 0.7`, the extraction is flagged as potentially incomplete and the step retries or escalates.

**Where this runs**: Between the `extract` step and the `generate` steps. Pure Python, no LLM, sub-second execution.

**How it would have caught the cli-portify bug**: The spec contained pseudocode for three-way dispatch (a code block with `if/elif/else`), the `PROGRAMMATIC_RUNNERS` registry definition (uppercase dict assignment), the `test_programmatic_step_routing` test name, and multiple `def _run_*` function signatures. The structural audit would have produced a high indicator count, and if the extraction dropped these, the discrepancy would trigger re-extraction before the roadmap generation even began.

---

### Solution D: Integration Task Injection via Prompt Constraint

**Concept**: Modify the generate prompt to include a structural constraint that forces the LLM to explicitly address integration/wiring for every component pair.

**How it works**: Add to the generate prompt (`src/superclaude/cli/roadmap/prompts.py`, `build_generate_prompt()`):

```
## MANDATORY: Integration Task Requirement

For every component or module that your roadmap defines as a deliverable, you MUST
include an explicit integration task that specifies:
1. What calls/imports/wires this component to its consumer
2. Which phase this integration occurs in
3. What the acceptance criterion for "properly wired" looks like

If a module is defined in Phase N and consumed in Phase M, there MUST be an explicit
task in Phase M (or between N and M) for wiring them together. "Implement X" is NOT
sufficient -- you must separately task "Wire X into Y" or "Register X in Z's dispatch table."

Common integration patterns that MUST be explicitly tasked:
- Dispatch tables: creating the mapping from IDs to implementation functions
- Constructor injection: passing dependencies that default to None
- Import chains: adding import statements from consumer to producer
- Registration: adding entries to registries, dictionaries, or configuration

If the spec defines a dispatch model (e.g., a dictionary mapping step IDs to functions),
the roadmap MUST contain a task for populating that dictionary with real function references.
"Implement executor" does NOT satisfy this -- "Wire step dispatch table to step implementations"
does.

After generating the roadmap, self-check: for every deliverable in Phase N,
trace forward to find the Phase M task that integrates it. If no integration task
exists, add one.
```

**Where this goes**: Appended to the generate prompt in `build_generate_prompt()` at `src/superclaude/cli/roadmap/prompts.py:130-165`.

**How it would have caught the cli-portify bug**: The prompt constraint explicitly calls out the dispatch-table-to-functions pattern and mandates a separate wiring task. The LLM would have been primed to create an explicit "Wire STEP_REGISTRY to step implementations via PROGRAMMATIC_RUNNERS dispatch map" task rather than absorbing dispatch into the vague "Implement executor" task.

**Limitation**: This is prompt engineering, which is inherently non-deterministic. It reduces the probability of the failure mode but does not eliminate it. Must be combined with deterministic solutions (A, B, or C) for defense in depth.

---

### Solution E: Post-Generation "Integration Completeness" LLM Pass with Structured Constraint

**Concept**: Add a separate LLM pass after roadmap generation that specifically hunts for missing integration tasks, with a structured output format that forces enumeration.

**How it works**:

1. New pipeline step: `integration-audit` (runs after `merge`, before or alongside `spec-fidelity`)
2. Prompt provides the roadmap and asks the LLM to enumerate ALL producer-consumer pairs
3. For each pair, the LLM must state the specific phase and task that wires them together
4. If no wiring task exists, the LLM must flag it as MISSING
5. Output is structured YAML with per-pair status

**Prompt structure**:

```
You are an integration completeness auditor.

Read the provided roadmap. For every component, module, class, registry, or function
that the roadmap defines as a deliverable:

1. Identify its PRODUCER phase (where it is created/implemented)
2. Identify its CONSUMER(s) (what will call/import/use it)
3. Identify the WIRING TASK (the specific roadmap task that connects producer to consumer)

Output a YAML table:

---
total_pairs: (integer)
wired_pairs: (integer)
missing_wiring: (integer)
integration_coverage: (float 0.0-1.0)
---

## Integration Pairs

| # | Producer | Producer Phase | Consumer | Consumer Phase | Wiring Task | Status |
|---|----------|---------------|----------|---------------|-------------|--------|
| 1 | steps/validate_config.py | Phase 2 | PortifyExecutor._execute_step | Phase 3 | [task ref or MISSING] | WIRED/MISSING |

If the Status column contains any MISSING entries, this roadmap has an integration gap.
```

**Gate**: `missing_wiring == 0` as a semantic check on the integration-audit output.

**How it would have caught the cli-portify bug**: The structured enumeration format forces the LLM to explicitly trace each producer to its consumer. When it tries to fill in the "Wiring Task" column for `steps/*.py -> PortifyExecutor._execute_step`, it would find no matching task and be forced to write MISSING. The structured table format counteracts the completeness bias because it forces per-pair accountability rather than allowing vague summaries.

**Why this is better than the existing spec-fidelity check**: The spec-fidelity prompt asks "find deviations" (open-ended, bias toward confirming completeness). The integration-audit prompt asks "for each pair, name the wiring task" (closed-form, bias toward finding gaps because MISSING is an explicit option).

---

## 4. Recommended Implementation Order

### Phase 1: Immediate (can ship in v2.27)

1. **Solution D (Prompt constraint)**: Lowest cost, immediate effect. Edit `build_generate_prompt()` in `src/superclaude/cli/roadmap/prompts.py`. ~30 lines of prompt text.
2. **Solution A (Traceability pass)**: Deterministic, high value. New file `src/superclaude/cli/roadmap/traceability.py` (~100 lines). New semantic check in `src/superclaude/cli/roadmap/gates.py`. Wire into executor step list in `src/superclaude/cli/roadmap/executor.py`.

### Phase 2: Near-term (v2.28)

3. **Solution E (Integration completeness LLM pass)**: New pipeline step. New prompt in `prompts.py`, new gate in `gates.py`, new step in `executor.py`. ~200 lines total.
4. **Solution C (Spec structural audit)**: Upstream guard. New file `src/superclaude/cli/roadmap/spec_structural_audit.py` (~80 lines). Wires into extraction step validation.

### Phase 3: Long-term (v2.29+)

5. **Solution B (Orphaned component detection)**: Highest complexity, requires robust NLP/heuristic parsing of roadmap text. May benefit from integration with Solution E's structured output as input.

---

## 5. Files to Modify / Create

### New files

| File | Solution | Purpose |
|------|----------|---------|
| `src/superclaude/cli/roadmap/traceability.py` | A | Deterministic FR-NNN cross-reference checker |
| `src/superclaude/cli/roadmap/spec_structural_audit.py` | C | Structural indicator counter for raw specs |
| `src/superclaude/cli/roadmap/orphan_detector.py` | B | Graph-based orphan component detector |

### Modified files

| File | Solution | Change |
|------|----------|--------|
| `src/superclaude/cli/roadmap/prompts.py` | D, E | Add integration constraint to generate prompt; add integration-audit prompt |
| `src/superclaude/cli/roadmap/gates.py` | A, E | Add `TRACEABILITY_GATE` and `INTEGRATION_AUDIT_GATE` with semantic checks |
| `src/superclaude/cli/roadmap/executor.py` | A, C, E | Wire new steps into `_build_steps()` |
| `src/superclaude/cli/roadmap/models.py` | A | Add `TraceabilityResult` if needed as pipeline state |

---

## 6. How Each Solution Would Have Caught the Specific Bug

| Solution | Would it have caught the dispatch wiring omission? | Confidence | Why |
|----------|---------------------------------------------------|------------|-----|
| A (Traceability) | YES, if extraction captured `FR-NNN` for dispatch | High (90%) | Deterministic ID matching; dispatch would be flagged as UNTRACED |
| B (Orphan detection) | YES, if roadmap mentioned step module names | Medium (70%) | Heuristic parsing may miss if roadmap uses abstract language |
| C (Structural audit) | YES | High (85%) | Spec's pseudocode block and `PROGRAMMATIC_RUNNERS` dict would inflate structural indicator count beyond extraction's requirement count |
| D (Prompt constraint) | LIKELY | Medium (75%) | Prompt explicitly names the dispatch-table pattern; but LLMs can still ignore instructions |
| E (Integration audit) | YES | High (90%) | Structured per-pair table forces explicit "name the wiring task" which would surface MISSING for step dispatch |

### Defense in depth

Running Solutions A + D + E together provides three independent checks:

1. **D** reduces the probability of the roadmap omitting the integration task (generation-time)
2. **A** catches it deterministically if the extraction captured the requirement ID (post-generation, deterministic)
3. **E** catches it via structured enumeration even if the ID was dropped (post-generation, LLM with structural constraint)

The probability of all three missing the same omission is the product of their individual miss rates: ~0.25 * 0.10 * 0.10 = 0.0025 (0.25%). Down from effectively 100% today.

---

## 7. Relationship to Existing Infrastructure

### What already exists and works

- **Extraction step** (`src/superclaude/cli/roadmap/prompts.py:58-127`): Produces `FR-NNN`, `NFR-NNN`, `SC-NNN` IDs. Solution A depends on this.
- **SPEC_FIDELITY_GATE** (`src/superclaude/cli/roadmap/gates.py:633-656`): LLM-based comparison with deterministic frontmatter enforcement. Solutions A and E augment this with deterministic and structured checks.
- **DEVIATION_ANALYSIS_GATE** (`src/superclaude/cli/roadmap/gates.py:712-758`): Routes deviations by class (SLIP, INTENTIONAL, PRE_APPROVED). Solutions A/E feed more accurate deviation data to this gate.
- **GateCriteria / SemanticCheck pattern** (`src/superclaude/cli/pipeline/models.py`): All new gates use this existing pattern. No new gate abstractions needed.
- **Pipeline executor** (`src/superclaude/cli/pipeline/executor.py`): Step insertion follows existing `Step(name=..., prompt_fn=..., gate=...)` pattern.

### What is broken and this fixes

- **Link 1 (Spec -> Roadmap)**: Currently entirely LLM-dependent. Solutions A and C add deterministic checks.
- **Completeness bias in generation**: Currently unmitigated. Solution D addresses at prompt level; Solution E addresses with structured post-generation audit.
- **"Looks complete" false confidence**: Currently no counter-signal. Solutions A/B/E all produce quantitative coverage metrics that expose gaps hiding behind structural completeness.

---

## 8. Open Questions

1. **ID stability**: Do extraction IDs remain stable across retries? If the extraction step produces different `FR-NNN` numbers on retry, Solution A's cross-reference breaks. May need content-hash-based matching as a fallback.

2. **Threshold calibration**: What traceability coverage threshold catches real bugs without blocking on noise? The 95% threshold in Solution A is a starting guess. Need shadow-mode data from 5-10 roadmap runs to calibrate.

3. **Integration audit prompt effectiveness**: Solution E relies on the LLM faithfully enumerating all producer-consumer pairs. If the same completeness bias makes the LLM skip pairs, the structured table alone may not be sufficient. May need to combine with Solution A's deterministic ID list as a forcing function: "Here are the 47 FR-NNN IDs. For each one, name the phase that implements it and the phase that integrates it."

4. **Pipeline cost**: Solutions A and C are sub-second. Solution E adds one LLM call (~60s, ~$0.10). Solution B adds significant parsing complexity. The Phase 1 set (A + D) adds near-zero latency and zero LLM cost.

5. **False positive rate**: How often will the traceability check flag IDs that are legitimately deferred or out-of-scope? Need an escape hatch (e.g., `deferred_ids` field in extraction frontmatter) to prevent the gate from blocking on intentional omissions.

# Anti-Instinct #03: Local Coherence Trap Mitigation

## The LLM Tendency

**Local Coherence Over Global Consistency**: LLMs optimize each section to be internally logical rather than verifying cross-section dependencies. Each phase reads well on its own, but global consistency -- "does Phase 4's output actually get consumed by Phase 2's structure?" -- requires tracking cross-phase dependencies across thousands of tokens. This is exactly the kind of long-range dependency that attention mechanisms handle poorly. The result: components that are individually correct but collectively disconnected.

## The Evidence: cli-portify Bug

During cli-portify roadmap generation, a 10-phase roadmap was produced where:

- **Phase 2** defined an executor loop structure with step dispatch slots
- **Phases 4-7** implemented individual step implementations (preflight, execution, validation, rollback)
- **Phase 10** defined tests for the step implementations

Each phase was locally coherent -- the executor loop in Phase 2 had sensible dispatch logic, the step implementations in Phases 4-7 had correct internal structures, and the tests in Phase 10 exercised reasonable scenarios. But the step implementations from Phases 4-7 were **never wired into** the executor structure from Phase 2. No import, no registration, no dispatch connection. The roadmap described building both a frame and its contents, but never described connecting them.

This is the signature of the Local Coherence Trap: each phase's LLM generation window produced text that was self-consistent, but no mechanism verified that cross-phase data flow contracts were satisfied.

## Proposed Solutions

### Solution 1: Producer-Consumer Graph Extraction (Primary -- Recommended)

**Concept**: After each phase is generated, programmatically extract what it *produces* (exports, definitions, registrations) and what it *consumes* (imports, references, calls). Build an accumulated graph. After all phases complete, validate that every produced artifact has at least one consumer, and every consumed artifact has a producer.

**Implementation**:

```
src/superclaude/cli/roadmap/coherence_graph.py  (new module)
```

**Data structures**:

```python
@dataclass(frozen=True)
class PhaseArtifact:
    """A concrete deliverable produced or consumed by a phase."""
    phase_id: str           # e.g. "phase-2", "phase-4"
    artifact_name: str      # e.g. "StepExecutor.dispatch()", "preflight_step.py"
    artifact_type: str      # "module", "class", "function", "config", "schema"
    role: Literal["producer", "consumer"]

@dataclass
class CoherenceGraph:
    """Tracks producer-consumer relationships across phases."""
    artifacts: list[PhaseArtifact]

    def orphan_producers(self) -> list[PhaseArtifact]:
        """Artifacts produced but never consumed by any later phase."""
        ...

    def unsatisfied_consumers(self) -> list[PhaseArtifact]:
        """Artifacts consumed but never produced by any earlier phase."""
        ...

    def disconnected_pairs(self) -> list[tuple[PhaseArtifact, PhaseArtifact]]:
        """Producer-consumer pairs in different phases with no wiring phase between them."""
        ...
```

**Extraction strategy**: After each phase's output passes its gate, run a lightweight regex/heuristic pass over the generated markdown to extract:

1. **Producers** -- detected via patterns like:
   - "Create `X`", "Define `X`", "Implement `X`", "Add `X` module"
   - "Export `X`", "Register `X`", "Emit `X`"
   - Code blocks defining classes, functions, modules

2. **Consumers** -- detected via patterns like:
   - "Import `X`", "Use `X`", "Call `X`", "Wire `X` into"
   - "Consume `X`", "Read `X`", "Depend on `X`"
   - "Register with `X`", "Dispatch via `X`"

3. **Wiring actions** -- detected via patterns like:
   - "Connect `X` to `Y`", "Register `X` in `Y`"
   - "Wire `X` into `Y`'s dispatch table"
   - "Import `X` from phase N into `Y`"

**Validation pass** (runs after all phases complete):

```python
def validate_coherence(graph: CoherenceGraph) -> CoherenceReport:
    """Post-generation validation of cross-phase data flow.

    Checks:
    1. No orphan producers (built but never used)
    2. No unsatisfied consumers (used but never built)
    3. No disconnected pairs (built in Phase N, used in Phase M,
       but no wiring step connects them)
    """
```

**Integration point**: Add as a new gate after the merge step in the roadmap pipeline executor (`src/superclaude/cli/roadmap/executor.py`). This gate is non-blocking (TRAILING mode) in v1 -- it emits warnings rather than failing the pipeline, allowing iterative tightening.

**How it would have caught the cli-portify bug**: The graph would have shown:
- Phase 2 *consumes* `preflight_step`, `execution_step`, `validation_step`, `rollback_step` (the executor dispatches to them)
- Phases 4-7 *produce* `preflight_step`, `execution_step`, `validation_step`, `rollback_step`
- **No phase** contains a wiring action connecting the Phase 4-7 productions to the Phase 2 consumer
- Result: `disconnected_pairs()` returns 4 pairs, each flagged as "producer exists, consumer exists, no wiring phase bridges them"

---

### Solution 2: Accumulated Deliverable Manifest Injection

**Concept**: Before generating each phase, inject a structured manifest of all deliverables produced by prior phases into the prompt. This gives the LLM visibility into what already exists, making it more likely to reference and wire prior outputs.

**Implementation**:

```
src/superclaude/cli/roadmap/manifest.py  (new module)
Changes to: src/superclaude/cli/roadmap/prompts.py (inject manifest into prompts)
Changes to: src/superclaude/cli/roadmap/executor.py (build manifest between phases)
```

**Manifest format** (injected into each phase's prompt):

```markdown
<prior_phase_deliverables>
## Deliverables from completed phases

### Phase 2: Executor Framework
- PRODUCED: `StepExecutor` class with `dispatch(step_name)` method
- PRODUCED: `StepRegistry` mapping step names to handler functions
- EXPECTS_WIRING: Step handlers for "preflight", "execute", "validate", "rollback"

### Phase 3: Configuration
- PRODUCED: `PipelineConfig` dataclass with step ordering
- PRODUCED: `StepConfig` per-step timeout and retry settings

YOU MUST explicitly wire any new deliverables into the structures above.
If you produce a step handler, you MUST describe how it is registered in StepRegistry.
</prior_phase_deliverables>
```

**Extraction**: After each phase passes its gate, parse its output for deliverable declarations (same heuristics as Solution 1) and append to the running manifest.

**Prompt injection**: The manifest is embedded in the prompt for the next phase via the existing `_embed_inputs()` mechanism in `executor.py`, but as structured context rather than a raw file.

**How it would have caught the cli-portify bug**: Phase 4's prompt would have included the manifest showing Phase 2's `StepRegistry` with `EXPECTS_WIRING: Step handlers for "preflight"...`. The LLM, seeing this explicit expectation, would be far more likely to include wiring instructions. This is a prevention-first approach (make it hard to produce the bug) rather than detection-after-the-fact.

**Limitation**: This is semi-deterministic. It improves the probability of correct wiring but does not guarantee it. The LLM may still ignore the manifest. Must be paired with Solution 1's post-hoc validation.

---

### Solution 3: Phase Output-Input DAG with Dangling Node Detection

**Concept**: Each pipeline step declares its expected inputs and outputs in structured metadata. Build a DAG from these declarations. After generation, validate that every declared output is consumed by some step's declared input, and every declared input is satisfied by some step's declared output.

**Implementation**:

```
Changes to: src/superclaude/cli/pipeline/models.py (extend Step with declared_inputs/outputs)
New file: src/superclaude/cli/roadmap/phase_dag.py
```

**Step extension**:

```python
@dataclass
class Step:
    # ... existing fields ...
    declared_outputs: list[str] = field(default_factory=list)  # artifact names this step produces
    declared_inputs: list[str] = field(default_factory=list)   # artifact names this step requires
```

**DAG validation**:

```python
def validate_phase_dag(steps: list[Step]) -> DAGReport:
    """Build DAG from step declarations and find:
    1. Dangling outputs: produced but never consumed
    2. Dangling inputs: consumed but never produced
    3. Disconnection gaps: output in step N, input in step M,
       with no integration step between N and M
    """
```

**How it would have caught the cli-portify bug**: Steps would declare:
- Phase 2: `declared_inputs=["preflight_handler", "execute_handler", ...]`
- Phase 4: `declared_outputs=["preflight_handler"]`
- No phase declares both a Phase-4 output and a Phase-2 input in its wiring
- DAG validation flags: "Phase 2 requires `preflight_handler`, Phase 4 produces it, but no phase wires them"

**Trade-off**: Requires upfront declaration of inputs/outputs for each step, which adds complexity to step definition. Best suited for roadmaps generated from specs where the deliverable graph is known before generation begins.

---

### Solution 4: Cross-Phase Integration Test Synthesis

**Concept**: After all phases are generated, programmatically synthesize integration test specifications that verify cross-phase wiring. These tests become a new phase appended to the roadmap.

**Implementation**:

```
New file: src/superclaude/cli/roadmap/integration_synth.py
Changes to: src/superclaude/cli/roadmap/executor.py (add synthesis step)
```

**Synthesis logic**:

```python
def synthesize_integration_tests(
    phases: list[PhaseOutput],
    coherence_graph: CoherenceGraph,
) -> list[IntegrationTest]:
    """For each producer-consumer pair across phases, generate a test spec:

    - Test that the producer's output type matches the consumer's expected input type
    - Test that the consumer can locate/import the producer's artifact
    - Test that the wiring code (if any) correctly connects them
    """
```

**How it would have caught the cli-portify bug**: Would generate tests like:
- "Verify `StepExecutor.dispatch('preflight')` resolves to `preflight_step.execute()`"
- "Verify `StepRegistry` contains entries for all step names defined in Phases 4-7"
- These test specifications would either expose the missing wiring during manual review, or (if executed) would fail immediately.

---

## Recommended Implementation Plan

### Phase A: Solution 1 (Detection) -- High Priority

Implement the Producer-Consumer Graph as a post-generation validation gate. This is the most deterministic and catches the problem with zero LLM involvement.

**Files to create/modify**:
- `src/superclaude/cli/roadmap/coherence_graph.py` (new)
- `src/superclaude/cli/roadmap/coherence_extractor.py` (new -- regex/heuristic extraction)
- `src/superclaude/cli/roadmap/gates.py` (add COHERENCE_GATE)
- `src/superclaude/cli/roadmap/executor.py` (wire coherence pass after merge)
- `tests/roadmap/test_coherence_graph.py` (new)

**Gate definition**:

```python
COHERENCE_GATE = GateCriteria(
    required_frontmatter_fields=["orphan_producers", "unsatisfied_consumers", "disconnected_pairs"],
    min_lines=10,
    enforcement_tier="STANDARD",  # TRAILING in v1, promote to STRICT once validated
    semantic_checks=[
        SemanticCheck(
            name="no_disconnected_pairs",
            check_fn=_no_disconnected_pairs,
            failure_message="Cross-phase deliverables produced but never wired into consumers",
        ),
    ],
)
```

### Phase B: Solution 2 (Prevention) -- Medium Priority

Add manifest injection to make the LLM aware of prior phase outputs. This is complementary to Solution 1 -- prevention reduces the frequency of the bug, detection catches what slips through.

**Files to modify**:
- `src/superclaude/cli/roadmap/manifest.py` (new)
- `src/superclaude/cli/roadmap/prompts.py` (inject manifest block)
- `src/superclaude/cli/roadmap/executor.py` (build manifest incrementally)

### Phase C: Solution 3 (Structural) -- Low Priority, High Value Long-Term

Extend the Step model with declared inputs/outputs. This requires more upfront work but enables the most rigorous validation. Best deferred until the roadmap spec format stabilizes.

---

## Relationship to Existing Infrastructure

The codebase already has strong primitives for this kind of analysis:

- **`src/superclaude/cli/pipeline/dataflow_graph.py`**: Already implements a DataFlowGraph with birth/write/read nodes, dead write detection, and cross-milestone edge tracking. Solution 1's CoherenceGraph is architecturally analogous but operates at the phase-deliverable level rather than the state-variable level.

- **`src/superclaude/cli/pipeline/dataflow_pass.py`**: Already runs a post-generation data flow tracing pass (M4) with contract extraction and conflict detection. The coherence graph can reuse the same pipeline integration pattern.

- **`src/superclaude/cli/pipeline/deliverables.py`**: Already classifies deliverables as behavioral/non-behavioral and decomposes them. The coherence extractor can leverage the same `is_behavioral()` heuristic to identify producer deliverables.

- **`src/superclaude/cli/pipeline/conflict_detector.py`** and **`contract_extractor.py`**: Already extract implicit contracts between deliverables. The coherence graph extends this from "do the contracts match?" to "are the contracts wired at all?"

- **`src/superclaude/cli/roadmap/gates.py`**: Already defines semantic checks as pure functions. The coherence gate follows the same pattern -- pure `content -> bool` functions registered on a `GateCriteria` instance.

The key insight is that the existing infrastructure validates *intra-phase* quality (frontmatter fields, heading structure, convergence scores) but lacks *inter-phase* coherence validation. Solutions 1-4 fill this gap.

## Success Criteria

The mitigation is successful when:

1. The cli-portify bug pattern (Phase N produces X, Phase M consumes X, no wiring exists) is detected automatically with zero false negatives on the original failing roadmap
2. False positive rate on valid roadmaps is below 10% (tuned via extraction heuristic thresholds)
3. The coherence gate adds less than 5 seconds to pipeline runtime (pure Python, no LLM calls)
4. The manifest injection (Solution 2) demonstrably reduces the frequency of disconnection bugs in A/B testing against the baseline prompt set

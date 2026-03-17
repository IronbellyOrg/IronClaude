# Adversarial Debate 02: End-to-End Call Path Task Verification (B5)

**Date**: 2026-03-17
**Proposal**: Brainstorm 02, Solution B5 -- End-to-End Call Path Task Verification
**Scoring Framework**: `/scoring-framework.md` (5-dimension weighted formula)
**Forensic Reference**: `/docs/generated/cli-portify-executor-noop-forensic-report.md`

---

## Proposal Summary

For every user-facing entry point defined in the roadmap, trace the expected call path through the architecture to the leaf implementation. Verify the tasklist contains at least one task per call-path segment. If any segment has no task, the gate fails.

- **Example**: `run_portify()` call path = `commands.py:run()` -> `run_portify()` -> `PortifyExecutor.run()` -> `_execute_step()` -> `step_runner()` -> `steps/*.py`. The tasklist covered segments 1-3 but not segments 4-5.
- **Integration**: New pipeline step after tasklist generation. LLM-prompted analysis. New `CALL_PATH_COVERAGE_GATE` at STRICT tier in `tasklist/gates.py`.

---

## Advocate Argument

### 1. Specific Bug Scenarios Caught

**The cli-portify no-op bug is the textbook case for this gate.** The forensic report (Section 6, "The Gap") documents two parallel development tracks that were never joined:

- **Track A**: Executor infrastructure -- `PortifyExecutor`, `STEP_REGISTRY` (metadata-only), `run()` loop, signal handling, resume logic, `run_portify()` entry point.
- **Track B**: Step implementations -- `steps/validate_config.py`, `steps/discover_components.py`, `steps/analyze_workflow.py`, and 5 other modules, plus standalone `execute_*()` functions in `executor.py` itself.

No tasklist in any of three releases (v2.24, v2.24.1, v2.25) contained a task connecting Track A to Track B. The call path verification gate would have traced the `run_portify()` entry point through its expected call chain:

```
Segment 1: commands.py:run() -> run_portify()        [TASKED: T10.01]
Segment 2: run_portify() -> PortifyExecutor.run()    [TASKED: T03.04]
Segment 3: PortifyExecutor.run() -> _execute_step()  [TASKED: T03.04 Step 4]
Segment 4: _execute_step() -> step_runner()           [UNTASKED]
Segment 5: step_runner() -> steps/*.py                [UNTASKED]
```

Segments 4 and 5 are UNTASKED. The gate fails. The pipeline halts. The "two parallel tracks never joined" failure is caught before a single line of code is written.

**Beyond cli-portify**, this gate catches an entire class of bugs documented in the forensic report Section 7:

- **DEVIATION_ANALYSIS_GATE** (Delta 2.2): fully defined in `roadmap/gates.py:712-758` but `_build_steps()` never includes a `deviation-analysis` step. A call path trace from `execute_roadmap()` -> `_build_steps()` -> `deviation-analysis` would flag the missing segment.
- **Trailing gate framework** (Delta 2.6): exists in `pipeline/trailing_gate.py` but `execute_sprint()` never calls it. Call path from `sprint entry` -> `execute_sprint()` -> `trailing_gate.evaluate()` would flag the untasked wiring.
- **SprintGatePolicy**: exists as a stub but is unwired. Same pattern.

The forensic report explicitly identifies "defined but not wired" as a recurring systemic pattern (Section 9, Systemic Root Cause). This gate is purpose-built for that exact pattern class.

**Silent no-op fallbacks are caught by construction.** When `_execute_step()` has a `None`-defaulting `step_runner` parameter, the call path analysis would model the `step_runner is not None` branch as the expected production path. The `else` branch (the no-op) would be flagged as a dead path that no task addresses. Even if the LLM does not catch the no-op semantics, the structural fact that no task covers "provide step_runner" is sufficient to fail the gate.

### 2. Integration Path into Existing Infrastructure

The gate integrates cleanly into the existing `GateCriteria`/`SemanticCheck` infrastructure:

**Pipeline placement**: New step in `src/superclaude/cli/tasklist/` inserted after tasklist generation completes and before (or as a component of) the `TASKLIST_FIDELITY_GATE`. This mirrors how `SPEC_FIDELITY_GATE` runs after roadmap generation -- same architectural pattern, different pipeline phase.

**Gate definition**: A new `CALL_PATH_COVERAGE_GATE` in `tasklist/gates.py` following the established pattern:

```python
CALL_PATH_COVERAGE_GATE = GateCriteria(
    name="call-path-coverage",
    tier=GateTier.STRICT,
    required_fields=["entry_points_analyzed", "segments_covered", "segments_untasked"],
    semantic_checks=[
        SemanticCheck(
            name="no_untasked_segments",
            check_fn=_untasked_segments_zero,
            severity="HIGH",
        ),
    ],
)
```

**Prompt design**: A new `build_call_path_prompt()` in `tasklist/prompts.py` takes the roadmap (for entry point and architecture extraction) and the tasklist files (for task coverage verification). The LLM outputs structured YAML with per-entry-point segment analysis. The deterministic `_untasked_segments_zero` semantic check validates the LLM's output.

**This matches the existing two-layer pattern** (LLM analysis + deterministic enforcement) used by both `SPEC_FIDELITY_GATE` and `TASKLIST_FIDELITY_GATE`. No new infrastructure patterns are required. The `SemanticCheck` context extension (passing roadmap path alongside tasklist content) is already needed by proposals B1 and B4 from the same brainstorm -- the infrastructure change is shared.

### 3. Composability with the Other 4 Top Proposals

**With Brainstorm 01 (Requirement ID Cross-Referencing)**: B5 and ID cross-referencing operate at different levels and reinforce each other. ID cross-referencing catches requirements that are entirely absent from the roadmap (Link 1 failure). B5 catches requirements that survive into the roadmap but are incompletely decomposed into tasks (Link 2 failure). Together they create layered defense: a requirement must (a) appear in the roadmap AND (b) have all its call-path segments tasked. If the spec's three-way dispatch was tagged as FR-012, ID cross-referencing catches it at Link 1 if the roadmap drops FR-012. If FR-012 survives but the roadmap describes it vaguely as "implement executor," B5 catches the incomplete task decomposition at Link 2.

**With Brainstorm 03 (Smoke Test Gates)**: B5 verifies structural completeness (every segment is tasked). Smoke test gates verify behavioral correctness (the pipeline actually produces output). B5 is a static analysis that runs at tasklist-generation time, catching gaps before any code is written. Smoke tests run at release time, catching gaps that survived all prior gates. They are complementary in timing and mechanism -- structural prevention vs. behavioral detection.

**With Brainstorm 04 (Hybrid LLM+Deterministic Gates)**: B5's LLM-prompted call path extraction can feed its segment list into hybrid gate infrastructure. The deterministic layer validates the LLM's claims by checking that each "TASKED" segment actually has a matching task reference. This is the same hybrid pattern proposed in Brainstorm 04, applied to call-path analysis. B5's output (structured segment lists) becomes input for deterministic cross-referencing -- the proposals share infrastructure.

**With Brainstorm 05 (Link 3 Code Fidelity)**: B5 catches missing tasks before code is written (preventing the gap). Link 3 catches task-code divergence after code is written (detecting the gap post-hoc). They cover different temporal phases. B5 reduces the burden on Link 3 by ensuring tasks exist for all segments -- Link 3 then only needs to verify that existing tasks were implemented correctly, not that the right tasks exist.

**Composability score justification**: B5 directly strengthens 4 other proposals, provides infrastructure (call-path segment lists) reusable by hybrid gates and code fidelity checks, and operates at a unique temporal position (post-tasklist, pre-code) that no other proposal covers. This warrants a high composability score.

---

## Skeptic Argument

### 1. Failure Modes Where This Gate Would NOT Catch Bugs

**Failure mode 1: Roadmap does not describe call paths.** The B5 mechanism depends on the LLM extracting call-path segments from the roadmap's "architectural description or module dependency graph." But the cli-portify roadmap that caused the actual bug did NOT contain a module dependency graph or an explicit call chain. It said: "Implement executor: sequential execution only." The call path `commands.py -> run_portify() -> PortifyExecutor.run() -> _execute_step() -> step_runner() -> steps/*.py` is reconstructed from the spec and the code, not from the roadmap. If the roadmap is already lossy (which is the root cause of the bug), B5 is asking the LLM to trace a call path through a document that has already dropped the critical segments. The LLM would trace what the roadmap describes, not what the spec intended. It would find 3 segments, all tasked, and pass the gate.

This is the fundamental chicken-and-egg problem: B5 detects incomplete task decomposition relative to the roadmap's call paths, but if the roadmap itself is incomplete, B5 validates a truncated call path and declares victory. The bug enters at Link 1 (Spec -> Roadmap), and B5 operates at Link 2 (Roadmap -> Tasklist). It cannot catch what the roadmap never described.

**Failure mode 2: Granularity mismatch.** The proposal acknowledges this: "Should `_execute_step() -> step_runner()` be one segment or two?" In the cli-portify case, collapsing these into one segment ("executor executes steps") would pass the gate because T03.04 Step 4 says "execute each step." The bug is only caught if the LLM segments at the exact granularity where the gap appears. LLMs are not reliable at consistent segmentation -- they tend toward the same level of abstraction as the source document. If the roadmap describes execution abstractly, the LLM will segment abstractly, and the gap disappears.

**Failure mode 3: Semantically vague tasks cover segments.** Consider a tasklist task: "T03.04 Step 4: Sequential loop: iterate STEP_REGISTRY; execute each step." Does this task cover the `_execute_step() -> step_runner()` segment? A literal reading says yes -- "execute each step" covers "step execution." But the actual implementation of this task was a no-op. The gate checks that a task EXISTS for each segment, not that the task's acceptance criteria REQUIRE the specific wiring. A vague task description can cover any number of segments without actually addressing any of them substantively.

**Failure mode 4: Novel architectures without clear call paths.** Event-driven systems, plugin architectures, message queues, and other non-linear control flows do not have simple `A -> B -> C` call paths. The proposal models execution as a linear chain, which works for cli-portify's sequential pipeline but fails for async dispatchers, observer patterns, or dependency-injected systems. As the codebase evolves toward more sophisticated architectures, the linear call-path model becomes increasingly inadequate.

### 2. False Positive Scenarios

**False positive 1: Intentionally thin entry points.** Some CLI commands are intentionally simple wrappers: `superclaude doctor` just calls `run_doctor()` which prints diagnostics. The "call path" is two segments. If the LLM over-segments this into `cli.py -> commands.py -> doctor.py -> _check_installation() -> _check_plugin() -> _check_mcp()`, it demands tasks for each internal function, flagging a simple command as having untasked segments. The gate cannot distinguish "intentionally simple" from "accidentally incomplete."

**False positive 2: Cross-release call paths.** The cli-portify executor was built across v2.24, v2.24.1, and v2.25. Each release's tasklist covers only that release's scope. B5 would analyze a single release's tasklist against the full call path from the roadmap, flagging segments that were completed in prior releases as UNTASKED. This produces false positives for any incremental/multi-release feature development.

**False positive 3: Refactoring changes call paths.** When a release refactors the call chain (e.g., extracting a method, introducing an intermediate dispatcher), the roadmap describes the new architecture but the tasklist decomposes the work by refactoring concern, not by call-path segment. The gate would flag "missing" segments that are covered implicitly by refactoring tasks like "extract _dispatch_step from _execute_step" -- the task covers the segment but does not name it using the roadmap's terminology.

### 3. Maintenance Burden Over 5+ Releases

**Prompt maintenance**: The `build_call_path_prompt()` must be updated whenever:
- New entry point patterns are added (API endpoints, webhook handlers, scheduled tasks)
- Architecture patterns change (the current prompt assumes linear call chains)
- Segmentation granularity expectations shift based on past false positive/negative experience

This is not a "set and forget" prompt. LLM-prompted analysis requires ongoing calibration. The existing `build_spec_fidelity_prompt()` has already been revised at least once (to add the 5-dimension comparison structure), and B5's prompt is more complex because it must handle variable-depth call graphs.

**Segmentation drift**: Over 5+ releases, the "right" segmentation granularity will shift. Early releases may need fine-grained segments (to catch cli-portify-style gaps). Later releases, after the team learns to write integration tasks, may need coarser segments (to reduce false positives). This requires threshold tuning -- how many segments is "enough"? The initial calibration will not remain correct.

**LLM cost scaling**: Each user-facing entry point requires a separate call-path trace. As the CLI grows (currently 30+ commands), the LLM cost scales linearly with entry point count. At 50 entry points with average 5-segment call paths, this is a substantial analysis that adds latency to every tasklist generation run.

**Gate version coupling**: The `CALL_PATH_COVERAGE_GATE` validates the tasklist against the roadmap's architecture. If the roadmap format changes (new section headers, different dependency graph notation), the gate's LLM prompt must be updated in lockstep. This creates a coupling between the roadmap generation prompt and the tasklist gate prompt that must be maintained across releases.

### 4. Whether Simpler Alternatives Achieve the Same Benefit

**Alternative 1: B3 (Acceptance Criteria Wiring Keyword Audit)** achieves 70% of B5's benefit at 10% of the cost. B3 scans acceptance criteria for wiring keywords ("imports," "calls," "dispatches to"). It would have flagged that T03's acceptance criteria lacked wiring verification language. It is purely deterministic (regex keyword scan), requires no LLM calls, has near-zero maintenance burden, and catches the exact failure mode from the forensic report. B5 adds call-path tracing on top, but the marginal bug-catching improvement over B3 is small relative to the complexity increase.

**Alternative 2: B1 (Deliverable-to-Task Traceability Matrix) + A1 (ID Cross-Reference)** provides layered coverage without call-path analysis. A1 catches dropped requirements at Link 1. B1 catches dropped deliverables at Link 2. Together they ensure every spec requirement appears in the roadmap and every roadmap deliverable appears in the tasklist. The cli-portify bug's "missing dispatch wiring" would be caught at Link 1 (A1) before B5 ever runs.

**Alternative 3: Brainstorm 05 (Link 3 Code Fidelity)** catches the bug at code time, which is later but more definitive. A code fidelity gate that checks "does the code satisfy the task's acceptance criteria" would catch the no-op executor regardless of whether the call path was tasked. It operates on concrete code rather than projected call paths, making it less susceptible to LLM segmentation errors.

The combination of B3 + A1 + Link 3 covers the same failure modes as B5 with less LLM dependency, less maintenance, and more deterministic checking. B5's unique contribution -- pre-code structural completeness verification -- is a "nice to have" rather than a "must have" when these simpler alternatives are in place.

---

## Scoring

### Advocate Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Likelihood to Succeed** | 8 | Would catch cli-portify segments 4-5 as UNTASKED. Catches the "defined but not wired" pattern class. Requires LLM to correctly segment the call path, which adds 1 assumption -- hence 8 not 9. |
| **Implementation Complexity** | 4 | New pipeline step, new prompt function, new gate definition, LLM-prompted analysis. Estimated 300-500 lines of production code across prompts.py, gates.py, and a new call_path.py module. Requires SemanticCheck context extension (shared with B1/B4). Score 4 = 500-1000 line range with cross-module changes. |
| **False Positive Risk** | 5 | LLM segmentation varies. Cross-release features trigger false positives. Intentionally simple commands may be over-segmented. Threshold tuning needed. Override via gate tier demotion available but coarse. |
| **Maintainability** | 5 | Prompt requires updates as architecture patterns evolve. Segmentation calibration drifts. LLM cost scales with entry point count. But gate auto-discovers entry points from roadmap -- no manual configuration per release. |
| **Composability** | 9 | Directly strengthens A1, B1, Brainstorm 03, Brainstorm 04, and Brainstorm 05. Provides reusable call-path segment infrastructure. Operates at unique temporal position (post-tasklist, pre-code). |

**Advocate Weighted Score**: (8 * 0.35) + (4 * 0.25) + (5 * 0.15) + (5 * 0.15) + (9 * 0.10) = 2.80 + 1.00 + 0.75 + 0.75 + 0.90 = **6.20**

### Skeptic Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Likelihood to Succeed** | 5 | The chicken-and-egg problem is severe: B5 validates against the roadmap, but the roadmap was already incomplete. LLM segmentation is unreliable. Vague tasks can cover segments nominally. Would catch some instances but has known blind spots depending on LLM quality and roadmap detail level. |
| **Implementation Complexity** | 3 | Underestimates complexity. The call-path tracing prompt is non-trivial to design and test. Integration testing requires mock roadmaps with varying architecture styles. Prompt tuning for segmentation granularity is iterative. Closer to 500-1000 lines with significant test fixture investment. |
| **False Positive Risk** | 4 | Cross-release features, intentionally thin commands, and refactoring tasks all trigger false positives. The gate requires tuning and possibly whitelisting. Probabilistic (LLM) checks amplify false positive risk. |
| **Maintainability** | 4 | Prompt drift is real. Segmentation calibration is ongoing. LLM cost scales linearly. Gate-roadmap coupling requires coordinated updates. Not self-maintaining -- requires attention each release cycle. |
| **Composability** | 7 | Complements other proposals but does not uniquely enable them. A1+B1+B3 achieve similar layered coverage without B5. The call-path segment list is useful but not required by other gates. Score 7 = complements 1-2 gates; outputs can be consumed downstream. |

**Skeptic Weighted Score**: (5 * 0.35) + (3 * 0.25) + (4 * 0.15) + (4 * 0.15) + (7 * 0.10) = 1.75 + 0.75 + 0.60 + 0.60 + 0.70 = **4.40**

---

## Tiebreaker Analysis

Scores differ by >2 on the following dimensions:

### Likelihood to Succeed: Advocate 8 vs. Skeptic 5 (delta = 3)

**Tiebreaker rationale**: The Advocate's core claim -- that B5 would flag segments 4-5 as UNTASKED -- holds only if the LLM correctly segments the call path at the right granularity AND the roadmap provides enough architectural detail for the LLM to construct the call path. The Skeptic's chicken-and-egg argument is valid: the actual cli-portify roadmap said "sequential execution with mocked steps," which does not describe segments 4-5. The LLM would trace 3 segments from the roadmap's text, find all 3 tasked, and pass the gate.

However, the Advocate's point about the "defined but not wired" pattern class is stronger. For future bugs where the roadmap DOES describe the architecture (but the tasklist drops a segment), B5 catches the gap. The cli-portify case is the worst case for B5, not the typical case.

**Tiebreaker score**: 6. Would catch the pattern class in most cases but would NOT have caught the specific cli-portify bug because the roadmap was already lossy at the point B5 operates.

### Implementation Complexity: Advocate 4 vs. Skeptic 3 (delta = 1)

No tiebreaker needed (delta <= 2).

### Composability: Advocate 9 vs. Skeptic 7 (delta = 2)

No tiebreaker needed (delta = 2, not >2).

---

## Final Scores

| Dimension | Weight | Advocate | Skeptic | Tiebreaker | Final |
|-----------|--------|----------|---------|------------|-------|
| Likelihood to Succeed | 0.35 | 8 | 5 | 6 | **6.0** |
| Implementation Complexity | 0.25 | 4 | 3 | -- | **3.5** |
| False Positive Risk | 0.15 | 5 | 4 | -- | **4.5** |
| Maintainability | 0.15 | 5 | 4 | -- | **4.5** |
| Composability | 0.10 | 9 | 7 | -- | **8.0** |

**Final Weighted Score**: (6.0 * 0.35) + (3.5 * 0.25) + (4.5 * 0.15) + (4.5 * 0.15) + (8.0 * 0.10) = 2.10 + 0.875 + 0.675 + 0.675 + 0.80 = **5.13**

### Interpretation

Score 5.13 falls in the **Conditional candidate** range (4.0-5.9): implement only if composability benefits justify it.

**Key takeaway**: B5's strength is its unique temporal position and composability with other proposals. Its weakness is the chicken-and-egg dependency on roadmap completeness -- it validates against a document that may already be lossy, which is the exact failure mode it aims to prevent. The Skeptic's argument that simpler alternatives (B3 + A1 + Link 3) cover the same failure modes with less complexity is compelling. B5 should be considered for implementation only after A1, B1, and B3 are in place, and only if those gates prove insufficient at catching incomplete task decomposition.

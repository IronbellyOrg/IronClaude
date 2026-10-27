# Adversarial Debate: Wiring Verification Gate (Static Import-Chain Analysis)

**Proposal**: A2 from brainstorm-05-link3-code-fidelity.md
**Date**: 2026-03-17
**Link Targeted**: Link 3 (Tasklist-to-Code)
**Scoring Framework**: scoring-framework.md (5-dimension weighted formula)

---

## Proposal Summary

After code is generated for a task, perform static analysis:

1. Parse all REGISTRY, DISPATCH, RUNNERS dictionary constants. Verify mapped values (function references) are importable.
2. Parse all `__init__` constructors with `Optional[Callable] = None` parameters. Flag any that are never explicitly provided in any call site.
3. Parse all files in `steps/` directories. Verify each exported function is imported by at least one consumer.
4. Detect no-op fallbacks: code paths where `None`-defaulting callable returns a success stub (`0`, `True`, `"SUCCESS"`).

Gate emits YAML report with `unwired_count`, `noop_fallback_count`, `orphan_module_count`. Passes when all are zero.

**Integration point**: New module `src/superclaude/cli/audit/wiring_gate.py`. Post-task-completion hook in sprint runner, or standalone audit.

---

## Advocate's Opening Argument

### 1. Specific Bug Scenarios Caught

The cli-portify executor no-op failure is the canonical case this gate was designed to catch. The forensic chain of failure was:

1. The spec defined three-way dispatch (`_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`).
2. The roadmap reduced this to "sequential execution with mocked steps" -- SPEC_FIDELITY_GATE did not catch it.
3. The tasklist faithfully reproduced the roadmap's incomplete executor -- TASKLIST_FIDELITY_GATE passed vacuously.
4. The code implemented a no-op default with `step_runner=None` -- no gate existed at this link.
5. Result: pipeline silently "succeeds" with all steps "completed" but no real work performed.

The Wiring Verification Gate would break this chain at link 4 through two independent detection mechanisms:

**Detection A -- Optional[Callable] = None never provided**: The gate parses constructor signatures across the codebase. When `executor.__init__(self, ..., step_runner: Optional[Callable] = None)` is found, the gate scans all call sites for the `Executor` class. If no call site ever passes an explicit `step_runner` argument, this is flagged as an unwired injectable. This is a deterministic, AST-level check with no LLM dependency.

**Detection B -- No-op fallback returning success**: The gate detects the pattern `if self.step_runner is None: return 0` (or `return True`, `return "SUCCESS"`). A callable that defaults to `None` and whose `None` branch returns a success value is a textbook no-op fallback. The cli-portify executor had exactly this pattern: when `step_runner` was `None`, `_execute_step()` returned success without executing anything.

Beyond the cli-portify case, this gate would catch:

- **DEVIATION_ANALYSIS_GATE defined but not wired** (Delta 2.2): The gate function exists in `roadmap/gates.py` but is never referenced in `_build_steps()`. The orphan-module check would flag this.
- **SprintGatePolicy stub** (Delta 2.6): `SprintGatePolicy` at `sprint/executor.py:47-90` was defined but its `build_remediation_step` and `files_changed` methods were stubs. The no-op fallback detector would flag methods that exist but return trivial values.
- **Future "Track A / Track B never joined" failures**: Any time two subsystems are developed independently and one team's dispatch table references functions from the other team's module without an actual import chain, the gate catches it.

### 2. Integration Path into Existing Infrastructure

The existing gate infrastructure in `src/superclaude/cli/pipeline/gates.py` already defines the `gate_passed(output_file, criteria)` pattern with tier-proportional enforcement (EXEMPT -> LIGHT -> STANDARD -> STRICT). The Wiring Verification Gate fits naturally as a STRICT-tier semantic check.

Concretely:

```python
# In src/superclaude/cli/audit/wiring_gate.py
def check_wiring(content: str) -> bool:
    """Semantic check: no unwired callables or no-op fallbacks."""
    ...

# Registered as a SemanticCheck on a GateCriteria instance
WIRING_GATE = GateCriteria(
    enforcement_tier="STRICT",
    min_lines=1,
    semantic_checks=[
        SemanticCheck(
            name="wiring_verification",
            check_fn=check_wiring,
            failure_message="Unwired callables or no-op fallbacks detected",
        ),
    ],
)
```

The `SemanticCheck` dataclass (`pipeline/models.py`) accepts any `check_fn: Callable[[str], bool]`. The wiring gate's analysis functions conform to this signature. No new infrastructure is needed -- only a new module providing the check functions and a `GateCriteria` constant.

For the sprint runner hook, `SprintGatePolicy` at `sprint/executor.py:47-90` already exists as the concrete `TrailingGatePolicy` implementation. The wiring gate can be invoked within `build_remediation_step` or as a pre-classification check after the Claude subprocess returns. The `TrailingGateRunner` infrastructure from `pipeline/trailing_gate.py` already supports deferred evaluation, so the wiring gate could run asynchronously without blocking the sprint loop.

### 3. Composability with Other Top Proposals

The Wiring Verification Gate composes well with the other proposals under debate:

- **A1 (Acceptance Criteria Extraction Gate)**: A1 handles semantic criteria ("pipeline runs end-to-end"), while A2 handles structural criteria ("all dispatch entries resolve to importable functions"). They are orthogonal and complementary -- A1 catches "wrong behavior" while A2 catches "no behavior wired at all."
- **A4 (Deliverable-ID Cross-Reference Gate)**: A4 verifies traceability IDs exist; A2 verifies the code behind those IDs is actually wired. A deliverable could pass A4 (file exists, ID present) while failing A2 (the module is orphaned, never imported).
- **B1 (Task-Scope Audit Gate)**: A2's check functions can be registered directly in B1's check catalog (`gate-check-catalog.yaml`) as `CHECK_CODE_WIRING` with severity `critical`.
- **B5 (Tasklist-Emitted Audit Metadata)**: When the tasklist emits `code_fidelity_checks` including `{type: "import_chain", target: "executor.py -> steps/*.py"}`, the A2 gate is the natural executor for that check type.

The gate's YAML output (`unwired_count`, `noop_fallback_count`, `orphan_module_count`) can also serve as input to other gates that need quantitative evidence of integration completeness.

### Advocate's Proposed Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Likelihood to Succeed | 9 | Deterministic AST analysis with two independent detection mechanisms for the exact cli-portify failure pattern. No LLM dependency. |
| Implementation Complexity | 6 | Estimated 300-400 lines: AST parsing, call-site scanning, pattern matching for no-op fallbacks, YAML report emission. One new module, but requires careful AST visitor implementation. |
| False Positive Risk | 6 | Intentional lazy imports, plugin architectures, and factory patterns may trigger false positives. Override mechanism (whitelist file) mitigates but adds configuration. |
| Maintainability | 7 | Auto-discovers patterns from code structure rather than requiring manual configuration. Naming convention heuristics ("REGISTRY", "DISPATCH") are the main fragility point. |
| Composability | 9 | Directly enables B1 CHECK_CODE_WIRING, feeds B5 import_chain checks, complements A1 and A4 without overlap. |

**Advocate's Weighted Score**: (9 * 0.35) + (6 * 0.25) + (6 * 0.15) + (7 * 0.15) + (9 * 0.10) = 3.15 + 1.50 + 0.90 + 1.05 + 0.90 = **7.50**

---

## Skeptic's Opening Argument

### 1. Failure Modes Where This Gate Would NOT Catch Bugs

The Advocate presents the wiring gate as a near-certain catch for the cli-portify failure. I challenge this on several fronts:

**Dynamic dispatch evasion**: Python is a dynamic language. The gate relies on AST-level analysis to find call sites that provide `step_runner`. But what if the caller uses `**kwargs`, `getattr()`, or a factory function? Consider:

```python
config = {"step_runner": some_function}
executor = Executor(**config)
```

The AST parser sees `**config` but cannot statically resolve whether `step_runner` is in that dict. The gate either misses this (false negative) or flags every `**kwargs` usage (false positive). In a codebase that uses configuration-driven dependency injection -- which this project does -- this is a real concern.

**No-op detection is pattern-fragile**: The gate detects `if self.step_runner is None: return 0`. But what about:

```python
if self.step_runner is None:
    logger.info("Step runner not configured, using default")
    return self._default_result()
```

Where `_default_result()` returns a `StepResult(status="SUCCESS", ...)`. The no-op is now indirected through a method call. The gate would need to follow call chains to detect this, turning a "simple static analysis" into a partial program analyzer. The Advocate's estimate of 300-400 lines is likely 600-800 once edge cases are handled.

**Cross-module boundaries**: The orphan-module check ("each exported function is imported by at least one consumer") scans `steps/` directories. But what if the consumer is in a different package, a CLI command definition, or a Markdown skill file that references a Python module by path string? The gate cannot trace references that live outside Python code.

**The actual cli-portify root cause was at Link 2, not Link 3**: The forensic report establishes that the spec's three-way dispatch was reduced at the Spec-to-Roadmap transition (Link 2). By the time code is generated, the tasklist already says "sequential execution with mocked steps." A wiring gate at Link 3 catches the symptom (no-op executor) but not the disease (roadmap reduced the spec). If the roadmap says "mock steps," then a properly wired mock-step executor passes the wiring gate while still doing nothing useful.

### 2. False Positive Scenarios

**Intentional Optional dependencies**: Many constructor patterns legitimately use `Optional[Callable] = None` for optional hooks:

```python
class Pipeline:
    def __init__(self, on_complete: Optional[Callable] = None):
        self._on_complete = on_complete

    def run(self):
        # ... actual work ...
        if self._on_complete:
            self._on_complete()
```

This is an event hook, not a dependency injection for core behavior. The gate would flag it as "unwired callable" because no call site provides `on_complete`. The developer must then add it to a whitelist, which erodes trust in the gate.

**Test fixtures and development helpers**: During development, functions in `steps/` may be defined but not yet consumed because they are being developed in a feature branch. The orphan-module check would block partially-complete work, forcing developers to wire consumers before implementing producers. This inverts the natural development flow.

**Plugin architecture patterns**: The `REGISTRY` and `DISPATCH` dictionaries may intentionally reference entry points that are resolved at runtime via `importlib` or `pkg_resources`. Static import-chain analysis flags these as unimportable, but they work correctly at runtime.

### 3. Maintenance Burden Over 5+ Releases

The gate's heuristics for recognizing "registry" and "dispatch" patterns depend on naming conventions. Today the codebase uses `REGISTRY`, `DISPATCH`, `RUNNERS`. If a future release introduces `HANDLER_MAP`, `STEP_TABLE`, or `ACTION_LOOKUP`, the gate silently misses them (false negative). The maintainer must update the pattern list for each new naming convention.

The no-op fallback detector must track an evolving set of "success stub" return values. Currently `0`, `True`, `"SUCCESS"`. What about `StepStatus.PASS`, `ExitCode.OK`, `{"status": "success"}`? Each new return type requires a heuristic update.

Over 5 releases, the gate accumulates exceptions (whitelisted Optional[Callable] parameters, known plugin registries, approved no-op patterns). The whitelist itself becomes a maintenance burden and a source of false confidence -- if an entry is whitelisted and later becomes a genuine bug, the gate silently passes.

AST parsing is also sensitive to Python version changes. Between Python 3.10 and 3.13, the AST module has had breaking changes in how type annotations are represented (PEP 604 union types, PEP 695 type aliases). The gate's AST visitors must be updated for each Python version the project supports.

### 4. Simpler Alternatives

**Alternative 1: Required integration test per task**. Instead of static analysis, require each task that touches dispatch tables or dependency injection to include a test that instantiates the full call chain and asserts non-trivial execution. This catches everything the wiring gate catches (and more), costs zero maintenance on the gate side, and produces no false positives because the test author defines what "wired correctly" means.

**Alternative 2: Ban `Optional[Callable] = None` by convention**. A linting rule that forbids `Optional[Callable]` constructor parameters in executor classes forces the developer to provide an explicit function at every call site. This is cheaper than a gate (a single ruff rule), catches the exact pattern, and has zero false positives because it is a style constraint, not a semantic analysis.

**Alternative 3: Smoke test (Proposal A3)**. Running the actual CLI command against a minimal fixture catches no-op behavior with higher confidence than static analysis, because it tests runtime behavior rather than code structure. A 5-line smoke test (`assert execution_time > 1s`) catches the cli-portify bug without any AST parsing infrastructure.

### Skeptic's Proposed Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Likelihood to Succeed | 6 | Would catch the specific cli-portify pattern in its literal form, but Python's dynamic nature creates blind spots. The root cause was at Link 2, not Link 3; this gate catches the symptom. |
| Implementation Complexity | 4 | Realistic estimate is 500-800 lines once edge cases for dynamic dispatch, `**kwargs`, indirected no-ops, and Python version compatibility are handled. Requires non-trivial AST visitor infrastructure. |
| False Positive Risk | 5 | Intentional Optional hooks, plugin registries, and in-progress feature branches will generate false positives requiring a whitelist system. |
| Maintainability | 5 | Naming convention heuristics, success-stub patterns, and whitelist files all require manual updates per release. AST compatibility across Python versions adds ongoing burden. |
| Composability | 8 | Genuinely strong composability with B1 and B5. Outputs are well-structured. Slightly lower than Advocate because overlap with A3 (smoke test) means one may make the other redundant. |

**Skeptic's Weighted Score**: (6 * 0.35) + (4 * 0.25) + (5 * 0.15) + (5 * 0.15) + (8 * 0.10) = 2.10 + 1.00 + 0.75 + 0.75 + 0.80 = **5.40**

---

## Advocate's Rebuttal

The Skeptic raises valid concerns about dynamic dispatch, but overstates their impact in this specific codebase. Examining the actual code at `src/superclaude/cli/sprint/executor.py`, the project uses straightforward constructor injection with explicit keyword arguments -- not `**kwargs` spreading or `getattr()` dispatch. The executor pattern is:

```python
class SprintGatePolicy:
    def __init__(self, config: SprintConfig) -> None:
```

This is standard, statically-analyzable Python. The gate does not need to solve the general program analysis problem; it needs to work for this codebase's actual patterns.

On the "root cause was at Link 2" argument: this is true, but irrelevant to the gate's value. The fidelity chain has four links, and a failure at any one link should be caught. The fact that Link 2 also failed does not diminish the value of catching the failure at Link 3. Defense in depth requires gates at every link.

On maintenance burden: the Skeptic's estimate of "500-800 lines" assumes comprehensive edge-case handling that is not required for an initial deployment. The gate can start with the literal patterns present in this codebase (REGISTRY, DISPATCH, RUNNERS; `Optional[Callable] = None`; `return 0/True/"SUCCESS"`) and extend incrementally. A shadow-mode rollout (Proposal B4) provides the data collection phase to tune heuristics before enforcement.

On simpler alternatives: banning `Optional[Callable] = None` by convention is a linting rule, not a gate. It prevents one pattern but does not detect unwired registries, orphan modules, or existing violations. Integration tests per task are excellent but require someone to write them -- the wiring gate catches the case where no one did.

### Advocate's Adjusted Scores

No changes. The Skeptic's concerns are mitigable, not fundamental.

---

## Skeptic's Rebuttal

The Advocate's rebuttal concedes that the gate works "for this codebase's actual patterns" and can "start with literal patterns." This is precisely the maintenance concern: a gate calibrated to today's patterns will need recalibration as patterns evolve. The initial 300-400 line estimate was for a pattern-specific scanner; the Advocate is now arguing for that scope, which supports my lower Likelihood to Succeed score (it catches today's patterns but may miss tomorrow's).

The "defense in depth" argument is valid, but it cuts both ways: if Link 2 is properly gated (via Proposal B3, DEVIATION_ANALYSIS_GATE wiring), the Link 3 wiring gate catches only the residual failures that survive an upstream fix. The marginal value decreases as upstream gates improve.

I concede the composability point -- A2's YAML output and check-function interface genuinely serve as infrastructure for B1 and B5.

### Skeptic's Adjusted Scores

I revise Implementation Complexity from 4 to 5, acknowledging the Advocate's point that initial scope can be narrower than worst-case. Other scores unchanged.

---

## Tiebreaker Rationale

Scores differ by >2 on two dimensions:

### Likelihood to Succeed: Advocate 9, Skeptic 6 (delta: 3)

**Tiebreaker**: The Advocate is correct that the gate would catch the literal cli-portify pattern through two independent mechanisms. The Skeptic is correct that dynamic dispatch creates blind spots. However, the scoring rubric asks "would this gate actually catch the cli-portify no-op bug?" -- and the answer is definitively yes for this specific case. The Skeptic's concern about future pattern drift is better captured in Maintainability. **Tiebreaker score: 8.** The gate catches this bug and most similar bugs but has edge cases in dynamic dispatch patterns.

### Implementation Complexity: Advocate 6, Skeptic 5 (delta: 1)

No tiebreaker needed (delta <= 2). Average: 5.5.

---

## Final Scoring

| Dimension | Weight | Advocate | Skeptic | Tiebreaker | Final |
|-----------|--------|----------|---------|------------|-------|
| Likelihood to Succeed | 0.35 | 9 | 6 | 8 | **8.0** |
| Implementation Complexity | 0.25 | 6 | 5 | -- | **5.5** |
| False Positive Risk | 0.15 | 6 | 5 | -- | **5.5** |
| Maintainability | 0.15 | 7 | 5 | -- | **6.0** |
| Composability | 0.10 | 9 | 8 | -- | **8.5** |

**Weighted Final Score**: (8.0 * 0.35) + (5.5 * 0.25) + (5.5 * 0.15) + (6.0 * 0.15) + (8.5 * 0.10)

= 2.80 + 1.375 + 0.825 + 0.90 + 0.85

= **6.75**

---

## Verdict

**Score: 6.75 -- Good candidate.** Implement after high-priority items.

The Wiring Verification Gate is a technically sound proposal with strong composability and a deterministic detection mechanism for the specific failure class that caused the cli-portify no-op bug. Its primary risks are maintenance burden from pattern heuristics and false positives from legitimate Optional[Callable] usage. These risks are mitigable through shadow-mode rollout (B4) and whitelist mechanisms, but they prevent it from reaching the "strong candidate" tier.

**Recommendation**: Implement as part of the B1 task-scope audit gate integration, starting with the narrow pattern set (REGISTRY/DISPATCH dictionary checks and Optional[Callable] = None call-site analysis). Defer the no-op fallback detector to a second iteration after shadow-mode data collection validates the heuristics. Pair with Proposal A3 (Smoke Test Gate) for runtime behavioral verification that complements the static structural checks.

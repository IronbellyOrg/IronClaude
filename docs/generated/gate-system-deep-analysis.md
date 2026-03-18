---
title: Gate System Deep Architecture Analysis
generated: 2026-03-18
scope: roadmap/gates.py, roadmap/executor.py, cleanup_audit/gates.py, pipeline/gates.py, pipeline/models.py
focus: GateCriteria schema, SemanticCheck interface, gate registration, extension points
---

# Gate System Deep Architecture Analysis

## 1. Schema Map

### `GateCriteria` (`pipeline/models.py:68-74`)

```
GateCriteria
├── required_frontmatter_fields: list[str]   # YAML keys that must exist
├── min_lines: int                           # Minimum output length
├── enforcement_tier: STRICT|STANDARD|LIGHT|EXEMPT
└── semantic_checks: list[SemanticCheck] | None
```

### `SemanticCheck` (`pipeline/models.py:59-64`)

```
SemanticCheck
├── name: str                        # Human-readable identifier
├── check_fn: Callable[[str], bool]  # Pure function: content -> pass/fail
└── failure_message: str             # Reason string on failure
```

The interface contract: `check_fn` receives raw file content as a string and returns `bool`. No side effects, no I/O -- pure functions only. Enforced by convention (docstring in `roadmap/gates.py:7-9`), not by the type system.

---

## 2. Gate Enforcement: Tiered Cascade (`pipeline/gates.py:20-74`)

The `gate_passed()` function implements a strict cascade:

| Tier         | Checks Applied                                    |
|--------------|---------------------------------------------------|
| **EXEMPT**   | Always passes                                     |
| **LIGHT**    | File exists + non-empty                           |
| **STANDARD** | + min_lines + required frontmatter fields         |
| **STRICT**   | + all semantic checks must return `True`           |

Each tier is a superset of the previous. Short-circuit exits at each tier boundary (lines 42, 62).

---

## 3. Gate Registration in `_build_steps()` (`roadmap/executor.py:344-476`)

Gates are **statically wired** -- each `Step` receives its `GateCriteria` constant at construction time via the `gate=` parameter. There is **no dynamic registry**, no lookup table, no registration mechanism. The binding is:

```python
Step(id="extract",        gate=EXTRACT_GATE,        ...)   # line 386
Step(id="generate-*",     gate=GENERATE_A_GATE,     ...)   # line 397
Step(id="generate-*",     gate=GENERATE_B_GATE,     ...)   # line 406
Step(id="diff",           gate=DIFF_GATE,           ...)   # line 419
Step(id="debate",         gate=DEBATE_GATE,         ...)   # line 429
Step(id="score",          gate=SCORE_GATE,           ...)   # line 439
Step(id="merge",          gate=MERGE_GATE,           ...)   # line 449
Step(id="test-strategy",  gate=TEST_STRATEGY_GATE,  ...)   # line 459
Step(id="spec-fidelity",  gate=SPEC_FIDELITY_GATE,  ...)   # line 469
```

**Notable**: `DEVIATION_ANALYSIS_GATE`, `REMEDIATE_GATE`, and `CERTIFY_GATE` are defined in `roadmap/gates.py` (lines 885, 831, 856) and listed in `ALL_GATES` but **not wired** into `_build_steps()`. They exist for reference and are imported by `certify_prompts.py`, suggesting they are spec'd but not yet operational in the main pipeline.

---

## 4. Pipeline Extension Points

There are **four distinct insertion points** for a new gate step:

### A. Inline in `_build_steps()` (primary)

Add a new `Step(...)` entry to the `steps` list. Position determines execution order. This is how all current 8 steps are wired.

**Insertion location**: After `spec-fidelity` (line 473), before `return steps` (line 476):

```python
Step(
    id="deviation-analysis",
    prompt=build_deviation_analysis_prompt(...),
    output_file=out / "deviation-analysis.md",
    gate=DEVIATION_ANALYSIS_GATE,
    timeout_seconds=600,
    inputs=[spec_fidelity_file, merge_file],
    retry_limit=1,
),
```

### B. Post-merge validation chain (current architecture)

Steps 7-8 (`test-strategy`, `spec-fidelity`) already form a post-merge validation chain after the merge step (Step 6). A new gate appends to this chain. The three unwired gates (`DEVIATION_ANALYSIS_GATE`, `REMEDIATE_GATE`, `CERTIFY_GATE`) are designed for exactly this position -- extending the post-merge pipeline.

### C. Trailing gate mode (`pipeline/trailing_gate.py`)

Set `gate_mode=GateMode.TRAILING` on a `Step` to make its gate non-blocking. The `TrailingGateRunner` evaluates asynchronously via daemon threads; failures are collected at pipeline end (`executor.py:124-136`). Extension point for **expensive** validation that shouldn't block fast-path steps.

Key components:
- `TrailingGateRunner.submit()` -- spawns daemon thread for gate evaluation
- `TrailingGateRunner.wait_for_pending()` -- sync point at pipeline end
- `DeferredRemediationLog` -- persists failures for `--resume` recovery
- `TrailingGatePolicy` (Protocol) -- consumer hook for remediation step construction

### D. Parallel group insertion

Wrap multiple `Step` objects in a `list[Step]` within the `steps` list (see lines 392-413 for the generate group). A parallel validation gate group could run independent checks concurrently.

---

## 5. Cross-Pipeline Gate Reuse Pattern

The gate system supports **cross-pipeline reuse** via direct imports:

| Consumer                   | Imports From       | Reused Symbols                                         |
|----------------------------|--------------------|-------------------------------------------------------|
| `tasklist/gates.py`        | `roadmap/gates.py` | `_high_severity_count_zero`, `_tasklist_ready_consistent` |
| `roadmap/validate_gates.py`| `roadmap/gates.py` | `_frontmatter_values_non_empty`                        |
| `cleanup_audit/gates.py`   | `pipeline/models.py`| `GateCriteria`, `SemanticCheck` (types only)           |

Dependency direction is strictly **unidirectional**: domain gates -> pipeline models. Never reverse. `pipeline/` has zero imports from `roadmap/`, `sprint/`, `cleanup_audit/`, or `tasklist/` (NFR-007).

---

## 6. Cleanup Audit Gate Comparison

`cleanup_audit/gates.py` follows the same pattern but with structural differences:

| Aspect               | Roadmap Gates                      | Cleanup Audit Gates            |
|-----------------------|------------------------------------|-------------------------------|
| Collection type       | `ALL_GATES: list[tuple]`           | `ALL_GATES: dict[str, GateCriteria]` |
| Naming convention     | `EXTRACT_GATE`, `MERGE_GATE`       | `GATE_G001`, `GATE_G002`      |
| Semantic check scope  | Frontmatter arithmetic, cross-refs | Content pattern matching       |
| Import style          | `from ..pipeline.models import`    | `from superclaude.cli.pipeline.models import` (absolute) |
| Check function prefix | `_` (private)                      | No underscore (public)         |

The absolute import in `cleanup_audit/gates.py:14` is inconsistent with the relative imports used everywhere else.

---

## 7. Findings

| #  | Severity   | Finding                                                                                                                                                                                   |
|----|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | **Medium** | 3 gates defined but unwired: `DEVIATION_ANALYSIS_GATE`, `REMEDIATE_GATE`, `CERTIFY_GATE` exist in `roadmap/gates.py` (lines 885, 831, 856) and `ALL_GATES` but are never bound to any `Step` in `_build_steps()`. Dead code or incomplete feature. |
| 2  | **Low**    | `_build_steps()` imports 8 of 12 gate constants (lines 27-38). The 4 omitted (`DEVIATION_ANALYSIS_GATE`, `REMEDIATE_GATE`, `CERTIFY_GATE`, plus `TASKLIST_FIDELITY_GATE` in tasklist) confirm the remediation/certification pipeline is spec'd but not wired. |
| 3  | **Low**    | `cleanup_audit/gates.py:14` uses absolute import (`from superclaude.cli.pipeline.models`) while all other gate modules use relative imports (`from ..pipeline.models`). Inconsistency. |
| 4  | **Info**   | No dynamic gate registration mechanism exists. Adding gates requires editing `_build_steps()` directly. Intentional simplicity but limits runtime extensibility.                          |
| 5  | **Info**   | `ALL_GATES` in `roadmap/gates.py:934-947` is a pipeline-order reference list but is never consumed programmatically. Could be used to auto-build steps if a registry pattern were desired. |

---

## 8. Answer: Where Does a New Gate Step Plug In?

### Primary path (5 steps)

1. **Define** the `GateCriteria` constant in `roadmap/gates.py` with semantic check functions
2. **Define** the prompt builder in `roadmap/prompts.py` (or dedicated module)
3. **Import** both into `roadmap/executor.py`
4. **Add** a `Step(...)` entry in `_build_steps()` at line 473, with `gate=YOUR_GATE`
5. **Update** `_get_all_step_ids()` (line 538) and `ALL_GATES` list (line 934)

### Concrete example: wiring `DEVIATION_ANALYSIS_GATE`

Step 1 is already done (`roadmap/gates.py:885-931`). The gate defines 6 semantic checks covering frontmatter consistency, routing ID validation, and slip-count arithmetic. Steps 2-5 remain to make it operational.

### Alternative paths

- **Non-blocking gate**: Add `gate_mode=GateMode.TRAILING` to the `Step` constructor + ensure `grace_period > 0` in config
- **Parallel validation**: Wrap the new step in a `list[Step]` group with other independent validation steps
- **Cross-pipeline reuse**: Import semantic check functions from `roadmap/gates.py` into another pipeline's gate module (pattern established by `tasklist/gates.py`)

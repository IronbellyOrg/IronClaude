# BF-2 Resolution: Remove SPEC_FIDELITY_GATE from Convergence Flow

## Selected Solution

**Solution B** -- Remove SPEC_FIDELITY_GATE from the convergence flow entirely. The convergence engine uses only the DeviationRegistry for pass/fail. SPEC_FIDELITY_GATE is retained only for legacy/non-convergence mode.

**Why**: Solution B resolves the dual authority conflict by elimination rather than alignment. It scores 9.4/10 vs Solution A's 6.7/10 across conflict resolution completeness (40%), backward compatibility (30%), and implementation simplicity (30%). The key insight is that aligning two authorities (Solution A) preserves a coupling that can drift, while eliminating the second authority (Solution B) removes the coupling entirely. Legacy mode is preserved byte-identical for NFR-7 compliance.

## Architecture Design Change

### Section 5.1 -- Replace the step 8 code block with:

```python
# Step 8 construction is mode-dependent.
#
# Convergence mode (default when v3.05+ modules are present):
#   The convergence engine (convergence.py) replaces step 8 internals.
#   Pass/fail is determined by registry.get_active_high_count() == 0.
#   SPEC_FIDELITY_GATE is NOT used. spec-fidelity.md is written as a
#   human-readable summary artifact but is not gated.
#
# Legacy mode (convergence_enabled=false):
#   Original LLM-based fidelity check with SPEC_FIDELITY_GATE.
#   Behavior is byte-identical to pre-v3.05 pipeline.

if config.convergence_enabled:
    Step(
        id="spec-fidelity",
        prompt=None,
        output_file=spec_fidelity_file,
        gate=None,
        timeout_seconds=600,
        inputs=[config.spec_file, merge_file],
        retry_limit=0,
    )
else:
    Step(
        id="spec-fidelity",
        prompt=build_spec_fidelity_prompt(config.spec_file, merge_file),
        output_file=spec_fidelity_file,
        gate=SPEC_FIDELITY_GATE,
        timeout_seconds=600,
        inputs=[config.spec_file, merge_file],
        retry_limit=1,
    )
```

### Section 5.3 -- Replace existing text entirely with:

```
### 5.3 Gate Authority Model

In **convergence mode** (default), SPEC_FIDELITY_GATE is not invoked for step 8.
The convergence engine (Sec 4.5, `convergence.py`) evaluates pass/fail exclusively
via `registry.get_active_high_count() == 0`. The spec-fidelity.md file is still
written as a human-readable summary artifact containing the registry's current
view, but it is not gated. This eliminates the dual-authority conflict between
the registry and the gate.

In **legacy mode** (`convergence_enabled=false`), SPEC_FIDELITY_GATE operates
exactly as in pre-v3.05 releases, validating the LLM-generated spec-fidelity.md
report frontmatter. This mode exists for backward compatibility and will be
deprecated when the convergence engine is proven stable.

**Design Principle #3 compliance**: The convergence gate reads the deviation
registry, never raw scan output. SPEC_FIDELITY_GATE reads raw scan output but
is never active in convergence mode. The two authorities never coexist in the
same execution mode.
```

### Section 1 (Design Principles) -- Amend Principle #3:

Replace:
```
3. **Registry-centric gate**: The convergence gate reads the deviation registry, never raw scan output.
```

With:
```
3. **Registry-centric gate**: The convergence gate reads the deviation registry, never raw scan output. SPEC_FIDELITY_GATE is excluded from convergence mode to prevent dual-authority conflicts (see Sec 5.3).
```

## Code Change Specification

### `executor.py`

1. **Import**: No change. SPEC_FIDELITY_GATE import stays (needed for legacy mode).

2. **`_build_steps()` method** (around line 496-505): Replace the unconditional Step 8 construction with a conditional:

```python
# Step 8: Spec Fidelity
if getattr(config, 'convergence_enabled', False):
    # Convergence mode: engine handles pass/fail via registry
    steps.append(Step(
        id="spec-fidelity",
        prompt=None,
        output_file=spec_fidelity_file,
        gate=None,
        timeout_seconds=600,
        inputs=[config.spec_file, merge_file],
        retry_limit=0,
    ))
else:
    # Legacy mode: LLM-based check with SPEC_FIDELITY_GATE
    steps.append(Step(
        id="spec-fidelity",
        prompt=build_spec_fidelity_prompt(config.spec_file, merge_file),
        output_file=spec_fidelity_file,
        gate=SPEC_FIDELITY_GATE,
        timeout_seconds=600,
        inputs=[config.spec_file, merge_file],
        retry_limit=1,
    ))
```

3. **Step runner (`roadmap_run_step`)**: When `step.prompt is None` and `step.gate is None`, the step runner delegates to the convergence engine rather than spawning a Claude subprocess. The convergence engine writes spec-fidelity.md and returns a StepResult with pass/fail based on registry state.

### `gates.py`

No changes. SPEC_FIDELITY_GATE definition (lines 806-829) remains as-is for legacy mode.

### `convergence.py` (new, per architecture Sec 4.5)

The `execute_fidelity_with_convergence()` function is the sole evaluator in convergence mode:

```python
def execute_fidelity_with_convergence(...) -> ConvergenceResult:
    # ... (as specified in architecture Sec 4.5)
    # Gate evaluation is INTERNAL:
    if registry.get_active_high_count() == 0:
        return ConvergenceResult(passed=True, ...)
    # ... convergence loop continues
```

No reference to SPEC_FIDELITY_GATE anywhere in this module.

### `models.py` (RoadmapConfig)

Add field:

```python
convergence_enabled: bool = False  # Default False until v3.05 ships; set True in v3.05
```

## Authority Model

```
CONVERGENCE MODE (convergence_enabled=true)
  Sole authority: DeviationRegistry
  Pass condition: registry.get_active_high_count() == 0
  SPEC_FIDELITY_GATE: NOT INVOKED
  spec-fidelity.md: Written as informational artifact, ungated

LEGACY MODE (convergence_enabled=false)
  Sole authority: SPEC_FIDELITY_GATE
  Pass condition: high_severity_count == 0 in spec-fidelity.md frontmatter
  DeviationRegistry: DOES NOT EXIST
  spec-fidelity.md: LLM-generated, gated

INVARIANT: At no point do both authorities coexist in the same execution.
The dual-authority conflict is resolved by mutual exclusion, not alignment.
```

## Validation

### V1: No dual authority in convergence mode
- Set `convergence_enabled=true`
- Verify step 8 is constructed with `gate=None`
- Verify convergence engine calls `registry.get_active_high_count()` for pass/fail
- Verify SPEC_FIDELITY_GATE is never invoked

### V2: Legacy mode unchanged
- Set `convergence_enabled=false`
- Verify step 8 is constructed with `gate=SPEC_FIDELITY_GATE`
- Verify `build_spec_fidelity_prompt` is called
- Verify behavior is byte-identical to pre-v3.05

### V3: False positive scenario eliminated
- Create a registry with 0 active HIGHs (all debated down)
- Run convergence mode
- Verify pipeline PASSES (previously would fail due to stale spec-fidelity.md)

### V4: Design Principle #3 compliance
- Grep convergence.py for any reference to SPEC_FIDELITY_GATE or spec-fidelity.md frontmatter parsing
- Verify zero matches: convergence engine reads only the registry

### V5: NFR-7 backward compatibility
- Run full pipeline with `convergence_enabled=false`
- Diff output against pre-v3.05 baseline
- Steps 1-7 output must be identical
- Step 8 output must be identical (same gate, same prompt, same LLM behavior)

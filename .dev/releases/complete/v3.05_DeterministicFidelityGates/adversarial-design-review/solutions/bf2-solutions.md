# BF-2 Solutions: Dual Authority Conflict — Registry vs SPEC_FIDELITY_GATE

## Problem Statement

Architecture Design Principle #3 states: "Registry-centric gate: The convergence gate reads the deviation registry, never raw scan output." However, Section 5.3 retains SPEC_FIDELITY_GATE for "per-run report validation." This creates a dual-authority conflict:

1. The DeviationRegistry (Sec 4.4) tracks findings with status lifecycle (ACTIVE/FIXED/FAILED/SKIPPED) and adversarial debate verdicts that can downgrade HIGH findings.
2. SPEC_FIDELITY_GATE (gates.py:806) reads `high_severity_count` from spec-fidelity.md frontmatter -- a raw scan output artifact that does not reflect registry state.

**Failure scenario**: Registry shows 0 active HIGHs (all debated down or FIXED), but spec-fidelity.md still reports `high_severity_count: 3` from the raw scan. SPEC_FIDELITY_GATE fails. Pipeline halts on a false positive.

---

## Solution A: Generate spec-fidelity.md FROM Registry State

### Description

Replace the current LLM-generated spec-fidelity.md with a report generated deterministically from DeviationRegistry state. The report's frontmatter is computed from `registry.get_active_high_count()` and friends, ensuring it is always consistent with the registry. SPEC_FIDELITY_GATE continues to validate the report structure but can never contradict the registry because the report IS the registry's view.

### Architecture Changes

**Section 5.1** -- Add after the convergence call:

```python
# After convergence engine completes, generate spec-fidelity.md from registry
from .deviation_registry import generate_fidelity_report

generate_fidelity_report(
    registry=registry,
    output_path=spec_fidelity_file,
    spec_path=config.spec_file,
    roadmap_path=out / "roadmap.md",
)
```

**Section 5.3** -- Replace existing text with:

```
SPEC_FIDELITY_GATE validates the structure of spec-fidelity.md (required fields,
min_lines, consistency checks). The report is generated from DeviationRegistry
state, not raw scan output. This guarantees SPEC_FIDELITY_GATE and the registry
always agree on active HIGH count.

Authority chain: DeviationRegistry -> spec-fidelity.md -> SPEC_FIDELITY_GATE
```

**New function in `deviation_registry.py`**:

```python
def generate_fidelity_report(
    registry: DeviationRegistry,
    output_path: Path,
    spec_path: Path,
    roadmap_path: Path,
) -> None:
    """Generate spec-fidelity.md from registry state.

    Frontmatter fields are computed directly from registry:
      high_severity_count = registry.get_active_high_count()
      medium_severity_count = len([f for f in active if f.severity == "MEDIUM"])
      low_severity_count = len([f for f in active if f.severity == "LOW"])
      total_deviations = sum of above
      validation_complete = true (always, since convergence finished)
      tasklist_ready = (high_severity_count == 0)

    Body contains a per-finding table with stable_id, dimension, severity,
    status, and debate verdict (if any).
    """
```

**Changes to `executor.py`**:

Step 8 keeps `gate=SPEC_FIDELITY_GATE` but the prompt changes from `build_spec_fidelity_prompt` to a no-op or the convergence engine handles output generation. The Step's output_file is written by `generate_fidelity_report`, not by a Claude subprocess.

### Analysis

| Criterion | Assessment |
|-----------|------------|
| NFR-7 (backward compat steps 1-7) | FULLY MAINTAINED. Steps 1-7 untouched. Step 8 output file and gate remain; only the content source changes. |
| Dual authority resolved? | YES. Single authority chain: Registry -> Report -> Gate. No independent data paths. |
| Implementation complexity | MODERATE. Requires new `generate_fidelity_report()` function (~80 LOC). Step 8 prompt construction changes. Gate definition unchanged. |
| Regression risk | LOW-MODERATE. The spec-fidelity.md format changes from LLM prose to structured registry dump. Downstream consumers of spec-fidelity.md (step 9 wiring-verification uses it as input) must accept the new format. |

### Advantages
- SPEC_FIDELITY_GATE remains as a structural validation layer (catches corrupted reports).
- spec-fidelity.md artifact still exists for human review and auditability.
- Minimal changes to gate definitions in gates.py.

### Disadvantages
- Adds an indirection layer: registry -> report -> gate, when the registry alone could serve.
- Report generation function must be kept in sync with SPEC_FIDELITY_GATE's expected fields.
- The "per-run report validation" purpose of SPEC_FIDELITY_GATE becomes tautological (the report is always valid by construction).

---

## Solution B: Remove SPEC_FIDELITY_GATE from Convergence Flow

### Description

The convergence engine evaluates pass/fail exclusively via `registry.get_active_high_count() == 0`. SPEC_FIDELITY_GATE is removed from step 8 in convergence mode. It is retained only for legacy/non-convergence mode (when the pipeline runs without the new deterministic fidelity system).

### Architecture Changes

**Section 5.1** -- Step 8 construction becomes mode-dependent:

```python
if config.convergence_enabled:
    # Step 8 runs the convergence engine; no SPEC_FIDELITY_GATE
    Step(
        id="spec-fidelity",
        prompt=None,  # No LLM prompt; convergence engine handles internally
        output_file=spec_fidelity_file,
        gate=None,  # Gate evaluation is internal to convergence engine
        timeout_seconds=600,
        inputs=[config.spec_file, merge_file],
        retry_limit=0,
    )
else:
    # Legacy mode: original LLM-based fidelity check with gate
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

**Section 5.3** -- Replace existing text with:

```
In convergence mode, SPEC_FIDELITY_GATE is not used. The convergence engine
(convergence.py) reads the DeviationRegistry directly for pass/fail evaluation
via `registry.get_active_high_count() == 0`. The spec-fidelity.md file is still
written as a human-readable summary but is NOT gated.

In legacy mode (convergence_enabled=false), SPEC_FIDELITY_GATE operates as
before, validating the LLM-generated spec-fidelity.md report.

Authority: DeviationRegistry is the sole authority for convergence pass/fail.
SPEC_FIDELITY_GATE is a legacy artifact retained for backward compatibility.
```

**Changes to `executor.py`**:

- Add `convergence_enabled` flag to `RoadmapConfig` (default: `True` once v3.05 ships).
- Step 8 construction branches on this flag.
- In convergence mode, the step runner invokes `execute_fidelity_with_convergence()` instead of spawning a Claude subprocess.

**Changes to `gates.py`**:

- No changes. SPEC_FIDELITY_GATE definition stays as-is for legacy mode.

### Analysis

| Criterion | Assessment |
|-----------|------------|
| NFR-7 (backward compat steps 1-7) | FULLY MAINTAINED. Steps 1-7 untouched. Legacy mode preserves exact current behavior. |
| Dual authority resolved? | YES, completely. In convergence mode, there is exactly one authority (registry). In legacy mode, there is exactly one authority (SPEC_FIDELITY_GATE). No mode has two authorities. |
| Implementation complexity | LOW. Conditional step construction (~15 LOC). `convergence_enabled` flag in config (~5 LOC). No new functions needed beyond what's already planned. |
| Regression risk | LOW. Legacy mode is byte-identical to current behavior. Convergence mode is entirely new code that doesn't touch existing gate machinery. |

### Advantages
- Cleanest resolution: eliminates the dual authority entirely rather than papering over it.
- No tautological validation (gate checking a report it knows will pass).
- Simpler mental model: convergence mode = registry authority, legacy mode = gate authority.
- Less code to maintain.

### Disadvantages
- spec-fidelity.md in convergence mode is ungated; a bug in report generation won't be caught by SPEC_FIDELITY_GATE.
- Two code paths (convergence vs legacy) in step 8 construction.
- If `convergence_enabled` flag is misconfigured, user could accidentally run legacy mode.

---

## Adversarial Comparison

### Round 1: Conflict Resolution Completeness (Weight 40%)

**Solution A** resolves the conflict by making the report a projection of the registry. The authority chain is linear (Registry -> Report -> Gate), but it introduces a coupling: the report format must match SPEC_FIDELITY_GATE's expectations. If someone adds a new gate check without updating `generate_fidelity_report`, the conflict resurfaces in a subtler form.

**Solution B** resolves the conflict by elimination. In convergence mode, there is one authority, period. There is no coupling between gate checks and report format because the gate is not invoked.

**Winner: Solution B** -- elimination is stronger than alignment.

### Round 2: Backward Compatibility (Weight 30%)

**Solution A** keeps SPEC_FIDELITY_GATE active in all modes. The gate validates the same fields. Consumers of spec-fidelity.md get a file in a compatible format. However, the content changes from LLM prose to structured registry dump, which could break downstream tools expecting specific prose patterns.

**Solution B** preserves the legacy path byte-identical. The `convergence_enabled=false` path runs exactly the current code. Only the new convergence path changes behavior, and that path is entirely new code that has no existing consumers.

**Winner: Solution B** -- byte-identical legacy preservation is stronger than format-compatible changes.

### Round 3: Implementation Simplicity (Weight 30%)

**Solution A** requires: new `generate_fidelity_report()` function (~80 LOC), modification of step 8 prompt construction, testing that generated report satisfies SPEC_FIDELITY_GATE, keeping report format and gate checks in sync.

**Solution B** requires: conditional in `_build_steps` (~15 LOC), `convergence_enabled` flag in config (~5 LOC), no new functions beyond already-planned convergence engine.

**Winner: Solution B** -- significantly less new code and no sync obligations.

### Final Score

| Criterion | Weight | Solution A | Solution B |
|-----------|--------|-----------|-----------|
| Conflict resolution | 40% | 7/10 | 10/10 |
| Backward compatibility | 30% | 7/10 | 9/10 |
| Implementation simplicity | 30% | 6/10 | 9/10 |
| **Weighted total** | | **6.7** | **9.4** |

### Winner: Solution B

Solution B wins decisively. It resolves the dual authority conflict by elimination rather than alignment, preserves legacy behavior byte-identically, and requires the least new code.

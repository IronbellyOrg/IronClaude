# ISS-013 Refactoring Proposals

**Issue**: SPEC_FIDELITY_GATE + wiring step ordering semantics undocumented when `convergence_enabled=true`.

**Source**: Compatibility Report Section 7d (Architectural Tensions)

**Root Cause Analysis**:

The pipeline executes steps 1-9 in fixed order:
```
1. extract -> 2. generate-* -> 3. diff -> 4. debate -> 5. score ->
6. merge -> 7. test-strategy -> 8. spec-fidelity -> 9. wiring-verification
```

Step 8 (spec-fidelity) is defined in `executor.py:516-525` with:
```python
gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE
```

Step 9 (wiring-verification) is defined in `executor.py:527-538` with:
```python
inputs=[merge_file, spec_fidelity_file],
gate=WIRING_GATE,
gate_mode=GateMode.TRAILING,
```

Three ordering semantics are undocumented:

1. **Step 9 lists `spec_fidelity_file` as an input** (executor.py:535), implying a data dependency on step 8's output. When `convergence_enabled=true`, step 8 still runs (gate=None means "no gate check", not "skip step") and still produces `spec-fidelity.md`. But this relationship is not documented in the spec.

2. **Step 9 bypasses input embedding entirely** (executor.py:244-259). The `wiring-verification` step has a special code path that calls `run_wiring_analysis()` directly, returning before `_embed_inputs(step.inputs)` is reached. The `inputs` list is therefore decorative for step 9 -- it has no runtime effect. The spec does not acknowledge this.

3. **In convergence mode, step 8 runs ungated then step 9 runs with WIRING_GATE**. The spec's FR-7 Gate Authority Model says "SPEC_FIDELITY_GATE is NOT invoked" and "spec-fidelity.md report is still written as a human-readable summary but is not gated." It does not address what happens to step 9 or whether step 9's execution is affected.

**Overlap Check**: ISS-012 (convergence loop vs linear pipeline) is related but distinct. ISS-012 addresses the tension of a convergence loop within a linear pipeline. ISS-013 addresses the specific step 8->9 ordering semantics when step 8's gate is None. No existing CRITICAL or HIGH proposals resolve ISS-013.

---

## Proposal #1: Add Step Ordering Subsection to FR-7 Gate Authority Model (RECOMMENDED)

**Rationale**: The most natural location for this documentation is within FR-7's Gate Authority Model, which already discusses the SPEC_FIDELITY_GATE bypass. A new subsection clarifies the downstream effect on step 9 without restructuring the spec.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Location**: After the Gate Authority Model paragraph (currently ending at line 364, before Acceptance Criteria)

**BEFORE** (lines 347-354):
```
**Gate Authority Model**: In convergence mode (`convergence_enabled=true`),
the convergence engine is the **sole authority** for pass/fail, evaluating
only the DeviationRegistry (`registry.get_active_high_count() == 0`). The
existing `SPEC_FIDELITY_GATE` is NOT invoked. The `spec-fidelity.md` report
is still written as a human-readable summary but is not gated.

In legacy mode (`convergence_enabled=false`), `SPEC_FIDELITY_GATE` operates
exactly as in pre-v3.05, validating the LLM-generated report frontmatter.
The two authorities never coexist in the same execution mode.
```

**AFTER**:
```
**Gate Authority Model**: In convergence mode (`convergence_enabled=true`),
the convergence engine is the **sole authority** for pass/fail, evaluating
only the DeviationRegistry (`registry.get_active_high_count() == 0`). The
existing `SPEC_FIDELITY_GATE` is NOT invoked. The `spec-fidelity.md` report
is still written as a human-readable summary but is not gated.

In legacy mode (`convergence_enabled=false`), `SPEC_FIDELITY_GATE` operates
exactly as in pre-v3.05, validating the LLM-generated report frontmatter.
The two authorities never coexist in the same execution mode.

**Step Ordering: spec-fidelity (Step 8) and wiring-verification (Step 9)**:

In both modes, pipeline step ordering is preserved: step 8 (spec-fidelity)
runs before step 9 (wiring-verification). The key differences by mode:

| Aspect | Legacy Mode | Convergence Mode |
|--------|------------|------------------|
| Step 8 gate | `SPEC_FIDELITY_GATE` (blocks on HIGH count) | `None` (no gate; step runs, output written, no pass/fail check) |
| Step 8 output | `spec-fidelity.md` (gated) | `spec-fidelity.md` (human-readable summary, not gated) |
| Step 9 execution | Runs after step 8 passes gate | Runs unconditionally after step 8 completes |
| Step 9 gate | `WIRING_GATE` (trailing mode) | `WIRING_GATE` (trailing mode, unchanged) |
| Step 9 data dependency on step 8 | None at runtime: wiring-verification bypasses input embedding and runs static analysis directly via `run_wiring_analysis()` | Same: no runtime dependency |

Step 9 declares `spec_fidelity_file` in its `inputs` list for pipeline
graph completeness (dataflow tracking, resume logic), but the wiring-
verification step bypasses the standard `_embed_inputs()` path and invokes
`run_wiring_analysis()` directly. Convergence mode therefore has no effect
on step 9's behavior or output.
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-7, Gate Authority Model section only)

### Risk: **LOW**
Additive text. No acceptance criteria change. No change to any other FR. The table makes the two-mode behavior explicit and machine-scannable.

### Requires Code Changes: **No**
The code already implements this behavior correctly. This is a documentation-only gap.

---

## Proposal #2: Add Wiring Step Invariant to FR-7 Acceptance Criteria

**Rationale**: Instead of (or in addition to) prose documentation, encode the step ordering invariant as a testable acceptance criterion. This ensures the relationship is not just documented but verified.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Location**: FR-7 Acceptance Criteria (lines 354-365)

**BEFORE** (end of acceptance criteria, line 365):
```
- [ ] `convergence_enabled: bool = False` field on pipeline config (default preserves legacy behavior)
```

**AFTER** (append three new criteria):
```
- [ ] `convergence_enabled: bool = False` field on pipeline config (default preserves legacy behavior)
- [ ] Wiring-verification (step 9) executes identically in both modes: `WIRING_GATE` evaluation, `run_wiring_analysis()` direct invocation, trailing gate mode
- [ ] Step 8 output (`spec-fidelity.md`) is always written regardless of mode; step 9 has no runtime dependency on step 8 output content
- [ ] When `convergence_enabled=true`, step 8 runs with `gate=None` (no gate evaluation), then step 9 runs with `gate=WIRING_GATE` (trailing); pipeline does not short-circuit between steps 8 and 9
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (FR-7 Acceptance Criteria only)

### Risk: **LOW**
Three additive acceptance criteria. No existing criteria change. Each criterion is directly testable against `executor.py:516-538`.

### Requires Code Changes: **No**
The code already satisfies all three criteria. These are verification-only additions.

---

## Proposal #3: Add Cross-Reference Note in Appendix A Pipeline Diagram

**Rationale**: The "Proposed (to-be)" architecture diagram in Appendix A (lines 587-599) describes the convergence flow but does not show how steps 8 and 9 interact in convergence mode. Adding an annotation makes the diagram self-documenting.

### Spec Text Change

**File**: `deterministic-fidelity-gate-requirements.md`

**Location**: Appendix A, after the "Proposed (to-be)" diagram (line 599)

**BEFORE** (line 599):
```
    → Fail + budget exhausted: halt with diagnostic report
```
```

**AFTER**:
```
    → Fail + budget exhausted: halt with diagnostic report

Step ordering note (convergence mode):
  Step 8 (spec-fidelity): runs with gate=None; produces spec-fidelity.md
    as human-readable summary (not gated, not authority for pass/fail)
  Step 9 (wiring-verification): runs unchanged from legacy mode;
    WIRING_GATE in trailing mode; no data dependency on step 8 output
    (wiring step bypasses input embedding, calls run_wiring_analysis() directly)
```

### Files Affected
- `deterministic-fidelity-gate-requirements.md` (Appendix A only)

### Risk: **VERY LOW**
Appendix annotation only. Zero impact on normative spec text. However, this alone is insufficient -- Appendix notes are informational and not binding. Should be combined with Proposal #1 or #2 for normative coverage.

### Requires Code Changes: **No**

---

## Summary Comparison

| # | Proposal | Location | Type | Self-Contained | Testable | Risk |
|---|----------|----------|------|----------------|----------|------|
| 1 | Gate Authority Model subsection | FR-7 body | Normative prose + table | Yes | No (descriptive) | LOW |
| 2 | Acceptance criteria additions | FR-7 AC list | Normative, testable | Partial (needs context) | Yes | LOW |
| 3 | Appendix A annotation | Appendix A | Informational | Yes | No | VERY LOW (insufficient alone) |

**Recommendation**: Combine **#1 + #2**. Proposal #1 provides the complete explanation of why convergence mode does not affect step 9, including the technical detail about `_embed_inputs()` bypass. Proposal #2 encodes the invariant as testable acceptance criteria so it cannot regress. Proposal #3 is optional polish.

The combined change adds approximately 25 lines of spec text (one subsection with table + three acceptance criteria), touches only FR-7, and requires zero code changes. The code at `executor.py:244-259` and `executor.py:516-538` already implements the documented behavior correctly.

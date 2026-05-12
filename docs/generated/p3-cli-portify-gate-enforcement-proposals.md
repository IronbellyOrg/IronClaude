---
title: "P3: cli_portify Gate Enforcement — Two Proposals"
date: 2026-03-25
status: draft
context: cli-unwired-components-audit recommended action
---

# P3: Wire cli_portify Gate Enforcement

## Problem Statement

The cli_portify executor (`src/superclaude/cli/cli_portify/executor.py:500-511`) calls `get_gate_criteria()` for logging only ("lightweight consultation"). It never calls `gate_passed()`, never instantiates `GateFailure`, and never enforces gate criteria. The entire `GATE_REGISTRY` + 10 `gate_*()` functions + `GateFailure` type form a complete but disconnected abstraction.

### Key Constraints
- `step_runner` is an active test seam used by 7+ tests — must not be removed
- `DiagnosticsCollector` already accepts `GateFailure` instances (diagnostics.py:62-67)
- STRICT-tier gates with semantic checks exist (e.g., ANALYZE_WORKFLOW_GATE requires >=5 sections)
- Enabling enforcement naively would halt pipelines on borderline artifacts
- Sprint executor already has a graduated rollout pattern via `SprintGatePolicy`

---

## Proposal A: Shadow-First Graduated Enforcement

### Approach
Mirror the sprint executor's `SprintGatePolicy` pattern. Add a `PortifyGatePolicy` that supports three enforcement modes — `shadow`, `soft`, `full` — defaulting to `shadow`. Gate results are always evaluated but only block execution in `full` mode.

### Implementation Sketch

1. **Add `PortifyGatePolicy`** to `cli_portify/executor.py`:
   - Accepts `gate_mode: Literal["shadow", "soft", "full"] = "shadow"`
   - `evaluate(step_id, output_file) -> GateEvaluation` — calls `get_gate_criteria()` then `gate_passed()`
   - Shadow: log result, never block
   - Soft: log + warn on failure, never block
   - Full: log + block on failure, instantiate `GateFailure`, feed to `DiagnosticsCollector`

2. **Wire into `_execute_step()`** at line ~500, replacing the current lightweight consultation block:
   ```python
   gate_eval = self._gate_policy.evaluate(step.step_id, step.output_file)
   self._execution_log.gate_eval(step.step_id, gate_id=gate_eval.gate_id, tier=gate_eval.tier)
   if gate_eval.blocked:
       self._diagnostics.record_gate_failure(gate_eval.failure)
       return PortifyStatus.HALT
   ```

3. **Expose `--gate-mode` CLI flag** in portify command, defaulting to `shadow`.

4. **Graduation criteria**: `shadow` passes >= 90% over 3+ runs before promoting to `soft`, then `full`.

### Risks Mitigated
- No pipeline breakage: shadow mode is non-blocking by default
- Existing tests unaffected: `step_runner` path bypasses gate evaluation
- Diagnostics integration is zero-effort (already built)

### Risks Remaining
- Graduation is manual — someone must promote the mode
- Shadow mode produces log noise with no enforcement value until promoted

---

## Proposal B: Inline Enforcement with Per-Gate Opt-In

### Approach
Instead of a global mode switch, make each `GateCriteria` in `GATE_REGISTRY` carry an `enforce: bool` field. Start with all gates set to `enforce=False`. Enable enforcement per-gate as confidence grows. This is finer-grained than a global mode and allows EXEMPT/LIGHT gates to be enforced immediately while STRICT gates remain advisory.

### Implementation Sketch

1. **Extend `GateCriteria` model** in `pipeline/models.py`:
   - Add `enforce: bool = False` field

2. **Update `GATE_REGISTRY`** entries in `cli_portify/gates.py`:
   - Set `enforce=True` for EXEMPT and LIGHT tier gates immediately
   - Leave STANDARD and STRICT as `enforce=False`

3. **Replace consultation block** in `executor.py:500-511`:
   ```python
   try:
       gate = get_gate_criteria(step.step_id)
       if gate.enforce:
           passed, reason = gate_passed(step.output_file, gate)
           if not passed:
               failure = GateFailure(gate_id=step.step_id, check_name="gate_passed",
                                     diagnostic=reason or "", artifact_path=str(step.output_file))
               self._diagnostics.record_gate_failure(failure)
               return PortifyStatus.HALT
   except KeyError:
       pass  # No gate registered for this step
   ```

4. **No CLI flag needed** — enforcement is controlled at the gate definition level.

### Risks Mitigated
- Granular control: low-risk gates enforced immediately, high-risk gates deferred
- No global mode to manage or graduate
- Simpler implementation (no policy class)

### Risks Remaining
- Modifying `GateCriteria` in `pipeline/models.py` affects all pipelines (roadmap, cleanup_audit, sprint), not just cli_portify — must ensure `enforce` defaults to current behavior (`False` or ignored) for other consumers
- Per-gate opt-in decisions are scattered across gate definitions, harder to audit than a single mode flag
- No soft/warn mode — gates are either enforced or silent
